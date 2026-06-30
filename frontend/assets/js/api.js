const API_BASE_URL = 'http://127.0.0.1:8000';

async function fetchPokemonList(limit = 20, offset = 0) {
  const response = await fetch(`${API_BASE_URL}/api/pokemon/?limit=${limit}&offset=${offset}`);
  if (!response.ok) throw new Error('Erro ao buscar lista de Pokémon.');
  return response.json();
}

async function fetchPokemonDetail(nameOrId) {
  const response = await fetch(`${API_BASE_URL}/api/pokemon/${nameOrId}`);
  if (!response.ok) throw new Error(`Pokémon '${nameOrId}' não encontrado.`);
  return response.json();
}

async function sendChatMessage(pokemonName, question) {
  const response = await fetch(`${API_BASE_URL}/api/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pokemon_name: pokemonName, question }),
  });
  if (!response.ok) throw new Error('Erro ao consultar o Professor Carvalho.');
  return response.json();
}