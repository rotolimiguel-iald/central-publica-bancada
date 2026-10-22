from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode() if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2).encode()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp);b.write_bytes(old);assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(raw);assert raw and t.read_bytes()==raw;t.replace(p)
proofs=[]
for name,label,count in [('TheEquationOfTruth.lean','equation_reproduction_01',46),('AxiomasContorno.lean','contour_reproduction_01',7)]:
    p=HERE/'A_reproducao';r=json.loads((p/(label+'.json')).read_bytes());a=json.loads((p/(label+'_audit.json')).read_bytes())
    assert r['rc']==0 and a['auditoria']=='PASSA' and a['n_declaracoes_auditadas']==count
    assert not r['newer_kernel_files'] and not r['scan_errors']
    assert r['source_sha256']==sha(p/name) and r['log_sha256']==sha(p/(label+'.log'))
    proofs.append(dict(source=str(p/name),source_sha256=sha(p/name),log=str(p/(label+'.log')),log_sha256=sha(p/(label+'.log')),receipt=r,audit=a))
insumo=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/V3_pre_resolucao_lean/TheEquationOfTruth.lean'
assert insumo.read_bytes()==(HERE/'A_reproducao/TheEquationOfTruth.lean').read_bytes()
wall=sum(x['receipt']['wall_seconds'] for x in proofs);cpu=sum(x['receipt']['cpu_user_seconds']+x['receipt']['cpu_kernel_seconds'] for x in proofs)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md');now=datetime.now(timezone.utc).isoformat()
m=dict(at=now,status='REAL_REPRODUCED_A6A',opening_sha256=opening,proofs=proofs,wall_seconds=wall,cpu_seconds=cpu,
       source_prefix_bytes=len(insumo.read_bytes()),original_source_sha256=sha(insumo),kernel_changed=False,gate_changed=False)
save(HERE/'A_reproducao/reproduction_manifest.json',m)
prices={}
for e in map(json.loads,(OUT/'LEDGER_016.jsonl').read_text(encoding='utf-8-sig').splitlines()):
    k=e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('custo_usd'))
    if k and v is not None:
        try:prices[k]=Decimal(str(v))
        except Exception:pass
cost=sum(prices.values(),Decimal(0))
save(OUT/'ENTREGA_016_A6_A_reproducao.md',f'''[REAL — reprodução isolada e auditoria]
# A6.A — Pedra reproduzida
Abertura SHA256 `{opening}`.

PAGO: fonte original copiada byte a byte, {len(insumo.read_bytes())} bytes,
SHA256 `{sha(insumo)}`. Compilação rc0: 46 teoremas, 46 entradas auditadas,
somente axiomas do trio, zero erros/admissões e 15 avisos preservados.
Não houve necessidade da variante só-Mathlib. O olean não é usado como
critério de identidade entre caminhos.

Contorno: sete declarações existentes importadas e auditadas, todas dentro
do trio (duas sem axiomas). Este arquivo audita o olean disponível;
não recompila a fonte canônica do Contorno.

90 insumos do A6 conferidos contra o manifesto. Comandos completos,
fontes/logs/axiomas e recursos estão em A_reproducao/reproduction_manifest.json,
SHA256 `{sha(HERE/'A_reproducao/reproduction_manifest.json')}`.
Reprodução: compile_isolated_v2.py kernel fonte label, fora do kernel;
auditar_axiomas.py fonte log. Fontes originais e kernel sem alteração.
Máquina {wall:.6f}s parede / {cpu:.6f}s CPU, bancada não exclusiva;
estimativas remotas acumuladas US${cost}, incompletas.

Não move gate. Trata-se de semigrupo dissipativo e conservação da leitura;
não é identificação com o fluxo modular nem uma prova do par físico H2/H3.
Segue B5 → B2a → B2b → B7 → B4 na ordem fixada.
''')
prepared=json.loads((HERE/'orchestration_v2/prepared_units.json').read_bytes())
ack=dict(at=now,status='ACCEPTED_STAGING_WAITING_EXISTING_CAPACITY',source='official send_message_to_thread response',
         coordinator_thread='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',active_jobs_reported=5,
         jobs_created=0,external_calls_started=0,requests=[x['request_id'] for x in prepared],
         old_preparation='Rejected locally before submit: 24000-character prompt validation. No remote call; old IDs excluded from staging.')
save(HERE/'orchestration_v2/coordinator_acknowledgment.json',ack)
rows='\n'.join(f"- {x['provider']}: {x['slug']} — `{x['request_id']}`." for x in prepared)
save(OUT/'ENTREGA_016_ORQUESTRACAO_A6_novas_unidades.md',f'''[REAL — preparação/prévia; INPUT — tarefas autorizadas]
Abertura SHA256 `{opening}`.

Três novas unidades delimitadas, com memória comum, executor travado e uma
chamada por unidade. Prévia selecionou o executor exigido:
{rows}

Coordenação confirmou staging, após as unidades A5 anteriores; cinco jobs
ativos na fila no recibo. Ainda nenhum job A6 criado nem execução iniciada.
Não se criou outra fila/worker. IDs e payloads preservados em
orchestration_v2/prepared_units.json, SHA256 `{sha(HERE/'orchestration_v2/prepared_units.json')}`.
Preparação anterior excedeu limite de prompt e falhou ANTES de submissão;
preservada, excluída do despacho e sem chamada remota. A versão atual usa
trechos dirigidos e conserva a memória comum em modo máximo.
''')
p=OUT/'ENTREGA_016_PROGRESSO.md';old=p.read_text(encoding='utf-8-sig');tag='A6A_REPRODUCTION_20260924'
if tag not in old:save(p,old+f'\n- {now} — A6.A PAGO: 46 teoremas reproduzidos + 7 entradas do Contorno auditadas. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU; 15 warnings, zero erro, kernel intacto. Custos explícitos US${cost}, incompletos. Três unidades A6 em staging (Kimi2/MiMo1), sem execução nova. Próximo B5/B2a/B2b. [{tag}]\n')
print(json.dumps(dict(reproduced_theorems=46,imported_audit_entries=7,wall_seconds=wall,cpu_seconds=cpu,new_staged_units=len(prepared))))
