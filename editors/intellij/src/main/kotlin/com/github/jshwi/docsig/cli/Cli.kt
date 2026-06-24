package com.github.jshwi.docsig.cli

import com.fasterxml.jackson.core.JsonProcessingException
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.github.jshwi.docsig.models.Issue
import com.github.jshwi.docsig.ui.Options
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.project.Project
import java.io.File

internal class Cli(
    private val project: Project,
    private val python: Python = Python(project),
) {
    private val log = Logger.getInstance(Cli::class.java)

    internal fun isAvailable(): Boolean = python.path() != null

    internal fun isPythonSupported(): Boolean = python.meetsMinimumVersion()

    internal fun run(file: String): List<Issue> {
        val interpreter = python.path() ?: return emptyList()

        if (!python.meetsMinimumVersion()) return emptyList()

        val exe = Executable.path()

        val command =
            buildList {
                add(interpreter)
                add(exe)
                add(file)
                Options(project).entries.forEach { it.add(::add) }
            }

        log.debug(command.joinToString(" "))

        val cwd = project.basePath?.let { File(it) }

        val res = Subprocess.run(command, cwd)

        if (res.out.isEmpty()) return emptyList()

        return try {
            jacksonObjectMapper().readValue(res.out)
        } catch (e: JsonProcessingException) {
            log.warn("parse failed path=$file output=${res.out}", e)

            emptyList()
        }
    }
}
