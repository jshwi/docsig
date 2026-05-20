/**
 * Run external commands and captures merged stdout/stderr.
 */
package com.github.jshwi.docsig.cli

import java.io.BufferedReader
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets

/**
 * Run a process to completion and expose exit status and output.
 */
internal object Subprocess {
    /**
     * Outcome from [run].
     *
     * @property exit Process exit status.
     * @property out Merged stdout and stderr text, trimmed.
     */
    data class Result(
        val exit: Int,
        val out: String,
    )

    /**
     * Build and start a process for a resolved argument list.
     *
     * Replace in tests to stub behavior without subprocesses.
     */
    var processFactory: (List<String>) -> Process = ::defaultProcessFactory

    internal fun defaultProcessFactory(cmd: List<String>): Process {
        val builder = ProcessBuilder(cmd)

        builder.environment()["DOCSIG_FORMAT_JSON"] = "true"

        builder.redirectErrorStream(true)

        return builder.start()
    }

    /**
     * Start a process using [processFactory].
     *
     * Wait for exit, and read UTF-8 output from the merged stream.
     */
    fun run(command: List<String>): Result {
        val process = processFactory(command)

        val out =
            BufferedReader(
                InputStreamReader(
                    process.inputStream,
                    StandardCharsets.UTF_8,
                ),
            ).use { it.readText().trim() }

        val exit = process.waitFor()

        return Result(exit, out)
    }
}
