package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.SimpleListCellRenderer
import com.intellij.ui.dsl.builder.Panel
import javax.swing.DefaultComboBoxModel
import javax.swing.JList

internal data class EnumOption<T : Any>(
    override val project: Project,
    override val group: Group,
    override val title: String,
    override val summary: String,
    override val get: (DocsigSettings) -> T,
    override val set: (DocsigSettings, T) -> Unit,
    private val values: List<T>,
    override val flagOf: (T) -> String?,
    private val display: (T) -> String,
) : SettingsBoundOption.WithValueFlag<T> {
    private var component: ComboBox<T>? = null

    private val settings = project.getService(DocsigSettings::class.java)

    override fun Panel.render() {
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
                    text = if (value == null) "" else display(value)
                }
            }
        combo.item = get(settings)

        component = combo

        row(title) { cell(combo) }.comment(summary)
    }

    override fun add(add: (String) -> Unit) {
        flagOf(get(settings))?.let(add)
    }

    override fun isModified(): Boolean =
        component?.item?.let { it != get(settings) } ?: false

    override fun apply() {
        component?.item?.let { value ->
            if (value != get(settings)) {
                set(settings, value)
            }
        }
    }

    override fun reset() {
        component?.item = get(settings)
    }
}
