import org.jetbrains.intellij.platform.gradle.extensions.intellijPlatform

rootProject.name = "docsig"

pluginManagement {
    repositories {
        gradlePluginPortal()
        maven("https://cache-redirector.jetbrains.com/intellij-dependencies")
    }

    plugins {
        id("org.jetbrains.kotlin.jvm") version "2.3.21"
        id("org.jetbrains.intellij.platform.settings") version "2.14.0"
        id("org.jetbrains.changelog") version "2.5.0"
        id("org.jlleitschuh.gradle.ktlint") version "14.2.0"
        id("org.jetbrains.kotlinx.kover") version "0.9.8"
        id("io.gitlab.arturbosch.detekt") version "1.23.8"
    }
}

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
