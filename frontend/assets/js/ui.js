// ── Helpers ──────────────────────────────────────────────────

function getStatColor(value) {
  if (value >= 100) return '#7AC74C';
  if (value >= 60)  return '#F7D02C';
  return '#E3350D';
}

function renderSkeletons() {
  const grid = document.getElementById('pokemonGrid');
  grid.innerHTML = Array(12).fill(0).map(() => `
    <div class="skeleton"></div>
  `).join('');
}

// ── Lista ─────────────────────────────────────────────────────

function renderPokemonGrid(pokemonList, selectedId = null) {
  const grid = document.getElementById('pokemonGrid');
  grid.innerHTML = pokemonList.map(pokemon => `
    <div
      class="pokemon-card ${pokemon.id === selectedId ? 'active' : ''}"
      data-id="${pokemon.id}"
      data-name="${pokemon.name}"
    >
      <img
        src="${pokemon.image || 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png'}"
        alt="${pokemon.name}"
        loading="lazy"
      />
      <div class="card-id">#${String(pokemon.id).padStart(3, '0')}</div>
      <div class="card-name">${pokemon.name}</div>
      <div class="card-types">
        ${pokemon.types.map(t => `<span class="type-badge type-${t.name}">${t.name}</span>`).join('')}
      </div>
    </div>
  `).join('');
}

// ── Detalhes ──────────────────────────────────────────────────

function renderPokemonDetail(pokemon) {
  document.getElementById('emptyState').classList.add('d-none');
  document.getElementById('pokemonDetail').classList.remove('d-none');

  document.getElementById('detailId').textContent = `#${String(pokemon.id).padStart(3, '0')}`;
  document.getElementById('detailName').textContent = pokemon.name;
  document.getElementById('detailHeight').textContent = `📏 ${pokemon.height_meters}m`;
  document.getElementById('detailWeight').textContent = `⚖️ ${pokemon.weight_kg}kg`;
  document.getElementById('detailXp').textContent = `⚡ XP ${pokemon.base_experience ?? '?'}`;

  const imgEl = document.getElementById('detailImage');
  imgEl.src = pokemon.image || '';
  imgEl.alt = pokemon.name;

  const shinyEl = document.getElementById('detailImageShiny');
  shinyEl.src = pokemon.image_shiny || '';
  shinyEl.alt = `${pokemon.name} shiny`;

  // Tipos
  document.getElementById('detailTypes').innerHTML = pokemon.types
    .map(t => `<span class="type-badge type-${t.name}">${t.name}</span>`)
    .join('');

  // Stats
  document.getElementById('statsContainer').innerHTML = pokemon.stats.map(stat => `
    <div class="stat-row">
      <span class="stat-name">${stat.name}</span>
      <span class="stat-value">${stat.base_stat}</span>
      <div class="stat-bar">
        <div
          class="stat-bar__fill"
          style="width: ${Math.min((stat.base_stat / 255) * 100, 100)}%; background: ${getStatColor(stat.base_stat)};"
        ></div>
      </div>
    </div>
  `).join('');

  // Habilidades
  document.getElementById('abilitiesContainer').innerHTML = pokemon.abilities.map(a => `
    <span class="badge ${a.is_hidden ? 'border border-warning text-warning' : 'bg-secondary'} text-capitalize">
      ${a.name}${a.is_hidden ? ' ★' : ''}
    </span>
  `).join('');

  // Limpa o chat ao trocar de Pokémon
  document.getElementById('chatMessages').innerHTML = '';
}

// ── Chat ────────────────────────────────────────
function appendChatBubble(text, type = 'ai') {
  const messages = document.getElementById('chatMessages');
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble chat-bubble--${type}`;

  if (type === 'ai') {
    bubble.innerHTML = marked.parse(text);
  } else {
    bubble.textContent = text;
  }

  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}

function showChatLoading() {
  return appendChatBubble('Professor Carvalho está pensando...', 'loading');
}

function removeChatBubble(bubble) {
  bubble?.remove();
}

// ── Paginação ─────────────────────────────────────────────────

function updatePagination(page, hasPrev, hasNext) {
  document.getElementById('pageInfo').textContent = `Página ${page}`;
  document.getElementById('prevBtn').disabled = !hasPrev;
  document.getElementById('nextBtn').disabled = !hasNext;
}