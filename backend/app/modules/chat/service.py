import httpx

from app.core.config import settings
from app.core.exceptions import (
    LLMNotConfiguredException,
    LLMInvalidKeyException,
    LLMRateLimitException,
    LLMUnavailableException,
    LLMUnexpectedResponseException,
)
from app.modules.pokemon.schemas import PokemonDetail


def _build_system_prompt() -> str:
    """
    Define o papel e comportamento do modelo.
    """
    return (
        "Você é o Professor Carvalho, o maior especialista em Pokémon do mundo. "
        "Responda perguntas sobre Pokémon de forma clara, precisa e em português do Brasil. "
        "Você tem acesso aos dados oficiais do Pokémon fornecidos no contexto e os usa como base principal. "
        "Quando relevante, complemente com seu conhecimento sobre jogos, anime e mecânicas de batalha. "
        "Seja direto, didático e entusiasta. Use os dados do contexto nas respostas. "
        "Se não souber algo com certeza, diga isso claramente em vez de inventar."
        "IMPORTANTE: Responda sempre em texto simples, sem usar Markdown, "
        "sem asteriscos, sem tabelas, sem hashtags e sem formatação especial."
    )


def _build_user_prompt(pokemon: PokemonDetail, question: str) -> str:
    """
    Injeta os dados estruturados do Pokémon como contexto antes da pergunta.
    Garante respostas fundamentadas nos dados reais da PokéAPI.
    """
    types = ", ".join(t.name for t in pokemon.types)
    stats = "\n".join(f"  - {s.name}: {s.base_stat}" for s in pokemon.stats)
    abilities = ", ".join(
        f"{a.name} {'(oculta)' if a.is_hidden else ''}" for a in pokemon.abilities
    )

    context = f"""
=== DADOS DO POKÉMON ===
Nome: {pokemon.name.capitalize()}
ID Nacional: #{pokemon.id}
Tipos: {types}
Altura: {pokemon.height_meters} m
Peso: {pokemon.weight_kg} kg
Experiência base: {pokemon.base_experience or 'desconhecida'}

Estatísticas base:
{stats}

Habilidades: {abilities}
========================

Pergunta do treinador: {question}
"""
    return context


async def ask_llm(pokemon: PokemonDetail, question: str) -> str:
    """
    Envia o contexto do Pokémon e a pergunta para o OpenRouter.
    Retorna a resposta gerada pelo modelo.
    """
    if not settings.OPENROUTER_API_KEY:
        raise LLMNotConfiguredException()

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/pokedex-inteligente",
        "X-Title": "Pokedex Inteligente",
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": _build_system_prompt()},
            {"role": "user", "content": _build_user_prompt(pokemon, question)},
        ],
        "max_tokens": 600,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )

    if response.status_code == 401:
        raise LLMInvalidKeyException()
    if response.status_code == 429:
        raise LLMRateLimitException()
    if response.status_code != 200:
        raise LLMUnavailableException(status_code=response.status_code)

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise LLMUnexpectedResponseException(detail=f"Resposta inesperada da API LLM: {e}")