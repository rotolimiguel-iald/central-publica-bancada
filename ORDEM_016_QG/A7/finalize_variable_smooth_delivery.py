"""Custody and short delivery for measured variable-reference contacts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'variable_smooth_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    if p.exists():
        assert replace,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b and b;t.replace(p)
def obj(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode())
def append(p,v):
    b=p.read_bytes();write(p,b+v.encode(),True);assert p.stat().st_size>len(b)
artifacts={};data=[];logs=[]
for name in ['smooth_firstjet_source','smooth_mixed_gradient','smooth_variable_bv']:
    m=H/name/'manifest.json'
    for a in json.loads(m.read_bytes())['artifacts']:
        p=Path(a['path']);assert sha(p)==a['sha256'],p
        artifacts[str(p)]=sha(p)
    artifacts[str(m)]=sha(m)
    log=H/(name+'_run.log');r=json.loads((H/name/'results.json').read_bytes())
    # Final log is compact by design; compare every printed result field.
    printed=json.loads(log.read_text('utf-8-sig').splitlines()[-1])
    assert all(r[k]==v for k,v in printed.items())
    assert r['full_Q2'] is False
    artifacts[str(log)]=sha(log);data.append(r)
    logs.append(dict(command=f'A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/{name}_check.py',
                     rc=0,log=str(log),sha256=sha(log)))
for p in [H/'smooth_variable_bv/DERIVACAO.md',Path(__file__)]:artifacts[str(p)]=sha(p)
checks=sum(r['checks'] for r in data);cpu=sum(r['cpu_seconds'] for r in data)
opening=OUT/'ENTREGA_016_ABERTURA_operador.md'
obj(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=sha(opening),
    artifacts=[dict(path=p,sha256=h) for p,h in sorted(artifacts.items())],
    logs=logs,checks=checks,cpu_seconds=cpu,gate_changed=False,full_Q2=False))
note=f'''[DERIVED — primitiva BV do contato relativo suave variável; Q2 completa OPEN]

{now.isoformat()}. Abertura SHA256 {sha(opening)}.

O vértice da fonte agora inclui os primeiros jatos suaves antes omitidos:
além de R_W∂c, há A_Wc. Na família isotrópica dependente de (X+Y)/2:

    A_Ic=-g c·∂wI/2; A_Tc=+g c·∂wT/4;
    A_Gc=-(c⊗∂wG+∂wG⊗c)/16.

A bolha foi calculada antes de mover derivadas pela referência. O tensor
métrico I contém96 componentes com parte antissimétrica nos índices de
derivada, invisível no símbolo de w constante. Com w=x1 e h00=x0, omitir
essa parte perde1/8 na saída01. Conservá-la fornece a Hessiana real
N_w=-div(w T grad), com pesos de fibra explícitos. O ghost é zero nesse
contato; a fonte ghost variável não é omitida.

A ligação usa o antifield já existente no BRST:

    B_W=-C_E integral(1/2 h.N_w h+hdagger.R_W c),
    s0B_W=-C_E integral h.(N_wG+E R_W)c.

Isso dispensa fatorar toda R_W por G. As correntes de integração por
partes foram escritas e verificadas localmente; nenhum termo de corte
foi declarado zero. No caso constante, B_W e a primitiva métrica anterior
diferem por -C_E s0 integral hdagger.L_W h, ligando as duas construções.

Controle: w=x0³-3x0x1², c=e0 dá Gc=0, mas E R_Ic=diag(6,-6,0,0).
Portanto uma primitiva apenas métrica perde o termo; a BV o produz.
Não se promoveu esse jato formal a estado físico/BRST-compatível.

Evidência: {checks} verificações, CPU{cpu}s, três comandos rc0.
Nota completa: {H/'smooth_variable_bv/DERIVACAO.md'}.
Manifesto: {D/'manifest.json'}, SHA256 {sha(D/'manifest.json')}.

Alcance: contato relativo de duas pontas, plano auxiliar, família suave
isotrópica dependente do centro; fórmulas da fonte admitem jatos gerais.
Restam curvatura, referência admissível geral, outros locais/aridades,
continuação causal e Q2 completa. Não adotado contratermo; gate intacto.
Próximo: verificar o transporte da referência e combinar com os termos
curvos já medidos, preservando a revisão independente em andamento.
'''
write(OUT/'ENTREGA_016_A7b_referencia_variavel_primitiva_BV.md',note.encode())
measure=f'''[REAL — MEDIDA de termo omitido pela redução à referência constante]

{now.isoformat()}. Abertura SHA256 {sha(opening)}.
Tentativa: reutilizar somente a Hessiana constante e uma primitiva métrica.
Controle1: no tensor métrico I, w=x1,h00=x0,
(N_completo-N_simétrico)01=1/8.
Controle2: w=x0³-3x0x1²,c=e0; Gc=0 e E R_Ic=diag(6,-6,0,0).
Portanto a variação só métrica é insuficiente neste jato formal.
Próximo ramo já executado: primitiva BV com hdagger.R_Wc, corrente explícita.
Não é obstrução à primitiva BV nem classe quântica não trivial.
Comandos, rc0 e hashes de logs: {json.dumps(logs,ensure_ascii=False)}.
Custo de CPU local{cpu}s; novas chamadas remotas0 nesta medição.
'''
write(OUT/'ENTREGA_016_MEDIDA_jatos_suaves_na_primitiva.md',measure.encode())
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='A7_VARIABLE_SMOOTH_BV_CONTACT_VERIFIED',
    target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,
    manifest_sha256=sha(D/'manifest.json'),full_Q2=False),ensure_ascii=False)+'\n')
seen=set();cost=Decimal(0)
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    r=json.loads(line);v=r.get('cost_estimate_usd')
    if v is None:v=r.get('cost_usd')
    if v is None:continue
    key=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: referência suave variável; fonteprimeirojato, tensorantissimétrico e primitivaBV conectados com correntes. {checks}checks,CPU{cpu}s; custo parcialUS${cost},unknownnotzero. Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes())
c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['First smooth source jets explicitly contracted',
    'Unintegrated mixed-gradient tensor: antisymmetric contribution measured',
    'Variable-reference BV primitive and Green currents verified'],
    variable_smooth_manifest=str(D/'manifest.json'),
    next=['Audit pending Kimi reviews',
    'General compatible reference and curved/local completion within A7b timebox',
    'A7.b deadline2026-09-25T20:32Z; then A7.c/d,A8,PartB,final audit'],
    partial_metered_cost_usd=str(cost),own_live_processes=[])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode(),True)
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,artifacts=len(artifacts),
    cost_partial=str(cost),manifest_sha256=sha(D/'manifest.json')),ensure_ascii=False))
