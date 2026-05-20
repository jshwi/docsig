/**
 * One editable text row plus remove control inside a [ListPanel].
 */
package com.github.jshwi.docsig.ui

import com.intellij.icons.AllIcons
import com.intellij.ui.components.JBTextField
import java.awt.Dimension
import javax.swing.Box
import javax.swing.BoxLayout
import javax.swing.JButton
import javax.swing.JPanel

/**
 * Single editable row with remove button.
 */
internal class ListRow(
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

    /**
     * @return The trimmed text from the text field.
     */
    fun value(): String = field.text.trim()

    /**
     * Requests focus on the text field.
     */
    fun focus() = field.requestFocusInWindow()

    companion object {
        private const val LIST_PANEL_WIDTH = 8
    }
}
