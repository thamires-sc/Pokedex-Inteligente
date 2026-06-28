import httpx
from fastapi import HTTPException

from app.core.config import settings


async def get_pokemon_list(limit: int, offset: int) -> dict:
    """Busca a lista paginada de Pokémon na PokéAPI."""
    url = f"{settings.POKEAPI_BASE_URL}/pokemon"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params={"limit": limit, "offset": offset})
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao buscar lista de Pokémon.")
        return response.json()


async def get_pokemon_by_name_or_id(name_or_id: str) -> dict:
    """Busca os dados crus de um Pokémon pelo nome ou ID na PokéAPI."""
    url = f"{settings.POKEAPI_BASE_URL}/pokemon/{name_or_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Pokémon '{name_or_id}' não encontrado.")
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao buscar detalhes do Pokémon.")
        return response.json()


async def get_pokemon_by_url(url: str) -> dict | None:
    """Busca os dados crus de um Pokémon por URL completa (usado na listagem)."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        if response.status_code != 200:
            return None
        return response.json()