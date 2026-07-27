package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.models.Issue

/**
 * Merge fresh cli output with cached issues when a global error occurs.
 *
 * A cli-wide failure reports no line, so taking the fresh result whole
 * would wipe every line-specific marker until the next good run. Keep
 * the previous line-level issues in that case and append the new
 * non-line ones.
 *
 * @param previous Issues already cached for the path, if any.
 * @param issues Issues from the run that has just finished.
 * @return Issues to cache for the path.
 */
internal fun mergeIssues(
    previous: List<Issue>?,
    issues: List<Issue>,
): List<Issue> {
    val hasGlobalError = issues.any { it.exit == 2 && it.line == null }

    if (!hasGlobalError) return issues

    val prevLineIssues = previous.orEmpty().filter { it.line != null }

    return prevLineIssues + issues.filter { it.line == null }
}
