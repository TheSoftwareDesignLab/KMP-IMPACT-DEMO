# detekt

## Metrics

* 131 number of properties

* 110 number of functions

* 89 number of classes

* 35 number of packages

* 73 number of kt files

## Complexity Report

* 3,570 lines of code (loc)

* 3,092 source lines of code (sloc)

* 2,031 logical lines of code (lloc)

* 58 comment lines of code (cloc)

* 236 cyclomatic complexity (mcc)

* 99 cognitive complexity

* 258 number of total code smells

* 1% comment source ratio

* 116 mcc per 1,000 lloc

* 127 code smells per 1,000 lloc

## Findings (258)

### complexity, CyclomaticComplexMethod (1)

Prefer splitting up complex methods into smaller, easier to test methods.

[Documentation](https://detekt.dev/docs/rules/complexity#cyclomaticcomplexmethod)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/PokemonAbilityUtils.kt:8:10
```
The function getAbilityColor appears to be too complex based on Cyclomatic Complexity (complexity: 19). Defined complexity threshold for methods is set to '15'
```
```kotlin
5  
6  object PokemonAbilityUtils {
7  
8       fun getAbilityColor(name: String): Color = when(name) {
!           ^ error
9           "fighting" -> Fighting
10          "flying" -> Flying
11          "poison" -> Poison

```

### complexity, LongMethod (6)

One method should have one responsibility. Long methods tend to handle many things at once. Prefer smaller methods to make them easier to understand.

[Documentation](https://detekt.dev/docs/rules/complexity#longmethod)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:31:14
```
The function DetailsContent is too long (155). The maximum length is 60.
```
```kotlin
28 
29 @OptIn(ExperimentalMaterial3Api::class)
30 @Composable
31 internal fun DetailsContent(
!!              ^ error
32     state: DetailsStore.State,
33     onEvent: (DetailsStore.Intent) -> Unit,
34     onOutput: (DetailsComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:21:14
```
The function PokemonInfos is too long (70). The maximum length is 60.
```
```kotlin
18 import com.mocoding.pokedex.core.model.PokemonInfo
19 
20 @Composable
21 internal fun PokemonInfos(
!!              ^ error
22     pokemonInfo: PokemonInfo,
23     modifier: Modifier = Modifier
24 ) {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:19:14
```
The function FavoriteContent is too long (73). The maximum length is 60.
```
```kotlin
16 
17 @OptIn(ExperimentalMaterial3Api::class)
18 @Composable
19 internal fun FavoriteContent(
!!              ^ error
20     state: FavoriteStore.State,
21     onEvent: (FavoriteStore.Intent) -> Unit,
22     onOutput: (FavoriteComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:19:14
```
The function MainContent is too long (107). The maximum length is 60.
```
```kotlin
16 import com.mocoding.pokedex.ui.main.store.MainStore
17 
18 @Composable
19 internal fun MainContent(
!!              ^ error
20     state: MainStore.State,
21     onEvent: (MainStore.Intent) -> Unit,
22     onOutput: (MainComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt:20:14
```
The function PokedexContent is too long (72). The maximum length is 60.
```
```kotlin
17 
18 @OptIn(ExperimentalMaterial3Api::class)
19 @Composable
20 internal fun PokedexContent(
!!              ^ error
21     state: PokedexStore.State,
22     onEvent: (PokedexStore.Intent) -> Unit,
23     onOutput: (PokedexComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:22:14
```
The function PokemonItem is too long (64). The maximum length is 60.
```
```kotlin
19 
20 @OptIn(ExperimentalMaterial3Api::class)
21 @Composable
22 internal fun PokemonItem(
!!              ^ error
23     onClick: () -> Unit,
24     pokemon: Pokemon,
25     modifier: Modifier = Modifier,

```

### complexity, LongParameterList (2)

The more parameters a function has the more complex it is. Long parameter lists are often used to control complex algorithms and violate the Single Responsibility Principle. Prefer functions with short parameter lists.

[Documentation](https://detekt.dev/docs/rules/complexity#longparameterlist)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:63:32
```
The function MainContentDefault(state: MainStore.State, onEvent: (MainStore.Intent) -> Unit, onOutput: (MainComponent.Output) -> Unit, items: List<Pair<String, ImageVector>>, selectedItem: Pair<String, ImageVector>, updateSelectedItem: (Pair<String, ImageVector>) -> Unit) has too many parameters. The current threshold is set to 6.
```
```kotlin
60 
61 @OptIn(ExperimentalMaterial3Api::class)
62 @Composable
63 internal fun MainContentDefault(
!!                                ^ error
64     state: MainStore.State,
65     onEvent: (MainStore.Intent) -> Unit,
66     onOutput: (MainComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:120:30
```
The function MainContentLarge(state: MainStore.State, onEvent: (MainStore.Intent) -> Unit, onOutput: (MainComponent.Output) -> Unit, items: List<Pair<String, ImageVector>>, selectedItem: Pair<String, ImageVector>, updateSelectedItem: (Pair<String, ImageVector>) -> Unit) has too many parameters. The current threshold is set to 6.
```
```kotlin
117 
118 @OptIn(ExperimentalMaterial3Api::class)
119 @Composable
120 internal fun MainContentLarge(
!!!                              ^ error
121     state: MainStore.State,
122     onEvent: (MainStore.Intent) -> Unit,
123     onOutput: (MainComponent.Output) -> Unit,

```

### exceptions, PrintStackTrace (1)

Do not print a stack trace. These debug statements should be removed or replaced with a logger.

[Documentation](https://detekt.dev/docs/rules/exceptions#printstacktrace)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepositoryImpl.kt:38:13
```
Do not print a stack trace. These debug statements should be removed or replaced with a logger.
```
```kotlin
35                 Result.success(cachedPokemonList.map { it.toPokemon() })
36             }
37         } catch (e: Exception) {
38             e.printStackTrace()
!!             ^ error
39             Result.failure(e)
40         }
41     }

```

### exceptions, SwallowedException (2)

The caught exception is swallowed. The original exception could be lost.

[Documentation](https://detekt.dev/docs/rules/exceptions#swallowedexception)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:17:13
```
The caught exception is swallowed. The original exception could be lost.
```
```kotlin
14 
15     val result = try {
16         response()
17     } catch(e: IOException) {
!!             ^ error
18         throw PokedexException(PokedexError.ServiceUnavailable)
19     }
20 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:30:13
```
The caught exception is swallowed. The original exception could be lost.
```
```kotlin
27 
28     return@withContext try {
29         result.body()
30     } catch(e: Exception) {
!!             ^ error
31         throw PokedexException(PokedexError.ServerError)
32     }
33 

```

### exceptions, TooGenericExceptionCaught (3)

The caught exception is too generic. Prefer catching specific exceptions to the case that is currently handled.

[Documentation](https://detekt.dev/docs/rules/exceptions#toogenericexceptioncaught)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:30:13
```
The caught exception is too generic. Prefer catching specific exceptions to the case that is currently handled.
```
```kotlin
27 
28     return@withContext try {
29         result.body()
30     } catch(e: Exception) {
!!             ^ error
31         throw PokedexException(PokedexError.ServerError)
32     }
33 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepositoryImpl.kt:37:18
```
The caught exception is too generic. Prefer catching specific exceptions to the case that is currently handled.
```
```kotlin
34             } else {
35                 Result.success(cachedPokemonList.map { it.toPokemon() })
36             }
37         } catch (e: Exception) {
!!                  ^ error
38             e.printStackTrace()
39             Result.failure(e)
40         }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepositoryImpl.kt:55:18
```
The caught exception is too generic. Prefer catching specific exceptions to the case that is currently handled.
```
```kotlin
52             } else {
53                 Result.success(cachedPokemon.toPokemonInfo())
54             }
55         } catch (e: Exception) {
!!                  ^ error
56             Result.failure(e)
57         }
58     }

```

### naming, FunctionNaming (26)

Function names should follow the naming convention set in the configuration.

[Documentation](https://detekt.dev/docs/rules/naming#functionnaming)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonScreen.kt:19:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
16 
17 @OptIn(ExperimentalMaterial3Api::class)
18 @Composable
19 internal fun ComingSoonScreen(component: ComingSoonComponent) {
!!              ^ error
20 
21     Scaffold(
22         topBar = {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/DetailsScreen.kt:9:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
6  import com.mocoding.pokedex.ui.details.components.DetailsContent
7  
8  @Composable
9  internal fun DetailsScreen(component: DetailsComponent) {
!               ^ error
10 
11     val state by component.state.collectAsState()
12 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/AbilityItem.kt:15:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
12 import androidx.compose.ui.unit.dp
13 
14 @Composable
15 internal fun AbilityItem(
!!              ^ error
16     name: String,
17     containerColor: Color,
18     modifier: Modifier = Modifier,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/AbilityRow.kt:13:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
10 import com.mocoding.pokedex.ui.utils.PokemonAbilityUtils
11 
12 @Composable
13 internal fun AbilityRow(
!!              ^ error
14     types: List<PokemonInfo.TypeResponse>,
15     modifier: Modifier = Modifier,
16 ) {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:31:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
28 
29 @OptIn(ExperimentalMaterial3Api::class)
30 @Composable
31 internal fun DetailsContent(
!!              ^ error
32     state: DetailsStore.State,
33     onEvent: (DetailsStore.Intent) -> Unit,
34     onOutput: (DetailsComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:21:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
18 import com.mocoding.pokedex.core.model.PokemonInfo
19 
20 @Composable
21 internal fun PokemonInfos(
!!              ^ error
22     pokemonInfo: PokemonInfo,
23     modifier: Modifier = Modifier
24 ) {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:24:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
21 import kotlin.math.roundToInt
22 
23 @Composable
24 internal fun PokemonStatItem(
!!              ^ error
25     statResponse: PokemonInfo.StatsResponse,
26     modifier: Modifier = Modifier
27 ) {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStats.kt:11:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
8  import com.mocoding.pokedex.core.model.PokemonInfo
9  
10 @Composable
11 internal fun PokemonStats(
!!              ^ error
12     pokemonInfo: PokemonInfo,
13     modifier: Modifier = Modifier
14 ) {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/FavoriteScreen.kt:9:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
6  import com.mocoding.pokedex.ui.favorite.components.FavoriteContent
7  
8  @Composable
9  internal fun FavoriteScreen(favoriteComponent: FavoriteComponent) {
!               ^ error
10     val state by favoriteComponent.state.collectAsState()
11 
12     FavoriteContent(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:19:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
16 
17 @OptIn(ExperimentalMaterial3Api::class)
18 @Composable
19 internal fun FavoriteContent(
!!              ^ error
20     state: FavoriteStore.State,
21     onEvent: (FavoriteStore.Intent) -> Unit,
22     onOutput: (FavoriteComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:25:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
22 import kotlinx.coroutines.launch
23 
24 @Composable
25 internal fun MainScreen(component: MainComponent) {
!!              ^ error
26 
27     val state by component.state.collectAsState()
28 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:63:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
60 
61 @OptIn(ExperimentalMaterial3Api::class)
62 @Composable
63 internal fun MainContentDefault(
!!              ^ error
64     state: MainStore.State,
65     onEvent: (MainStore.Intent) -> Unit,
66     onOutput: (MainComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:120:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
117 
118 @OptIn(ExperimentalMaterial3Api::class)
119 @Composable
120 internal fun MainContentLarge(
!!!              ^ error
121     state: MainStore.State,
122     onEvent: (MainStore.Intent) -> Unit,
123     onOutput: (MainComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/AsyncImage.kt:23:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
20 
21 
22 @Composable
23 internal fun AsyncImage(
!!              ^ error
24     url: String,
25     contentDescription: String?,
26     contentScale: ContentScale = ContentScale.Fit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/CategoryButton.kt:21:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
18 import com.mocoding.pokedex.ui.theme.Black
19 
20 @Composable
21 internal fun CategoryButton(
!!              ^ error
22     onClick: () -> Unit,
23     categoryState: CategoryState,
24     modifier: Modifier = Modifier,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:19:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
16 import com.mocoding.pokedex.ui.main.store.MainStore
17 
18 @Composable
19 internal fun MainContent(
!!              ^ error
20     state: MainStore.State,
21     onEvent: (MainStore.Intent) -> Unit,
22     onOutput: (MainComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainModelDrawerSheet.kt:18:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
15 
16 @OptIn(ExperimentalMaterial3Api::class)
17 @Composable
18 internal fun MainModalDrawerSheet(
!!              ^ error
19     items: List<Pair<String, ImageVector>>,
20     selectedItem: Pair<String, ImageVector>,
21     onItemsClick: (Pair<String, ImageVector>) -> Unit

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt:24:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
21 import com.mocoding.pokedex.ui.theme.Black
22 
23 @Composable
24 internal fun VideoItem(
!!              ^ error
25     onClick: () -> Unit,
26     video: Video,
27     modifier: Modifier = Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoRow.kt:12:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
9  import com.mocoding.pokedex.core.model.Video
10 
11 @Composable
12 internal fun VideoRow(
!!              ^ error
13     videoList: List<Video>,
14     onVideoClicked: (id: String) -> Unit,
15     modifier: Modifier = Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/PokedexScreen.kt:9:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
6  import com.mocoding.pokedex.ui.pokedex.components.PokedexContent
7  
8  @Composable
9  internal fun PokedexScreen(component: PokedexComponent) {
!               ^ error
10 
11     val state by component.state.collectAsState()
12 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt:20:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
17 
18 @OptIn(ExperimentalMaterial3Api::class)
19 @Composable
20 internal fun PokedexContent(
!!              ^ error
21     state: PokedexStore.State,
22     onEvent: (PokedexStore.Intent) -> Unit,
23     onOutput: (PokedexComponent.Output) -> Unit,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:19:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
16 import com.mocoding.pokedex.core.model.Pokemon
17 
18 @Composable
19 internal fun PokemonGrid(
!!              ^ error
20     onPokemonClicked: (name: String) -> Unit,
21     pokemonList: List<Pokemon>,
22     isLoading: Boolean,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:22:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
19 
20 @OptIn(ExperimentalMaterial3Api::class)
21 @Composable
22 internal fun PokemonItem(
!!              ^ error
23     onClick: () -> Unit,
24     pokemon: Pokemon,
25     modifier: Modifier = Modifier,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:19:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
16 import kotlin.random.Random
17 
18 @Composable
19 internal fun PokemonLoadingItem(
!!              ^ error
20     modifier: Modifier = Modifier,
21     alpha: Float,
22 ) {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootContent.kt:14:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
11 import com.mocoding.pokedex.ui.pokedex.PokedexScreen
12 
13 @Composable
14 internal fun RootContent(component: RootComponent) {
!!              ^ error
15     Children(
16         stack = component.childStack,
17         animation = stackAnimation(fade()),

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Theme.kt:43:14
```
Function names should match the pattern: [a-z][a-zA-Z0-9]*
```
```kotlin
40 )
41 
42 @Composable
43 internal fun PokedexTheme(
!!              ^ error
44     darkTheme: Boolean = isSystemInDarkTheme(),
45     content: @Composable () -> Unit
46 ) {

```

### style, MagicNumber (105)

Report magic numbers. Magic number is a numeric literal that is not defined as a constant and hence it's unclear what the purpose of this number is. It's better to declare such numbers as constants and give them a proper name. By default, -1, 0, 1, and 2 are not considered to be magic numbers.

[Documentation](https://detekt.dev/docs/rules/style#magicnumber)

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonEntityQueries.kt:37:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
34   }
35 
36   public fun insert(pokemonEntity: PokemonEntity) {
37     driver.execute(-636_263_788, """
!!                     ^ error
38         |INSERT OR REPLACE INTO pokemonEntity(page, name, url)
39         |VALUES (?, ?, ?)
40         """.trimMargin(), 3) {

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonEntityQueries.kt:40:27
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
37     driver.execute(-636_263_788, """
38         |INSERT OR REPLACE INTO pokemonEntity(page, name, url)
39         |VALUES (?, ?, ?)
40         """.trimMargin(), 3) {
!!                           ^ error
41           bindLong(0, pokemonEntity.page)
42           bindString(1, pokemonEntity.name)
43           bindString(2, pokemonEntity.url)

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonEntityQueries.kt:45:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
42           bindString(1, pokemonEntity.name)
43           bindString(2, pokemonEntity.url)
44         }
45     notifyQueries(-636_263_788) { emit ->
!!                    ^ error
46       emit("pokemonEntity")
47     }
48   }

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonEntityQueries.kt:63:30
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
60     }
61 
62     override fun <R> execute(mapper: (SqlCursor) -> QueryResult<R>): QueryResult<R> =
63         driver.executeQuery(-1_228_302_992, """
!!                              ^ error
64     |SELECT *
65     |FROM pokemonEntity
66     |WHERE page = ?

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:29:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
26       cursor.getLong(0)!!,
27       cursor.getString(1)!!,
28       cursor.getLong(2)!!,
29       cursor.getLong(3)!!,
!!                      ^ error
30       cursor.getLong(4)!!,
31       cursor.getString(5)!!,
32       cursor.getString(6)!!,

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:30:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
27       cursor.getString(1)!!,
28       cursor.getLong(2)!!,
29       cursor.getLong(3)!!,
30       cursor.getLong(4)!!,
!!                      ^ error
31       cursor.getString(5)!!,
32       cursor.getString(6)!!,
33       cursor.getLong(7)!!

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:31:24
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
28       cursor.getLong(2)!!,
29       cursor.getLong(3)!!,
30       cursor.getLong(4)!!,
31       cursor.getString(5)!!,
!!                        ^ error
32       cursor.getString(6)!!,
33       cursor.getLong(7)!!
34     )

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:32:24
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
29       cursor.getLong(3)!!,
30       cursor.getLong(4)!!,
31       cursor.getString(5)!!,
32       cursor.getString(6)!!,
!!                        ^ error
33       cursor.getLong(7)!!
34     )
35   }

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:33:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
30       cursor.getLong(4)!!,
31       cursor.getString(5)!!,
32       cursor.getString(6)!!,
33       cursor.getLong(7)!!
!!                      ^ error
34     )
35   }
36 

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:60:30
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
57     types: String,
58     stats: String,
59     isFavorite: Long,
60   ) -> T): Query<T> = Query(-2_110_085_000, arrayOf("pokemonInfoEntity"), driver,
!!                              ^ error
61       "PokemonInfoEntity.sq", "selectAllFavorite", """
62   |SELECT *
63   |FROM pokemonInfoEntity

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:70:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
67       cursor.getLong(0)!!,
68       cursor.getString(1)!!,
69       cursor.getLong(2)!!,
70       cursor.getLong(3)!!,
!!                      ^ error
71       cursor.getLong(4)!!,
72       cursor.getString(5)!!,
73       cursor.getString(6)!!,

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:71:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
68       cursor.getString(1)!!,
69       cursor.getLong(2)!!,
70       cursor.getLong(3)!!,
71       cursor.getLong(4)!!,
!!                      ^ error
72       cursor.getString(5)!!,
73       cursor.getString(6)!!,
74       cursor.getLong(7)!!

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:72:24
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
69       cursor.getLong(2)!!,
70       cursor.getLong(3)!!,
71       cursor.getLong(4)!!,
72       cursor.getString(5)!!,
!!                        ^ error
73       cursor.getString(6)!!,
74       cursor.getLong(7)!!
75     )

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:73:24
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
70       cursor.getLong(3)!!,
71       cursor.getLong(4)!!,
72       cursor.getString(5)!!,
73       cursor.getString(6)!!,
!!                        ^ error
74       cursor.getLong(7)!!
75     )
76   }

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:74:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
71       cursor.getLong(4)!!,
72       cursor.getString(5)!!,
73       cursor.getString(6)!!,
74       cursor.getLong(7)!!
!!                      ^ error
75     )
76   }
77 

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:93:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
90   }
91 
92   public fun insert(pokemonInfoEntity: PokemonInfoEntity) {
93     driver.execute(-2_056_316_318, """
!!                     ^ error
94         |INSERT OR REPLACE INTO pokemonInfoEntity(id, name, height, weight, experience, types, stats, isFavorite)
95         |VALUES (?, ?, ?, ?, ?, ?, ?, ?)
96         """.trimMargin(), 8) {

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:96:27
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
93      driver.execute(-2_056_316_318, """
94          |INSERT OR REPLACE INTO pokemonInfoEntity(id, name, height, weight, experience, types, stats, isFavorite)
95          |VALUES (?, ?, ?, ?, ?, ?, ?, ?)
96          """.trimMargin(), 8) {
!!                            ^ error
97            bindLong(0, pokemonInfoEntity.id)
98            bindString(1, pokemonInfoEntity.name)
99            bindLong(2, pokemonInfoEntity.height)

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:100:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
97            bindLong(0, pokemonInfoEntity.id)
98            bindString(1, pokemonInfoEntity.name)
99            bindLong(2, pokemonInfoEntity.height)
100           bindLong(3, pokemonInfoEntity.weight)
!!!                    ^ error
101           bindLong(4, pokemonInfoEntity.experience)
102           bindString(5, pokemonInfoEntity.types)
103           bindString(6, pokemonInfoEntity.stats)

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:101:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
98            bindString(1, pokemonInfoEntity.name)
99            bindLong(2, pokemonInfoEntity.height)
100           bindLong(3, pokemonInfoEntity.weight)
101           bindLong(4, pokemonInfoEntity.experience)
!!!                    ^ error
102           bindString(5, pokemonInfoEntity.types)
103           bindString(6, pokemonInfoEntity.stats)
104           bindLong(7, pokemonInfoEntity.isFavorite)

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:102:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
99            bindLong(2, pokemonInfoEntity.height)
100           bindLong(3, pokemonInfoEntity.weight)
101           bindLong(4, pokemonInfoEntity.experience)
102           bindString(5, pokemonInfoEntity.types)
!!!                      ^ error
103           bindString(6, pokemonInfoEntity.stats)
104           bindLong(7, pokemonInfoEntity.isFavorite)
105         }

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:103:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
100           bindLong(3, pokemonInfoEntity.weight)
101           bindLong(4, pokemonInfoEntity.experience)
102           bindString(5, pokemonInfoEntity.types)
103           bindString(6, pokemonInfoEntity.stats)
!!!                      ^ error
104           bindLong(7, pokemonInfoEntity.isFavorite)
105         }
106     notifyQueries(-2_056_316_318) { emit ->

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:104:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
101           bindLong(4, pokemonInfoEntity.experience)
102           bindString(5, pokemonInfoEntity.types)
103           bindString(6, pokemonInfoEntity.stats)
104           bindLong(7, pokemonInfoEntity.isFavorite)
!!!                    ^ error
105         }
106     notifyQueries(-2_056_316_318) { emit ->
107       emit("pokemonInfoEntity")

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:106:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
103           bindString(6, pokemonInfoEntity.stats)
104           bindLong(7, pokemonInfoEntity.isFavorite)
105         }
106     notifyQueries(-2_056_316_318) { emit ->
!!!                    ^ error
107       emit("pokemonInfoEntity")
108     }
109   }

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:112:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
109   }
110 
111   public fun updateIsFavorite(isFavorite: Long, name: String) {
112     driver.execute(755_857_144, """
!!!                    ^ error
113         |UPDATE pokemonInfoEntity
114         |SET isFavorite = ?
115         |WHERE name = ?

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:120:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
117           bindLong(0, isFavorite)
118           bindString(1, name)
119         }
120     notifyQueries(755_857_144) { emit ->
!!!                   ^ error
121       emit("pokemonInfoEntity")
122     }
123   }

```

* /tmp/output/phase1/before/shared/build/generated/sqldelight/code/PokemonDatabase/commonMain/commocodingpokedex/PokemonInfoEntityQueries.kt:138:29
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
135     }
136 
137     override fun <R> execute(mapper: (SqlCursor) -> QueryResult<R>): QueryResult<R> =
138         driver.executeQuery(771_271_267, """
!!!                             ^ error
139     |SELECT *
140     |FROM pokemonInfoEntity
141     |WHERE name = ?

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:22:12
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
19     }
20 
21     when(result.status.value) {
22         in 200..299 -> Unit
!!            ^ error
23         in 400..499 -> throw PokedexException(PokedexError.ClientError)
24         500 -> throw PokedexException(PokedexError.ServerError)
25         else -> throw PokedexException(PokedexError.UnknownError)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:22:17
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
19     }
20 
21     when(result.status.value) {
22         in 200..299 -> Unit
!!                 ^ error
23         in 400..499 -> throw PokedexException(PokedexError.ClientError)
24         500 -> throw PokedexException(PokedexError.ServerError)
25         else -> throw PokedexException(PokedexError.UnknownError)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:23:12
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
20 
21     when(result.status.value) {
22         in 200..299 -> Unit
23         in 400..499 -> throw PokedexException(PokedexError.ClientError)
!!            ^ error
24         500 -> throw PokedexException(PokedexError.ServerError)
25         else -> throw PokedexException(PokedexError.UnknownError)
26     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:23:17
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
20 
21     when(result.status.value) {
22         in 200..299 -> Unit
23         in 400..499 -> throw PokedexException(PokedexError.ClientError)
!!                 ^ error
24         500 -> throw PokedexException(PokedexError.ServerError)
25         else -> throw PokedexException(PokedexError.UnknownError)
26     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:24:9
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
21     when(result.status.value) {
22         in 200..299 -> Unit
23         in 400..499 -> throw PokedexException(PokedexError.ClientError)
24         500 -> throw PokedexException(PokedexError.ServerError)
!!         ^ error
25         else -> throw PokedexException(PokedexError.UnknownError)
26     }
27 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:42:93
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
39                 url = pokemonInfo.imageUrl,
40                 contentDescription = pokemonInfo.name,
41                 contentScale = ContentScale.FillWidth,
42                 colorFilter = ColorFilter.colorMatrix(ColorMatrix().apply { setToSaturation(3f) }),
!!                                                                                             ^ error
43                 modifier = Modifier
44                     .widthIn(max = 800.dp)
45                     .fillMaxWidth(.9f)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:45:35
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
42                 colorFilter = ColorFilter.colorMatrix(ColorMatrix().apply { setToSaturation(3f) }),
43                 modifier = Modifier
44                     .widthIn(max = 800.dp)
45                     .fillMaxWidth(.9f)
!!                                   ^ error
46                     .wrapContentHeight(Alignment.Top, true)
47                     .scale(1f, 1.8f)
48                     .blur(70.dp, BlurredEdgeTreatment.Unbounded)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:47:32
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
44                     .widthIn(max = 800.dp)
45                     .fillMaxWidth(.9f)
46                     .wrapContentHeight(Alignment.Top, true)
47                     .scale(1f, 1.8f)
!!                                ^ error
48                     .blur(70.dp, BlurredEdgeTreatment.Unbounded)
49                     .alpha(.5f)
50             )

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:49:28
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
46                     .wrapContentHeight(Alignment.Top, true)
47                     .scale(1f, 1.8f)
48                     .blur(70.dp, BlurredEdgeTreatment.Unbounded)
49                     .alpha(.5f)
!!                            ^ error
50             )
51         }
52 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:140:50
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
137                                 modifier = Modifier
138                                     .widthIn(max = 500.dp)
139                                     .fillMaxWidth()
140                                     .aspectRatio(1.2f)
!!!                                                  ^ error
141                                     .fillMaxHeight()
142                             )
143                         }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:180:51
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
177                                 pokemonInfo = pokemonInfo,
178                                 modifier = Modifier
179                                     .padding(top = 18.dp)
180                                     .fillMaxWidth(.9f)
!!!                                                   ^ error
181                             )
182                         }
183 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:189:51
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
186                                 pokemonInfo = pokemonInfo,
187                                 modifier = Modifier
188                                     .padding(top = 12.dp)
189                                     .fillMaxWidth(.9f)
!!!                                                   ^ error
190                             )
191                         }
192                     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:30:64
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
27         modifier = modifier
28             .fillMaxWidth()
29             .clip(MaterialTheme.shapes.large)
30             .background(MaterialTheme.colorScheme.outline.copy(.2f))
!!                                                                ^ error
31             .padding(horizontal = 12.dp, vertical = 16.dp)
32     ) {
33         Column(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:44:55
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
41                 )
42                 Spacer(Modifier.width(4.dp))
43 
44                 val weightInKg = pokemonInfo.weight / 10f
!!                                                       ^ error
45 
46                 Text(
47                     text = "$weightInKg kg",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:59:69
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
56 
57             Text(
58                 text = "Weight",
59                 color = MaterialTheme.colorScheme.onBackground.copy(.8f),
!!                                                                     ^ error
60                 style = MaterialTheme.typography.bodyMedium
61             )
62         }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:79:48
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
76                 Icon(
77                     Icons.Outlined.Straighten,
78                     contentDescription = null,
79                     modifier = Modifier.rotate(90f)
!!                                                ^ error
80                 )
81                 Spacer(Modifier.width(4.dp))
82 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:83:58
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
80                 )
81                 Spacer(Modifier.width(4.dp))
82 
83                 val heightInMeter = pokemonInfo.height / 10f
!!                                                          ^ error
84 
85                 Text(
86                     text = "$heightInMeter m",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:98:69
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
95  
96              Text(
97                  text = "Height",
98                  color = MaterialTheme.colorScheme.onBackground.copy(.8f),
!!                                                                      ^ error
99                  style = MaterialTheme.typography.bodyMedium
100             )
101         }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:50:65
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
47     ) {
48         Text(
49             text = statResponse.name,
50             color = MaterialTheme.colorScheme.onBackground.copy(.8f),
!!                                                                 ^ error
51             style = MaterialTheme.typography.bodyMedium,
52             modifier = Modifier.weight(.3f)
53         )

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:52:40
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
49             text = statResponse.name,
50             color = MaterialTheme.colorScheme.onBackground.copy(.8f),
51             style = MaterialTheme.typography.bodyMedium,
52             modifier = Modifier.weight(.3f)
!!                                        ^ error
53         )
54 
55         Text(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:61:40
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
58             style = MaterialTheme.typography.bodyLarge.copy(
59                 fontWeight = FontWeight.Bold
60             ),
61             modifier = Modifier.weight(.2f)
!!                                        ^ error
62         )
63 
64         val progress = statResponse.value.toFloat() / statResponse.maxValue.toFloat()

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:67:45
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
64         val progress = statResponse.value.toFloat() / statResponse.maxValue.toFloat()
65         val animatedProgress = progress * animationProgress.value
66 
67         val progressColor = if (progress >= .5f) Green300 else Yellow400
!!                                             ^ error
68         val progressTrackColor = MaterialTheme.colorScheme.outline.copy(.2f)
69 
70         Box(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:68:73
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
65         val animatedProgress = progress * animationProgress.value
66 
67         val progressColor = if (progress >= .5f) Green300 else Yellow400
68         val progressTrackColor = MaterialTheme.colorScheme.outline.copy(.2f)
!!                                                                         ^ error
69 
70         Box(
71             modifier = Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:72:25
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
69 
70         Box(
71             modifier = Modifier
72                 .weight(.5f)
!!                         ^ error
73                 .height(10.dp)
74                 .drawBehind {
75                     drawRoundRect(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:83:77
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
80                 } else if (state.pokemonList.isEmpty()) {
81                     Text(
82                         text = "Your favorite list is empty!",
83                         color = MaterialTheme.colorScheme.onBackground.copy(.8f),
!!                                                                             ^ error
84                         style = MaterialTheme.typography.bodyLarge,
85                         modifier = Modifier.padding(20.dp)
86                     )

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/CategoryButton.kt:53:32
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
50         ) {
51             Box(
52                 modifier = Modifier
53                     .scale(1f, .5f)
!!                                ^ error
54                     .offset(y = 40.dp)
55                     .size(40.dp)
56                     .background(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainModelDrawerSheet.kt:49:85
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
46                     onItemsClick(item)
47                 },
48                 colors = NavigationDrawerItemDefaults.colors(
49                     selectedContainerColor = MaterialTheme.colorScheme.primary.copy(.6f),
!!                                                                                     ^ error
50                     unselectedContainerColor = Color.Transparent,
51                     selectedTextColor = MaterialTheme.colorScheme.onPrimary,
52                     unselectedTextColor = MaterialTheme.colorScheme.onBackground,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt:45:59
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
42                 url = video.imageUrl,
43                 contentDescription = video.title,
44                 contentScale = ContentScale.Crop,
45                 colorFilter = ColorFilter.tint(Black.copy(.5f), BlendMode.Darken),
!!                                                           ^ error
46                 modifier = Modifier
47                     .fillMaxWidth()
48                     .aspectRatio(1.5f)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt:48:34
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
45                 colorFilter = ColorFilter.tint(Black.copy(.5f), BlendMode.Darken),
46                 modifier = Modifier
47                     .fillMaxWidth()
48                     .aspectRatio(1.5f)
!!                                  ^ error
49                     .clip(MaterialTheme.shapes.medium)
50             )
51 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt:76:65
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
73 
74         Text(
75             text = "${video.year} | ${video.category} | ${video.details}",
76             color = MaterialTheme.colorScheme.onBackground.copy(.8f),
!!                                                                 ^ error
77             style = MaterialTheme.typography.bodyMedium,
78         )
79     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:31:31
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
28         initialValue = .1f,
29         targetValue = .4f,
30         animationSpec = infiniteRepeatable(
31             animation = tween(800, easing = LinearEasing),
!!                               ^ error
32             repeatMode = RepeatMode.Reverse
33         )
34     )

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:40:34
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
37         val columns = when(maxWidth) {
38             in 0.dp..349.dp -> 1
39             in 350.dp..599.dp -> 2
40             in 600.dp..899.dp -> 3
!!                                  ^ error
41             in 900.dp..1199.dp -> 4
42             else -> 5
43         }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:41:35
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
38             in 0.dp..349.dp -> 1
39             in 350.dp..599.dp -> 2
40             in 600.dp..899.dp -> 3
41             in 900.dp..1199.dp -> 4
!!                                   ^ error
42             else -> 5
43         }
44 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:42:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
39             in 350.dp..599.dp -> 2
40             in 600.dp..899.dp -> 3
41             in 900.dp..1199.dp -> 4
42             else -> 5
!!                     ^ error
43         }
44 
45         LazyVerticalGrid(

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:61:23
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
58             }
59 
60             if (isLoading) {
61                 items(5) { index ->
!!                       ^ error
62                     LaunchedEffect(Unit) {
63                         if (index == 0) loadMoreItems()
64                     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:71:34
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
68                 contentScale = ContentScale.Fit,
69                 modifier = Modifier
70                     .fillMaxWidth()
71                     .aspectRatio(1.2f)
!!                                  ^ error
72                     .fillMaxHeight()
73             )
74 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:82:43
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
79                 style = MaterialTheme.typography.titleLarge.copy(
80                     fontWeight = FontWeight.Bold
81                 ),
82                 modifier = Modifier.alpha(.8f)
!!                                           ^ error
83             )
84 
85             Spacer(Modifier.height(4.dp))

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:90:43
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
87             Text(
88                 text = pokemon.numberString,
89                 style = MaterialTheme.typography.titleMedium,
90                 modifier = Modifier.alpha(.4f)
!!                                           ^ error
91             )
92         }
93     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:29:64
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
26                 this.alpha = abs(1f - alpha)
27             }
28             .clip(MaterialTheme.shapes.small)
29             .background(MaterialTheme.colorScheme.primary.copy(.6f))
!!                                                                ^ error
30     ) {
31         Column(
32             horizontalAlignment = Alignment.CenterHorizontally,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:39:34
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
36             Box(
37                 modifier = modifier
38                     .fillMaxWidth()
39                     .aspectRatio(1.2f)
!!                                  ^ error
40                     .fillMaxHeight()
41                     .graphicsLayer {
42                         this.alpha = alpha

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:45:77
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
42                         this.alpha = alpha
43                     }
44                     .clip(MaterialTheme.shapes.small)
45                     .background(MaterialTheme.colorScheme.onBackground.copy(.4f))
!!                                                                             ^ error
46             )
47 
48             val firstBoxWidthFraction = remember {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:53:39
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
50             }
51             Box(
52                 modifier = modifier
53                     .fillMaxWidth(max(.3f, firstBoxWidthFraction))
!!                                       ^ error
54                     .height(20.dp)
55                     .graphicsLayer {
56                         this.alpha = alpha

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:59:77
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
56                         this.alpha = alpha
57                     }
58                     .clip(MaterialTheme.shapes.small)
59                     .background(MaterialTheme.colorScheme.onBackground.copy(.4f))
!!                                                                             ^ error
60             )
61 
62             val secondBoxWidthFraction = remember {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:67:39
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
64             }
65             Box(
66                 modifier = modifier
67                     .fillMaxWidth(max(.3f, secondBoxWidthFraction))
!!                                       ^ error
68                     .height(20.dp)
69                     .graphicsLayer {
70                         this.alpha = alpha

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:73:77
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
70                         this.alpha = alpha
71                     }
72                     .clip(MaterialTheme.shapes.small)
73                     .background(MaterialTheme.colorScheme.onBackground.copy(.4f))
!!                                                                             ^ error
74             )
75         }
76     }

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:5:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
2 
3 import androidx.compose.ui.graphics.Color
4 
5 val Black = Color(0xFF090f0b)
!                   ^ error
6 
7 val Green300 = Color(0xFF2EB688)
8 val Green400 = Color(0xFF145526)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:7:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
4  
5  val Black = Color(0xFF090f0b)
6  
7  val Green300 = Color(0xFF2EB688)
!                       ^ error
8  val Green400 = Color(0xFF145526)
9  val Green500 = Color(0xFF046D4A)
10 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:8:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
5  val Black = Color(0xFF090f0b)
6  
7  val Green300 = Color(0xFF2EB688)
8  val Green400 = Color(0xFF145526)
!                       ^ error
9  val Green500 = Color(0xFF046D4A)
10 
11 val Red300 = Color(0xFFF33736)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:9:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
6  
7  val Green300 = Color(0xFF2EB688)
8  val Green400 = Color(0xFF145526)
9  val Green500 = Color(0xFF046D4A)
!                       ^ error
10 
11 val Red300 = Color(0xFFF33736)
12 val Red400 = Color(0xFFcb290b)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:11:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
8  val Green400 = Color(0xFF145526)
9  val Green500 = Color(0xFF046D4A)
10 
11 val Red300 = Color(0xFFF33736)
!!                    ^ error
12 val Red400 = Color(0xFFcb290b)
13 val Red500 = Color(0xFF9C2221)
14 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:12:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
9  val Green500 = Color(0xFF046D4A)
10 
11 val Red300 = Color(0xFFF33736)
12 val Red400 = Color(0xFFcb290b)
!!                    ^ error
13 val Red500 = Color(0xFF9C2221)
14 
15 val Blue300 = Color(0xFF54B1DF)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:13:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
10 
11 val Red300 = Color(0xFFF33736)
12 val Red400 = Color(0xFFcb290b)
13 val Red500 = Color(0xFF9C2221)
!!                    ^ error
14 
15 val Blue300 = Color(0xFF54B1DF)
16 val Blue500 = Color(0xFF1E3DA8)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:15:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
12 val Red400 = Color(0xFFcb290b)
13 val Red500 = Color(0xFF9C2221)
14 
15 val Blue300 = Color(0xFF54B1DF)
!!                     ^ error
16 val Blue500 = Color(0xFF1E3DA8)
17 
18 val Yellow300 = Color(0xFFF1A22C)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:16:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
13 val Red500 = Color(0xFF9C2221)
14 
15 val Blue300 = Color(0xFF54B1DF)
16 val Blue500 = Color(0xFF1E3DA8)
!!                     ^ error
17 
18 val Yellow300 = Color(0xFFF1A22C)
19 val Yellow400 = Color(0xFFfaae41)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:18:23
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
15 val Blue300 = Color(0xFF54B1DF)
16 val Blue500 = Color(0xFF1E3DA8)
17 
18 val Yellow300 = Color(0xFFF1A22C)
!!                       ^ error
19 val Yellow400 = Color(0xFFfaae41)
20 val Yellow500 = Color(0xFFCB5C0D)
21 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:19:23
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
16 val Blue500 = Color(0xFF1E3DA8)
17 
18 val Yellow300 = Color(0xFFF1A22C)
19 val Yellow400 = Color(0xFFfaae41)
!!                       ^ error
20 val Yellow500 = Color(0xFFCB5C0D)
21 
22 val Blue400 = Color(0xFF4572E8)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:20:23
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
17 
18 val Yellow300 = Color(0xFFF1A22C)
19 val Yellow400 = Color(0xFFfaae41)
20 val Yellow500 = Color(0xFFCB5C0D)
!!                       ^ error
21 
22 val Blue400 = Color(0xFF4572E8)
23 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:22:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
19 val Yellow400 = Color(0xFFfaae41)
20 val Yellow500 = Color(0xFFCB5C0D)
21 
22 val Blue400 = Color(0xFF4572E8)
!!                     ^ error
23 
24 val LightGray400 = Color(0xFFb8b6b3)
25 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:24:26
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
21 
22 val Blue400 = Color(0xFF4572E8)
23 
24 val LightGray400 = Color(0xFFb8b6b3)
!!                          ^ error
25 
26 val DarkGray400 = Color(0xFF3e4047)
27 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:26:25
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
23 
24 val LightGray400 = Color(0xFFb8b6b3)
25 
26 val DarkGray400 = Color(0xFF3e4047)
!!                         ^ error
27 
28 val Gray400 = Color(0xFF595C61)
29 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:28:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
25 
26 val DarkGray400 = Color(0xFF3e4047)
27 
28 val Gray400 = Color(0xFF595C61)
!!                     ^ error
29 
30 val Bug = Color(0xFF179A55)
31 val Dark = Color(0xFF040706)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:30:17
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
27 
28 val Gray400 = Color(0xFF595C61)
29 
30 val Bug = Color(0xFF179A55)
!!                 ^ error
31 val Dark = Color(0xFF040706)
32 val Dragon = Color(0xFF378A94)
33 val Electric = Color(0xFFE0E64B)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:31:18
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
28 val Gray400 = Color(0xFF595C61)
29 
30 val Bug = Color(0xFF179A55)
31 val Dark = Color(0xFF040706)
!!                  ^ error
32 val Dragon = Color(0xFF378A94)
33 val Electric = Color(0xFFE0E64B)
34 val Fairy = Color(0xFF9E1A44)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:32:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
29 
30 val Bug = Color(0xFF179A55)
31 val Dark = Color(0xFF040706)
32 val Dragon = Color(0xFF378A94)
!!                    ^ error
33 val Electric = Color(0xFFE0E64B)
34 val Fairy = Color(0xFF9E1A44)
35 val Fire = Color(0xFFB22328)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:33:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
30 val Bug = Color(0xFF179A55)
31 val Dark = Color(0xFF040706)
32 val Dragon = Color(0xFF378A94)
33 val Electric = Color(0xFFE0E64B)
!!                      ^ error
34 val Fairy = Color(0xFF9E1A44)
35 val Fire = Color(0xFFB22328)
36 val Flying = Color(0xFF90B1C5)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:34:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
31 val Dark = Color(0xFF040706)
32 val Dragon = Color(0xFF378A94)
33 val Electric = Color(0xFFE0E64B)
34 val Fairy = Color(0xFF9E1A44)
!!                   ^ error
35 val Fire = Color(0xFFB22328)
36 val Flying = Color(0xFF90B1C5)
37 val Ghost = Color(0xFF363069)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:35:18
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
32 val Dragon = Color(0xFF378A94)
33 val Electric = Color(0xFFE0E64B)
34 val Fairy = Color(0xFF9E1A44)
35 val Fire = Color(0xFFB22328)
!!                  ^ error
36 val Flying = Color(0xFF90B1C5)
37 val Ghost = Color(0xFF363069)
38 val Ice = Color(0xFF7ECFF2)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:36:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
33 val Electric = Color(0xFFE0E64B)
34 val Fairy = Color(0xFF9E1A44)
35 val Fire = Color(0xFFB22328)
36 val Flying = Color(0xFF90B1C5)
!!                    ^ error
37 val Ghost = Color(0xFF363069)
38 val Ice = Color(0xFF7ECFF2)
39 val Poison = Color(0xFF642785)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:37:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
34 val Fairy = Color(0xFF9E1A44)
35 val Fire = Color(0xFFB22328)
36 val Flying = Color(0xFF90B1C5)
37 val Ghost = Color(0xFF363069)
!!                   ^ error
38 val Ice = Color(0xFF7ECFF2)
39 val Poison = Color(0xFF642785)
40 val Psychic = Color(0xFFAC296B)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:38:17
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
35 val Fire = Color(0xFFB22328)
36 val Flying = Color(0xFF90B1C5)
37 val Ghost = Color(0xFF363069)
38 val Ice = Color(0xFF7ECFF2)
!!                 ^ error
39 val Poison = Color(0xFF642785)
40 val Psychic = Color(0xFFAC296B)
41 val Rock = Color(0xFF4B190E)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:39:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
36 val Flying = Color(0xFF90B1C5)
37 val Ghost = Color(0xFF363069)
38 val Ice = Color(0xFF7ECFF2)
39 val Poison = Color(0xFF642785)
!!                    ^ error
40 val Psychic = Color(0xFFAC296B)
41 val Rock = Color(0xFF4B190E)
42 val Steel = Color(0xFF5C756D)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:40:21
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
37 val Ghost = Color(0xFF363069)
38 val Ice = Color(0xFF7ECFF2)
39 val Poison = Color(0xFF642785)
40 val Psychic = Color(0xFFAC296B)
!!                     ^ error
41 val Rock = Color(0xFF4B190E)
42 val Steel = Color(0xFF5C756D)
43 val Water = Color(0xFF2648DC)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:41:18
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
38 val Ice = Color(0xFF7ECFF2)
39 val Poison = Color(0xFF642785)
40 val Psychic = Color(0xFFAC296B)
41 val Rock = Color(0xFF4B190E)
!!                  ^ error
42 val Steel = Color(0xFF5C756D)
43 val Water = Color(0xFF2648DC)
44 val Fighting = Color(0xFF9F422A)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:42:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
39 val Poison = Color(0xFF642785)
40 val Psychic = Color(0xFFAC296B)
41 val Rock = Color(0xFF4B190E)
42 val Steel = Color(0xFF5C756D)
!!                   ^ error
43 val Water = Color(0xFF2648DC)
44 val Fighting = Color(0xFF9F422A)
45 val Grass = Color(0xFF007C42)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:43:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
40 val Psychic = Color(0xFFAC296B)
41 val Rock = Color(0xFF4B190E)
42 val Steel = Color(0xFF5C756D)
43 val Water = Color(0xFF2648DC)
!!                   ^ error
44 val Fighting = Color(0xFF9F422A)
45 val Grass = Color(0xFF007C42)
46 val Ground = Color(0xFFAD7235)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:44:22
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
41 val Rock = Color(0xFF4B190E)
42 val Steel = Color(0xFF5C756D)
43 val Water = Color(0xFF2648DC)
44 val Fighting = Color(0xFF9F422A)
!!                      ^ error
45 val Grass = Color(0xFF007C42)
46 val Ground = Color(0xFFAD7235)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:45:19
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
42 val Steel = Color(0xFF5C756D)
43 val Water = Color(0xFF2648DC)
44 val Fighting = Color(0xFF9F422A)
45 val Grass = Color(0xFF007C42)
!!                   ^ error
46 val Ground = Color(0xFFAD7235)

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:46:20
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
43 val Water = Color(0xFF2648DC)
44 val Fighting = Color(0xFF9F422A)
45 val Grass = Color(0xFF007C42)
46 val Ground = Color(0xFFAD7235)
!!                    ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/KgHelper.kt:3:41
```
This expression contains a magic number. Consider defining it to a well named constant.
```
```kotlin
1 package com.mocoding.pokedex.ui.utils
2 
3 fun kgToPounds(kg: Float): Float = kg * 2.205f
!                                         ^ error

```

### style, MaxLineLength (11)

Line detected, which is longer than the defined maximum line length in the code style.

[Documentation](https://detekt.dev/docs/rules/style#maxlinelength)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/model/Video.kt:16:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
13             Video(
14                 id = "01",
15                 title = "Pokemon Master Journeys: The Series",
16                 imageUrl = "https://orgoglionerd.it/wp-content/uploads/2022/05/Esplorazioni-Pokemon-Super-nuova-serie-tv-trailer.jpg",
!! ^ error
17                 year = 2021,
18                 category = "Series",
19                 details = "10 EP",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/model/Video.kt:24:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
21             Video(
22                 id = "02",
23                 title = "Pokémon: Mewtwo Strikes Back—Evolution",
24                 imageUrl = "https://assets.pokemon.com/assets/cms2/img/watch-pokemon-tv/movies/movie22/movie22_ss01.jpg",
!! ^ error
25                 year = 2020,
26                 category = "Series",
27                 details = "12 EP",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/model/Video.kt:32:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
29             Video(
30                 id = "03",
31                 title = "Pokémon the Movie: The Power of Us",
32                 imageUrl = "https://assets.pokemon.com/assets/cms2/img/watch-pokemon-tv/movies/movie21/movie21_ss01.jpg",
!! ^ error
33                 year = 2018,
34                 category = "Movie",
35                 details = "1h 52m",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/model/Video.kt:40:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
37             Video(
38                 id = "04",
39                 title = "Pokémon the Movie: Hoopa and the Clash of Ages",
40                 imageUrl = "https://assets.pokemon.com/assets/cms2/img/watch-pokemon-tv/movies/movie18/movie18_ss03.jpg",
!! ^ error
41                 year = 2015,
42                 category = "Movie",
43                 details = "1h 46m",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/model/Video.kt:48:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
45             Video(
46                 id = "05",
47                 title = "Pokémon—Zoroark: Master of Illusions",
48                 imageUrl = "https://assets.pokemon.com/assets/cms2/img/watch-pokemon-tv/movies/movie13/movie13_ss01.jpg",
!! ^ error
49                 year = 2011,
50                 category = "Series",
51                 details = "8 EP",

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:89:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
86                             }
87                         ) {
88                             Icon(
89                                 if (state.pokemonInfo?.isFavorite == true) Icons.Rounded.Favorite else Icons.Rounded.FavoriteBorder,
!! ^ error
90                                 contentDescription = "Favorite",
91                                 tint = if (state.pokemonInfo?.isFavorite == true) MaterialTheme.colorScheme.primary
92                                     else MaterialTheme.colorScheme.onBackground

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStoreFactory.kt:46:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
43 
44         override fun executeIntent(intent: DetailsStore.Intent, getState: () -> DetailsStore.State): Unit =
45             when (intent) {
46                 is DetailsStore.Intent.UpdatePokemonFavoriteState -> togglePokemonFavorite(pokemonName, intent.isFavorite)
!! ^ error
47             }
48 
49         private var loadPokemonInfoByNameJob: Job? = null

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStoreFactory.kt:88:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
85                 is Msg.PokemonInfoLoading -> DetailsStore.State(isLoading = true)
86                 is Msg.PokemonInfoLoaded -> DetailsStore.State(pokemonInfo = msg.pokemonInfo)
87                 is Msg.PokemonInfoFailed -> DetailsStore.State(error = msg.error)
88                 is Msg.PokemonInfoFavoriteStateUpdated -> copy(pokemonInfo = pokemonInfo?.copy(isFavorite = msg.isFavorite))
!! ^ error
89             }
90     }
91 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStoreFactory.kt:48:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
45 
46         override fun executeIntent(intent: PokedexStore.Intent, getState: () -> PokedexStore.State): Unit =
47             when (intent) {
48                 is PokedexStore.Intent.LoadPokemonListByPage -> loadPokemonListByPage(intent.page, getState().isLastPageLoaded)
!! ^ error
49                 is PokedexStore.Intent.UpdateSearchValue -> dispatch(Msg.SearchValueUpdated(intent.searchValue))
50             }
51 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootComponent.kt:86:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
83     private fun createChild(configuration: Configuration, componentContext: ComponentContext): Child =
84         when (configuration) {
85             is Configuration.Main -> Child.Main(main(componentContext, ::onMainOutput))
86             is Configuration.Pokedex -> Child.Pokedex(pokedex(componentContext, configuration.searchValue, ::onPokedexOutput))
!! ^ error
87             is Configuration.Favorite -> Child.Favorite(favorite(componentContext, ::onFavoriteOutput))
88             is Configuration.Details -> Child.Details(details(componentContext, configuration.pokemonName, ::onDetailsOutput))
89             is Configuration.ComingSoon -> Child.ComingSoon(comingSoon(componentContext, ::onComingSoonOutput))

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootComponent.kt:88:1
```
Line detected, which is longer than the defined maximum line length in the code style.
```
```kotlin
85             is Configuration.Main -> Child.Main(main(componentContext, ::onMainOutput))
86             is Configuration.Pokedex -> Child.Pokedex(pokedex(componentContext, configuration.searchValue, ::onPokedexOutput))
87             is Configuration.Favorite -> Child.Favorite(favorite(componentContext, ::onFavoriteOutput))
88             is Configuration.Details -> Child.Details(details(componentContext, configuration.pokemonName, ::onDetailsOutput))
!! ^ error
89             is Configuration.ComingSoon -> Child.ComingSoon(comingSoon(componentContext, ::onComingSoonOutput))
90         }
91 

```

### style, NewLineAtEndOfFile (62)

Checks whether files end with a line separator.

[Documentation](https://detekt.dev/docs/rules/style#newlineatendoffile)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt:11:50
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/PokedexDispatchers.kt is not ending with a new line.
```
```kotlin
8      val unconfined: CoroutineDispatcher
9  }
10 
11 expect val pokedexDispatchers: PokedexDispatchers
!!                                                  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/DatabaseConstants.kt:5:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/DatabaseConstants.kt is not ending with a new line.
```
```kotlin
2 
3 object DatabaseConstants {
4     const val name = "pokemonDatabase"
5 }
!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/SqlDriverFactory.kt:13:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/SqlDriverFactory.kt is not ending with a new line.
```
```kotlin
10     )
11 
12     return database
13 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/dao/PokemonDao.kt:20:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/dao/PokemonDao.kt is not ending with a new line.
```
```kotlin
17     suspend fun insert(pokemonEntity: PokemonEntity) = withContext(pokedexDispatchers.io) {
18         query.insert(pokemonEntity)
19     }
20 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/dao/PokemonInfoDao.kt:33:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/dao/PokemonInfoDao.kt is not ending with a new line.
```
```kotlin
30             name = name
31         )
32     }
33 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/di/DatabaseModule.kt:14:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/di/DatabaseModule.kt is not ending with a new line.
```
```kotlin
11     single { createDatabase(driver = get()) }
12     single { PokemonDao(pokemonDatabase = get()) }
13     single { PokemonInfoDao(pokemonDatabase = get()) }
14 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/di/AppModule.kt:17:6
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/di/AppModule.kt is not ending with a new line.
```
```kotlin
14             networkModule(enableNetworkLogs),
15             dataModule
16         )
17     }
!!      ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt:22:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt is not ending with a new line.
```
```kotlin
19             level = LogLevel.ALL
20         }
21     }
22 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt:5:50
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt is not ending with a new line.
```
```kotlin
2 
3 import io.ktor.client.HttpClient
4 
5 expect fun createPlatformHttpClient(): HttpClient
!                                                  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/NetworkConstants.kt:10:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/NetworkConstants.kt is not ending with a new line.
```
```kotlin
7          const val route = baseUrl + "pokemon"
8          val byName: (String) -> String = { name -> "$route/$name"}
9      }
10 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/client/PokemonClient.kt:44:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/client/PokemonClient.kt is not ending with a new line.
```
```kotlin
41         private const val PageSize = 20
42     }
43 
44 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/di/NetworkModule.kt:13:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/di/NetworkModule.kt is not ending with a new line.
```
```kotlin
10         single { createHttpClient(enableLogging) }
11         single { PokemonClient(httpClient = get()) }
12     }
13 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/errors/PokedexException.kt:12:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/errors/PokedexException.kt is not ending with a new line.
```
```kotlin
9  
10 class PokedexException(error: PokedexError): Exception(
11     "Something goes wrong: $error"
12 )
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt:34:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt is not ending with a new line.
```
```kotlin
31         throw PokedexException(PokedexError.ServerError)
32     }
33 
34 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/Mappers.kt:48:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/Mappers.kt is not ending with a new line.
```
```kotlin
45 fun PokemonInfoEntity.toPokemon() = Pokemon(
46     name = name,
47     url = "$id/"
48 )
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/di/DataModule.kt:9:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/di/DataModule.kt is not ending with a new line.
```
```kotlin
6  
7  val dataModule = module {
8      single<PokemonRepository> { PokemonRepositoryImpl() }
9  }
!   ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepository.kt:15:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepository.kt is not ending with a new line.
```
```kotlin
12     suspend fun getFavoritePokemonListFlow(): Flow<List<Pokemon>>
13     suspend fun updatePokemonFavoriteState(name: String, isFavorite: Boolean)
14 
15 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepositoryImpl.kt:73:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepositoryImpl.kt is not ending with a new line.
```
```kotlin
70         )
71     }
72 
73 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonComponent.kt:18:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonComponent.kt is not ending with a new line.
```
```kotlin
15         object NavigateBack : Output()
16     }
17 
18 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonScreen.kt:79:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonScreen.kt is not ending with a new line.
```
```kotlin
76         }
77     }
78 
79 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/DetailsComponent.kt:42:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/DetailsComponent.kt is not ending with a new line.
```
```kotlin
39         object NavigateBack : Output()
40     }
41 
42 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/DetailsScreen.kt:19:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/DetailsScreen.kt is not ending with a new line.
```
```kotlin
16         onOutput = component::onOutput
17     )
18 
19 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/AbilityItem.kt:30:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/AbilityItem.kt is not ending with a new line.
```
```kotlin
27             .padding(horizontal = 10.dp, vertical = 4.dp)
28     )
29 
30 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/AbilityRow.kt:28:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/AbilityRow.kt is not ending with a new line.
```
```kotlin
25             )
26         }
27     }
28 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:197:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt is not ending with a new line.
```
```kotlin
194             }
195         }
196     }
197 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:103:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt is not ending with a new line.
```
```kotlin
100             )
101         }
102     }
103 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:91:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt is not ending with a new line.
```
```kotlin
88                 }
89         )
90     }
91 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStats.kt:29:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStats.kt is not ending with a new line.
```
```kotlin
26             }
27         }
28     }
29 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStore.kt:18:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStore.kt is not ending with a new line.
```
```kotlin
15         val pokemonInfo: PokemonInfo? = null
16     )
17 
18 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStoreFactory.kt:92:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStoreFactory.kt is not ending with a new line.
```
```kotlin
89             }
90     }
91 
92 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/FavoriteComponent.kt:41:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/FavoriteComponent.kt is not ending with a new line.
```
```kotlin
38         data class NavigateToDetails(val name: String) : Output()
39     }
40 
41 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/FavoriteScreen.kt:17:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/FavoriteScreen.kt is not ending with a new line.
```
```kotlin
14         onEvent = favoriteComponent::onEvent,
15         onOutput = favoriteComponent::onOutput
16     )
17 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:101:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt is not ending with a new line.
```
```kotlin
98  
99          }
100     }
101 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/store/FavoriteStore.kt:16:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/store/FavoriteStore.kt is not ending with a new line.
```
```kotlin
13         val pokemonList: List<Pokemon> = emptyList(),
14     )
15 
16 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/store/FavoriteStoreFactory.kt:68:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/store/FavoriteStoreFactory.kt is not ending with a new line.
```
```kotlin
65                 is Msg.PokemonListFailed -> copy(error = msg.error)
66             }
67     }
68 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/helper/LocalSafeArea.kt:8:72
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/helper/LocalSafeArea.kt is not ending with a new line.
```
```kotlin
5  import androidx.compose.ui.unit.dp
6  
7  // Define a CompositionLocal global object that will contain IOS safe area
8  internal val LocalSafeArea = compositionLocalOf { PaddingValues(0.dp) }
!                                                                         ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainComponent.kt:44:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainComponent.kt is not ending with a new line.
```
```kotlin
41         data class PokedexSearchSubmitted(val searchValue: String) : Output()
42     }
43 
44 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:158:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt is not ending with a new line.
```
```kotlin
155             )
156         }
157     }
158 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/AsyncImage.kt:63:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/AsyncImage.kt is not ending with a new line.
```
```kotlin
60             }
61         }
62     }
63 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/CategoryButton.kt:75:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/CategoryButton.kt is not ending with a new line.
```
```kotlin
72             )
73         }
74     }
75 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:140:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt is not ending with a new line.
```
```kotlin
137         }
138 
139     }
140 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainModelDrawerSheet.kt:60:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainModelDrawerSheet.kt is not ending with a new line.
```
```kotlin
57             )
58         }
59     }
60 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt:81:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt is not ending with a new line.
```
```kotlin
78         )
79     }
80 
81 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoRow.kt:30:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoRow.kt is not ending with a new line.
```
```kotlin
27         }
28     }
29 
30 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/store/MainStore.kt:18:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/store/MainStore.kt is not ending with a new line.
```
```kotlin
15         val search: String = "",
16     )
17 
18 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/store/MainStoreFactory.kt:46:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/store/MainStoreFactory.kt is not ending with a new line.
```
```kotlin
43             }
44     }
45 
46 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/PokedexComponent.kt:44:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/PokedexComponent.kt is not ending with a new line.
```
```kotlin
41         data class NavigateToDetails(val name: String) : Output()
42     }
43 
44 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/PokedexScreen.kt:19:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/PokedexScreen.kt is not ending with a new line.
```
```kotlin
16         onOutput = component::onOutput
17     )
18 
19 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt:132:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt is not ending with a new line.
```
```kotlin
129 
130         }
131     }
132 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:72:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt is not ending with a new line.
```
```kotlin
69 
70         }
71     }
72 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:94:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt is not ending with a new line.
```
```kotlin
91             )
92         }
93     }
94 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:77:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt is not ending with a new line.
```
```kotlin
74             )
75         }
76     }
77 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStore.kt:20:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStore.kt is not ending with a new line.
```
```kotlin
17         val pokemonList: List<Pokemon> = emptyList(),
18         val searchValue: String = "",
19     )
20 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStoreFactory.kt:89:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStoreFactory.kt is not ending with a new line.
```
```kotlin
86                 Msg.LastPageLoaded -> copy(isLastPageLoaded = true)
87             }
88     }
89 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootComponent.kt:144:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootComponent.kt is not ending with a new line.
```
```kotlin
141         data class ComingSoon(val component: ComingSoonComponent) : Child()
142     }
143 
144 }
!!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootContent.kt:27:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootContent.kt is not ending with a new line.
```
```kotlin
24             is RootComponent.Child.ComingSoon -> ComingSoonScreen(child.component)
25         }
26     }
27 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt:46:31
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Color.kt is not ending with a new line.
```
```kotlin
43 val Water = Color(0xFF2648DC)
44 val Fighting = Color(0xFF9F422A)
45 val Grass = Color(0xFF007C42)
46 val Ground = Color(0xFFAD7235)
!!                               ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Shape.kt:13:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Shape.kt is not ending with a new line.
```
```kotlin
10     medium = RoundedCornerShape(12.dp),
11     large = RoundedCornerShape(16.dp),
12     extraLarge = RoundedCornerShape(20.dp)
13 )
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Theme.kt:59:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Theme.kt is not ending with a new line.
```
```kotlin
56         shapes = Shapes,
57         content = content
58     )
59 }
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Type.kt:41:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/theme/Type.kt is not ending with a new line.
```
```kotlin
38         fontSize = 12.sp
39     )
40     */
41 )
!!  ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/KgHelper.kt:3:47
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/KgHelper.kt is not ending with a new line.
```
```kotlin
1 package com.mocoding.pokedex.ui.utils
2 
3 fun kgToPounds(kg: Float): Float = kg * 2.205f
!                                               ^ error

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/PokemonAbilityUtils.kt:29:2
```
The file /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/PokemonAbilityUtils.kt is not ending with a new line.
```
```kotlin
26          else -> Gray400
27      }
28 
29 }
!!  ^ error

```

### style, UnusedParameter (2)

Function parameter is unused and should be removed.

[Documentation](https://detekt.dev/docs/rules/style#unusedparameter)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt:9:31
```
Function parameter `enableLogging` is unused.
```
```kotlin
6  import io.ktor.serialization.kotlinx.json.*
7  import kotlinx.serialization.json.Json
8  
9  internal fun createHttpClient(enableLogging: Boolean): HttpClient {
!                                ^ error
10     return createPlatformHttpClient().config {
11         install(ContentNegotiation) {
12             json(Json {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:21:5
```
Function parameter `onEvent` is unused.
```
```kotlin
18 @Composable
19 internal fun FavoriteContent(
20     state: FavoriteStore.State,
21     onEvent: (FavoriteStore.Intent) -> Unit,
!!     ^ error
22     onOutput: (FavoriteComponent.Output) -> Unit,
23 ) {
24     Scaffold(

```

### style, WildcardImport (37)

Wildcard imports should be replaced with imports using fully qualified class names. Wildcard imports can lead to naming conflicts. A library update can introduce naming clashes with your classes which results in compilation errors.

[Documentation](https://detekt.dev/docs/rules/style#wildcardimport)

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt:3:1
```
io.ktor.client.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.core.network
2 
3 import io.ktor.client.*
! ^ error
4 import io.ktor.client.plugins.contentnegotiation.*
5 import io.ktor.client.plugins.logging.*
6 import io.ktor.serialization.kotlinx.json.*

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt:4:1
```
io.ktor.client.plugins.contentnegotiation.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.core.network
2 
3 import io.ktor.client.*
4 import io.ktor.client.plugins.contentnegotiation.*
! ^ error
5 import io.ktor.client.plugins.logging.*
6 import io.ktor.serialization.kotlinx.json.*
7 import kotlinx.serialization.json.Json

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt:5:1
```
io.ktor.client.plugins.logging.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
2 
3 import io.ktor.client.*
4 import io.ktor.client.plugins.contentnegotiation.*
5 import io.ktor.client.plugins.logging.*
! ^ error
6 import io.ktor.serialization.kotlinx.json.*
7 import kotlinx.serialization.json.Json
8 

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt:6:1
```
io.ktor.serialization.kotlinx.json.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
3  import io.ktor.client.*
4  import io.ktor.client.plugins.contentnegotiation.*
5  import io.ktor.client.plugins.logging.*
6  import io.ktor.serialization.kotlinx.json.*
!  ^ error
7  import kotlinx.serialization.json.Json
8  
9  internal fun createHttpClient(enableLogging: Boolean): HttpClient {

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonScreen.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.comingsoon
2 
3 import androidx.compose.foundation.Image
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material.icons.Icons
6 import androidx.compose.material.icons.outlined.Timelapse
7 import androidx.compose.material.icons.rounded.ArrowBackIosNew

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/comingsoon/ComingSoonScreen.kt:8:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
5  import androidx.compose.material.icons.Icons
6  import androidx.compose.material.icons.outlined.Timelapse
7  import androidx.compose.material.icons.rounded.ArrowBackIosNew
8  import androidx.compose.material3.*
!  ^ error
9  import androidx.compose.runtime.Composable
10 import androidx.compose.ui.Alignment
11 import androidx.compose.ui.Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:3:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.details.components
2 
3 import androidx.compose.foundation.layout.*
! ^ error
4 import androidx.compose.foundation.lazy.LazyColumn
5 import androidx.compose.material.icons.Icons
6 import androidx.compose.material.icons.rounded.ArrowBackIosNew

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/DetailsContent.kt:9:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
6  import androidx.compose.material.icons.rounded.ArrowBackIosNew
7  import androidx.compose.material.icons.rounded.Favorite
8  import androidx.compose.material.icons.rounded.FavoriteBorder
9  import androidx.compose.material3.*
!  ^ error
10 import androidx.compose.runtime.Composable
11 import androidx.compose.ui.Alignment
12 import androidx.compose.ui.Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonInfos.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.details.components
2 
3 import androidx.compose.foundation.background
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material.icons.Icons
6 import androidx.compose.material.icons.outlined.Scale
7 import androidx.compose.material.icons.outlined.Straighten

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:3:1
```
androidx.compose.animation.core.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.details.components
2 
3 import androidx.compose.animation.core.*
! ^ error
4 import androidx.compose.foundation.layout.*
5 import androidx.compose.material3.MaterialTheme
6 import androidx.compose.material3.Text

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStatItem.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.details.components
2 
3 import androidx.compose.animation.core.*
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material3.MaterialTheme
6 import androidx.compose.material3.Text
7 import androidx.compose.runtime.Composable

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/components/PokemonStats.kt:3:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.details.components
2 
3 import androidx.compose.foundation.layout.*
! ^ error
4 import androidx.compose.runtime.Composable
5 import androidx.compose.runtime.key
6 import androidx.compose.ui.Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:3:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.favorite.components
2 
3 import androidx.compose.foundation.layout.*
! ^ error
4 import androidx.compose.material.icons.Icons
5 import androidx.compose.material.icons.rounded.ArrowBackIosNew
6 import androidx.compose.material3.*

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/components/FavoriteContent.kt:6:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
3  import androidx.compose.foundation.layout.*
4  import androidx.compose.material.icons.Icons
5  import androidx.compose.material.icons.rounded.ArrowBackIosNew
6  import androidx.compose.material3.*
!  ^ error
7  import androidx.compose.runtime.Composable
8  import androidx.compose.ui.Alignment
9  import androidx.compose.ui.Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:3:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.main
2 
3 import androidx.compose.foundation.layout.*
! ^ error
4 import androidx.compose.material.icons.Icons
5 import androidx.compose.material.icons.filled.Favorite
6 import androidx.compose.material.icons.filled.Home

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:10:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
7  import androidx.compose.material.icons.outlined.Favorite
8  import androidx.compose.material.icons.outlined.Home
9  import androidx.compose.material.icons.rounded.Menu
10 import androidx.compose.material3.*
!! ^ error
11 import androidx.compose.runtime.*
12 import androidx.compose.ui.Modifier
13 import androidx.compose.ui.graphics.Color

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/MainScreen.kt:11:1
```
androidx.compose.runtime.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
8  import androidx.compose.material.icons.outlined.Home
9  import androidx.compose.material.icons.rounded.Menu
10 import androidx.compose.material3.*
11 import androidx.compose.runtime.*
!! ^ error
12 import androidx.compose.ui.Modifier
13 import androidx.compose.ui.graphics.Color
14 import androidx.compose.ui.graphics.vector.ImageVector

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/AsyncImage.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.main.components
2 
3 import androidx.compose.foundation.Image
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material3.CircularProgressIndicator
6 import androidx.compose.material3.Text
7 import androidx.compose.runtime.Composable

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/CategoryButton.kt:5:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
2 
3 import androidx.compose.foundation.background
4 import androidx.compose.foundation.clickable
5 import androidx.compose.foundation.layout.*
! ^ error
6 import androidx.compose.material3.MaterialTheme
7 import androidx.compose.material3.Text
8 import androidx.compose.runtime.Composable

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:3:1
```
androidx.compose.foundation.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.main.components
2 
3 import androidx.compose.foundation.*
! ^ error
4 import androidx.compose.foundation.layout.*
5 import androidx.compose.material.icons.Icons
6 import androidx.compose.material.icons.rounded.Search

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.main.components
2 
3 import androidx.compose.foundation.*
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material.icons.Icons
6 import androidx.compose.material.icons.rounded.Search
7 import androidx.compose.material3.*

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:7:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
4  import androidx.compose.foundation.layout.*
5  import androidx.compose.material.icons.Icons
6  import androidx.compose.material.icons.rounded.Search
7  import androidx.compose.material3.*
!  ^ error
8  import androidx.compose.runtime.*
9  import androidx.compose.ui.Modifier
10 import androidx.compose.ui.graphics.Color

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainContent.kt:8:1
```
androidx.compose.runtime.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
5  import androidx.compose.material.icons.Icons
6  import androidx.compose.material.icons.rounded.Search
7  import androidx.compose.material3.*
8  import androidx.compose.runtime.*
!  ^ error
9  import androidx.compose.ui.Modifier
10 import androidx.compose.ui.graphics.Color
11 import androidx.compose.ui.text.font.FontWeight

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/MainModelDrawerSheet.kt:7:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
4  import androidx.compose.foundation.layout.WindowInsets
5  import androidx.compose.foundation.layout.height
6  import androidx.compose.foundation.layout.padding
7  import androidx.compose.material3.*
!  ^ error
8  import androidx.compose.runtime.Composable
9  import androidx.compose.ui.Modifier
10 import androidx.compose.ui.graphics.Color

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/components/VideoItem.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.main.components
2 
3 import androidx.compose.foundation.clickable
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material.icons.Icons
6 import androidx.compose.material.icons.outlined.Circle
7 import androidx.compose.material.icons.rounded.PlayArrow

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/main/state/CategoryState.kt:4:1
```
com.mocoding.pokedex.ui.theme.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.main.state
2 
3 import androidx.compose.ui.graphics.Color
4 import com.mocoding.pokedex.ui.theme.*
! ^ error
5 
6 data class CategoryState(
7     val title: String,

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt:3:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.pokedex.components
2 
3 import androidx.compose.foundation.layout.*
! ^ error
4 import androidx.compose.material.icons.Icons
5 import androidx.compose.material.icons.rounded.ArrowBackIosNew
6 import androidx.compose.material3.*

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt:6:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
3  import androidx.compose.foundation.layout.*
4  import androidx.compose.material.icons.Icons
5  import androidx.compose.material.icons.rounded.ArrowBackIosNew
6  import androidx.compose.material3.*
!  ^ error
7  import androidx.compose.runtime.Composable
8  import androidx.compose.ui.Alignment
9  import androidx.compose.ui.Modifier

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokedexContent.kt:16:1
```
com.mocoding.pokedex.ui.theme.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
13 import com.mocoding.pokedex.ui.helper.LocalSafeArea
14 import com.mocoding.pokedex.ui.pokedex.PokedexComponent
15 import com.mocoding.pokedex.ui.pokedex.store.PokedexStore
16 import com.mocoding.pokedex.ui.theme.*
!! ^ error
17 
18 @OptIn(ExperimentalMaterial3Api::class)
19 @Composable

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonGrid.kt:3:1
```
androidx.compose.animation.core.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.pokedex.components
2 
3 import androidx.compose.animation.core.*
! ^ error
4 import androidx.compose.foundation.layout.Arrangement
5 import androidx.compose.foundation.layout.BoxWithConstraints
6 import androidx.compose.foundation.layout.PaddingValues

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:4:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.pokedex.components
2 
3 import androidx.compose.foundation.background
4 import androidx.compose.foundation.layout.*
! ^ error
5 import androidx.compose.material3.*
6 import androidx.compose.runtime.Composable
7 import androidx.compose.runtime.remember

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:5:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
2 
3 import androidx.compose.foundation.background
4 import androidx.compose.foundation.layout.*
5 import androidx.compose.material3.*
! ^ error
6 import androidx.compose.runtime.Composable
7 import androidx.compose.runtime.remember
8 import androidx.compose.ui.Alignment

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonItem.kt:18:1
```
com.mocoding.pokedex.ui.theme.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
15 import androidx.compose.ui.unit.dp
16 import com.mocoding.pokedex.core.model.Pokemon
17 import com.mocoding.pokedex.ui.main.components.AsyncImage
18 import com.mocoding.pokedex.ui.theme.*
!! ^ error
19 
20 @OptIn(ExperimentalMaterial3Api::class)
21 @Composable

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:3:1
```
androidx.compose.animation.core.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.pokedex.components
2 
3 import androidx.compose.animation.core.*
! ^ error
4 import androidx.compose.foundation.background
5 import androidx.compose.foundation.layout.*
6 import androidx.compose.material3.*

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:5:1
```
androidx.compose.foundation.layout.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
2 
3 import androidx.compose.animation.core.*
4 import androidx.compose.foundation.background
5 import androidx.compose.foundation.layout.*
! ^ error
6 import androidx.compose.material3.*
7 import androidx.compose.runtime.Composable
8 import androidx.compose.runtime.remember

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/components/PokemonLoadingItem.kt:6:1
```
androidx.compose.material3.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
3  import androidx.compose.animation.core.*
4  import androidx.compose.foundation.background
5  import androidx.compose.foundation.layout.*
6  import androidx.compose.material3.*
!  ^ error
7  import androidx.compose.runtime.Composable
8  import androidx.compose.runtime.remember
9  import androidx.compose.ui.Alignment

```

* /tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/utils/PokemonAbilityUtils.kt:4:1
```
com.mocoding.pokedex.ui.theme.* is a wildcard import. Replace it with fully qualified imports.
```
```kotlin
1 package com.mocoding.pokedex.ui.utils
2 
3 import androidx.compose.ui.graphics.Color
4 import com.mocoding.pokedex.ui.theme.*
! ^ error
5 
6 object PokemonAbilityUtils {
7 

```

generated with [detekt version 1.23.7](https://detekt.dev/) on 2026-05-29 02:13:51 UTC
