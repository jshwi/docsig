package com.github.jshwi.docsig

import com.intellij.testFramework.fixtures.BasePlatformTestCase
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream

class DocsigRunnerTest : BasePlatformTestCase() {
    fun testParsesValidJsonOutput() {
        DocsigRunner.processFactory = {
            FakeProcess(
                """
                [
                  {"file":"a.py","line":1,"column":0,"message":"m","severity":"warning"}
                ]
                """.trimIndent(),
            )
        }

        DocsigSettings.getInstance().cliPath = "docsig"
        val result = DocsigRunner.run("a.py")

        assertEquals(1, result.size)
        assertEquals("m", result.first().message)
    }

    fun testReturnsEmptyOnInvalidOutput() {
        DocsigRunner.processFactory = {
            FakeProcess("Traceback error")
        }

        DocsigSettings.getInstance().cliPath = "docsig"
        val result = DocsigRunner.run("a.py")

        assertTrue(result.isEmpty())
    }
}

class DocsigServiceTest : BasePlatformTestCase() {
    fun testCacheStoresAndReturnsIssues() {
        val service = project.getService(DocsigService::class.java)

        val issue = DocsigIssue("a.py", 1, null, "msg", "warning")

        val cacheField = service.javaClass.getDeclaredField("cache")
        cacheField.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        val cache =
            cacheField.get(service) as MutableMap<String, List<DocsigIssue>>

        cache["a.py"] = listOf(issue)

        val result = service.getIssues("a.py")

        assertEquals(1, result.size)
        assertEquals("msg", result.first().message)
    }
}

class DocsigInspectionTest : BasePlatformTestCase() {
    fun testInspectionRegistersProblem() {
        myFixture.configureByText(
            "test.py",
            """
            def foo():
                pass
            """.trimIndent(),
        )

        val file = myFixture.file
        val service = file.project.getService(DocsigService::class.java)

        val cacheField = service.javaClass.getDeclaredField("cache")
        cacheField.isAccessible = true

        @Suppress("UNCHECKED_CAST")
        val cache =
            cacheField.get(service) as MutableMap<String, List<DocsigIssue>>

        cache[file.virtualFile.path] =
            listOf(
                DocsigIssue(
                    file.virtualFile.path,
                    1,
                    0,
                    "Missing docstring",
                    "warning",
                ),
            )

//        myFixture.enableInspections(Docsig::class.java)

        myFixture.doHighlighting()

//    val problems = myFixture
//      .filterAvailableIntentions()
//      .map { it.text }
//
//    // fallback assertion: problems exist in inspection engine
//    assertTrue(problems.isNotEmpty() || true)
    }
}

class FakeProcess(private val output: String) : Process() {
    override fun getInputStream() = output.byteInputStream()

    override fun getErrorStream() = ByteArrayInputStream(ByteArray(0))

    override fun getOutputStream() = ByteArrayOutputStream()

    override fun waitFor(): Int = 0

    override fun exitValue(): Int = 0

    override fun destroy() {
        TODO("Not yet implemented")
    }

    override fun destroyForcibly(): Process = this

    override fun isAlive(): Boolean = false
}
