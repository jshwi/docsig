package com.github.jshwi.docsig.settings

import com.github.jshwi.docsig.model.DocsigState
import com.github.jshwi.docsig.ui.ClassCheckMode
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class DocsigSettingsTest {
    @Test
    fun `default state is correctly initialized`() {
        val settings = DocsigSettings()

        val state = settings.state

        assertEquals("docsig", state.cliPath)
        assertEquals(ClassCheckMode.NONE, state.classCheckMode)
        assertFalse(state.checkDunders)
        assertFalse(state.checkNested)
        assertFalse(state.checkOverridden)
        assertFalse(state.checkPropertyReturns)
        assertFalse(state.checkProtected)

        assertFalse(state.ignoreArgs)
        assertFalse(state.ignoreKwargs)
        assertFalse(state.ignoreNoParams)

        assertFalse(state.includeIgnored)
        assertTrue(state.disable.isEmpty())
    }

    @Test
    fun `loadDocsigState replaces entire state object`() {
        val settings = DocsigSettings()

        val newState =
            DocsigState(
                cliPath = "/custom/path/docsig",
                classCheckMode = ClassCheckMode.CLASS,
                checkDunders = true,
                checkNested = true,
                checkOverridden = true,
                checkPropertyReturns = true,
                checkProtected = true,
                ignoreArgs = true,
                ignoreKwargs = true,
                ignoreNoParams = true,
                includeIgnored = true,
                exclude = ".*\\/src\\/__init__\\.py",
                disable = listOf("sig1", "sig2"),
                target = listOf("sig1", "sig2"),
            )

        settings.loadState(newState)

        val state = settings.getState()

        assertEquals("/custom/path/docsig", state.cliPath)
        assertEquals(ClassCheckMode.CLASS, state.classCheckMode)
        assertTrue(state.checkDunders)
        assertTrue(state.checkNested)
        assertTrue(state.checkOverridden)
        assertTrue(state.checkPropertyReturns)
        assertTrue(state.checkProtected)

        assertTrue(state.ignoreArgs)
        assertTrue(state.ignoreKwargs)
        assertTrue(state.ignoreNoParams)
        assertEquals(".*\\/src\\/__init__\\.py", state.exclude)
        assertTrue(state.includeIgnored)
        assertEquals(listOf("sig1", "sig2"), state.disable)
    }

    @Test
    fun `state mutation is reflected in persistent object`() {
        val settings = DocsigSettings()

        val state = settings.state
        state.cliPath = "changed"
        state.checkDunders = true
        state.disable = listOf("x")

        val retrieved = settings.state

        assertEquals("changed", retrieved.cliPath)
        assertTrue(retrieved.checkDunders)
        assertEquals(listOf("x"), retrieved.disable)
    }

    @Test
    fun `disable list is safely mutable via replacement`() {
        val settings = DocsigSettings()
        settings.loadState(
            DocsigState(disable = listOf("a", "b", "c")),
        )
        val state = settings.getState()
        assertEquals(3, state.disable.size)
        assertEquals("a", state.disable.first())
    }
}
