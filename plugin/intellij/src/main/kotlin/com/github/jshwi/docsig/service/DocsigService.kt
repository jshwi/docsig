/**
 * Project-scoped docsig orchestration and PSI refresh.
 */
package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.models.Issue
import com.github.jshwi.docsig.notifications.Notifications
import com.intellij.codeInsight.daemon.DaemonCodeAnalyzer
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.Service
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.LocalFileSystem
import com.intellij.psi.PsiManager
import java.util.concurrent.ConcurrentHashMap

/**
 * Project-scoped docsig orchestration and PSI refresh.
 *
 * Debounces overlapping runs per path; concurrent calls skip when path
 * already held.
 *
 * One instance exists per open project. It runs the docsig CLI for a
 * file path, stores results in a per-path issue cache, and refreshes
 * inspections so the editor picks up new diagnostics.
 */
@Service(Service.Level.PROJECT)
internal class DocsigService(private val project: Project) {
    private val log = Logger.getInstance(DocsigService::class.java)

    // last known issues keyed by absolute file path for inspection to
    // read
    private val cache = ConcurrentHashMap<String, List<Issue>>()

    // paths currently running docsig stored in a concurrent set
    private val inFlight = ConcurrentHashMap.newKeySet<String>()

    // separate alarm-like instances per path for “saved” vs “idle”
    // triggers, so debouncing for saves does not fight debouncing for
    // idle typing
    private val saveAlarms = ConcurrentHashMap<String, AlarmLike>()
    private val idleAlarms = ConcurrentHashMap<String, AlarmLike>()

    // one cli per project so python sdk resolution runs once
    private val cli: Cli by lazy { cliFactory(project) }

    // scheduling
    private fun schedule(
        path: String,
        alarmMap: ConcurrentHashMap<String, AlarmLike>,
        source: String,
        resetDebounce: Boolean,
    ) {
        // tests: if true, run docsig immediately and return (no alarm)
        if (runScheduledWorkSynchronouslyForTests) {
            runDocsig(path)

            log.debug("$source scheduled path=$path")

            return
        }

        // normal: get or creates an alarm-like for that path in the
        // given map
        val alarm = alarmMap.computeIfAbsent(path) { alarmFactory(project) }

        // save: reset timer on each save so rapid writes coalesce
        // idle: do not cancel — daemon re-runs inspection often; each
        // pass would push the run forever if we kept resetting
        if (alarm.hasPendingRequests()) return

        if (resetDebounce) alarm.cancelAllRequests()

        alarm.addRequest({ runDocsig(path) }, DEBOUNCE_MS)

        log.debug("$source scheduled path=$path")
    }

    // execution
    private fun runDocsig(path: String) {
        // python missing
        if (!cli.isAvailable()) {
            log.warn("docsig unavailable: no python interpreter configured")

            Notifications.notifyMissingPython(project)

            return
        }

        if (!cli.isPythonSupported()) {
            log.warn("docsig unavailable: python below minimum version")

            Notifications.notifyUnsupportedPython(project)

            return
        }

        // second caller waits for the first run to finish, if false,
        // another thread already holds this path; this call returns
        // without running (second waiter does not queue another cli
        // run)
        if (!inFlight.add(path)) return

        ApplicationManager.getApplication().executeOnPooledThread {
            try {
                // run cli on a pooled thread
                val issues = cli.run(path)

                // update cache
                cache[path] = mergeIssues(path, issues)
            } finally {
                inFlight.remove(path)
            }

            // call on the edt after the run so the daemon re-runs
            // inspections for that file
            // why inspections update
            // on the edt (invoke later with project.disposed as
            // modality state), it finds the virtual file and psi file,
            // then daemoncodeanalyzer.getinstance(project).restart(psi)
            // so intellij re-runs local inspections (including docsig)
            // against fresh cache data
            notifyPsi(path)
        }
    }

    // keeps previous non-line issues unless a fresh run provides
    // replacements
    private fun mergeIssues(path: String, issues: List<Issue>): List<Issue> {
        // if the new result has a “global” failure (exit == 2 and
        // line == null), the service keeps previous line-level issues
        // from the cache and appends the new non-line issues
        // that way a cli-wide error does not wipe line-specific markers
        // until a good run replaces them
        val hasGlobalError = issues.any { it.exit == 2 && it.line == null }

        return if (!hasGlobalError) {
            issues
        } else {
            // if there is no such global error, just use issues as
            // returned
            val previousLineIssues =
                cache[path]
                    .orEmpty()
                    .filter { it.line != null }

            previousLineIssues + issues.filter { it.line == null }
        }
    }

    // psi refresh
    private fun notifyPsi(path: String) {
        ApplicationManager.getApplication().invokeLater(
            {
                val file = LocalFileSystem.getInstance().findFileByPath(path)

                val psi =
                    file?.let {
                        PsiManager
                            .getInstance(project)
                            .findFile(it)
                    }

                if (psi != null) {
                    DaemonCodeAnalyzer
                        .getInstance(project)
                        .restart(psi, DOCSIG_DAEMON_RESTART_REASON)
                }
            },
            project.disposed,
        )
    }

    /**
     * Whether [path] has a cache entry from a completed docsig run.
     *
     * An empty issue list still counts as cached so the inspection does
     * not keep scheduling work for a clean file on every daemon pass.
     *
     * @param path Absolute file path.
     * @return True when [getIssues] reflects a stored result.
     */
    fun hasCached(path: String): Boolean = cache.containsKey(path)

    /**
     * Get cached issues, if any, or return an empty list.
     *
     * @param path The currently open file.
     * @return The list of issues belonging to the file.
     */
    fun getIssues(path: String): List<Issue> = cache[path].orEmpty()

    /**
     * Schedules a cache refresh when the editor is idle.
     *
     * @param path The currently open file.
     */
    fun ensureFresh(path: String) {
        schedule(path, idleAlarms, "idle", resetDebounce = false)
    }

    /**
     * Schedules a cache refresh when the file is saved.
     *
     * @param path The currently open file.
     */
    fun scheduleFromSave(path: String) {
        log.debug("save trigger path=$path")

        schedule(path, saveAlarms, "save", resetDebounce = true)
    }

    companion object {
        private const val DOCSIG_DAEMON_RESTART_REASON = "docsig"

        private const val DEBOUNCE_MS = 600L

        /**
         * When true, [schedule] runs [runDocsig] immediately so tests
         * do not construct alarm, which needs a real platform
         * application.
         */
        internal var runScheduledWorkSynchronouslyForTests = false

        internal var alarmFactory: (Project) -> AlarmLike = {
            AlarmAdapter(it)
        }

        /**
         * Replace in tests to supply a mock [Cli] without running the
         * real subprocess path.
         */
        internal var cliFactory: (Project) -> Cli = { Cli(it) }
    }
}
