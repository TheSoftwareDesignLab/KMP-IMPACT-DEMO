package commocodingpokedex

import app.cash.sqldelight.Query
import app.cash.sqldelight.TransacterImpl
import app.cash.sqldelight.db.QueryResult
import app.cash.sqldelight.db.SqlCursor
import app.cash.sqldelight.db.SqlDriver
import kotlin.Any
import kotlin.Long
import kotlin.String

public class PokemonInfoEntityQueries(
  driver: SqlDriver,
) : TransacterImpl(driver) {
  public fun <T : Any> selectOneByName(name: String, mapper: (
    id: Long,
    name: String,
    height: Long,
    weight: Long,
    experience: Long,
    types: String,
    stats: String,
    isFavorite: Long,
  ) -> T): Query<T> = SelectOneByNameQuery(name) { cursor ->
    mapper(
      cursor.getLong(0)!!,
      cursor.getString(1)!!,
      cursor.getLong(2)!!,
      cursor.getLong(3)!!,
      cursor.getLong(4)!!,
      cursor.getString(5)!!,
      cursor.getString(6)!!,
      cursor.getLong(7)!!
    )
  }

  public fun selectOneByName(name: String): Query<PokemonInfoEntity> = selectOneByName(name) { id,
      name_, height, weight, experience, types, stats, isFavorite ->
    PokemonInfoEntity(
      id,
      name_,
      height,
      weight,
      experience,
      types,
      stats,
      isFavorite
    )
  }

  public fun <T : Any> selectAllFavorite(mapper: (
    id: Long,
    name: String,
    height: Long,
    weight: Long,
    experience: Long,
    types: String,
    stats: String,
    isFavorite: Long,
  ) -> T): Query<T> = Query(-2_110_085_000, arrayOf("pokemonInfoEntity"), driver,
      "PokemonInfoEntity.sq", "selectAllFavorite", """
  |SELECT *
  |FROM pokemonInfoEntity
  |WHERE isFavorite != 0
  """.trimMargin()) { cursor ->
    mapper(
      cursor.getLong(0)!!,
      cursor.getString(1)!!,
      cursor.getLong(2)!!,
      cursor.getLong(3)!!,
      cursor.getLong(4)!!,
      cursor.getString(5)!!,
      cursor.getString(6)!!,
      cursor.getLong(7)!!
    )
  }

  public fun selectAllFavorite(): Query<PokemonInfoEntity> = selectAllFavorite { id, name, height,
      weight, experience, types, stats, isFavorite ->
    PokemonInfoEntity(
      id,
      name,
      height,
      weight,
      experience,
      types,
      stats,
      isFavorite
    )
  }

  public fun insert(pokemonInfoEntity: PokemonInfoEntity) {
    driver.execute(-2_056_316_318, """
        |INSERT OR REPLACE INTO pokemonInfoEntity(id, name, height, weight, experience, types, stats, isFavorite)
        |VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """.trimMargin(), 8) {
          bindLong(0, pokemonInfoEntity.id)
          bindString(1, pokemonInfoEntity.name)
          bindLong(2, pokemonInfoEntity.height)
          bindLong(3, pokemonInfoEntity.weight)
          bindLong(4, pokemonInfoEntity.experience)
          bindString(5, pokemonInfoEntity.types)
          bindString(6, pokemonInfoEntity.stats)
          bindLong(7, pokemonInfoEntity.isFavorite)
        }
    notifyQueries(-2_056_316_318) { emit ->
      emit("pokemonInfoEntity")
    }
  }

  public fun updateIsFavorite(isFavorite: Long, name: String) {
    driver.execute(755_857_144, """
        |UPDATE pokemonInfoEntity
        |SET isFavorite = ?
        |WHERE name = ?
        """.trimMargin(), 2) {
          bindLong(0, isFavorite)
          bindString(1, name)
        }
    notifyQueries(755_857_144) { emit ->
      emit("pokemonInfoEntity")
    }
  }

  private inner class SelectOneByNameQuery<out T : Any>(
    public val name: String,
    mapper: (SqlCursor) -> T,
  ) : Query<T>(mapper) {
    override fun addListener(listener: Query.Listener) {
      driver.addListener("pokemonInfoEntity", listener = listener)
    }

    override fun removeListener(listener: Query.Listener) {
      driver.removeListener("pokemonInfoEntity", listener = listener)
    }

    override fun <R> execute(mapper: (SqlCursor) -> QueryResult<R>): QueryResult<R> =
        driver.executeQuery(771_271_267, """
    |SELECT *
    |FROM pokemonInfoEntity
    |WHERE name = ?
    """.trimMargin(), mapper, 1) {
      bindString(0, name)
    }

    override fun toString(): String = "PokemonInfoEntity.sq:selectOneByName"
  }
}
