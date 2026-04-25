/**
 * Project-scoped docsig orchestration and PSI refresh.
 */
package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.model.Issue
import com.intellij.codeInsight.daemon.DaemonCodeAnalyzer
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.Service
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.LocalFileSystem
import com.intellij.psi.PsiManager
import com.intellij.util.Alarm
import java.util.concurrent.ConcurrentHashMap

private const val DEBOUNCE_MS = 600L

@Service(Service.Level.PROJECT)
class DocsigService(private val project: Project) {
    private val log = Logger.getInstance(DocsigService::class.java)

    private val cache = ConcurrentHashMap<String, List<Issue>>()
    private val inFlight = ConcurrentHashMap.newKeySet<String>()

    private val saveAlarms = ConcurrentHashMap<String, Alarm>()
    private val idleAlarms = ConcurrentHashMap<String, Alarm>()

    // scheduling
    @Suppress("UnstableApiUsage")
    private fun schedule(
        path: String,
        alarmMap: ConcurrentHashMap<String, Alarm>,
        source: String,
    ) {
        val alarm =
            alarmMap.computeIfAbsent(path) {
                Alarm(Alarm.ThreadToUse.POOLED_THREAD, project)
            }

        alarm.cancelAllRequests()
        alarm.addRequest({ runDocsig(path) }, DEBOUNCE_MS)

        log.debug("$source scheduled path=$path")
    }

    // execution
    private fun runDocsig(path: String) {
        if (!inFlight.add(path)) return

        ApplicationManager.getApplication().executeOnPooledThread {
            try {
                val issues = Cli.run(project, path)
                cache[path] = mergeIssues(path, issues)
            } finally {
                inFlight.remove(path)
            }

            notifyPsi(path)
        }
    }

    // keeps previous non-line issues unless a fresh run provides
    // replacements
    private fun mergeIssues(path: String, issues: List<Issue>): List<Issue> {
        val hasGlobalError = issues.any { it.exit == 2 && it.line == null }

        return if (!hasGlobalError) {
            issues
        } else {
            val previousLineIssues =
                cache[path].orEmpty().filter { it.line != null }

            previousLineIssues + issues.filter { it.line == null }
        }
    }

    // psi refresh
    @Suppress("DEPRECATION")
    private fun notifyPsi(path: String) {
        ApplicationManager.getApplication().invokeLater(
            {
                val vFile =
                    LocalFileSystem.getInstance().findFileByPath(path)
                        ?: return@invokeLater

                val psi =
                    PsiManager.getInstance(project).findFile(vFile)
                        ?: return@invokeLater

                DaemonCodeAnalyzer.getInstance(project).restart(psi)
            },
            project.disposed,
        )
    }

    /**
     * Get cached issues, if any, or return an empty list.
     *
     * @param path The currently open file.
     * @return The list of issues belonging to the file.
     */
    fun getIssues(path: String): List<Issue> =
        cache[path].orEmpty()

    /**
     * Schedules a cache refresh when the editor is idle.
     *
     * @param path The currently open file.
     */
    fun ensureFresh(path: String) {
        schedule(path, idleAlarms, "idle")
    }

    /**
     * Schedules a cache refresh when the file is saved.
     *
     * @param path The currently open file.
     */
    fun scheduleFromSave(path: String) {
        log.debug("save trigger path=$path")
        schedule(path, saveAlarms, "save")
    }
}
