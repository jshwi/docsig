/**
 * List option emitted as separate argv tokens.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project

/**
 * List-valued CLI flag edited as stacked text rows in a [ListPanel].
 *
 * [apply] emits [flag] once, then one argv token per non-empty element
 * (no comma joining), for flags such as ``--excludes`` with
 * ``nargs="+"``.
 *
 * @param T Element type stored by the option list.
 * @param label Row label describing the list semantics.
 * @param group Section title for grouped layout in settings UI.
 * @param summary Bundle key for helper text below the list panel.
 * @param flag CLI list flag inserted before each serialized value.
 * @param get Reads the current backing list for this row.
 * @param set Replaces the persisted list after user edits.
 * @param io Maps stored elements to panel rows and argv tokens.
 */
internal class WhitespaceListOption<T : Any>(
    label: String,
    group: String,
    summary: String,
    flag: String,
    get: (DocsigSettings) -> List<T>,
    set: (DocsigSettings, List<T>) -> Unit,
    io: OptionIo<T>,
) : ListOption<T>(label, group, summary, flag, get, set, io) {
    constructor(
        label: String,
        group: String,
        summary: String,
        flag: String,
        get: (DocsigSettings) -> List<T>,
        set: (DocsigSettings, List<T>) -> Unit,
        serialize: (T) -> String,
        parse: (String) -> T,
    ) : this(
        label,
        group,
        summary,
        flag,
        get,
        set,
        IdentityOptionIo(serialize, parse),
    )

    override fun apply(project: Project, add: (String) -> Unit) {
        val settings = docsigSettings(project)

        val list = get(settings)

        if (list.isEmpty()) return

        add(flag)

        list.forEach { element ->
            val token = io.toOutput(project, element)

            if (token.isNotEmpty()) {
                add(token)
            }
        }
    }

    override fun applyTo(project: Project) {
        val c = component ?: return

        val settings = docsigSettings(project)

        val values =
            c.values().mapNotNull { io.fromInput(project, it) }

        set(settings, values)
    }
}
