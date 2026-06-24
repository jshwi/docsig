package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.AlignX
import com.intellij.ui.dsl.builder.Panel
import javax.swing.JTextField

internal class StringOption(
    override val project: Project,
    override val group: Group,
    override val title: String,
    override val summary: String,
    override val flag: String,
    override val get: (DocsigSettings) -> String?,
    override val set: (DocsigSettings, String?) -> Unit,
    private val normalize: (String) -> String = { it.trim() },
) : SettingsBoundOption.WithFixedFlag<String?> {
    private var component: JTextField? = null

    private val settings = project.getService(DocsigSettings::class.java)

    override fun Panel.render() {
        val value = get(settings) ?: ""

        val field = JTextField().apply { text = value }

        component = field

        row(title) {
            cell(field).resizableColumn().align(AlignX.FILL)
        }.comment(summary)
    }

    override fun add(add: (String) -> Unit) {
        val value =
            get(settings)
                ?.let(normalize)
                ?.takeIf { it.isNotEmpty() }
                ?: return

        add(flag)

        add(value)
    }

    override fun isModified(): Boolean =
        component?.let { uiValue(it) != get(settings) } ?: false

    override fun apply() {
        component?.let { set(settings, uiValue(it)) }
    }

    override fun reset() {
        component?.text = get(settings).orEmpty()
    }

    private fun uiValue(field: JTextField): String? =
        field.text.trim().ifEmpty { null }
}
