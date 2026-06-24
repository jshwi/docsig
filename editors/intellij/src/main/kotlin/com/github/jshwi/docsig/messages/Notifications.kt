package com.github.jshwi.docsig.messages

import com.github.jshwi.docsig.cli.Python
import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.project.Project
import java.util.concurrent.ConcurrentHashMap

internal object Notifications {
    private const val NOTIFICATION_GROUP = "Docsig"

    private val missingPyNotified = ConcurrentHashMap.newKeySet<String>()

    private val unsupportedPyNotified = ConcurrentHashMap.newKeySet<String>()

    private fun notifyOnce(
        project: Project,
        notified: MutableSet<String>,
        title: String,
        content: String,
    ) {
        val key = project.locationHash

        if (!notified.add(key)) return

        NotificationGroupManager
            .getInstance()
            .getNotificationGroup(NOTIFICATION_GROUP)
            .createNotification(title, content, NotificationType.WARNING)
            .notify(project)
    }

    internal fun notifyMissingPython(project: Project) {
        notifyOnce(
            project,
            missingPyNotified,
            DocsigBundle.message(
                "notification.missing-python.title",
            ),
            DocsigBundle.message(
                "notification.missing-python.content",
                Python.MIN_MAJOR,
                Python.MIN_MINOR,
            ),
        )
    }

    internal fun notifyUnsupportedPython(project: Project) {
        notifyOnce(
            project,
            unsupportedPyNotified,
            DocsigBundle.message(
                "notification.unsupported-python.title",
            ),
            DocsigBundle.message(
                "notification.unsupported-python.content",
                Python.MIN_MAJOR,
                Python.MIN_MINOR,
            ),
        )
    }
}
