package com.github.jshwi.docsig.cli

import com.intellij.openapi.application.PathManager
import com.intellij.openapi.diagnostic.Logger
import java.io.IOException
import java.io.InputStream
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption
import java.security.MessageDigest

/**
 * Bundled docsig checker extracted for subprocess invocation.
 *
 * The plugin JAR ships docsig.pyz as a classpath resource. This object
 * copies it into the IDE system directory so Python can execute it as a
 * file. A SHA-256 digest of the bundle decides whether an on-disk copy
 * is still current after a plugin update.
 */
internal object Executable {
    private val log = Logger.getInstance(Executable::class.java)

    private const val BUNDLE = "docsig.pyz"

    private const val BUFFER_SIZE = 8192

    // computed once per class load from the jar resource
    private val bundledDigest: ByteArray by lazy {
        openBundledStream().use(::digest)
    }

    private fun openBundledStream(): InputStream =
        // classloader reads docsig.pyz from the plugin jar resources
        Executable::class.java.classLoader.getResourceAsStream(BUNDLE)
            ?: error("missing bundled cli")

    private fun digest(input: InputStream): ByteArray {
        val digest = MessageDigest.getInstance("SHA-256")

        val buffer = ByteArray(BUFFER_SIZE)

        var read = input.read(buffer)

        // read returns -1 at eof; zero-length reads are skipped
        while (read >= 0) {
            if (read > 0) {
                digest.update(buffer, 0, read)
            }

            read = input.read(buffer)
        }

        return digest.digest()
    }

    private fun digest(path: Path): ByteArray? = try {
        Files.newInputStream(path).use(::digest)
    } catch (e: IOException) {
        log.warn(e)

        // unreadable cache is treated the same as a missing file
        null
    }

    private fun needsExtract(target: Path): Boolean {
        if (!Files.isRegularFile(target)) return true

        val cached = digest(target) ?: return true

        // isEqual avoids early exit on the first differing byte
        return !MessageDigest.isEqual(cached, bundledDigest)
    }

    private fun extract(target: Path) {
        Files.createDirectories(target.parent)

        val temp = Files.createTempFile(target.parent, BUNDLE, ".tmp")

        try {
            openBundledStream().use { input ->
                Files.copy(
                    input,
                    temp,
                    StandardCopyOption.REPLACE_EXISTING,
                )
            }

            // python must spawn the pyz as an executable file
            temp.toFile().setExecutable(true)

            // write via temp so a failed copy never leaves a half file
            Files.move(
                temp,
                target,
                StandardCopyOption.REPLACE_EXISTING,
                StandardCopyOption.ATOMIC_MOVE,
            )
        } catch (e: IOException) {
            Files.deleteIfExists(temp)

            throw e
        }
    }

    /**
     * Return the filesystem path to the bundled docsig executable.
     *
     * The file lives under the IDE system directory, not inside the
     * plugin JAR. Re-extract when missing or when the cached digest
     * differs from the bundled resource.
     */
    internal fun path(): String {
        // system path is writable and survives plugin jar replacement
        val target = Paths.get(PathManager.getSystemPath(), BUNDLE)

        if (needsExtract(target)) extract(target)

        return target.toString()
    }
}
