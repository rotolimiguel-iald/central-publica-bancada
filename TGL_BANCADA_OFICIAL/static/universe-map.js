/* Educational navigation shares laboratories, never their scientific state. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const catalog = window.CosmosLessons;
  const model = window.CosmosTeaching;
  if (!catalog || !model || !Array.isArray(catalog.topics) || catalog.topics.length !== 8) {
    $('app-error').hidden = false;
    $('app-error').textContent = 'O conteúdo ou o modelo didático não foi carregado. Reabra a página; os laboratórios continuam acessíveis pelos links superiores.';
    return;
  }
  const topics = catalog.topics;
  const storageKey = 'tgl-universe-learning-v1';
  const components = [
    { key: 'baryons', label: 'Matéria bariônica', topic: 'baryons', color: '#7de0cf' },
    { key: 'darkMatter', label: 'Matéria escura', topic: 'dark-matter', color: '#78b7e8' },
    { key: 'darkEnergy', label: 'Energia escura · Λ', topic: 'dark-energy', color: '#a9a0ef' },
    { key: 'radiation', label: 'Radiação', topic: 'cmb', color: '#f2c48b' },
  ];
  const icons = ['⊙', '◌', '↗', '∿', '⤢', '⋈', '◎', '≋'];
  const presets = { baryons: 0, 'dark-matter': 10, 'dark-energy': 0, cmb: 1100, expansion: 1, structure: 10, bao: 1, 'gravitational-waves': 0 };
  const number = (value, digits = 3) => new Intl.NumberFormat('pt-BR', { maximumFractionDigits: digits }).format(value);
  let selected = topics[0].id, mode = 'free', read = new Set(), storageWorks = true;
  let parameters = model.defaultParameters(), z = 0, historySignature = null, labRequest = 0;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (saved && typeof saved === 'object') {
      if (topics.some(t => t.id === saved.selected)) selected = saved.selected;
      if (saved.mode === 'guided') mode = 'guided';
      if (Array.isArray(saved.read)) read = new Set(saved.read.filter(id => topics.some(t => t.id === id)));
    }
  } catch (_) { storageWorks = false; }
  const queryTopic = new URLSearchParams(location.search).get('topic');
  if (topics.some(t => t.id === queryTopic)) selected = queryTopic;
  const svgElement = (tag, attributes = {}) => {
    const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, String(value));
    return node;
  };
  const textNode = (tag, text, className) => {
    const node = document.createElement(tag); node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  function persist() {
    try { localStorage.setItem(storageKey, JSON.stringify({ selected, mode, read: [...read] })); }
    catch (_) { storageWorks = false; }
    $('progress-storage').textContent = storageWorks ? 'Seu percurso fica guardado neste navegador.' : 'Armazenamento local indisponível; o percurso vale apenas nesta visita.';
  }
  function sourceLinks(target, ids) {
    target.replaceChildren();
    for (const id of ids) {
      const source = catalog.sources.find(s => s.id === id);
      if (!source || !/^https:\/\//.test(source.url)) continue;
      const li = document.createElement('li'), link = textNode('a', source.title);
      link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer';
      li.append(link); target.append(li);
    }
  }
  function updateProgress() {
    $('reading-progress').textContent = `${read.size} de ${topics.length} temas marcados como lidos`;
    document.querySelectorAll('.topic-card').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.topic === selected));
      button.querySelector('.read-mark').textContent = read.has(button.dataset.topic) ? '✓' : '';
    });
    $('lesson-read').checked = read.has(selected);
    persist();
  }
  function selectTopic(id, focus = false) {
    const index = topics.findIndex(t => t.id === id);
    if (index < 0) return;
    selected = id;
    const topic = topics[index];
    for (const key of ['title', 'eyebrow', 'summary', 'question', 'observe', 'experiment', 'tgl', 'capability']) {
      $(`lesson-${key}`).textContent = topic[key];
    }
    const lab = $('lesson-lab');
    // In-page experiments use the existing button, retaining the active scenario.
    const inPageLab = topic.lab && new URL(topic.lab.url, location.href).pathname === '/explore';
    lab.hidden = !topic.lab || inPageLab;
    if (topic.lab && !inPageLab) { lab.href = topic.lab.url; lab.textContent = topic.lab.label + ' ↗'; }
    $('lesson-demo').textContent = id === 'cmb' ? 'Ver composição em z ≈ 1100' : 'Explorar neste diagrama';
    $('guided-position').textContent = `Etapa ${index + 1} de ${topics.length} · ${topic.group}`;
    $('previous-lesson').disabled = index === 0;
    $('next-lesson').disabled = index === topics.length - 1;
    sourceLinks($('lesson-sources'), topic.sourceIds);
    updateProgress();
    if (focus) $('lesson-title').focus({ preventScroll: true });
  }
  function setMode(next) {
    mode = next;
    $('mode-free').setAttribute('aria-pressed', String(mode === 'free'));
    $('mode-guided').setAttribute('aria-pressed', String(mode === 'guided'));
    $('guided-controls').hidden = mode !== 'guided';
    $('mode-description').textContent = mode === 'free' ? 'Comece pelo que desperta sua curiosidade.' : 'Da composição à observação, em oito etapas. Você pode sair do percurso a qualquer momento.';
    persist();
  }
  topics.forEach((topic, index) => {
    const button = textNode('button', '', 'topic-card'); button.dataset.topic = topic.id;
    const copy = document.createElement('span');
    copy.append(textNode('small', `${String(index + 1).padStart(2, '0')} / ${topic.group}`), textNode('strong', topic.title));
    const symbol = textNode('span', icons[index], 'topic-symbol'); symbol.setAttribute('aria-hidden', 'true');
    const mark = textNode('span', '', 'read-mark'); mark.setAttribute('aria-hidden', 'true');
    button.append(symbol, copy, mark); button.onclick = () => selectTopic(topic.id);
    $('topic-map').append(button);
  });
  $('mode-free').onclick = () => setMode('free');
  $('mode-guided').onclick = () => setMode('guided');
  $('previous-lesson').onclick = () => selectTopic(topics[Math.max(0, topics.findIndex(t => t.id === selected) - 1)].id, true);
  $('next-lesson').onclick = () => selectTopic(topics[Math.min(topics.length - 1, topics.findIndex(t => t.id === selected) + 1)].id, true);
  $('lesson-read').onchange = event => { if (event.target.checked) read.add(selected); else read.delete(selected); updateProgress(); };
  $('lesson-demo').onclick = () => { setRedshift(presets[selected]); $('experiment-title').scrollIntoView({ block: 'nearest', behavior: 'auto' }); };

  components.forEach(component => {
    const circle = svgElement('circle', { cx: 150, cy: 150, r: 113, fill: 'none', stroke: component.color, 'stroke-width': 28, id: 'ring-' + component.key });
    $('ring-segments').append(circle);
    const button = textNode('button', '', 'component-row'); button.style.setProperty('--color', component.color);
    button.append(textNode('span', component.label), textNode('strong', '—'));
    button.id = 'fraction-' + component.key;
    button.onclick = () => selectTopic(component.topic);
    $('component-legend').append(button);
  });
  function drawHistory() {
    const rows = model.history(parameters), w = 920, h = 190, left = 48, top = 16;
    $('history-grid').replaceChildren(); $('history-lines').replaceChildren();
    for (let f = 0; f <= 1.001; f += .25) {
      const y = top + h * (1 - f);
      $('history-grid').append(svgElement('line', { x1: left, x2: left + w, y1: y, y2: y, class: 'history-gridline' }));
      const label = svgElement('text', { x: left - 9, y: y + 4, 'text-anchor': 'end', class: 'history-label' }); label.textContent = number(f * 100, 0) + '%'; $('history-grid').append(label);
    }
    [0, 1, 2, 3, 4, 5].forEach(log => {
      const x = left + log / 5 * w;
      const label = svgElement('text', { x, y: 233, 'text-anchor': log === 5 ? 'end' : log === 0 ? 'start' : 'middle', class: 'history-label' }); label.textContent = log === 0 ? 'Hoje · z = 0' : 'z = ' + number(10 ** log - 1, 0); $('history-grid').append(label);
    });
    for (const c of components) {
      const points = rows.map(row => `${left + Math.log10(1 + row.z) / 5 * w},${top + h * (1 - row.fractions[c.key])}`);
      $('history-lines').append(svgElement('path', { d: 'M' + points.join(' L'), stroke: c.color, 'stroke-width': 2.5, fill: 'none' }));
    }
    historySignature = JSON.stringify(parameters);
    drawCursor();
  }
  function drawCursor() {
    const x = 48 + Math.log10(1 + z) / 5 * 920;
    $('history-cursor').setAttribute('x1', x); $('history-cursor').setAttribute('x2', x);
  }
  function displayResult() {
    try {
      const result = model.evaluate(z, parameters);
      $('model-error').hidden = true;
      const circumference = 2 * Math.PI * 113;
      let offset = 0;
      for (const component of components) {
        const fraction = result.fractions[component.key], length = fraction * circumference;
        const segment = $('ring-' + component.key);
        segment.setAttribute('stroke-dasharray', `${length} ${circumference - length}`);
        segment.setAttribute('stroke-dashoffset', -offset); segment.style.display = fraction === 0 ? 'none' : '';
        offset += length;
        const label = fraction > 0 && fraction * 100 < .0001 ? '< 0,0001%' : number(100 * fraction, fraction < .001 ? 4 : 2) + '%';
        $('fraction-' + component.key).querySelector('strong').textContent = label;
        $('fraction-' + component.key).setAttribute('aria-label', `${component.label}: ${label}. Abrir tema.`);
      }
      $('redshift-display').textContent = number(z, 3);
      $('scale-display').textContent = 'a = ' + number(result.a, result.a < .001 ? 7 : 5);
      $('lambda-value').textContent = number(result.omegaLambda, 6);
      $('ring-desc').textContent = `Cenário didático em z=${number(z)}. ` + components.map(c => `${c.label} ${$('fraction-' + c.key).querySelector('strong').textContent}`).join('; ');
      const matter = result.fractions.baryons + result.fractions.darkMatter;
      const dominant = matter >= result.fractions.radiation && matter >= result.fractions.darkEnergy ? 'A matéria, somando bárions e matéria escura, domina a densidade deste cenário.' : result.fractions.radiation > result.fractions.darkEnergy ? 'A radiação domina a densidade deste cenário.' : 'A constante cosmológica domina a densidade deste cenário.';
      $('era-description').textContent = dominant + (z > 900 && z < 1300 ? ' A época aproximada do CMB está destacada; este diagrama não calcula sua recombinação ou seus espectros.' : ' As frações se referem à época selecionada.');
      $('composition-ring').style.opacity = '1'; $('density-history').style.opacity = '1';
      document.querySelectorAll('[data-z]').forEach(button => button.setAttribute('aria-pressed', String(Math.abs(Number(button.dataset.z) - z) < .001)));
      if (historySignature !== JSON.stringify(parameters)) drawHistory();
      else drawCursor();
      return true;
    } catch (error) {
      $('model-error').hidden = false;
      $('model-error').textContent = 'Cenário não calculado. Use redshift entre 0 e 100.000 e frações não negativas cuja soma seja menor que 1. Preencha todos os campos. O último gráfico válido está esmaecido.';
      $('composition-ring').style.opacity = '.3'; $('density-history').style.opacity = '.3';
      return false;
    }
  }
  function setRedshift(value, syncNumber = true) {
    z = value;
    if (Number.isFinite(z) && z >= 0 && z <= 100000) $('epoch-slider').value = Math.log10(1 + z);
    if (syncNumber) $('epoch-number').value = String(z);
    displayResult();
  }
  $('epoch-slider').oninput = event => setRedshift(Math.pow(10, Number(event.target.value)) - 1);
  $('epoch-number').oninput = event => setRedshift(event.target.value === '' ? NaN : Number(event.target.value), false);
  document.querySelectorAll('[data-z]').forEach(button => button.onclick = () => setRedshift(Number(button.dataset.z)));
  const inputParams = () => ({ omegaB: $('density-b').value === '' ? NaN : Number($('density-b').value), omegaC: $('density-c').value === '' ? NaN : Number($('density-c').value), omegaR: $('density-r').value === '' ? NaN : Number($('density-r').value) });
  ['density-b', 'density-c', 'density-r'].forEach(id => $(id).oninput = () => { parameters = inputParams(); displayResult(); });
  $('reset-composition').onclick = () => {
    parameters = model.defaultParameters();
    $('density-b').value = parameters.omegaB; $('density-c').value = parameters.omegaC; $('density-r').value = parameters.omegaR;
    if (!Number.isFinite(z) || z < 0 || z > 100000) setRedshift(0);
    displayResult();
  };
  // The reference diagram does not change the V3 parameters or cached data.
  sourceLinks($('model-sources'), catalog.sources.map(s => s.id).filter(id => /model|flrw|planck|expansion/.test(id)));
  if (!$('model-sources').children.length) sourceLinks($('model-sources'), topics.find(t => t.id === 'expansion').sourceIds);
  async function refreshLabs() {
    const revision = ++labRequest;
    $('cosmology-availability').textContent = 'Consultando o laboratório…';
    try {
      const response = await fetch('/api/cosmology/status', { signal: AbortSignal.timeout(8000), cache: 'no-store' });
      const data = await response.json();
      if (revision !== labRequest) return;
      if (!response.ok || data.status !== 'ok') throw new Error('Fontes não confirmadas pelo executor');
      $('cosmology-availability').textContent = 'Disponível · fontes verificadas pelo executor local';
    } catch (error) {
      if (revision === labRequest) $('cosmology-availability').textContent = 'Disponibilidade não confirmada · abra o laboratório para diagnóstico';
    }
  }
  $('refresh-labs').onclick = refreshLabs;
  const regimes = [
    {
      id: 'acoustic', title: 'Universo jovem · acústica', tag: 'Prioridade D10', symbol: '◎',
      status: 'ÉPOCA DIDÁTICA + LABORATÓRIO BAO', topic: 'cmb', z: 1100,
      description: 'A rota acústica é a prioridade de avaliação conjunta definida para a bancada. O diagrama permite situar a época do CMB; o laboratório trabalha com as distâncias BAO já carregadas.',
      controls: 'Época no diagrama; H₀, matéria total, r_d e redshift no laboratório BAO.',
      effect: 'Comparar as distâncias V3 com β fixo e β zero. Mapas e espectros CMB ainda por integrar.',
      sensitivity: 'Disponível: vetor BAO e covariância. Poder de rejeição e significância global ainda não calculados.',
      url: '/cosmos', action: 'Abrir rota BAO', teaching: 'Situar a época do CMB',
    },
    {
      id: 'black-holes', title: 'Horizontes · ringdown', tag: 'Evento GW250114', symbol: '◉',
      status: 'DADOS DE DETECTORES DISPONÍVEIS', topic: 'gravitational-waves',
      description: 'Entre diretamente na janela pós-pico de GW250114 e compare os canais H1 e L1. O painel mostra o sinal observado e as curvas condicionais no mesmo contexto temporal.',
      controls: 'Janela após o pico, detector, massa, spin, redshift e hipótese de relógio.',
      effect: 'Amortecimento e diferença entre as curvas GR e TGL; o sinal de um detector não é uma imagem do horizonte.',
      sensitivity: 'Máscaras e tratamento de ruído disponíveis. Antena, posteriores e teste global ainda precisam completar a ligação.',
      url: 'http://127.0.0.1:18765/universe#event-panel', action: 'Abrir GW250114', teaching: 'Entender ondas gravitacionais',
    },
    {
      id: 'high-spin', title: 'Rotação elevada', tag: 'Cenário controlado', symbol: '↻',
      status: 'PREPARAÇÃO DE CENÁRIO · NÃO É AJUSTE', topic: 'gravitational-waves',
      description: 'Prepare um remanescente com spin 0,95 e compare sua escala de amortecimento. Os parâmetros servem para exploração e não são atribuídos ao evento observado.',
      controls: 'Massa da fonte 65 M☉, spin 0,95, z=0,1. Escolha explicitamente o relógio antes de calcular.',
      effect: 'Inspecionar Γτ_GR e a mudança fracionária de τ, que combinam a taxa prevista com a duração do modo.',
      sensitivity: 'Não estimada neste cenário. A magnitude prevista não é sinal/ruído nem sigma.',
      url: 'http://127.0.0.1:18765/universe?regime=high-spin#ringdown', action: 'Preparar spin elevado', teaching: 'Entender o sinal',
    },
    {
      id: 'high-frequency', title: 'Modos de maior frequência', tag: 'Cenário controlado', symbol: '≋',
      status: 'PREPARAÇÃO DE CENÁRIO · NÃO É AJUSTE', topic: 'gravitational-waves',
      description: 'Explore o modo 220 reduzindo a massa em relação ao cenário de referência, com spin e redshift mantidos. A taxa e o tempo disponível para agir devem ser lidos juntos.',
      controls: 'Massa da fonte 20 M☉, spin 0,7, z=0,1. Escolha explicitamente o relógio.',
      effect: 'Comparar frequência, Γ e Γτ_GR no executor existente. Não extrapolar uma taxa maior para melhor detecção.',
      sensitivity: 'Depende da resposta do detector e do ruído nessa faixa; ainda não calculada pelo cenário.',
      url: 'http://127.0.0.1:18765/universe?regime=high-frequency#ringdown', action: 'Preparar maior frequência', teaching: 'Entender o sinal',
    },
    {
      id: 'voids', title: 'Vazios · contrastes de densidade', tag: 'Rota a integrar', symbol: '◌',
      status: 'TEMA DISPONÍVEL · EXECUTOR AINDA NÃO LIGADO', topic: 'structure',
      description: 'A busca também inclui ambientes de baixa densidade e o contraste entre vazios e estruturas. Eles precisam ser examinados por seus perfis observados, não pelo diagrama homogêneo de composição.',
      controls: 'Perfis de vazios, seleção de amostra, lentes e covariâncias, quando ligados ao painel.',
      effect: 'Retomar o teste do piso dos vazios e suas hipóteses no executor específico do acervo.',
      sensitivity: 'Sem medida nova nesta interface. Não há mapa local de vazios carregado aqui.',
      teaching: 'Entender a formação de estruturas',
    },
    {
      id: 'particles', title: 'Partículas · coerência', tag: 'Rota a integrar', symbol: '⋈',
      status: 'DADOS E EXECUTORES AINDA POR INTEGRAR',
      description: 'Organizar a passagem às escalas de partículas exige a energia, o tempo de propagação e o observável próprios de cada experimento.',
      controls: 'Energia, distância, coerência e resposta instrumental de cada banco de partículas.',
      effect: 'Comparar a previsão específica com a referência do mesmo experimento; o cenário de buracos negros não fornece essa previsão.',
      sensitivity: 'Ainda não calculada neste painel. A busca deve respeitar limiares e sistemáticas de cada experimento.',
    },
  ];
  let activeRegime = regimes[0];
  function selectRegime(regime) {
    activeRegime = regime;
    for (const key of ['status', 'description', 'controls', 'effect', 'sensitivity']) $('extreme-' + key).textContent = regime[key];
    $('extreme-detail-title').textContent = regime.title;
    $('extreme-link').hidden = !regime.url;
    if (regime.url) { $('extreme-link').href = regime.url; $('extreme-link').textContent = regime.action + ' ↗'; }
    $('extreme-teach').hidden = !regime.topic;
    if (regime.topic) $('extreme-teach').textContent = regime.teaching;
    document.querySelectorAll('.extreme-card').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.regime === regime.id)));
  }
  for (const regime of regimes) {
    const button = textNode('button', '', 'extreme-card'); button.dataset.regime = regime.id;
    const symbol = textNode('span', regime.symbol, 'regime-symbol'); symbol.setAttribute('aria-hidden', 'true');
    const copy = textNode('span', '', 'regime-copy'); copy.append(textNode('small', regime.tag), textNode('strong', regime.title));
    button.append(symbol, copy); button.onclick = () => selectRegime(regime); $('extreme-map').append(button);
  }
  $('extreme-teach').onclick = () => {
    if (!activeRegime.topic) return;
    selectTopic(activeRegime.topic);
    if (Number.isFinite(activeRegime.z)) setRedshift(activeRegime.z);
    $('lesson-title').scrollIntoView({ block: 'start', behavior: 'auto' });
  };
  selectRegime(regimes.find(regime => regime.id === new URLSearchParams(location.search).get('regime')) || regimes[0]);
  setMode(mode); selectTopic(selected); displayResult(); refreshLabs();
})();
