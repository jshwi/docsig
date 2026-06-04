package com.github.jshwi.docsig.cli

import com.intellij.openapi.module.ModuleManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.roots.ProjectRootManager
import com.intellij.psi.util.CachedValueProvider
import com.intellij.psi.util.CachedValuesManager
import com.jetbrains.python.sdk.PythonSdkUtil

internal class Python(private val project: Project) {
    private data class InterpreterCache(
        val path: String?,
        val meetsMinimum: Boolean,
    )

    private fun resolvePath(): String? {
        val module = ModuleManager.getInstance(project).modules.firstOrNull()

        val sdk = module?.let { PythonSdkUtil.findPythonSdk(it) }

        return sdk?.homePath
    }

    private fun resolveCache(): InterpreterCache {
        val path = resolvePath() ?: return InterpreterCache(null, false)

        return InterpreterCache(path, versionSupported(path))
    }

    private fun cache(): InterpreterCache = CachedValuesManager
        .getManager(project)
        .getCachedValue(project) {
            CachedValueProvider.Result.create(
                resolveCache(),
                ProjectRootManager.getInstance(project),
            )
        }

    internal fun path(): String? = cache().path

    internal fun meetsMinimumVersion(): Boolean = cache().meetsMinimum

    internal fun versionSupported(python: String): Boolean {
        val res = Subprocess.run(listOf(python, "-c", VERSION_CHECK_SCRIPT))

        return res.exit == 0
    }

    companion object {
        internal const val MIN_MAJOR = 3

        internal const val MIN_MINOR = 10

        private const val VERSION_CHECK_SCRIPT =
            "import sys;" +
                "min_versions = ($MIN_MAJOR, $MIN_MINOR);" +
                "sys.exit(0 if sys.version_info >= min_versions else 1)"
    }
}
