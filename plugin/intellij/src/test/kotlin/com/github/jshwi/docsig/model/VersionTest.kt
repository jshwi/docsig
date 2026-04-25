package com.github.jshwi.docsig.model

import com.github.jshwi.docsig.util.extractVersion
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import kotlin.test.assertNull

class VersionTest {
    @Test
    fun `parse normal version`() {
        val v = Version.parse("1.2.3")
        assertEquals(1, v.major)
        assertEquals(2, v.minor)
        assertEquals(3, v.patch)
    }

    @Test
    fun `parse missing components default to zero`() {
        val v = Version.parse("1.2")
        assertEquals(1, v.major)
        assertEquals(2, v.minor)
        assertEquals(0, v.patch)
    }

    @Test
    fun `parse non-numeric components default to zero`() {
        val v = Version.parse("a.b.c")
        assertEquals(0, v.major)
        assertEquals(0, v.minor)
        assertEquals(0, v.patch)
    }

    @Test
    fun `parse mixed valid and invalid components`() {
        val v = Version.parse("1.x.3")
        assertEquals(1, v.major)
        assertEquals(0, v.minor)
        assertEquals(3, v.patch)
    }

    @Test
    fun `compare versions major wins`() {
        val a = Version(2, 0, 0)
        val b = Version(1, 999, 999)
        assertTrue(a > b)
    }

    @Test
    fun `compare versions minor wins when major equal`() {
        val a = Version(1, 2, 0)
        val b = Version(1, 1, 999)
        assertTrue(a > b)
    }

    @Test
    fun `compare versions patch wins when major and minor equal`() {
        val a = Version(1, 1, 2)
        val b = Version(1, 1, 1)
        assertTrue(a > b)
    }

    @Test
    fun `versions equal`() {
        val a = Version(1, 2, 3)
        val b = Version(1, 2, 3)
        assertEquals(0, a.compareTo(b))
    }

    @Test
    fun `toString formats correctly`() {
        val v = Version(3, 4, 5)
        assertEquals("3.4.5", v.toString())
    }
}

class ExtractVersionTest {
    @Test
    fun `extracts first version in text`() {
        val input = "docsig version 1.2.3 installed"
        assertEquals("1.2.3", extractVersion(input))
    }

    @Test
    fun `extracts first occurrence only`() {
        val input = "1.2.3 then later 4.5.6"
        assertEquals("1.2.3", extractVersion(input))
    }

    @Test
    fun `returns null when no version present`() {
        val input = "no version here"
        assertNull(extractVersion(input))
    }

    @Test
    fun `handles version embedded in complex text`() {
        val input = "error: docsig-2.10.7-beta (build)"
        assertEquals("2.10.7", extractVersion(input))
    }
}
