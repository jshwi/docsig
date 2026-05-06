/**
 * IntelliJ UI and PSI helpers used across the plugin.
 */
package com.github.jshwi.docsig.util

import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.application.ModalityState
import com.intellij.openapi.ui.Messages
import kotlinx.io.IOException

/**
 * Returns the first semver-like x.y.z substring in text.
 *
 * @param string Extract version number from a string.
 * @return Matched version token, or null when no pattern matches.
 */
fun extractVersion(string: String): String? {
    val regex = Regex("""\d+\.\d+\.\d+""")
    return regex.find(string)?.value
}

/**
 * Posts [action] to the Swing EDT via invokeLater.
 *
 * @param action Work that touches Swing components or UI models.
 */
fun communicateUi(action: () -> Unit) {
    ApplicationManager.getApplication().invokeLater(
        action,
        ModalityState.any(),
    )
}

/**
 * Shows a modal error dialog with a fixed Docsig title.
 *
 * @param message Body text shown to the user.
 */
fun communicateError(message: String) {
    communicateUi { Messages.showErrorDialog(message, "Docsig") }
}

/**
 * Shows a modal info dialog with an optional success message.
 *
 * @param message Body text; defaults to a generic success string.
 */
fun communicateSuccess(message: String = "Valid Docsig executable") {
    communicateUi { Messages.showInfoMessage(message, "Docsig") }
}

/**
 * Runs task on a pooled thread and maps common failures to dialogs.
 *
 * @param task Work that may perform I/O or wait on a process.
 */
fun runDocsigBackground(task: () -> Unit) {
    ApplicationManager.getApplication().executeOnPooledThread {
        try {
            task()
        } catch (e: IOException) {
            communicateError("I/O error: ${e.message}")
        } catch (_: InterruptedException) {
            Thread.currentThread().interrupt()
            communicateError("Interrupted while running Docsig")
        }
    }
}
