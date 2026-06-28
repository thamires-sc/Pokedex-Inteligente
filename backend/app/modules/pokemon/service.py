from app.modules.pokemon.schemas import PokemonDetail, PokemonSummary
from app.modules.pokemon.client import get_pokemon_list, get_pokemon_by_name_or_id, get_pokemon_by_url
from app.modules.pokemon import mapper


async def fetch_pokemon_list_with_sprites(limit: int, offset: int) -> list[PokemonSummary]:
    """Busca lista paginada de Pokémon já com sprite e tipos."""
    data = await get_pokemon_list(limit=limit, offset=offset)
    results = data.get("results", [])

    summaries = []
    for item in results:
        raw = await get_pokemon_by_url(item["url"])
        if raw is None:
            continue
        summaries.append(mapper.to_summary(raw))

    return summaries


async def fetch_pokemon_detail(name_or_id: str) -> PokemonDetail:
    """Busca e normaliza os detalhes de um Pokémon pelo nome ou ID."""
    raw = await get_pokemon_by_name_or_id(name_or_id)
    return mapper.to_detail(raw)