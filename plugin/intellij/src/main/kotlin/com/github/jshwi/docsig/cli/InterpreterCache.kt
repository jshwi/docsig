/**
 * Cached interpreter path and minimum-version check result.
 */
package com.github.jshwi.docsig.cli

/**
 * Cached interpreter path and minimum-version check result.
 *
 * @property path Resolved interpreter executable path, if any.
 * @property meetsMinimum True when [path] satisfies the docsig minimum.
 */
internal data class InterpreterCache(
    val path: String?,
    val meetsMinimum: Boolean,
)
