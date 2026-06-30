from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)


def test_chat_com_dados_validos_retorna_200():
    """POST /api/chat/ com dados válidos deve retornar 200 com a resposta do LLM."""
    with patch("app.modules.chat.service.ask_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "O Pikachu é fraco contra ataques do tipo Terra!"
        response = client.post(
            "/api/chat/",
            json={"pokemon_name": "pikachu", "question": "Quais são as fraquezas?"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["pokemon_name"] == "pikachu"
    assert "answer" in data


def test_chat_com_dados_invalidos_retorna_422():
    """POST /api/chat/ sem o campo question deve retornar 422."""
    response = client.post(
        "/api/chat/",
        json={"pokemon_name": "pikachu"},
    )
    assert response.status_code == 422


def test_chat_pokemon_inexistente_retorna_404():
    """POST /api/chat/ com Pokémon inexistente deve retornar 404."""
    response = client.post(
        "/api/chat/",
        json={"pokemon_name": "pokemon-inexistente-xyz", "question": "Teste"},
    )
    assert response.status_code == 404