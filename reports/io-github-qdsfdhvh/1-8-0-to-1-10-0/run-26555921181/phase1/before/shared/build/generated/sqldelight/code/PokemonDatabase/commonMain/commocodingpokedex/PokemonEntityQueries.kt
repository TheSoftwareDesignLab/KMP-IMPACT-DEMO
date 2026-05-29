package commocodingpokedex

import app.cash.sqldelight.Query
import app.cash.sqldelight.TransacterImpl
import app.cash.sqldelight.db.QueryResult
import app.cash.sqldelight.db.SqlCursor
import app.cash.sqldelight.db.SqlDriver
import kotlin.Any
import kotlin.Long
import kotlin.String

public class PokemonEntityQueries(
  driver: SqlDriver,
) : TransacterImpl(driver) {
  public fun <T : Any> selectAllByPage(page: Long, mapper: (
    page: Long,
    name: String,
    url: String,
  ) -> T): Query<T> = SelectAllByPageQuery(page) { cursor ->
    mapper(
      cursor.getLong(0)!!,
      cursor.getString(1)!!,
      cursor.getString(2)!!
    )
  }

  public fun selectAllByPage(page: Long): Query<PokemonEntity> = selectAllByPage(page) { page_,
      name, url ->
    PokemonEntity(
      page_,
      name,
      url
    )
  }

  public fun insert(pokemonEntity: PokemonEntity) {
    driver.execute(-636_263_788, """
        |INSERT OR REPLACE INTO pokemonEntity(page, name, url)
        |VALUES (?, ?, ?)
        """.trimMargin(), 3) {
          bindLong(0, pokemonEntity.page)
          bindString(1, pokemonEntity.name)
          bindString(2, pokemonEntity.url)
        }
    notifyQueries(-636_263_788) { emit ->
      emit("pokemonEntity")
    }
  }

  private inner class SelectAllByPageQuery<out T : Any>(
    public val page: Long,
    mapper: (SqlCursor) -> T,
  ) : Query<T>(mapper) {
    override fun addListener(listener: Query.Listener) {
      driver.addListener("pokemonEntity", listener = listener)
    }

    override fun removeListener(listener: Query.Listener) {
      driver.removeListener("pokemonEntity", listener = listener)
    }

    override fun <R> execute(mapper: (SqlCursor) -> QueryResult<R>): QueryResult<R> =
        driver.executeQuery(-1_228_302_992, """
    |SELECT *
    |FROM pokemonEntity
    |WHERE page = ?
    """.trimMargin(), mapper, 1) {
      bindLong(0, page)
    }

    override fun toString(): String = "PokemonEntity.sq:selectAllByPage"
  }
}
