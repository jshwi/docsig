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
val junitVersion = providers.gradleProperty("junitVersion").get()
val mockkVersion = providers.gradleProperty("mockkVersion").get()
dependencies {
    testImplementation(kotlin("test"))
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
    testImplementation("io.mockk:mockk:$mockkVersion")

    intellijPlatform {
        pycharm(providers.gradleProperty("pycharmVersion"))

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
            JavaLanguageVersion.of(
                providers
                    .gradleProperty("javaVersion")
                    .get()
                    .toInt(),
            ),
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
val sinceVersion = providers.gradleProperty("sinceVersion").get()
val untilVersion = providers.gradleProperty("untilVersion").get()
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
                    if (!containsAll(listOf(start, end))) {
                        throw GradleException(
                            "Plugin description section not found in " +
                                "README.md:\n$start ... $end",
                        )
                    }

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
    version.set(
        providers.gradleProperty("ktlintVersion"),
    )

    debug.set(false)
    verbose.set(true)

    android.set(false)

    outputToConsole.set(true)

    ignoreFailures.set(false)

    filter {
        exclude("**/build/**")
    }
}

// #####################################################################
// Detekt
detekt {
    toolVersion = providers.gradleProperty("detektVersion").get()

    buildUponDefaultConfig = true

    allRules = false

    config.setFrom(
        files("$rootDir/detekt.yaml"),
    )
}

tasks.withType<Detekt>().configureEach {
    setSource(
        files(
            "src/main/kotlin",
            "src/test/kotlin",
        ),
    )

    // Required for IntelliJ plugin projects
    classpath.setFrom(files())
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
