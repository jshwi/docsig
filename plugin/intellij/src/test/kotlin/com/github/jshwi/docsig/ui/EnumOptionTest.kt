package com.github.jshwi.docsig.ui

import com.github.jshwi.docsig.messages.DocsigBundle
import com.github.jshwi.docsig.settings.DocsigSettings
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.dsl.builder.panel
import io.mockk.mockk
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import javax.swing.DefaultComboBoxModel
import javax.swing.JLabel
import javax.swing.JList
import kotlin.test.assertEquals
import kotlin.test.assertFalse

/**
 * Tests for [EnumOption] combo wiring and CLI flag mapping.
 */
class EnumOptionTest {
    enum class TestEnum { A, B }

    private val testProject = mockk<Project>(relaxed = true)

    @AfterEach
    fun resetSettingsProvider() {
        DocsigSettings.settingsProvider =
            DocsigSettings.defaultSettingsProvider
    }

    private fun bind(settings: DocsigSettings) {
        DocsigSettings.settingsProvider = { settings }
    }

    private fun component(opt: EnumOption<TestEnum>): ComboBox<TestEnum> {
        val field = EnumOption::class.java.getDeclaredField("component")
        field.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        return field.get(opt) as ComboBox<TestEnum>
    }

    private fun option(
        get: () -> TestEnum,
        set: (TestEnum) -> Unit,
        flag: (TestEnum) -> String?,
    ): EnumOption<TestEnum> =
        EnumOption(
            label = "test",
            group = "group",
            summary = "",
            get = { get() },
            set = { _, v -> set(v) },
            values = listOf(TestEnum.A, TestEnum.B),
            flagOf = flag,
            display = { it.name },
        )

    @Test
    fun `render seeds combo from settings`() {
        val settings = DocsigSettings()
        bind(settings)

        var stored = TestEnum.B
        val opt =
            option(
                get = { stored },
                set = { stored = it },
                flag = { null },
            )

        panel {
            with(opt) {
                render(testProject)
            }
        }

        assertEquals(TestEnum.B, component(opt).item)
    }

    @Test
    fun `render cell renderer formats value and null`() {
        val settings = DocsigSettings()
        bind(settings)

        val opt =
            option(
                get = { TestEnum.A },
                set = {},
                flag = { null },
            )

        panel {
            with(opt) {
                render(testProject)
            }
        }

        val combo = component(opt)
        val list = JList<TestEnum>()
        val renderer = combo.renderer

        val withValue =
            renderer.getListCellRendererComponent(
                list,
                TestEnum.A,
                0,
                false,
                false,
            ) as JLabel

        assertEquals(DocsigBundle.message("A"), withValue.text)

        val empty =
            renderer.getListCellRendererComponent(
                list,
                null,
                0,
                false,
                false,
            ) as JLabel

        assertEquals("", empty.text)
    }

    @Test
    fun `apply emits flag`() {
        val settings = mockk<DocsigSettings>(relaxed = true)
        bind(settings)

        val opt =
            option(
                get = { TestEnum.A },
                set = {},
                flag = { "--a" },
            )

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertEquals(listOf("--a"), out)
    }

    @Test
    fun `apply skips null flag`() {
        val settings = mockk<DocsigSettings>(relaxed = true)
        bind(settings)

        val opt =
            option(
                get = { TestEnum.B },
                set = {},
                flag = { null },
            )

        val out = mutableListOf<String>()

        opt.apply(testProject) { out.add(it) }

        assertTrue(out.isEmpty())
    }

    @Test
    fun `isModified returns true when different`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        val opt =
            option(
                get = { TestEnum.A },
                set = {},
                flag = { "--a" },
            )

        val combo = ComboBox<TestEnum>()
        combo.model = DefaultComboBoxModel(arrayOf(TestEnum.B))
        combo.item = TestEnum.B

        val field = opt.javaClass.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, combo)

        assertTrue(opt.isModified(testProject))
    }

    @Test
    fun `isModified returns false when component missing`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        val opt =
            option(
                get = { TestEnum.A },
                set = {},
                flag = { "--a" },
            )

        assertFalse(opt.isModified(testProject))
    }

    @Test
    fun `applyTo returns when component missing`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        var called = false
        val opt =
            option(
                get = { TestEnum.A },
                set = {
                    called = true
                },
                flag = { "--a" },
            )

        opt.applyTo(testProject)

        assertFalse(called)
    }

    @Test
    fun `applyTo returns when selected item is null`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        var called = false
        val opt =
            option(
                get = { TestEnum.A },
                set = {
                    called = true
                },
                flag = { "--a" },
            )

        val combo = ComboBox<TestEnum>()
        combo.model = DefaultComboBoxModel()
        combo.item = null

        val field = opt.javaClass.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, combo)

        opt.applyTo(testProject)

        assertFalse(called)
    }

    @Test
    fun `applyTo does not write when unchanged`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        var called = false
        val opt =
            option(
                get = { TestEnum.B },
                set = {
                    called = true
                },
                flag = { "--b" },
            )

        val combo = ComboBox<TestEnum>()
        combo.model = DefaultComboBoxModel(arrayOf(TestEnum.B))
        combo.item = TestEnum.B

        val field = opt.javaClass.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, combo)

        opt.applyTo(testProject)

        assertFalse(called)
    }

    @Test
    fun `applyTo writes when changed`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        var stored = TestEnum.A
        val opt =
            option(
                get = { stored },
                set = { stored = it },
                flag = { "--x" },
            )

        val combo = ComboBox<TestEnum>()
        combo.model = DefaultComboBoxModel(arrayOf(TestEnum.A, TestEnum.B))
        combo.item = TestEnum.B

        val field = opt.javaClass.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, combo)

        opt.applyTo(testProject)

        assertEquals(TestEnum.B, stored)
    }

    @Test
    fun `resetFrom returns when component missing`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        val opt =
            option(
                get = { TestEnum.B },
                set = {},
                flag = { "--b" },
            )

        opt.resetFrom(testProject)
    }

    @Test
    fun `resetFrom updates selected item`() {
        val settings = mockk<DocsigSettings>()
        bind(settings)

        var stored = TestEnum.A
        val opt =
            option(
                get = { stored },
                set = { stored = it },
                flag = { "--x" },
            )

        val combo = ComboBox<TestEnum>()
        combo.model = DefaultComboBoxModel(arrayOf(TestEnum.A, TestEnum.B))
        combo.item = TestEnum.B

        val field = opt.javaClass.getDeclaredField("component")
        field.isAccessible = true
        field.set(opt, combo)

        assertTrue(opt.isModified(testProject))

        opt.resetFrom(testProject)
        assertEquals(TestEnum.A, combo.item)
        assertFalse(opt.isModified(testProject))
    }
}
