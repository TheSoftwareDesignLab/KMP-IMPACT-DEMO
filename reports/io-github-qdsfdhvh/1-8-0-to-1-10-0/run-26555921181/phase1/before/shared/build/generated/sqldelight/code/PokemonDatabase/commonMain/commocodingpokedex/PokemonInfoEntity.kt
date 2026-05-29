package commocodingpokedex

import kotlin.Long
import kotlin.String

public data class PokemonInfoEntity(
  public val id: Long,
  public val name: String,
  public val height: Long,
  public val weight: Long,
  public val experience: Long,
  public val types: String,
  public val stats: String,
  public val isFavorite: Long,
)
