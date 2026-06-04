package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project
import java.nio.file.Path
import java.nio.file.Paths

internal class ProjectPathOptionIo : OptionIo<String> {
    override fun toInput(project: Project, stored: String): String = stored

    override fun fromInput(project: Project, input: String): String? {
        if (input.isEmpty()) return null

        val path = Paths.get(input.trim())

        val base = projectBase(project) ?: return path.asPosixString()

        val absolute = base.resolve(path)

        return if (absolute.startsWith(base)) {
            base.relativize(absolute)
        } else {
            path
        }.asPosixString().takeIf { it.isNotEmpty() }
    }

    override fun toOutput(project: Project, stored: String): String {
        if (stored.isEmpty()) return stored

        val path = Paths.get(stored.trim())

        val base =
            projectBase(project)
                ?: return path.toAbsolutePath().normalize().asPosixString()

        return if (path.isAbsolute) {
            path
        } else {
            base.resolve(path)
        }.normalize().asPosixString()
    }

    private fun projectBase(project: Project): Path? =
        project.basePath?.let { Paths.get(it).normalize() }

    private fun Path.asPosixString(): String = toString().replace('\\', '/')
}
