import org.jetbrains.compose.desktop.application.dsl.TargetFormat

plugins {
    id("com.google.devtools.ksp")
    id("org.jetbrains.kotlinx.kover")
    id("io.gitlab.arturbosch.detekt")
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.jetbrains.compose)
    alias(libs.plugins.kotlin.compose)
}

group = "com.mocoding"
version = "1.0.0-SNAPSHOT"

kotlin {
    jvmToolchain(11)

    jvm {
        withJava()
    }
    sourceSets {
        val jvmMain by getting {
            dependencies {
                implementation(project(":shared"))
                implementation(compose.desktop.currentOs)
            }
        }
        val jvmTest by getting
    }
}

compose.desktop {
    application {
        mainClass = "MainKt"
        nativeDistributions {
            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)
            packageName = "desktop"
            packageVersion = "1.0.0"
        }
    }
}

detekt {
    ignoreFailures = true
    buildUponDefaultConfig = true
    reports { xml { required.set(true) } }
}

dependencies {
    add("kspCommonMainMetadata", files("/home/runner/work/KMP-IMPACT-DEMO/KMP-IMPACT-DEMO/tools/kmp-impact-analyzer/tools/ksp/impact-analysis-processor.jar"))
}
