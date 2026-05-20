/**
 * Optional mapping between persisted values and UI/CLI strings.
 */
package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project

/**
 * Maps a persisted list element to panel input and CLI argv text.
 *
 */
internal interface OptionIo<T> {
    /**
     * Text shown for [stored] in a [ListPanel] row.
     */
    fun toInput(project: Project, stored: T): String

    /**
     * Persisted value parsed from a panel row, or null when empty.
     */
    fun fromInput(project: Project, input: String): T?

    /**
     * One argv token emitted for [stored] on the CLI.
     */
    fun toOutput(project: Project, stored: T): String
}
