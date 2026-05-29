# detekt

## Metrics

* 4 number of properties

* 3 number of functions

* 0 number of classes

* 4 number of packages

* 4 number of kt files

## Complexity Report

* 50 lines of code (loc)

* 42 source lines of code (sloc)

* 16 logical lines of code (lloc)

* 0 comment lines of code (cloc)

* 3 cyclomatic complexity (mcc)

* 0 cognitive complexity

* 8 number of total code smells

* 0% comment source ratio

* 187 mcc per 1,000 lloc

* 500 code smells per 1,000 lloc

## Findings (8)

### coroutines, InjectDispatcher (2)

Don't hardcode dispatchers when creating new coroutines or calling `withContext`. Use dependency injection for dispatchers to make testing easier.

[Documentation](https://detekt.dev/docs/rules/coroutines#injectdispatcher)

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt:8:56
```
Dispatcher IO is used without dependency injection.
```
```kotlin
5  
6  actual val pokedexDispatchers: PokedexDispatchers = object: PokedexDispatchers {
7      override val main: CoroutineDispatcher = Dispatchers.Main.immediate
8      override val io: CoroutineDispatcher = Dispatchers.IO
!                                                         ^ error
9      override val unconfined: CoroutineDispatcher = Dispatchers.Unconfined
10 }

```

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt:9:64
```
Dispatcher Unconfined is used without dependency injection.
```
```kotlin
6  actual val pokedexDispatchers: PokedexDispatchers = object: PokedexDispatchers {
7      override val main: CoroutineDispatcher = Dispatchers.Main.immediate
8      override val io: CoroutineDispatcher = Dispatchers.IO
9      override val unconfined: CoroutineDispatcher = Dispatchers.Unconfined
!                                                                 ^ error
10 }

```

### naming, FunctionNaming (1)

Function names should follow the naming convention set in the configuration.

[Documentation](https://detekt.dev/docs/rules/naming#functionnaming)

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/ui/ContentView.kt:13:5
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
10 import com.mocoding.pokedex.ui.theme.PokedexTheme
11 
12 @Composable
13 fun ContentView(component: RootComponent) {
!!     ^ error
14     PokedexTheme {
15         Surface(
16             modifier = Modifier.fillMaxSize(),

```

### style, NewLineAtEndOfFile (4)

Checks whether files end with a line separator.

[Documentation](https://detekt.dev/docs/rules/style#newlineatendoffile)

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt:10:2
```
The file /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt is not ending with a new line.
```
```kotlin
7      override val main: CoroutineDispatcher = Dispatchers.Main.immediate
8      override val io: CoroutineDispatcher = Dispatchers.IO
9      override val unconfined: CoroutineDispatcher = Dispatchers.Unconfined
10 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/core/database/AndroidSqlDriverFactory.kt:10:2
```
The file /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/core/database/AndroidSqlDriverFactory.kt is not ending with a new line.
```
```kotlin
7  
8  actual fun Scope.sqlDriverFactory(): SqlDriver {
9      return AndroidSqliteDriver(PokemonDatabase.Schema, androidContext(), "${DatabaseConstants.name}.db")
10 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt:8:2
```
The file /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt is not ending with a new line.
```
```kotlin
5  
6  actual fun createPlatformHttpClient(): HttpClient {
7      return HttpClient(Android)
8  }
!   ^ error

```

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/ui/ContentView.kt:22:2
```
The file /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/ui/ContentView.kt is not ending with a new line.
```
```kotlin
19             RootContent(component)
20         }
21     }
22 }
!!  ^ error

```

### style, WildcardImport (1)

Wildcard imports should be replaced with imports using fully qualified class names. Wildcard imports can lead to naming conflicts. A library update can introduce naming clashes with your classes which results in compilation errors.

[Documentation](https://detekt.dev/docs/rules/style#wildcardimport)

* /tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt:3:1
```
io.ktor.client.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.core.network
2 
3 import io.ktor.client.*
! ^ error
4 import io.ktor.client.engine.android.Android
5 
6 actual fun createPlatformHttpClient(): HttpClient {

```

generated with [detekt version 1.23.7](https://detekt.dev/) on 2026-05-29 02:49:42 UTC
