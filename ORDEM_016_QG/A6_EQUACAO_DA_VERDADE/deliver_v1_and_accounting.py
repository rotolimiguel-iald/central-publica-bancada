from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json

HERE=Path(__file__).resolve().parent
OUT=HERE.parent.parent/'TUNEL/DO_CHATGPT'
D=HERE/'D_harness/refeito_V1'
REF=HERE.parent.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/V1_verificacao_independente'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=v if isinstance(v,bytes) else (v.encode('utf-8') if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp);b.write_bytes(old);assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(raw);assert t.read_bytes()==raw and raw;t.replace(p)

r=json.loads((D/'reproduction_receipt.json').read_bytes())
assert r['rc']==0 and r['n_pass']==51 and r['n_detected']==9
comparisons=[]
for own,ref in [('verifica_equacao_da_verdade.py','verifica_equacao_da_verdade.py'),
                ('reproduction.log','log_V1.txt'),('resultados_V1.json','resultados_V1.json')]:
    assert (D/own).read_bytes()==(REF/ref).read_bytes(),(own,ref)
    comparisons.append(dict(local=str(D/own),reference=str(REF/ref),sha256=sha(D/own),byte_identical=True))
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes()
events=[json.loads(l) for l in old.decode('utf-8-sig').splitlines() if l.strip()]
costs={}
for e in events:
    c=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    if c is not None:
        key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
        if key: costs[key]=Decimal(str(c))
cost=sum(costs.values(),Decimal(0))
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(status='REAL_D1_REPRODUCED',at=now.isoformat(),opening_sha256=opening,
              comparisons=comparisons,receipt=r,reported_estimates_usd=str(cost),accounting_complete=False,
              limitations=['C29 checks scalar limits only, not an infinite-dimensional operator construction',
                           'Derivative grid has 16 high-precision points, not interval certification',
                           'expand_log force identity is interpreted only on the stated positive real domain'],
              d2='PRE_REGISTERED_NOT_EXECUTED',gate_changed=False)
save(D/'reproduction_manifest.json',manifest)
save(OUT/'ENTREGA_016_A6_D1_reproducao.md',f'''[REAL — reprodução byte-idêntica do harness V1]

# A6.D1 — reprodução verificada

Abertura SHA256: `{opening}`.

Copiado somente o script para a bancada, depois executado com UTF-8 e SymPy {r['sympy']}. Resultado medido: rc0, {r['n_pass']}/{r['n_checks']} verificações e {r['n_detected']}/{r['n_controls']} controles detectados. Tempo {r['wall_seconds']:.6f}s de parede. Fonte, log e JSON de resultados foram comparados byte a byte aos originais somente após a execução; os três são idênticos. Hashes no manifesto.

Escopo conferido: C29 mede limites escalares; seu título não constitui construção do operador em ℓ² nem prova geral de convergência forte. A derivada entrópica foi medida em 16 pontos a 50 dígitos, sem aritmética de intervalos. A identidade com expand_log(force=True) exige o domínio real positivo do enunciado. Essas limitações não foram apagadas pelo total PASS.

D2 permanece em construção independente; pré-registro em D_harness/D2_PRE_REGISTRO.json, semente declarada antes da geração. O pacote externo “22/22 + 5” continua NÃO_VERIFICÁVEL nesta rodada.

Correção ao lado da linha A6.C do progresso: o somatório US$0 ali foi erro do agregador, que só aceitava valores numéricos e omitia execution_task_id. O ledger guarda também custos como strings. Refeito por Decimal e identificação por unidade: US${cost}, estimativa incompleta, não fatura; Kimi por assinatura não é custo zero. Nenhuma execução externa nova foi criada por esta reprodução.

Manifesto: `{D/'reproduction_manifest.json'}`.
Nenhum um.py, kernel ou gate alterado.
''')
marker='A6_D1_AND_ACCOUNTING_CORRECTION_20260924'
if marker.encode() not in old:
    e=dict(event=marker,at=now.isoformat(),manifest=str(D/'reproduction_manifest.json'),manifest_sha256=sha(D/'reproduction_manifest.json'),
           external_execution=False,wall_seconds=r['wall_seconds'],reported_estimates_usd=str(cost),accounting_complete=False)
    save(ledger,old+(json.dumps(e,ensure_ascii=False)+'\n').encode())
p=OUT/'ENTREGA_016_PROGRESSO.md';raw=p.read_bytes()
if marker.encode() not in raw:
    line=f'\n- {now.isoformat()} — A6.D1 PAGO: 51/51 + 9/9; fonte/log/JSON byte-idênticos. Máquina {r["wall_seconds"]/3600:.6f}h parede; bancada não exclusiva. Correção ao lado do custo A6.C: US${cost}, incompleto (não zero; valores string e execution_task_id omitidos antes). Semente D2 pré-registrada, execução ainda pendente. Abertura {opening}. Não move gate. [{marker}]\n'
    save(p,raw+line.encode())
ack=dict(at=now.isoformat(),source_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
         status='STAGED_CAPACITY_PENDING',active_jobs_reported=5,new_calls_for_review_units=0,
         request_ids=[u['request_id'] for u in json.loads((HERE/'orchestration_reviews/prepared_units.json').read_bytes())],
         scope='Official message acknowledgment; no job_id assigned yet; preserve order behind previous A6 catalogs')
save(HERE/'orchestration_reviews/coordinator_acknowledgment.json',ack)
print(json.dumps(dict(status=manifest['status'],all_byte_identical=True,estimated_costs=str(cost))))
