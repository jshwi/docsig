/**
 * Data class for an issue emitted by the docsig CLI.
 */
package com.github.jshwi.docsig.models

/**
 * One issue emitted by the docsig CLI in JSON form.
 *
 * @property line The line number of the issue.
 * @property message The issue message.
 * @property exit The issue exit status.
 */
internal data class Issue(
    val line: Int?,
    val message: String,
    val exit: Int,
)
