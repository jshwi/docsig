package com.github.jshwi.docsig.inspection

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

internal class DocsigInspection : LocalInspectionTool() {
    // walk up the psi tree until a function name element is found
    private fun getFunctionName(element: PsiElement): PsiElement {
        var current: PsiElement? = element

        while (current != null) {
            val id = (current as? PsiNameIdentifierOwner)?.nameIdentifier

            if (id != null) return id

            current = current.parent
        }

        return element
    }

    // get a function name or file element
    private fun resolveElement(file: PsiFile, line: Int?): PsiElement {
        // fall back to file if line is null, indicating file level
        // issue
        if (line == null) return file

        val instance = PsiDocumentManager.getInstance(file.project)

        val document = instance.getDocument(file) ?: return file

        // map index to a line starting from one to a document offset
        val index = line - 1

        if (index < 0 || index >= document.lineCount) return file

        val startOffset = document.getLineStartOffset(index)

        // skip leading whitespace
        val nonWhitespaceOffset =
            CharArrayUtil.shiftForward(
                document.charsSequence,
                startOffset,
                " \t",
            )

        val element = file.findElementAt(nonWhitespaceOffset) ?: return file

        // ensure highlight sits on the function name
        return getFunctionName(element)
    }

    override fun buildVisitor(
        holder: ProblemsHolder,
        isOnTheFly: Boolean,
    ): PsiElementVisitor = object : PsiElementVisitor() {
        override fun visitFile(file: PsiFile) {
            val vFile = file.virtualFile ?: return

            if (!vFile.isInLocalFileSystem) return

            val svc = file.project.getService(DocsigService::class.java)

            if (!svc.hasCached(vFile.path)) {
                svc.ensureFresh(vFile.path)

                return
            }

            val issues = svc.getIssues(vFile.path)

            if (issues.isEmpty()) return

            issues.forEach { issue ->
                val element = resolveElement(file, issue.line)

                val highlight = if (issue.exit == 2) {
                    ProblemHighlightType.ERROR
                } else {
                    ProblemHighlightType.WARNING
                }

                holder.registerProblem(element, issue.message, highlight)
            }
        }
    }
}
