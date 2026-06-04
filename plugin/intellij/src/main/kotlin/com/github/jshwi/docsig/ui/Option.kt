package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.Panel

internal sealed interface Option {
    val title: String
    val group: Group
    val summary: String
    val project: Project

    fun Panel.render()

    fun add(add: (String) -> Unit)

    fun isModified(): Boolean

    fun apply()

    fun reset()
}
