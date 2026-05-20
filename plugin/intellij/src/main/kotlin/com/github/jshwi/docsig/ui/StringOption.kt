/**
 * Data class for a string option.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.AlignX
import com.intellij.ui.dsl.builder.Panel
import javax.swing.JTextField

/**
 * Single string argument rendered as a text field.
 *
 * @param label Row label shown beside the input.
 * @param group Section title for grouped layout in settings UI.
 * @param summary Bundle key for helper text below the text field.
 * @param flag CLI flag inserted before the value.
 * @param get Reads the current string from settings.
 * @param set Persists the updated string into settings.
 * @param normalize Optional transform before emitting (e.g. trim).
 */
internal data class StringOption(
    override val label: String,
    override val group: String,
    override val summary: String,
    val flag: String,
    val get: (DocsigSettings) -> String?,
    val set: (DocsigSettings, String?) -> Unit,
    val normalize: (String) -> String = { it.trim() },
) : Option {
    private var component: JTextField? = null

    /**
     * Connects this row to the text field created by the settings UI.
     *
     * @param project Project whose settings seed the text field.
     */
    override fun Panel.render(project: Project) {
        val settings = docsigSettings(project)

        val field = JTextField().apply { text = get(settings) ?: "" }

        component = field

        row(label) {
            cell(field).resizableColumn().align(AlignX.FILL)
        }.comment(summary)
    }

    override fun apply(project: Project, add: (String) -> Unit) {
        val settings = docsigSettings(project)

        val value = get(settings)?.let(normalize)?.takeIf { it.isNotEmpty() }

        if (value != null) {
            add(flag)

            add(value)
        }
    }

    override fun isModified(project: Project): Boolean {
        val c = component ?: return false

        val settings = docsigSettings(project)

        val ui = c.text.trim().ifEmpty { null }

        return ui != get(settings)
    }

    override fun applyTo(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        val value = c.text.trim().ifEmpty { null }

        set(settings, value)
    }

    override fun resetFrom(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        c.text = get(settings) ?: ""
    }
}
