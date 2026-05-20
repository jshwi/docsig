package com.github.jshwi.docsig.inspection

import com.github.jshwi.docsig.models.Issue
import com.github.jshwi.docsig.service.DocsigService
import com.intellij.codeInspection.ProblemHighlightType
import com.intellij.codeInspection.ProblemsHolder
import com.intellij.openapi.editor.Document
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.psi.PsiDocumentManager
import com.intellij.psi.PsiElement
import com.intellij.psi.PsiFile
import com.intellij.psi.PsiNameIdentifierOwner
import io.mockk.every
import io.mockk.just
import io.mockk.mockk
import io.mockk.runs
import io.mockk.slot
import io.mockk.unmockkAll
import io.mockk.verify
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.BeforeEach
import kotlin.test.Test

/**
 * Tests for [DocsigInspection] problem registration and PSI targeting.
 */
class DocsigInspectionTest {
    private lateinit var service: DocsigService
    private lateinit var project: Project
    private lateinit var psiFile: PsiFile
    private lateinit var virtualFile: VirtualFile
    private lateinit var holder: ProblemsHolder
    private lateinit var psiDocumentManager: PsiDocumentManager
    private lateinit var document: Document

    @BeforeEach
    fun setup() {
        service = mockk(relaxed = true)
        project = mockk()
        psiFile = mockk(relaxed = true)
        virtualFile = mockk()
        holder = mockk(relaxed = true)
        psiDocumentManager = mockk()
        document = mockk()

        every { psiFile.project } returns project
        every { psiFile.virtualFile } returns virtualFile
        every { virtualFile.isInLocalFileSystem } returns true
        every { virtualFile.path } returns "/test/file.py"

        every {
            project.getService(
                DocsigService::class.java,
            )
        } returns service

        every { service.hasCached(any()) } returns true

        every {
            project.getService(
                PsiDocumentManager::class.java,
            )
        } returns psiDocumentManager

        every {
            psiDocumentManager.getDocument(psiFile)
        } returns document

        every { document.lineCount } returns 10
        every { document.getLineStartOffset(any()) } returns 0
        every { document.charsSequence } returns "def hello()"

        val element = mockk<PsiElement>()

        every {
            psiFile.findElementAt(any())
        } returns element

        every { element.parent } returns null
    }

    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    @Test
    fun `does nothing when file has no virtual file`() {
        every { psiFile.virtualFile } returns null

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 0) {
            service.getIssues(any())
        }
    }

    @Test
    fun `does nothing when file is not local`() {
        every {
            virtualFile.isInLocalFileSystem
        } returns false

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 0) {
            service.getIssues(any())
        }
    }

    @Test
    fun `schedules refresh when path not yet in cache`() {
        every { service.hasCached("/test/file.py") } returns false

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 1) {
            service.ensureFresh("/test/file.py")
        }

        verify(exactly = 0) {
            service.getIssues(any())
        }

        verify(exactly = 0) {
            holder.registerProblem(
                any<PsiElement>(),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        }
    }

    @Test
    fun `does not refresh when cache is empty but known`() {
        every {
            service.getIssues("/test/file.py")
        } returns emptyList()

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 0) {
            service.ensureFresh(any())
        }

        verify(exactly = 0) {
            holder.registerProblem(
                any<PsiElement>(),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        }
    }

    @Test
    fun `registers warning problems`() {
        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 1,
                    message = "Warning",
                    exit = 1,
                ),
            )

        every {
            holder.registerProblem(
                any<PsiElement>(),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 1) {
            holder.registerProblem(
                any<PsiElement>(),
                "Warning",
                ProblemHighlightType.WARNING,
            )
        }
    }

    @Test
    fun `registers error problems`() {
        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 1,
                    message = "Error",
                    exit = 2,
                ),
            )

        every {
            holder.registerProblem(
                any<PsiElement>(),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 1) {
            holder.registerProblem(
                any<PsiElement>(),
                "Error",
                ProblemHighlightType.ERROR,
            )
        }
    }

    @Test
    fun `registers one problem for each issue`() {
        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 1,
                    message = "First",
                    exit = 1,
                ),
                Issue(
                    line = 2,
                    message = "Second",
                    exit = 2,
                ),
            )

        every {
            holder.registerProblem(
                any<PsiElement>(),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        verify(exactly = 1) {
            holder.registerProblem(
                any<PsiElement>(),
                "First",
                ProblemHighlightType.WARNING,
            )
        }

        verify(exactly = 1) {
            holder.registerProblem(
                any<PsiElement>(),
                "Second",
                ProblemHighlightType.ERROR,
            )
        }
    }

    @Test
    fun `highlights name identifier when element is name owner`() {
        val nameIdentifier = mockk<PsiElement>()
        val element =
            mockk<PsiElement>(
                relaxed = true,
                moreInterfaces = arrayOf(PsiNameIdentifierOwner::class),
            )

        every {
            (element as PsiNameIdentifierOwner).nameIdentifier
        } returns nameIdentifier

        every {
            psiFile.findElementAt(any())
        } returns element

        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 1,
                    message = "On name",
                    exit = 1,
                ),
            )

        val elementSlot = slot<PsiElement>()

        every {
            holder.registerProblem(
                capture(elementSlot),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        Assertions.assertEquals(
            nameIdentifier,
            elementSlot.captured,
        )
    }

    @Test
    fun `passes file when document is unavailable for line issue`() {
        every {
            psiDocumentManager.getDocument(psiFile)
        } returns null

        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 1,
                    message = "No doc",
                    exit = 1,
                ),
            )

        val elementSlot = slot<PsiElement>()

        every {
            holder.registerProblem(
                capture(elementSlot),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        Assertions.assertEquals(
            psiFile,
            elementSlot.captured,
        )
    }

    @Test
    fun `passes file when line has no psi element`() {
        every {
            psiFile.findElementAt(any())
        } returns null

        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 1,
                    message = "No leaf",
                    exit = 1,
                ),
            )

        val elementSlot = slot<PsiElement>()

        every {
            holder.registerProblem(
                capture(elementSlot),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        Assertions.assertEquals(
            psiFile,
            elementSlot.captured,
        )
    }

    @Test
    fun `passes file when issue line is beyond document`() {
        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 11,
                    message = "Past end",
                    exit = 1,
                ),
            )

        val elementSlot = slot<PsiElement>()

        every {
            holder.registerProblem(
                capture(elementSlot),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        Assertions.assertEquals(
            psiFile,
            elementSlot.captured,
        )

        verify(exactly = 0) {
            document.getLineStartOffset(any())
        }
    }

    @Test
    fun `passes file when issue line is zero`() {
        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = 0,
                    message = "Line zero",
                    exit = 1,
                ),
            )

        val elementSlot = slot<PsiElement>()

        every {
            holder.registerProblem(
                capture(elementSlot),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        Assertions.assertEquals(
            psiFile,
            elementSlot.captured,
        )

        verify(exactly = 0) {
            document.getLineStartOffset(any())
        }
    }

    @Test
    fun `passes resolved psi element into holder`() {
        every {
            service.getIssues("/test/file.py")
        } returns
            listOf(
                Issue(
                    line = null,
                    message = "Message",
                    exit = 1,
                ),
            )

        val elementSlot = slot<PsiElement>()

        every {
            holder.registerProblem(
                capture(elementSlot),
                any<String>(),
                any<ProblemHighlightType>(),
            )
        } just runs

        val visitor =
            DocsigInspection().buildVisitor(holder, true)

        visitor.visitFile(psiFile)

        Assertions.assertEquals(
            psiFile,
            elementSlot.captured,
        )
    }
}
