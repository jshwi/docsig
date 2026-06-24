package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.service.DocsigService
import com.intellij.openapi.options.SearchableConfigurable
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.panel
import javax.swing.JComponent

internal class DocsigConfigurable(private val project: Project) :
    SearchableConfigurable {
    private var options: Options? = null

    private fun ensureOptions(): List<Option> {
        options?.let { return it.entries }

        return Options(project).also { options = it }.entries
    }

    override fun getDisplayName(): String =
        DocsigBundle.message("configurable.display.name")

    override fun getId(): String = "docsig.settings"

    override fun createComponent(): JComponent = panel {
        val grouped = ensureOptions().groupBy { it.group }

        grouped.forEach { (group, opts) ->
            group(group.label) {
                opts.forEach { it.run { render() } }
            }
        }
    }

    override fun isModified(): Boolean =
        ensureOptions().any { it.isModified() }

    override fun apply() {
        ensureOptions().forEach { it.apply() }

        project
            .getService(DocsigService::class.java)
            .scheduleAfterSettingsChange()
    }

    override fun reset() {
        ensureOptions().forEach { it.reset() }
    }
}
