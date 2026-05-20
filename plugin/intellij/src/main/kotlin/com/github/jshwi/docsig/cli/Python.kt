/**
 * Resolve the configured Python interpreter for an IntelliJ project.
 */
package com.github.jshwi.docsig.cli

import com.intellij.openapi.module.ModuleManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.roots.ProjectRootManager
import com.intellij.psi.util.CachedValueProvider
import com.intellij.psi.util.CachedValuesManager
import com.jetbrains.python.sdk.PythonSdkUtil

/**
 * Resolve the Python interpreter for one project.
 */
internal class Python(private val project: Project) {
    private fun resolvePath(): String? {
        val module = ModuleManager.getInstance(project).modules.firstOrNull()

        val sdk = module?.let { PythonSdkUtil.findPythonSdk(it) }

        return sdk?.homePath
    }

    private fun resolveCache(): InterpreterCache {
        val path = resolvePath()

        return InterpreterCache(path, path != null && versionSupported(path))
    }

    private fun cache(): InterpreterCache {
        if (cacheBypassForTests) return resolveCache()

        return CachedValuesManager.getManager(project)
            .getCachedValue(project) {
                CachedValueProvider.Result.create(
                    resolveCache(),
                    ProjectRootManager.getInstance(project),
                )
            }
    }

    /**
     * Resolve the path to the Python interpreter for the project.
     *
     * Results are cached until the project SDK or module roots change.
     *
     * @return The path to the Python interpreter, or null if no
     *     interpreter is configured.
     */
    fun path(): String? = cache().path

    /**
     * Whether the configured interpreter meets the docsig minimum version.
     *
     * @return False when no interpreter is configured or the version is
     *     below [MINIMUM_MAJOR].[MINIMUM_MINOR].
     */
    fun meetsMinimumVersion(): Boolean = cache().meetsMinimum

    internal fun versionSupported(interpreter: String): Boolean {
        val res =
            Subprocess.run(listOf(interpreter, "-c", VERSION_CHECK_SCRIPT))

        return res.exit == 0
    }

    companion object {
        internal const val MINIMUM_MAJOR = 3

        internal const val MINIMUM_MINOR = 10

        private const val VERSION_CHECK_SCRIPT =
            "import sys; raise SystemExit(0 if sys.version_info >= " +
                "($MINIMUM_MAJOR, $MINIMUM_MINOR) else 1)"

        // when true, path and minimum version resolve on every call
        // (unit tests only)
        internal var cacheBypassForTests: Boolean = false
    }
}
