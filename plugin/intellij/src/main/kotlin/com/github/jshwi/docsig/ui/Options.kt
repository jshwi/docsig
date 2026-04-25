/**
 * Option row definitions shared by the settings UI and CLI runner.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.components.JBCheckBox
import com.intellij.ui.dsl.builder.AlignX
import com.intellij.ui.dsl.builder.Panel
import javax.swing.DefaultComboBoxModel
import javax.swing.JTextField

/**
 * Shared shape for settings rows grouped in the UI.
 *
 * @property label Short text shown beside each control.
 * @property group Section title used by the Kotlin UI DSL builder.
 */
sealed interface Option {
    val label: String
    val group: String

    fun Panel.render(settings: DocsigSettings)

    /**
     * Appends argv tokens for this row from persisted settings.
     *
     * @param settings Source of values for the current project.
     * @param add Callback invoked once per argv fragment to append.
     */
    fun apply(settings: DocsigSettings, add: (String) -> Unit)

    /**
     * True when the bound control disagrees with persisted settings.
     *
     * @param settings Snapshot used as the non-UI side of comparison.
     */
    fun isModified(settings: DocsigSettings): Boolean

    /**
     * Writes the bound control into [settings] for persistence.
     *
     * @param settings Settings to apply to.
     */
    fun applyTo(settings: DocsigSettings)

    /**
     * Reloads the bound control from [settings] after cancel or reopen.
     *
     * @param settings Settings to reset from.
     */
    fun resetFrom(settings: DocsigSettings)
}

/**
 * Toggle that maps directly to a single CLI flag when enabled.
 *
 * @param label Row label inside the grouped settings layout.
 * @param group Section title shared by related checkboxes.
 * @param flag CLI argument inserted when the value is true.
 * @param get Reads the current persisted boolean for this option.
 * @param set Writes the boolean back into plugin settings state.
 */
data class BoolOption(
    override val label: String,
    override val group: String,
    val flag: String,
    val get: (DocsigSettings) -> Boolean,
    val set: (DocsigSettings, Boolean) -> Unit,
) : Option {
    private var component: JBCheckBox? = null

    override fun Panel.render(settings: DocsigSettings) {
        val checkBox =
            JBCheckBox(label).apply {
                isSelected = get(settings)
            }

        component = checkBox

        row { cell(checkBox) }
    }

    override fun apply(settings: DocsigSettings, add: (String) -> Unit) {
        if (get(settings)) add(flag)
    }

    override fun isModified(settings: DocsigSettings): Boolean {
        val c = component ?: return false
        return c.isSelected != get(settings)
    }

    override fun applyTo(settings: DocsigSettings) {
        val c = component ?: return
        set(settings, c.isSelected)
    }

    override fun resetFrom(settings: DocsigSettings) {
        val c = component ?: return
        c.isSelected = get(settings)
    }
}

/**
 * Single string argument rendered as a text field.
 *
 * @param label Row label shown beside the input.
 * @param group Section title for grouped layout in settings UI.
 * @param flag CLI flag inserted before the value.
 * @param get Reads the current string from settings.
 * @param set Persists the updated string into settings.
 * @param normalize Optional transform before emitting (e.g. trim).
 */
data class StringOption(
    override val label: String,
    override val group: String,
    val flag: String,
    val get: (DocsigSettings) -> String?,
    val set: (DocsigSettings, String?) -> Unit,
    val normalize: (String) -> String = { it.trim() },
) : Option {
    private var component: JTextField? = null

    /**
     * Connects this row to the text field created by the settings UI.
     *
     * @param settings Settings to render panel from.
     */
    override fun Panel.render(settings: DocsigSettings) {
        val field =
            JTextField().apply {
                text = get(settings) ?: ""
            }

        component = field

        row(label) {
            cell(field).resizableColumn().align(AlignX.FILL)
        }
    }

    override fun apply(settings: DocsigSettings, add: (String) -> Unit) {
        val value = get(settings)?.let(normalize)?.takeIf { it.isNotEmpty() }
        if (value != null) {
            add(flag)
            add(value)
        }
    }

    override fun isModified(settings: DocsigSettings): Boolean {
        val c = component ?: return false
        val ui = c.text.trim().ifEmpty { null }
        return ui != get(settings)
    }

    override fun applyTo(settings: DocsigSettings) {
        val c = component ?: return
        val value = c.text.trim().ifEmpty { null }
        set(settings, value)
    }

    override fun resetFrom(settings: DocsigSettings) {
        val c = component ?: return
        c.text = get(settings) ?: ""
    }
}

/**
 * Single-choice setting rendered as a combo box.
 *
 * @param label Row label shown next to the combo control.
 * @param group Section title for grouped layout in settings UI.
 * @param get Reads the current choice from plugin settings state.
 * @param set Persists a newly selected enumeration constant.
 * @param values Legal choices shown in the combo box model.
 * @param flagOf Maps a choice to argv text, or null when omitted.
 * @param display Renders a choice as the visible list cell text.
 */
data class EnumOption<T : Any>(
    override val label: String,
    override val group: String,
    val get: (DocsigSettings) -> T,
    val set: (DocsigSettings, T) -> Unit,
    val values: List<T>,
    val flagOf: (T) -> String?,
    val display: (T) -> String,
) : Option {
    private var component: ComboBox<T>? = null

    /**
     * Connects this row to the combo box created by the settings UI.
     *
     * @param settings Settings to render panel from.
     */
    override fun Panel.render(settings: DocsigSettings) {
        val model = DefaultComboBoxModel<T>()

        values.forEach { model.addElement(it) }

        val combo = ComboBox(model)

        component = combo

        row(label) {
            cell(combo)
        }
    }

    override fun apply(settings: DocsigSettings, add: (String) -> Unit) {
        flagOf(get(settings))?.let(add)
    }

    override fun isModified(settings: DocsigSettings): Boolean {
        val c = component ?: return false
        return c.item != get(settings)
    }

    override fun applyTo(settings: DocsigSettings) {
        val c = component ?: return
        val value = c.item ?: return
        if (value != get(settings)) {
            set(settings, value)
        }
    }

    override fun resetFrom(settings: DocsigSettings) {
        val c = component ?: return
        c.item = get(settings)
    }
}

/**
 * Comma-separated list rendered as a text field.
 *
 * @param label Row label describing the list semantics.
 * @param group Section title for grouped layout in settings UI.
 * @param flag CLI list flag inserted before joined values.
 * @param get Reads the current backing list for this row.
 * @param set Replaces the persisted list after user edits.
 * @param serialize Turns each element into comma-separated argv text.
 * @param parse Parses one trimmed token back into a list element.
 */
data class ListOption<T : Any>(
    override val label: String,
    override val group: String,
    val flag: String,
    val get: (DocsigSettings) -> List<T>,
    val set: (DocsigSettings, List<T>) -> Unit,
    val serialize: (T) -> String,
    val parse: (String) -> T,
) : Option {
    private var component: ListPanel? = null

    /**
     * Connects this row to the list panel created by the settings UI.
     *
     * @param settings Settings to render panel from.
     */
    override fun Panel.render(settings: DocsigSettings) {
        val initial = get(settings).map(serialize)
        val panel = ListPanel(initial)
        component = panel
        group(label) {
            row {
                cell(panel).resizableColumn().align(AlignX.FILL)
            }
        }
    }

    override fun apply(settings: DocsigSettings, add: (String) -> Unit) {
        val list = get(settings)
        if (list.isNotEmpty()) {
            add(flag)
            add(list.joinToString(",") { serialize(it) })
        }
    }

    override fun isModified(settings: DocsigSettings): Boolean {
        val c = component ?: return false
        return c.values() != get(settings)
    }

    override fun applyTo(settings: DocsigSettings) {
        val c = component ?: return
        set(settings, c.values().map(parse))
    }

    override fun resetFrom(settings: DocsigSettings) {
        val c = component ?: return
        c.setValues(get(settings).map(serialize))
    }
}

/**
 * Maps class-check UI choices to optional CLI flags.
 *
 * @property label Combo box caption shown to the user.
 * @property flag CLI flag when present, or null when omitted.
 */
enum class ClassCheckMode(val label: String, val flag: String?) {
    NONE("None", null),
    CLASS("Check class", "--check-class"),
    CLASS_CONSTRUCTOR("Check class constructor", "--check-class-constructor"),
}

/**
 * Canonical option table backing the settings UI and command builder.
 *
 * Order defines CLI flag emission order in DocsigRunner.
 */
val options =
    listOf(
        EnumOption(
            "Class checking mode",
            "Check",
            { it.state.classCheckMode },
            { s, v -> s.state.classCheckMode = v },
            ClassCheckMode.entries,
            { it.flag },
            { it.label },
        ),
        BoolOption(
            "Dunders",
            "Check",
            "--check-dunders",
            { it.state.checkDunders },
            { s, v -> s.state.checkDunders = v },
        ),
        BoolOption(
            "Nested",
            "Check",
            "--check-nested",
            { it.state.checkNested },
            { s, v -> s.state.checkNested = v },
        ),
        BoolOption(
            "Overridden",
            "Check",
            "--check-overridden",
            { it.state.checkOverridden },
            { s, v -> s.state.checkOverridden = v },
        ),
        BoolOption(
            "Property returns",
            "Check",
            "--check-property-returns",
            { it.state.checkPropertyReturns },
            { s, v -> s.state.checkPropertyReturns = v },
        ),
        BoolOption(
            "Protected",
            "Check",
            "--check-protected",
            { it.state.checkProtected },
            { s, v -> s.state.checkProtected = v },
        ),
        BoolOption(
            "Args",
            "Ignore",
            "--ignore-args",
            { it.state.ignoreArgs },
            { s, v -> s.state.ignoreArgs = v },
        ),
        BoolOption(
            "Kwargs",
            "Ignore",
            "--ignore-kwargs",
            { it.state.ignoreKwargs },
            { s, v -> s.state.ignoreKwargs = v },
        ),
        BoolOption(
            "No params",
            "Ignore",
            "--ignore-no-params",
            { it.state.ignoreNoParams },
            { s, v -> s.state.ignoreNoParams = v },
        ),
        BoolOption(
            "Include ignored",
            "File discovery",
            "--include-ignored",
            { it.state.includeIgnored },
            { s, v -> s.state.includeIgnored = v },
        ),
        StringOption(
            "Exclude pattern",
            "File discovery",
            "--exclude",
            { it.state.exclude },
            { s, v -> s.state.exclude = v },
        ),
        ListOption(
            "Disable",
            "Messages",
            "--disable",
            { it.state.disable },
            { s, v -> s.state.disable = v },
            { it },
            { it },
        ),
        ListOption(
            "Target",
            "Messages",
            "--target",
            { it.state.target },
            { s, v -> s.state.target = v },
            { it },
            { it },
        ),
    )
