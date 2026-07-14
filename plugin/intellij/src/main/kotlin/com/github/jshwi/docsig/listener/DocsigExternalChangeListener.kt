package com.github.jshwi.docsig.listener

import com.github.jshwi.docsig.service.DocsigService
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.newvfs.BulkFileListener
import com.intellij.openapi.vfs.newvfs.events.VFileEvent

/**
 * VFS hook that invalidates Docsig results for external file changes.
 *
 * Saves made inside the IDE go through the save listener, but a file
 * edited by another program (formatter, git, another editor) only
 * surfaces as a VFS refresh. Without this hook the issue cache stays
 * stale and re-saving the unmodified document is a no-op, so the old
 * highlights never clear.
 */
internal class DocsigExternalChangeListener(private val project: Project) :
    BulkFileListener {
    /** Forward externally changed local files to the Docsig service. */
    override fun after(events: List<VFileEvent>) {
        val service = project.getService(DocsigService::class.java)

        // events raised from inside the ide (document saves) are
        // already handled by the save listener
        // refresh events are the ones detecting external edits
        // docsig results are only cached for real filesystem paths, and
        // the service only acts when the path has cached results, so
        // unrelated files cost nothing here
        events
            .asSequence()
            .filter { it.isFromRefresh }
            .mapNotNull { it.file }
            .filter { it.isInLocalFileSystem }
            .forEach { service.invalidateExternalChange(it.path) }
    }
}
