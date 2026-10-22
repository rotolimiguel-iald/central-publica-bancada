/* Local UI: backend computes cosmology; GPU draws only the requested view. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const write = (id, value) => { $(id).textContent = value; };
  const element = (tag, text) => { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; return e; };
  const fmt = (v, digits = 3) => Number.isFinite(v) ? v.toLocaleString('pt-BR', {maximumFractionDigits: digits}) : '—';
  const colors = {DM_over_rd:[.54,.89,.81,1], DH_over_rd:[.58,.72,1,1], DV_over_rd:[.93,.77,.57,1]};
  const fields = {DM_over_rd:'dm_over_rd', DH_over_rd:'dh_over_rd', DV_over_rd:'dv_over_rd'};
  const labels = {DM_over_rd:'Dₘ/r_d', DH_over_rd:'Dₕ/r_d', DV_over_rd:'Dᵥ/r_d'};
  const ids = {H0:'parameter-H0',omega_m:'parameter-omega-m',rd_mpc:'parameter-rd',w0:'parameter-w0',wa:'parameter-wa',redshift:'cursor-z'};
  let source = null, result = null, reference = null, fresh = false, saving = false, requestId = 0, controller = null, timer = null, scenarioRevision = 0;
  let z = .5, activeTab = 'distances', playing = false, lastFrame = 0, frameId = 0;
  const visible = new Set(Object.keys(fields));
  const orbit = {yaw:.6,pitch:.4,zoom:1};

  async function api(path, payload, signal) {
    const response = await fetch(path, {cache:'no-store', signal,
      ...(payload === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})});
    const body = await response.json();
    if (!response.ok || body.status === 'error') throw new Error(body.error?.message || body.error || `HTTP ${response.status}`);
    return body;
  }

  class Renderer {
    constructor(name) {
      this.canvas = $(name+'-gpu'); this.overlay = $(name+'-axes');
      this.ctx = this.overlay.getContext('2d'); this.gl = null; this.driver = 'Canvas 2D';
      this.canvas.addEventListener('webglcontextlost', event => {
        event.preventDefault(); this.gl = null; this.driver = 'WebGL perdido · fallback 2D'; draw();
      });
      this.canvas.addEventListener('webglcontextrestored', () => { this.init(); draw(); });
      this.init();
    }
    init() {
      try {
        const gl = this.canvas.getContext('webgl2', {alpha:true,antialias:true});
        if (!gl) return;
        const shader = (type, text) => { const s=gl.createShader(type);gl.shaderSource(s,text);gl.compileShader(s);
          if (!gl.getShaderParameter(s,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));return s; };
        const vs=shader(gl.VERTEX_SHADER, '#version 300 es\nin vec2 p;uniform float size;void main(){gl_Position=vec4(p,0.,1.);gl_PointSize=size;}');
        const fs=shader(gl.FRAGMENT_SHADER, '#version 300 es\nprecision highp float;uniform vec4 color;out vec4 outColor;void main(){outColor=color;}');
        const program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);
        if (!gl.getProgramParameter(program,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
        gl.deleteShader(vs);gl.deleteShader(fs);
        this.program=program;this.buffer=gl.createBuffer();this.position=gl.getAttribLocation(program,'p');
        this.color=gl.getUniformLocation(program,'color');this.size=gl.getUniformLocation(program,'size');this.gl=gl;
        const debug=gl.getExtension('WEBGL_debug_renderer_info');
        this.driver = debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : 'Identidade do dispositivo não exposta pelo navegador';
      } catch (error) { this.gl=null;this.driver='Fallback 2D: '+error.message; }
    }
    clear() {
      const rect=this.overlay.getBoundingClientRect(); if(rect.width < 1 || rect.height < 1) return false;
      this.w=rect.width;this.h=rect.height;this.dpr=Math.min(window.devicePixelRatio||1,2);
      for(const canvas of [this.canvas,this.overlay]) {
        const w=Math.round(this.w*this.dpr),h=Math.round(this.h*this.dpr);
        if(canvas.width!==w || canvas.height!==h){canvas.width=w;canvas.height=h;}
      }
      this.ctx.setTransform(this.dpr,0,0,this.dpr,0,0);this.ctx.clearRect(0,0,this.w,this.h);
      if(this.gl){this.gl.viewport(0,0,this.canvas.width,this.canvas.height);this.gl.clearColor(0,0,0,0);this.gl.clear(this.gl.COLOR_BUFFER_BIT);}
      return true;
    }
    stroke(points, color, mode='line') {
      if(!points.length)return;
      if(this.gl){const gl=this.gl;gl.useProgram(this.program);gl.bindBuffer(gl.ARRAY_BUFFER,this.buffer);
        gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(points.flat()),gl.DYNAMIC_DRAW);gl.enableVertexAttribArray(this.position);
        gl.vertexAttribPointer(this.position,2,gl.FLOAT,false,0,0);gl.uniform4fv(this.color,color);gl.uniform1f(this.size,6*this.dpr);
        gl.drawArrays(mode==='points'?gl.POINTS:mode==='segments'?gl.LINES:gl.LINE_STRIP,0,points.length);
      }else{const c=this.ctx;c.strokeStyle=`rgba(${color.slice(0,3).map(x=>Math.round(x*255)).join(',')},${color[3]})`;c.fillStyle=c.strokeStyle;
        c.beginPath();points.forEach(([x,y],i)=>{x=(x+1)*this.w/2;y=(1-y)*this.h/2;
          if(mode==='points'){c.fillRect(x-3,y-3,6,6);}else if(i===0 || (mode==='segments' && i%2===0))c.moveTo(x,y);else c.lineTo(x,y);});c.stroke();}
    }
  }
  const distance=new Renderer('distance'), expansion=new Renderer('expansion'), difference=new Renderer('difference');
  const ndc=(r,x,y)=>[x/r.w*2-1,1-y/r.h*2];

  function drawDistances() {
    if(!distance.clear() || !result)return;
    const r=distance,c=r.ctx,w=r.w,h=r.h, l=56,right=w-25,top=18,bottom=h-40;
    const ymax=Math.max(10,...result.series.flatMap(row=>[...visible].map(type=>row[fields[type]])),
      ...result.observations.filter(row=>visible.has(row.type)).map(row=>row.observed+row.sigma),
      ...(canCompare() ? reference.evaluation.series.flatMap(row=>[...visible].map(type=>row[fields[type]])) : []))*1.12;
    const xy=(zz,v)=>ndc(r,l+zz/3*(right-l),bottom-v/ymax*(bottom-top));
    c.font='11px Segoe UI';c.fillStyle='#a0b2c3';c.strokeStyle='#283745';c.lineWidth=1;
    for(let i=0;i<=5;i++){const yy=bottom-i/5*(bottom-top);c.beginPath();c.moveTo(l,yy);c.lineTo(right,yy);c.stroke();c.fillText(fmt(ymax*i/5,1),4,yy+4);}
    for(let i=0;i<=6;i++){const zz=i*.5; const xx=l+zz/3*(right-l);c.fillText(fmt(zz,1),xx-6,bottom+22);}
    c.fillText('z',right+8,bottom+22);c.fillText('Distância / r_d',l,14);
    for(const type of visible){
      if(canCompare()){const rows=reference.evaluation.series;const dashed=[];for(let i=0;i<rows.length-1;i+=2)dashed.push(xy(rows[i].z,rows[i][fields[type]]),xy(rows[i+1].z,rows[i+1][fields[type]]));r.stroke(dashed,colors[type],'segments');}
      r.stroke(result.series.map(row=>xy(row.z,row[fields[type]])),colors[type]);
      const rows=result.observations.filter(row=>row.type===type);
      r.stroke(rows.flatMap(row=>[xy(row.z,row.observed-row.sigma),xy(row.z,row.observed+row.sigma)]),colors[type],'segments');
      r.stroke(rows.map(row=>xy(row.z,row.observed)),colors[type],'points');}
    r.stroke([xy(z,0),xy(z,ymax)],[.8,.84,.9,1]);
  }

  function drawExpansion() {
    if(!expansion.clear())return;
    const a=1/(1+z),r=expansion;
    const project=(x,y,zz,scale)=>{
      x*=scale;y*=scale;zz*=scale;
      const xx=x*Math.cos(orbit.yaw)-zz*Math.sin(orbit.yaw),z1=x*Math.sin(orbit.yaw)+zz*Math.cos(orbit.yaw);
      const yy=y*Math.cos(orbit.pitch)-z1*Math.sin(orbit.pitch),depth=y*Math.sin(orbit.pitch)+z1*Math.cos(orbit.pitch);
      const factor=2.2/(3.8+depth)*orbit.zoom;
      return [xx*factor*(r.h/r.w),yy*factor];
    };
    const grid=(scale,color)=>{const pts=[];for(let i=-2;i<=2;i++)for(let j=-2;j<=2;j++){
      const x=i/2,y=j/2;pts.push(project(-1,x,y,scale),project(1,x,y,scale),project(x,-1,y,scale),project(x,1,y,scale),project(x,y,-1,scale),project(x,y,1,scale));}
      r.stroke(pts,color,'segments');};
    grid(1,[.16,.22,.29,1]);grid(a,[.54,.89,.81,1]);
    const axes=[[[1.3,0,0],'x'],[[0,1.3,0],'y'],[[0,0,1.3],'z espacial']];
    r.ctx.font='12px Segoe UI';r.ctx.fillStyle='#bccddd';
    axes.forEach(([p,label])=>{const end=project(...p,1);r.stroke([project(0,0,0,1),end],[.58,.72,1,1]);r.ctx.fillText(label,(end[0]+1)*r.w/2+5,(1-end[1])*r.h/2);});
    write('diagram-scale','a = '+fmt(a,4));
  }

  function draw() {
    if(activeTab==='distances')drawDistances();else if(activeTab==='difference')drawDifference();else drawExpansion();
    const r=activeTab==='distances'?distance:activeTab==='difference'?difference:expansion;
    write('renderer-status',r.gl?'WebGL2':'Canvas 2D');$('renderer-status').title=r.driver;
    write('render-device',r.driver);
  }

  function updateCursor(value) {
    if(!source || !Number.isFinite(value))return;
    z=Math.max(source.parameters.redshift.min,Math.min(source.parameters.redshift.max,value));
    $('cursor-z').value=Number(z.toFixed(5));$('redshift-scrub').value=z;
    write('scale-factor',fmt(1/(1+z),5));write('diagram-scale','a = '+fmt(1/(1+z),4));
    if(result){
      const i=Math.min(result.series.length-2,Math.floor(z/.025)),left=result.series[i],right=result.series[i+1];
      const f=(z-left.z)/(right.z-left.z);
      const exact=Math.abs(result.cursor.z-z)<1e-8;
      const row=exact?result.cursor:Object.fromEntries(Object.values(fields).map(key=>[key,left[key]+(right[key]-left[key])*f]));
      $('cursor-metrics').replaceChildren(...Object.entries(fields).map(([type,key])=>element('span',`${labels[type]} · ${fmt(row[key],4)}`)),element('small',exact?'Cursor calculado':'Leitura interpolada para navegação'));
    }
    draw();
  }

  function memory(receipt) {
    write('memory-size','Em RAM');write('read-source',`${receipt.loaded_source_bytes} bytes de fontes · ${receipt.source_reads_since_load} novas leituras · carga ${receipt.load_id.slice(0,8)}`);
  }

  function observations(rows) {
    $('observation-rows').replaceChildren(...rows.map((row,i)=>{
      const tr=element('tr');[i+1,labels[row.type],fmt(row.z),fmt(row.observed,5),fmt(row.sigma,5),fmt(row.predicted,5),fmt(row.residual,5)].forEach(value=>tr.append(element('td',String(value))));return tr;
    }));
    write('observation-summary',`${rows.length} componentes · ordem preservada`);
  }

  function covariance() {
    const data=source.dataset,cov=data.covariance,n=cov.length,canvas=$('covariance-canvas'),ctx=canvas.getContext('2d');
    const size=canvas.width,cell=size/n;ctx.clearRect(0,0,size,size);
    const table=element('table'),thead=element('thead'),head=element('tr');head.append(element('th','#'));
    for(let j=0;j<n;j++)head.append(element('th',String(j+1)));thead.append(head);table.append(thead);const body=element('tbody');
    for(let i=0;i<n;i++){const tr=element('tr');tr.append(element('th',String(i+1)));
      for(let j=0;j<n;j++){const rho=cov[i][j]/Math.sqrt(cov[i][i]*cov[j][j]);
        ctx.fillStyle=rho>=0?`rgb(${20+50*rho},${32+190*rho},${47+155*rho})`:`rgb(${20-210*rho},${32-80*rho},${47-80*rho})`;
        ctx.fillRect(j*cell+1,i*cell+1,cell-2,cell-2);tr.append(element('td',fmt(cov[i][j],5)));}body.append(tr);
    }table.append(body);$('covariance-table-wrap').replaceChildren(table);write('covariance-size',`${n} × ${n} · completa`);
    canvas.onpointermove=event=>{const box=canvas.getBoundingClientRect();const j=Math.min(n-1,Math.floor((event.clientX-box.left)/box.width*n)),i=Math.min(n-1,Math.floor((event.clientY-box.top)/box.height*n));
      if(i<0||j<0)return;const a=data.points[i],b=data.points[j];write('covariance-readout',`#${i+1} ${labels[a.type]} z=${a.z} × #${j+1} ${labels[b.type]} z=${b.z}: ρ=${fmt(cov[i][j]/Math.sqrt(cov[i][i]*cov[j][j]),6)}`);};
  }

  function setBusy(busy) { fresh=false;$('evaluate').disabled=busy;actions();write('evaluation-state',busy?'Calculando… · curva anterior':'Avaliação pronta · parâmetros manuais'); }
  async function evaluate() {
    clearTimeout(timer);if(!source)return;
    if(!$('parameter-form').reportValidity()){fresh=false;actions();write('evaluation-state','Parâmetros inválidos · última curva preservada');return;}
    const payload={...Object.fromEntries(Object.entries(ids).map(([key,id])=>[key,Number($(id).value)])),model_id:$('model-choice').value};
    const revision=++requestId;controller?.abort();controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),60000);setBusy(true);
    try {const current=await api('/api/cosmology/evaluate',payload,controller.signal);if(revision!==requestId)return;
      compatible({evaluation:current});
      if(reference){try{compatible(reference);}catch(error){reference=null;write('scenario-status','Referência removida: '+error.message);}}
      result=current;fresh=true;syncSliders();modelDescription(result.model);comparison();actions();write('chi2-value',fmt(result.chi2.value,4));write('chi2-note','13 medidas · rᵀC⁻¹r · sem ajuste ou σ');
      write('evaluation-time',fmt(result.elapsed_ms,2)+' ms · executor');write('parameter-status','Curva atualizada com os parâmetros exibidos.');
      memory(result.memory);observations(result.observations);updateCursor(playing?z:payload.redshift);$('distance-empty').hidden=true;
      write('evaluation-receipt',JSON.stringify({parameters:result.parameters,memory:result.memory,quadrature:result.quadrature,model:result.model,engine_sha256:result.engine_sha256,engine_generation:result.engine_generation,engine_components:result.engine_components,data_hashes:result.data_hashes},null,2));
      $('connection-dot').classList.add('ready');write('connection-status','Dados residentes e cálculo disponíveis.');write('evaluation-state','Avaliação pronta · parâmetros manuais');
    }catch(error){if(revision===requestId){write('parameter-status',error.name==='AbortError'?'Consulta interrompida; última curva preservada.':error.message);write('evaluation-state','Falha · última curva preservada');$('connection-dot').classList.remove('ready');write('connection-status','Falha na avaliação atual; confira os parâmetros e o recibo da última curva.');}}
    finally{clearTimeout(timeout);if(revision===requestId)$('evaluate').disabled=false;}
  }
  const schedule=()=>{++scenarioRevision;fresh=false;actions();syncSliders();clearTimeout(timer);++requestId;controller?.abort();$('evaluate').disabled=false;timer=setTimeout(evaluate,220);write('evaluation-state','Alterações pendentes · última curva preservada');write('parameter-status','Parâmetros alterados · aguardando cálculo…');};

  async function load() {
    fresh=false;actions();++scenarioRevision;
    try {source=await api('/api/cosmology/status');if(source.schema_version!=='cosmology_background_v1')throw new Error('Contrato cosmológico não reconhecido');
      if(reference){try{compatible(reference);}catch(error){reference=null;comparison();actions();write('scenario-status','Referência removida: '+error.message);}}
      const d=source.dataset;if(d.points.length!==13 || d.covariance.length!==13)throw new Error('Vetor/covariância incompletos');
      for(const [key,id]of Object.entries(ids)){const rule=source.parameters[key];$(id).min=rule.min;$(id).max=rule.max;if(!result)$(id).value=rule.default;}
      $('parameter-fields').disabled=false;$('redshift-controls').disabled=false;$('evaluate').disabled=false;$('reset-parameters').disabled=false;
      $('redshift-scrub').min=source.parameters.redshift.min;$('redshift-scrub').max=source.parameters.redshift.max;
      write('redshift-min','z = '+source.parameters.redshift.min);write('redshift-max','z = '+source.parameters.redshift.max);write('point-count',d.n_points);write('redshift-count',d.n_distinct_redshifts);memory(source.memory);
      write('backend-status','Pronto · '+source.schema_version);write('background-assumptions','FLRW plano · matéria + energia escura CPL · z ≤ 3 · sem radiação/curvatura · r_d como entrada independente.');
      $('source-list').replaceChildren(element('p',d.release_label),element('p','Vetor SHA-256: '+d.mean_sha256),element('p','Covariância SHA-256: '+d.covariance_sha256),element('p','Cópias locais verificadas; commit remoto não conferido nesta entrega.'));
      $('redshift-stops').replaceChildren(...[...new Set(d.points.map(p=>p.z))].map(value=>{const b=element('button','z '+value);b.type='button';b.onclick=()=>{pause();updateCursor(value);schedule();};return b;}));
      installSliders();chooseModel(false);covariance();await evaluate();await refreshScenarios();
    }catch(error){write('connection-status','Indisponível: '+error.message);write('backend-status','Falha de leitura');$('parameter-fields').disabled=true;}
  }

  function pause(){playing=false;if(frameId)cancelAnimationFrame(frameId);frameId=0;lastFrame=0;$('play-expansion').setAttribute('aria-pressed','false');write('play-expansion','▶ Expandir diagrama');}
  function animate(t){frameId=0;if(!playing)return;const dt=lastFrame?Math.min(.1,(t-lastFrame)/1000):0;lastFrame=t;updateCursor(z-dt*.2*Number($('playback-speed').value));
    if(z<=source.parameters.redshift.min){pause();schedule();}else frameId=requestAnimationFrame(animate);}
  $('play-expansion').onclick=()=>{if(playing){pause();schedule();return;}if(!source)return;if(z<=source.parameters.redshift.min+.001)updateCursor(3);
    playing=true;fresh=false;actions();lastFrame=0;$('play-expansion').setAttribute('aria-pressed','true');write('play-expansion','Ⅱ Pausar diagrama');frameId=requestAnimationFrame(animate);};
  $('parameter-form').onsubmit=e=>{e.preventDefault();pause();evaluate();};
  Object.values(ids).filter(id=>id!=='cursor-z').forEach(id=>$(id).addEventListener('input',()=>{pause();schedule();}));
  for(const id of ['cursor-z','redshift-scrub'])$(id).addEventListener('input',()=>{pause();updateCursor(Number($(id).value));schedule();});
  $('reset-parameters').onclick=()=>{pause();for(const [key,id]of Object.entries(ids))$(id).value=source.parameters[key].default;chooseModel(false);evaluate();};
  $('refresh-status').onclick=load;
  for(const tab of ['distances','difference','expansion'])$('tab-'+tab).onclick=()=>{
    activeTab=tab;for(const other of ['distances','difference','expansion']){$('view-'+other).hidden=tab!==other;$('tab-'+other).setAttribute('aria-selected',String(tab===other));$('tab-'+other).tabIndex=tab===other?0:-1;}draw();};
  for(const type of Object.keys(fields)){const b=element('button',labels[type]);b.type='button';b.setAttribute('aria-pressed','true');b.onclick=()=>{if(visible.has(type))visible.delete(type);else visible.add(type);b.setAttribute('aria-pressed',String(visible.has(type)));draw();};$('curve-filters').append(b);}
  $('distance-axes').onclick=e=>{if(!result)return;const box=e.currentTarget.getBoundingClientRect();pause();updateCursor((e.clientX-box.left-56)/(box.width-81)*3);schedule();};
  const orbitCanvas=$('expansion-axes');let pointer=null;
  orbitCanvas.onpointerdown=e=>{pointer=[e.clientX,e.clientY];orbitCanvas.setPointerCapture(e.pointerId);};
  orbitCanvas.onpointermove=e=>{if(!pointer)return;orbit.yaw+=(e.clientX-pointer[0])*.008;orbit.pitch=Math.max(-1.4,Math.min(1.4,orbit.pitch+(e.clientY-pointer[1])*.008));pointer=[e.clientX,e.clientY];draw();};
  orbitCanvas.onpointerup=orbitCanvas.onpointercancel=()=>{pointer=null;};
  orbitCanvas.addEventListener('wheel',e=>{e.preventDefault();orbit.zoom=Math.max(.4,Math.min(2,orbit.zoom*Math.exp(-e.deltaY*.001)));draw();},{passive:false});
  const resetOrbit=()=>{Object.assign(orbit,{yaw:.6,pitch:.4,zoom:1});draw();};$('reset-orbit').onclick=resetOrbit;
  orbitCanvas.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-','=','Home'].includes(e.key))return;e.preventDefault();
    if(e.key==='Home')resetOrbit();else if(e.key==='ArrowLeft')orbit.yaw-=.1;else if(e.key==='ArrowRight')orbit.yaw+=.1;else if(e.key==='ArrowUp')orbit.pitch+=.1;else if(e.key==='ArrowDown')orbit.pitch-=.1;else orbit.zoom=Math.max(.4,Math.min(2,orbit.zoom*(e.key==='-'?.9:1.1)));draw();};
  new ResizeObserver(draw).observe($('distance-plot'));new ResizeObserver(draw).observe($('expansion-plot'));new ResizeObserver(draw).observe($('difference-plot'));
  document.addEventListener('visibilitychange',()=>{if(document.hidden){pause();if(result)schedule();}});
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)write('motion-note','Movimento reduzido respeitado: animação só começa ao apertar Reproduzir. Duração visual não é tempo cosmológico.');

  const modelLabels={FLAT_MATTER_CPL_BACKGROUND:'FLRW CPL',TGL_V3_TOTAL_FIXED_BETA:'TGL V3 · β fixo',V3_TOTAL_BETA_ZERO:'V3 · β zero'};
  function chooseModel(recalculate=true){
    const v3=$('model-choice').value!=='FLAT_MATTER_CPL_BACKGROUND';
    for(const [key,value]of [['w0',-1],['wa',0]]){const id=ids[key];if(v3)$(id).value=value;$(id).disabled=v3;if($(id+'-slider'))$(id+'-slider').disabled=v3;}
    syncSliders();if(recalculate){pause();schedule();}
  }
  function modelDescription(model){
    const v3=model.id!=='FLAT_MATTER_CPL_BACKGROUND';
    write('model-badge',v3?'[CONDICIONAL] '+modelLabels[model.id]:'[EXPLORATÓRIO] FLRW CPL');
    write('model-scope',v3?'Rota V3 do fluido total, reutilizada do programa. Ramo Φ = 1 + β(ρ+p)/ρ; C = 0; Λ fecha H(0) = H₀. r_d é entrada independente; CMB não executado.':'Fundo plano CPL, z ≤ 3, sem radiação. r_d como entrada independente; nenhuma previsão TGL completa neste modelo.');
    write('model-statute',model.status);
    write('background-assumptions',v3?'Radiação + matéria + Λ · w₀ = −1, wₐ = 0 · Ωm total · TCMB = 2,7255 K, N_eff = 3,046 · r_d independente.':model.domain);
    const ex=model.execution;
    $('model-values').replaceChildren(...(ex?[element('span','β = '+fmt(ex.beta,12)),element('span','ΩΛ do fecho = '+fmt(ex.omega_lambda_closed,6)),element('small',ex.beta_mode==='fixed'?'β calculado por α CODATA 2018 × √e':'Controle β = 0; mantém radiação e o mesmo fecho'),element('small',ex.background_cache_hit?'Fundo em RAM · reutilizado nesta consulta':'Fundo recalculado e mantido em RAM')]:[]));
    write('canonical-status',v3?`[DERIVED / CONDICIONAL] Motor FundoV3 pinado. ${ex ? 'Consulte β, normalização, resíduos de controle e fontes no recibo.' : ''} A face recíproca e as perturbações não são substituídas por este ramo.`:'Referência CPL exploratória; selecione TGL V3 para usar a rota de fundo do programa.');
  }
  $('model-choice').onchange=()=>chooseModel();
  const parameterLabel = p => `H₀ ${fmt(p.H0,2)} · Ωm ${fmt(p.omega_m,4)} · r_d ${fmt(p.rd_mpc,2)} · w₀ ${fmt(p.w0,3)} · wₐ ${fmt(p.wa,3)}`;
  function actions(){
    const enabled=!!result && fresh && !playing;
    $('pin-reference').disabled=!enabled;$('save-scenario').disabled=!enabled || saving;
    $('clear-reference').disabled=!reference;$('export-comparison').disabled=!enabled || !canCompare();
  }
  function compatible(snapshot){
    const d=source.dataset,ev=snapshot.evaluation;
    if(ev.schema_version!==source.schema_version || ev.dataset_id!==d.id ||
       ev.data_hashes?.mean_sha256!==d.mean_sha256 || ev.data_hashes?.covariance_sha256!==d.covariance_sha256)
      throw new Error('Fontes diferentes: comparação recusada. Carregue os parâmetros como B e recalcule.');
    if(ev.engine_sha256!==source.engine_sha256 || ev.engine_generation!==source.engine_generation)throw new Error('Versão do cálculo diferente. Carregue como B, recalcule e fixe a nova referência.');
    if(!Array.isArray(ev.series) || ev.series.length!==121 || ev.series.some((row,i)=>Math.abs(row.z-i*.025)>1e-12))
      throw new Error('Grade de comparação não reconhecida.');
  }
  function setReference(snapshot){compatible(snapshot);if(result)compatible({evaluation:result});reference=structuredClone(snapshot);comparison();actions();draw();}
  function canCompare(){try{if(!reference||!result)return false;compatible(reference);compatible({evaluation:result});return true;}catch(_){return false;}}
  function comparison(){
    write('reference-label',reference?`${reference.label} · χ² ${fmt(reference.evaluation.chi2.value,4)}`:'Nenhuma referência fixada');
    write('reference-parameters',reference?modelLabels[reference.evaluation.model.id]+' · '+parameterLabel(reference.evaluation.parameters):'Fixe a curva atual e altere os controles para explorar B.');
    write('comparison-readout',result?(canCompare()?`χ² B ${fmt(result.chi2.value,4)} · Δχ² B − A ${fmt(result.chi2.value-reference.evaluation.chi2.value,4)}`:`χ² B ${fmt(result.chi2.value,4)}`):'Aguardando cálculo');
  }
  function drawDifference(){
    if(!difference.clear())return;
    const r=difference,c=r.ctx,w=r.w,h=r.h,l=56,right=w-25,top=25,bottom=h-40;
    c.font='11px Segoe UI';c.fillStyle='#a0b2c3';
    if(!canCompare()){c.fillText('Fixe uma referência compatível com B.',l,h/2);return;}
    const type=$('difference-observable').value,key=fields[type];
    const values=result.series.map((row,i)=>row[key]-reference.evaluation.series[i][key]);
    const limit=Math.max(1e-6,...values.map(Math.abs))*1.15;
    const xy=(zz,v)=>ndc(r,l+zz/3*(right-l),bottom-(v+limit)/(2*limit)*(bottom-top));
    c.strokeStyle='#283745';
    for(let i=0;i<=4;i++){const val=limit*(i/2-1),yy=bottom-i/4*(bottom-top);c.beginPath();c.moveTo(l,yy);c.lineTo(right,yy);c.stroke();c.fillText(fmt(val,4),2,yy+4);}
    for(let i=0;i<=6;i++)c.fillText(fmt(i*.5,1),l+i/6*(right-l)-6,bottom+22);
    c.fillText(labels[type]+' · B − A',l,16);c.fillText('z',right+8,bottom+22);
    r.stroke([xy(0,0),xy(3,0)],[.58,.64,.72,1]);r.stroke(values.map((v,i)=>xy(result.series[i].z,v)),colors[type]);
    r.stroke([xy(z,-limit),xy(z,limit)],[.8,.84,.9,1]);
    const i=Math.min(119,Math.floor(z/.025)),f=(z-result.series[i].z)/.025;
    write('difference-readout',`z ${fmt(z,4)} · Δ ${labels[type]} = ${fmt(values[i]+f*(values[i+1]-values[i]),6)} · leitura interpolada. Diferença entre modelos, não resíduo dos dados.`);
  }
  function installSliders(){
    const steps={H0:.1,omega_m:.001,rd_mpc:.1,w0:.01,wa:.01};
    for(const [key,step]of Object.entries(steps)){
      const id=ids[key],sid=id+'-slider';if($(sid))continue;
      const slider=element('input');slider.type='range';slider.id=sid;slider.min=source.parameters[key].min;slider.max=source.parameters[key].max;slider.step=step;
      slider.setAttribute('aria-label',`${key}: ajuste contínuo`);$(id).insertAdjacentElement('afterend',slider);
      slider.oninput=()=>{$(id).value=slider.value;pause();schedule();};
    }syncSliders();
  }
  function syncSliders(){for(const id of Object.values(ids)){const slider=$(id+'-slider');if(slider)slider.value=$(id).value;}}
  async function exportFile(payload){
    const exported=await api('/api/cosmology/exports',payload);
    const link=element('a','Ver JSON ↗');link.href=exported.download_url;link.target='_blank';link.rel='noopener';
    $('scenario-status').replaceChildren(element('span','JSON gravado no computador: '+exported.path+' · '),link);
  }
  async function scenarioAction(id,action){
    const revision=++scenarioRevision;
    try{const record=await api('/api/cosmology/scenarios/'+encodeURIComponent(id));if(revision!==scenarioRevision)return;
      if(action==='export'){await exportFile({scenario_id:record.id});return;}
      if(action==='reference'){setReference({label:record.label,evaluation:record.evaluation,id:record.id,sha256:record.sha256});write('scenario-status',`Referência A: ${record.label}.`);return;}
      if(!source.models.some(model=>model.id===record.evaluation.model.id))throw new Error('Modelo salvo não disponível neste executor; exporte o cenário para inspecionar.');
      $('model-choice').value=record.evaluation.model.id;chooseModel(false);
      pause();for(const [key,value]of Object.entries(record.inputs)){if(!ids[key])throw new Error('Parâmetro salvo desconhecido');$(ids[key]).value=value;}
      $('scenario-label').value=record.label+' (recalculado)';syncSliders();await evaluate();
      write('scenario-status',fresh?`Parâmetros de “${record.label}” recalculados como B. O cenário original foi preservado.`:'Reavaliação falhou; cenário salvo preservado.');
    }catch(error){write('scenario-status',error.message);}
  }
  async function refreshScenarios(){
    try{const response=await api('/api/cosmology/scenarios'),items=response.scenarios;
      if(!Array.isArray(items))throw new Error('Lista de cenários inválida');
      $('scenario-list').replaceChildren(...items.map(item=>{
        const card=element('article');card.className='scenario-card';const info=element('div');
        info.append(element('h3',item.label),element('p',item.engine_sha256===source.engine_sha256?'Versão atual do cálculo':'Versão anterior · carregar como B para recalcular'),element('p',`${new Date(item.created_at_utc).toLocaleString('pt-BR')} · χ² ${fmt(item.chi2.value,4)}`),element('p',(modelLabels[item.model_id]||item.model_id)+' · '+parameterLabel(item.parameters)));
        const buttons=element('div');buttons.className='scenario-buttons';
        for(const [action,label]of [['reference','Usar como A'],['load','Carregar como B'],['export','JSON ↓']]){const b=element('button',label);b.type='button';b.className='button quiet';b.onclick=()=>scenarioAction(item.id,action);if(action==='reference'&&item.engine_sha256!==source.engine_sha256)b.disabled=true;buttons.append(b);}card.append(info,buttons);return card;
      }));write('scenario-status',items.length?`${items.length} cenários verificados no computador.`:'Seu caderno está vazio. Salve a primeira exploração.');
    }catch(error){write('scenario-status','Falha ao ler caderno: '+error.message);}
  }
  $('pin-reference').onclick=()=>{if(fresh)setReference({label:'Referência fixada nesta exploração',evaluation:result});};
  $('clear-reference').onclick=()=>{reference=null;comparison();actions();draw();write('difference-readout','Fixe uma referência A para inspecionar a mudança do modelo.');};
  $('difference-observable').onchange=draw;
  $('export-comparison').onclick=async()=>{
    if(!fresh||!reference)return;
    try{compatible(reference);compatible({evaluation:result});
      await exportFile({reference_parameters:{...reference.evaluation.parameters,model_id:reference.evaluation.model.id},current_parameters:{...result.parameters,model_id:result.model.id}});
    }catch(error){write('scenario-status','Exportação não confirmada: '+error.message);}
  };
  $('scenario-form').onsubmit=async e=>{e.preventDefault();if(!fresh || !result || saving || !$('scenario-form').reportValidity())return;
    saving=true;actions();const payload={label:$('scenario-label').value,parameters:{...structuredClone(result.parameters),model_id:result.model.id}};
    try{const saved=await api('/api/cosmology/scenarios',payload);await refreshScenarios();write('scenario-status',`Salvo: ${saved.label} · ${saved.id}. Cálculo refeito e verificado no servidor.`);}
    catch(error){write('scenario-status','Não foi possível confirmar o salvamento: '+error.message+'. Atualize a lista antes de tentar novamente.');}
    finally{saving=false;actions();}
  };
  $('refresh-scenarios').onclick=refreshScenarios;
  $('difference-axes').onclick=e=>{if(!result || !reference)return;const box=e.currentTarget.getBoundingClientRect();pause();updateCursor((e.clientX-box.left-56)/(box.width-81)*3);schedule();};

  load();
})();
