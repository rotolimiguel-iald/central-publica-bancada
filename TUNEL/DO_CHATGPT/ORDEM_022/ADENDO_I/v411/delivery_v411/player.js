(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const filmButtons = [...document.querySelectorAll('[data-film]')];
  const languageNames = new Intl.DisplayNames(['pt-BR'], { type: 'language' });
  let film = '1';
  let video, scenes = [], active = -2, loopIndex = -1;
  let desiredTime = 0, desiredPlay = false;
  let tracks = new Map();
  let chapterButtons = [];

  function rows(data) {
    if (!Array.isArray(data)) return [];
    return data.filter(r => r && Number.isFinite(Number(r.start)) &&
      Number.isFinite(Number(r.end)) && Number(r.start) >= 0 && Number(r.end) > Number(r.start))
      .map(r => ({ ...r, start: Number(r.start), end: Number(r.end) }))
      .sort((a, b) => a.start - b.start);
  }

  function stamp(value) {
    const sec = Math.floor(value);
    return Math.floor(sec / 60) + ':' + String(sec % 60).padStart(2, '0');
  }

  function sceneAt(time) {
    return scenes.findIndex(s => s.start <= time && time < s.end);
  }

  function showScene(time) {
    const index = sceneAt(time);
    syncLab(time, index);
    const previous = scenes.findLastIndex(s => s.start < (index >= 0 ? scenes[index].start : time));
    const next = scenes.findIndex(s => s.start > time);
    $('previous').disabled = previous < 0;
    $('next').disabled = next < 0;
    $('previous').onclick = () => chapterButtons[previous]?.click();
    $('next').onclick = () => chapterButtons[next]?.click();
    $('repeat').disabled = index < 0 || !isReady();
    if (index === active) return;
    active = index;
    chapterButtons.forEach((b, i) => {
      if (i === index) b.setAttribute('aria-current', 'true');
      else b.removeAttribute('aria-current');
    });
    const scene = scenes[index];
    $('sceneTitle').textContent = scene ? scene.title || 'Capítulo ' + (index + 1) : 'Cena atual';
    for (const key of ['formula', 'note', 'source', 'status']) {
      const value = scene?.[key];
      $(key).textContent = typeof value === 'object' && value !== null ? JSON.stringify(value) : value ?? '';
      if ($(key + 'Row')) $(key + 'Row').hidden = !$(key).textContent;
    }
  }

  function setLoop(index) {
    loopIndex = index;
    $('repeat').setAttribute('aria-pressed', String(index >= 0));
  }

  function makeChapters() {
    scenes = rows(window.SCENES?.[film]);
    $('count').textContent = String(scenes.length);
    $('chapterStatus').textContent = scenes.length ? '' : 'Capítulos indisponíveis para este filme.';
    chapterButtons = scenes.map((s, i) => {
      const button = document.createElement('button');
      const time = document.createElement('span');
      time.className = 'stamp';
      time.textContent = stamp(s.start);
      button.append(time, document.createTextNode(s.title || 'Capítulo ' + (i + 1)));
      button.onclick = () => {
        if (loopIndex >= 0) setLoop(i);
        seek(s.start);
      };
      return button;
    });
    $('chapterList').replaceChildren(...chapterButtons.map(b => {
      const li = document.createElement('li');
      li.append(b);
      return li;
    }));
    active = -2;
  }

  function nameOf(code) {
    try { return languageNames.of(code); } catch { return code; }
  }

  function buildTracks(v) {
    const cues = rows(window.CAPTIONS?.[film]?.[$('voice').value]);
    const languages = new Set(cues.flatMap(c => Object.keys(c.translations || {})));
    const previous = $('language').value || 'pt-BR';
    const codes = languages.size ? [...languages] : ['pt-BR', 'en', 'fr', 'zh-Hans'];
    const menu = $('language');
    menu.replaceChildren(...codes.map(code => new Option(nameOf(code), code)), new Option('Desativadas', 'off'));
    menu.value = previous === 'off' || codes.includes(previous) ? previous : codes[0];
    tracks = new Map();
    for (const code of languages) {
      const t = v.addTextTrack('subtitles', nameOf(code), code);
      for (const c of cues) {
        const line = c.translations?.[code];
        if (typeof line !== 'string' || !line.trim()) continue;
        const literal = line.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
        t.addCue(new VTTCue(c.start, c.end, literal));
      }
      tracks.set(code, t);
    }
    applyCaptions();
    v.textTracks.onchange = () => {
      if (v !== video || !tracks.size) return;
      const selected = [...tracks].find(([, t]) => t.mode === 'showing');
      menu.value = selected?.[0] || 'off';
    };
    $('captionStatus').textContent = tracks.size ? '' : 'Legendas indisponíveis para esta narração.';
  }

  function applyCaptions() {
    for (const [code, track] of tracks) track.mode = code === $('language').value ? 'showing' : 'disabled';
  }

  function isReady() {
    return video && video.readyState >= 1 && !video.error && Number.isFinite(video.duration);
  }

  function seek(time) {
    desiredTime = Math.max(0, time);
    if (isReady()) video.currentTime = Math.min(desiredTime, video.duration);
    showScene(isReady() ? video.currentTime : desiredTime);
  }

  function requestPlay(v) {
    v.play().catch(error => {
      if (video === v && error.name !== 'AbortError') {
        desiredPlay = false;
        $('mediaStatus').textContent = 'Reprodução interrompida. Use Reproduzir para continuar.';
      }
    });
  }

  function loadMedia(reset = false) {
    const old = video;
    if (old && isReady()) {
      desiredTime = old.currentTime;
      desiredPlay = !old.paused && !old.ended;
    }
    if (reset) {
      desiredTime = 0;
      desiredPlay = false;
      setLoop(-1);
      makeChapters();
    }
    const v = document.createElement('video');
    video = v;
    v.controls = true;
    v.playsInline = true;
    v.preload = 'metadata';
    v.lang = $('voice').value;
    v.setAttribute('aria-label', 'Filme ' + film + ', narração em ' + $('voice').selectedOptions[0].text);
    v.poster = 'render/filme' + film + '_poster.jpg';
    if (old) {
      v.volume = old.volume;
      v.muted = old.muted;
      old.pause();
      old.replaceChildren();
      old.removeAttribute('src');
      old.load();
    }
    $('stage').replaceChildren(v);
    $('mediaStatus').textContent = 'Carregando filme…';
    $('retry').hidden = true;
    $('play').textContent = 'Reproduzir';
    for (const id of ['play', 'back', 'forward', 'repeat']) $(id).disabled = true;
    buildTracks(v);
    showScene(desiredTime);
    const quality = $('quality').value;
    const variants = quality === 'auto' ? ['1080p.mp4', '1080p.webm', '720p.mp4'] : [quality];
    const suffix = $('voice').value === 'pt-BR' ? '_pt-BR' : '';

    function failed() {
      if (v !== video) return;
      $('mediaStatus').textContent = 'Não foi possível abrir o vídeo local desta narração. Confira a pasta render ou selecione outro formato.';
      $('retry').hidden = false;
      for (const id of ['play', 'back', 'forward', 'repeat']) $(id).disabled = true;
    }
    v.onerror = failed;
    variants.forEach((variant, i) => {
      const [size, ext] = variant.split('.');
      const source = document.createElement('source');
      source.src = 'render/filme' + film + '_' + size + suffix + '.' + ext;
      source.type = 'video/' + ext;
      if (i === variants.length - 1) source.onerror = failed;
      v.append(source);
    });

    v.onloadedmetadata = () => {
      if (v !== video) return;
      $('mediaStatus').textContent = '';
      for (const id of ['play', 'back', 'forward']) $(id).disabled = false;
      v.playbackRate = Number($('speed').value);
      seek(desiredTime);
      if (desiredPlay) requestPlay(v);
    };
    v.onplay = v.onpause = () => {
      if (v !== video) return;
      desiredPlay = !v.paused;
      $('play').textContent = v.paused ? 'Reproduzir' : 'Pausar';
    };
    v.onratechange = () => {
      if (v !== video || !isReady()) return;
      const speed = String(v.playbackRate);
      if (![...$('speed').options].some(option => option.value === speed)) {
        $('speed').add(new Option(speed, speed));
      }
      $('speed').value = speed;
    };
    v.onseeking = () => {
      if (v !== video) return;
      if (loopIndex >= 0) setLoop(sceneAt(v.currentTime));
      showScene(v.currentTime);
    };
    v.ontimeupdate = () => {
      if (v !== video || !isReady()) return;
      const loop = scenes[loopIndex];
      if (loop && !v.paused && !v.seeking && v.currentTime >= loop.end) v.currentTime = loop.start;
      showScene(v.currentTime);
    };
    v.onended = () => {
      const loop = scenes[loopIndex];
      if (v !== video || !loop) return;
      v.currentTime = loop.start;
      requestPlay(v);
    };
    v.load();
  }

  filmButtons.forEach(b => b.onclick = () => {
    if (film === b.dataset.film) return;
    film = b.dataset.film;
    filmButtons.forEach(item => item.setAttribute('aria-pressed', String(item === b)));
    loadMedia(true);
  });
  $('voice').onchange = $('quality').onchange = () => loadMedia();
  $('retry').onclick = () => loadMedia();
  $('language').onchange = applyCaptions;
  $('speed').onchange = () => { video.playbackRate = Number($('speed').value); };
  $('play').onclick = () => { if (video.paused) requestPlay(video); else video.pause(); };
  $('back').onclick = () => seek(video.currentTime - 10);
  $('forward').onclick = () => seek(video.currentTime + 10);
  $('repeat').onclick = () => setLoop(loopIndex >= 0 ? -1 : sceneAt(video.currentTime));

  function createLab() {
    // Extracted from the v411 source, without importing or executing um.py.
    const alpha = 7.2973525693e-3;
    const beta = alpha * Math.sqrt(Math.E);
    const a = beta, c = beta / 2;
    const caustic = Math.PI / (2 * Math.sqrt(Math.max(a, c)));
    const tMax = 0.85 * caustic;
    const density = k => 0.25 / Math.cosh(k / 2) ** 2;
    const polarization = k => Math.tanh(k / 2);
    const area = t => Math.cos(Math.sqrt(a) * t) * Math.cos(Math.sqrt(c) * t);
    const format = (n, digits = 5) => n.toLocaleString('pt-BR', {maximumFractionDigits: digits});
    const panel = $('lab'), mode = $('labMode'), kInput = $('kappa'), tInput = $('opticalTime');
    tInput.max = String(tMax);
    $('constants').textContent = 'α = ' + format(alpha, 13) + ' • β = α√e = ' + format(beta, 12) +
      ' • t máx. = ' + format(tMax) + ' • primeira cáustica em t = ' + format(caustic) + '.';

    function plot(id, xMin, xMax, yMin, yMax, fn) {
      const svg = $(id);
      const left = 37, right = 279, top = 10, bottom = 99;
      const x = n => left + (right - left) * (n - xMin) / (xMax - xMin);
      const y = n => bottom - (bottom - top) * (n - yMin) / (yMax - yMin);
      svg.setAttribute('viewBox', '0 0 292 124');
      function element(tag, attributes, label) {
        const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (const [key, value] of Object.entries(attributes)) el.setAttribute(key, String(value));
        if (label !== undefined) el.textContent = label;
        svg.append(el);
        return el;
      }
      function tick(px, py, label, alignment) {
        element('text', { x: px, y: py, 'text-anchor': alignment }, label);
      }
      element('path', { class: 'axis', d: 'M'+left+' '+top+'V'+bottom+'H'+right });
      tick(left - 5, top + 6, format(yMax), 'end');
      tick(left - 5, bottom, format(yMin), 'end');
      for (const [value, align] of [[xMin, 'start'], [xMax, 'end']]) {
        tick(x(value), bottom + 18, format(value, 2), align);
      }
      if (xMin < 0) {
        element('line', {class: 'guide', x1: x(0), x2: x(0), y1: top, y2: bottom});
        tick(x(0), bottom + 18, '0', 'middle');
      }
      if (yMin < 0) element('line', {class: 'guide', x1: left, x2: right, y1: y(0), y2: y(0)});
      const curve = [];
      for (let i = 0; i <= 240; i++) {
        const value = xMin + (xMax - xMin) * i / 240;
        curve.push(x(value).toFixed(3) + ',' + y(fn(value)).toFixed(3));
      }
      element('polyline', {class: 'curve', points: curve.join(' ')});
      const dot = element('circle', {class: 'point', r: 4.5});
      return value => {
        const result = fn(value);
        dot.setAttribute('cx', x(value));
        dot.setAttribute('cy', y(result));
        return result;
      };
    }

    const rhoPoint = plot('rhoPlot', -6, 6, 0, .25, density);
    const qPoint = plot('qPlot', -6, 6, -1, 1, polarization);
    const areaPoint = plot('areaPlot', 0, tMax, 0, 1, area);
    function setKappa(k) {
      kInput.value = String(k);
      const value = kInput.valueAsNumber;
      $('kappaValue').textContent = '= ' + format(value, 2);
      $('rhoValue').textContent = 'ρ = ' + format(rhoPoint(value), 6);
      $('qValue').textContent = 'q = ' + format(qPoint(value), 6);
      kInput.setAttribute('aria-valuetext', 'κ igual a ' + format(value, 2) + ', ' +
        $('rhoValue').textContent + ', ' + $('qValue').textContent);
    }
    function setTime(t) {
      tInput.value = String(t);
      const value = tInput.valueAsNumber;
      $('timeValue').textContent = '= ' + format(value);
      $('areaValue').textContent = 'A(t)/A(0) = ' + format(areaPoint(value), 6);
      tInput.setAttribute('aria-valuetext', 't igual a ' + format(value) + ', área relativa ' +
        format(area(value), 6));
    }

    let frame = 0;
    function stop() {
      cancelAnimationFrame(frame);
      frame = 0;
      $('sweep').textContent = 'Animar κ';
    }
    $('sweep').onclick = () => {
      if (frame) { stop(); return; }
      const initial = kInput.valueAsNumber + 6;
      const start = performance.now();
      $('sweep').textContent = 'Pausar κ';
      function advance(now) {
        const phase = (initial + (now - start) / 1000 * 2) % 24;
        setKappa(6 - Math.abs(phase - 12));
        frame = requestAnimationFrame(advance);
      }
      frame = requestAnimationFrame(advance);
    };
    kInput.oninput = () => { stop(); setKappa(kInput.valueAsNumber); };
    tInput.oninput = () => setTime(tInput.valueAsNumber);
    function follow(time, index) {
      if (!panel.open || mode.value !== 'follow') return;
      const s = scenes[index];
      const fraction = s ? (time - s.start) / (s.end - s.start) :
        video?.ended ? 1 : 0;
      const u = Math.max(0, Math.min(1, fraction));
      setKappa(-6 + 12 * u);
      setTime(tMax * u);
    }
    function refreshMode() {
      stop();
      const synced = mode.value === 'follow';
      for (const control of [kInput, tInput, $('sweep')]) control.disabled = synced;
      $('labHint').textContent = synced
        ? 'O avanço de cada capítulo percorre a faixa de κ e o intervalo óptico t. A pausa congela os pontos. Fora dos capítulos, a inspeção fica no início ou no fim do filme.'
        : 'Use as setas nos seletores para ajustar κ e t de forma independente.';
      const time = isReady() ? video.currentTime : desiredTime;
      follow(time, sceneAt(time));
    }
    panel.ontoggle = mode.onchange = refreshMode;
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    setKappa(0);
    setTime(0);
    refreshMode();
    return follow;
  }
  const syncLab = createLab();
  loadMedia(true);
})();
