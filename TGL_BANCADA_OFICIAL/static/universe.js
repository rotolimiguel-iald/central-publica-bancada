/* Universo residente: same-origin API client. No physical model is computed here. */
(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const finite = (value) => typeof value === "number" && Number.isFinite(value);
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
  const integer = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
  const decimal = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 6 });
  const FRAME_MS = 125;
  const MODEL_DELAY_MS = 420;
  const STATES = new Set(["IDLE", "LOADING", "READY", "PARTIAL", "FAILED", "RELEASING"]);
  const READINGS = new Set(["R-A", "R-B", "R-RAIZ-0", "R-GLOBAL"]);
  const state = {
    domains: [], snapshot: null, connected: false, mutating: false,
    series: [], selected: null, userSelected: false, seriesSignature: "", start: 0, duration: 1,
    playing: false, speed: 1, lastAdvance: 0,
    viewRevision: 0, viewController: null, viewTimer: null, lastViewAt: -Infinity,
    pollRevision: 0, pollController: null, pollTimer: null,
    modelRevision: 0, modelController: null, modelTimer: null,
    eventMetadata: null, eventMetadataLoading: false, eventMetadataRevision: 0, eventMetadataController: null,
    eventDefaultsSet: false, eventRevision: 0, eventController: null, eventTimer: null,
    eventAccessKey: "", eventLoadIdentity: null, eventResult: null, eventResultLabel: "",
    domainsRevision: 0, domainButtons: new Map(), destroyed: false
  };

  function number(value, digits = 4) {
    if (!finite(value)) return "—";
    if (value === 0) return "0";
    if (Math.abs(value) < 0.001 || Math.abs(value) >= 1e7) {
      return value.toExponential(digits).replace(".", ",");
    }
    return new Intl.NumberFormat("pt-BR", { maximumFractionDigits: digits }).format(value);
  }
  function count(value) { return finite(value) && value >= 0 ? integer.format(value) : "—"; }
  function modelMetric(value, unit = "") {
    return finite(value) ? `${number(value, 6)}${unit}` : "Indisponível";
  }
  function qnmMode(value) {
    return Array.isArray(value) && value.length === 3 && value.every(Number.isInteger)
      ? value.join(", ") : "Indisponível";
  }
  function regimePreset(search) {
    const regimes = new URLSearchParams(search).getAll("regime");
    if (regimes.length !== 1) return null;
    const presets = new Map([
      ["high-spin", { title: "Spin elevado", controls: { "model-mass": 65, "model-spin": 0.95, "model-redshift": 0.1, "model-duration": 0.12 } }],
      ["high-frequency", { title: "Frequência elevada", controls: { "model-mass": 20, "model-spin": 0.7, "model-redshift": 0.1, "model-duration": 0.12 } }]
    ]);
    return presets.get(regimes[0]) || null;
  }
  function seconds(value) { return finite(value) ? `${number(value, 6)} s` : "—"; }
  function percent(value) {
    return finite(value) && value >= 0 && value <= 1 ? `${number(value * 100, 2)}%` : "—";
  }
  function bytes(value) {
    if (!finite(value) || value < 0) return "—";
    const units = ["B", "KiB", "MiB", "GiB", "TiB"];
    const power = value > 0 ? Math.min(4, Math.floor(Math.log(value) / Math.log(1024))) : 0;
    return `${number(value / (1024 ** power), power ? 1 : 0)} ${units[power]}`;
  }
  function content(value, fallback = "Não informado") {
    if (value === null || value === undefined || value === "") return fallback;
    return typeof value === "object" ? JSON.stringify(value) : String(value);
  }
  function text(id, value) { $(id).textContent = value; }
  function node(tag, className, value) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (value !== undefined) element.textContent = value;
    return element;
  }
  function reference(value) {
    if (!value || typeof value !== "object") return "Referência temporal não informada pelo executor.";
    return [content(value.status, "Estatuto não informado"), content(value.text, "Descrição não informada")].join(" · ");
  }

  async function api(path, options = {}) {
    const { body, signal, method = "GET", timeout = 20000 } = options;
    const controller = new AbortController();
    let timedOut = false;
    const abort = () => controller.abort();
    if (signal?.aborted) controller.abort();
    else signal?.addEventListener("abort", abort, { once: true });
    const timer = setTimeout(() => { timedOut = true; controller.abort(); }, timeout);
    try {
      const response = await fetch(`/api/universe/${path}`, {
        method, credentials: "same-origin", cache: "no-store", signal: controller.signal,
        headers: body === undefined ? { Accept: "application/json" } : { Accept: "application/json", "Content-Type": "application/json" },
        ...(body === undefined ? {} : { body: JSON.stringify(body) })
      });
      let result;
      try { result = await response.json(); }
      catch (error) {
        if (error.name === "AbortError") throw error;
        throw new Error(`Resposta inválida do servidor (HTTP ${response.status}).`);
      }
      if (!response.ok) {
        const error = new Error(content(result?.error || result?.message || result?.detail, `HTTP ${response.status}`));
        error.response = result;
        throw error;
      }
      if (!result || typeof result !== "object") throw new Error("O servidor não retornou um objeto JSON.");
      return result;
    } catch (error) {
      if (timedOut) throw new Error("O servidor excedeu o tempo de resposta. Consulte o estado antes de tentar novamente.");
      throw error;
    } finally {
      clearTimeout(timer);
      signal?.removeEventListener("abort", abort);
    }
  }

  /* Plot coordinates are normalized on the CPU before Float32 upload. This keeps
     tiny strain values and large time offsets out of the shader's numeric range. */
  class Plot {
    constructor(canvas, gpuCanvas = null, options = {}) {
      this.canvas = canvas;
      this.context = canvas.getContext("2d");
      this.gpuCanvas = gpuCanvas;
      this.gl = null;
      this.program = null;
      this.buffer = null;
      this.data = null;
      this.kind = options.kind || (gpuCanvas ? "envelope" : "model");
      this.rendererId = options.rendererId || "renderer-label";
      this.width = 0;
      this.height = 0;
      this.rect = null;
      this.gpuReason = "";
      if (gpuCanvas) {
        gpuCanvas.addEventListener("webglcontextlost", (event) => {
          event.preventDefault();
          this.gl = null;
          this.gpuReason = "contexto GPU perdido";
          this.rendererLabel();
          this.draw();
        });
        gpuCanvas.addEventListener("webglcontextrestored", () => { this.initGPU(); this.draw(); });
        this.initGPU();
      }
      this.observer = typeof ResizeObserver === "function" ? new ResizeObserver(() => this.draw()) : null;
      this.observer?.observe(canvas.parentElement);
      this.resize = () => this.draw();
      window.addEventListener("resize", this.resize);
      this.draw();
    }

    initGPU() {
      const gl = this.gpuCanvas.getContext("webgl2", { alpha: true, antialias: false, premultipliedAlpha: false, depth: false });
      if (!gl) { this.gpuReason = "WebGL2 indisponível"; this.rendererLabel(); return; }
      const shaders = [];
      let program = null;
      let buffer = null;
      try {
        const compile = (type, source) => {
          const shader = gl.createShader(type);
          if (!shader) throw new Error("Shader indisponível");
          shaders.push(shader);
          gl.shaderSource(shader, source);
          gl.compileShader(shader);
          if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error("Compilação do renderizador indisponível");
          return shader;
        };
        const vertex = compile(gl.VERTEX_SHADER, `#version 300 es
          in vec2 position;
          void main() { gl_Position = vec4(position, 0.0, 1.0); }`);
        const fragment = compile(gl.FRAGMENT_SHADER, `#version 300 es
          precision mediump float;
          uniform vec4 strokeColor;
          out vec4 color;
          void main() { color = strokeColor; }`);
        program = gl.createProgram();
        if (!program) throw new Error("Programa GPU indisponível");
        gl.attachShader(program, vertex);
        gl.attachShader(program, fragment);
        gl.linkProgram(program);
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error("Ligação do renderizador indisponível");
        buffer = gl.createBuffer();
        if (!buffer) throw new Error("Buffer GPU indisponível");
        this.gl = gl;
        this.program = program;
        this.buffer = buffer;
        this.position = gl.getAttribLocation(program, "position");
        this.colorLocation = gl.getUniformLocation(program, "strokeColor");
        this.gpuReason = "";
      } catch (error) {
        if (program) gl.deleteProgram(program);
        if (buffer) gl.deleteBuffer(buffer);
        this.gl = null;
        this.gpuReason = error.message;
      } finally { shaders.forEach((shader) => gl.deleteShader(shader)); }
      this.rendererLabel();
    }

    rendererLabel() {
      if (!this.gpuCanvas) return;
      text(this.rendererId, this.gl ? "GPU · WebGL2" : "Canvas2D · fallback");
      $(this.rendererId).title = this.gl ? "Traços na GPU; eixos em Canvas2D." : this.gpuReason;
    }
    setData(data) { this.data = data; this.draw(); }
    clear() { this.setData(null); }
    validPoint(point) {
      return Array.isArray(point) && finite(point[0]) && finite(point[1]) && finite(point[2]) && point[1] <= point[2];
    }
    curves() {
      if (this.kind === "event") return [["strain", "#ecc188", []], ["gr", "#90b9f8", []], ["tgl", "#80ead0", [5, 3]]];
      if (this.kind === "residual") return [["residual_gr", "#90b9f8", []], ["residual_tgl", "#80ead0", [5, 3]]];
      return [["gr", "#90b9f8", []], ["tgl", "#80ead0", [5, 3]]];
    }
    layout() {
      const bounds = this.canvas.parentElement.getBoundingClientRect();
      this.width = Math.max(1, bounds.width);
      this.height = Math.max(1, bounds.height);
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      for (const canvas of [this.canvas, this.gpuCanvas].filter(Boolean)) {
        const width = Math.round(this.width * ratio);
        const height = Math.round(this.height * ratio);
        if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; }
      }
      if (this.context) this.context.setTransform(ratio, 0, 0, ratio, 0, 0);
      this.rect = { left: this.width < 480 ? 66 : 77, top: 30, right: this.width - 20, bottom: this.height - (this.data?.displayMode === "normalized" ? 61 : 43) };
    }
    draw() {
      this.layout();
      const ctx = this.context;
      if (!ctx) return;
      ctx.clearRect(0, 0, this.width, this.height);
      if (this.gl) {
        this.gl.viewport(0, 0, this.gpuCanvas.width, this.gpuCanvas.height);
        this.gl.clearColor(0, 0, 0, 0);
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
      }
      const data = this.data;
      const r = this.rect;
      if (r.right <= r.left) return;
      let peak = 0;
      if (data) {
        if (this.kind === "envelope") {
          for (const point of data.points) if (this.validPoint(point)) peak = Math.max(peak, Math.abs(point[1]), Math.abs(point[2]));
        } else {
          for (const [key] of this.curves()) for (const value of data[key]) if (finite(value)) peak = Math.max(peak, Math.abs(value));
        }
      }
      const limit = peak > 0 ? peak * 1.1 : 1;
      const xStart = data ? (this.kind === "envelope" ? data.start_s : data.time_s.find(finite) ?? 0) : 0;
      const lastTime = data && this.kind !== "envelope" ? data.time_s.filter(finite).at(-1) : null;
      const xDuration = data ? (this.kind === "envelope" ? data.duration_s : Math.max(Number.EPSILON, lastTime - xStart)) : 1;
      this.scale = { xStart, xDuration, limit };
      const x = (value) => r.left + ((value - xStart) / xDuration) * (r.right - r.left);
      const y = (value) => (r.top + r.bottom) / 2 - (value / limit) * (r.bottom - r.top) / 2;
      this.axes(ctx, data, xStart, xDuration, limit);
      if (!data) return;
      ctx.save();
      ctx.beginPath(); ctx.rect(r.left, r.top, r.right - r.left, r.bottom - r.top); ctx.clip();
      if (this.kind === "envelope") {
        if (this.gl) this.envelopeGPU(data.points, x, y);
        else {
          ctx.strokeStyle = "#80ead0"; ctx.lineWidth = 1;
          ctx.beginPath();
          for (const point of data.points) {
            if (!this.validPoint(point)) continue;
            const px = x(point[0]);
            const low = y(point[2]);
            const high = y(point[1]);
            ctx.moveTo(px, low); ctx.lineTo(px, Math.max(low + 1, high));
          }
          ctx.stroke();
        }
      } else {
        for (const [key, color, dash] of this.curves()) {
          if (this.gl) { this.curveGPU(data.time_s, data[key], x, y, color); continue; }
          ctx.beginPath(); ctx.strokeStyle = color; ctx.lineWidth = 1.7; ctx.setLineDash(dash);
          let connected = false;
          for (let i = 0; i < data.time_s.length; i += 1) {
            const value = data[key][i];
            const time = data.time_s[i];
            if (!finite(time) || !finite(value)) { connected = false; continue; }
            if (connected) ctx.lineTo(x(time), y(value));
            else ctx.moveTo(x(time), y(value));
            connected = true;
          }
          ctx.stroke();
        }
      }
      ctx.restore();
    }

    axes(ctx, data, start, duration, limit) {
      const r = this.rect;
      ctx.save(); ctx.font = '10px "Segoe UI", sans-serif'; ctx.lineWidth = 1;
      const columns = this.width < 500 ? 3 : 5;
      for (let i = 0; i <= columns; i += 1) {
        const tick = data?.displayMode === "normalized" ? Math.round(start + duration * i / columns) : start + duration * i / columns;
        const px = r.left + (r.right - r.left) * (tick - start) / duration;
        ctx.strokeStyle = "#23334388"; ctx.beginPath(); ctx.moveTo(px, r.top); ctx.lineTo(px, r.bottom); ctx.stroke();
        ctx.fillStyle = "#91a7b6"; ctx.textAlign = i === 0 ? "left" : (i === columns ? "right" : "center");
        if (data) ctx.fillText(number(tick, 5), px, r.bottom + 19);
      }
      for (let i = 0; i <= 4; i += 1) {
        const py = r.top + (r.bottom - r.top) * i / 4;
        ctx.strokeStyle = i === 2 ? "#40525f" : "#23334388";
        ctx.beginPath(); ctx.moveTo(r.left, py); ctx.lineTo(r.right, py); ctx.stroke();
        ctx.fillStyle = "#91a7b6"; ctx.textAlign = "right";
        if (data) ctx.fillText(number(limit * (1 - i / 2), 2), r.left - 9, py + 3);
      }
      if (data) {
        ctx.textAlign = "left"; ctx.fillStyle = "#a5bac3";
        const eventPlot = this.kind === "event" || this.kind === "residual";
        const normalized = eventPlot && data.displayMode === "normalized";
        const units = this.kind === "envelope" ? content(data.units, "Unidade não informada") : normalized ? "Coordenada transformada · adimensional" : eventPlot ? (this.kind === "residual" ? "Resíduo · strain" : "Strain · dado / GR / TGL") : "Polarização efetiva";
        ctx.fillText(units, r.left, 17, r.right - r.left);
        ctx.textAlign = "right"; ctx.fillStyle = "#8c9fae";
        if (normalized) {
          ctx.fillText("Índice da amostra de referência (0–409;", r.right, this.height - 20, r.right - r.left);
          ctx.fillText("Δt=1/2048 s)", r.right, this.height - 6, r.right - r.left);
        } else ctx.fillText(this.kind === "envelope" ? "Tempo relativo ao arquivo · s" : eventPlot ? "Tempo desde o pico de referência · s" : "Tempo do modelo · s", r.right, this.height - 6, r.right - r.left);
      }
      ctx.restore();
    }

    envelopeGPU(points, x, y) {
      const r = this.rect;
      const vertices = [];
      const nx = (value) => value / this.width * 2 - 1;
      const ny = (value) => 1 - value / this.height * 2;
      for (const point of points) {
        if (!this.validPoint(point)) continue;
        const px = x(point[0]);
        if (px < r.left || px > r.right) continue;
        const top = clamp(y(point[2]), r.top, r.bottom);
        const bottom = clamp(Math.max(top + 1, y(point[1])), r.top, r.bottom);
        const left = nx(Math.max(r.left, px - 0.5));
        const right = nx(Math.min(r.right, px + 0.5));
        const upper = ny(top); const lower = ny(bottom);
        // Independent rectangles preserve min/max and never bridge missing bins.
        vertices.push(left, upper, left, lower, right, upper, right, upper, left, lower, right, lower);
      }
      this.drawGPU(vertices, "#80ead0");
    }
    curveGPU(times, values, x, y, color) {
      const vertices = [];
      const vertex = (px, py) => vertices.push(px / this.width * 2 - 1, 1 - py / this.height * 2);
      for (let i = 1; i < times.length; i += 1) {
        if (![times[i - 1], times[i], values[i - 1], values[i]].every(finite)) continue;
        const ax = x(times[i - 1]); const ay = y(values[i - 1]);
        const bx = x(times[i]); const by = y(values[i]);
        const length = Math.hypot(bx - ax, by - ay);
        if (!length) continue;
        const dx = -(by - ay) / length * 0.8; const dy = (bx - ax) / length * 0.8;
        // Adjacent finite samples only: nulls break each detector's curves.
        vertex(ax + dx, ay + dy); vertex(ax - dx, ay - dy); vertex(bx + dx, by + dy);
        vertex(bx + dx, by + dy); vertex(ax - dx, ay - dy); vertex(bx - dx, by - dy);
      }
      this.drawGPU(vertices, color);
    }
    drawGPU(vertices, color) {
      const gl = this.gl;
      const rgb = [1, 3, 5].map((offset) => parseInt(color.slice(offset, offset + 2), 16) / 255);
      gl.useProgram(this.program); gl.uniform4f(this.colorLocation, ...rgb, 1);
      gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.DYNAMIC_DRAW);
      gl.enableVertexAttribArray(this.position);
      gl.vertexAttribPointer(this.position, 2, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, vertices.length / 2);
    }
    destroy() {
      this.observer?.disconnect(); window.removeEventListener("resize", this.resize);
      if (this.gl) { this.gl.deleteBuffer(this.buffer); this.gl.deleteProgram(this.program); }
    }
  }

  const observedPlot = new Plot($("observed-axes"), $("observed-gpu"));
  const modelPlot = new Plot($("model-canvas"));
  const eventPlots = Object.fromEntries(["H1", "L1"].map((detector) => [detector, {
    overlay: new Plot($(`event-${detector}-axes`), $(`event-${detector}-gpu`), { kind: "event", rendererId: `event-${detector}-renderer` }),
    residual: new Plot($(`event-${detector}-residual`), null, { kind: "residual" })
  }]));

  function renderDomains() {
    const grid = $("domain-grid");
    const fragment = document.createDocumentFragment();
    state.domainButtons.clear();
    state.domains.forEach((domain, index) => {
      if (domain.id === "cosmology") {
        const card = node("article", "domain-card");
        const top = node("div", "domain-top");
        top.append(node("span", "domain-symbol", "◎"), node("span", "badge", "DESI BAO"));
        const link = node("a", "button secondary", "Explorar expansão e redshift →");
        link.href = "http://127.0.0.1:18766/cosmos";
        card.append(top, node("h3", "", "Cosmologia · domínio acústico"),
          node("p", "domain-description", "13 medidas DESI DR2 e sua covariância completa. Distâncias, expansão e resíduos interativos."),
          node("p", "domain-scope", "Primeira etapa: background FLRW de referência. Previsão canônica TGL e espectros CMB ainda em integração."), link);
        fragment.append(card);
        return;
      }
      const card = node("article", `domain-card${domain.implemented ? "" : " unavailable"}`);
      const top = node("div", "domain-top");
      const symbol = node("span", "domain-symbol", domain.id === "gw_strain" ? "∿" : String(index + 1).padStart(2, "0"));
      symbol.setAttribute("aria-hidden", "true");
      const badge = node("span", `badge${domain.implemented ? "" : " neutral"}`, domain.implemented ? "Disponível" : "Em preparação");
      top.append(symbol, badge);
      const stats = node("div", "domain-stats");
      const files = Array.isArray(domain.files) ? domain.files.length : domain.files;
      if (domain.implemented) stats.append(node("span", "", `${count(files)} arquivos`), node("span", "", `${bytes(domain.source_bytes)} na fonte`));
      else stats.append(node("span", "", "Perfil de carga em preparação"));
      const button = node("button", "button secondary", "Carregar domínio inteiro →");
      button.type = "button";
      button.setAttribute("aria-label", `Carregar ${content(domain.title)} por inteiro em RAM`);
      button.addEventListener("click", () => mutateMemory("load", { domain: domain.id }));
      card.append(top, node("h3", "", content(domain.title)), node("p", "domain-description", content(domain.description)), stats,
        node("p", "domain-scope", `Escopo · ${content(domain.scope)}`), button);
      fragment.append(card);
      state.domainButtons.set(domain.id, { button, card, badge, domain });
    });
    grid.replaceChildren(fragment);
    text("domain-count", count(state.domains.filter((domain) => domain.implemented || domain.id === "cosmology").length));
    updateDomainButtons();
  }
  function updateDomainButtons() {
    const snapshot = state.snapshot;
    const busy = state.mutating || ["LOADING", "RELEASING"].includes(snapshot?.status);
    for (const { button, card, badge, domain } of state.domainButtons.values()) {
      const resident = snapshot?.domain === domain.id && ["LOADING", "READY", "PARTIAL"].includes(snapshot?.status);
      card.classList.toggle("active", resident);
      button.disabled = !domain.implemented || busy || !state.connected || (resident && snapshot?.status === "READY");
      button.textContent = !domain.implemented ? "Domínio ainda não implementado" : resident ?
        (snapshot.status === "LOADING" ? "Carregando em RAM…" : snapshot.status === "READY" ? "Domínio residente em RAM" : "Recarregar domínio inteiro →") : "Carregar domínio inteiro →";
      badge.textContent = resident ? (snapshot.status === "PARTIAL" ? "Parcial" : snapshot.status === "LOADING" ? "Carregando" : "Em RAM") : domain.implemented ? "Disponível" : "Em preparação";
    }
    $("release-memory").disabled = !state.connected || state.mutating || !snapshot || ["IDLE", "RELEASING"].includes(snapshot.status);
  }
  async function loadDomains() {
    const revision = ++state.domainsRevision;
    $("refresh-domains").disabled = true;
    text("domains-message", "Consultando os domínios disponíveis…");
    try {
      const result = await api("domains");
      if (revision !== state.domainsRevision || state.destroyed) return;
      if (!Array.isArray(result.domains) || result.domains.some((domain) => !domain || typeof domain.id !== "string" || typeof domain.implemented !== "boolean")) {
        throw new Error("Lista de domínios inválida.");
      }
      state.domains = result.domains;
      renderDomains();
      text("domains-message", result.domains.length ? "Escolha um domínio para carregar seus arquivos em memória." : "O servidor ainda não disponibilizou domínios.");
      $("domains-message").classList.remove("error");
      text("time-reference-text", content(result.time_reference?.text, "Referência temporal não informada pelo servidor."));
      text("time-reference-status", content(result.time_reference?.status, "Não informado"));
    } catch (error) {
      if (revision !== state.domainsRevision || state.destroyed) return;
      text("domains-message", `Não foi possível consultar os domínios: ${error.message}`);
      $("domains-message").classList.add("error");
    } finally { if (revision === state.domainsRevision) $("refresh-domains").disabled = false; }
  }

  function cancelPoll() {
    state.pollRevision += 1; clearTimeout(state.pollTimer); state.pollController?.abort();
  }
  function schedulePoll(delay = 0) {
    clearTimeout(state.pollTimer);
    if (!state.destroyed && !state.mutating) state.pollTimer = setTimeout(pollStatus, delay);
  }
  async function pollStatus() {
    if (state.destroyed || state.mutating) return;
    const revision = ++state.pollRevision;
    state.pollController?.abort();
    const controller = new AbortController(); state.pollController = controller;
    try {
      const result = await api("status", { signal: controller.signal });
      if (revision !== state.pollRevision || state.destroyed) return;
      applyStatus(result);
    } catch (error) {
      if (revision !== state.pollRevision || state.destroyed || error.name === "AbortError") return;
      state.connected = false; pause(); cancelView(); clearObserved("Consulta indisponível", "O estado da memória não pôde ser confirmado.");
      text("load-title", "Estado indisponível"); text("load-message", error.message);
      text("resident-size", "—"); text("series-count", "—");
      text("worker-rss", "—"); text("worker-swap", "—");
      $("status-dot").dataset.state = "OFFLINE"; updateDomainButtons(); syncTimeline();
      syncEventAccess();
    } finally {
      if (revision === state.pollRevision) {
        state.pollController = null;
        schedulePoll(["LOADING", "RELEASING"].includes(state.snapshot?.status) && state.connected ? 750 : 3000);
      }
    }
  }
  function applyStatus(snapshot) {
    if (!STATES.has(snapshot.status) || !Array.isArray(snapshot.series)) throw new Error("É necessário um estado válido com a lista de séries.");
    const previousDomain = state.snapshot?.domain;
    const previousStatus = state.snapshot?.status;
    const loadChanged = (snapshot.load_id != null && state.snapshot?.load_id !== snapshot.load_id) ||
      (snapshot.generation != null && state.snapshot?.generation !== snapshot.generation);
    const wasConnected = state.connected;
    state.snapshot = snapshot; state.connected = true;
    state.series = snapshot.series.filter((series) => series && typeof series.id === "string");
    $("status-dot").dataset.state = snapshot.status;
    $("memory-bar").setAttribute("aria-busy", String(["LOADING", "RELEASING"].includes(snapshot.status) || state.mutating));
    const labels = { IDLE: "Memória disponível", LOADING: "Carregando domínio em RAM", READY: "Domínio residente", PARTIAL: "Domínio parcialmente carregado", FAILED: "Falha no carregamento", RELEASING: "Liberando memória residente" };
    text("load-title", labels[snapshot.status]);
    text("load-message", content(snapshot.message, snapshot.status === "IDLE" ? "Escolha um domínio para começar." : "Estado informado pelo servidor."));
    text("series-count", count(state.series.length)); text("series-badge", count(state.series.length));
    text("resident-size", bytes(snapshot.resident_bytes));
    text("worker-rss", bytes(snapshot.worker_rss_bytes)); text("worker-swap", bytes(snapshot.worker_swap_bytes));
    text("quality-note", snapshot.mask_policy === "QUALITY_ARRAYS_LOADED_NOT_AUTOMATICALLY_APPLIED" ? "Política DQ: máscaras carregadas não são aplicadas automaticamente ao sinal." : "Máscaras DQ: aplicação ao sinal não confirmada pelo servidor.");
    text("load-count", `${count(snapshot.loaded_files)} / ${count(snapshot.total_files)} arquivos`);
    const progressKnown = finite(snapshot.loaded_files) && finite(snapshot.total_files) && snapshot.total_files > 0;
    const progress = progressKnown ? clamp(snapshot.loaded_files / snapshot.total_files * 100, 0, 100) : 0;
    text("load-percent", progressKnown ? `${number(progress, 0)}%` : "—");
    if (snapshot.status === "LOADING" && !progressKnown) $("load-progress").removeAttribute("value");
    else $("load-progress").value = progress;
    const errors = Array.isArray(snapshot.errors) ? snapshot.errors : [];
    $("load-errors").hidden = !errors.length;
    text("load-errors-summary", `${errors.length} falha(s) no carregamento`);
    $("load-error-list").replaceChildren(...errors.map((error) => node("li", "", `${content(error?.name, "Arquivo não informado")}: ${content(error?.error)}`)));
    const signature = JSON.stringify(state.series);
    const changed = signature !== state.seriesSignature || previousDomain !== snapshot.domain || loadChanged;
    if (changed) {
      state.seriesSignature = signature;
      if (previousDomain !== snapshot.domain) state.userSelected = false;
      const selected = previousDomain === snapshot.domain ? state.series.find((series) => series.id === state.selected?.id) : null;
      const preferred = state.series.find((series) => finite(series.finite_fraction) && series.finite_fraction > 0.9);
      const next = (state.userSelected && selected) || preferred || selected || state.series[0] || null;
      selectSeries(next, Boolean(next && selected && next.id === selected.id));
    } else if (!wasConnected && state.selected) { syncTimeline(); queueView(); }
    updateDomainButtons(); syncTimeline();
    if (snapshot.status === "LOADING") {
      awaitCompleteLoad();
    } else if (["IDLE", "RELEASING", "FAILED"].includes(snapshot.status) && previousStatus !== snapshot.status) {
      pause(); cancelView(); clearObserved(labels[snapshot.status], content(snapshot.message, "Aguardando um domínio disponível."));
    } else if (canView() && (previousStatus === "LOADING" || (!observedPlot.data && !state.viewController && !state.viewTimer))) queueView();
    syncEventAccess();
  }
  async function mutateMemory(operation, body) {
    if (state.mutating || !state.connected || state.snapshot?.status === "RELEASING" || (operation === "load" && state.snapshot?.status === "LOADING")) return;
    state.mutating = true; cancelPoll(); pause(); cancelView();
    syncEventAccess();
    updateDomainButtons(); syncTimeline();
    $("memory-bar").setAttribute("aria-busy", "true");
    text("load-title", operation === "load" ? "Solicitando carga do domínio…" : "Liberando memória…");
    text("load-message", "Aguardando confirmação do servidor.");
    clearObserved("Atualizando memória", "A janela será consultada após a confirmação do estado.");
    try {
      const result = await api(operation, { method: "POST", body, timeout: 60000 });
      if (Array.isArray(result.series) && STATES.has(result.status)) applyStatus(result);
      else text("load-message", content(result.message, "Pedido recebido. Consultando estado…"));
    } catch (error) {
      // Never retry a mutation whose outcome may be uncertain; reconcile by GET.
      text("load-title", "Pedido sem confirmação");
      text("load-message", `${error.message} O estado será consultado; o pedido não foi repetido.`);
      state.connected = false;
    } finally {
      state.mutating = false; updateDomainButtons(); syncTimeline(); schedulePoll();
    }
  }

  function renderSeries() {
    const query = $("series-search").value.trim().toLocaleLowerCase("pt-BR");
    const items = state.series.filter((series) => `${series.name} ${series.detector}`.toLocaleLowerCase("pt-BR").includes(query))
      .sort((a, b) => Number(finite(b.finite_fraction) && b.finite_fraction > 0.9) - Number(finite(a.finite_fraction) && a.finite_fraction > 0.9));
    const fragment = document.createDocumentFragment();
    for (const series of items) {
      const button = node("button", "series-button"); button.type = "button";
      button.setAttribute("aria-pressed", String(series.id === state.selected?.id));
      button.append(node("strong", "", content(series.name, series.id)));
      const meta = node("span", "series-meta");
      meta.append(node("span", "detector-tag", content(series.detector, "Detector —")), node("span", "", seconds(series.duration_s)));
      button.append(meta);
      button.append(node("span", "series-meta", `Valores finitos · ${percent(series.finite_fraction)}`));
      button.title = `${count(series.rows)} amostras · fração finita ${percent(series.finite_fraction)}`;
      button.addEventListener("click", () => { state.userSelected = true; selectSeries(series); }); fragment.append(button);
    }
    if (!items.length) fragment.append(node("p", "empty-copy", state.series.length ? "Nenhuma série corresponde à busca." : "Carregue um domínio para trazer suas séries para a memória."));
    $("series-list").replaceChildren(fragment);
  }
  function selectSeries(series, preserveWindow = false) {
    pause(); cancelView(); state.selected = series;
    if (!preserveWindow) { state.start = 0; state.duration = series && finite(series.duration_s) ? Math.min(1, series.duration_s) : 1; }
    text("selected-name", series ? content(series.name, series.id) : "Nenhuma série selecionada");
    text("selected-detector", series ? content(series.detector, "—") : "—");
    text("selected-dt", seconds(series?.dt_s)); text("selected-duration", seconds(series?.duration_s));
    text("selected-gps", finite(series?.gps_start) ? decimal.format(series.gps_start) : "—");
    renderSeries(); syncTimeline();
    if (state.snapshot?.status === "LOADING") awaitCompleteLoad();
    else clearObserved(series ? "Consultando a série residente…" : "O sinal começa na fonte.", series ? "Preparando o envelope mínimo e máximo." : "Carregue um domínio e selecione uma série.");
    if (canView()) queueView();
  }
  function canView() {
    return state.connected && !state.mutating && ["READY", "PARTIAL"].includes(state.snapshot?.status) && state.selected && finite(state.selected.duration_s) && state.selected.duration_s > 0;
  }
  function awaitCompleteLoad() {
    pause(); cancelView();
    clearObserved("Aguardando carga completa", "A visualização iniciará automaticamente quando a carga terminar em READY ou PARTIAL.");
    text("view-state", "Aguardando carga completa");
  }
  function minDuration() {
    return Math.min(state.selected?.duration_s || 1, finite(state.selected?.dt_s) && state.selected.dt_s > 0 ? state.selected.dt_s : 0.000001);
  }
  function maxStart() { return Math.max(0, (state.selected?.duration_s || 0) - state.duration); }
  function syncTimeline() {
    const enabled = Boolean(canView());
    $("timeline-controls").disabled = !enabled;
    if (!state.selected || !finite(state.selected.duration_s) || state.selected.duration_s <= 0) return;
    state.duration = clamp(state.duration, minDuration(), state.selected.duration_s);
    state.start = clamp(state.start, 0, maxStart());
    $("time-scrub").max = String(maxStart()); $("time-scrub").value = String(state.start);
    $("time-scrub").disabled = maxStart() === 0;
    $("time-scrub").setAttribute("aria-valuetext", `${seconds(state.start)} desde o início do arquivo`);
    $("window-start").max = String(maxStart());
    if (document.activeElement !== $("window-start")) $("window-start").value = String(state.start);
    $("window-duration").min = String(minDuration()); $("window-duration").max = String(state.selected.duration_s);
    if (document.activeElement !== $("window-duration")) $("window-duration").value = String(state.duration);
    $("play-toggle").disabled = !enabled || maxStart() === 0;
    text("scrub-position", seconds(state.start)); text("scrub-end", seconds(state.selected.duration_s));
    text("window-end", seconds(state.start + state.duration));
    text("window-gps", finite(state.selected.gps_start) ? `GPS inicial da janela ${decimal.format(state.selected.gps_start + state.start)}` : "GPS não informado");
  }
  function pause() {
    state.playing = false; state.lastAdvance = 0;
    text("play-label", "Reproduzir"); text("play-symbol", "▶"); $("play-toggle").setAttribute("aria-pressed", "false");
  }
  function cancelView() {
    state.viewRevision += 1; clearTimeout(state.viewTimer); state.viewTimer = null; state.viewController?.abort(); state.viewController = null;
  }
  function clearObserved(title, description) {
    observedPlot.clear(); $("observed-empty").hidden = false;
    $("observed-empty").querySelector("strong").textContent = title;
    $("observed-empty").querySelector("p").textContent = description;
    text("view-state", "Sem janela carregada"); text("chart-readout", "Passe sobre o gráfico para inspecionar tempo, mínimo e máximo.");
    for (const id of ["read-source", "disk-reads", "window-rows", "finite-fraction", "view-elapsed"]) text(id, "—");
    text("gap-coverage", "Cada traço preserva o mínimo e o máximo do intervalo. Lacunas nulas permanecem abertas; não há ligação entre bins. Escala vertical automática.");
  }
  function queueView(delay = 0) {
    cancelView();
    if (!canView() || state.destroyed) return;
    const revision = state.viewRevision;
    const wait = Math.max(delay, FRAME_MS - (performance.now() - state.lastViewAt), 0);
    state.viewTimer = setTimeout(() => fetchView(revision), wait);
  }
  async function fetchView(revision) {
    state.viewTimer = null;
    if (revision !== state.viewRevision || !canView() || state.destroyed) return;
    // Recheck the clock: timers can fire early. All /view calls share this limiter.
    const remaining = FRAME_MS - (performance.now() - state.lastViewAt);
    if (remaining > 0) { state.viewTimer = setTimeout(() => fetchView(revision), Math.ceil(remaining)); return; }
    if (state.playing) {
      const now = performance.now();
      if (state.lastAdvance) state.start = Math.min(maxStart(), state.start + (now - state.lastAdvance) / 1000 * state.speed);
      state.lastAdvance = now; syncTimeline();
    }
    const selected = state.selected;
    const start = state.start; const duration = state.duration;
    const bins = Math.round(clamp(observedPlot.width * (window.devicePixelRatio || 1), 128, 1600));
    const parameters = new URLSearchParams({ id: selected.id, start_s: String(start), duration_s: String(duration), bins: String(bins) });
    const controller = new AbortController(); state.viewController = controller; state.lastViewAt = performance.now();
    text("view-state", "Consultando RAM…");
    try {
      const result = await api(`view?${parameters}`, { signal: controller.signal });
      if (revision !== state.viewRevision || state.destroyed || state.selected?.id !== selected.id) return;
      if (result.id !== selected.id || !Array.isArray(result.points) || !finite(result.start_s) || !finite(result.duration_s) || result.duration_s <= 0) throw new Error("Janela inválida retornada pelo servidor.");
      for (const key of ["load_id", "generation"]) {
        if (state.snapshot?.[key] != null && result[key] != null && state.snapshot[key] !== result[key]) throw new Error("A janela pertence a outra geração de carga. Aguardando o estado atual da memória.");
      }
      if (result.read_source !== "RESIDENT_RAM" || result.data_reads_since_load !== 0) throw new Error("O servidor não confirmou o strain residente em RAM, sem novas leituras de strain.");
      observedPlot.setData(result);
      const hasData = result.points.some((point) => observedPlot.validPoint(point));
      $("observed-empty").hidden = hasData;
      if (!hasData) {
        $("observed-empty").querySelector("strong").textContent = "Janela sem valores finitos.";
        $("observed-empty").querySelector("p").textContent = "A lacuna foi preservada. Navegue para outro trecho da série.";
      }
      text("read-source", "RAM residente"); text("disk-reads", "0");
      text("window-rows", `${count(result.window_rows)} / ${count(result.total_rows)}`);
      text("finite-fraction", percent(result.window_finite_fraction)); text("view-elapsed", `${number(result.elapsed_ms, 1)} ms`);
      text("view-state", `${seconds(result.start_s)} → ${seconds(result.start_s + result.duration_s)}`);
      text("chart-readout", `${content(result.units?.y, "Unidade não informada")} · segundos relativos ao início GPS ${number(result.gps_start, 3)} · envelope mínimo/máximo · ${bytes(result.resident_bytes)} residentes`);
      const fractions = Array.isArray(result.valid_fraction_per_bin) ? result.valid_fraction_per_bin : null;
      const mixed = finite(result.mixed_gap_bins) ? result.mixed_gap_bins : fractions ? fractions.filter((fraction) => finite(fraction) && fraction > 0 && fraction < 1).length : null;
      text("gap-coverage", `${mixed === null ? "Cobertura por bin não informada. " : `${count(mixed)} bins com lacunas internas. `}Cada traço mostra mínimo/máximo das amostras finitas; lacunas nulas permanecem abertas. Não há ligação entre bins. Escala vertical automática.`);
      if (state.playing && state.start >= maxStart()) pause();
    } catch (error) {
      if (revision !== state.viewRevision || state.destroyed || error.name === "AbortError") return;
      pause(); clearObserved("Janela indisponível", error.message); text("view-state", "Falha de leitura");
    } finally {
      if (revision === state.viewRevision) {
        state.viewController = null;
        if (state.playing) queueView(FRAME_MS - (performance.now() - state.lastViewAt));
      }
    }
  }

  function editWindow(start, duration) {
    if (!canView() || !finite(start) || !finite(duration) || duration <= 0) return;
    pause(); state.duration = duration; state.start = start; syncTimeline();
    clearObserved("Consultando esta janela…", "Leitura do envelope residente em RAM."); queueView();
  }

  function resetModel(message = "Selecione um relógio para calcular as curvas.") {
    modelPlot.clear(); $("model-empty").hidden = false;
    $("model-empty").querySelector("strong").textContent = $("model-reading").value ? "Preparando a leitura condicional." : "Escolha o relógio da leitura.";
    $("model-empty").querySelector("p").textContent = message;
    text("model-status", message); $("model-status").dataset.error = "false";
    for (const id of ["prediction-frequency", "prediction-tau", "prediction-mass", "model-beta"]) text(id, "—");
    for (const id of ["prediction-gamma", "prediction-x", "prediction-delta-tau", "prediction-qnm-mode", "prediction-qnm-method"]) text(id, "Indisponível");
    text("model-source-path", "Aguardando fonte da nova resposta."); text("model-source-hash", "SHA-256 não recebido");
    text("model-scope", "Aguardando resposta"); text("model-time-reference", "Aguardando resposta");
    text("prediction-scope", "Modelo condicional de ensemble. Não constitui ajuste ao evento nem estimativa de significância.");
  }
  function cancelModel() {
    state.modelRevision += 1; clearTimeout(state.modelTimer); state.modelController?.abort(); state.modelController = null;
    $("model-chart").setAttribute("aria-busy", "false");
  }
  function applyRegimePreset(search) {
    const preset = regimePreset(search);
    if (!preset) return false;
    cancelModel();
    for (const [id, value] of Object.entries(preset.controls)) $(id).value = String(value);
    text("model-regime-name", preset.title);
    $("model-regime-banner").hidden = false;
    const hasReading = READINGS.has($("model-reading").value);
    $("model-submit").disabled = !hasReading;
    resetModel(hasReading ? "Cenário preparado. Calcule as curvas com o relógio selecionado." : "Cenário preparado. Selecione explicitamente o relógio condicional.");
    return true;
  }
  function modelParameters() {
    const reading = $("model-reading").value;
    if (!READINGS.has(reading)) throw new Error("Selecione explicitamente um relógio condicional.");
    const body = { reading };
    const mapping = { mass_source_solar: "model-mass", spin: "model-spin", redshift: "model-redshift", amplitude: "model-amplitude", phase: "model-phase", duration_s: "model-duration" };
    for (const [key, id] of Object.entries(mapping)) {
      const input = $(id); const value = input.valueAsNumber;
      if (!input.checkValidity() || !finite(value)) throw new Error("Preencha os parâmetros com números válidos nos intervalos indicados.");
      body[key] = value;
    }
    return body;
  }
  function modelEdited() {
    cancelModel();
    const reading = $("model-reading").value;
    $("model-submit").disabled = !READINGS.has(reading);
    text("clock-note", reading === "R-A" ? "[INPUT] R-A · relógio Planck. Hipótese explícita no executor atual." : reading === "R-B" ? "[INPUT] R-B · relógio massa. Hipótese explícita no executor atual." : reading ? `${reading} · leitura condicional solicitada. Escopo e referência dependem da resposta do executor.` : "Nenhum relógio foi assumido. R-A e R-B são entradas do executor atual; as demais leituras dependem de seu suporte.");
    resetModel(reading ? "Aguardando o fim da edição…" : "Aguardando seleção explícita do relógio.");
    if (!READINGS.has(reading)) return;
    try { modelParameters(); }
    catch (error) { text("model-status", error.message); return; }
    const revision = state.modelRevision;
    state.modelTimer = setTimeout(() => fetchModel(revision), MODEL_DELAY_MS);
  }
  async function fetchModel(revision) {
    if (revision !== state.modelRevision || state.destroyed) return;
    let body;
    try { body = modelParameters(); }
    catch (error) { text("model-status", error.message); return; }
    const controller = new AbortController(); state.modelController = controller;
    $("model-submit").disabled = true; $("model-chart").setAttribute("aria-busy", "true");
    text("model-status", "Calculando a leitura condicional…");
    try {
      const result = await api("model", { method: "POST", body, signal: controller.signal });
      if (revision !== state.modelRevision || state.destroyed) return;
      if (result.scope !== "CONDITIONAL_ENSEMBLE_NOT_EVENT_FIT") throw new Error("O executor não confirmou o escopo condicional de ensemble.");
      if (!Array.isArray(result.time_s) || !Array.isArray(result.gr) || !Array.isArray(result.tgl) || result.time_s.length < 2 || result.gr.length !== result.time_s.length || result.tgl.length !== result.time_s.length) throw new Error("As curvas recebidas têm dimensões inválidas.");
      let previous = -Infinity; let validTimes = 0;
      for (const time of result.time_s) {
        if (time === null) continue;
        if (!finite(time) || time <= previous) throw new Error("Eixo temporal do modelo inválido.");
        previous = time; validTimes += 1;
      }
      if (validTimes < 2) throw new Error("O modelo não retornou um intervalo temporal válido.");
      for (const key of ["gr", "tgl"]) {
        if (!result[key].some((value, index) => finite(value) && finite(result.time_s[index]))) throw new Error(`A curva ${key.toUpperCase()} não contém valores finitos.`);
        if (result[key].some((value) => value !== null && !finite(value))) throw new Error("O modelo contém valores inválidos.");
      }
      modelPlot.setData(result); $("model-empty").hidden = true;
      const prediction = result.prediction || {};
      text("prediction-frequency", `${number(prediction.f_gr_hz, 3)} Hz`); text("prediction-tau", seconds(prediction.tau_gr_s));
      text("prediction-gamma", modelMetric(prediction.gamma_per_s, " s⁻¹")); text("prediction-mass", `${number(result.mass_detector_solar, 3)} M☉`);
      // These dimensionless metrics are supplied by the executor, never derived here.
      text("prediction-x", modelMetric(prediction.x));
      text("prediction-delta-tau", modelMetric(prediction.delta_tau_ensemble_exact));
      text("prediction-qnm-mode", qnmMode(prediction.mode));
      text("prediction-qnm-method", typeof prediction.qnm_method === "string" && prediction.qnm_method.trim() ? prediction.qnm_method : "Indisponível");
      text("model-beta", number(prediction.beta_runtime, 16));
      text("model-source-path", content(result.source?.path, "Caminho da fonte não informado pelo executor."));
      text("model-source-hash", result.source?.sha256 ? `SHA-256 · ${content(result.source.sha256)}` : "SHA-256 não informado pelo executor");
      text("model-scope", `${result.scope} · ${content(prediction.scope, "Escopo da previsão não informado")}`);
      text("model-time-reference", reference(result.time_reference));
      text("prediction-scope", `Modelo condicional de ensemble, sem ajuste ao evento ou estimativa de significância. ${content(prediction.scope, "")}`);
      text("model-status", `${body.reading} · ${count(result.time_s.length)} pontos por curva · resposta do executor`);
      $("model-status").dataset.error = "false";
    } catch (error) {
      if (revision !== state.modelRevision || state.destroyed || error.name === "AbortError") return;
      resetModel(error.message); $("model-empty").querySelector("strong").textContent = "Leitura condicional indisponível.";
      $("model-status").dataset.error = "true";
    } finally {
      if (revision === state.modelRevision) {
        state.modelController = null; $("model-submit").disabled = !READINGS.has($("model-reading").value);
        $("model-chart").setAttribute("aria-busy", "false");
      }
    }
  }

  function eventReady() {
    return Boolean(state.connected && !state.mutating && !state.eventMetadataLoading && state.eventMetadata &&
      ["READY", "PARTIAL"].includes(state.snapshot?.status) && state.snapshot?.domain === "gw_strain");
  }
  function eventWaitReason() {
    if (state.eventMetadataLoading) return "Consultando a referência de GW250114…";
    if (!state.eventMetadata) return "Aguardando referência válida do evento.";
    if (!state.connected) return "Aguardando confirmação do estado da memória.";
    if (state.mutating || state.snapshot?.status === "RELEASING") return "Memória em transição; sobreposição suspensa.";
    if (!["READY", "PARTIAL"].includes(state.snapshot?.status) || state.snapshot?.domain !== "gw_strain") return "Aguardando ondas gravitacionais em READY ou PARTIAL. A consulta fica bloqueada durante LOADING.";
    const partial = state.snapshot.status === "PARTIAL" ? "Carga parcial: o evento depende do par residente validado por hashes e DQ. " : "";
    if (!READINGS.has($("event-reading").value)) return `${partial}Selecione explicitamente o relógio do evento.`;
    if (partial) return `${partial}Pronto para solicitar a validação ao executor.`;
    return "Parâmetros prontos para uma leitura exploratória.";
  }
  function showEventLoadStatus(status) {
    text("event-domain-status", status === "PARTIAL" ? "PARTIAL · carga parcial" : status === "READY" ? "READY · domínio residente" : content(status, "Estado não confirmado"));
    $("event-load-note").hidden = status !== "PARTIAL";
  }
  function showEventGate(gate) {
    text("event-gate-status", content(gate?.status, "Gate não informado"));
    text("event-gate-reason", content(gate?.reason, "Motivo não informado pelo executor."));
  }
  function cancelEvent() {
    state.eventRevision += 1; clearTimeout(state.eventTimer); state.eventTimer = null;
    state.eventController?.abort(); state.eventController = null;
    $("event-panel").setAttribute("aria-busy", "false");
  }
  function clearEvent(message) {
    state.eventResult = null; state.eventResultLabel = "";
    for (const detector of ["H1", "L1"]) {
      eventPlots[detector].overlay.clear(); eventPlots[detector].residual.clear();
      const empty = $(`event-${detector}-empty`); empty.hidden = false;
      empty.querySelector("strong").textContent = `Aguardando dados de ${detector}.`;
      empty.querySelector("p").textContent = message;
      text(`event-${detector}-quality`, "DQ e injeções: aguardando verificação desta janela.");
      $(`event-${detector}-quality`).dataset.error = "false";
      $(`event-${detector}-noise`).hidden = true;
      $(`event-${detector}-view-error`).hidden = true;
      text(`event-${detector}-time`, `Tempo relativo ao pico ${detector}; origem do modelo aguardando resposta.`);
      for (const suffix of ["dq", "injections", "gps", "source", "hash"]) text(`event-${detector}-${suffix}`, "—");
    }
    text("event-status", message); $("event-status").dataset.error = "false";
    for (const id of ["event-read-source", "event-disk-reads", "event-elapsed"]) text(id, "—");
    for (const id of ["event-scope", "event-source", "event-normalization", "event-assumptions", "event-parameters", "event-prediction"]) text(id, "Aguardando resposta.");
    updateEventDisplayLabels();
  }
  function syncEventAccess() {
    const snapshot = state.snapshot;
    const key = JSON.stringify([state.connected, state.mutating, state.eventMetadataLoading, Boolean(state.eventMetadata),
      snapshot?.status, snapshot?.domain, snapshot?.load_id, snapshot?.generation]);
    $("event-fields").disabled = !state.eventMetadata || state.eventMetadataLoading;
    $("event-submit").disabled = !eventReady() || !READINGS.has($("event-reading").value) || Boolean(state.eventController);
    if (key === state.eventAccessKey) return;
    state.eventAccessKey = key; state.eventLoadIdentity = null;
    showEventLoadStatus(state.connected ? snapshot?.status : null);
    cancelEvent(); clearEvent(eventWaitReason());
    if (eventReady() && READINGS.has($("event-reading").value)) eventEdited();
  }
  async function loadEventMetadata() {
    const revision = ++state.eventMetadataRevision;
    state.eventMetadataController?.abort();
    const controller = new AbortController(); state.eventMetadataController = controller;
    state.eventMetadataLoading = true; $("event-refresh").disabled = true;
    text("event-metadata-status", "Consultando a referência do evento; esta operação independe da RAM.");
    syncEventAccess();
    try {
      const result = await api("event", { signal: controller.signal });
      if (revision !== state.eventMetadataRevision || state.destroyed) return;
      if (result.event !== "GW250114_082203" || result.samples !== 410 || result.sample_rate_hz !== 2048 ||
          !Array.isArray(result.starts_tm) || !result.starts_tm.length || !result.starts_tm.every((value) => finite(value) && value > 0) ||
          !result.starts_tm.includes(result.primary_start_tm) || !finite(result.reference_tM_seconds) || result.reference_tM_seconds <= 0 ||
          !finite(result.reference_mass_detector_solar) || result.reference_mass_detector_solar <= 0 ||
          !finite(result.redshift) || result.redshift < 0 || !["H1", "L1"].every((detector) => finite(result.reference_peak_gps?.[detector]))) {
        throw new Error("Referência incompatível com GW250114 e sua janela fixa de 410 amostras a 2048 Hz.");
      }
      state.eventMetadata = result;
      const previousStart = $("event-start").value;
      $("event-start").replaceChildren(...result.starts_tm.map((value) => {
        const option = node("option", "", `${number(value)} tM${value === result.primary_start_tm ? " · primário" : ""}`);
        option.value = String(value); return option;
      }));
      $("event-start").value = previousStart && result.starts_tm.includes(Number(previousStart)) ? previousStart : String(result.primary_start_tm);
      if (!state.eventDefaultsSet) {
        $("event-redshift").value = String(result.redshift);
        $("event-mass").value = String(result.reference_mass_detector_solar / (1 + result.redshift));
        state.eventDefaultsSet = true;
      }
      text("event-window-spec", `${count(result.samples)} amostras / ${count(result.sample_rate_hz)} Hz · duração nominal ${seconds(result.samples / result.sample_rate_hz)}`);
      text("event-reference-tm", seconds(result.reference_tM_seconds));
      text("event-reference-mass", `${number(result.reference_mass_detector_solar, 6)} M☉`);
      for (const detector of ["H1", "L1"]) text(`event-peak-${detector}`, decimal.format(result.reference_peak_gps[detector]));
      text("event-provenance", content(result.provenance)); showEventGate(result.physical_gate);
      text("event-metadata-status", "Referência recebida. O início em tM e a janela são definidos por essa referência; editar massa ou redshift altera o modelo solicitado.");
      $("event-metadata-status").classList.remove("error");
    } catch (error) {
      if (revision !== state.eventMetadataRevision || state.destroyed || error.name === "AbortError") return;
      state.eventMetadata = null; showEventGate(null);
      text("event-metadata-status", `Referência indisponível: ${error.message}`); $("event-metadata-status").classList.add("error");
    } finally {
      if (revision === state.eventMetadataRevision && !state.destroyed) {
        state.eventMetadataController = null; state.eventMetadataLoading = false; $("event-refresh").disabled = false; syncEventAccess();
      }
    }
  }
  function eventParameters() {
    const reading = $("event-reading").value;
    if (!READINGS.has(reading)) throw new Error("Selecione explicitamente o relógio do evento.");
    const numeric = (id) => {
      const input = $(id); const value = input.valueAsNumber;
      if (!input.checkValidity() || !finite(value)) throw new Error("Preencha os parâmetros do evento com números válidos nos intervalos indicados.");
      return value;
    };
    const start_tm = Number($("event-start").value);
    if (!state.eventMetadata?.starts_tm.includes(start_tm)) throw new Error("Selecione um início da grade pré-registrada.");
    return { start_tm, reading, mass_source_solar: numeric("event-mass"), spin: numeric("event-spin"), redshift: numeric("event-redshift"),
      detectors: Object.fromEntries(["H1", "L1"].map((detector) => [detector, { amplitude: numeric(`event-${detector}-amplitude`), phase: numeric(`event-${detector}-phase`) }])) };
  }
  function eventEdited() {
    cancelEvent();
    const reading = $("event-reading").value;
    text("event-clock-note", reading === "R-A" ? "[INPUT] R-A · relógio Planck, selecionado explicitamente." : reading === "R-B" ? "[INPUT] R-B · relógio massa, selecionado explicitamente." : reading ? `${reading} · leitura condicional; o executor determina o escopo.` : "Nenhum relógio foi assumido. R-A e R-B são entradas do executor atual.");
    $("event-submit").disabled = !eventReady() || !READINGS.has(reading);
    clearEvent(eventWaitReason());
    if (!eventReady() || !READINGS.has(reading)) return;
    try { eventParameters(); }
    catch (error) { text("event-status", error.message); return; }
    text("event-status", "Aguardando o fim da edição…");
    const revision = state.eventRevision;
    state.eventTimer = setTimeout(() => fetchEvent(revision), MODEL_DELAY_MS);
  }
  function validateEventChannel(channel, metadata) {
    if (channel.quality?.passed !== true) return;
    if (channel.units?.y !== "strain" || channel.units?.x !== "s from detector reference peak") throw new Error(`${channel.detector}: unidades incompatíveis com strain e tempo desde o pico.`);
    const keys = ["time_s", "strain", "gr", "tgl", "residual_gr", "residual_tgl"];
    if (keys.some((key) => !Array.isArray(channel[key]) || channel[key].length !== metadata.samples)) throw new Error(`${channel.detector}: a janela deve conter exatamente ${metadata.samples} amostras em cada array.`);
    for (const key of keys) if (channel[key].some((value) => value !== null && !finite(value))) throw new Error(`${channel.detector}: valores inválidos no array ${key}.`);
    for (let i = 0; i < channel.time_s.length; i += 1) {
      if (!finite(channel.time_s[i]) || (i && Math.abs(channel.time_s[i] - channel.time_s[i - 1] - 1 / metadata.sample_rate_hz) > 1e-8)) throw new Error(`${channel.detector}: eixo temporal incompatível com a amostragem da referência.`);
    }
    if (!["strain", "gr", "tgl"].every((key) => channel[key].some(finite))) throw new Error(`${channel.detector}: uma das curvas não contém valores finitos.`);
    if (!finite(channel.model_time_origin_s)) throw new Error(`${channel.detector}: origem temporal do modelo não informada.`);
  }
  function updateEventDisplayLabels() {
    const normalized = $("event-display").value === "normalized";
    const unit = normalized ? "adimensional" : "strain";
    const xLabel = normalized ? "Índice da amostra de referência (0–409; Δt=1/2048 s)" : "Tempo desde o pico de referência · s";
    text("event-display-unit", normalized ? "Coordenada transformada · adimensional" : "Bruto · strain");
    text("event-display-note", normalized ? "Branqueamento simétrico do intervalo; remove direções polinomiais da análise registrada. Mesma transformação aplicada às três curvas. Não há reconstrução de sinal." : "Arrays brutos de strain retornados pelo executor, com os modelos nas mesmas unidades. A troca de visualização não modifica os dados originais nem os parâmetros.");
    text("event-time-note", normalized ? "410 coordenadas transformadas, posto ≤407: não são 410 dados independentes. Cada componente mistura amostras de modo não local; não é o valor observado naquele instante físico. O índice identifica a grade original; Δt e GPS servem apenas à indexação. Não há reconstrução de sinal." : "Os eixos usam segundos desde o pico de referência de cada detector. O início é expresso em tM de referência; a janela mantém 410 amostras a 2048 Hz. A origem temporal de cada modelo vem do executor, sem deslocamento adicional pela interface.");
    for (const detector of ["H1", "L1"]) {
      text(`event-${detector}-residual-units`, `GR / TGL · ${unit}`);
      $(`event-${detector}-axes`).parentElement.setAttribute("aria-label", `${detector}: dado, GR e TGL · ${normalized ? "coordenadas transformadas adimensionais, mistura não local" : "strain bruto"}. ${xLabel}.`);
      $(`event-${detector}-residual`).parentElement.setAttribute("aria-label", `${detector}: resíduos em eixo separado · ${unit}. ${xLabel}${normalized ? "; transformação não local" : ""}.`);
      if (!state.eventResult) text(`event-${detector}-time`, normalized ? "Indexação da grade original: 0–409, Δt=1/2048 s; GPS aguardando a fonte. A transformação é não local." : `Tempo relativo ao pico ${detector}; origem do modelo aguardando resposta.`);
    }
  }
  function eventDisplayData(channel) {
    if ($("event-display").value === "raw") return { ...channel, displayMode: "raw" };
    if (channel.normalization?.units !== "dimensionless" || channel.normalization?.method !== "RIGHT_POLAR_FACTOR_SQRT_W_TRANSPOSE_W" || channel.normalization?.mixes_samples_nonlocally !== true) {
      throw new Error(`${channel.detector}: a definição e as unidades da normalização não foram confirmadas pelo executor.`);
    }
    const values = channel.normalized;
    const keys = ["strain", "gr", "tgl", "residual_gr", "residual_tgl"];
    if (!values || keys.some((key) => !Array.isArray(values[key]) || values[key].length !== 410 ||
        values[key].some((value) => value !== null && !finite(value)) || !values[key].some(finite))) {
      throw new Error(`${channel.detector}: arrays normalizados ausentes ou inválidos. Para ver os dados brutos, selecione explicitamente “Bruto (strain)”.`);
    }
    // Layout only: select backend arrays unchanged. No whitening, rescaling,
    // signal reconstruction or norm computation is performed in JavaScript.
    return { displayMode: "normalized", time_s: channel.time_s.map((_, index) => index),
      ...Object.fromEntries(keys.map((key) => [key, values[key]])) };
  }
  function showEventChannel(channel) {
    const detector = channel.detector; const quality = channel.quality;
    const passed = quality?.passed === true;
    const qualityLabel = $(`event-${detector}-quality`);
    qualityLabel.dataset.error = String(!passed);
    qualityLabel.textContent = passed ? "DQ e injeções: requisitos atendidos no intervalo C6 completo, segundo o executor." : "Janela recusada: DQ/injeções não atendidos ou não confirmados. Curvas bloqueadas.";
    text(`event-${detector}-dq`, content(quality?.required_dq)); text(`event-${detector}-injections`, content(quality?.required_injections));
    text(`event-${detector}-gps`, `${finite(channel.first_sample_gps) ? decimal.format(channel.first_sample_gps) : "—"} / ${finite(channel.last_sample_gps) ? decimal.format(channel.last_sample_gps) : "—"}`);
    text(`event-${detector}-source`, content(channel.source_id)); text(`event-${detector}-hash`, content(channel.strain_array_sha256));
    const normalized = $("event-display").value === "normalized";
    text(`event-${detector}-time`, normalized ? `Indexação da grade original: primeiro GPS ${finite(channel.first_sample_gps) ? decimal.format(channel.first_sample_gps) : "não informado"}; Δt=1/2048 s. Cada coordenada transformada mistura amostras; não é um valor observado em um instante físico.` : `Eixo: segundos desde o pico ${detector}. Origem do modelo: ${seconds(channel.model_time_origin_s)} desde esse pico. Unidades: strain.`);
    const empty = $(`event-${detector}-empty`); empty.hidden = passed;
    $(`event-${detector}-view-error`).hidden = true;
    const noise = channel.noise;
    $(`event-${detector}-noise`).hidden = !passed || !noise;
    if (passed && noise) {
      text(`event-${detector}-norm-gr`, finite(noise.diagnostic_norm2_gr) && noise.diagnostic_norm2_gr >= 0 ? number(noise.diagnostic_norm2_gr, 6) : "Não informada");
      text(`event-${detector}-norm-tgl`, finite(noise.diagnostic_norm2_tgl) && noise.diagnostic_norm2_tgl >= 0 ? number(noise.diagnostic_norm2_tgl, 6) : "Não informada");
      const shape = noise.whitener_shape;
      const shapeText = Array.isArray(shape) && shape.length === 2 && shape.every((value) => Number.isInteger(value) && value > 0) ? `${count(shape[0])} coordenadas a partir de ${count(shape[1])} amostras. ` : "Dimensão do quociente não informada. ";
      text(`event-${detector}-whitener`, `${shapeText}As coordenadas misturam amostras e não formam um eixo temporal.`);
    }
    if (passed) {
      try {
        const displayData = eventDisplayData(channel);
        eventPlots[detector].overlay.setData(displayData); eventPlots[detector].residual.setData(displayData);
      } catch (error) {
        eventPlots[detector].overlay.clear(); eventPlots[detector].residual.clear(); empty.hidden = false;
        empty.querySelector("strong").textContent = `${detector} · normalizado indisponível`;
        empty.querySelector("p").textContent = "A vista bruta requer seleção explícita.";
        text(`event-${detector}-view-error`, error.message); $(`event-${detector}-view-error`).hidden = false;
        return error.message;
      }
    }
    else {
      eventPlots[detector].overlay.clear(); eventPlots[detector].residual.clear();
      empty.querySelector("strong").textContent = `${detector} · qualidade não confirmada`;
      empty.querySelector("p").textContent = `DQ exigido: ${content(quality?.required_dq)}. Injeções: ${content(quality?.required_injections)}.`;
    }
    return null;
  }
  function renderEventResult() {
    updateEventDisplayLabels();
    const result = state.eventResult;
    if (!result) return;
    const errors = result.channels.map(showEventChannel).filter(Boolean);
    const rejected = result.channels.filter((channel) => channel.quality?.passed !== true).map((channel) => channel.detector);
    if (rejected.length) errors.unshift(`Qualidade recusada/não confirmada em ${rejected.join(" e ")}. Consulte os requisitos DQ e de injeções.`);
    const mode = $("event-display").value === "normalized" ? "Normalizado pelo ruído · adimensional" : "Bruto · strain";
    text("event-status", errors.length ? errors.join(" ") : `${mode} · ${state.eventResultLabel}`);
    $("event-status").dataset.error = String(errors.length > 0);
    const normalization = { response: result.normalization ?? null,
      channels: Object.fromEntries(result.channels.map((channel) => [channel.detector, channel.normalization ?? null])) };
    text("event-normalization", content(normalization));
  }
  async function fetchEvent(revision) {
    state.eventTimer = null;
    if (revision !== state.eventRevision || state.destroyed || !eventReady()) return;
    let body;
    try { body = eventParameters(); } catch (error) { text("event-status", error.message); return; }
    const metadata = state.eventMetadata;
    const requestedLoad = { load_id: state.snapshot.load_id, generation: state.snapshot.generation };
    const controller = new AbortController(); state.eventController = controller;
    $("event-submit").disabled = true; $("event-panel").setAttribute("aria-busy", "true");
    text("event-status", "Consultando a janela fixa de H1 e L1 em RAM…");
    try {
      const result = await api("event_view", { method: "POST", body, signal: controller.signal });
      if (revision !== state.eventRevision || state.destroyed || !eventReady()) return;
      if (result.event !== metadata.event || result.scope !== "EXPLORATORY_DETECTOR_OVERLAY_NOT_C6_INFERENCE") throw new Error("O executor não confirmou o evento e o escopo exploratório da sobreposição.");
      if (!["READY", "PARTIAL"].includes(result.domain_load_status)) throw new Error("O executor não confirmou carga READY ou PARTIAL para consultar o evento.");
      if (result.load_id == null || result.generation == null) throw new Error("Identidade da carga ausente na resposta do evento.");
      for (const key of ["load_id", "generation"]) {
        if ((requestedLoad[key] != null && result[key] !== requestedLoad[key]) ||
            (state.snapshot[key] != null && result[key] !== state.snapshot[key]) ||
            (state.eventLoadIdentity?.[key] != null && result[key] !== state.eventLoadIdentity[key])) throw new Error("Resposta de outra carga/geração descartada. Aguarde o estado atual da RAM.");
      }
      if (result.data_reads_since_load !== 0) throw new Error("A resposta não confirmou ausência de novas leituras de strain.");
      if (!Array.isArray(result.channels) || result.channels.length !== 2 ||
          !["H1", "L1"].every((detector) => result.channels.filter((channel) => channel?.detector === detector).length === 1)) throw new Error("O evento deve retornar exatamente os canais H1 e L1.");
      result.channels.forEach((channel) => validateEventChannel(channel, metadata));
      state.eventLoadIdentity = { load_id: result.load_id, generation: result.generation };
      state.eventResult = result;
      state.eventResultLabel = `${body.reading} · início ${number(body.start_tm)} tM · ${count(metadata.samples)} posições por detector · sobreposição exploratória`;
      renderEventResult(); showEventGate(result.physical_gate); showEventLoadStatus(result.domain_load_status);
      text("event-read-source", "RAM residente"); text("event-disk-reads", "0"); text("event-elapsed", `${number(result.elapsed_ms, 1)} ms`);
      text("event-scope", result.scope); text("event-source", content(result.source));
      text("event-assumptions", content(result.model_assumptions));
      text("event-parameters", content(result.parameters)); text("event-prediction", content(result.prediction));
    } catch (error) {
      if (revision !== state.eventRevision || state.destroyed || error.name === "AbortError") return;
      clearEvent(`Sobreposição indisponível: ${error.message}`); $("event-status").dataset.error = "true";
      if (error.response?.physical_gate) showEventGate(error.response.physical_gate);
      if (error.response?.quality) text("event-status", `${error.message} · Qualidade: ${content(error.response.quality)}`);
    } finally {
      if (revision === state.eventRevision) {
        state.eventController = null; $("event-panel").setAttribute("aria-busy", "false");
        $("event-submit").disabled = !eventReady() || !READINGS.has($("event-reading").value);
      }
    }
  }

  $("event-refresh").addEventListener("click", loadEventMetadata);
  $("event-display").addEventListener("change", renderEventResult);
  $("event-form").addEventListener("input", eventEdited);
  $("event-form").addEventListener("submit", (event) => {
    event.preventDefault(); cancelEvent(); clearEvent(eventWaitReason()); fetchEvent(state.eventRevision);
  });
  $("event-residuals").addEventListener("change", (event) => {
    for (const detector of ["H1", "L1"]) {
      $(`event-${detector}-residual-wrap`).hidden = !event.target.checked;
      eventPlots[detector].residual.draw();
    }
  });
  $("refresh-domains").addEventListener("click", loadDomains);
  $("release-memory").addEventListener("click", () => mutateMemory("release"));
  $("series-search").addEventListener("input", renderSeries);
  $("time-scrub").addEventListener("input", (event) => editWindow(Number(event.target.value), state.duration));
  for (const id of ["window-start", "window-duration"]) {
    $(id).addEventListener("input", () => {
      const start = $("window-start").valueAsNumber; const duration = $("window-duration").valueAsNumber;
      if (!finite(start) || !finite(duration) || duration <= 0) { text("view-state", "Informe início e duração válidos."); return; }
      editWindow(start, duration);
    });
  }
  $("rewind").addEventListener("click", () => editWindow(0, state.duration));
  $("full-series").addEventListener("click", () => editWindow(0, state.selected?.duration_s));
  $("play-speed").addEventListener("change", (event) => {
    state.speed = Number(event.target.value); state.lastAdvance = performance.now();
  });
  $("play-toggle").addEventListener("click", () => {
    if (state.playing) { pause(); cancelView(); queueView(); return; }
    if (!canView() || maxStart() <= 0) return;
    if (state.start >= maxStart()) state.start = 0;
    state.playing = true; state.lastAdvance = performance.now();
    text("play-label", "Pausar"); text("play-symbol", "Ⅱ"); $("play-toggle").setAttribute("aria-pressed", "true");
    syncTimeline(); queueView();
  });
  $("observed-axes").addEventListener("pointermove", (event) => {
    const data = observedPlot.data; const r = observedPlot.rect;
    if (!data || !r) return;
    const localX = event.clientX - $("observed-axes").getBoundingClientRect().left;
    if (localX < r.left || localX > r.right) return;
    const time = data.start_s + (localX - r.left) / (r.right - r.left) * data.duration_s;
    let nearest = null; let nearestIndex = -1; let distance = Infinity;
    // Null-valued bins participate in hit testing: the tooltip must expose gaps.
    for (let index = 0; index < data.points.length; index += 1) {
      const point = data.points[index];
      if (Array.isArray(point) && finite(point[0]) && Math.abs(point[0] - time) < distance) { nearest = point; nearestIndex = index; distance = Math.abs(point[0] - time); }
    }
    if (!nearest) { text("chart-readout", "Sem amostras nesta janela."); return; }
    const gps = finite(state.selected?.gps_start) ? ` · GPS ${decimal.format(state.selected.gps_start + nearest[0])}` : "";
    const fraction = data.valid_fraction_per_bin?.[nearestIndex];
    const coverage = finite(fraction) ? ` · cobertura ${percent(fraction)}` : "";
    text("chart-readout", observedPlot.validPoint(nearest) ? `t ${seconds(nearest[0])} · mín ${number(nearest[1])} · máx ${number(nearest[2])}${coverage}${gps}` : `t ${seconds(nearest[0])} · lacuna: valores não finitos${coverage}${gps}`);
  });
  $("model-form").addEventListener("input", modelEdited);
  $("model-form").addEventListener("submit", (event) => {
    event.preventDefault(); cancelModel(); resetModel("Calculando a leitura condicional…"); fetchModel(state.modelRevision);
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { pause(); cancelView(); }
    else { schedulePoll(); if (canView()) queueView(); }
  });
  window.addEventListener("pagehide", () => {
    state.destroyed = true; pause(); cancelPoll(); cancelView(); cancelModel(); cancelEvent(); state.eventMetadataController?.abort();
    observedPlot.destroy(); modelPlot.destroy();
    for (const plots of Object.values(eventPlots)) { plots.overlay.destroy(); plots.residual.destroy(); }
  });
  window.addEventListener("pageshow", (event) => { if (event.persisted) window.location.reload(); });
  applyRegimePreset(window.location.search);
  loadDomains(); loadEventMetadata(); schedulePoll();
})();
