/**
 * JSON models used to communicate with the docsig CLI.
 */
package com.github.jshwi.docsig.model

/**
 * Result from a completed command.
 */
data class CommandResult(
    val exit: Int,
    val out: String,
)

/**
 * One issue emitted by the docsig CLI in JSON form.
 */
data class Issue(
    val line: Int?,
    val message: String,
    val exit: Int,
)

/**
 * Value type for dotted semver-like versions.
 */
data class Version(
    val major: Int,
    val minor: Int,
    val patch: Int,
) : Comparable<Version> {
    override fun compareTo(other: Version): Int =
        compareValuesBy(
            this,
            other,
            { it.major },
            { it.minor },
            { it.patch },
        )

    override fun toString(): String =
        "$major.$minor.$patch"

    companion object {
        /**
         * Parses dotted segments; missing parts become zero.
         */
        fun parse(string: String): Version {
            val (major, minor, patch) =
                string
                    .split(".")
                    .map { it.toIntOrNull() ?: 0 }
                    .let { it + List(3 - it.size) { 0 } }

            return Version(major, minor, patch)
        }
    }
}
