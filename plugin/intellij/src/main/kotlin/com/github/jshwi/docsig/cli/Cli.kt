/**
 * Invokes the docsig CLI with settings-derived flags and parses JSON.
 */
package com.github.jshwi.docsig.cli

import com.fasterxml.jackson.core.JsonProcessingException
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.github.jshwi.docsig.model.CommandResult
import com.github.jshwi.docsig.model.Issue
import com.github.jshwi.docsig.settings.DocsigSettings
import com.github.jshwi.docsig.ui.options
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.project.Project

/**
 * Bridges IntelliJ settings to a subprocess and JSON issue payloads.
 */
object Cli {
    private val log = Logger.getInstance(Cli::class.java)

    // supplies settings when building cli argument lists
    // replace in tests to avoid touching application services
    internal var settingsProvider: (Project) -> DocsigSettings = {
        DocsigSettings.getInstance(it)
    }

    /**
     * Builds and starts a process for a resolved argument list.
     *
     * Replace in tests to stub CLI behavior without subprocesses.
     */
    var processFactory: (List<String>) -> Process = { cmd ->
        ProcessBuilder(cmd)
            .apply {
                environment()["DOCSIG_FORMAT_JSON"] = "true"
                redirectErrorStream(true)
            }
            .start()
    }

    // builds argv with executable, path, then active option flags
    private fun buildCommand(
        settings: DocsigSettings,
        file: String,
    ): List<String> {
        return buildList {
            add(settings.state.cliPath)
            add(file)
            options.forEach { it.apply(settings, ::add) }
        }.also { log.debug("$it") }
    }

    // runs a process to completion and collects merged stdout/stderr
    private fun execute(command: List<String>): CommandResult {
        val process = processFactory(command)

        val out =
            process.inputStream
                .bufferedReader(Charsets.UTF_8)
                .use { it.readText().trim() }

        val exit = process.waitFor()

        return CommandResult(exit, out)
    }

    /**
     * Run docsig on a single path with current settings flags.
     *
     * Deserializes JSON issues and returns empty on parse errors.
     *
     * @param project The current project.
     * @param path File or directory argument passed to the CLI.
     * @return Parsed issues, or empty when output is not valid JSON.
     */
    fun run(project: Project, path: String): List<Issue> {
        val settings = settingsProvider(project)

        val command = buildCommand(settings, path)

        val res = execute(command)

        return try {
            jacksonObjectMapper().readValue(res.out)
        } catch (e: JsonProcessingException) {
            log.warn("parse failed path=$path output=${res.out}", e)
            emptyList()
        }
    }
}
