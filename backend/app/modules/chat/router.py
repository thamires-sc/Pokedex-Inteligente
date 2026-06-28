from fastapi import APIRouter

from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.service import ask_llm
from app.modules.pokemon.service import fetch_pokemon_detail

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_with_pokemon(body: ChatRequest):
    """
    Recebe o nome do Pokémon e a pergunta do usuário.
    Busca os dados atualizados na PokéAPI, monta o contexto e consulta o LLM.
    Retorna a resposta gerada pelo modelo.
    """
    pokemon = await fetch_pokemon_detail(body.pokemon_name.lower())
    answer = await ask_llm(pokemon=pokemon, question=body.question)

    return ChatResponse(answer=answer, pokemon_name=pokemon.name)