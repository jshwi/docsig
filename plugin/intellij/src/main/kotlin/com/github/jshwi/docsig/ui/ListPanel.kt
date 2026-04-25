/**
 * Swing list editor for list-valued docsig CLI options.
 */
package com.github.jshwi.docsig.ui

import com.intellij.icons.AllIcons
import com.intellij.ui.components.JBTextField
import java.awt.Dimension
import javax.swing.Box
import javax.swing.BoxLayout
import javax.swing.JButton
import javax.swing.JPanel

private const val LIST_PANEL_HEIGHT = 6
private const val LIST_PANEL_WIDTH = 8

/**
 * Vertical list of text rows with add and remove for list-valued flags.
 *
 * @param initial The initial list panel string.
 */
class ListPanel(
    initial: List<String>,
) : JPanel() {
    private val rows = mutableListOf<ListRow>()
    private val container = JPanel()

    init {
        layout = BoxLayout(this, BoxLayout.Y_AXIS)
        alignmentX = LEFT_ALIGNMENT

        container.layout = BoxLayout(container, BoxLayout.Y_AXIS)
        container.alignmentX = LEFT_ALIGNMENT

        add(container)
        rebuild(initial)

        add(Box.createVerticalStrut(LIST_PANEL_HEIGHT))
        add(createAddButton())
    }

    private fun createAddButton(): JButton =
        JButton(AllIcons.General.Add).apply {
            text = "Add"
            alignmentX = LEFT_ALIGNMENT
            addActionListener { addRow("") }
        }

    private fun addRow(value: String) {
        val row = ListRow(value) { removeRow(it) }

        rows += row
        container.add(row)
        container.add(verticalSpacer())

        refresh()

        row.focus()
    }

    private fun removeRow(row: ListRow) {
        rows.remove(row)
        container.remove(row)
        refresh()
    }

    private fun rebuild(values: List<String>) {
        rows.clear()
        container.removeAll()

        val source = if (values.isEmpty()) listOf("") else values
        source.forEach { addRow(it) }

        refresh()
    }

    private fun refresh() {
        container.revalidate()
        container.repaint()
    }

    private fun verticalSpacer() = Box.createVerticalStrut(LIST_PANEL_HEIGHT)

    /**
     * Returns each row trimmed, omitting blanks, in visual order.
     */
    fun values(): List<String> =
        rows.map { it.value() }.filter { it.isNotEmpty() }

    /**
     * Rebuilds rows from persisted values; empty shows one blank row.
     */
    fun setValues(values: List<String>) {
        rebuild(values)
    }
}

/**
 * Single editable row with remove button.
 */
private class ListRow(
    initial: String,
    private val onRemove: (ListRow) -> Unit,
) : JPanel() {
    private val field = JBTextField(initial)

    init {
        layout = BoxLayout(this, BoxLayout.X_AXIS)
        alignmentX = LEFT_ALIGNMENT

        field.maximumSize =
            Dimension(Int.MAX_VALUE, field.preferredSize.height)

        add(field)
        add(Box.createHorizontalStrut(LIST_PANEL_WIDTH))
        add(createRemoveButton())
    }

    private fun createRemoveButton(): JButton =
        JButton(AllIcons.General.Remove).apply {
            maximumSize = preferredSize
            addActionListener { onRemove(this@ListRow) }
        }

    fun value(): String = field.text.trim()

    fun focus() {
        field.requestFocusInWindow()
    }
}
