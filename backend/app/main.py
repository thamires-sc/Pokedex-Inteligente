from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.pokemon.router import router as pokemon_router
from app.modules.chat.router import router as chat_router

app = FastAPI(
    title="Pokédex Inteligente",
    description="API da Pokédex com integração LLM para análise de Pokémon",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pokemon_router, prefix="/api/pokemon", tags=["Pokémon"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat LLM"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Pokédex Inteligente API rodando!"}