package com.github.jshwi.docsig.ui

import org.junit.jupiter.api.Test
import javax.swing.JButton
import kotlin.test.assertEquals

/**
 * Tests for [ListPanel] row lifecycle and value round-trips.
 */
class ListPanelTest {
    @Test
    fun `setValues rebuilds list and covers line 98`() {
        val panel = ListPanel(listOf("a", "b"))

        panel.setValues(listOf("x", "y"))

        assertEquals(listOf("x", "y"), panel.values())
    }

    @Test
    fun `setValues with empty list creates single blank row`() {
        val panel = ListPanel(listOf("a"))

        panel.setValues(emptyList())

        assertEquals(emptyList(), panel.values())
    }

    @Test
    fun `values filters empty strings`() {
        val panel = ListPanel(listOf("a", "", "b"))

        assertEquals(listOf("a", "b"), panel.values())
    }

    @Test
    fun `add button triggers addRow and refresh path`() {
        val panel = ListPanel(emptyList())

        val addButton = findAddButton(panel)

        addButton.doClick()

        assertEquals(emptyList(), panel.values().filter { it.isNotBlank() })
    }

    @Test
    fun `remove row triggers refresh`() {
        val panel = ListPanel(listOf("a"))

        val rowsField = ListPanel::class.java.getDeclaredField("rows")
        rowsField.isAccessible = true

        val rows = rowsField.get(panel) as MutableList<*>

        val firstRow = rows.first()

        val method =
            ListPanel::class.java.getDeclaredMethod(
                "removeRow",
                firstRow!!::class.java,
            )

        method.isAccessible = true
        method.invoke(panel, firstRow)

        assertEquals(emptyList(), panel.values())
    }

    private fun findAddButton(panel: ListPanel): JButton {
        val components = panel.components
        return components.filterIsInstance<JButton>().first()
    }
}
