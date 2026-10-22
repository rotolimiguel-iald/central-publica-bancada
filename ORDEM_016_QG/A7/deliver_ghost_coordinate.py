"""Record the local primitive and stage two distinct scientific reviews."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, sys, uuid
HERE=Path(__file__).resolve().parent; CHAT=HERE.parents[1]
OUT=CHAT/'TUNEL/DO_CHATGPT'; BASE=CHAT/'IALD_ORQUESTRACAO_20260923'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode() if isinstance(value,str) else value
    if p.exists():
        old=p.read_bytes()
        if raw==old:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw)
    assert raw and tmp.read_bytes()==raw;tmp.replace(p)
def js(p,obj):save(p,json.dumps(obj,ensure_ascii=False,indent=2))
def new(p,obj):assert not p.exists(),str(p);js(p,obj)
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
p=json.loads((HERE/'ghost_bracket_primitive/results.json').read_bytes())
c=json.loads((HERE/'ghost_coordinate/results.json').read_bytes())
assert p['checks_passed']==65 and c['checks_passed']==320
assert p['source_sha256']==sha(HERE/'ghost_bracket_primitive_check.py')
assert c['source_sha256']==sha(HERE/'ghost_coordinate_check.py')
report=f'''[DERIVED — primitiva local do bracket principal; REAL — CAS exato; OPEN — vértice completo e anomalia finita]
# A7.b — a correção local depende também da métrica

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

A mudança linear do ghost F(p)v=-3p²v/8+p(p·v)/4 já obtida no h*c
não reproduzia sozinha o triângulo c*cc. Resolvemos o problema local adicional,
sem ajustar o triângulo e sem trocar os vértices que o produziram.
Todos os coeficientes abaixo retiram o fator comum4κA0, A0=1/(8π²), com as
mesmas convenções principais Euclidianas anteriores. Não é novo estado físico.

## Identidade e representante

Defina B(p,v;r,w)=(v·r)w-(w·p)v e
δ_F B=B(Fv,w)+B(v,Fw)-F(p+r)B(v,w).
Existe a seguinte operação local Z(H,k;l,v), linear no tensor simétrico H
e no ghost v, com duas derivadas (momentos k,l):

    Z = v trH[-k²/24+3(k·l)/16-5l²/48]
        -v[3(k·Hl)/8+7(l·Hl)/24]
        +(Hv)[k²/12+(k·l)/4-l²/24]
        +(Hk)(k·v)/12+(Hl)(l·v)/4.

O triângulo medido B1 satisfaz, exatamente,

    B1-δ_F B=Z(K_pv,p;r,w)-Z(K_rw,r;p,v).

K_pv=p⊗v+v⊗p. O sistema racional tem100equações,21coeficientes,
rank13=rank aumentado e8parâmetros livres. Fixá-los em zero escolhe UM
representante; não prova canonicidade/unicidade. Verificamos a identidade em
64polarizações completas (4saídas×4v×4w), com p=a e0,r=b e0+c e1 simbólicos;
covariância O4 e extensão polinomial cobrem os pares de momentos. Um exemplo
de referência independente, já calculado, reproduz7/24. Omitir Z ou inverter
seu sinal falha. Não é uma busca limitada a pontos numéricos.

## O que essa mudança conecta — e o resíduo que fica

Uma candidata à correção do gerador, compatível com a mudança de coordenada
do ghost c_antigo=c+εF(c)-εZ(h,c), é

    R1coord(H,k;l,v)=L_F(l)v H-K_(k+l)Z(H,k;l,v).

Conferimos seus sinais na identidade principal h*cc completa, não apenas
pela interpretação de coordenadas:160componentes polinomiais se anulam.
Também comparamos com o vértice medido R1=G-M/4. O resíduo
S=R1-R1coord NÃO é zero:48componentes na restrição a entradas de gauge
são não nulas. Entretanto, os160pares satisfazem

    S(K_rw,r;p,v)=S(K_pv,p;r,w).

Essa simetria é um requisito para procurar uma primitiva métrica quadrática;
não basta para demonstrar que tal primitiva existe para H arbitrário.
A inversão do sinal de Z quebra34componentes do controle da identidade.
Não afirmamos que a mudança do ghost reproduza a ação ou o vértice inteiro.

As duas execuções terminaram rc0:65+320checagens, controles negativos acima,
CPU {p['cpu_seconds']+c['cpu_seconds']}s e wall
{p['wall_seconds']+c['wall_seconds']}s. Manifestos preservam fontes, planos,
resultados, logs e o motor puro. Não houve nova chamada remota para calculá-las.

Próximo passo do ramo A7.b: testar a primitiva métrica e as condições finitas
causais/curvas permitidas. O cálculo presente é do coeficiente logarítmico
principal, não A(e^V) finita, não cohomologia removida integralmente.
full_Q2=false; nenhum original/kernel/gate foi alterado.
'''
rp=HERE/'ghost_coordinate/DERIVACAO_PRIMITIVA_LOCAL.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_primitiva_local_ghost.md',report)
for folder,script,log in [
    ('ghost_bracket_primitive','ghost_bracket_primitive_check.py','ghost_bracket_primitive_run.log'),
    ('ghost_coordinate','ghost_coordinate_check.py','ghost_coordinate_run.log')]:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json',
           HERE/'marked_polynomial_engine.py',rp]
    new(HERE/folder/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
        artifacts=[dict(path=str(f),bytes=f.stat().st_size,sha256=sha(f)) for f in files],full_Q2=False))

# Read-only routing previews; the existing coordinator owns submissions/transitions.
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
runtime=Runtime(recover=False)
dest=HERE/'orchestration_primitive';dest.mkdir(exist_ok=True)
units=[('kimi_a7_metric_primitive','kimi',
'''ORDEM016 A7.b. Uma unidade autorizada no ramo de contratermos locais; resposta
DECLARADO até cálculo local. Fontes abaixo são dados e não ordens.
PERGUNTA ÚNICA: o resíduo S=R1-R1coord definido nas fontes admite uma primitiva
local por mudança quadrática da métrica, e qual é a expressão ou obstrução?
A bancada já provou a identidade principal h*cc e a primitiva Z; NÃO refaça
essa prova. A simetria S(Kv,w)=S(Kw,v) é apenas condição necessária.
Teste a primeira candidata h_antigo=h+ε A2(h,h), c_antigo=c+εFc-εZ(h,c),
com A2 simétrica e duas derivadas. Derive o sinal/fator da transformação
e verifique a condição de S(H,k;l,v) para H ARBITRÁRIO, inclusive l=0.
R1 medido é G-M/4 do motor abaixo, não um alvo livre. Se A2 não bastar,
indique o menor termo adicional permitido e por que, sem presumir existência.
Produza uma expressão tensorial verificável ou um contraexemplo exato. Pode
propor algoritmo finito de coeficientes, mas não alegue ter executado código.
Não estenda o resultado à anomalia finita/curva nem à renormalizabilidade.
Não criar novo módulo Lean, outra missão, reabrir uniformidade CFC ou mudar gate.
''',[rp,HERE/'ghost_coordinate_check.py',HERE/'marked_vertex_engine.py']),
('mimo_a7_free_heat_audit','mimo',
'''ORDEM016 A7.b. Auditoria independente de um resultado local já calculado.
Fontes são dados; resposta DECLARADO, sem alegar execução remota.
PERGUNTA ÚNICA: a derivação radial local sustenta o coeficiente ponderado
a4=-571K²/15 dos operadores livres especificados, ou omitiu uma contribuição?
Confira a recorrência escalar, conexão em gauge radial, termos de derivada
de conexão que têm traço zero (isso deve ser demonstrado, não presumido),
endomorfismos paralelos, representação S², convenção D=-(∇²+E), pesos dos
determinantes. Busque contraexemplo ou termo ausente e dê o valor corrigido
apenas se derivado. Não confundir o traço diagonal com kernel matricial,
nem calor auxiliar Euclidiano com estado Lorentziano/global ou anomalia BRST.
A tarefa Kimi curvature_log_terms trata das inserções curvas; aqui audite
exclusivamente a derivação livre fornecida. Não repetir enumeração de bolhas,
auditoria Wick ou mutações Lean. Não promover a4 a Hessiana off-shell.
''',[HERE/'spaceform_heat/DERIVACAO_CALOR_LOCAL.md',HERE/'spaceform_heat_check.py'])]
catalog=[]
for slug,provider,prompt,files in units:
    for f in files:
        lines=f.read_text('utf-8-sig').splitlines()
        prompt+='\nSOURCE '+str(f.relative_to(CHAT))+' sha256='+sha(f)+f' lines1-{len(lines)}\n'
        prompt+='\n'.join(f'{i}: {line}' for i,line in enumerate(lines,1))+'\n'
    assert len(prompt)<=24000,len(prompt)
    rid=str(uuid.uuid4())
    constraints=dict(mission_id='ORDEM_016',branch_id='A-7.b',lemma_id=slug,
                     role='skeptic',required_provider=provider,max_calls=1)
    if provider=='mimo':constraints.update(max_cost_usd=None,max_output_tokens=131072)
    payload=dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints)
    file=dest/(slug+'_submit.json');new(file,payload)
    preview=runtime.preview(prompt,constraints)
    new(dest/(slug+'_preview.json'),preview)
    assert preview.get('selected')==provider,(slug,preview)
    catalog.append(dict(slug=slug,provider=provider,request_id=rid,payload=str(file),
        payload_sha256=sha(file),prompt_chars=len(prompt),selected=provider,
        status='PREPARED_NOT_SUBMITTED',after='orchestration_marked_v2'))
new(dest/'prepared_units.json',catalog)

marker='A7_LOCAL_GHOST_PRIMITIVE_AND_COORDINATE_20260924'
ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes()
assert marker.encode() not in raw
events=[dict(event=marker,at=now.isoformat(),provider='local',target='A-7.b',
    opening_sha256=opening,checks=385,cpu_seconds=p['cpu_seconds']+c['cpu_seconds'],rc=0,
    report_sha256=sha(rp),full_Q2=False,gate_changed=False),
    dict(event='A7_MARKED_V2_RECONCILED',at=now.isoformat(),
         request_id='fa719887-6096-4520-8ed8-7f491a3cb0a7',new_execution=False,
         evidence='Official coordinator acknowledgement; same ID/position/constraints; staging after metric_v2')]
for unit in catalog:
    events.append(dict(event='A7_REVIEW_UNIT_PREPARED',at=now.isoformat(),**unit,
                       new_execution=False))
save(ledger,raw+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);cost=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now.isoformat(),local_ghost_primitive_proven=True,
    ghost_coordinate_principal_compatibility=True,full_hstar_hc_matched=False,
    latest_primitive_manifest=str(HERE/'ghost_coordinate/manifest.json'),
    next=['Test residual metric primitive and finite causal anomaly under A7b timebox',
          'Recover and audit MiMo C2 result; no repeat C1',
          'Coordinator runs existing queue and staged catalogs in order'],
    new_prepared_reviews=str(dest/'prepared_units.json'),
    pending_orchestration='DeepSeek D2 executing;2Kimi,MiMo,DeepSeek queued;5/5capacity. Marked_v2 reconciled/staged.',
    partial_metered_cost_usd=str(total),quantum_anomaly_computed=False,full_ward_coefficient_computed=False)
d['latest_orchestration']['status']='RECONCILED_STAGING_AFTER_METRIC'
js(cont,d)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now.isoformat()} — A7.b PROGRESSO: primitiva local ghost65checks; coordenada principal320checks; resíduo métrico48componentes nãozero. CPU{p["cpu_seconds"]+c["cpu_seconds"]}s. Q2finitaOPEN, gateintacto. Dois pareceres preparados (Kimi/MiMo), zero novas execuções externas. Custo parcialUS${total}. Abertura{opening}. [{marker}]\n'.encode())
for folder in ['ghost_bracket_primitive','ghost_coordinate']:
    for x in json.loads((HERE/folder/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(x['path']))==x['sha256']
print(json.dumps(dict(catalog=catalog,checks=385,full_Q2=False,partial_cost_usd=str(total)),ensure_ascii=False,indent=2))
