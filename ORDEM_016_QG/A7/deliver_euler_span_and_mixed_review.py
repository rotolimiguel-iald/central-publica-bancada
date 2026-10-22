"""Record a failed restricted completion and preserve the next actual Ward target."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'euler_span_mixed_review_delivery';assert not D.exists();D.mkdir()
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,existing=False):
    if p.exists():
        assert existing,p;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False).encode('utf-8'),existing)
def append(p,t):write(p,p.read_bytes()+t.encode('utf-8'),True)
span=json.loads((H/'euler_descendant_span/results.json').read_bytes())
audit=json.loads((H/'kimi_mixed_current_normalization_review/local_audit.json').read_bytes())
checks=span['checks']+audit['checks'];cpu=span['cpu_seconds']+audit['cpu_seconds']
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — não pertencimento ao span de duas inserções; Q2 completa OPEN]

Hipótese examinada: a diferença de consistência do representante h,c seria
cancelável apenas por um peso global/alocação do regulador nos dois kernels
Euler ordenados já calculados. Nenhum coeficiente foi escolhido por ajuste.
Com lambda=(1,-1,0,0),eta=(1,0,0,0), extraímos572 linhas de coeficientes
polinomiais das16 componentes. Os dois geradores D_X,D_Y têm posto2; ao
adicionar a diferença medida F, o posto sobe a3. O resultado vale tanto
para F ordenado quanto para sua polarização dos dois cutoffs.

Uma testemunha exata usa a entrada00 e os monômios q0^5,q0^4q1,q0^3q1²:

                 D_X       D_Y         F
 q0^5            47/240    47/240     -3259/960
 q0^4q1           1/12        0          -1/2
 q0^3q1²         13/24      13/24      -541/96

O determinante é -847/13824, não zero. A polarização muda o terceiro
coeficiente da segunda linha para217/192 e conserva esse determinante.
Logo nenhum par de constantes a,b satisfaz F+a D_X+b D_Y=0.
É uma afirmação sobre os kernels que efetivamente calculamos, não sobre
todas as normalizações possíveis de inserções compostas. Não se atribui
classe de obstrução BV a esse resultado. O tau permanece não escolhido.

Há também uma separação de ordens útil, sob hipóteses explícitas: se W1
é o tadpole LOCAL de um único vértice cúbico, é linear nos campos; se A1
e J1 são os correspondentes termos locais de número de ghost1, são
lineares em c após integrar por partes. Escreva W1=int h_ab F_ab e
A1=int c_a f_a, J1=int c_a j_a, com coeficientes independentes dos ghosts.
Na projeção de dois ghosts e nenhum campo par, (W1,I1) vem de
delta I1/delta hdagger=-[G,chi](c.dc); (V1,A1) e (V1,J1) vêm do
vértice cdagger chi(c.dc). Cada expressão tem no máximo UMA derivada
sobre um ghost; a adjunção ponderada não aumenta essa ordem. Assim
esses três termos locais de primeira ordem NÃO alteram o menor de grau5
acima. Isto não supõe W1=0, nem cobre W1 não local, nem elimina J2 completo.

O alvo seguinte é a normalização diferencial completa das inserções e dos
termos de descida de J2, inclusive o vínculo entre o representante calculado
e a anomalia A2. Não basta reescalar os dois Euler kernels ou declarar
tadpoles nulos. A identidade inhomogênea permanece a referência escrita:
s0 A2+(V1,A1)+(W1,I1)+s0 J2+(V1,J1)=0.

Auditoria independente Kimi ee44: suas cinco famílias de J_b coincidem
com current_terms nos16 pares(mu,r); o toy -18/2401*gQ*gD confere.
Porém, a convolução com o adjunto formal impõe gD*ell=-2gQ, não+2gQ.
O inverso já verificado usa gD=-4kappa,ell=1/(2kappa),gQ=1 nas unidades
do kernel comum. O b_column já traz os dois deltas: no controle diagonal
ele vale-4/49, contra-2/49 se se retiver só a fibra de traço invertido.
Logo o termo de traço não está ausente do motor. Não o somar novamente.
Substituir dc por eta*c é avaliação especial do campo externo, não o
adjunto(d-eta) do diagrama; o motor conserva esse adjunto. Sua escala v3
é+1/4 por contração ordenada, derivada antes, não a escala/16 do antigo
motor métrico citado pelo parecer. Nenhuma alteração do engine foi feita.

Sete verificações do span,30 da auditoria; CPU total{cpu}s,rc0.
Kimi ee44:370528tokens,1011.191s; assinatura sem custo por chamada informado.
Recibo já lançado uma única vez. Provas/checagens anteriores não recontadas.
Comandos: python A7/euler_descendant_span_diagnostic.py e
python A7/audit_kimi_mixed_current_normalization.py (runtime SymPy de A4,
-X utf8 -B; intake é único, não repetir custos). Logs e hashes no manifesto.

Estado coordenado15:46:11UTC: MiMoa369 e Kimi5e1 RUNNING no worker91153;
Kimi51c admitido no job039cab4b-a3a1-4cad-8d8c-349a55d705b3 após e710.
Mantidos cinco admitidos, FIFO e prazo20:32UTC. Originais/kernel/gate intactos.
Abertura sha256={opening}.
'''
write(D/'DERIVACAO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_MEDIDA_euler_span_duas_insercoes.md',report.encode('utf-8'))
paths=[Path(__file__),D/'DERIVACAO.md']+[H/p for p in [
 'euler_descendant_span/results.json','euler_descendant_span/manifest.json',
 'euler_descendant_span_diagnostic.py','euler_descendant_span_run.log',
 'kimi_mixed_current_normalization_review/local_audit.json',
 'kimi_mixed_current_normalization_review/manifest.json',
 'audit_kimi_mixed_current_normalization.py','audit_kimi_mixed_current_normalization_run.log',
 'localized_brst_anticommutator/results.json','second_curvature_bv_order_delivery/DERIVACAO.md']]
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='EULER_SPAN_NONMEMBERSHIP_AND_MIXED_REVIEW',
 target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
cost=Decimal(0);seen=set()
for line in ledger.read_text('utf-8').splitlines():
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is None:continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b MEDIDA: dois Euler kernels não geram a diferença medida (posto2→3); Kimi ee44 auditado, motorv3 preservado;{checks}checks,CPU{cpu}s,custo conhecido parcialUSD{cost}; prossegue descida/normalização completa,Q2 OPEN. Abertura sha256={opening}.\n')
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
# Keep the previous head as history so stale summary fields no longer masquerade as current.
headkeys=['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','partial_metered_cost_usd']
state.setdefault('head_history',[]).append({k:state.get(k) for k in headkeys})
state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Euler two-ordering span excluded exactly, determinant -847/13824',
 'Kimi ee44 received and audited, four corrections, no new mixed engine',
 'Local first-order tadpole terms cannot remove degree5 witness under stated arity assumptions'],
 next=['Derive differential normalization of complete J2; do not refit tau/global weights',
 'Source hdagger-h-c loop already included in localized_source_boundary_engine; do not duplicate it',
 'Receive Kimi5e1/bd879/e710/51c and MiMoa369, audit independently',
 'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
 pending_orchestration='Official15:46:11UTC: Kimi5e1 and MiMoa369 running in coordinator worker91153; Kimi bd879,e710,51c waiting; five admitted',
 partial_metered_cost_usd=str(cost))
state['euler_span_mixed_review_update']=dict(at=now.isoformat(),manifest=str(D/'manifest.json'),
 normalization_selected=False,restricted_euler_span_closed=False,own_processes=[],
 newest_kimi_job='039cab4b-a3a1-4cad-8d8c-349a55d705b3',full_Q2=False,gate_changed=False)
put(p,state,True)
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,known_partial_cost_usd=str(cost))))
