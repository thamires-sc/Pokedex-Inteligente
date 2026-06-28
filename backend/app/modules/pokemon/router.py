from fastapi import APIRouter, Query

from app.modules.pokemon.schemas import PokemonDetail, PokemonSummary
from app.modules.pokemon.service import fetch_pokemon_detail, fetch_pokemon_list_with_sprites

router = APIRouter()


@router.get("/", response_model=list[PokemonSummary])
async def list_pokemon(
    limit: int = Query(default=20, ge=1, le=100, description="Quantidade de Pokémon por página"),
    offset: int = Query(default=0, ge=0, description="Índice inicial para paginação"),
):
    """Retorna lista paginada de Pokémon com id, nome, sprite e tipos."""
    return await fetch_pokemon_list_with_sprites(limit=limit, offset=offset)


@router.get("/{name_or_id}", response_model=PokemonDetail)
async def get_pokemon(name_or_id: str):
    """Retorna detalhes completos de um Pokémon pelo nome ou ID."""
    return await fetch_pokemon_detail(name_or_id.lower())