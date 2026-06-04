package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.AlignX
import com.intellij.ui.dsl.builder.Panel

internal abstract class ListOption<T : Any>(
    override val project: Project,
    override val group: Group,
    override val title: String,
    override val summary: String,
    override val flag: String,
    override val get: (DocsigSettings) -> List<T>,
    override val set: (DocsigSettings, List<T>) -> Unit,
    internal val io: OptionIo<T>,
) : SettingsBoundOption.WithFixedFlag<List<T>> {
    protected var component: ListPanel? = null

    private val settings = project.getService(DocsigSettings::class.java)

    override fun Panel.render() {
        val panel = ListPanel(storedInputs())

        component = panel

        group(title) {
            row {
                cell(panel).resizableColumn().align(AlignX.FILL)
            }.comment(summary)
        }
    }

    override fun isModified(): Boolean {
        val c = component ?: return false

        return c.values() != storedInputs()
    }

    override fun apply() {
        component?.values()
            ?.mapNotNull { io.fromInput(project, it) }
            ?.let { set(settings, it) }
    }

    override fun reset() {
        component?.setValues(storedInputs())
    }

    abstract override fun add(add: (String) -> Unit)

    private fun storedInputs(): List<String> = get(settings).map {
        io.toInput(project, it)
    }
}
