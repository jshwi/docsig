/**
 * User-facing notifications for docsig IDE integration.
 */
package com.github.jshwi.docsig.notifications

import com.github.jshwi.docsig.cli.Python
import com.github.jshwi.docsig.messages.DocsigBundle
import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.project.Project

/**
 * Show docsig notifications; deduplicate per project location hash.
 */
internal object Notifications {
    private val missingPythonNotified = mutableSetOf<String>()

    private val unsupportedPythonNotified = mutableSetOf<String>()

    private fun notifyOnce(
        project: Project,
        notified: MutableSet<String>,
        titleKey: String,
        content: String,
    ) {
        val key = project.locationHash

        if (!notified.add(key)) return

        NotificationGroupManager
            .getInstance()
            .getNotificationGroup("Docsig")
            .createNotification(titleKey, content, NotificationType.WARNING)
            .notify(project)
    }

    /**
     * Warns once per project session that an interpreter is required.
     *
     * @param project The current project.
     */
    fun notifyMissingPython(project: Project) {
        notifyOnce(
            project,
            missingPythonNotified,
            DocsigBundle.message(
                "notification.missing-python.title",
            ),
            DocsigBundle.message(
                "notification.missing-python.content",
                Python.MINIMUM_MAJOR,
                Python.MINIMUM_MINOR,
            ),
        )
    }

    /**
     * Warns once per project session that the interpreter is too old.
     *
     * @param project The current project.
     */
    fun notifyUnsupportedPython(project: Project) {
        notifyOnce(
            project,
            unsupportedPythonNotified,
            DocsigBundle.message(
                "notification.unsupported-python.title",
            ),
            DocsigBundle.message(
                "notification.unsupported-python.content",
                Python.MINIMUM_MAJOR,
                Python.MINIMUM_MINOR,
            ),
        )
    }
}
