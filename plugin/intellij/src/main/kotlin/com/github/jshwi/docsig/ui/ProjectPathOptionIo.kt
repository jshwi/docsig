/**
 * Path [OptionIo]: relative in settings, absolute on the CLI.
 */
package com.github.jshwi.docsig.ui

import com.intellij.openapi.project.Project
import java.nio.file.Path
import java.nio.file.Paths

/**
 * [OptionIo] for exclude paths stored relative to the project root.
 *
 * Panel input is normalized for portable storage; argv output is
 * resolved to an absolute path for docsig.
 */
internal class ProjectPathOptionIo : OptionIo<String> {
    override fun toInput(project: Project, stored: String): String = stored

    override fun fromInput(project: Project, input: String): String? {
        if (input.isEmpty()) return null

        val path = Paths.get(input.trim())

        val base =
            project.basePath?.let { Paths.get(it).normalize() }
                ?: return path.asPosixString()

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
            project.basePath?.let { Paths.get(it).normalize() }
                ?: return path.toAbsolutePath().normalize().asPosixString()

        return if (path.isAbsolute) {
            path
        } else {
            base.resolve(path)
        }.normalize().asPosixString()
    }

    private fun Path.asPosixString(): String = toString().replace('\\', '/')
}
