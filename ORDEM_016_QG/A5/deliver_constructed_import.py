from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import json, hashlib, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'A0'))
from auditar_axiomas import audita
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode('utf-8') if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+stamp); bak.write_bytes(old); assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+stamp); temp.write_bytes(raw); assert temp.read_bytes()==raw and raw; temp.replace(p)
proofs=[]
for name,label in [('NullSolutionConsumerReuse.lean','null_solution_consumer_01'),('ConstructedImportH3_v2.lean','constructed_import_h3_02'),('EmptyImportControl.lean','empty_import_control_01')]:
    source=HERE/name; log=HERE/(label+'.log'); receipt_path=HERE/(label+'.json')
    receipt=json.loads(receipt_path.read_bytes()); audit=audita(str(source),str(log))
    assert receipt['rc']==0 and audit['auditoria']=='PASSA'
    assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
    assert receipt['source_sha256']==sha(source) and receipt['log_sha256']==sha(log)
    proofs.append(dict(source=str(source),source_sha256=sha(source),log=str(log),log_sha256=sha(log),receipt=receipt,audit=audit))
negative=json.loads((HERE/'empty_index_rejected_01.json').read_bytes())
negative_log=HERE/'empty_index_rejected_01.log'
assert negative['rc']!=0 and 'synthesize placeholder' in negative_log.read_text(encoding='utf-8')
assert 'ContratoH2 W R N' in negative_log.read_text(encoding='utf-8')
assert negative['source_sha256']==sha(HERE/'ProbeEmptyIndexRejected.lean') and negative['log_sha256']==sha(negative_log)
assert not negative['newer_kernel_files'] and not negative['scan_errors']
attempts=[]
for pattern in ['null_solution_consumer_*.json','constructed_import_h3_*.json','empty_import_control_*.json','empty_index_rejected_*.json']:
    for p in HERE.glob(pattern):
        r=json.loads(p.read_bytes())
        if 'rc' in r: attempts.append(dict(path=str(p),sha256=sha(p),receipt=r))
wall=sum(x['receipt']['wall_seconds'] for x in attempts)
cpu=sum(x['receipt']['cpu_user_seconds']+x['receipt']['cpu_kernel_seconds'] for x in attempts)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'); now=datetime.now(timezone.utc).isoformat()
prices={}
for e in map(json.loads,(OUT/'LEDGER_016.jsonl').read_text(encoding='utf-8-sig').splitlines()):
    key=e.get('job_id') or e.get('request_id'); value=e.get('cost_estimate_usd',e.get('custo_usd'))
    if key and value is not None:
        try: prices[key]=Decimal(str(value))
        except Exception: pass
cost=sum(prices.values(),Decimal(0))
incoming=[]
for p in sorted((OUT.parent/'PARA_CHATGPT').glob('*.md'),key=lambda p:p.stat().st_mtime,reverse=True)[:10]:
    incoming.append(dict(name=p.name,sha256=sha(p),mtime_ns=p.stat().st_mtime_ns))
save(HERE/'incoming_at_constructed_import_delivery.json',incoming)
manifest=dict(at=now,status='REAL_CONDITIONAL_IMPORT_WITH_SCOPED_NEGATIVE_CONTROL',opening_sha256=opening,
              proofs=proofs,negative=negative,attempts=attempts,lean_audit_entries=9,
              wall_seconds=wall,cpu_seconds=cpu,physical_h2_constructed=False,gate_changed=False,
              exact_original_probe_recompiled=False,
              original_probe_limit='The complete legacy/toy dependency graph remains the A1 memory MEDIDA. Generalized same index attack compiled and rejected at the missing H2 index.')
save(HERE/'constructed_import_manifest.json',manifest)
report=f'''[REAL — compilação isolada; DERIVED — import condicional no tipo original]
# A5.e — Propagador construído ligado ao import H3
Abertura SHA256 `{opening}`.

**PAGO no escopo condicional.** `construct_import` produz o tipo original
`ContratoImportH3 W R N T h2`, reutilizando `construct_null_solution` e os
corpos originais de `responseOf`, `areaDensity_responseOf` e
`H3_of_null_solution`. `same_horizon` fecha por `rfl`.

As hipóteses são explícitas: H2 do par; G positivo fixo; classe A de estados
unitários, incluindo o vácuo e estável por translações; continuidade e
integrabilidade absoluta das caudas de ordens zero e um do tensor T.
Há ainda o elo modular, energia não trivial e tela plana **para todo H2
admissível do mesmo par**, porque o campo `produce` tem esse quantificador.
Não reduzimos esse campo ao H2 que indexa o import.

**Controle do vazio:** provado que U(nullDir)=1 exclui H2 fiel e, portanto,
exclui o par dependente (h2, import indexado por h2). Uma função que recebe
esse H2 impossível continua definível, mas não fornece o índice.
O ataque `(Classical.choice ⟨_⟩)` recompilado contra o contrato original
foi rejeitado exatamente no argumento H2 ausente: rc 1, `synthesize placeholder`.
Não foi um erro de import/dependência.

**MEDIDA preservada:** esta sonda é uma generalização do ataque da v3.1.
Não recompilamos os dois exemplos completos legado/brinquedo de
`ProbeVacuousImportV31`: a cadeia integral deles segue a limitação de memória
registrada em A1. O teorema geral cobre a hipótese que ambos utilizam;
nesta rodada não afirmamos ter revalidado suas instanciações completas.

Três módulos finais rc0, 9 entradas auditadas somente com o trio permitido;
cinco tentativas totais, incluindo o negativo esperado. Uma tentativa falhou
por nome não qualificado `solderMetric4`; a versão seguinte acrescentou apenas
`TGLExt.` e passou. Fontes/logs/recibos estão no manifesto.
Máquina: {wall:.6f}s parede e {cpu:.6f}s CPU; bancada não exclusiva.
Custos remotos explícitos acumulados US${cost}, incompletos, sem nova chamada.

**Não move o gate:** não construímos H2 físico, não escolhemos tensor T0,
não descarregamos o elo modular para esse tensor. A construção é um termo
condicional do contrato exato, não um pagamento incondicional do par físico.
Próximo: A6, equação da verdade, reutilizando a pedra de 46 teoremas.

Manifesto `{HERE/'constructed_import_manifest.json'}`
SHA256 `{sha(HERE/'constructed_import_manifest.json')}`.
'''
save(OUT/'ENTREGA_016_A5e_import_construido.md',report)
parts=[('A5.a','ENTREGA_016_A5a_dados_mesmo_horizonte.md','PAGO como leitura campo a campo; usa H3, não H2 sozinho'),
       ('A5.b','ENTREGA_016_A5b_propagador_teleologico.md','PAGO sob continuidade e integrabilidade nomeadas'),
       ('A5.c/c′','ENTREGA_016_MEDIDA_A5c_elo_modular_e_traco.md','MEDIDA no elo físico; PAGO no condicional nomeado; extensão canônica de traço já existente preservada'),
       ('A5.d','ENTREGA_016_A5d_primeira_ordem_dois_corpos.md','PAGO como harness exato e lema bilateral'),
       ('A5.e','ENTREGA_016_A5e_import_construido.md','PAGO condicional; reprodução integral do probe original permanece MEDIDA')]
rows='\n'.join(f'| {branch} | {status} | `{sha(OUT/name)}` |' for branch,name,status in parts)
save(OUT/'ENTREGA_016_A5_RELATORIO.md',f'''[REAL — consolidação de resultados com escopos explícitos]
# A5 — H3 no mesmo horizonte
Abertura SHA256 `{opening}`.

| Ramo | Resultado | SHA256 da entrega |
|---|---|---|
{rows}

A cadeia construída é: condições sobre T/A → solução teleológica nn →
resposta matricial covariante → H3 → import indexado, preservando o mesmo
horizonte. O elo entre a carga de T0 e o gerador físico permanece hipótese
nomeada. As duas primeiras setas não o demonstram por si.

Não move os itens físicos restantes nem o gate. Não alterado um.py/kernel.
Listagem de entradas relida em incoming_at_constructed_import_delivery.json;
nenhuma ratificação nova dos índices físicos foi usada. Segue A6.
''')
tag='A5E_CONSTRUCTED_IMPORT_20260924'
p=OUT/'ENTREGA_016_PROGRESSO.md'; old=p.read_text(encoding='utf-8-sig')
if tag not in old: save(p,old+f'\n- {now} — A5.e PAGO condicional, 9 entradas Lean e índice vazio rejeitado; sonda original completa ainda MEDIDA de A1. A5 consolidado, elo T0 físico nomeado. Máquina {wall/3600:.6f}h parede/{cpu/3600:.6f}h CPU. Custos explícitos US${cost}, incompletos. Entrada do túnel relida, nenhuma ratificação usada. Não move gate; próximo A6. [{tag}]\n')
print(json.dumps(dict(entries=9,attempts=len(attempts),negative_rc=negative['rc'],wall_seconds=wall,report=str(OUT/'ENTREGA_016_A5e_import_construido.md'))))
