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
        val trimmed = input.trim()

        if (trimmed.isEmpty()) return null

        val base =
            project.basePath?.let { Paths.get(it).normalize() }
                ?: return trimmed.replace('\\', '/')

        val normInput = trimmed.replace('\\', '/')

        val inputPath = Paths.get(normInput)

        val absolute =
            if (inputPath.isAbsolute) {
                inputPath.normalize()
            } else {
                base.resolve(normInput).normalize()
            }

        val stored =
            if (absolute.startsWith(base)) {
                base.relativize(absolute).asPosixString()
            } else {
                normInput
            }

        return stored.takeIf { it.isNotEmpty() }
    }

    override fun toOutput(project: Project, stored: String): String {
        val trimmed = stored.trim()

        if (trimmed.isEmpty()) return ""

        val base =
            project.basePath?.let { Paths.get(it).normalize() }
                ?: return Paths.get(
                    trimmed,
                ).toAbsolutePath().normalize().asPosixString()

        val path = Paths.get(trimmed.replace('\\', '/'))

        val resolved =
            (if (path.isAbsolute) path else base.resolve(path)).normalize()

        return resolved.asPosixString()
    }

    private fun Path.asPosixString(): String = toString().replace('\\', '/')
}
