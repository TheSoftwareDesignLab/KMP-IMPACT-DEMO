package com.mocoding.pokedex.core.database.shared

import app.cash.sqldelight.TransacterImpl
import app.cash.sqldelight.db.AfterVersion
import app.cash.sqldelight.db.QueryResult
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.db.SqlSchema
import com.mocoding.pokedex.core.database.PokemonDatabase
import commocodingpokedex.PokemonEntityQueries
import commocodingpokedex.PokemonInfoEntityQueries
import kotlin.Long
import kotlin.Unit
import kotlin.reflect.KClass

internal val KClass<PokemonDatabase>.schema: SqlSchema<QueryResult.Value<Unit>>
  get() = PokemonDatabaseImpl.Schema

internal fun KClass<PokemonDatabase>.newInstance(driver: SqlDriver): PokemonDatabase =
    PokemonDatabaseImpl(driver)

private class PokemonDatabaseImpl(
  driver: SqlDriver,
) : TransacterImpl(driver), PokemonDatabase {
  override val pokemonEntityQueries: PokemonEntityQueries = PokemonEntityQueries(driver)

  override val pokemonInfoEntityQueries: PokemonInfoEntityQueries = PokemonInfoEntityQueries(driver)

  public object Schema : SqlSchema<QueryResult.Value<Unit>> {
    override val version: Long
      get() = 1

    override fun create(driver: SqlDriver): QueryResult.Value<Unit> {
      driver.execute(null, """
          |CREATE TABLE IF NOT EXISTS pokemonEntity (
          |  page INTEGER NOT NULL,
          |  name TEXT NOT NULL PRIMARY KEY,
          |  url TEXT NOT NULL
          |)
          """.trimMargin(), 0)
      driver.execute(null, """
          |CREATE TABLE IF NOT EXISTS pokemonInfoEntity (
          |  id INTEGER NOT NULL PRIMARY KEY,
          |  name TEXT NOT NULL,
          |  height INTEGER NOT NULL,
          |  weight INTEGER NOT NULL,
          |  experience INTEGER NOT NULL,
          |  types TEXT NOT NULL,
          |  stats TEXT NOT NULL,
          |  isFavorite INTEGER DEFAULT 0 NOT NULL
          |)
          """.trimMargin(), 0)
      return QueryResult.Unit
    }

    override fun migrate(
      driver: SqlDriver,
      oldVersion: Long,
      newVersion: Long,
      vararg callbacks: AfterVersion,
    ): QueryResult.Value<Unit> = QueryResult.Unit
  }
}
