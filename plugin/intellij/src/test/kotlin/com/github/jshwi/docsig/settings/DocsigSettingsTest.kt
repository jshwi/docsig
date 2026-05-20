package com.github.jshwi.docsig.settings

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

/**
 * Tests for [DocsigSettings] defaults and [DocsigState] round-trips.
 */
class DocsigSettingsTest {
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
