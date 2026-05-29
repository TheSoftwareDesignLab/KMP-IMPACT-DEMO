### Dependabot impact companion

- **Dependency:** `io.ktor`
- **Version change:** `2.3.10` → `2.3.13`
- **Risk:** **HIGH**
- **Recommendation:** Hold merge until impacted files are reviewed and targeted regression checks pass.
- **Static impact:** 46 files (8 direct / 38 transitive-or-expect-actual)
- **UI impact:** 6 screens
- **Dynamic analysis:** completed (0 screen diffs)
- **Full report:** generated as static artifact/site in `output/report/`

### Top impacted files

| File | Relation | Source set | RLOC | MCC |
|------|----------|------------|------|-----|
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/helper/ErrorHandler.kt` | direct | commonMain | 28 | 5 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/client/PokemonClient.kt` | direct | commonMain | 38 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClient.kt` | direct | commonMain | 19 | 1 |
| `/tmp/output/phase1/before/tools/kmp-impact-analyzer/tests/fixtures/sample_kotlin/CommonModule.kt` | direct | common | 8 | 1 |
| `/tmp/output/phase1/before/shared/src/androidMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt` | direct | androidMain | 6 | 1 |
| `/tmp/output/phase1/before/shared/src/desktopMain/kotlin/com.mocoding.pokedex/core/network/HttpClientFactory.kt` | direct | desktopMain | 6 | 1 |
| `/tmp/output/phase1/before/shared/src/iosMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt` | direct | ios | 6 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/HttpClientFactory.kt` | direct | commonMain | 3 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/root/RootComponent.kt` | transitive | commonMain | 128 | 7 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStoreFactory.kt` | transitive | commonMain | 78 | 7 |
