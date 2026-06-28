from app.modules.pokemon.schemas import (
    PokemonDetail,
    PokemonSummary,
    PokemonType,
    PokemonStat,
    PokemonAbility,
)


def to_summary(raw: dict) -> PokemonSummary:
    """Converte o dict cru da PokéAPI para o schema de listagem."""
    return PokemonSummary(
        id=raw["id"],
        name=raw["name"],
        image=raw["sprites"].get("front_default"),
        types=[PokemonType(name=t["type"]["name"]) for t in raw["types"]],
    )


def to_detail(raw: dict) -> PokemonDetail:
    """Converte o dict cru da PokéAPI para o schema de detalhes."""
    return PokemonDetail(
        id=raw["id"],
        name=raw["name"],
        height_meters=raw["height"] / 10,
        weight_kg=raw["weight"] / 10,
        base_experience=raw.get("base_experience"),
        image=raw["sprites"].get("front_default"),
        image_shiny=raw["sprites"].get("front_shiny"),
        types=[PokemonType(name=t["type"]["name"]) for t in raw["types"]],
        stats=[PokemonStat(name=s["stat"]["name"], base_stat=s["base_stat"]) for s in raw["stats"]],
        abilities=[PokemonAbility(name=a["ability"]["name"], is_hidden=a["is_hidden"]) for a in raw["abilities"]],
    )