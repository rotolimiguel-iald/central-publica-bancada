"""Record the scoped independent audit without promoting provider claims."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'kimi_ghost_reduction_delivery';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if p.exists():
        assert update,p;old=p.read_bytes()
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert b and t.read_bytes()==b;t.replace(p)
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode(),update)
r=json.loads((H/'kimi_ghost_reduction_audit_v2/results.json').read_bytes())
g=json.loads((H/'kimi_ghost_gamma/results.json').read_bytes())
receipt=json.loads((H/'kimi_ghost_reduction_audit_v2/RECEIPT.json').read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
checks=r['checks']+g['checks'];neg=len(r['negative_controls'])+len(g['negative_controls'])
cpu=r['cpu_seconds']+g['cpu_seconds']
report=O/'ENTREGA_016_A7b_Kimi_ghost_reducao_corrigida.md'
text=f'''[DERIVED — resíduo integrado condicionado; REAL — CAS; OPEN — Q2 causal]
# A7.b — revisão do Kimi: parcela F² e correção mista
Abertura SHA256 `{opening}`. UTC {now}.

Recebido job `{receipt['job_id']}`, Kimi K3 máximo:
{receipt['usage']['prompt_tokens']} tokens entrada/{receipt['usage']['completion_tokens']} saída,
{receipt['usage']['total_tokens']} total. A resposta é preservada integralmente,
com o recibo e SHA. O Kimi entregou uma redução parcial e deixou F²/48
sem reduzir; o total conforme e o limite plano coincidiam com a bancada.

**A concordância desses controles não bastou.** A primeira tentativa local
usou a diferença entre a fórmula completa existente e a parcial do Kimi
para inferir F². Falhou em rc1 no par T=H=e00, ordemK: resíduo3/4.
O script/log v1 permanece. No v2, os coeficientes de F² foram extraídos
diretamente da contração de palavras covariantes, depois conferidos nos55
pares da base simétrica, nas ordens p⁴,Kp²,K² e num controle denso não axial.
O ajuste anterior ao teste é declarado; não é uma avaliação cega.

Com tau=trh, L=divh e Psi=divL, módulo divergências:

 tr(F²)/48 = -(Boxh)²/12+(Boxtau)²/24-Psi Boxtau/8
             -5 L BoxL/24-Psi²/24
             +K[7hBoxh/12+L²/6-7Psi tau/24-3tau Boxtau/32]
             +K²[-2h²/3+tau²/6].

O erro da parcial foi localizado em gamma=tr(B-Boxh)²/8. A forma corrigida é

 gamma = [Psi²+2 LBoxL+(Boxtau)²/4+(Boxh)²
          +K(7L²+9Psi tau-5tau Boxtau/4)]/8.

O modelo escrevera 5Psi tau e -tau Boxtau/4 dentro dos colchetes.
A correção total é K(Psi tau/2-tau Boxtau/8). Ela some para h=f g e
para TT, explicando por que os dois controles do texto não a detectavam.
A nova expressão gamma passou165 controles exatos; a antiga falha em26.

**Derivação algébrica curta.** C=L-gradtau/2, B=gradC. Pela integração
por partes em Ric=3Kg, tr(B²) equivale a
Psi²-Psi Boxtau+(Boxtau)²/4-3KL²-3KPsi tau+3Ktau Boxtau/4.
Usando div(Boxh)=BoxL+5KL-2Kgradtau e div(BoxL)=BoxPsi+3KPsi,
-2tr(B Boxh) equivale a
2LBoxL+Psi Boxtau+10KL²+12KPsi tau-2Ktau Boxtau.
Somando (Boxh)², obtém-se gamma acima. Nenhuma troca de derivadas
por momentos comutativos foi usada no controle curvo.

Também corrigido o sinal impresso da integração por partes:
int L BoxL = -int h^(ab) nabla_a Box nabla^r h_rb.
O sinal positivo do texto deixa diferença-4 num controle plano exato.
A parcela F² contribui nas três ordens; suprimi-la falha em três controles.

Com a correção, a soma reproduz a densidade integrada já registrada em
ghost_curved_hessian/DERIVACAO.md; não altera essa entrega anterior.
O controle conforme de F² dá K f Boxf/8, e o completo permanece
7(Boxf)²/8+19K f Boxf/2, módulo divergências.

O exemplo CE2 do modelo compara E1+E2, não o determinante do produto de
operadores: não demonstra anomalia multiplicativa. A corrente D2 exige
tr(Omega0 hA), não Omega0 tr(hA). São ressalvas de leitura, não novos
teoremas analíticos. As hipóteses do resíduo de calor permanecem explícitas.

Resultado: {checks} controles reportados/{neg} negativos, rc0 nos v2/gamma,
CPU{cpu}s; o custo de CPU da tentativa falha não foi medido. O conjunto
não é uma prova de determinantes finitos, identidade pontual, contatos de
cutoff nem Q2 completo. Gate e originais intactos. Próximo: voltar à
integração por partes bilocal, mantendo estas correções como verificação
do setor ghost e sem contaminar o parecer MiMo já em andamento.
'''
write(report,text.encode())
files={Path(__file__),report,H/'kimi_ghost_reduction_audit.py',H/'kimi_ghost_reduction_audit_run.log',
       H/'kimi_ghost_reduction_audit_v2.py',H/'kimi_ghost_reduction_audit_v2_run.log',
       H/'kimi_ghost_gamma_check.py',H/'kimi_ghost_gamma_run.log'}
for stem in ['kimi_ghost_reduction_audit','kimi_ghost_reduction_audit_v2','kimi_ghost_gamma']:
    files.update((H/stem).glob('*.json'));files.update((H/stem).glob('*.md'))
    p=H/stem/'manifest.json'
    if p.exists():
        for a in json.loads(p.read_bytes())['artifacts']:
            p=Path(a['path']);assert sha(p)==a['sha256'];files.add(p)
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks=checks,negative_controls=neg,
    cpu_seconds=cpu,full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in sorted(files)]))
ledger=O/'LEDGER_016.jsonl'
events=[dict(at=now,event='KIMI_GHOST_REDUCTION_RECEIVED_AND_AUDITED',provider='kimi',
    target='A7.b',job_id=receipt['job_id'],execution_task_id=receipt['execution_task_id'],
    tokens=receipt['usage'],cost_estimate_usd=None,response_sha256=receipt['response_sha256'],
    request_id='cbb53fdd-b01c-4148-9dc3-6c4fdab63956',
    prompt_sha256=hashlib.sha256(json.loads((H/'orchestration_ghost_reduction/kimi_a7_ghost_curved_hessian_reduction_submit.json').read_bytes())['prompt'].encode()).hexdigest(),
    full_Q2=False,checks=checks,negative_controls=neg,cpu_seconds=cpu,
    delivery_manifest_sha256=sha(D/'manifest.json'))]
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()];parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(row):return [str(row[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if row.get(k)]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row);cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and cost is not None:known[root(ix[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,known_partial_usd=str(total),ledger_sha256=sha(ledger),unknown_not_zero=True))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: Kimi ghost recebido, parcelaF² reduzida diretamente e dois coeficientes mistos de gamma corrigidos. {checks}checks/{neg}negativos,CPU{cpu}s,rc0; v1rc1preservado. Custo parcialUS${total}; desconhecidos não zerados. Q2 OPEN.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',kimi_ghost_reduction_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total))
v['completed_this_turn']=['Kimi ghost438176 tokens received;partial curvature mismatch measured',
    'F² directly reduced,172checks;gamma corrected165checks;30negative controls total',
    'Old complete ghost density unchanged;both conformal and TT controls blind to model error']
v['next']=['Continue bilocal Y differentiation before anchoring; new paired kernels available',
    'Keep MiMo independent review unchanged; do not inject the Kimi corrections into its prompt',
    'A7.b timebox then A7.c/d,A8,PartB and final audit remain required']
put(p,v,True)
print(json.dumps(dict(artifacts=len(files),checks=checks,negative_controls=neg,cpu_seconds=cpu,full_Q2=False)))
