package commocodingpokedex

import kotlin.Long
import kotlin.String

public data class PokemonEntity(
  public val page: Long,
  public val name: String,
  public val url: String,
)
