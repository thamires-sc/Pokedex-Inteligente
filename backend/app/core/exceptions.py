from fastapi import HTTPException

# ── Pokémon ───────────────────────────────────────────────────

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


# ── LLM ───────────────────────────────────────────────────────

class LLMNotConfiguredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=503,
            detail="Chave da API LLM não configurada. Verifique o arquivo .env."
        )


class LLMInvalidKeyException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Chave da API LLM inválida ou expirada."
        )


class LLMRateLimitException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Limite de requisições atingido. Tente novamente em breve."
        )


class LLMUnavailableException(HTTPException):
    def __init__(self, status_code: int):
        super().__init__(
            status_code=502,
            detail=f"Erro na API LLM (status {status_code})."
        )


class LLMUnexpectedResponseException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=502,
            detail=f"Resposta inesperada da API LLM: {detail}"
        )