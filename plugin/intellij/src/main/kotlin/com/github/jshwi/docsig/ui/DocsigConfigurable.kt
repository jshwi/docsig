/**
 * IDE settings page for the docsig executable path and CLI flags.
 */
package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.cli.Cli
import com.github.jshwi.docsig.model.Version
import com.github.jshwi.docsig.settings.DocsigSettings
import com.github.jshwi.docsig.util.communicateError
import com.github.jshwi.docsig.util.communicateSuccess
import com.github.jshwi.docsig.util.extractVersion
import com.github.jshwi.docsig.util.runDocsigBackground
import com.intellij.openapi.fileChooser.FileChooser
import com.intellij.openapi.fileChooser.FileChooserDescriptor
import com.intellij.openapi.options.SearchableConfigurable
import com.intellij.openapi.project.Project
import com.intellij.openapi.project.ProjectManager
import com.intellij.openapi.ui.Messages
import com.intellij.openapi.ui.TextFieldWithBrowseButton
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.ui.dsl.builder.AlignX
import com.intellij.ui.dsl.builder.panel
import javax.swing.JComponent

private val MINIMUM_DOCSIG_VERSION = Version.parse("0.84.0")

/**
 * Binds UI controls to [DocsigSettings] and validates the CLI binary.
 *
 * Widget maps let [isModified] compare the live form against storage.
 */
class DocsigConfigurable : SearchableConfigurable {
    private val project: Project by lazy {
        ProjectManager.getInstance().openProjects.first()
    }
    private val field = TextFieldWithBrowseButton()

    /**
     * @return Human-readable node title in the settings tree.
     */
    override fun getDisplayName(): String = "Docsig"

    /**
     * @return Stable configurable id used by search and navigation.
     */
    override fun getId(): String = "docsig.settings"

    private fun com.intellij.ui.dsl.builder.Panel.executableRow() {
        row("Path to Docsig executable:") {
            cell(field).resizableColumn().align(AlignX.FILL)
            button("...") { chooseExecutable() }
            button("Test") { testExecutable() }
        }
    }

    @Suppress("removal", "DEPRECATION")
    private fun configureField() {
        field.addBrowseFolderListener(
            "Select Docsig Executable",
            null,
            null,
            FileChooserDescriptor(true, false, false, false, false, false),
        )
    }

    // opens a file chooser and copies the chosen path into the field
    private fun chooseExecutable() {
        val descriptor =
            FileChooserDescriptor(true, false, false, false, false, false)

        val file: VirtualFile? =
            FileChooser.chooseFile(descriptor, null, null)

        if (file != null) field.text = file.path
    }

    // validates path, semver, and minimum version on a worker thread
    private fun testExecutable() {
        val path = field.text.trim()
        if (path.isEmpty()) {
            Messages.showErrorDialog("Path is empty", "Docsig")
            return
        }

        runDocsigBackground {
            if (!isValidExecutable(path)) {
                communicateError("Not a valid Docsig executable")
                return@runDocsigBackground
            }

            val version = getExecutableVersion(path)
            if (version == null) {
                communicateError("Could not detect version")
                return@runDocsigBackground
            }

            if (version < MINIMUM_DOCSIG_VERSION) {
                communicateError(
                    "Configured Docsig executable version v$version is below" +
                        " the required minimum version" +
                        " v$MINIMUM_DOCSIG_VERSION",
                )
                return@runDocsigBackground
            }

            communicateSuccess()
        }
    }

    // runs --help and checks for a known docsig banner substring
    private fun isValidExecutable(path: String): Boolean {
        val marker = "Check signature params for proper documentation"
        val process = Cli.processFactory(listOf(path, "--help"))
        val output = process.inputStream.bufferedReader().readText()
        val exit = process.waitFor()
        return exit == 0 && marker in output
    }

    // parses semver from --version stdout for minimum version checks
    private fun getExecutableVersion(path: String): Version? {
        val process = Cli.processFactory(listOf(path, "--version"))
        val output = process.inputStream.bufferedReader().readText()
        process.waitFor()
        val versionStr = extractVersion(output) ?: return null
        return Version.parse(versionStr)
    }

    /**
     * Builds executable path, boolean, enum, and list option rows.
     *
     * @return Root panel hosted under Settings > Tools > Docsig.
     */
    override fun createComponent(): JComponent {
        val settings = DocsigSettings.getInstance(project)

        configureField()

        return panel {
            executableRow()

            val grouped = options.groupBy { it.group }
            grouped.forEach { (groupName, opts) ->
                group(groupName) {
                    opts.forEach { it.run { render(settings) } }
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
        val s = DocsigSettings.getInstance(project)

        return field.text != s.state.cliPath ||

            options.any { it.isModified(s) }
    }

    /**
     * Copies widget values into [DocsigSettings] application state.
     */
    override fun apply() {
        val s = DocsigSettings.getInstance(project)

        s.state.cliPath = field.text

        options.forEach { it.applyTo(s) }
    }

    /**
     * Reloads widgets from [DocsigSettings] after cancel or reopen.
     */
    override fun reset() {
        val s = DocsigSettings.getInstance(project)

        field.text = s.state.cliPath

        options.forEach { it.resetFrom(s) }
    }
}
