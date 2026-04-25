import org.jetbrains.changelog.Changelog
import org.jetbrains.changelog.markdownToHTML
import org.jetbrains.intellij.platform.gradle.TestFrameworkType
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("org.jetbrains.kotlin.jvm")
    id("org.jetbrains.intellij.platform")
    id("org.jetbrains.changelog")
    id("org.jlleitschuh.gradle.ktlint")
    id("org.jetbrains.kotlinx.kover")
    id("io.gitlab.arturbosch.detekt") version "1.23.6"
}

dependencies {
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.17.+")
    intellijPlatform {
        pycharm("2026.1")
        testFramework(TestFrameworkType.Platform)
    }
    testImplementation(kotlin("test"))
}

intellijPlatform {
    pluginConfiguration {
        description =
            providers.fileContents(
                layout.projectDirectory.file("README.md"),
            ).asText.map {
                val start = "<!-- Plugin description -->"
                val end = "<!-- Plugin description end -->"
                with(it.lines()) {
                    if (!containsAll(listOf(start, end))) {
                        throw GradleException(
                            "Plugin description section not found in" +
                                " README.md:\n$start ... $end",
                        )
                    }
                    subList(
                        indexOf(start) + 1,
                        indexOf(end),
                    ).joinToString("\n").let(::markdownToHTML)
                }
            }
        val changelog = project.changelog
        changeNotes =
            version.map { pluginVersion ->
                with(changelog) {
                    renderItem(
                        (getOrNull(pluginVersion) ?: getUnreleased())
                            .withHeader(false)
                            .withEmptySections(false),
                        Changelog.OutputType.HTML,
                    )
                }
            }
    }
}

changelog {
    groups.empty()
    repositoryUrl = providers.gradleProperty("pluginRepositoryUrl")
    versionPrefix = ""
}

tasks {
    publishPlugin {
        dependsOn(patchChangelog)
    }
}

tasks.runIde {
    systemProperty("idea.log.debug.categories", "#com.github.jshwi.docsig")
}

ktlint {
    version.set("1.2.1")
    debug.set(false)
    verbose.set(true)
    android.set(false)
    outputToConsole.set(true)
    ignoreFailures.set(false)
    filter {
        exclude("**/build/**")
    }
    additionalEditorconfig.set(
        mapOf(
            "max_line_length" to "88",
        ),
    )
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_21)
    }
}

detekt {
    toolVersion = "1.23.6"
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(files("$rootDir/detekt.yml"))
}

tasks.withType<io.gitlab.arturbosch.detekt.Detekt>().configureEach {
    setSource(files("src/main/kotlin", "src/test/kotlin"))

    // 🔑 critical for IntelliJ plugin projects
    classpath.setFrom(files())
}

tasks.detekt {
    reports {
        html.required.set(true)
        xml.required.set(true)
    }
}
