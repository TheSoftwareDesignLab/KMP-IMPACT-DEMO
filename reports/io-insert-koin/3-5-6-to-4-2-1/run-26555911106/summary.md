### Dependabot impact companion

- **Dependency:** `io.insert-koin`
- **Version change:** `3.5.6` → `4.2.1`
- **Risk:** **HIGH**
- **Recommendation:** Hold merge until impacted files are reviewed and targeted regression checks pass.
- **Static impact:** 42 files (13 direct / 29 transitive-or-expect-actual)
- **UI impact:** 5 screens
- **Dynamic analysis:** completed (0 screen diffs)
- **Full report:** generated as static artifact/site in `output/report/`

### Top impacted files

| File | Relation | Source set | RLOC | MCC |
|------|----------|------------|------|-----|
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/pokedex/store/PokedexStoreFactory.kt` | direct | commonMain | 78 | 7 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/data/repository/PokemonRepositoryImpl.kt` | direct | commonMain | 61 | 7 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/details/store/DetailsStoreFactory.kt` | direct | commonMain | 78 | 5 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/ui/favorite/store/FavoriteStoreFactory.kt` | direct | commonMain | 57 | 3 |
| `/tmp/output/phase1/before/android/src/main/java/com/mocoding/pokedex/android/MainActivity.kt` | direct | main | 33 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/di/AppModule.kt` | direct | commonMain | 15 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/di/DatabaseModule.kt` | direct | commonMain | 12 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/network/di/NetworkModule.kt` | direct | commonMain | 11 | 1 |
| `/tmp/output/phase1/before/shared/src/desktopMain/kotlin/com.mocoding.pokedex/core/database/DesktopSqlDriverFactory.kt` | direct | desktopMain | 11 | 1 |
| `/tmp/output/phase1/before/shared/src/commonMain/kotlin/com/mocoding/pokedex/core/database/SqlDriverFactory.kt` | direct | commonMain | 10 | 1 |
