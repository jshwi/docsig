import io.gitlab.arturbosch.detekt.Detekt
import org.jetbrains.changelog.markdownToHTML
import org.jetbrains.intellij.platform.gradle.TestFrameworkType
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("org.jetbrains.kotlin.jvm")
    id("org.jetbrains.intellij.platform")
    id("org.jetbrains.changelog")
    id("org.jlleitschuh.gradle.ktlint")
    id("org.jetbrains.kotlinx.kover")
    id("io.gitlab.arturbosch.detekt")
    id("org.jetbrains.dokka")
}

// #####################################################################
// Dependencies
dependencies {
    testImplementation(kotlin("test"))
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
    testImplementation("io.mockk:mockk:1.13.12")
    intellijPlatform {
        pycharm("2026.1")
        testFramework(TestFrameworkType.Platform)
        bundledPlugin("PythonCore")
        bundledPlugin("Pythonid")
    }
}

// #####################################################################
// Java / Kotlin
java {
    toolchain {
        languageVersion.set(
            JavaLanguageVersion.of(21),
        )
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_21)
    }
}

// #####################################################################
// IntelliJ Platform
intellijPlatform {
    pluginConfiguration {
        ideaVersion {
            sinceBuild
            untilBuild
        }
        description =
            providers.fileContents(
                layout.projectDirectory.file("README.md"),
            ).asText.map {
                val start = "<!-- Plugin description -->"
                val end = "<!-- Plugin description end -->"
                with(it.lines()) {
                    subList(
                        indexOf(start) + 1,
                        indexOf(end),
                    )
                        .joinToString("\n")
                        .let(::markdownToHTML)
                }
            }
    }
    pluginVerification {
        // python sdk types come from bundled pycharm plugins; the
        // verifier's downloaded ide images omit some module jars
        externalPrefixes.set(listOf("com.jetbrains.python"))
        ides {
            recommended()
        }
    }
}

// #####################################################################
// Ktlint
ktlint {
    version.set("1.2.1")
    debug.set(false)
    verbose.set(true)
    android.set(false)
    outputToConsole.set(true)
    ignoreFailures.set(false)
}

// #####################################################################
// Detekt
detekt {
    toolVersion = "1.23.6"
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(
        files("$rootDir/detekt.yaml"),
    )
}

tasks.withType<Detekt>().configureEach {
    // required for intellij plugin projects
    classpath.setFrom(files())
    setSource(
        files(
            "src/main/kotlin",
            "src/test/kotlin",
        ),
    )
}

tasks.detekt {
    reports {
        html.required.set(true)
        xml.required.set(true)
    }
}

// #####################################################################
// Kover
kover {
    reports {
        verify {
            rule {
                minBound(99)
            }
        }
    }
}

// #####################################################################
// Tasks
tasks {
    test {
        useJUnitPlatform()
    }

    runIde {
        systemProperty(
            "idea.log.debug.categories",
            "#com.github.jshwi.docsig",
        )
    }

    publishPlugin {
        dependsOn(patchChangelog)
    }

    named("detekt") {
        dependsOn(named("detektBaseline"))
    }
    runIde {
        environment("PATH", "/usr/bin")
    }
}

val buildPyz by tasks.registering(Exec::class) {
    workingDir = file("../../")
    commandLine(
        "make",
        "build/docsig.pyz",
    )
}

val bundleCli by tasks.registering(Copy::class) {
    dependsOn(buildPyz)

    from(
        rootProject.file(
            "../../build/docsig.pyz",
        ),
    )

    into(
        layout.buildDirectory.dir(
            "generated/resources/cli",
        ),
    )
}

sourceSets {
    main {
        resources {
            srcDir(bundleCli)
        }
    }
}
