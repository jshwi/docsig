/**
 * Identity mapping between persisted values and UI/CLI strings.
 *
 * The same conversion is used in both directions between a stored value
 * and its string form, with no separate “settings shape” vs “CLI
 * shape.”
 */
package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project

/**
 * [OptionIo] that uses the same string form for input and output.
 */
internal class IdentityOptionIo<T : Any>(
    private val serialize: (T) -> String,
    private val parse: (String) -> T,
) : OptionIo<T> {
    // string shown in the list panel
    override fun toInput(project: Project, stored: T): String =
        serialize(stored)

    // string typed in the panel
    override fun fromInput(project: Project, input: String): T? {
        val trimmed = input.trim()

        if (trimmed.isEmpty()) return null

        return parse(trimmed)
    }

    // string passed to the cli for one list item
    override fun toOutput(project: Project, stored: T): String =
        serialize(stored).trim()
}
