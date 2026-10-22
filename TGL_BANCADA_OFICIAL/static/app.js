const $ = (id) => document.getElementById(id);
const views = [...document.querySelectorAll('.view')];
const tabs = [...document.querySelectorAll('.tab')];

function show(view) {
  views.forEach(node => node.classList.toggle('active', node.id === view));
  tabs.forEach(node => node.classList.toggle('active', node.dataset.view === view));
  window.scrollTo({top: 0, behavior: 'smooth'});
}
tabs.forEach(button => button.addEventListener('click', () => show(button.dataset.view)));

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

function element(tag, className, value) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (value !== undefined) node.textContent = value;
  return node;
}

function renderOverview(data) {
  const metrics = $('metrics'); metrics.replaceChildren();
  const items = [
    [data.module_count.toLocaleString('pt-BR'), 'módulos no índice v368'],
    [data.declaration_count.toLocaleString('pt-BR'), 'declarações catalogadas'],
    [data.route_count.toLocaleString('pt-BR'), 'rotas com localizador'],
    ['0', 'promoções automáticas do gate']
  ];
  items.forEach(([number, label]) => {
    const box = element('div', 'metric');
    box.append(element('b', '', number), element('span', '', label)); metrics.append(box);
  });
  const sources = $('sources'); sources.replaceChildren();
  data.sources.forEach(source => {
    const box = element('div', 'source');
    box.append(element('strong', '', source.label),
               element('small', '', `${source.status} · ${source.path}`),
               element('small', '', source.sha256 ? `SHA-256 ${source.sha256}` : 'arquivo indisponível'));
    sources.append(box);
  });
}

let lastInquiryText = '';

function inquiryItem(container, title, detail, actionLabel, action) {
  const row = element('div', 'item');
  row.append(element('strong', '', title), element('small', '', detail));
  if (action) {
    const button = element('button', '', actionLabel);
    button.addEventListener('click', action);
    row.append(button);
  }
  container.append(row);
}

function renderInquiry(id, result, events = []) {
  const root = $('inquiry-output'); root.replaceChildren();
  const summary = element('div', 'inquiry-summary');
  summary.append(element('b', '', `INVESTIGAÇÃO #${id} · ${result.status}`),
                 element('p', '', result.question),
                 element('small', '', `${result.analysis_stage || 'EXPLORATORY_NOT_PREREGISTERED'} · índice ${result.index_release} · SHA-256 ${result.source_sha256}`));
  root.append(summary);
  events.forEach(event => {
    const note = element('div', 'notice', `${event.event_type}: ${event.note}`);
    if (event.related_inquiry_id) note.append(element('small', '', `Registro relacionado: #${event.related_inquiry_id}`));
    root.append(note);
  });
  const hypotheses = element('div', 'inquiry-hypotheses');
  [
    ['Hipótese principal', result.hypothesis],
    ['Contraprova', result.falsifier],
    ['Explicação rival', result.alternative],
    ['Efeito instrumental', result.instrumental],
    ['Cálculo ou medição discriminante', result.discriminator]
  ].forEach(([label, value]) => {
    const card = element('div', 'inquiry-hypothesis');
    card.append(element('small', '', label), element('p', '', value || 'Ainda não formulado.'));
    hypotheses.append(card);
  });
  root.append(hypotheses);
  const grid = element('div', 'inquiry-grid');
  const formal = element('section', 'inquiry-card');
  formal.append(element('h3', '', `Torre formal · ${result.formal_total} correspondências`));
  if (!result.formal.length) formal.append(element('p', 'inquiry-empty', 'Nenhuma declaração localizada pelos termos.'));
  result.formal.forEach(item => inquiryItem(formal, item.module,
    `${item.path || 'caminho indisponível'} · ${item.status}`,
    'Abrir na torre', () => { $('relation-search').value = item.module; show('tower'); searchRelations(); }));
  const data = element('section', 'inquiry-card');
  data.append(element('h3', '', 'Dados locais'));
  if (!result.datasets.length) data.append(element('p', 'inquiry-empty', 'Nenhum catálogo associado por termo.'));
  result.datasets.forEach(item => inquiryItem(data, `${item.label} · ${item.count} arquivos`,
    `${item.status} · ${item.root}`, 'Ver catálogo', () => show('data')));
  const protocols = element('section', 'inquiry-card');
  protocols.append(element('h3', '', `Protocolos · ${result.protocol_total} correspondências`));
  if (!result.protocols.length) protocols.append(element('p', 'inquiry-empty', 'Nenhum protocolo associado por termo.'));
  result.protocols.forEach(item => inquiryItem(protocols, `${item.target} · ${item.family}`,
    `${item.summary} · ${item.replay_status}`, 'Ver experimentos', () => show('experiment')));
  grid.append(formal, data, protocols); root.append(grid);
  const note = element('div', 'notice', result.method);
  if (result.open_items.length) note.append(element('p', '', `Pendências: ${result.open_items.join('; ')}.`));
  root.append(note);
  lastInquiryText = `Investigação ${id}. ${result.question}. Foram localizadas ${result.formal_total} relações formais, ${result.datasets.length} grupos de dados e ${result.protocol_total} protocolos. ${result.open_items.join('. ')}. ${result.method}`;
  $('read-inquiry').disabled = !('speechSynthesis' in window);
}

async function loadInquiries() {
  const root = $('inquiry-history');
  try {
    const records = await api('/api/inquiries'); root.replaceChildren();
    if (!records.length) { root.textContent = 'Nenhuma investigação registrada.'; return; }
    records.forEach(record => {
      const row = element('div', 'inquiry-history-row');
      const button = element('button', '', `#${record.id} · ${record.question}`);
      button.addEventListener('click', () => { renderInquiry(record.id, record.result, record.events || []); show('research'); });
      const labels = (record.events || []).map(event => event.event_type).join(', ');
      row.append(button, element('small', '', `${record.created_utc} · ${record.status}${labels ? ' · ' + labels : ''}`));
      root.append(row);
    });
  } catch (error) { root.textContent = `Histórico indisponível: ${error.message}`; }
}

$('run-inquiry').addEventListener('click', async () => {
  const button = $('run-inquiry');
  if (button.disabled) return;
  button.disabled = true;
  $('research-status').textContent = 'Mapeando fontes e registrando a investigação…';
  try {
    const payload = {question: $('inquiry-question').value,
      hypothesis: $('inquiry-hypothesis').value, falsifier: $('inquiry-falsifier').value,
      alternative: $('inquiry-alternative').value, instrumental: $('inquiry-instrumental').value,
      discriminator: $('inquiry-discriminator').value};
    const record = await api('/api/inquiry', {method: 'POST',
      headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
    renderInquiry(record.inquiry_id, record.result);
    $('research-status').textContent = `Investigação #${record.inquiry_id} registrada. Fontes e lacunas aparecem abaixo.`;
    await loadInquiries();
  } catch (error) { $('research-status').textContent = `Investigação recusada: ${error.message}`; }
  finally { button.disabled = false; }
});

$('read-inquiry').addEventListener('click', () => {
  if (!lastInquiryText || !('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(lastInquiryText);
  utterance.lang = 'pt-BR'; utterance.rate = 1;
  window.speechSynthesis.speak(utterance);
});

async function searchRelations() {
  const query = $('relation-search').value.trim();
  const root = $('relations'); root.textContent = 'Buscando na torre…';
  try {
    const data = await api(`/api/relations?q=${encodeURIComponent(query)}&limit=60`);
    root.replaceChildren();
    if (!data.matches.length) { root.textContent = 'Nenhuma declaração localizada neste snapshot.'; return; }
    data.matches.forEach(item => {
      const card = element('article', 'relation');
      card.append(element('h3', '', item.module), element('small', '', `${item.path} · ${item.declaration_count} declarações`));
      const tags = element('div', 'tags');
      (item.declarations.length ? item.declarations : [{kind: 'module', short_name: 'módulo'}]).slice(0, 10).forEach(decl =>
        tags.append(element('span', 'tag', `${decl.kind} ${decl.short_name}${decl.line ? ':' + decl.line : ''}`)));
      card.append(tags);
      if (item.imports.length) card.append(element('small', '', `Importa: ${item.imports.join(', ')}`));
      root.append(card);
    });
    if (data.limited) root.append(element('p', '', 'Busca limitada a 60 módulos. Refine o termo para localizar mais.'));
  } catch (error) { root.textContent = `Falha visível: ${error.message}`; }
}
$('search-button').addEventListener('click', searchRelations);
$('relation-search').addEventListener('keydown', event => { if (event.key === 'Enter') searchRelations(); });

async function loadRoutes() {
  try {
    const routes = await api('/api/routes');
    const strip = $('route-strip'); strip.replaceChildren();
    routes.slice(0, 8).forEach(route => strip.append(element('span', '', route.flag || route.term || 'rota')));
  } catch (error) { $('route-strip').textContent = `Rotas indisponíveis: ${error.message}`; }
}

async function loadData() {
  const root = $('datasets'); root.textContent = 'Lendo o catálogo local…';
  try {
    const groups = await api('/api/data'); root.replaceChildren();
    groups.forEach(group => {
      const box = element('article', 'data-group');
      box.append(element('h3', '', `${group.label} · ${group.count} arquivos`),
                 element('span', 'status', group.status), element('p', '', group.root));
      const details = element('details'); details.append(element('summary', '', 'Ver arquivos e recibos'));
      group.files.forEach(file => {
        const row = element('div', 'file');
        row.append(element('span', '', file.name),
                   element('em', '', `${(file.bytes / 1048576).toFixed(2)} MiB${file.receipt ? ' · recibo presente' : ''}`));
        details.append(row);
      });
      if (group.truncated) details.append(element('p', '', 'Lista abreviada aos primeiros 100 arquivos.'));
      box.append(details); root.append(box);
    });
  } catch (error) { root.textContent = `Falha visível: ${error.message}`; }
}

let labCatalog = [];
const gib = bytes => `${(bytes / 1024 ** 3).toLocaleString('pt-BR', {maximumFractionDigits: 2})} GiB`;

function filterLab() {
  const term = $('lab-search').value.trim().toLocaleLowerCase('pt-BR');
  const selector = $('lab-file'), current = selector.value;
  selector.replaceChildren(new Option('Escolha uma fonte', ''));
  const matches = labCatalog.filter(item => `${item.name} ${item.path} ${item.group}`.toLocaleLowerCase('pt-BR').includes(term));
  matches.slice(0, 300).forEach(item => selector.append(new Option(`${item.name} · ${gib(item.bytes)} · ${item.group}`, item.id)));
  if (matches.some(item => item.id === current)) selector.value = current;
  $('lab-catalog-summary').textContent = `${labCatalog.length.toLocaleString('pt-BR')} arquivos indexados · ${gib(labCatalog.reduce((n, item) => n + item.bytes, 0))} em disco · ${matches.length} correspondem à busca${matches.length > 300 ? ' (lista limitada a 300; refine a busca)' : ''}. Arquivos não validados como evidência física.${labCoverage ? ` Rotas de leitor: ${labCoverage.reader_routes.READY.files} disponíveis para tentativa, ${labCoverage.reader_routes.PENDING.files} pendentes; esquema individual e independência estatística não estabelecidos.` : ''}`;
}

let labCoverage = null;
async function loadLab() {
  try {
    const [memory, inventory, gpu] = await Promise.all([api('/api/lab/memory'), api('/api/lab/catalog'), api('/api/lab/gpu')]);
    renderMemory(memory);
    renderGpuMemory(gpu);
    labCatalog = inventory.items;
    filterLab();
    try { labCoverage = await api('/api/lab/coverage'); filterLab(); }
    catch (coverageError) { $('lab-catalog-summary').textContent += ` Cobertura indisponível: ${coverageError.message}.`; }
    const first = labCatalog.find(item => item.name === 'desi_gaussian_bao_ALL_GCcomb_mean.txt') ||
                  labCatalog.find(item => item.group.includes('canônica') && item.name.includes('DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits')) ||
                  labCatalog.find(item => item.name.includes('DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits'));
    if (first) { $('lab-search').value = first.name; filterLab(); $('lab-file').value = first.id; await labDescribe(); await labPlot(); }
  } catch (error) { $('lab-catalog-summary').textContent = `Catálogo indisponível: ${error.message}`; }
}

function renderMemory(memory) {
  $('lab-memory').textContent = `RAM em ${new Date().toLocaleTimeString('pt-BR')}: ${gib(memory.total_bytes)} total · ${gib(memory.available_bytes)} livre · ${gib(memory.interactive_budget_bytes)} de orçamento inicial para análise. O navegador recebe no máximo ${memory.browser_point_limit} pontos por gráfico.`;
}

function renderGpuMemory(gpu) {
  $('lab-gpu-memory').textContent = gpu.devices.length
    ? `GPU em ${new Date().toLocaleTimeString('pt-BR')}: ${gpu.devices.map(d => `${d.name} · ${d.free_mib.toLocaleString('pt-BR')} / ${d.total_mib.toLocaleString('pt-BR')} MiB livres/total · ${d.utilization_percent}% de uso`).join(' · ')}. Telemetria não reserva memória.`
    : 'Telemetria GPU indisponível; capacidade não presumida.';
}

setInterval(async () => {
  if (document.hidden) return;
  try { const [memory, gpu] = await Promise.all([api('/api/lab/memory'), api('/api/lab/gpu')]); renderMemory(memory); renderGpuMemory(gpu); }
  catch (error) { $('lab-memory').textContent = `Memória indisponível agora: ${error.message}`; }
}, 15000);

async function loadCanonicalForm() {
  const root = $('lab-canonical');
  try {
    const info = await api('/api/lab/canonical');
    root.replaceChildren();
    root.append(element('p', '', `Fonte: ${info.form.path} · SHA-256 ${info.form.sha256}`),
                element('p', '', `Programa: ${info.program.path} · SHA-256 ${info.program.sha256}`),
                element('small', '', `${info.section_count} seções documentadas · ${info.status}`));
    if (info.bao_model) root.append(element('p', '', `Rota BAO D9 já implementada: ${info.bao_model.path} · ${info.bao_model.status}${info.bao_model.sha256 ? ' · SHA-256 ' + info.bao_model.sha256 : ''}`));
    if (info.chain_excerpt) root.append(element('pre', 'lab-formula', info.chain_excerpt));
    root.append(element('p', '', `Seções finais: ${info.latest_sections.join(' · ')}`));
  } catch (error) { root.textContent = `Forma canônica indisponível: ${error.message}`; }
}

async function loadBaoReport() {
  const root = $('lab-bao-report');
  try {
    const record = await api('/api/lab/bao-report'); root.replaceChildren();
    root.append(element('p', 'report-scope', `Relatório ${record.reported_timestamp_utc} · ${record.observations} medidas · ${record.degrees_of_freedom} graus de liberdade · ${record.status}`));
    const grid = element('div', 'report-grid');
    for (const [name, model] of [['ΛCDM', record.lcdm], ['TGL', record.tgl]]) {
      const card = element('div', 'report-card');
      card.append(element('small', '', name), element('strong', '', `χ² = ${model.chi2.toLocaleString('pt-BR', {maximumFractionDigits: 6})}`),
                  element('span', '', `Ωm = ${model.Om0.toPrecision(6)} · rd = ${model.rd_Mpc.toPrecision(7)} Mpc`));
      grid.append(card);
    }
    root.append(grid, element('div', 'report-delta', `Δχ²(TGL − ΛCDM) = ${record.delta_chi2_tgl_minus_lcdm.toExponential(6)} · sem conversão para σ`),
                element('p', 'report-note', record.scope),
                element('small', 'report-hash', `Relatório: ${record.report.path} · SHA-256 ${record.report.sha256}`),
                element('small', 'report-hash', `Script D9 atual: ${record.model_source_now.path} · SHA-256 ${record.model_source_now.sha256}`));
  } catch (error) { root.textContent = `Artefato D9 indisponível: ${error.message}`; }
}

async function labDescribe() {
  const id = $('lab-file').value;
  chart.data = null; chart.full = chart.view = null; chart.hidden.clear();
  chartCanvas.getContext('2d').clearRect(0, 0, chartCanvas.width, chartCanvas.height);
  if (gpuState.gl && !gpuState.lost) gpuScatter([]);
  $('lab-chart-reset').disabled = true; $('lab-chart-export').disabled = true;
  $('lab-chart-note').textContent = 'Nenhuma amostra desta fonte foi carregada ainda.';
  $('lab-chart-readout').textContent = 'Escolha dois eixos e visualize a amostra da fonte selecionada.';
  renderCovariance({});
  $('lab-treatment').textContent = 'Lendo o contrato de tratamento desta fonte…';
  for (const select of [$('lab-x'), $('lab-y')]) select.replaceChildren(new Option('Escolha uma coluna', ''));
  if (!id) { $('lab-status').textContent = 'Selecione um arquivo.'; return; }
  const item = labCatalog.find(entry => entry.id === id);
  try {
    const record = await api(`/api/lab/treatment?id=${encodeURIComponent(id)}`);
    const t = record.treatment, stats = record.statistics;
    $('lab-treatment').textContent = `Tratamento ${record.schema}: ${t.status} · ${record.source.format} · ${record.source.bytes.toLocaleString('pt-BR')} bytes · ${t.columns.length} colunas · unidades ${t.columns.map(c => `${c.name}:${c.unit}`).slice(0, 8).join(', ') || 'não lidas'}${t.columns.length > 8 ? '…' : ''} · covariância ${stats.covariance} · independência ${stats.independence} · impressão parcial ${record.source.edge_fingerprint.sha256.slice(0, 16)}… (${record.source.edge_fingerprint.method}; não é SHA integral). ${t.quality.join('; ')}`;
  } catch (error) { $('lab-treatment').textContent = `Tratamento recusado: ${error.message}`; }
  if (!item.interactive) { $('lab-status').textContent = `Arquivo ${item.format} indexado; leitor de colunas ainda não conectado. O original permanece intacto.`; return; }
  $('lab-status').textContent = 'Lendo apenas o cabeçalho…';
  try {
    const data = await api(`/api/lab/describe?id=${encodeURIComponent(id)}`);
    data.columns.forEach(column => {
      for (const select of [$('lab-x'), $('lab-y')]) select.append(new Option(`${column.name}${column.unit ? ' [' + column.unit + ']' : ''}`, column.name));
    });
    if (data.columns.length >= 2) { $('lab-x').value = data.columns[0].name; $('lab-y').value = data.columns[1].name; }
    $('lab-status').textContent = `${data.format} · ${data.rows === null ? 'linhas contadas na leitura' : (data.format === 'HDF5_NUMERIC' ? 'até ' : '') + data.rows.toLocaleString('pt-BR') + ' linhas'} · ${data.columns.length} colunas escalares numéricas · ${gib(data.bytes)}. Escolha os eixos.`;
  } catch (error) { $('lab-status').textContent = `Leitura recusada: ${error.message}`; }
}

const chart = {data: null, full: null, view: null, hidden: new Set(), drag: null};
const chartColors = {DV_over_rs: '#ffca86', DM_over_rs: '#66e3c7', DH_over_rs: '#85aaff'};
const chartPad = 62;
const chartCanvas = $('lab-chart');
const gpuCanvas = $('lab-gpu-chart');
const gpuState = {gl: null, program: null, buffer: null, initialized: false, lost: false, renderer: ''};

function gpuStatus(message) { $('lab-renderer-status').textContent = message; }

function compileShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source); gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const reason = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader); throw new Error(reason || 'Falha de shader WebGL2');
  }
  return shader;
}

function initGpu() {
  if (gpuState.initialized) return Boolean(gpuState.gl && !gpuState.lost);
  gpuState.initialized = true;
  try {
    const gl = gpuCanvas.getContext('webgl2', {alpha: true, antialias: false, preserveDrawingBuffer: false});
    if (!gl) throw new Error('WebGL2 indisponível');
    const vs = compileShader(gl, gl.VERTEX_SHADER, `#version 300 es
      in vec2 position; in vec3 color; in float size;
      out vec3 vColor;
      void main(){gl_Position=vec4(position,0.0,1.0);gl_PointSize=size;vColor=color;}`);
    const fs = compileShader(gl, gl.FRAGMENT_SHADER, `#version 300 es
      precision mediump float; in vec3 vColor; out vec4 outColor;
      void main(){vec2 p=gl_PointCoord*2.0-1.0;float r=dot(p,p);if(r>1.0)discard;outColor=vec4(vColor,1.0);}`);
    const program = gl.createProgram(); gl.attachShader(program, vs); gl.attachShader(program, fs);
    gl.linkProgram(program); gl.deleteShader(vs); gl.deleteShader(fs);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
    gpuState.gl = gl; gpuState.program = program; gpuState.buffer = gl.createBuffer();
    const ext = gl.getExtension('WEBGL_debug_renderer_info');
    gpuState.renderer = ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)) : 'adaptador não divulgado pelo navegador';
    gpuStatus(`WebGL2 ativo · ${gpuState.renderer} · pontos na GPU, eixos no Canvas2D.`);
    return true;
  } catch (error) {
    gpuState.gl = null; gpuCanvas.style.visibility = 'hidden';
    gpuStatus(`Canvas2D de reserva · ${error.message}`);
    return false;
  }
}

gpuCanvas.addEventListener('webglcontextlost', event => {
  event.preventDefault(); gpuState.lost = true; gpuState.gl = null; gpuState.initialized = false;
  gpuCanvas.style.visibility = 'hidden'; gpuStatus('Contexto WebGL2 perdido · Canvas2D ativo');
  if (chart.data?.points.length) renderChart();
});
gpuCanvas.addEventListener('webglcontextrestored', () => {
  gpuState.lost = false; gpuState.initialized = false;
  if (chart.data?.points.length) renderChart();
});

function useGpu() {
  if (!$('lab-gpu-toggle').checked || gpuState.lost) { gpuCanvas.style.visibility = 'hidden'; return false; }
  const ready = initGpu(); gpuCanvas.style.visibility = ready ? 'visible' : 'hidden'; return ready;
}

function gpuScatter(vertices) {
  const gl = gpuState.gl;
  if (!gl || gpuState.lost) return;
  gl.viewport(0, 0, gpuCanvas.width, gpuCanvas.height);
  gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
  if (!vertices.length) return;
  gl.useProgram(gpuState.program);
  gl.bindBuffer(gl.ARRAY_BUFFER, gpuState.buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.DYNAMIC_DRAW);
  for (const [name, count, offset] of [['position', 2, 0], ['color', 3, 2], ['size', 1, 5]]) {
    const location = gl.getAttribLocation(gpuState.program, name);
    gl.enableVertexAttribArray(location);
    gl.vertexAttribPointer(location, count, gl.FLOAT, false, 24, offset * 4);
  }
  gl.drawArrays(gl.POINTS, 0, vertices.length / 6);
}

$('lab-gpu-toggle').addEventListener('change', () => {
  if (!$('lab-gpu-toggle').checked) gpuStatus('Canvas2D selecionado; GPU pausada para este gráfico.');
  if (chart.data?.points.length) renderChart();
});

function chartPosition(event) {
  const rect = chartCanvas.getBoundingClientRect();
  return {x: (event.clientX - rect.left) * chartCanvas.width / rect.width,
          y: (event.clientY - rect.top) * chartCanvas.height / rect.height};
}

function chartMaps() {
  const {xmin, xmax, ymin, ymax} = chart.view;
  const w = chartCanvas.width, h = chartCanvas.height, pad = chartPad;
  return {px: x => pad + (x - xmin) / (xmax - xmin) * (w - 2 * pad),
          py: y => h - pad - (y - ymin) / (ymax - ymin) * (h - 2 * pad),
          ix: x => xmin + (x - pad) / (w - 2 * pad) * (xmax - xmin),
          iy: y => ymin + (h - pad - y) / (h - 2 * pad) * (ymax - ymin)};
}

function visibleChartPoint(index) {
  const observation = chart.data.observations?.[index];
  return !observation || !chart.hidden.has(observation.quantity);
}

function renderChart() {
  if (!chart.data?.points.length) return;
  const ctx = chartCanvas.getContext('2d');
  const w = chartCanvas.width, h = chartCanvas.height, pad = chartPad;
  const {px, py} = chartMaps();
  const gpu = useGpu(), vertices = [];
  ctx.fillStyle = '#08151c'; ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = '#294a56'; ctx.lineWidth = 1;
  for (let k = 0; k <= 5; k++) {
    const x = pad + k * (w - 2 * pad) / 5, y = pad + k * (h - 2 * pad) / 5;
    ctx.beginPath(); ctx.moveTo(x, pad); ctx.lineTo(x, h - pad); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pad, y); ctx.lineTo(w - pad, y); ctx.stroke();
    ctx.fillStyle = '#7ca2aa'; ctx.font = '12px Segoe UI, sans-serif';
    ctx.fillText((chart.view.xmin + k * (chart.view.xmax - chart.view.xmin) / 5).toPrecision(3), x - 16, h - 39);
    ctx.fillText((chart.view.ymax - k * (chart.view.ymax - chart.view.ymin) / 5).toPrecision(3), 5, y + 3);
  }
  ctx.save(); ctx.beginPath(); ctx.rect(pad, pad, w - 2 * pad, h - 2 * pad); ctx.clip();
  let shown = 0;
  chart.data.points.forEach(([x, y], i) => {
    if (!visibleChartPoint(i)) return;
    const observation = chart.data.observations?.[i];
    const sx = px(x), sy = py(y);
    if (sx < pad - 10 || sx > w - pad + 10 || sy < pad - 10 || sy > h - pad + 10) return;
    shown++;
    ctx.fillStyle = observation ? chartColors[observation.quantity] || '#e6edf0' : 'rgba(102, 227, 199, 0.7)';
    if (observation && chart.data.y === 'value') {
      ctx.strokeStyle = ctx.fillStyle; ctx.beginPath();
      ctx.moveTo(sx, py(y - observation.sigma)); ctx.lineTo(sx, py(y + observation.sigma)); ctx.stroke();
    }
    if (gpu) {
      const hex = observation ? chartColors[observation.quantity] || '#e6edf0' : '#66e3c7';
      vertices.push(2 * sx / w - 1, 1 - 2 * sy / h,
                    parseInt(hex.slice(1, 3), 16) / 255, parseInt(hex.slice(3, 5), 16) / 255,
                    parseInt(hex.slice(5, 7), 16) / 255, observation ? 12 : 6);
    } else {
      ctx.beginPath(); ctx.arc(sx, sy, observation ? 6 : 3, 0, Math.PI * 2); ctx.fill();
    }
  });
  ctx.restore();
  if (gpu) gpuScatter(vertices);
  ctx.fillStyle = '#e2f5f2'; ctx.font = '15px Segoe UI, sans-serif';
  ctx.fillText(`${chart.data.y} ↑`, pad, 28);
  ctx.fillText(`${chart.data.x} →`, w - pad - 150, h - 12);
  $('lab-chart-readout').textContent = `${shown.toLocaleString('pt-BR')} pontos visíveis · X [${chart.view.xmin.toPrecision(5)}, ${chart.view.xmax.toPrecision(5)}] · Y [${chart.view.ymin.toPrecision(5)}, ${chart.view.ymax.toPrecision(5)}] · roda: ampliar · arrastar: mover · duplo clique: recentrar.`;
}

function drawScatter(data) {
  chart.data = data; chart.hidden.clear(); chart.drag = null;
  const filters = $('lab-chart-filters'); filters.replaceChildren();
  $('lab-chart-reset').disabled = !data.points.length;
  $('lab-chart-export').disabled = !data.points.length;
  $('lab-chart-tooltip').textContent = '';
  if (!data.points.length) {
    chart.full = chart.view = null;
    chartCanvas.getContext('2d').clearRect(0, 0, chartCanvas.width, chartCanvas.height);
    if (gpuState.gl && !gpuState.lost) gpuScatter([]);
    renderCovariance(data);
    $('lab-chart-note').textContent = `Nenhum par numérico finito nesta amostra${data.coverage ? ` de ${data.sampled_rows} posições; ${data.dropped_nonfinite_pairs} pares não finitos omitidos. Índice sintético não é tempo físico; stride não autoriza espectro.` : '.'}`;
    return;
  }
  const xs = data.points.map(point => point[0]), ys = data.points.map(point => point[1]);
  const xmin = Math.min(...xs), xmax = Math.max(...xs), ymin = Math.min(...ys), ymax = Math.max(...ys);
  const dx = xmax - xmin || Math.max(1, Math.abs(xmin) * .1), dy = ymax - ymin || Math.max(1, Math.abs(ymin) * .1);
  chart.full = {xmin: xmin - dx * .06, xmax: xmax + dx * .06, ymin: ymin - dy * .08, ymax: ymax + dy * .08};
  chart.view = {...chart.full};
  if (data.observations) {
    [...new Set(data.observations.map(item => item.quantity))].forEach(quantity => {
      const label = element('label', 'chart-layer');
      const check = document.createElement('input'); check.type = 'checkbox'; check.checked = true;
      check.addEventListener('change', () => { if (check.checked) chart.hidden.delete(quantity); else chart.hidden.add(quantity); renderChart(); });
      const swatch = element('i'); swatch.style.background = chartColors[quantity] || '#e6edf0';
      label.append(check, swatch, element('span', '', quantity)); filters.append(label);
    });
  }
  renderCovariance(data);
  renderChart();
  $('lab-chart-note').textContent = `${data.points.length.toLocaleString('pt-BR')} pares na amostra de ${data.sampled_rows.toLocaleString('pt-BR')} posições examinadas · ${data.sample_method} · ${data.status}. ${data.coverage ? `${data.dropped_nonfinite_pairs} pares não finitos omitidos; índice sintético não é tempo físico; amostragem por stride não autoriza inferência espectral. ` : ''}Fonte: ${data.source.path}. ${data.covariance_path ? 'Barras = raiz da diagonal da covariância; os termos correlacionados continuam na matriz completa em ' + data.covariance_path + '. Filtrar cores não altera a matriz nem produz ajuste. ' : ''}Tamanho ${gib(data.source.bytes)}; mtime ${data.source_mtime_ns}. Sem inferência TGL aplicada.`;
}

let covarianceData = null;
const covCanvas = $('lab-cov-chart');
const covPad = 52;
function renderCovariance(data) {
  covarianceData = Array.isArray(data.covariance) ? data : null;
  $('lab-cov-panel').hidden = !covarianceData;
  if (!covarianceData) return;
  const ctx = covCanvas.getContext('2d'), n = data.covariance.length;
  const cell = (covCanvas.width - covPad * 2) / n;
  ctx.fillStyle = '#08151c'; ctx.fillRect(0, 0, covCanvas.width, covCanvas.height);
  ctx.font = '12px Segoe UI, sans-serif'; ctx.textAlign = 'center';
  for (let i = 0; i < n; i++) {
    ctx.fillStyle = '#9abfc4';
    ctx.fillText(String(i + 1), covPad + (i + .5) * cell, covPad - 15);
    ctx.fillText(String(i + 1), covPad - 20, covPad + (i + .65) * cell);
    for (let j = 0; j < n; j++) {
      const covariance = data.covariance[i][j];
      const correlation = Math.max(-1, Math.min(1, covariance / Math.sqrt(data.covariance[i][i] * data.covariance[j][j])));
      const strength = Math.abs(correlation);
      const color = correlation >= 0 ? [40, 110 + Math.round(115 * strength), 130 + Math.round(75 * strength)]
                                     : [105 + Math.round(130 * strength), 80 + Math.round(55 * strength), 70];
      ctx.fillStyle = `rgb(${color.join(',')})`;
      ctx.fillRect(covPad + j * cell + 1, covPad + i * cell + 1, cell - 2, cell - 2);
    }
  }
  ctx.textAlign = 'left';
  $('lab-cov-readout').textContent = 'Clique em uma célula para examinar o par de observáveis. A cor representa correlação, não significância.';
  $('lab-cov-source').textContent = `Média SHA-256 ${data.mean_sha256} · covariância SHA-256 ${data.covariance_sha256} · ${data.covariance_path}. Matriz completa lida do arquivo; nenhum χ² calculado nesta vista.`;
}
covCanvas.addEventListener('click', event => {
  if (!covarianceData) return;
  const rect = covCanvas.getBoundingClientRect();
  const x = (event.clientX - rect.left) * covCanvas.width / rect.width;
  const y = (event.clientY - rect.top) * covCanvas.height / rect.height;
  const cell = (covCanvas.width - covPad * 2) / covarianceData.covariance.length;
  const i = Math.floor((y - covPad) / cell), j = Math.floor((x - covPad) / cell);
  if (i < 0 || j < 0 || i >= covarianceData.covariance.length || j >= covarianceData.covariance.length) return;
  const a = covarianceData.observations[i], b = covarianceData.observations[j];
  const c = covarianceData.covariance[i][j];
  const rho = c / Math.sqrt(covarianceData.covariance[i][i] * covarianceData.covariance[j][j]);
  $('lab-cov-readout').textContent = `Célula ${i + 1}, ${j + 1} · ${a.quantity} (z=${a.z}) × ${b.quantity} (z=${b.z}) · Cij=${c.toPrecision(6)} · correlação=${rho.toPrecision(5)}. É um par da matriz original, sem recorte estatístico.`;
});

chartCanvas.addEventListener('wheel', event => {
  if (!chart.view) return;
  event.preventDefault();
  const position = chartPosition(event), map = chartMaps();
  const centerX = map.ix(position.x), centerY = map.iy(position.y);
  const factor = event.deltaY < 0 ? .82 : 1.22;
  const spanX = (chart.view.xmax - chart.view.xmin) * factor;
  const spanY = (chart.view.ymax - chart.view.ymin) * factor;
  if (spanX < (chart.full.xmax - chart.full.xmin) / 1e5 || spanX > (chart.full.xmax - chart.full.xmin) * 50) return;
  const fx = (position.x - chartPad) / (chartCanvas.width - 2 * chartPad);
  const fy = (chartCanvas.height - chartPad - position.y) / (chartCanvas.height - 2 * chartPad);
  chart.view = {xmin: centerX - fx * spanX, xmax: centerX + (1 - fx) * spanX,
                ymin: centerY - fy * spanY, ymax: centerY + (1 - fy) * spanY};
  renderChart();
}, {passive: false});
chartCanvas.addEventListener('pointerdown', event => {
  if (!chart.view || event.button !== 0) return;
  chart.drag = chartPosition(event); chartCanvas.setPointerCapture(event.pointerId);
});
chartCanvas.addEventListener('pointermove', event => {
  if (!chart.view) return;
  const position = chartPosition(event), map = chartMaps();
  if (chart.drag) {
    const dx = map.ix(chart.drag.x) - map.ix(position.x);
    const dy = map.iy(chart.drag.y) - map.iy(position.y);
    chart.view = {xmin: chart.view.xmin + dx, xmax: chart.view.xmax + dx,
                  ymin: chart.view.ymin + dy, ymax: chart.view.ymax + dy};
    chart.drag = position; renderChart(); return;
  }
  let nearest = -1, distance = 14 * 14;
  chart.data.points.forEach(([x, y], i) => {
    if (!visibleChartPoint(i)) return;
    const d = (map.px(x) - position.x) ** 2 + (map.py(y) - position.y) ** 2;
    if (d < distance) { distance = d; nearest = i; }
  });
  const tip = $('lab-chart-tooltip');
  if (nearest < 0) { tip.textContent = ''; return; }
  const point = chart.data.points[nearest], observation = chart.data.observations?.[nearest];
  tip.textContent = `${chart.data.x}=${point[0].toPrecision(6)} · ${chart.data.y}=${point[1].toPrecision(6)}${observation ? ' · ' + observation.quantity + ' · σ(diag)=' + observation.sigma.toPrecision(5) : ''}`;
});
chartCanvas.addEventListener('pointerup', () => { chart.drag = null; });
chartCanvas.addEventListener('pointercancel', () => { chart.drag = null; });
chartCanvas.addEventListener('pointerleave', () => { if (!chart.drag) $('lab-chart-tooltip').textContent = ''; });
chartCanvas.addEventListener('dblclick', () => { if (chart.full) { chart.view = {...chart.full}; renderChart(); } });
$('lab-chart-reset').addEventListener('click', () => { if (chart.full) { chart.view = {...chart.full}; renderChart(); } });
$('lab-chart-export').addEventListener('click', () => {
  if (!chart.data) return;
  const payload = {status: chart.data.status, source: chart.data.source, x: chart.data.x, y: chart.data.y,
                   sample_method: chart.data.sample_method, sampled_rows: chart.data.sampled_rows,
                   points: chart.data.points, observations: chart.data.observations || null,
                   note: 'Amostra exploratória; filtros e zoom são apenas visualização, sem ajuste físico.'};
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'}));
  link.download = `TGL_amostra_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
  link.click(); setTimeout(() => URL.revokeObjectURL(link.href), 1000);
});

async function labPlot() {
  const id = $('lab-file').value, x = $('lab-x').value, y = $('lab-y').value;
  if (!id || !x || !y) { $('lab-status').textContent = 'Escolha arquivo e duas colunas.'; return; }
  $('lab-status').textContent = 'Amostrando o arquivo em leitura limitada…';
  try {
    const data = await api(`/api/lab/preview?id=${encodeURIComponent(id)}&x=${encodeURIComponent(x)}&y=${encodeURIComponent(y)}&limit=800`);
    drawScatter(data);
    $('lab-status').textContent = `Amostra de ${data.points.length} pares exibida; fonte original não foi carregada inteira nem alterada.`;
  } catch (error) { $('lab-status').textContent = `Amostra recusada: ${error.message}`; }
}

$('lab-search').addEventListener('input', filterLab);
$('lab-file').addEventListener('change', labDescribe);
$('lab-plot').addEventListener('click', labPlot);

async function run(payload, target) {
  $(target).textContent = 'Executando…';
  try {
    const record = await api('/api/run', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
    const result = record.result;
    const displayed = {...result.values}; delete displayed.curve;
    $(target).textContent = `RUN #${record.run_id} · ${result.status}\n${JSON.stringify(displayed, null, 2)}\n\n${result.scope}`;
    if (result.operation === 'dephasing') drawCurve(result.values.curve);
    await loadRuns();
    return record;
  } catch (error) { $(target).textContent = `Execução recusada: ${error.message}`; }
}
$('run-chain').addEventListener('click', () => run({operation: 'identity_chain'}, 'chain-result'));
$('run-dephasing').addEventListener('click', () => run({operation: 'dephasing',
  omega_rad_s: $('omega').value === '' ? null : Number($('omega').value),
  tau_s: $('tau').value === '' ? null : Number($('tau').value),
  duration_s: $('duration').value === '' ? null : Number($('duration').value)}, 'dephasing-result'));

function drawCurve(values) {
  const canvas = $('curve'), context = canvas.getContext('2d');
  const {width, height} = canvas; context.clearRect(0, 0, width, height);
  context.strokeStyle = '#315659'; context.lineWidth = 1;
  for (let i = 0; i <= 4; i++) { context.beginPath(); context.moveTo(34, 16 + i * 36); context.lineTo(width - 14, 16 + i * 36); context.stroke(); }
  context.strokeStyle = '#66e3c7'; context.lineWidth = 2.5; context.beginPath();
  values.forEach((value, i) => { const x = 34 + (width - 48) * i / (values.length - 1), y = 16 + 144 * (1 - value); if (i) context.lineTo(x, y); else context.moveTo(x, y); });
  context.stroke(); context.fillStyle = '#9bb8b7'; context.font = '12px sans-serif'; context.fillText('coerência 1', 35, 13); context.fillText('tempo →', width - 80, height - 9);
}

async function loadRuns() {
  try {
    const rows = await api('/api/runs'), root = $('runs'); root.replaceChildren();
    if (!rows.length) { root.textContent = 'Nenhuma execução registrada.'; return; }
    rows.forEach(row => { const card = element('div', 'run');
      card.append(element('b', '', `#${row.id} · ${row.operation} · ${row.status}`),
                  element('small', '', `${row.created_utc} · parâmetros ${JSON.stringify(row.parameters)} · fonte ${row.source_sha256}`));
      root.append(card); });
  } catch (error) { $('runs').textContent = `Histórico indisponível: ${error.message}`; }
}

async function loadProtocols() {
  const panel = element('section', 'panel history');
  const head = element('div', 'panel-head');
  head.append(element('h3', '', 'Protocolos anteriores'), element('span', '', 'INDEXADOS POR RELATÓRIO'));
  panel.append(head, element('p', '', 'Alvos A0–A8 e T01–T19, com estatuto documental e origem. Reexecução pesada ainda não conectada.'));
  const root = element('div', 'protocol-grid', 'Lendo relatórios…');
  panel.append(root); $('experiment').append(panel);
  try {
    const records = await api('/api/protocols'); root.replaceChildren();
    records.forEach(record => {
      const card = element('details', 'protocol');
      const summary = element('summary');
      summary.append(element('b', '', record.target), element('span', '', record.reported_status));
      card.append(summary,
                  element('p', '', record.summary),
                  element('small', '', `${record.family} · ${record.source_path}:${record.source_line}`),
                  element('small', '', `SHA-256 ${record.source_sha256} · replay pendente`));
      root.append(card);
    });
  } catch (error) { root.textContent = `Inventário indisponível: ${error.message}`; }
}

function interpret(text) {
  const phrase = text.toLocaleLowerCase('pt-BR').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  if (phrase.startsWith('pesquisar ') || phrase.startsWith('investigar ')) {
    const question = text.replace(/^\s*(pesquisar|investigar)\s+/i, '').trim();
    return {label: 'Preparar pergunta no cockpit', action: () => { $('inquiry-question').value = question; show('research'); }};
  }
  if (phrase.includes('torre') || phrase.includes('kernel')) return {label: 'Abrir torre formal', action: () => show('tower')};
  if (phrase.includes('desi') || phrase.includes('kids') || phrase.includes('planck')) {
    const term = phrase.includes('desi') ? 'DESIVAST' : phrase.includes('kids') ? 'KiDS' : 'planck';
    return {label: `Localizar ${term} no catálogo`, action: () => { $('lab-search').value = term; filterLab(); show('data'); }};
  }
  if (phrase.includes('dados') || phrase.includes('gwosc')) return {label: 'Abrir dados instalados', action: () => show('data')};
  if (phrase.includes('calcular beta') || phrase.includes('cadeia da identidade')) return {label: 'Executar e registrar a cadeia da identidade', action: () => { show('experiment'); $('run-chain').click(); }};
  if (phrase.includes('experimento') || phrase.includes('dephasing')) return {label: 'Abrir experimentos', action: () => show('experiment')};
  return null;
}
$('interpret').addEventListener('click', () => {
  const command = interpret($('voice-text').value), root = $('intent'); root.replaceChildren();
  if (!command) { root.textContent = 'Comando não reconhecido. Nenhuma ação foi executada.'; return; }
  root.append(element('div', '', `Interpretação: ${command.label}`));
  const confirm = element('button', '', 'Confirmar ação');
  confirm.addEventListener('click', () => { command.action(); root.textContent = `Executado: ${command.label}`; });
  root.append(confirm);
});

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
function listenInto(inputId, statusId) {
  const recognition = new SpeechRecognition(); recognition.lang = 'pt-BR'; recognition.interimResults = false;
  recognition.onresult = event => { $(inputId).value = event.results[0][0].transcript; $(statusId).textContent = 'Transcrição recebida; confira antes de executar.'; };
  recognition.onerror = event => { $(statusId).textContent = `Falha do microfone: ${event.error}`; };
  recognition.onend = () => { if ($(statusId).textContent === 'Escutando…') $(statusId).textContent = 'Escuta encerrada.'; };
  $(statusId).textContent = 'Escutando…'; recognition.start();
}
if (!SpeechRecognition) {
  $('mic').disabled = true; $('research-mic').disabled = true;
  $('voice-status').textContent = 'Ditado indisponível neste navegador; digitação funciona.';
  $('research-voice-status').textContent = 'Ditado indisponível neste navegador.';
} else {
  $('mic').addEventListener('click', () => listenInto('voice-text', 'voice-status'));
  $('research-mic').addEventListener('click', () => listenInto('inquiry-question', 'research-voice-status'));
}

Promise.all([api('/api/overview'), loadRoutes(), loadData(), loadLab(), loadCanonicalForm(), loadBaoReport(), loadRuns(), loadProtocols(), loadInquiries()]).then(([overview]) => {
  renderOverview(overview); searchRelations();
}).catch(error => { $('metrics').textContent = `Fonte central indisponível: ${error.message}`; });
