# detekt

## Metrics

* 9 number of properties

* 4 number of functions

* 0 number of classes

* 4 number of packages

* 5 number of kt files

## Complexity Report

* 98 lines of code (loc)

* 81 source lines of code (sloc)

* 37 logical lines of code (lloc)

* 1 comment lines of code (cloc)

* 6 cyclomatic complexity (mcc)

* 0 cognitive complexity

* 6 number of total code smells

* 1% comment source ratio

* 162 mcc per 1,000 lloc

* 162 code smells per 1,000 lloc

## Findings (6)

### naming, FunctionNaming (1)

Function names should follow the naming convention set in the configuration.

[Documentation](https://detekt.dev/docs/rules/naming#functionnaming)

* /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/ui/ContentView.kt:8:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
5  import com.mocoding.pokedex.ui.root.RootContent
6  
7  @Composable
8  internal fun ContentView(
!               ^ error
9      component: RootComponent,
10 ) {
11     RootContent(component)

```

### style, NewLineAtEndOfFile (4)

Checks whether files end with a line separator.

[Documentation](https://detekt.dev/docs/rules/style#newlineatendoffile)

* /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt:10:2
```
The file /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt is not ending with a new line.
```
```kotlin
7      override val main: CoroutineDispatcher = Dispatchers.Main
8      override val io: CoroutineDispatcher = Dispatchers.Default
9      override val unconfined: CoroutineDispatcher = Dispatchers.Unconfined
10 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/core/database/SqlDriverFactory.kt:10:2
```
The file /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/core/database/SqlDriverFactory.kt is not ending with a new line.
```
```kotlin
7  
8  actual fun Scope.sqlDriverFactory(): SqlDriver {
9      return NativeSqliteDriver(PokemonDatabase.Schema, "${DatabaseConstants.name}.db")
10 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt:8:2
```
The file /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt is not ending with a new line.
```
```kotlin
5  
6  actual fun createPlatformHttpClient(): HttpClient {
7      return HttpClient(Darwin)
8  }
!   ^ error

```

* /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/ui/ContentView.kt:12:2
```
The file /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/ui/ContentView.kt is not ending with a new line.
```
```kotlin
9      component: RootComponent,
10 ) {
11     RootContent(component)
12 }
!!  ^ error

```

### style, WildcardImport (1)

Wildcard imports should be replaced with imports using fully qualified class names. Wildcard imports can lead to naming conflicts. A library update can introduce naming clashes with your classes which results in compilation errors.

[Documentation](https://detekt.dev/docs/rules/style#wildcardimport)

* /tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/main.ios.kt:20:1
```
platform.UIKit.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
17 import com.mocoding.pokedex.ui.helper.LocalSafeArea
18 import com.mocoding.pokedex.ui.root.RootComponent
19 import com.mocoding.pokedex.ui.theme.PokedexTheme
20 import platform.UIKit.*
!! ^ error
21 
22 @Suppress("unused", "FunctionName")
23 fun MainViewController(

```

generated with [detekt version 1.23.7](https://detekt.dev/) on 2026-05-28 05:11:30 UTC
