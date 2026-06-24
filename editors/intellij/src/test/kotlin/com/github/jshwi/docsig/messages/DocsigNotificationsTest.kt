package com.github.jshwi.docsig.messages

import com.intellij.notification.Notification
import com.intellij.notification.NotificationGroup
import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.project.Project
import io.mockk.every
import io.mockk.mockk
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import io.mockk.verify
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Test
import java.util.UUID

class DocsigNotificationsTest {
    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    @Test
    fun `notifyMissingPython creates warning notification once`() {
        val project = mockk<Project>()

        every {
            project.locationHash
        } returns "notify-${UUID.randomUUID()}"

        mockkStatic(NotificationGroupManager::class)

        val groupManager = mockk<NotificationGroupManager>()

        val group = mockk<NotificationGroup>()

        val notification = mockk<Notification>(relaxed = true)

        every {
            NotificationGroupManager.getInstance()
        } returns groupManager

        every {
            groupManager.getNotificationGroup("Docsig")
        } returns group

        every {
            group.createNotification(
                any<String>(),
                any<String>(),
                any<NotificationType>(),
            )
        } returns notification

        Notifications.notifyMissingPython(project)
        Notifications.notifyMissingPython(project)

        verify(exactly = 1) {
            notification.notify(project)
        }
    }

    @Test
    fun `notifyUnsupportedPython creates warning notification once`() {
        val project = mockk<Project>()

        every {
            project.locationHash
        } returns "unsupported-${UUID.randomUUID()}"

        mockkStatic(NotificationGroupManager::class)

        val groupManager = mockk<NotificationGroupManager>()

        val group = mockk<NotificationGroup>()

        val notification = mockk<Notification>(relaxed = true)

        every {
            NotificationGroupManager.getInstance()
        } returns groupManager

        every {
            groupManager.getNotificationGroup("Docsig")
        } returns group

        every {
            group.createNotification(
                any<String>(),
                any<String>(),
                any<NotificationType>(),
            )
        } returns notification

        Notifications.notifyUnsupportedPython(project)
        Notifications.notifyUnsupportedPython(project)

        verify(exactly = 1) {
            notification.notify(project)
        }
    }
}
