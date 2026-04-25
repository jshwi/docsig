package com.github.jshwi.docsig.util

import com.intellij.openapi.application.Application
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.application.ModalityState
import com.intellij.openapi.ui.Messages
import io.mockk.Runs
import io.mockk.every
import io.mockk.just
import io.mockk.mockk
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import io.mockk.verify
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Test
import kotlin.test.assertTrue

class UtilTest {
    private val app = mockk<Application>()

    @AfterEach
    fun tearDown() {
        unmockkAll()
    }

    @Suppress("DEPRECATION")
    private fun stubEdtInvokeLaterRunsSynchronously() {
        every { app.getAnyModalityState() } returns mockk(relaxed = true)
        every {
            app.invokeLater(any<Runnable>(), any<ModalityState>())
        } answers {
            firstArg<Runnable>().run()
        }
    }

    @Test
    fun `ui executes action`() {
        mockkStatic(ApplicationManager::class)

        every { ApplicationManager.getApplication() } returns app

        stubEdtInvokeLaterRunsSynchronously()

        var ran = false

        communicateUi {
            ran = true
        }

        assertTrue(ran)
    }

    @Test
    fun `error shows dialog`() {
        mockkStatic(ApplicationManager::class)
        mockkStatic(Messages::class)

        every { ApplicationManager.getApplication() } returns app

        stubEdtInvokeLaterRunsSynchronously()

        every {
            Messages.showErrorDialog(any<String>(), any<String>())
        } returns Unit

        communicateError("boom")

        verify {
            Messages.showErrorDialog("boom", "Docsig")
        }
    }

    @Test
    fun `success shows message`() {
        mockkStatic(ApplicationManager::class)
        mockkStatic(Messages::class)

        every { ApplicationManager.getApplication() } returns app

        stubEdtInvokeLaterRunsSynchronously()

        every { Messages.showInfoMessage(any(), any()) } just Runs

        communicateSuccess("ok")

        verify {
            Messages.showInfoMessage("ok", "Docsig")
        }
    }
}
