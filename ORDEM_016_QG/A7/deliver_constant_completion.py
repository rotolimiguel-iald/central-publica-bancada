"""Preserve the full constant-ghost identity and orchestration snapshot."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f:f.write(b)
    assert b and temp.read_bytes()==b;temp.replace(p)
def fresh(p,o):assert not p.exists();save(p,json.dumps(o,ensure_ascii=False,indent=2))
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((HERE/'constant_ghost_full_basis/results.json').read_bytes())
z=json.loads((HERE/'constant_ghost_completion/results.json').read_bytes())
assert r['components']==400 and not r['mismatches'] and z['symbolic_bracket_checks']==64
report=f'''[DERIVED — identidade principal de ghost constante; REAL — CAS exato; OPEN — ghost variável e Q2 finita]
# A7.b — completar todas as polarizações do ghost constante

Abertura SHA256 `{opening}`. UTC {now}.

O ajuste do representante Z preservou as64 componentes simbólicas da
identidade do bracket já obtida. O sistema combinado tem posto15 em21
coeficientes; seis parâmetros livres foram postos em zero. Isso é escolha
de representante, não unicidade/canonicidade. Os coeficientes e suas bases
estão registrados em constant_ghost_completion/results.json e no script.

Fixados esses coeficientes ANTES do ensaio completo, verificamos

    R1(H,p;0,v) = -K_p Z_new(H,p;0,v) + (p·v) B(E_p H),
    B(A) = -A/6 - I tr(A)/12,
    E_p H = p² Itr(H) - Itr(K_p C_p H).

Aqui K_p v=pv^T+vp^T, C_p H=Hp-p tr(H)/2, Itr(H)=H-I tr(H)/2.
Normalização: R1=G-M/4 após retirar4iκA0, A0=1/(8π²), como nos
vértices anteriores. E é4κ vezes a Hessiana física livre, não a Hessiana
gauge-fixada. O termo B(E) é justamente a contribuição de equação de
movimento permitida pela primitiva de antifields deslocados já construída.

Cobertura:10 polarizações simétricas H ×10 fontes simétricas T ×4 vetores v,
p=e0, momento do ghost zero. {r['nonzero_components']} componentes não nulas,
400 comparações exatas, zero diferenças. Não se impôs transversalidade a H
nem paralelismo entre p e v. Covariância O(4) e homogeneidade cúbica dos
dois lados estendem o resultado a qualquer p Euclidiano; p=0 segue por
continuidade polinomial. Não se deduz daí uma extensão Lorentziana causal
ou uma escolha do estado físico sem verificar essa ponte.

Com ghost constante, Z_new é

    -v trH p²/8 + v(p·Hp)/12 + (Hv)p²/4
    -(Hp)(p·v)/12 + p trH(p·v)/6 - p(v·Hp)/6.

O ensaio usa o mesmo motor de vértices previamente auditado. As400
comparações verificam a nova decomposição; não constituem400 avaliações
independentes do motor. Não houve compilação Lean nesta etapa.
CPU do ajuste: {z['cpu_seconds']}s; CPU do ensaio: {r['cpu_seconds']}s;
paredes: {z['wall_seconds']}s + {r['wall_seconds']}s. Ambas execuções rc0.

Próximo passo na mesma A7.b: calcular o polinômio principal completo com
momento do ghost não nulo e medir o resíduo da candidata BV. A ação
completa, termos curvos, realidade e anomalia causal finita continuam OPEN.
Nenhum original, kernel ou gate modificado.
'''
rp=HERE/'constant_ghost_full_basis/DERIVACAO.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_ghost_constante_completo.md',report)
files=[rp,HERE/'constant_ghost_completion_check.py',HERE/'constant_ghost_full_basis_check.py',
       HERE/'constant_ghost_completion_run.log',HERE/'constant_ghost_full_basis_run.log',
       HERE/'marked_vertex_engine.py']
for folder in ['constant_ghost_completion','constant_ghost_full_basis']:
    files.extend([HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json'])
fresh(HERE/'constant_ghost_full_basis/manifest.json',dict(at=now,opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
ledger=OUT/'LEDGER_016.jsonl'
event=dict(event='A7_FULL_CONSTANT_GHOST_COMPLETION',at=now,provider='local',target='A-7.b',
           components=400,symbolic_bracket_checks=64,rc=0,cpu_seconds=z['cpu_seconds']+r['cpu_seconds'],
           report_sha256=sha(rp),full_Q2=False,gate_changed=False)
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for ln in ledger.read_text('utf-8-sig').splitlines():
    if not ln.strip():continue
    x=json.loads(ln);v=x.get('cost_estimate_usd',x.get('cost_usd',x.get('custo_usd')))
    k=x.get('execution_id') or x.get('job_id') or x.get('request_id') or x.get('execution_task_id')
    if k and v is not None:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,constant_ghost_full_basis_manifest=str(HERE/'constant_ghost_full_basis/manifest.json'),
    constant_ghost_vertex_complete=True,full_hstar_hc_matched=False,
    pending_orchestration='5 active/queued: Kimi2 MiMo2 DeepSeek1;9 staging:Kimi5 MiMo4; cohomology executing',
    partial_metered_cost_usd=total)
d['completed_this_turn'].append('Full constant-ghost principal vertex 400/400 with bracket-compatible Z and BV EOM term')
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: ghost constante completo400/400, bracket64/64, sem novo ajuste entre componentes. CPU{event["cpu_seconds"]}s; Q2finitaOPEN; custo externo parcialUS${total}. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),components=400,bracket_checks=64,partial_cost=total)))
