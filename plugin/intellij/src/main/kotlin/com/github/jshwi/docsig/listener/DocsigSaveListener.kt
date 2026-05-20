/**
 * File save hook that triggers docsig for the saved path.
 *
 * Runs only for documents backed by a local virtual file.
 */
package com.github.jshwi.docsig.listener

import com.github.jshwi.docsig.service.DocsigService
import com.intellij.openapi.editor.Document
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.fileEditor.FileDocumentManagerListener
import com.intellij.openapi.project.ProjectLocator

/**
 * Listen for imminent document saves and debounce a docsig run.
 *
 * An IntelliJ save hook: whenever a document is about to be written to
 * disk, the platform calls beforeDocumentSaving. This class uses that
 * moment to ask the project’s DocsigService to schedule a docsig run
 * for that file’s path.
 */
internal class DocsigSaveListener : FileDocumentManagerListener {
    /**
     * Forward local saves to the project docsig debouncer.
     *
     * IntelliJ calls this right before persisting the editor buffer.
     *
     * @param document Document about to be written to disk.
     */
    override fun beforeDocumentSaving(document: Document) {
        // map the in-memory document to a virtual file, if there is no
        // backing file (unsaved scratch, etc.), return early
        val file =
            FileDocumentManager.getInstance().getFile(document)
                ?: return

        // skips things like in-memory-only or special virtual files, so
        // docsig is not pointed at non-path resources
        if (!file.isInLocalFileSystem) return

        // pick which open project “owns” that file, if none is found,
        // return (nothing to schedule)
        val project =
            ProjectLocator.getInstance().guessProjectForFile(file)
                ?: return

        // the per-project service
        val service = project.getService(DocsigService::class.java)

        // trigger the debounced refresh path (save alarms in docsig
        // service), so rapid saves do not spam the cli
        service.scheduleFromSave(file.path)
    }
}
