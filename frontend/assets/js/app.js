// ── Estado ───────────────────────────────────────────────────
const STATE = {
  currentPage: 1,
  limit: 18,
  selectedPokemon: null,
  pokemonList: [],
};

// ── Inicialização ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  loadPokemonList();
  setupEventListeners();
});

// ── Carregamento da lista ─────────────────────────────────────
async function loadPokemonList() {
  renderSkeletons();
  const offset = (STATE.currentPage - 1) * STATE.limit;

  try {
    STATE.pokemonList = await fetchPokemonList(STATE.limit, offset);
    console.log('Pokémon carregados:', STATE.pokemonList);
    renderPokemonGrid(STATE.pokemonList, STATE.selectedPokemon?.id);
    updatePagination(STATE.currentPage, STATE.currentPage > 1, STATE.pokemonList.length === STATE.limit);
  } catch (error) {
    console.error('Erro ao carregar lista:', error);
    document.getElementById('pokemonGrid').innerHTML = `
      <p class="text-danger small">Erro ao carregar Pokémon. Tente novamente.</p>
    `;
  }
}

// ── Seleção de Pokémon ────────────────────────────────────────
async function selectPokemon(nameOrId) {
  try {
    const pokemon = await fetchPokemonDetail(nameOrId);
    STATE.selectedPokemon = pokemon;
    renderPokemonDetail(pokemon);
    renderPokemonGrid(STATE.pokemonList, pokemon.id);
  } catch (error) {
    alert(error.message);
  }
}

// ── Chat ──────────────────────────────────────────────────────
async function sendMessage(question) {
  if (!STATE.selectedPokemon) return;
  if (!question.trim()) return;

  appendChatBubble(question, 'user');
  document.getElementById('chatInput').value = '';

  const loading = showChatLoading();

  try {
    const data = await sendChatMessage(STATE.selectedPokemon.name, question);
    removeChatBubble(loading);
    appendChatBubble(data.answer, 'ai');
  } catch (error) {
    removeChatBubble(loading);
    appendChatBubble('Erro ao consultar o Professor Carvalho. Tente novamente.', 'error');
  }
}

// ── Event Listeners ───────────────────────────────────────────
function setupEventListeners() {
  // Seleção de Pokémon no grid
  document.getElementById('pokemonGrid').addEventListener('click', (e) => {
    const card = e.target.closest('.pokemon-card');
    if (!card) return;
    selectPokemon(card.dataset.name);
  });

  // Paginação
  document.getElementById('nextBtn').addEventListener('click', () => {
    STATE.currentPage++;
    loadPokemonList();
  });

  document.getElementById('prevBtn').addEventListener('click', () => {
    if (STATE.currentPage > 1) {
      STATE.currentPage--;
      loadPokemonList();
    }
  });

  // Busca
  document.getElementById('searchBtn').addEventListener('click', () => {
    const query = document.getElementById('searchInput').value.trim().toLowerCase();
    if (query) selectPokemon(query);
  });

  document.getElementById('searchInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const query = e.target.value.trim().toLowerCase();
      if (query) selectPokemon(query);
    }
  });

  // Chat - enviar
  document.getElementById('chatSendBtn').addEventListener('click', () => {
    const question = document.getElementById('chatInput').value.trim();
    if (question) sendMessage(question);
  });

  document.getElementById('chatInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const question = e.target.value.trim();
      if (question) sendMessage(question);
    }
  });

  // Sugestões de perguntas
  document.querySelectorAll('.suggestion-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      sendMessage(btn.dataset.q);
    });
  });
}