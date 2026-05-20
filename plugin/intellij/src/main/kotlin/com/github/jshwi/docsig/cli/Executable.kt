/**
 * Get the docsig executable.
 *
 * Copy the bundled docsig pyz from the plugin classpath into the IDE
 * system directory when missing, and return the executable path.
 */
package com.github.jshwi.docsig.cli

import com.intellij.openapi.application.PathManager
import java.io.InputStream
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths

/**
 * Materialize the bundled CLI artifact next to the IDE system path.
 */
internal object Executable {
    private const val BUNDLE = "docsig.pyz"

    // tests can force the missing-resource branch without changing the
    // classpath
    internal var bundledPyzStreamProvider: (() -> InputStream?)? = null

    // if the stream provider has been set by a test return the mock
    // stream, otherwise look for and return the bundle
    private fun openBundledPyzStream(): InputStream? {
        bundledPyzStreamProvider?.let { return it() }

        // all application resources merged into one virtual filesystem
        // the jar contents become accessible through classpath lookup
        // the .pyz is inside the jar archive (this is the jvm
        // resource-loading api), it loads a file embedded inside the
        // application package
        // look from the root of the classpath (this does not mean "look
        // inside class executable"), the class is only used to access;
        // the classloader or package info
        // also note that resources inside jars are streams, not
        // filesystem files
        return Executable::class.java.getResourceAsStream("/$BUNDLE")
    }

    private fun extract(target: Path) {
        // get resource as stream (/docsig.pyz) from the plugin
        // classpath
        val resource =
            openBundledPyzStream()
                ?: error("missing bundled cli resource")

        // create the parent directory
        Files.createDirectories(target.parent)

        // copy the stream into target
        resource.use { input -> Files.copy(input, target) }

        // mark as executable so it can be run like a script entrypoint
        // (with the project’s python interpreter)
        target.toFile().setExecutable(true)
    }

    /**
     * Get the path to the docsig executable.
     *
     * If the executable doesn't exist, extract the bundled CLI artifact
     * to the system directory.
     *
     * Make sure the bundled docsig CLI (docsig.pyz) exists on disk
     * under the IDE’s system path, then returns the absolute path
     * string to that file so the plugin can pass it to Python.
     *
     * @return The path to the extracted executable.
     */
    fun path(): String {
        // path to the target that lives or will live next to other
        // ide-managed data, not inside the plugin jar
        val target = Paths.get(PathManager.getSystemPath(), BUNDLE)

        // if target doesn't exist, create it
        if (!Files.exists(target)) extract(target)

        return target.toString()
    }
}
