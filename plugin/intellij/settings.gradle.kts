import org.jetbrains.intellij.platform.gradle.extensions.intellijPlatform

rootProject.name = "docsig"

/**
 * Plugin resolution happens BEFORE build.gradle.kts executes.
 *
 * This is why plugin versions belong here instead of build.gradle.kts.
 */
pluginManagement {
    repositories {
        gradlePluginPortal()
        maven("https://cache-redirector.jetbrains.com/intellij-dependencies")
    }

    plugins {
        id("org.jetbrains.kotlin.jvm") version "2.3.0"
        id("org.jetbrains.intellij.platform") version "2.14.0"
        id("org.jetbrains.intellij.platform.settings") version "2.14.0"
        id("org.jetbrains.changelog") version "2.5.0"
        id("org.jlleitschuh.gradle.ktlint") version "14.2.0"
        id("org.jetbrains.kotlinx.kover") version "0.9.8"
        id("io.gitlab.arturbosch.detekt") version "1.23.6"
        id("org.jetbrains.dokka") version "2.2.0"
    }
}

/**
 * Defines repositories for NORMAL project dependencies.
 *
 * Example:
 * implementation(...)
 * testImplementation(...)
 */
plugins {
    id("org.jetbrains.intellij.platform.settings")
}

@Suppress("UnstableApiUsage")
dependencyResolutionManagement {
    repositories {
        mavenCentral()

        intellijPlatform {
            defaultRepositories()
        }
    }
}
