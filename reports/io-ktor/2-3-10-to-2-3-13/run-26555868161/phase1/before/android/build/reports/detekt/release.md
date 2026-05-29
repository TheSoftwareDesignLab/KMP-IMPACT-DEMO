# detekt

## Metrics

* 1 number of properties

* 2 number of functions

* 1 number of classes

* 1 number of packages

* 1 number of kt files

## Complexity Report

* 40 lines of code (loc)

* 33 source lines of code (sloc)

* 16 logical lines of code (lloc)

* 0 comment lines of code (cloc)

* 2 cyclomatic complexity (mcc)

* 0 cognitive complexity

* 1 number of total code smells

* 0% comment source ratio

* 125 mcc per 1,000 lloc

* 62 code smells per 1,000 lloc

## Findings (1)

### style, NewLineAtEndOfFile (1)

Checks whether files end with a line separator.

[Documentation](https://detekt.dev/docs/rules/style#newlineatendoffile)

* /tmp/output/phase1/before/android/src/main/java/com/mocoding/pokedex/android/MainActivity.kt:40:2
```
The file /tmp/output/phase1/before/android/src/main/java/com/mocoding/pokedex/android/MainActivity.kt is not ending with a new line.
```
```kotlin
37         super.onDestroy()
38         stopKoin()
39     }
40 }
!!  ^ error

```

generated with [detekt version 1.23.7](https://detekt.dev/) on 2026-05-28 05:11:37 UTC
