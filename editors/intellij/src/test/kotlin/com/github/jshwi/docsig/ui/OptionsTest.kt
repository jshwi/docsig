package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.dsl.builder.panel
import io.mockk.every
import io.mockk.mockk
import io.mockk.unmockkAll
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Test
import javax.swing.JLabel
import javax.swing.JList
import kotlin.test.assertEquals

/**
 * Smoke test that every option row from [Options] supports the option
 * lifecycle.
 */
class OptionsTest {
    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    @Test
    fun `all options execute lifecycle methods`() {
        val settings = DocsigSettings()
        every {
            testProject.getService(DocsigSettings::class.java)
        } returns settings

        val entries = Options(testProject).entries

        // render once so each option has a non-null component
        // applyTo then exercises the set lambdas defined in Options
        panel {
            entries.forEach { with(it) { render() } }
        }

        entries.forEach { option ->

            val args = mutableListOf<String>()

            option.add { args.add(it) }

            option.isModified()

            option.apply()

            option.reset()
        }
    }

    @Test
    fun `option table lambdas are exercised`() {
        val settings = DocsigSettings()
        every {
            testProject.getService(DocsigSettings::class.java)
        } returns settings

        val entries = Options(testProject).entries

        @Suppress("UNCHECKED_CAST")
        val classModeOpt =
            entries.first() as EnumOption<ClassCheckMode>
        classModeOpt.set(settings, ClassCheckMode.CLASS)
        assertEquals(ClassCheckMode.CLASS, classModeOpt.get(settings))

        // exercise the display lambda via the rendered cell renderer
        // since display is a private constructor parameter
        panel {
            with(classModeOpt) { render() }
        }
        assertEquals(
            DocsigBundle.message(
                "settings.options.class-checking-mode-check-class",
            ),
            renderedLabel(classModeOpt, ClassCheckMode.CLASS).text,
        )

        @Suppress("UNCHECKED_CAST")
        val disableOpt =
            entries.first {
                it.title ==
                    DocsigBundle.message(
                        "settings.options.messages-disable.title",
                    )
            } as CommaListOption<String>
        assertEquals(
            "x",
            disableOpt.io.toInput(testProject, "x"),
        )
        assertEquals(
            "y",
            disableOpt.io.fromInput(testProject, "y"),
        )

        @Suppress("UNCHECKED_CAST")
        val targetOpt =
            entries.first {
                it.title ==
                    DocsigBundle.message(
                        "settings.options.messages-target.title",
                    )
            } as CommaListOption<String>
        assertEquals(
            "a",
            targetOpt.io.toInput(testProject, "a"),
        )
        assertEquals(
            "b",
            targetOpt.io.fromInput(testProject, "b"),
        )

        @Suppress("UNCHECKED_CAST")
        val excludesOpt =
            entries.first {
                it.title ==
                    DocsigBundle.message(
                        "settings.options.file-discovery.exclude-path.title",
                    )
            } as WhitespaceListOption<String>
        assertEquals(
            "exclude/me",
            excludesOpt.io.toInput(testProject, "exclude/me"),
        )
        assertEquals(
            "exclude/me",
            excludesOpt.io.fromInput(testProject, "exclude/me"),
        )
    }

    @Suppress("SameParameterValue")
    private fun <T : Any> renderedLabel(
        opt: EnumOption<T>,
        value: T,
    ): JLabel {
        val field = EnumOption::class.java.getDeclaredField("component")
        field.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        val combo = field.get(opt) as ComboBox<T>

        return combo.renderer.getListCellRendererComponent(
            JList(),
            value,
            0,
            false,
            false,
        ) as JLabel
    }
}
