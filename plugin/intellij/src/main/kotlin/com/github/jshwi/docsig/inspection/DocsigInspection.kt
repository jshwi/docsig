/**
 * Local inspection that surfaces docsig messages as warnings.
 *
 * DocsigInspection is a Python local inspection (LocalInspectionTool).
 * The IDE calls buildVisitor when it analyzes a file; the returned
 * visitor’s visitFile runs for each PsiFile root. The inspection does
 * not run docsig itself here; it reads cached results from
 * DocsigService and turns them into editor squiggles (problems).
 * DocsigService owns running the CLI and caching Issues.
 * DocsigInspection is the view layer: “given what we already know for
 * this path, paint problems in the editor; if we have never stored a
 * result for the path, ask the service to refresh in the background.”
 *
 */
package com.github.jshwi.docsig.inspection

import com.github.jshwi.docsig.models.Issue
import com.github.jshwi.docsig.service.DocsigService
import com.intellij.codeInspection.LocalInspectionTool
import com.intellij.codeInspection.ProblemHighlightType
import com.intellij.codeInspection.ProblemsHolder
import com.intellij.psi.PsiDocumentManager
import com.intellij.psi.PsiElement
import com.intellij.psi.PsiElementVisitor
import com.intellij.psi.PsiFile
import com.intellij.psi.PsiNameIdentifierOwner
import com.intellij.util.text.CharArrayUtil

/**
 * Register one problem per cached issue on the matching source line.
 *
 * When the service has no cache entry yet for the path, schedule one
 * background refresh so a later pass can show newly computed results.
 */
internal class DocsigInspection : LocalInspectionTool() {
    // walk up the psi tree until a psi name identifier owner, if found,
    // and use its name identifier (e.g. function/class name) that way
    // the underline sits on the symbol, not on random tokens like a
    // comma
    private fun findBestHighlightTarget(element: PsiElement): PsiElement {
        var current: PsiElement? = element

        while (current != null) {
            val nameIdentifier =
                (current as? PsiNameIdentifierOwner)?.nameIdentifier

            if (nameIdentifier != null) return nameIdentifier

            current = current.parent
        }

        return element
    }

    // line 1 is first document line; fall back to file when out of
    // range
    private fun resolveElement(file: PsiFile, line: Int?): PsiElement {
        // highlight the whole file (file-level issue)
        if (line == null) return file

        val document =
            PsiDocumentManager.getInstance(file.project).getDocument(file)
                ?: return file

        // map 1-based line to a document offset
        val index = line - 1

        if (index < 0 || index >= document.lineCount) return file

        val startOffset = document.getLineStartOffset(index)

        // skip leading spaces/tabs
        val nonWhitespaceOffset =
            CharArrayUtil.shiftForward(
                document.charsSequence,
                startOffset,
                " \t",
            )

        // find element at offset
        val element = file.findElementAt(nonWhitespaceOffset) ?: return file

        // prefer the name leaf so squiggles sit on the symbols
        return findBestHighlightTarget(element)
    }

    // maps an issue exit code to an intellij highlight type
    private fun Issue.toHighlightType(): ProblemHighlightType =
        if (exit == 2) {
            ProblemHighlightType.ERROR
        } else {
            ProblemHighlightType.WARNING
        }

    /**
     * Visit file roots to register cached docsig issues as problems.
     *
     * @param holder Sink used to register weak warnings on elements.
     * @param isOnTheFly True when invoked from editor highlighting.
     * @return Visitor that only handles [PsiFile] traversal roots.
     */
    override fun buildVisitor(
        holder: ProblemsHolder,
        isOnTheFly: Boolean,
    ): PsiElementVisitor =
        object : PsiElementVisitor() {
            /**
             * Register cached problems or schedule a first check.
             *
             * @param psiFile PSI file under inspection on the local FS.
             */
            override fun visitFile(psiFile: PsiFile) {
                // if no virtual file found, return (no problems)
                val file = psiFile.virtualFile ?: return

                // if no file on the local filesystem found, return (no
                // problems)
                if (!file.isInLocalFileSystem) return

                // resolve docsig service for the project
                val service =
                    psiFile.project.getService(
                        DocsigService::class.java,
                    )

                if (!service.hasCached(file.path)) {
                    service.ensureFresh(file.path)

                    return
                }

                val issues = service.getIssues(file.path)

                if (issues.isEmpty()) return

                issues.forEach { issue ->
                    val element = resolveElement(psiFile, issue.line)

                    holder.registerProblem(
                        element,
                        issue.message,
                        issue.toHighlightType(),
                    )
                }
            }
        }
}
