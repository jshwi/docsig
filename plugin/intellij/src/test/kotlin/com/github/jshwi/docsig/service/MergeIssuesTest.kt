package com.github.jshwi.docsig.service

import com.github.jshwi.docsig.models.Issue
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

/**
 * The vscode extension and the neovim plugin merge the same way, so
 * these cases mirror theirs.
 */
class MergeIssuesTest {
    @Test
    fun `a clean run replaces the cache`() {
        val previous = listOf(Issue(1, "old", 1))
        val issues = listOf(Issue(2, "new", 1))

        assertEquals(issues, mergeIssues(previous, issues))
    }

    @Test
    fun `a global error keeps previous line issues`() {
        val previous = listOf(Issue(1, "old", 1), Issue(null, "stale", 2))
        val issues = listOf(Issue(null, "cli blew up", 2))

        assertEquals(
            listOf(Issue(1, "old", 1), Issue(null, "cli blew up", 2)),
            mergeIssues(previous, issues),
        )
    }

    @Test
    fun `a global error with no cache yields the new issues`() {
        val issues = listOf(Issue(null, "cli blew up", 2))

        assertEquals(issues, mergeIssues(null, issues))
    }

    @Test
    fun `a line level error is not treated as global`() {
        val previous = listOf(Issue(1, "old", 1))
        val issues = listOf(Issue(3, "syntax error", 2))

        assertEquals(issues, mergeIssues(previous, issues))
    }

    @Test
    fun `an empty run clears the cache`() {
        val previous = listOf(Issue(1, "old", 1))

        assertEquals(emptyList(), mergeIssues(previous, emptyList()))
    }
}
