import io.gitlab.arturbosch.detekt.Detekt
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
    id("io.gitlab.arturbosch.detekt")
}

dependencies {
    implementation("com.fasterxml.jackson.core:jackson-databind:2.22.0")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.18.3")
    testImplementation(kotlin("test"))
    testImplementation("org.junit.jupiter:junit-jupiter:6.1.0")
    testImplementation("junit:junit:4.13.2")
    testImplementation("io.mockk:mockk:1.14.11")
    intellijPlatform {
        pycharm("2026.1")
        testFramework(TestFrameworkType.Platform)
        bundledPlugin("PythonCore")
        bundledPlugin("Pythonid")
    }
}

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

intellijPlatform {
    pluginConfiguration {
        ideaVersion {
            sinceBuild
            untilBuild
        }
        description =
            providers
                .fileContents(layout.projectDirectory.file("README.md"))
                .asText
                .map {
                    val start = "<!-- Plugin description -->"
                    val end = "<!-- Plugin description end -->"
                    with(it.lines()) {
                        subList(
                            indexOf(start) + 1,
                            indexOf(end),
                        ).joinToString("\n")
                            .let(::markdownToHTML)
                    }
                }
        val changelog = project.changelog
        changeNotes =
            providers.gradleProperty("version").map { pluginVersion ->
                with(changelog) {
                    renderItem(
                        (
                            getOrNull(pluginVersion)
                                ?: getUnreleased()
                            )
                            .withHeader(false)
                            .withEmptySections(false),
                        Changelog.OutputType.HTML,
                    )
                }
            }
    }
    signing {
        certificateChain =
            providers.environmentVariable("CERTIFICATE_CHAIN")
        privateKey = providers.environmentVariable("PRIVATE_KEY")
        password =
            providers.environmentVariable("PRIVATE_KEY_PASSWORD")
    }
    publishing {
        token = providers.environmentVariable("PUBLISH_TOKEN")
    }
    pluginVerification {
        externalPrefixes.set(listOf("com.jetbrains.python"))
        ides {
            recommended()
        }
    }
}

changelog {
    groups.empty()
    repositoryUrl = providers.gradleProperty("pluginRepositoryUrl")
    versionPrefix = ""
}

ktlint {
    version.set("1.8.0")
    debug.set(false)
    verbose.set(true)
    android.set(false)
    outputToConsole.set(true)
    ignoreFailures.set(false)
}

detekt {
    toolVersion = "1.23.8"
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(
        files("$rootDir/detekt.yaml"),
    )
}

tasks.withType<Detekt>().configureEach {
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

kover {
    reports {
        verify {
            rule {
                minBound(99)
            }
        }
    }
}

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
    description = "Build bundled python cli"
    workingDir = file("../../")
    commandLine(
        "make",
        "build/docsig.pyz",
    )
}

val bundleCli by tasks.registering(Copy::class) {
    description = "Add bundled python cli"
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
