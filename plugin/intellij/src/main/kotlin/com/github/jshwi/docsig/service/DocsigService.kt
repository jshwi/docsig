package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.messages.Notifications
import com.github.jshwi.docsig.models.Issue
import com.intellij.codeInsight.daemon.DaemonCodeAnalyzer
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.Service
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.fileEditor.FileEditorManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.LocalFileSystem
import com.intellij.psi.PsiManager
import com.intellij.util.Alarm
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

    // separate alarms (per-path for saved vs idle triggers) so
    // debouncing for saves do not fight debouncing for idle typing
    private val saveAlarms = ConcurrentHashMap<String, Alarm>()

    private val idleAlarms = ConcurrentHashMap<String, Alarm>()

    // one cli per project so python sdk resolution runs once
    private val cli: Cli by lazy { Cli(project) }

    private fun schedule(
        path: String,
        alarmMap: ConcurrentHashMap<String, Alarm>,
        source: String,
        resetDebounce: Boolean,
    ) {
        log.debug("$source scheduled path=$path")

        val alarm = alarmMap.computeIfAbsent(path) { alarmFactory(project) }

        // for saving, reset timer on each save so rapid writes coalesce
        // when idle, do not cancel
        // daemon re-runs inspection often
        // each pass would push the run forever if we kept resetting
        if (!alarm.isEmpty) return

        if (resetDebounce) alarm.cancelAllRequests()

        alarm.addRequest({ runDocsig(path) }, DEBOUNCE_MS)
    }

    private fun runDocsig(path: String) {
        if (!cli.isAvailable()) {
            Notifications.notifyMissingPython(project)

            return
        }

        if (!cli.isPythonSupported()) {
            Notifications.notifyUnsupportedPython(project)

            return
        }

        // second caller waits for the first run to finish, if false,
        // another thread already holds this path
        // this call returns without running (second waiter does not
        // queue another cli run)
        if (!inFlight.add(path)) return

        // run cli on a pooled thread
        ApplicationManager.getApplication().executeOnPooledThread {
            try {
                val issues = cli.run(path)

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

        // if there is no global error, just return issues
        if (!hasGlobalError) return issues

        // if the new result has a global failure the service keeps
        // previous line-level issues from the cache and appends the new
        // non-line issues, that way a cli-wide error does not wipe
        // line-specific markers until a good run replaces them
        val prevLineIssues = cache[path].orEmpty().filter { it.line != null }

        return prevLineIssues + issues.filter { it.line == null }
    }

    // call on the edt after the run so the daemon re-runs inspections
    // for that file
    // inspections update on the edt (invoke later with disposed project
    // as modality state)
    // it finds the virtual file and psi file, so intellij re-runs local
    // inspections (including docsig) against fresh cache data
    private fun notifyPsi(path: String) {
        ApplicationManager.getApplication().invokeLater(
            {
                val file = LocalFileSystem.getInstance().findFileByPath(path)

                val psi =
                    file?.let { PsiManager.getInstance(project).findFile(it) }

                if (psi != null) {
                    DaemonCodeAnalyzer
                        .getInstance(project)
                        .restart(psi, DOCSIG_DAEMON_RESTART_REASON)
                }
            },
            project.disposed,
        )
    }

    // an empty issue list still counts as cached so the inspection does
    // not keep scheduling work for a clean file on every daemon pass
    internal fun hasCached(path: String): Boolean = cache.containsKey(path)

    internal fun getIssues(path: String): List<Issue> = cache[path].orEmpty()

    // schedules a cache refresh when the editor is idle
    internal fun ensureFresh(path: String) =
        schedule(path, idleAlarms, "idle", resetDebounce = false)

    internal fun scheduleFromSave(path: String) {
        log.debug("save trigger path=$path")

        schedule(path, saveAlarms, "save", resetDebounce = true)
    }

    // drop stale results when a file changes outside the ide
    // restarting the daemon makes the inspection see an empty cache and
    // schedule a fresh run, but only for files the editor is actually
    // analysing, so bulk external changes do not fan out cli runs
    internal fun invalidateExternalChange(path: String) {
        if (cache.remove(path) == null) return

        log.debug("external change path=$path")

        notifyPsi(path)
    }

    private fun pathsAffectedBySettingsChange(): Set<String> {
        val paths = linkedSetOf<String>()

        paths.addAll(cache.keys)

        FileEditorManager.getInstance(project).openFiles
            .asSequence()
            .filter { it.isInLocalFileSystem && it.extension == "py" }
            .mapTo(paths) { it.path }

        return paths
    }

    // re-run docsig for every path we have checked or that is open in
    // an editor so highlights match the new settings
    internal fun scheduleAfterSettingsChange() {
        val paths = pathsAffectedBySettingsChange()

        if (paths.isEmpty()) return

        log.debug("settings trigger paths=${paths.size}")

        paths.forEach { path ->
            cache.remove(path)
            notifyPsi(path)
            schedule(path, saveAlarms, "settings", resetDebounce = true)
        }
    }

    companion object {
        private const val DOCSIG_DAEMON_RESTART_REASON = "docsig"

        private const val DEBOUNCE_MS = 600L

        @Suppress("UnstableApiUsage")
        internal var alarmFactory: (Project) -> Alarm = { project ->
            Alarm(Alarm.ThreadToUse.POOLED_THREAD, project)
        }
    }
}
