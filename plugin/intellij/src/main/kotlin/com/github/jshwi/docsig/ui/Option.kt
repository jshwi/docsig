/**
 * Settings row types rendered under Tools > Docsig.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.Panel
import com.intellij.ui.dsl.builder.Row

/**
 * One settings row: UI binding, argv fragments, and dirty detection.
 *
 * Implementations resolve persisted values through [docsigSettings].
 */
internal sealed interface Option {
    /** Short text shown beside each control. */
    val label: String

    /** Section title used by the Kotlin UI DSL builder. */
    val group: String

    /** Bundle key for helper text shown below the control. */
    val summary: String

    /**
     * Resolves the project-level docsig settings service for this row.
     *
     * @param project Project whose settings are loaded.
     */
    fun docsigSettings(project: Project): DocsigSettings =
        DocsigSettings.getInstance(project)

    /**
     * Renders the option row in the settings UI.
     *
     * @param project Project whose docsig settings back this row.
     */
    fun Panel.render(project: Project)

    /**
     * Appends argv tokens for this row from persisted settings.
     *
     * @param project Project whose docsig settings supply values.
     * @param add Callback invoked once per argv fragment to append.
     */
    fun apply(project: Project, add: (String) -> Unit)

    /**
     * True when the bound control disagrees with persisted settings.
     *
     * @param project Project whose docsig settings are compared to the
     *     UI.
     */
    fun isModified(project: Project): Boolean

    /**
     * Writes the bound control into project docsig settings.
     *
     * @param project Project whose settings receive the UI snapshot.
     */
    fun applyTo(project: Project)

    /**
     * Reloads the bound control from project docsig settings after
     * cancel or reopen.
     *
     * @param project Project whose settings reload the widgets.
     */
    fun resetFrom(project: Project)
}

/**
 * Renders [summary] as a row comment when the bundle key is non-empty.
 */
internal fun Row.applyOptionSummary(summary: String) {
    if (summary.isNotEmpty()) {
        comment(DocsigBundle.message(summary))
    }
}
