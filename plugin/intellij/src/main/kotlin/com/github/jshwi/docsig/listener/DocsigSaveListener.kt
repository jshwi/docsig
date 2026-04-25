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
 * Listens for imminent document saves and debounces a docsig run.
 */
class DocsigSaveListener : FileDocumentManagerListener {
    /**
     * Forwards local saves to the project docsig debouncer.
     *
     * @param document Document about to be written to disk.
     */
    override fun beforeDocumentSaving(document: Document) {
        val file =
            FileDocumentManager.getInstance().getFile(document)
                ?: return

        if (!file.isInLocalFileSystem) return

        val project =
            ProjectLocator.getInstance().guessProjectForFile(file)
                ?: return

        val service = project.getService(DocsigService::class.java)

        service.scheduleFromSave(file.path)
    }
}
