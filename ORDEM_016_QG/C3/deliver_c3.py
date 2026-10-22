"""Seal isolated coexistence of the twelve A6 sources, with no theorem-body edits."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,sys,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C3';P=D/'package'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,write,put,append
plan=json.loads((D/'PLAN.json').read_bytes());now=datetime.now(timezone.utc)
auditor=OUT.parent/'PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/MEDIDAS_DO_REDATOR/auditar_axiomas.py'
args=[];receipts=[]
for i,item in enumerate(plan['groups']+[dict(copy=str(P/'IntegrationAudit.lean'))]):
    source=Path(item['copy']);p=P/('module_'+str(i+1).zfill(2)+'_01.json')
    r=json.loads(p.read_bytes());assert r['rc']==0 and not r['scan_errors'] and not r['newer_kernel_files']
    assert sha(source)==r['source_sha256'] and sha(p.with_suffix('.log'))==r['log_sha256']
    if 'source' in item:
        assert sha(Path(item['source']))==item['source_sha256'] and sha(source)==item['copy_sha256']
        def body(b):return b''.join(x for x in b.splitlines(keepends=True) if not x.startswith(b'import '))
        assert body(source.read_bytes())==body(Path(item['source']).read_bytes())
    args.extend([str(source),str(p.with_suffix('.log'))]);receipts.append(dict(path=str(p),sha256=sha(p),**r))
a=subprocess.run([sys.executable,'-X','utf8','-B',str(auditor),*args],capture_output=True)
assert a.returncode==0,a.stdout.decode('utf-8')
write(D/'AXIOM_AUDIT.json',a.stdout);audit=json.loads(a.stdout)
expected=set(plan['expected_names']);got=set(audit[-1]['axiomas']);assert got==expected
decls=sum(x['n_theorem_lemma_na_fonte'] for x in audit[:-1])
assert all(x['auditoria']=='PASSA' for x in audit)
cpu=sum(x['cpu_user_seconds']+x['cpu_kernel_seconds'] for x in receipts);wall=sum(x['wall_seconds'] for x in receipts)
elapsed=(now-datetime.fromisoformat(plan['at'])).total_seconds()/3600
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
review=ROOT/'ADENDO_002_CRITICAS/C25_RECEIVED/KIMI_ORIGINAL.md'
crit=dict(at=now.isoformat(),source=str(review),sha256=sha(review),status='PARTIAL_ACCEPTANCE_WITH_MEASURED_EXECUTION',
    accepted=['One sole v3 base; twelve sources and dependency DAG','Only import header edits; keep theorem bodies','Measure coexistence and peak memory; preserve strong infinite limit hypothesis'],
    measured=['Two local import lines changed; all remaining code bytes identical','Twelve modules and aggregate compile serially within8GiB','130 expected printed declarations coexist in aggregate'],
    rejected_operational=['No lake build; only isolated lake env lean','No canonical TGL/Audit edits','No six concurrent Lean jobs; ran one at a time','No omission of negative-control theorems from coexistence consumer'],
    unnecessary=['No Mathlib import reduction needed for this measured package','No heartbeat reduction needed','No module/declaration renaming needed'],
    limits=['Response saw partial projections','Its cause-of-memory narrative was not a measurement','No installed canonical public module, no um.py edits, no new mathematical theorem'])
put(D/'C25_SOURCE_AUDIT.json',crit)
ledger=OUT/'LEDGER_016.jsonl';units={}
for x in [json.loads(z) for z in ledger.read_text('utf-8').splitlines() if z.strip()]:
    u=next((x[k] for k in ['usage','raw_usage','tokens'] if isinstance(x.get(k),dict) and 'completion_tokens' in x[k]),None)
    provider=x.get('provider') or x.get('provedor'); key=x.get('execution_task_id') or x.get('execution_id') or x.get('task_id') or x.get('job_id') or x.get('request_id')
    if not u or not key or not provider:continue
    cost=next((x[k] for k in ['cost_estimate_usd','cost_usd','custo_usd'] if x.get(k) is not None),None)
    if cost is None and key in units:cost=units[key]['cost']
    units[key]=dict(provider=provider,usage=u,cost=cost)
known=sum((Decimal(str(x['cost'])) for x in units.values() if x['cost'] is not None),Decimal(0))
put(D/'LEDGER_TOTALS.json',dict(at=now.isoformat(),ledger_sha256=sha(ledger),units=units,partial_metered_cost_usd=str(known),unknown_is_not_zero=True))
result=dict(at=now.isoformat(),status='PAGO_ISOLATED_TWELVE_SOURCE_INTEGRATION',sources=12,theorems=decls,
    audited_unique_declarations=len(got),all_13_compilations_rc0=True,axioms_in_trio=True,body_bytes_unchanged=True,
    import_lines_changed=2,original_core_bytes_unchanged=True,source_count_changed=False,
    strong_infinite_limit='OPEN: FlowTendsToFamily; no uniform limit smuggled in',
    kernel_installed=False,gate_changed=False,receipts=receipts,compile_wall_seconds=wall,compile_cpu_seconds=cpu,
    peak_process_committed_bytes=max(x['peak_process_committed_bytes'] for x in receipts),bench_elapsed_hours=elapsed,ceiling_hours=6,
    partial_metered_cost_usd=str(known))
put(D/'RESULTS.json',result)
note=f'''[REAL — C3: as doze fontes coexistem em compilação isolada]

AberturaSHA256={opening}.

**Integração paga no escopo da bancada.** Doze módulos recompilados e um
consumidor que importa os doze:13 processos rc0; {decls} teoremas/lemas nos
corpos e {len(got)} declarações únicas impressas, todas no trio. A contagem
de declarações também inclui uma definição e dois teoremas importados.
AXIOM_AUDIT.json confere cobertura integral dos corpos, zero sorry e nenhum
axioma novo. IntegrationAudit.lean é o consumidor de coexistência, com
os controles negativos incluídos; não se limitou a módulos separados.

A mudança necessária foi **duas linhas de import**: InscriptionBridge e
PenaltyThreeLocksBridge_v2 passaram de TheEquationOfTruth_T20 para a mesma
TheEquationOfTruth_T20_v3 já usada pela taxa espectral. Fora dessas linhas,
os bytes foram preservados; o núcleo v3 inteiro permanece idêntico.
Não acrescentamos função, hipótese, prova ou nome para fazê-los encaixar.
O manifesto registra origem, cópia e hash do corpo sem imports.

Convivem a exclusão conjunta ker(ΣD†D), preservação da leitura, inscrição
transportada, comparação discriminante, recíproca em dimensão finita,
exponencial de dephasing idempotente, taxa com gap, entropia escalar do qubit,
controle do gerador modular e controles de falso reconhecimento.
**A recíproca infinita ainda conserva FlowTendsToFamily como hipótese**;
não foi paga por esta ligação. Entropia escalar não vira automaticamente
teorema de entropia matricial. Nenhum fluxo dissipativo foi identificado
com o fluxo modular unitário.

Crítica Kimi C2.5: adotado o núcleo único e o DAG das12fontes. Conferidos
e corrigidos os detalhes pelo compilador. Não foi necessário reduzir
imports Mathlib, heartbeats nem renomear declarações. Rejeitadas as
sugestões de lake build, escrita canônica e seis processos simultâneos,
incompatíveis com a missão. A compilação foi estritamente serial.

Recursos: parede {wall:.3f}s, CPU {cpu:.3f}s, pico de memória comprometida
por processo {result['peak_process_committed_bytes']}bytes (<8GiB);
bancada {elapsed:.4f}h/teto6h. Custos remotos conhecidos parciais acumulados
USD{known}; Kimi sem preço informado não foi contabilizado como gratuito.
Nenhuma nova chamada remota nesta integração. Comandos/logs/hashes no manifesto.

**Não instalado em um.py/kernel; gate intacto.** É o pacote verificável
para a gerência incorporar, sem a falha anterior de imports conflitantes.
Próximo C4: cociclo físico no ramo cone de luz, preservando a partição
como decisão do operador.
'''
write(D/'RELATORIO.md',note.encode());write(OUT/'ENTREGA_016_C3_integracao_das_doze_fontes.md',note.encode())
write(OUT/'ENTREGA_016_C_CRITICA_integracao_doze_fontes.md',note.encode())
refs=[p for p in D.rglob('*') if p.is_file() and p.suffix!='.marker']+[review,auditor]
put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],gate_changed=False))
append(ledger,json.dumps(dict(at=now.isoformat(),event='C3_TWELVE_SOURCE_INTEGRATION',target='PartC.C3',remote_call=False,
    compile_wall_seconds=wall,compile_cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json')))+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} C3PAGO:12fontes+consumidor,13rc0,{decls}teoremas/{len(got)}decls auditadas;2imports,0corpos alterados. Bancada{elapsed:.4f}h/6h;CPU{cpu:.3f}s;parede{wall:.3f}s;custos remotos conhecidos USD{known},outrosdesconhecidos. ManifestoSHA256={sha(D/"manifest.json")}. Gateintacto;C4. AberturaSHA256={opening}.\n')
p=ROOT/'A7/CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',next=['C4 actual light-cone helicity cocycle and C23 source audit','C5KMS/C24 critique;C6Q2;PartB;finalaudit'],C3_manifest=str(D/'manifest.json'),own_live_processes=[])
c['remaining_full_goal']=['C4-C6','C2.3/4 full source audits','ORDEM015 PartB','final audit and reports'];put(p,c,True)
print(json.dumps({k:result[k] for k in ['status','theorems','audited_unique_declarations','compile_cpu_seconds','compile_wall_seconds','peak_process_committed_bytes']}))
