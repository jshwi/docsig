package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project

internal interface OptionIo<T> {
    fun toInput(project: Project, stored: T): String

    fun fromInput(project: Project, input: String): T?

    fun toOutput(project: Project, stored: T): String
}
