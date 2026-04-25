/**
 * Docsig IntelliJ Plugin
 *
 * Integrates the Docsig CLI into IntelliJ as a background inspection.
 *
 * High-level architecture:
 *
 * - DocsigInspection → entry point from IntelliJ inspection system
 * - DocsigService → orchestration (cache, debounce, diffing, scheduling)
 * - DocsigRunner → executes external CLI + parses JSON
 * - DocsigSettings → persistent configuration (CLI path)
 *
 * Execution flow:
 * 1. IntelliJ visits a file via LocalInspectionTool
 * 2. Cached issues are returned immediately (fast, non-blocking)
 * 3. Service decides if the file is stale
 * 4. If stale → schedules background CLI execution (debounced)
 * 5. Results are merged with cache (partial invalidation)
 * 6. IntelliJ highlighting is refreshed
 *
 * Performance strategy:
 * - Avoid running CLI on every keystroke
 * - Use text + PSI diffing to limit invalidation scope
 * - Reuse existing issues where possible
 * - Always keep UI thread non-blocking
 */

package com.github.jshwi.docsig

import com.fasterxml.jackson.core.JsonProcessingException
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.intellij.codeInsight.daemon.DaemonCodeAnalyzer
import com.intellij.codeInspection.LocalInspectionTool
import com.intellij.codeInspection.ProblemHighlightType
import com.intellij.codeInspection.ProblemsHolder
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.openapi.components.service
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.editor.Document
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.fileEditor.FileDocumentManagerListener
import com.intellij.openapi.options.Configurable
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.LocalFileSystem
import com.intellij.psi.PsiDocumentManager
import com.intellij.psi.PsiElement
import com.intellij.psi.PsiElementVisitor
import com.intellij.psi.PsiFile
import com.intellij.psi.PsiManager
import com.intellij.util.Alarm
import java.util.concurrent.ConcurrentHashMap
import javax.swing.BoxLayout
import javax.swing.JComponent
import javax.swing.JLabel
import javax.swing.JPanel
import javax.swing.JTextField

private const val DEBOUNCE_MS = 600L

class DocsigSaveListener : FileDocumentManagerListener {
    private val service =
        ApplicationManager.getApplication()
            .getService(DocsigService::class.java)

    override fun beforeDocumentSaving(document: Document) {
        val file =
            FileDocumentManager
                .getInstance()
                .getFile(document)
                ?: return

        if (!file.isInLocalFileSystem) return

        service.scheduleFromSave(file.path)
    }
}

/**
 * Represents a single issue emitted by the Docsig CLI.
 *
 * This structure must match the JSON output of Docsig exactly.
 *
 * @property file absolute file path associated with the issue
 * @property line 1-based line number (Docsig convention)
 * @property column optional column (currently unused)
 * @property message human-readable issue description
 * @property severity severity string from Docsig
 */
data class DocsigIssue(
    val file: String,
    val line: Int,
    val column: Int?,
    val message: String,
    val severity: String,
)

/**
 * Resolve a PSI element corresponding to a given line.
 *
 * IntelliJ highlights PSI elements rather than raw line numbers,
 * so we translate:
 *
 *   line → offset → PSI element
 *
 * Strategy:
 * - Try the start of the line
 * - Fallback to the end of the line
 *
 * @param file PSI file to inspect
 * @param line zero-based line index
 * @return PSI element at that line, or null if unavailable
 */
fun getElementAtLine(
    file: PsiFile,
    line: Int,
): PsiElement? {
    val document =
        PsiDocumentManager.getInstance(file.project).getDocument(file)
            ?: return null

    if (line < 0 || line >= document.lineCount) return null

    return file.findElementAt(document.getLineStartOffset(line))
        ?: file.findElementAt(document.getLineEndOffset(line))
}

/**
 * Persistent application-level settings.
 *
 * Stores configuration shared across all projects.
 *
 * Currently only:
 * - Docsig CLI executable path
 */
@Service
@State(name = "DocsigSettings", storages = [Storage("docsig.xml")])
class DocsigSettings : PersistentStateComponent<DocsigSettings.State> {
    /**
     * Serializable state container.
     *
     * @property cliPath path to Docsig executable
     */
    data class State(var cliPath: String = "docsig")

    /** Backing state instance persisted by IntelliJ */
    private var state = State()

    /**
     * @return current persisted state
     */
    override fun getState(): State = state

    /**
     * Replace in-memory state with persisted state.
     *
     * @param state loaded state
     */
    override fun loadState(state: State) {
        this.state = state
    }

    /**
     * Public accessor for CLI path.
     */
    var cliPath: String
        get() = state.cliPath
        set(value) {
            state.cliPath = value
        }

    companion object {
        /**
         * Retrieve singleton instance via IntelliJ service container.
         *
         * @return DocsigSettings instance
         */
        fun getInstance(): DocsigSettings = service()
    }
}

/**
 * IntelliJ Settings UI for Docsig configuration.
 *
 * Provides a simple text field to edit CLI path.
 */
class DocsigConfigurable : Configurable {
    /** Input field for CLI path */
    private val field = JTextField()

    override fun getDisplayName(): String = "Docsig"

    /**
     * Build settings UI component.
     *
     * @return root Swing component
     */
    override fun createComponent(): JComponent {
        val panel = JPanel()
        panel.layout = BoxLayout(panel, BoxLayout.Y_AXIS)
        panel.add(JLabel("Docsig CLI path:"))
        panel.add(field)
        return panel
    }

    /**
     * Determine if UI state differs from persisted state.
     *
     * @return true if modified
     */
    override fun isModified(): Boolean =
        field.text != DocsigSettings.getInstance().cliPath

    /**
     * Persist UI changes.
     */
    override fun apply() {
        DocsigSettings.getInstance().cliPath = field.text
    }

    /**
     * Reset UI to persisted values.
     */
    override fun reset() {
        field.text = DocsigSettings.getInstance().cliPath
    }
}

/**
 * Executes Docsig CLI and parses output.
 *
 * Responsibilities:
 * - Spawn process
 * - Read stdout
 * - Parse JSON
 *
 * Stateless and safe for reuse.
 */
object DocsigRunner {
    private val log = Logger.getInstance(DocsigRunner::class.java)
    private val mapper = jacksonObjectMapper()

    /**
     * Process factory for testability.
     */
    var processFactory: (List<String>) -> Process = { cmd ->
        val builder = ProcessBuilder(cmd)
        builder.environment()["DOCSIG_FORMAT_JSON"] = "true"
        builder.redirectErrorStream(true).start()
    }

    /**
     * Run Docsig CLI against a file.
     *
     * @param path absolute file path
     * @return parsed issues (empty on failure)
     */
    fun run(path: String): List<DocsigIssue> {
        val exe = DocsigSettings.getInstance().cliPath

        val process = processFactory(listOf(exe, path))

        val output =
            process.inputStream.bufferedReader(Charsets.UTF_8).use {
                it.readText().trim()
            }

        val exit = process.waitFor()

        log.debug("docsig exit=$exit path=$path size=${output.length}")

        return try {
            mapper.readValue(output)
        } catch (e: JsonProcessingException) {
            log.warn("parse failed path=$path", e)
            emptyList()
        }
    }
}

/**
 * Core orchestration service (project-scoped).
 *
 * Handles:
 * - caching
 * - change detection
 * - debounce scheduling
 * - merging results
 * - triggering UI updates
 */
@Service(Service.Level.PROJECT)
class DocsigService(private val project: Project) {
    private val log = Logger.getInstance(DocsigService::class.java)

    /** Cached issues per file */
    private val cache = ConcurrentHashMap<String, List<DocsigIssue>>()

    /** Tracks currently running executions */
    private val inFlight = ConcurrentHashMap.newKeySet<String>()

    /** Debounce schedulers per file */
    private val alarms = ConcurrentHashMap<String, Alarm>()

    private val idleAlarms = ConcurrentHashMap<String, Alarm>()

    /**
     * Retrieve cached issues.
     *
     * @param path file path
     * @return cached issues or empty list
     */
    fun getIssues(path: String): List<DocsigIssue> = cache[path] ?: emptyList()

    /**
     * Ensure file has fresh Docsig results.
     *
     * Uses PSI-aware diffing to minimize recomputation.
     *
     * @param file PSI file
     */
    fun ensureFresh(file: PsiFile) {
        val vFile = file.virtualFile ?: return
        if (!vFile.isInLocalFileSystem) return

        val path = vFile.path

        // instead of diffing or hashing per edit:
        scheduleIdle(path)
    }

    /**
     * Schedule debounced execution.
     *
     * @param path file path
     */
    @Suppress("UnstableApiUsage")
    private fun schedule(path: String) {
        val alarm =

            alarms.computeIfAbsent(path) {
                Alarm(Alarm.ThreadToUse.POOLED_THREAD, project)
            }

        alarm.cancelAllRequests()

        alarm.addRequest(
            { runDocsig(path) },
            DEBOUNCE_MS,
        )
    }

    /**
     * Execute Docsig and merge results.
     *
     * @param path file path
     */
    private fun runDocsig(path: String) {
        if (!inFlight.add(path)) return

        ApplicationManager.getApplication().executeOnPooledThread {
            try {
                val issues = DocsigRunner.run(path)
                cache[path] = issues
            } finally {
                inFlight.remove(path)
            }

            notifyPsi(path)
        }
    }

    /**
     * Trigger IntelliJ re-analysis.
     *
     * @param path file path
     */
    private fun notifyPsi(path: String) {
        ApplicationManager.getApplication().invokeLater(
            {
                val vFile =
                    LocalFileSystem.getInstance().findFileByPath(path)
                        ?: return@invokeLater

                val psi =
                    PsiManager.getInstance(project).findFile(vFile)
                        ?: return@invokeLater

                @Suppress("DEPRECATION")
                DaemonCodeAnalyzer.getInstance(project).restart(psi)
            },
            project.disposed,
        )
    }

    /**
     * Schedule a Docsig run after user becomes idle.
     *
     * This avoids running CLI on every keystroke and instead batches
     * updates into a single execution after a quiet period.
     *
     * @param path file path
     */
    private fun scheduleIdle(path: String) {
        val alarm =
            idleAlarms.computeIfAbsent(path) {
                @Suppress("UnstableApiUsage")
                Alarm(Alarm.ThreadToUse.POOLED_THREAD, project)
            }

        alarm.cancelAllRequests()

        alarm.addRequest(
            {
                runDocsig(path)
            },
            DEBOUNCE_MS,
        )

        log.debug("idle scheduled path=$path")
    }

    /**
     * Trigger Docsig immediately on file save.
     *
     * @param path file path
     */
    fun scheduleFromSave(path: String) {
        log.debug("save trigger path=$path")
        schedule(path)
    }
}

/**
 * IntelliJ inspection entry point.
 *
 * Converts Docsig issues into editor highlights.
 */
class DocsigInspection : LocalInspectionTool() {
    /**
     * Build visitor that processes files.
     *
     * @param holder problem collector
     * @param isOnTheFly real-time flag
     * @return PSI visitor
     */
    override fun buildVisitor(
        holder: ProblemsHolder,
        isOnTheFly: Boolean,
    ): PsiElementVisitor {
        return object : PsiElementVisitor() {
            override fun visitFile(file: PsiFile) {
                val vFile = file.virtualFile ?: return
                if (!vFile.isInLocalFileSystem) return

                val path = vFile.path
                val service =
                    file.project.getService(DocsigService::class.java)

                val issues = service.getIssues(path)

                service.ensureFresh(file)

                for (issue in issues) {
                    val element =
                        getElementAtLine(file, issue.line - 1)
                            ?: continue

                    holder.registerProblem(
                        element,
                        issue.message,
                        ProblemHighlightType.WEAK_WARNING,
                    )
                }
            }
        }
    }
}
