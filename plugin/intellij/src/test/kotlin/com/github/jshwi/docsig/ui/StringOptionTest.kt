package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.ui.dsl.builder.panel
import io.mockk.every
import io.mockk.mockk
import io.mockk.unmockkAll
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
    fun teardown() {
        unmockkAll()
    }

    private fun bind(settings: DocsigSettings) {
        every {
            testProject.getService(DocsigSettings::class.java)
        } returns settings
    }

    private fun option(
        get: (DocsigSettings) -> String? = { null },
        set: (DocsigSettings, String?) -> Unit = { _, _ -> },
        normalize: (String) -> String = { it.trim() },
    ): StringOption = StringOption(
        project = testProject,
        group = Group.CHECK,
        title = "test",
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
                render()
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
                render()
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

        opt.add { out.add(it) }

        assertEquals(listOf("--flag", "value"), out)
    }

    @Test
    fun `apply skips when settings value is null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        val out = mutableListOf<String>()

        opt.add { out.add(it) }

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

        opt.add { out.add(it) }

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

        assertFalse(opt.isModified())
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

        assertTrue(opt.isModified())
    }

    @Test
    fun `isModified treats blank ui as null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        setComponent(opt, JTextField("   "))

        assertFalse(opt.isModified())
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

        opt.apply()

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

        opt.apply()

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

        opt.apply()

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

        opt.reset()
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

        opt.reset()

        assertEquals("fresh", field.text)
    }

    @Test
    fun `resetFrom clears text field when settings value is null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt = option()

        val field = JTextField("stale")
        setComponent(opt, field)

        opt.reset()

        assertEquals("", field.text)
    }
}
