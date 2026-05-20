/**
 * Swing list editor for list-valued docsig CLI options.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.intellij.icons.AllIcons
import javax.swing.Box
import javax.swing.BoxLayout
import javax.swing.JButton
import javax.swing.JPanel

/**
 * Vertical list of text rows with add and remove for list-valued flags.
 *
 * @param initial Row strings shown after the panel is built; empty
 * yields one blank row so the user can type immediately.
 */
internal class ListPanel(
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
            text = DocsigBundle.message("list-panel.button.add")

            alignmentX = LEFT_ALIGNMENT

            addActionListener { addRow("") }
        }

    private fun addRow(value: String) {
        val row = ListRow(value) { removeRow(it) }

        rows += row

        container.add(row)

        // keeps vertical rhythm between rows consistent with rebuild()
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

        val source = values.ifEmpty { listOf("") }

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

    companion object {
        private const val LIST_PANEL_HEIGHT = 6
    }
}
