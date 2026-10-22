"""Record the smooth-reference audit and algebraic rotation obstruction."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import ast,hashlib,json,uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'smooth_rotation_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat()
# Reuse only custody helpers; never import the prior delivery's side effects.
helper=H/'deliver_contact_frame_and_cutoff.py'
tree=ast.parse(helper.read_text('utf-8'))
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'sha','write','put'}]
assert len(defs)==3
exec(compile(ast.Module(body=defs,type_ignores=[]),str(helper),'exec'))
names=['smooth_reference_transport_audit','smooth_source_rotation']
rs={n:json.loads((H/n/'results.json').read_bytes()) for n in names}
files=[Path(__file__),helper,H/'smooth_source_rotation/DERIVACAO.md']
for n in names:
    mp=H/n/'manifest.json';files.append(mp)
    for row in json.loads(mp.read_bytes())['artifacts']:
        p=Path(row['path']);assert sha(p)==row['sha256'];files.append(p)
    files.append(H/(n+'_run.log'))
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
count=sum(r['checks'] for r in rs.values());cpu=sum(r['cpu_seconds'] for r in rs.values())
report=O/'ENTREGA_016_A7b_referencia_suave_rotacao_e_transporte.md'
write(report,f'''[DERIVED — contração geral da fonte suave e companheiro BRST; Q2 completa OPEN]

Data {now}. Abertura SHA256 {opening}.

O contato suave da fonte foi estendido do controle isotrópico para todos
os 55 componentes algébricos de W_ab|cd no ponto de coincidência.
A contração original do vértice foi conferida em 8.800 coeficientes.
Com S_ar=sum_m W_am|rm, M_jr=grad_j c_r e Omega=(M-M^T)/2, obteve-se

    R_W(M)=L_W(M+M^T)-[Omega,S]/4,
    L_W(H)=-(SH+HS+2W_cross(H)-2W_direct(H))/8.

O contato fatora pelo gerador de gauge simétrico em toda a fibra se,
e somente se, S é escalar. O mapa do defeito tem posto9 e núcleo
gerado pela identidade. Não se exige que W inteiro seja isotrópico.
O termo restante é a parte rotacional da variação da referência.
Isso identifica uma obrigação de transporte, não uma anomalia física.

No caso isotrópico, L_W=aI+b g tr, com a=-(wI+wT)/2 e
b=-wI/8+wT/4, reproduz o resultado anterior. O gerador de ghost-1
F_W=integral hdagger.L_W h fornece o par de ação de ghost0

    s0F_W=integral(Eh).L_W h-hdagger.L_W Gc.

A Hessiana companheira N_W=E L_W+L_W E satisfaz N_W G=E R_W no
recorte testado. É uma construção explícita de companhia BRST para
essa fonte; não foi identificada com a soma dos diagramas suaves.
Não deve ser confundida com a anomalia de ghost1.

## Auditoria do Kimi

A chamada smooth_reference_ward_transport foi recebida e lida. Sua
fórmula com alpha_W somente nas entradas perde hbar*W já para dois
funcionais lineares. A conjugação correta, no modelo bosônico testado,
é alpha_W T_D(alpha_W^-1 F,alpha_W^-1 G). Ela passou em todas as
potências de0a4. Os sinais ghost não foram certificados por esse teste.
Também não se troca o operador gauge-fixado por E_phys sem o elo próprio.

Total local: {count} verificações, CPU{cpu}s; rc0 nos dois scripts.
Controles negativos: perda de hbar*W; diferença-1/4 entre jatos com
o mesmo Gc; omitir a parcela rotacional perde-1/8 no exemplo dado.
Referência/estado físico não foram escolhidos; nenhum W arbitrário foi
declarado bisolução física. Fontes e logs: {D/'manifest.json'}.

Próximo passo: confrontar esse companheiro com bolhas mistas singular/suave
e com o transporte completo dos jatos. Persistem W geral, outros locais,
K², aridades e continuação lorentziana. Originais, kernel e gate intactos.
''')
measure=O/'ENTREGA_016_MEDIDA_rotacao_da_referencia_suave.md'
write(measure,f'''[REAL — fatoração medida e controle negativo preservado]

Data {now}; abertura SHA256 {opening}.
Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/smooth_source_rotation_check.py; rc0;
log SHA256 {sha(H/'smooth_source_rotation_run.log')}.

Identidade exata: R_W(M)=L_W(Gc)-[Omega,S]/4. O mapa simétricoS para
o defeito tem posto9, núcleo escalar. W=diag(1,0,0,0) tensor ela mesma
produz diferença-1/4 entre R_01 para M_10 e M_01, embora Gc seja igual.
Sem pressupor admissibilidade de estado desse dado algébrico.

Próximo ramo: calcular os demais termos suaves/companheiros e preservar
o transporte rotacional. Nenhuma nulidade de anomalia inferida. CPU local
total da entrega{cpu}s; nenhuma nova chamada externa. A assinatura do
Kimi não tem custo monetário atribuível informado, nunca assumido zero.
''')
files += [report,measure];files=list(dict.fromkeys(files))
put(D/'manifest.json',dict(at=now,checks=count,cpu_seconds=cpu,opening_sha256=opening,
    full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
receipt=json.loads((H/'smooth_reference_transport_audit/RECEIPT.json').read_bytes())
prompt_path=H/'orchestration_harmonic_followup/kimi_a7_smooth_reference_ward_transport_submit.json'
payload=json.loads(prompt_path.read_bytes())
ledger=O/'LEDGER_016.jsonl'
events=[dict(at=now,event='A7_SMOOTH_SOURCE_ROTATION_AND_TRANSPORT_LOCAL_AUDIT',
    target='A7.b',checks=count,cpu_seconds=cpu,remote_call=False,full_Q2=False,
    manifest_sha256=sha(D/'manifest.json')),
    dict(at=now,event='KIMI_SMOOTH_REFERENCE_RECEIVED_AND_AUDITED',provider='kimi',target='A7.b',
      job_id=receipt['job_id'],execution_task_id=receipt['execution_task_id'],
      request_id=payload['request_id'],tokens=receipt['usage'],
      cost_estimate_usd=None,cost_status=receipt['cost_status'],
      prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
      response_sha256=receipt['response_sha256'],new_remote_execution=False)]
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
for r in rows:
    keys=ids(r)
    for k in keys[1:]:parents[root(k)]=root(keys[0])
known={}
for r in rows:
    keys=ids(r);cost=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    if keys and cost is not None:known[root(keys[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,known_partial_usd=str(total),unknown_not_zero=True,ledger_sha256=sha(ledger)))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: fonteW geral, rotação/strain e companheiroBRST tipado; KimiWick auditado. {count}checks,CPU{cpu}s; custo parcial US${total}, desconhecidosnãozero. Soma suave/Q2 OPEN.\n'.encode(),True)
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
state.update(at=now,previous_goal_turn='PROGRESS',own_live_processes=[],
    smooth_rotation_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total),
    quantum_anomaly_computed=False,
    completed_this_turn=['General W source tensor factorization and rotation defect; exhaustive55-dimensional basis',
        'Constructed typed ghost-number0 BRST action companion for isotropicW',
        'Kimi Wick input-only transport refuted; correct bosonic conjugation tested'],
    next=['Calculate singular/smooth mixed bubble contacts and compare with typed companion',
          'Audit Kimi harmonic and future bilocal/source reviews',
          'A7.b deadline2026-09-25T20:32Z; then A7.c/d,A8,PartB and full final audit'])
put(p,state,True)
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
print(json.dumps(dict(checks=count,cpu_seconds=cpu,artifacts=len(files),
    known_partial_usd=str(total),provider_usage=receipt['usage'],goal='ACTIVE',full_Q2=False)))
