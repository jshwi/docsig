/**
 * Local inspection that surfaces docsig messages as weak warnings.
 */
package com.github.jshwi.docsig.inspection

import com.github.jshwi.docsig.model.Issue
import com.github.jshwi.docsig.service.DocsigService
import com.intellij.codeInspection.LocalInspectionTool
import com.intellij.codeInspection.ProblemHighlightType
import com.intellij.codeInspection.ProblemsHolder
import com.intellij.psi.PsiDocumentManager
import com.intellij.psi.PsiElement
import com.intellij.psi.PsiElementVisitor
import com.intellij.psi.PsiFile

/**
 * Registers one problem per cached issue on the matching source line.
 *
 * Schedules refresh so a later pass can show newly computed results.
 */
class DocsigInspection : LocalInspectionTool() {
    // resolves the psi element for a given issue line
    private fun resolveElement(file: PsiFile, line: Int?): PsiElement {
        if (line == null) return file

        val document =
            PsiDocumentManager.getInstance(file.project).getDocument(file)
                ?: return file

        val index = line - 1
        if (index !in 0 until document.lineCount) return file

        // uses the element at the start of the line when possible
        // falls back to end-of-line if needed
        // returns the file itself when line is null or invalid
        return file.findElementAt(document.getLineStartOffset(index))
            ?: file.findElementAt(document.getLineEndOffset(index))
            ?: file
    }

    // maps an issue exit code to an intellij highlight type
    private fun Issue.toHighlightType(): ProblemHighlightType =
        if (exit == 2) {
            ProblemHighlightType.ERROR
        } else {
            ProblemHighlightType.WARNING
        }

    /**
     * Visits file roots to register cached docsig issues as problems.
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
             * Registers cached problems and schedules a cache refresh.
             *
             * @param psiFile PSI file under inspection on the local FS.
             */
            override fun visitFile(psiFile: PsiFile) {
                val vFile = psiFile.virtualFile ?: return

                if (!vFile.isInLocalFileSystem) return

                val service =
                    psiFile.project.getService(
                        DocsigService::class.java,
                    )

                val path = vFile.path

                val issues = service.getIssues(path)

                if (issues.isEmpty()) {
                    service.ensureFresh(path)
                    return
                }

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
