pluginManagement {
    plugins {
        id("io.gitlab.arturbosch.detekt") version "1.23.7" apply false
        id("org.jetbrains.kotlinx.kover") version "0.9.8" apply false
        id("com.google.devtools.ksp") version "2.3.2" apply false
    }

    repositories {
        google()
        gradlePluginPortal()
        maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
        mavenCentral()
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "Pokedex"
include(":android")
include(":desktop")
include(":shared")
