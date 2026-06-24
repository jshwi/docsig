package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project

internal class IdentityOptionIo<T : Any>(
    private val serialize: (T) -> String,
    private val parse: (String) -> T,
) : OptionIo<T> {
    override fun toInput(project: Project, stored: T): String =
        serialize(stored)

    override fun fromInput(project: Project, input: String): T? {
        val trimmed = input.trim()

        if (trimmed.isEmpty()) return null

        return parse(trimmed)
    }

    override fun toOutput(project: Project, stored: T): String =
        serialize(stored).trim()
}
