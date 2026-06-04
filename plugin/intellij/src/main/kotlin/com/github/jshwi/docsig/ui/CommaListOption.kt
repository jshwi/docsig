package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project

internal class CommaListOption<T : Any>(
    project: Project,
    group: Group,
    label: String,
    summary: String,
    flag: String,
    get: (DocsigSettings) -> List<T>,
    set: (DocsigSettings, List<T>) -> Unit,
    io: OptionIo<T>,
) : ListOption<T>(project, group, label, summary, flag, get, set, io) {
    constructor(
        project: Project,
        group: Group,
        label: String,
        summary: String,
        flag: String,
        get: (DocsigSettings) -> List<T>,
        set: (DocsigSettings, List<T>) -> Unit,
        serialize: (T) -> String,
        parse: (String) -> T,
    ) : this(
        project,
        group,
        label,
        summary,
        flag,
        get,
        set,
        IdentityOptionIo(serialize, parse),
    )

    override fun add(add: (String) -> Unit) {
        val settings = project.getService(DocsigSettings::class.java)

        val list = get(settings)

        if (list.isNotEmpty()) {
            add(flag)

            add(list.joinToString(",") { io.toOutput(project, it) })
        }
    }
}
