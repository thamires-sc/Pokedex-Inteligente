from fastapi import HTTPException


class PokemonNotFoundException(HTTPException):
    def __init__(self, name_or_id: str):
        super().__init__(
            status_code=404,
            detail=f"Pokémon '{name_or_id}' não encontrado."
        )


class ExternalAPIException(HTTPException):
    def __init__(self, service: str = "PokéAPI"):
        super().__init__(
            status_code=502,
            detail=f"Erro ao se comunicar com o serviço externo: {service}."
        )