from pydantic import BaseModel


class ChatRequest(BaseModel):
    pokemon_name: str
    question: str


class ChatResponse(BaseModel):
    answer: str
    pokemon_name: str