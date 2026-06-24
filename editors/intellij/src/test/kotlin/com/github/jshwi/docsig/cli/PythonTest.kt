package com.github.jshwi.docsig.cli

import com.intellij.openapi.module.Module
import com.intellij.openapi.module.ModuleManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.projectRoots.Sdk
import com.intellij.openapi.roots.ProjectRootManager
import com.intellij.psi.util.CachedValueProvider
import com.intellij.psi.util.CachedValuesManager
import com.jetbrains.python.sdk.PythonSdkUtil
import io.mockk.every
import io.mockk.mockk
import io.mockk.mockkObject
import io.mockk.mockkStatic
import io.mockk.unmockkAll
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertNull
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

/**
 * Tests for [Python] interpreter resolution and platform caching.
 */
class PythonTest {
    @AfterEach
    fun teardown() {
        unmockkAll()
    }

    private fun mockCachedValuesManager(project: Project) {
        val valuesManager = mockk<CachedValuesManager>()
        val rootManager = mockk<ProjectRootManager>()

        mockkStatic(CachedValuesManager::class)
        mockkStatic(ProjectRootManager::class)

        every { CachedValuesManager.getManager(project) } returns valuesManager
        every { ProjectRootManager.getInstance(project) } returns rootManager

        every {
            valuesManager.getCachedValue(
                project,
                any<CachedValueProvider<*>>(),
            )
        } answers {
            val provider = secondArg<CachedValueProvider<*>>()
            provider.compute()!!.value
        }
    }

    @Test
    fun `path uses CachedValuesManager`() {
        val project = mockk<Project>()
        val module = mockk<Module>()
        val sdk = mockk<Sdk>()
        val moduleManager = mockk<ModuleManager>()

        mockCachedValuesManager(project)
        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns arrayOf(module)
        every { PythonSdkUtil.findPythonSdk(module) } returns sdk
        every { sdk.homePath } returns "/usr/bin/python3"

        assertEquals("/usr/bin/python3", Python(project).path())
    }

    @Test
    fun `meetsMinimumVersion uses CachedValuesManager`() {
        val project = mockk<Project>()
        val module = mockk<Module>()
        val sdk = mockk<Sdk>()
        val moduleManager = mockk<ModuleManager>()

        mockCachedValuesManager(project)
        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)
        mockkObject(Subprocess)

        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns arrayOf(module)
        every { PythonSdkUtil.findPythonSdk(module) } returns sdk
        every { sdk.homePath } returns "/usr/bin/python3"
        every { Subprocess.run(any(), any()) } returns Subprocess.Result(0, "")

        assertTrue(Python(project).meetsMinimumVersion())
    }

    @Test
    fun `path returns null when no interpreter`() {
        val project = mockk<Project>()
        val moduleManager = mockk<ModuleManager>()

        mockCachedValuesManager(project)
        mockkObject(ModuleManager.Companion)

        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns emptyArray()

        assertNull(Python(project).path())
    }

    @Test
    fun `versionSupported returns true when check exits zero`() {
        mockkObject(Subprocess)

        every { Subprocess.run(any(), any()) } answers {
            val cmd = firstArg<List<String>>()

            assertEquals("python3", cmd.first())
            assertEquals("-c", cmd[1])

            Subprocess.Result(0, "")
        }

        assertTrue(Python(mockk()).versionSupported("python3"))
    }

    @Test
    fun `versionSupported returns false when check exits non zero`() {
        mockkObject(Subprocess)

        every { Subprocess.run(any(), any()) } returns Subprocess.Result(1, "")

        assertFalse(Python(mockk()).versionSupported("python3"))
    }

    @Test
    fun `meetsMinimumVersion returns false when no interpreter`() {
        val project = mockk<Project>()
        val moduleManager = mockk<ModuleManager>()

        mockCachedValuesManager(project)
        mockkObject(ModuleManager.Companion)

        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns emptyArray()

        assertFalse(Python(project).meetsMinimumVersion())
    }
}
