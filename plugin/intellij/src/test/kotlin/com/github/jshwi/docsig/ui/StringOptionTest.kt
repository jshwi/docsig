package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.panel
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import javax.swing.JTextField
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Tests for [StringOption] text field binding, argv emission, and dirty
 * tracking.
 */
class StringOptionTest {
    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun resetSettingsProvider() {
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
    }

    private fun bind(settings: DocsigSettings) {
        DocsigSettings.settingsProvider = { settings }
    }

    private fun option(
        get: (DocsigSettings) -> String? = { null },
        set: (DocsigSettings, String?) -> Unit = { _, _ -> },
        normalize: (String) -> String = { it.trim() },
    ): StringOption =
        StringOption(
            label = "test",
            group = "group",
            summary = "",
            flag = "--flag",
            get = get,
            set = set,
            normalize = normalize,
        )

    private fun component(opt: StringOption): JTextField {
        val field = StringOption::class.java.getDeclaredField("component")
        field.isAccessible = true
        return field.get(opt) as JTextField
    }

    private fun setComponent(opt: StringOption, field: JTextField) {
        val declared = StringOption::class.java.getDeclaredField("component")
        declared.isAccessible = true
        declared.set(opt, field)
    }

    @Test
    fun `render seeds text field from settings`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "hello" },
            )

        panel {
            with(opt) {
                render(testProject)
            }
        }

        assertEquals("hello", component(opt).text)
    }

    @Test
    fun `render uses empty string when settings value is null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        panel {
            with(opt) {
                render(testProject)
            }
        }

        assertEquals("", component(opt).text)
    }

    @Test
    fun `apply adds flag and normalized value`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "  value  " },
            )

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertEquals(listOf("--flag", "value"), out)
    }

    @Test
    fun `apply skips when settings value is null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertTrue(out.isEmpty())
    }

    @Test
    fun `apply skips empty value after normalize`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "   " },
            )

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertTrue(out.isEmpty())
    }

    @Test
    fun `isModified returns false when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "a" },
            )

        assertFalse(opt.isModified(testProject))
    }

    @Test
    fun `isModified detects text field change`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "stored" },
            )

        setComponent(opt, JTextField("edited"))

        assertTrue(opt.isModified(testProject))
    }

    @Test
    fun `isModified treats blank ui as null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        setComponent(opt, JTextField("   "))

        assertFalse(opt.isModified(testProject))
    }

    @Test
    fun `applyTo returns when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        var called = false

        val opt =
            option(
                set = { _, _ ->
                    called = true
                },
            )

        opt.applyTo(testProject)

        assertFalse(called)
    }

    @Test
    fun `applyTo writes trimmed value`() {
        val settings = DocsigSettings()
        bind(settings)

        var captured: String? = "old"

        val opt =
            option(
                get = { _: DocsigSettings -> captured },
                set = { _, value ->
                    captured = value
                },
            )

        setComponent(opt, JTextField("  new  "))

        opt.applyTo(testProject)

        assertEquals("new", captured)
    }

    @Test
    fun `applyTo writes null for blank text`() {
        val settings = DocsigSettings()
        bind(settings)

        var captured: String? = "keep"

        val opt =
            option(
                get = { _: DocsigSettings -> captured },
                set = { _, value ->
                    captured = value
                },
            )

        setComponent(opt, JTextField("   "))

        opt.applyTo(testProject)

        assertNull(captured)
    }

    @Test
    fun `resetFrom returns when component missing`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "a" },
            )

        opt.resetFrom(testProject)
    }

    @Test
    fun `resetFrom updates text field from settings`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { _: DocsigSettings -> "fresh" },
            )

        val field = JTextField("stale")
        setComponent(opt, field)

        opt.resetFrom(testProject)

        assertEquals("fresh", field.text)
    }

    @Test
    fun `resetFrom clears text field when settings value is null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        val field = JTextField("stale")
        setComponent(opt, field)

        opt.resetFrom(testProject)

        assertEquals("", field.text)
    }
}
