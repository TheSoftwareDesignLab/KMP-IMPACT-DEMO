# detekt

## Metrics

* 4 number of properties

* 2 number of functions

* 0 number of classes

* 1 number of packages

* 1 number of kt files

## Complexity Report

* 49 lines of code (loc)

* 40 source lines of code (sloc)

* 22 logical lines of code (lloc)

* 0 comment lines of code (cloc)

* 2 cyclomatic complexity (mcc)

* 0 cognitive complexity

* 1 number of total code smells

* 0% comment source ratio

* 90 mcc per 1,000 lloc

* 45 code smells per 1,000 lloc

## Findings (1)

### style, NewLineAtEndOfFile (1)

Checks whether files end with a line separator.

[Documentation](https://detekt.dev/docs/rules/style#newlineatendoffile)

* /tmp/output/phase1/before/desktop/src/jvmMain/kotlin/Main.kt:49:2
```
The file /tmp/output/phase1/before/desktop/src/jvmMain/kotlin/Main.kt is not ending with a new line.
```
```kotlin
46 
47     @Suppress("UNCHECKED_CAST")
48     return result as T
49 }
!!  ^ error

```

generated with [detekt version 1.23.7](https://detekt.dev/) on 2026-05-29 02:13:49 UTC
