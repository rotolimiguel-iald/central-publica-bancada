"""Deliver first-curvature operator and preserve the nonzero Ward diagnostic."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def data(rel):return json.loads((H/rel).read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
folders=['radial_covariant_jet','position_metric_adjoint','position_metric_adjoint_audit','first_curvature_total_hessian','first_curvature_ward_probe','oneform_classical_ward','first_curvature_ward_audit']
files=[];results={}
for folder in folders:
    results[folder]=data(folder+'/results.json')
    for f in data(folder+'/manifest.json')['files']:
        p=Path(f['path']);assert sha(p)==f['sha256'],str(p);files.append(p)
checks=sum(r.get('checks',0) for r in results.values());cpu=sum(r.get('cpu_seconds',0) for r in results.values())
total=results['first_curvature_total_hessian'];ward=results['first_curvature_ward_audit']
report=f'''[DERIVED — operador logarítmico na primeira curvatura; REAL — CAS; OPEN — soma causal]
# A7.b — adjunto, operador covariante e resíduo medido
Abertura SHA256 `{opening}`. UTC {now}.

O perfil radial anterior deixou uma derivada na perna externa B ancorada.
Sua transferência por partes não é substituição de momento em espaço curvo:
troca sym(nabla^4) por nabla_j sym(nabla^3). A diferença atua na fibra
tensorial e nos índices de derivada. Foi calculada, sem impor Ward=0.

**Jatos.** Para h=e A e^t exp(ipx), e=I-K(zI-xx)/6, os jatos covariantes
totalmente simétricos de ordem2/4 não têm termoK. O jato com uma derivada
externa a sym(nabla^3) tem termoK não nulo. Verificação4551checks,
1620 jatos externos não nulos; calibração escalar Box² exp(ipx)|K=2Kp².

**Adjunto da bolha.** Os dois setores que contêm gradB dão

    -1/6 T2 [nabla_j sym(nabla^3)-sym(nabla^4)]A
    -1/2 T1 [nabla_j sym(nabla^3)-sym(nabla^4)]A,

com T2/T1 as contrações angulares dos vértices de duas/uma derivadas
internas na ponta X. Derivadas na ponta Y foram transferidas só aqui.
Na base ordenada [p²trAB,p²trA trB,pAp trB,pBp trA,pABp], resulta

    delta = [83/9,-25/6,28/9,145/18,-134/9].

Somando ao perfil derivativo anterior, os coeficientes mistos tornam-se
iguais a269/9. Isso foi consequência da conta, não condição de ajuste.
Auditoria independente por contração inteira:100 pares, três momentos
fora do eixo e calibrações,106checks. Excluir o adjunto volta a quebrar
a igualdade. Os primeiros cinco casos serviram só para extrair a tabela.

**Mesmo símbolo para todos os setores.** Agora usamos a quantização por
derivadas covariantes completamente simetrizadas. Sob essa convenção,
o símbolo em quadro radial identifica os coeficientes locais. A parte
principal de ordem4 continua sendo a tabela plana já paga. Na ordemKp²,
incluindo potencial, peso-1/2 da bolha e tadpole:

    métrica: {total['metric_with_tadpole']}
    ghost:   {total['ghost']}
    soma:    {total['total']}.

Todos divididos por hbar*A0, A0=1/(8pi²), com K retirado. O ghost foi
avaliado de seu operador com derivadas ordenadas, não da variação do calor
livre. Há100 pares e três controles não axiais nessa conversão (106checks).
Coeficientes iguais nas posições3/4 significam compatibilidade com o
adjunto neste recorte; não são uma identidade Ward por si só.

**O teste de Ward NÃO zerou.** Com G(v)=nabla v+(nabla v)^t e a fase i
retirada, a aplicação do operador montado fornece

    (H_loop G)_K = K[-(1/2)p²(pv^t+vp^t)
                         -2pp^t(p.v)+(3/2)g p²(p.v)].

A fonte previamente calculada fornece (E R)_K=4K(pp^t-gp²)(p.v).
Portanto a combinação com sinal mais tem coeficientes[-1/2,2,-5/2]
na base[p²G,pp(p.v),gp²(p.v)]. O sinal oposto também não zera;
para p=e0,v=e1 a fonte é zero e(H_loop G)01=-K/2 nos dois casos.

O avaliador passa a Ward CLÁSSICA E G=0 em256 componentes e a Ward
plana do operador de laço. Jatos ímpares e probes:960checks; teste
adicional do resíduo em15 polarizações e da família local:252checks.
O resíduo é real no cálculo executado; ainda não está identificado como
a anomalia causal completa da prescrição. Falta reconciliar os contatos,
ordens superiores e normalizações das diferentes representações.

**Família algébrica localizada, não adotada:** neste setor homogêneo,
um acréscimo à Hessiana de ordemK com coeficientes

    (d1,d2,d3,d4)=(1/2-t/2,9/4+t/2,-1-t/2,t)

cancelaria a combinação local indicada. Isso localiza uma liberdade
de contratermos na ordem testada; não escolhe t, não autoriza modificar
a prescrição, não demonstra Wess-Zumino/BRST completo nem QME finita.
É necessário verificar a extensão na hierarquia causal antes de usar
essa família. Nenhum coeficiente da conta foi trocado para obter zero.

Execuções deste pacote rc0; {checks} checks, CPU{cpu}s. A parteK²,
os termos finitos dependentes de estado/cutoff e Q2 completa permanecem
abertos. Gate, um.py e kernel intactos. Resultados não enviados aos
revisores independentes em espera.
'''
rp=O/'ENTREGA_016_A7b_adjunto_e_primeira_curvatura.md';assert not rp.exists();save(rp,report)
mp=O/'ENTREGA_016_MEDIDA_primeiro_log_curvo_Ward.md'
measure=f'''[REAL — resíduo local medido; OPEN — identificação de Q2 completa]
Abertura SHA256 `{opening}`. UTC {now}.

Tentativa: contrair a Hessiana logarítmica métrica+ghost+tadpole com o
mapa de gauge, somando a fonte BV previamente calculada na primeiraK.
Comando: C:\\Python314\\python.exe -X utf8 -B first_curvature_ward_audit.py.
rc0 significa que os252 controles do RESÍDUO passaram, não que ele zerou.
Log SHA256 `{sha(H/'first_curvature_ward_audit_run.log')}`.
Para p=e0,v=e1: (H_loop G)01=-K/2; (E R)01=0.
Resíduo da soma: K[-p²G/2+2pp(p.v)-5gp²(p.v)/2].
Custos: CPU do audit {ward['cpu_seconds']}s; nenhuma chamada externa.

Próximo ramo dentro de A7.b: cotejar a conversão covariante e os
contatos/normalizações com as revisões independentes já solicitadas;
continuar a componenteK² e a extensão temporal finita. A família
algébrica de correção está explicitada na entrega, mas não foi adotada.
Não descartar o resíduo e não anunciá-lo como anomalia física confirmada.
O timebox A7.b segue; não iniciar A7.c antes de seu limite de24h.
'''
assert not mp.exists();save(mp,measure)
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_FIRST_K_ADJOINT_AND_NONZERO_WARD'
if marker.encode() not in raw:
    raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=checks,cpu_seconds=cpu,
        report_sha256=sha(rp),measure_sha256=sha(mp),new_external_execution=False,full_Q2=False),ensure_ascii=False)+'\n').encode()
save(ledger,raw)
rows=[json.loads(t) for t in raw.decode('utf-8-sig').splitlines() if t.strip()];parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for e in rows:
    ix=ids(e)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for e in rows:
    ix=ids(e);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
cost=sum(known.values(),Decimal(0))
extra=['position_metric_adjoint_engine.py','radial_covariant_jet_run.log','position_metric_adjoint_run.log','position_metric_adjoint_audit_run.log',
    'first_curvature_total_hessian_run.log','first_curvature_ward_probe_run.log','oneform_classical_ward_run.log',
    'first_curvature_ward_audit_run.log','capture_marked_review_transition.py','received_reviews/A7_transition_after_mimo_marked_failure.json']
files+= [H/r for r in extra]+[Path(__file__),rp,mp]
files=list(dict.fromkeys(files))
manifest=H/'first_curvature_total_hessian/delivery_manifest.json'
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['Covariant radial Taylor jets4551checks','Adjoint correction full100fiber audit106checks',
        'Combined firstK local Hessian106checks','Nonzero Ward diagnostic960+252checks; classical calibration256checks'],
    first_curvature_hessian_manifest=str(manifest),first_curvature_ward_measure=str(mp),
    pending_orchestration='5registered/8staging; MiMo marked failed no retry; Kimi primitive running',
    latest_live_execution=dict(job_id='f1293276-0c3a-4b5b-bbf6-b3585a862ad2',execution_id='a1db5302-f89d-45c8-a924-a38496f9416d',status='running',observed_utc='2026-09-25T04:20:06.954720+00:00'),
    partial_metered_cost_usd=str(cost),
    next=['Localize nonzero firstK logarithmic Ward residual: reconcile contacts/conventions and independent reviews; never tune it away',
        'Continue full K2 and finite causal hierarchy; algebraic local-family is not adopted or full BRST cohomology',
        'Do not repeat terminal MiMo failures; single worker manages running Kimi and staging8',
        'A7.c onlyafter24h; A7.d,A8,PartB and finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: adjunto eHessiana primeiraK; {checks}checks CPU{cpu}s. Resíduo Ward NÃO ZERO preservado em MEDIDA, Q2OPEN. MiMo marcado failed semretry;Kimi primitive running. Custo parcialUS${cost}, desconhecidosnãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(rp),measure=str(mp),checks=checks,cpu_seconds=cpu,verified_artifacts=len(files),partial_cost=str(cost))))
