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
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test

/**
 * Tests for [Python] interpreter resolution and platform caching.
 */
class PythonTest {
    @BeforeEach
    fun setup() {
        Python.cacheBypassForTests = false
    }

    @AfterEach
    fun teardown() {
        Python.cacheBypassForTests = false
        Subprocess.processFactory = Subprocess::defaultProcessFactory
        unmockkAll()
    }

    @Test
    fun `path uses CachedValuesManager when not bypassing cache`() {
        val project = mockk<Project>()
        val module = mockk<Module>()
        val sdk = mockk<Sdk>()
        val moduleManager = mockk<ModuleManager>()
        val rootManager = mockk<ProjectRootManager>()
        val valuesManager = mockk<CachedValuesManager>()

        mockkStatic(CachedValuesManager::class)
        mockkStatic(ProjectRootManager::class)
        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        every { CachedValuesManager.getManager(project) } returns valuesManager
        every { ProjectRootManager.getInstance(project) } returns rootManager
        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns arrayOf(module)
        every { PythonSdkUtil.findPythonSdk(module) } returns sdk
        every { sdk.homePath } returns "/usr/bin/python3"

        every {
            valuesManager.getCachedValue(
                project,
                any<CachedValueProvider<InterpreterCache>>(),
            )
        } answers {
            val provider = secondArg<CachedValueProvider<InterpreterCache>>()
            provider.compute()!!.value
        }

        assertEquals("/usr/bin/python3", Python(project).path())
    }

    @Test
    fun `meetsMinimumVersion uses CachedValuesManager not bypassing cache`() {
        val project = mockk<Project>()
        val module = mockk<Module>()
        val sdk = mockk<Sdk>()
        val moduleManager = mockk<ModuleManager>()
        val rootManager = mockk<ProjectRootManager>()
        val valuesManager = mockk<CachedValuesManager>()

        mockkStatic(CachedValuesManager::class)
        mockkStatic(ProjectRootManager::class)
        mockkObject(ModuleManager.Companion)
        mockkStatic(PythonSdkUtil::class)

        every { CachedValuesManager.getManager(project) } returns valuesManager
        every { ProjectRootManager.getInstance(project) } returns rootManager
        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns arrayOf(module)
        every { PythonSdkUtil.findPythonSdk(module) } returns sdk
        every { sdk.homePath } returns "/usr/bin/python3"

        Subprocess.processFactory = {
            mockk<Process>().apply {
                every { inputStream } returns
                    java.io.ByteArrayInputStream(ByteArray(0))
                every { waitFor() } returns 0
            }
        }

        every {
            valuesManager.getCachedValue(
                project,
                any<CachedValueProvider<*>>(),
            )
        } answers {
            val provider = secondArg<CachedValueProvider<*>>()
            @Suppress("UNCHECKED_CAST")
            provider.compute()!!.value
        }

        assertTrue(Python(project).meetsMinimumVersion())
    }

    @Test
    fun `path bypasses cache in tests`() {
        Python.cacheBypassForTests = true

        val project = mockk<Project>()
        val moduleManager = mockk<ModuleManager>()

        mockkObject(ModuleManager.Companion)

        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns emptyArray()

        assertNull(Python(project).path())
    }

    @Test
    fun `versionSupported returns true when check exits zero`() {
        Subprocess.processFactory = { cmd ->
            assertEquals("python3", cmd.first())
            assertEquals("-c", cmd[1])

            mockk<Process>().apply {
                every { inputStream } returns
                    java.io.ByteArrayInputStream(ByteArray(0))
                every { waitFor() } returns 0
            }
        }

        assertTrue(Python(mockk()).versionSupported("python3"))
    }

    @Test
    fun `versionSupported returns false when check exits non zero`() {
        Subprocess.processFactory = {
            mockk<Process>().apply {
                every { inputStream } returns
                    java.io.ByteArrayInputStream(ByteArray(0))
                every { waitFor() } returns 1
            }
        }

        assertFalse(Python(mockk()).versionSupported("python3"))
    }

    @Test
    fun `meetsMinimumVersion returns false when no interpreter`() {
        Python.cacheBypassForTests = true

        val project = mockk<Project>()
        val moduleManager = mockk<ModuleManager>()

        mockkObject(ModuleManager.Companion)

        every { ModuleManager.getInstance(project) } returns moduleManager
        every { moduleManager.modules } returns emptyArray()

        assertFalse(Python(project).meetsMinimumVersion())
    }
}
