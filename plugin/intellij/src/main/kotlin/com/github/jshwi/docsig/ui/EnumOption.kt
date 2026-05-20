/**
 * Data class for an enumeration option.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.SimpleListCellRenderer
import com.intellij.ui.dsl.builder.Panel
import javax.swing.DefaultComboBoxModel
import javax.swing.JList

/**
 * Single-choice setting rendered as a combo box.
 *
 * @param T Type represented by the combo box choices.
 * @property label Row label shown next to the combo control.
 * @property group Section title for grouped layout in settings UI.
 * @property summary Bundle key for helper text below the combo box.
 * @property get Reads the current choice from plugin settings state.
 * @property set Persists a newly selected enumeration constant.
 * @property values Legal choices shown in the combo box model.
 * @property flagOf Maps a choice to argv text, or null when omitted.
 * @property display Renders a choice as the visible list cell text.
 */
internal data class EnumOption<T : Any>(
    override val label: String,
    override val group: String,
    override val summary: String,
    val get: (DocsigSettings) -> T,
    val set: (DocsigSettings, T) -> Unit,
    val values: List<T>,
    val flagOf: (T) -> String?,
    val display: (T) -> String,
) : Option {
    private var component: ComboBox<T>? = null

    /**
     * Fills the model with [values] and selects the persisted choice.
     *
     * @param project Project whose settings select the combo value.
     */
    override fun Panel.render(project: Project) {
        val settings = docsigSettings(project)

        val model = DefaultComboBoxModel<T>()

        values.forEach { model.addElement(it) }

        val combo = ComboBox(model)

        combo.renderer =
            object : SimpleListCellRenderer<T>() {
                override fun customize(
                    list: JList<out T>,
                    value: T?,
                    index: Int,
                    selected: Boolean,
                    hasFocus: Boolean,
                ) {
                    text =
                        if (value == null) {
                            ""
                        } else {
                            DocsigBundle.message(display(value))
                        }
                }
            }

        combo.item = get(settings)

        component = combo

        row(DocsigBundle.message(label)) {
            cell(combo)
        }.applyOptionSummary(summary)
    }

    override fun apply(project: Project, add: (String) -> Unit) {
        val settings = docsigSettings(project)

        flagOf(get(settings))?.let(add)
    }

    override fun isModified(project: Project): Boolean {
        val c = component ?: return false

        val settings = docsigSettings(project)

        return c.item != get(settings)
    }

    override fun applyTo(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        val value = c.item ?: return

        if (value != get(settings)) {
            set(settings, value)
        }
    }

    override fun resetFrom(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        c.item = get(settings)
    }
}
