from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_pokemon_retorna_200():
    """GET /api/pokemon/ deve retornar 200 e uma lista de Pokémon."""
    response = client.get("/api/pokemon/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5


def test_get_pokemon_por_id_retorna_dados_validos():
    """GET /api/pokemon/{id} deve retornar dados válidos do Pokémon."""
    response = client.get("/api/pokemon/25")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "pikachu"
    assert data["id"] == 25
    assert "height_meters" in data
    assert "weight_kg" in data
    assert "stats" in data
    assert "abilities" in data


def test_get_pokemon_inexistente_retorna_404():
    """GET /api/pokemon/{id} deve retornar 404 para Pokémon inexistente."""
    response = client.get("/api/pokemon/pokemon-inexistente-xyz")
    assert response.status_code == 404