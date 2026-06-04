package com.github.jshwi.docsig.listener

import com.github.jshwi.docsig.service.DocsigService
import com.intellij.openapi.editor.Document
import com.intellij.openapi.fileEditor.FileDocumentManager
import com.intellij.openapi.fileEditor.FileDocumentManagerListener
import com.intellij.openapi.project.ProjectLocator

/**
 * File save hook that triggers Docsig for the saved path.
 *
 * Run only for documents backed by a local virtual file.
 * Listen for imminent document saves and debounce a Docsig run.
 */
internal class DocsigSaveListener : FileDocumentManagerListener {
    /** Forward local saves to the project Docsig debouncer. */
    override fun beforeDocumentSaving(document: Document) {
        // resolve the editor document to its backing virtual file
        // if the document has no associated file (scratch buffer,
        // unsaved file, etc.), there is nothing for docsig to process
        val file =
            FileDocumentManager.getInstance().getFile(document) ?: return

        // ignore non-local files such as in-memory or special virtual
        // filesystem entries
        // docsig expects a real filesystem path
        if (!file.isInLocalFileSystem) return

        // determine which currently open project owns this file
        // docsig service is project-scoped, so we need the correct
        // project instance
        val project =
            ProjectLocator.getInstance().guessProjectForFile(file) ?: return

        // get the project's docsig service and schedule a debounced
        // refresh
        // debouncing prevents rapid consecutive saves from repeatedly
        // invoking the cli
        project
            .getService(DocsigService::class.java)
            .scheduleFromSave(file.path)
    }
}
