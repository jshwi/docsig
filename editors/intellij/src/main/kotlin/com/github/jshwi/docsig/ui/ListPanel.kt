package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.intellij.icons.AllIcons
import javax.swing.Box
import javax.swing.BoxLayout
import javax.swing.JButton
import javax.swing.JPanel

internal class ListPanel(initial: List<String>) : JPanel() {
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

    private fun addRow(value: String, scheduleRefresh: Boolean = true) {
        val row = ListRow(value) { removeRow(it) }

        rows += row

        container.add(row)

        container.add(verticalSpacer())

        if (scheduleRefresh) refresh()

        row.focus()
    }

    private fun removeRow(row: ListRow) {
        val containerIndex = container.components.indexOf(row)

        if (!rows.remove(row)) return

        if (containerIndex < 0) {
            refresh()
            return
        }

        container.remove(containerIndex)

        if (containerIndex < container.componentCount) {
            container.remove(containerIndex)
        }

        refresh()
    }

    private fun rebuild(values: List<String>) {
        rows.clear()

        container.removeAll()

        val source = values.ifEmpty { listOf("") }

        source.forEach { addRow(it, scheduleRefresh = false) }

        refresh()
    }

    private fun refresh() {
        container.revalidate()

        container.repaint()
    }

    private fun verticalSpacer() = Box.createVerticalStrut(LIST_PANEL_HEIGHT)

    fun values(): List<String> =
        rows.map { it.value() }.filter { it.isNotEmpty() }

    fun setValues(values: List<String>) = rebuild(values)

    companion object {
        private const val LIST_PANEL_HEIGHT = 6
    }
}
