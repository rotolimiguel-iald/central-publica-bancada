"""Deliver the checked reference-transfer correction without changing prescriptions."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid
H=Path(__file__).resolve().parent
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'harmonic_reference_delivery'
D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc); stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    if p.exists():
        assert replace,p
        old=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists(); bak.write_bytes(old); assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b); assert b and t.read_bytes()==b; t.replace(p)
def append(p,s):
    old=p.read_bytes(); write(p,old+s.encode('utf-8'),True)
    assert p.stat().st_size>len(old)
artifacts={}; data=[]; logs=[]
for name in ['harmonic_reference_audit','principal_harmonic_bridge']:
    m=H/name/'manifest.json'
    for row in json.loads(m.read_bytes())['artifacts']:
        p=Path(row['path']); assert sha(p)==row['sha256']; artifacts[str(p)]=sha(p)
    artifacts[str(m)]=sha(m)
    r=json.loads((H/name/'results.json').read_bytes())
    log=H/(name+'_run.log')
    assert json.loads(log.read_text('utf-8-sig').splitlines()[-1])==r
    data.append(r); artifacts[str(log)]=sha(log)
    logs.append(dict(command=f'A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/{name}_check.py',rc=0,log=str(log),sha256=sha(log)))
receipt=json.loads((H/'harmonic_reference_audit/RECEIPT.json').read_bytes())
assert sha(Path(receipt['source']))==receipt['source_sha256']
assert sha(H/'harmonic_reference_audit/KIMI_RESPONSE.md')==receipt['response_sha256']
for p in [Path(__file__),H/'harmonic_reference_audit/DERIVACAO.md',H/'harmonic_reference_audit/RECEIPT.json']:
    artifacts[str(p)]=sha(p)
checks=sum(r['checks'] for r in data); cpu=sum(r['cpu_seconds'] for r in data)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
    artifacts=[dict(path=p,sha256=h) for p,h in sorted(artifacts.items())],logs=logs,
    full_Q2=False,prescription_changed=False,gate_changed=False)
write(D/'manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
note=f'''[DERIVED — transferência de referência com termo local preservado]

{now.isoformat()}. Abertura SHA256 {opening}.

O parecer Kimi harmonic_reference_intertwining foi lido integralmente.
Sua separação entre parte local e parte não local não é única. A igualdade
das distribuições implica, na mesma prescrição R:

    D_H-X_P-D_rem=C_E(N_P+N_rem-N_H)delta.

Contraexemplo exato: F=deriv_i²(1/z), com resto zero, tem
D_H-X_P=-C_E delta/4. Portanto não se pode descartar essa diferença.

Para todo polinômio quartico P(q), nos35 elementos da base:

    N_P-N_H=-3q² Lap(P)/128-q⁴ Lap²(P)/9216.

Aplicação ao P4 da Hessiana já medido, na base de cinco invariantes
definida na derivação: N_P-N_H=(47/192,71/768,-5/128,-1/4,0).
Sua contração longitudinal não é zero. Preservar esse termo evita
alterar artificialmente a soma de Ward. Trata-se de duas representações
do mesmo P4U2; não de dois diagramas a somar nem de toda a bolha.

O exemplo harmônico do parecer conserva o contato anunciado, mas
tem resíduo UV tensorial não nulo. Média angular sem peso zero não
implica resíduo completo zero. A nota registra ambas as verificações.

Evidência: {checks} igualdades/controles exatos; CPU{cpu}s; dois comandos rc0.
Derivação: {H/'harmonic_reference_audit/DERIVACAO.md'}.
Manifesto: {D/'manifest.json'}; SHA256 {sha(D/'manifest.json')}.
Não são experiências independentes nem nova compilação Lean.

Q2 completa permanece OPEN. Normalização lorentziana, amostras curvas
do parecer e identificação do kernel completo com P4U2 não foram provadas
nesta auditoria. Nenhum original, kernel ou gate alterado.
'''
write(OUT/'ENTREGA_016_A7b_transferencia_harmonica_com_contato.md',note.encode())
write(OUT/'ENTREGA_016_MEDIDA_unicidade_da_separacao.md',f'''[REAL — MEDIDA da separação local/não local]

{now.isoformat()}. Abertura SHA256 {opening}.
Tentativa: inferir igualdade separada de partes locais e não locais.
Resultado: refutada; deriv_i²(1/z) produz diferença -C_E delta/4.
Rota seguinte: manter a identidade distribucional inteira e o defeito
de referência na soma. Aplicação ao P4 efetivo já medida.
Comandos, rc e hashes dos logs: {json.dumps(logs,ensure_ascii=False)}.
CPU{cpu}s. Nenhuma chamada remota nova; parecer recebido anteriormente
auditado aqui. Custo da assinatura Kimi desconhecido, não zero.
'''.encode())
ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(s) for s in ledger.read_text('utf-8-sig').splitlines() if s.strip()]
if not any(r.get('execution_task_id')==receipt['execution_task_id'] for r in rows):
    event=dict(receipt,at=now.isoformat(),provider='kimi',target='A7.b',
        event='RECEIVED_REPLY_AUDITED_REFERENCE_TRANSFER',remote_call=False)
    append(ledger,json.dumps(event,ensure_ascii=False)+'\n')
append(ledger,json.dumps(dict(at=now.isoformat(),event='A7_HARMONIC_REFERENCE_TRANSFER',
    target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,
    manifest_sha256=sha(D/'manifest.json'),full_Q2=False),ensure_ascii=False)+'\n')
seen=set(); cost=Decimal(0)
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip(): continue
    r=json.loads(line); v=r.get('cost_estimate_usd')
    if v is None: v=r.get('cost_usd')
    if v is None: continue
    key=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
    if key and key in seen: continue
    if key: seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: transferência harmônica corrigida, defeito local aplicado ao P4; {checks}checks CPU{cpu}s; custo parcial US${cost}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json'; c=json.loads(p.read_bytes())
c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['Kimi harmonic reference review audited; false uniqueness rejected',
        'Quartic trace defect measured and transferred to existing principal Hessian'],
    harmonic_reference_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(cost),
    next=['Read and audit received Fourier review','Assemble remaining Ward contributions before A7b deadline2026-09-25T20:32Z',
          'A7c/d, A8, PartB and final report still outstanding'],own_live_processes=[])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode(),True)
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,artifacts=len(artifacts),cost_partial=str(cost),manifest_sha256=sha(D/'manifest.json'))))
