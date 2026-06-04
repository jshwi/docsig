package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.components.JBCheckBox
import com.intellij.ui.dsl.builder.Panel

internal data class BoolOption(
    override val project: Project,
    override val group: Group,
    override val title: String,
    override val summary: String,
    override val flag: String,
    override val get: (DocsigSettings) -> Boolean,
    override val set: (DocsigSettings, Boolean) -> Unit,
) : SettingsBoundOption.WithFixedFlag<Boolean> {
    private var component: JBCheckBox? = null

    private val settings = project.getService(DocsigSettings::class.java)

    override fun Panel.render() {
        val checkBox = JBCheckBox(title).apply { isSelected = get(settings) }

        component = checkBox

        row { cell(checkBox) }.comment(summary)
    }

    override fun add(add: (String) -> Unit) {
        if (get(settings)) add(flag)
    }

    override fun isModified(): Boolean =
        component?.isSelected?.let { it != get(settings) } ?: false

    override fun apply() {
        component?.let { set(settings, it.isSelected) }
    }

    override fun reset() {
        component?.let { it.isSelected = get(settings) }
    }
}
