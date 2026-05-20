/**
 * Invoke the docsig CLI with settings-derived flags and parse JSON.
 */
package com.github.jshwi.docsig.cli

import com.fasterxml.jackson.core.JsonProcessingException
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.github.jshwi.docsig.models.Issue
import com.github.jshwi.docsig.ui.Options
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.project.Project

/**
 * Bridge IntelliJ settings to a subprocess and JSON issue payloads.
 */
internal class Cli(
    private val project: Project,
    private val python: Python = Python(project),
) {
    private val log = Logger.getInstance(Cli::class.java)

    /**
     * Check if a Python interpreter is available for the project.
     *
     * @return Whether interpreter is available.
     */
    fun isAvailable(): Boolean = python.path() != null

    /**
     * Check whether python version meets docsig's minimum.
     *
     * @return False when no interpreter is configured or the version is
     *     too old.
     */
    fun isPythonSupported(): Boolean = python.meetsMinimumVersion()

    /**
     * Run docsig on a single path with current settings flags.
     *
     * Deserializes JSON issues and returns empty on parse errors.
     *
     * @param file File or directory argument passed to the CLI.
     * @return Parsed issues, or empty when output is not valid JSON,
     *     when no interpreter is configured, or when the subprocess
     *     yields no JSON.
     */
    fun run(file: String): List<Issue> {
        val interpreter = python.path() ?: return emptyList()

        if (!python.versionSupported(interpreter)) return emptyList()

        val exe = Executable.path()

        val command =
            buildList {
                add(interpreter)
                add(exe)
                add(file)
                Options.default.entries.forEach { it.apply(project, ::add) }
            }

        log.debug(command.joinToString(" "))

        val res = Subprocess.run(command)

        if (res.out.isEmpty()) return emptyList()

        return try {
            jacksonObjectMapper().readValue(res.out)
        } catch (e: JsonProcessingException) {
            log.warn("parse failed path=$file output=${res.out}", e)

            emptyList()
        }
    }
}
