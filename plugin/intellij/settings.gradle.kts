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
        id("org.jetbrains.kotlin.jvm") version extra["kotlinVersion"] as String
        id("org.jetbrains.intellij.platform") version extra["intellijPlatformVersion"] as String
        id("org.jetbrains.intellij.platform.settings") version extra["intellijPlatformVersion"] as String
        id("org.jetbrains.changelog") version extra["changelogVersion"] as String
        id("org.jlleitschuh.gradle.ktlint") version extra["ktlintPluginVersion"] as String
        id("org.jetbrains.kotlinx.kover") version extra["koverVersion"] as String
        id("io.gitlab.arturbosch.detekt") version extra["detektVersion"] as String
        id("org.jetbrains.dokka") version extra["dokkaVersion"] as String
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
