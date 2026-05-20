/**
 * Shared list-panel wiring for multi-value CLI flags.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.AlignX
import com.intellij.ui.dsl.builder.Panel

/**
 * Base type for list-valued options edited as stacked text rows in a
 * [ListPanel].
 *
 * Subclasses define how values become argv fragments and how rows are
 * persisted.
 *
 * @param T Element type stored by the option list.
 * @property label Row label describing the list semantics.
 * @property group Section title for grouped layout in settings UI.
 * @property summary Bundle key for helper text below the list panel.
 * @property flag CLI list flag inserted before serialized values.
 * @property get Reads the current backing list for this row.
 * @property set Replaces the persisted list after user edits.
 * @property io Maps stored elements to panel rows and argv tokens.
 */
internal abstract class ListOption<T : Any>(
    override val label: String,
    override val group: String,
    override val summary: String,
    internal val flag: String,
    internal val get: (DocsigSettings) -> List<T>,
    internal val set: (DocsigSettings, List<T>) -> Unit,
    internal val io: OptionIo<T>,
) : Option {
    /**
     * The list panel component created by the settings UI.
     */
    protected var component: ListPanel? = null

    /**
     * Connects this row to the list panel created by the settings UI.
     *
     * @param project Project whose settings seed the list panel.
     */
    override fun Panel.render(project: Project) {
        val settings = docsigSettings(project)

        val initial = get(settings).map { io.toInput(project, it) }

        val panel = ListPanel(initial)

        component = panel

        group(label) {
            row {
                cell(panel).resizableColumn().align(AlignX.FILL)
            }.comment(summary)
        }
    }

    override fun isModified(project: Project): Boolean {
        val c = component ?: return false

        val settings = docsigSettings(project)

        return c.values() != get(settings).map { io.toInput(project, it) }
    }

    override fun resetFrom(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        c.setValues(get(settings).map { io.toInput(project, it) })
    }

    abstract override fun apply(project: Project, add: (String) -> Unit)

    abstract override fun applyTo(project: Project)
}
