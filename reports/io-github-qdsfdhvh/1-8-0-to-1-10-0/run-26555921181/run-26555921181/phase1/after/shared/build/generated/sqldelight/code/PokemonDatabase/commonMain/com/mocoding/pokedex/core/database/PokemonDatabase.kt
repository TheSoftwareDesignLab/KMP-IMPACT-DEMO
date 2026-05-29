package com.mocoding.pokedex.core.database

import app.cash.sqldelight.Transacter
import app.cash.sqldelight.db.QueryResult
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.db.SqlSchema
import com.mocoding.pokedex.core.database.shared.newInstance
import com.mocoding.pokedex.core.database.shared.schema
import commocodingpokedex.PokemonEntityQueries
import commocodingpokedex.PokemonInfoEntityQueries
import kotlin.Unit

public interface PokemonDatabase : Transacter {
  public val pokemonEntityQueries: PokemonEntityQueries

  public val pokemonInfoEntityQueries: PokemonInfoEntityQueries

  public companion object {
    public val Schema: SqlSchema<QueryResult.Value<Unit>>
      get() = PokemonDatabase::class.schema

    public operator fun invoke(driver: SqlDriver): PokemonDatabase =
        PokemonDatabase::class.newInstance(driver)
  }
}
