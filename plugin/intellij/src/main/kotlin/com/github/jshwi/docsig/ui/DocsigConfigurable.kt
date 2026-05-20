/**
 * IDE settings page for the docsig executable path and CLI flags.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.intellij.openapi.options.SearchableConfigurable
import com.intellij.openapi.project.Project
import com.intellij.openapi.project.ProjectManager
import com.intellij.ui.dsl.builder.panel
import javax.swing.JComponent

/**
 * Binds UI controls to docsig settings and validates the CLI binary.
 *
 * Widget maps let [isModified] compare the live form against storage.
 */
internal class DocsigConfigurable : SearchableConfigurable {
    private val project: Project?
        get() = ProjectManager.getInstance().openProjects.firstOrNull()

    /**
     * @return Human-readable node title in the settings tree.
     */
    override fun getDisplayName(): String =
        DocsigBundle.message("configurable.display.name")

    /**
     * @return Stable configurable id used by search and navigation.
     */
    override fun getId(): String = "docsig.settings"

    /**
     * Builds executable path, boolean, enum, and list option rows.
     *
     * @return Root panel hosted under Settings > Tools > Docsig.
     */
    override fun createComponent(): JComponent {
        val project = project ?: return panel {}

        return panel {
            val grouped =
                Options.default.entries.groupBy {
                    DocsigBundle.message(
                        it.group,
                    )
                }

            grouped.forEach { (groupName, opts) ->
                group(groupName) {
                    opts.forEach { it.run { render(project) } }
                }
            }
        }
    }

    /**
     * Detects differences between widgets and persisted settings.
     *
     * @return True when Apply should persist a new snapshot.
     */
    override fun isModified(): Boolean {
        val project = project ?: return false

        return Options.default.entries.any { it.isModified(project) }
    }

    /**
     * Copies widget values into persisted docsig settings.
     */
    override fun apply() {
        val project = project ?: return

        Options.default.entries.forEach { it.applyTo(project) }
    }

    /**
     * Reloads widgets from persisted docsig settings after cancel or reopen.
     */
    override fun reset() {
        val project = project ?: return

        Options.default.entries.forEach { it.resetFrom(project) }
    }
}
