import httpx

from app.core.config import settings
from app.core.exceptions import PokemonNotFoundException, ExternalAPIException

async def get_pokemon_list(limit: int, offset: int) -> dict:
    """Busca a lista paginada de Pokémon na PokéAPI."""
    url = f"{settings.POKEAPI_BASE_URL}/pokemon"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params={"limit": limit, "offset": offset})
        if response.status_code != 200:
            raise ExternalAPIException("PokéAPI")
        return response.json()


async def get_pokemon_by_name_or_id(name_or_id: str) -> dict:
    """Busca os dados crus de um Pokémon pelo nome ou ID na PokéAPI."""
    url = f"{settings.POKEAPI_BASE_URL}/pokemon/{name_or_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        if response.status_code == 404:
            raise PokemonNotFoundException(name_or_id)
        if response.status_code != 200:
            raise ExternalAPIException("PokéAPI")
        return response.json()


async def get_pokemon_by_url(url: str) -> dict | None:
    """Busca os dados crus de um Pokémon por URL completa (usado na listagem)."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        if response.status_code != 200:
            return None
        return response.json()