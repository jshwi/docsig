package com.github.jshwi.docsig.cli

import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets

internal object Subprocess {
    internal data class Result(
        internal val exit: Int,
        internal val out: String,
    )

    internal fun run(
        command: List<String>,
        workingDirectory: File? = null,
    ): Result {
        val builder = ProcessBuilder(command)

        workingDirectory?.let { builder.directory(it) }

        builder.environment()["_DOCSIG_FORMAT_JSON"] = "true"

        builder.redirectErrorStream(true)

        val proc = builder.start()

        val stream =
            InputStreamReader(
                proc.inputStream,
                StandardCharsets.UTF_8,
            )

        val out = BufferedReader(stream).use { it.readText().trim() }

        val exit = proc.waitFor()

        return Result(exit, out)
    }
}
