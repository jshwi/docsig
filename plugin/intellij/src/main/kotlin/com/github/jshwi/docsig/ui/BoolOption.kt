/**
 * Data class for a boolean option.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.components.JBCheckBox
import com.intellij.ui.dsl.builder.Panel

/**
 * Toggle that maps directly to a single CLI flag when enabled.
 *
 * @param label Row label inside the grouped settings layout.
 * @param group Section title shared by related checkboxes.
 * @param summary Bundle key for helper text below the checkbox.
 * @param flag CLI argument inserted when the value is true.
 * @param get Reads the current persisted boolean for this option.
 * @param set Writes the boolean back into plugin settings state.
 */
internal data class BoolOption(
    override val label: String,
    override val group: String,
    override val summary: String,
    val flag: String,
    val get: (DocsigSettings) -> Boolean,
    val set: (DocsigSettings, Boolean) -> Unit,
) : Option {
    private var component: JBCheckBox? = null

    /**
     * Renders a single checkbox row
     *
     * Label is both control text and row key.
     */
    override fun Panel.render(project: Project) {
        val settings = docsigSettings(project)

        val checkBox =
            JBCheckBox(DocsigBundle.message(label)).apply {
                isSelected = get(settings)
            }

        component = checkBox

        row { cell(checkBox) }.applyOptionSummary(summary)
    }

    override fun apply(project: Project, add: (String) -> Unit) {
        val settings = docsigSettings(project)

        if (get(settings)) add(flag)
    }

    override fun isModified(project: Project): Boolean {
        val c = component ?: return false

        val settings = docsigSettings(project)

        return c.isSelected != get(settings)
    }

    override fun applyTo(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        set(settings, c.isSelected)
    }

    override fun resetFrom(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        c.isSelected = get(settings)
    }
}
