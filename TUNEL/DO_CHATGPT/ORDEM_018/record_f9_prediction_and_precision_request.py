"""Persist actual local execution and a bounded preparation request, not science."""
import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from audit_inputs import file_info, safe_write, save_json

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_F9_C435_PREDICTION_572_PRIOR_569_20261006 -->'

def update(path, edit):
    raw = path.read_bytes()
    value = json.loads(raw)
    edit(value)
    assert path.read_bytes() == raw
    save_json(path, value)

def main():
    receipt = ROOT/'RECIBO_MEMORIA_PREDICAO_F9_C435.json'
    request_file = ROOT/'F9_PRECISION_SERVICES_PREPARATION_REQUEST.json'
    assert not receipt.exists() and not request_file.exists()
    now = datetime.now(timezone.utc).isoformat()
    metadata = json.load(sys.stdin)
    metadata.update(checked_at=now, source='Official iald_orchestration_status metadata only')
    meta = ROOT/'ORCHESTRATOR_METADATA_AFTER_C435.json'
    save_json(meta, metadata)
    actual_path = ROOT/'RECIBO_ROOT_PREDICAO_F9_REPARO_IMPORTS.json'
    actual = json.loads(actual_path.read_bytes())
    assert actual['status'] == 'ENGINEERING_PREDICTIONS_VERIFIED_ONCE'
    assert actual['metrics']['solver_calls_attempted'] == actual['metrics']['solver_calls_returned'] == 1
    pin = file_info(actual_path)
    prior_path = ROOT/'f9_physical_prior_preparation/MANIFESTO_PREPARACAO.json'
    prior = json.loads(prior_path.read_bytes())
    members = []
    for entry in prior['artifacts']:
        measured = file_info(entry['path'])
        assert all(measured[k] == entry[k] for k in ('bytes','sha256'))
        members.append(measured)
    intake = ROOT/'RECIBO_ROOT_ENTREGA_PRIORS_F9.json'
    assert not intake.exists()
    save_json(intake, {'at':now,'manifest':file_info(prior_path),'members':members,
        'status':'PREPARATION_RECEIVED_INDEPENDENT_REVIEW_PENDING', 'map_delivery':569,
        'root_read':'API contract and manifest; byte verification only, no imports or numerical evaluation.',
        'review_agent':'/root/ordem018_derivacoes','science_calls':0,'observed_reads':0})
    rid = str(uuid.uuid4())
    request = {'request_id':rid,'at':now,'mission':'ORDEM018 F1(c)',
        'manager_thread_id':'01a070fc-9484-7e13-a654-c6b5f61093a4',
        'status':'PREPARED_NOT_SENT', 'output_folder':'f9_precision_services_preparation',
        'purpose':'Prepare the two missing local numerical services consumed by df482: stable log exponential-quadratic finite window and bounded positive one-dimensional quadrature. Pure integration dependency only.',
        'sources':[file_info(ROOT/p) for p in ('f9_physical_prior_preparation/API_CONTRATO.md','f9_physical_prior_preparation/DERIVACAO.md','f9_physical_prior_preparation/physical_prior.py','f9_physical_prior_preparation/CONTRATO_API.json','f9_numerical_certification_preparation/CONTRATO_NUMERICO_F9.md')],
        'alternatives':['Analytic stable log-CDF/erfc finite-window evaluation plus existing qualified quadrature, with exact finite tail and small-window handling.', 'Bounded adaptive positive quadrature after scaling and geometric localization of the quadratic peak, shared by both services; disclose missed-peak and estimated-error limits.'],
        'deliverables':['Choose and explain a finite algorithm and installed or standard-library dependencies, preserving the exact injected APIs.', 'Pure module with countable evaluations, strict finite/type checks, failure propagation, no hidden retry and honest nonconvergence/error estimates.', 'Derivation of scaling/tail/window handling and machine-rounding limits; distinguish estimated local error from certification and theory/backend error.', 'Manifest, exact source/runtime metadata pins available read-only, static review evidence. Do not authorize or launch any numerical unit.'],
        'restrictions':['Preparation only: no candidate/backend/NumPy/SciPy imports, numerical controls, solver, WSL child, provider/network, observed values or covariance.', 'No AUTH/CLAIM or new numerical campaign; no repeats of consumed units; do not edit frozen packages.', 'No new priors/maps or V1 ratification. Preserve ENGINEERING_ONLY and MM conditional.', 'Write only the specified new Central output folder. Consult map first and register delivery; do not alter ROOT memories or ledger.'],
        'dependency_note':'df482 source interface is sealed and independently under review; any review defect must be reconciled explicitly before consumption.'}
    save_json(request_file,request)
    with sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row
        jobs=[dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks=[dict(x) for x in db.execute("SELECT id,status FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
        blocks=[dict(x) for x in db.execute('SELECT * FROM provider_blocks')]
    ledger_path=BASE/'state/handoffs/slot_management.json'
    def ledger(d):
        for e in d['effective_limits_verified']['sources']:
            m=file_info(e['path'])
            assert m['sha256']==e['sha256'] and m['bytes']==e['bytes']
        d['effective_limits_verified']['at']=now
        d.update(last_checked_at=now,free_admission_slots=5-len(jobs),free_execution_slots=3-len(tasks),manager_runtime_status='Official manager acknowledged c435 result; no duplicated request')
        d['queue_read_error'].update(at=now,receipt='needs_attention',dispatch='none')
        d['provider_eligibility_observation'].update(at=now,receipt=file_info(meta),canonical_memory=metadata['canonical_memory'],sources_ok=metadata['sources']['ok'])
        d['ordem018_F9_import_closure_repair_preparation'].update(dispatch_state='CONSUMED_ENGINEERING_PREDICTIONS_VERIFIED_ONCE_NO_RETRY',result=pin,result_map_sequence=572,external_exit_code=0,solver_calls_attempted=1,solver_calls_returned=1,manager_acknowledged=True)
        d['ordem018_F9_physical_prior_preparation'].update(status='DELIVERED_INDEPENDENT_REVIEW_PENDING',manifest=file_info(prior_path),root_intake=file_info(intake),delivery_map_sequence=569,review_agent='/root/ordem018_derivacoes')
        d['ordem018_F9_precision_services_preparation']={**request,'request_pin':file_info(request_file)}
        d['ordem018_discriminante_slot_request']['latest_check']={'at':now,'queue_state':'needs_attention','nonterminal':len(jobs),'active_executions':len(tasks),'provider_calls':0,'work_calls':0,'useful_local_work':'c435 completed; prior review active; concrete precision dependency prepared, not yet sent.'}
    update(ledger_path,ledger)
    update(ROOT/'SLOT_SNAPSHOT.json',lambda d:d.update(checked_at=now,nonterminal=jobs,executions=tasks,provider_blocks=blocks,next_state='needs_attention',metadata_status=file_info(meta),dispatch='No remote/Work calls; local c435 consumed successfully; concrete precision preparation request recorded.'))
    note=f'''{MARK}
## 06/10/2026 UTC — Previsão teórica F9 c435 concluída; integração dos priors em construção

[REAL — mapas567/568/570/572] Pacote corrigido e5d recebido da gerente, delta revisado independentemente e decisão específica ROOT registrada antes da chamada. c4359a48-bf7c-4dd5-a753-8c3413774cdf executou exatamente uma vez: saída externa0, {actual['metrics']['outer_wall_seconds']}s, motor1tentativa/1retorno, montagem de cinco modelos com283linhas/63colunas nuisance. Verificador ROOT conferiu27membros, identidades, hashes/proveniência, streams completos, filho recolhido, limpeza sem processos controlados vivos e relações aritméticas entre os modelos. Recibo {pin['path']} SHA256 {pin['sha256']}. Guard cooperativo sem recusas nesta unidade; isso não equivale a sandbox de sistema nem cobertura de todas as chamadas nativas.

[REAL computacional — ENGINEERING_ONLY] Um ponto congelado derivado do prior, sem ajuste: theta={actual['predictions']['theta']}; K_TGL={actual['predictions']['K_TGL']}. Este número pertence somente a esse ponto. Não houve observados, likelihood, evidência Bayesiana, significância ou veredito físico; não é teste de convergência/cota uniforme. A tentativa ffd6 continua FAILED_TERMINAL_CLEANED com solver0; c435 está consumida e não se repete. Gerente recebeu e conferiu o recibo. A sequência correta do resultado é572 (571 foi antecipada equivocadamente na mensagem de entrega, sem efeito sobre o arquivo/mapa).

[REAL documental — mapa569] Recebida preparação df482 dos priors físicos;13membros conferidos por ROOT. H3/H4 com normalização e Jacobiano; H5 q=1/rd com q^-2. Revisão independente de derivações em andamento. Não houve importação ou execução desta preparação. As integrais são condicionais em theta; não são logZ. Duas dependências numéricas explícitas ainda precisam implementação/qualificação: janela exponencial-quadrática estável e quadratura positiva1D. Pedido local concreto {rid}, arquivo {request_file}, preparado para a gerente, sem AUTH/CLAIM, campanha, ciência ou observados.

[REAL operacional] Fila remota continua needs_attention por geração divergente: {len(jobs)}coordenação não terminal/{len(tasks)}execuções ativas; limites5/3/1por provedor paralelo. Fonte operacional e memória comum indisponíveis para despacho; ready não significa elegível. Nenhum repin, substituição, provedor ou Work. F1c, V1 e F3 continuam abertos; F4 não pronta. Dados para veredito só pelo operador após V1 por hash; kernel/gate/originais intactos.'''
    changes=[]
    paths=[MEM/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]+[ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']
    for path in paths:
        old=path.read_bytes()
        assert MARK.encode() not in old
        new=old+('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode()
        assert path.read_bytes()==old
        safe_write(path,new)
        assert path.stat().st_size>len(old)
        changes.append({'before_bytes':len(old),'after':file_info(path)})
    def continuity(d):
        d.update(updated_at=now,F9_import_repair_status='CONSUMED_ENGINEERING_PREDICTIONS_VERIFIED_ONCE_NO_RETRY',F9_import_repair_result=pin,F9_physical_prior_status='DELIVERED_INDEPENDENT_REVIEW_PENDING',F9_physical_prior_delivery=file_info(intake),F9_precision_preparation_request=file_info(request_file))
        d['milestone_sequences']=sorted(set(d.get('milestone_sequences',[])+[567,568,569,570,572]))
        d['phases']['F1']='THEORY_POINT_AND_FIVE_MODELS_COMPUTED_ONCE; CONSUMER_STATIC_ACCEPTED; PHYSICAL_PRIOR_REVIEW_PENDING; NUMERICAL_SERVICES_PREPARATION_REQUESTED; OBSERVED_COMPOSITE_CLOSED'
        d['next_steps']=['Review physical-prior derivative package; prepare its two concrete precision dependencies without observed inputs.', 'Qualify concrete coupled integration with preserved covariance and theory receipt; V1 remains conditional and unratified.', 'Continue F1/F3; consumed units never repeated; F4 not ready.']
    update(ROOT/'CONTINUIDADE.json',continuity)
    save_json(receipt,{'at':now,'marker':MARK,'result':pin,'prior_intake':file_info(intake),'precision_request':file_info(request_file),'changes':changes,'continuity':file_info(ROOT/'CONTINUIDADE.json'),'ledger':file_info(ledger_path),'backup_policy':'Exact bytes, same-folder backup, verified temporary and compare-before-write.'})
    def manifest(d):
        files={Path(e['path']) for e in d['files']}
        files.update([Path(__file__).resolve(),receipt,request_file,intake,meta,actual_path,ROOT/'F9_IMPORT_REPAIR_EXECUTION_TOOL_RECEIPT.json',ROOT/'verify_f9_import_repair_result.py',ROOT/'RECIBO_ROOT_ENTREGA_REPARO_IMPORTS_F9.json'])
        for folder in ('f9_engine_import_closure_repair_preparation','proveniencia/revisao_f9_import_closure_repair','f9_physical_prior_preparation'):
            files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
        files.update(Path(e['path']) for e in prior['artifacts'])
        assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in files)
        d.update(updated_at=now,previous_snapshot=file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),status='PARTIAL_F9_THEORY_COMPUTED_PRIOR_REVIEW_AND_PRECISION_PREPARATION',files=[file_info(p) for p in sorted(files,key=lambda p:str(p).casefold())])
    update(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json',manifest)
    print(json.dumps({'result':pin,'request_id':rid,'request':file_info(request_file),'memory_receipt':file_info(receipt),'partial_manifest':file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),'nonterminal':len(jobs),'executions':len(tasks)},ensure_ascii=False))

if __name__=='__main__':
    main()
