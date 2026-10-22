"""Record static review, diagnosis, and queue metadata without running science."""
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from audit_inputs import file_info, safe_write, save_json

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MEM = Path(r'C:\IALD\Central de Patentes\memory')
MARK = '<!-- ORDEM018_F9_REVIEW_563_DIAGNOSIS_561_REPAIR_562_20261006 -->'


def verify_manifest(path):
    data = json.loads(path.read_bytes())
    checks = []
    for member in data['artifacts']:
        measured = file_info(member['path'])
        assert all(measured[k] == member[k] for k in ('bytes', 'sha256')), member['path']
        checks.append(measured)
    return checks


def update(path, edit):
    old = path.read_bytes()
    value = json.loads(old)
    edit(value)
    assert path.read_bytes() == old
    save_json(path, value)


def main():
    out = ROOT/'RECIBO_MEMORIA_CONSUMIDOR_REVISADO_DIAGNOSTICO.json'
    assert not out.exists(), 'Consumed recording unit; inspect existing receipt.'
    stamp = datetime.now(timezone.utc).isoformat()
    metadata = json.load(sys.stdin)
    metadata['checked_at'] = stamp
    metadata['source'] = 'Official iald_orchestration_status tool, metadata only'
    meta_path = ROOT/'ORCHESTRATOR_METADATA_CONSUMER_REVIEW_ROUND.json'
    save_json(meta_path, metadata)
    review = ROOT/'derivacoes/revisao_f9_likelihood_consumer/MANIFESTO_REVISAO_CONSUMIDOR_F9.json'
    source = ROOT/'f9_likelihood_consumer_preparation/MANIFESTO_PREPARACAO.json'
    reviewed = verify_manifest(review)
    source_members = verify_manifest(source)
    review_data = json.loads(review.read_bytes())
    assert file_info(source)['sha256'] == review_data['source_manifest_final_sha256']
    assert review_data['status'] == 'STATIC_NO_MATERIAL_BLOCKER_WITHIN_DECLARED_SCOPE'
    receipt_path = ROOT/'RECIBO_ROOT_REVISAO_CONSUMIDOR_F9.json'
    assert not receipt_path.exists()
    save_json(receipt_path, {
        'at': stamp, 'request_id': review_data['request_id'],
        'status': 'STATIC_REVIEW_ACCEPTED_FOR_CONCRETE_ENGINEERING_INTEGRATION_NOT_EXECUTION',
        'review_manifest': file_info(review), 'review_members': reviewed,
        'source_manifest': file_info(source), 'source_members': source_members,
        'map_review_sequence': 563,
        'root_read': 'Full independent opinion; source/API read at intake; measured manifests and members now.',
        'accepted_scope': '283 ordered rows, 63 nuisance coordinates; Ty/TCTt/affine origin; existing Gaussian backend; offsets once; common support and relative kappa d-eta; five-model collection aborts on engineering error.',
        'limitations': ['No candidate/backend imports or numeric execution in this receipt',
                        'Caller must authenticate injected modules, inputs and authorization',
                        'Pointwise nuisance integral is not physical-prior evidence',
                        'MM conditional, V1 not ratified, no observed data released',
                        'No uniform numerical certificate, no physical verdict'],
        'scientific_calls': 0, 'provider_calls': 0, 'work_assistance_used': False,
        'execution_authorized': False, 'consumed_ffd6_retry': False,
    })
    pin = file_info(receipt_path)
    diagnosis = file_info(ROOT/'RECIBO_ROOT_DIAGNOSTICO_FFD6.json')
    repair = file_info(ROOT/'F9_IMPORT_CLOSURE_REPAIR_PREPARATION_REQUEST.json')
    with sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
        blocks = [dict(x) for x in db.execute('SELECT * FROM provider_blocks')]
    limits = {'at':stamp, 'coordination':5, 'executions':3, 'per_parallel_provider':1,
              'parallel_providers':['kimi','mimo','deepseek'], 'other_providers_exclusive':True,
              'sources':[file_info(BASE/'iald_orchestrator'/n) for n in ('coordination.py','runtime.py','transport.py')]}
    update(ROOT/'SLOT_SNAPSHOT.json', lambda d:d.update(
        checked_at=stamp, nonterminal=jobs, executions=tasks, provider_blocks=blocks,
        next_state='needs_attention', next_error='Geração canônica diferente da autorizada no pedido.',
        source_files=limits['sources'], metadata_status=file_info(meta_path),
        dispatch='No provider/Work dispatch or duplicate request; concrete e5d214 preparation active in manager.'))
    def ledger_edit(d):
        d.update(last_checked_at=stamp, effective_limits_verified=limits,
                 free_admission_slots=5-len(jobs), free_execution_slots=3-len(tasks),
                 manager_cursor='ca905f1b-d9cd-4a47-9f7e-cb2b71f4b405:118',
                 manager_runtime_status='Official snapshot revision118: e5d214 preparation inProgress')
        d['queue_read_error'].update(at=stamp, receipt='needs_attention', dispatch='none')
        d['provider_eligibility_observation'].update(at=stamp,receipt=file_info(meta_path),canonical_memory=metadata['canonical_memory'],sources_ok=metadata['sources']['ok'])
        d['ordem018_F9_likelihood_consumer_preparation'].update(status='STATIC_INDEPENDENT_REVIEW_ACCEPTED_NO_EXECUTION', review_sequence=563, root_review=pin)
        d['ordem018_F9_engine_terminal_diagnosis'].update(status='ROOT_ACCEPTED_STATIC_DIAGNOSIS_ERRATA_555',map_sequence=561,delivery=diagnosis)
        d['ordem018_F9_import_closure_repair_preparation'].update(dispatch_state='OFFICIAL_MANAGER_IN_PROGRESS_REVISION_118',request_pin=repair)
        d['ordem018_discriminante_slot_request']['latest_check']={'at':stamp,'queue_state':'needs_attention','nonterminal':len(jobs),'active_executions':len(tasks),'new_provider_calls':0,'no_repeat_request':True,'useful_work':'e5d214 repair preparation already active; consumer review563 accepted locally; sources unavailable for remote dispatch.'}
    update(BASE/'state/handoffs/slot_management.json', ledger_edit)
    note = f'''{MARK}
## 06/10/2026 UTC — Consumidor F9 revisado e correção de imports em preparação

[REAL documental — revisão563] Revisão independente do consumidor a987 sem bloqueador material no escopo de chamador confiável. ROOT leu o parecer e conferiu os3membros da revisão e14da preparação. Ty/TCTᵀ/origem,283linhas/63nuisances, offsets uma vez, backend gaussiano existente e medida comum κ dη preservados. É integral pontual dos nuisances, não evidência integrada dos priors físicos. Falhas de engenharia abortam a coleção; −inf só representa densidade zero legitimamente fora do suporte comum. Aceite estático para integração concreta, sem execução, AUTH/CLAIM ou observados. Recibo {pin['path']} SHA256 {pin['sha256']}. MM continua condicional; tolerâncias float64 e erro teórico não limitado impedem alegação de certificado, sem impedir engenharia honesta.

[REAL documental — diagnóstico561/errata555] A cadeia estática SciPy→array_api_compat→importação estrela NumPy→f2py→crackfortran alcança charset_normalizer, omitido do inventário. Os eventos físicos demonstram as recusas de pyc/fonte e do ZIP ausente; a origem dinâmica exata da sondagem ZIP não foi preservada pelo traceback truncado e continua OPEN. Integridade de pins não demonstrava fechamento de imports. Recibo {diagnosis['path']} SHA256 {diagnosis['sha256']}. ffd6 permanece consumida/terminal, solver0, nenhuma previsão aceita.

[REAL operacional — pedido562] A gerente recebeu e5d214e4-972e-41f5-bd14-0dc071c00e6b e está preparando pacote separado: fechamento finito das dependências instaladas charset_normalizer, sondagem de ausência do caminho ZIP exato e traceback com quadros finais. Motor científico, montagem e configurações permanecem preservados. Pedido {repair['path']} SHA256 {repair['sha256']}. Não autoriza imports/solver/controle/likelihood/observados nem repetiçãoffd6; futura decisão exige delta concreto revisado.

[REAL fila] next voltou a falhar por geração canônica distinta, registrado needs_attention, não idle. Snapshot: {len(jobs)}coordenação não terminal, {len(tasks)}execução queued/running; limites5/3/1por provedor paralelo. Memória comum indisponível e fonte operacional divergente; ready não demonstra elegibilidade. Sem repin, substituição, chamada remota/Work ou cobrança duplicada. F1/F3 abertas e F4 não pronta; abertura observada permanece com o operador após V1 por hash. Kernel, gate e originais intactos.'''
    changes=[]
    for path in [MEM/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]+[ROOT/'ENTREGA_018_F1_HUBBLE.md',ROOT/'ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md']:
        old=path.read_bytes()
        assert MARK.encode() not in old
        new=old+('\r\n\r\n'+note.replace('\n','\r\n')+'\r\n').encode('utf-8')
        assert path.read_bytes()==old
        safe_write(path,new)
        assert path.stat().st_size>len(old)
        changes.append({'before_bytes':len(old),'after':file_info(path)})
    def continuity_edit(d):
        d.update(updated_at=stamp,F9_likelihood_consumer_status='STATIC_REVIEW_ACCEPTED_NO_EXECUTION',F9_likelihood_consumer_review=pin,F9_engine_import_diagnosis=diagnosis,F9_engine_repair_preparation=repair)
        d['milestone_sequences']=sorted(set(d.get('milestone_sequences',[])+[561,562,563]))
        d['phases']['F1']='CONSUMER_STATIC_REVIEW_ACCEPTED; FFD6_TERMINAL_IMPORT_FAILURE_ZERO_SOLVER; NEW_IMPORT_REPAIR_PREPARATION_ACTIVE; OBSERVED_COMPOSITE_CLOSED'
        d['next_steps']=['Receive e5d214 concrete import-closure repair from manager and review its delta; no retry of consumed ffd6.', 'Prepare remaining physical-prior evidence integration from the existing Gaussian and five-model code, preserving full covariance and observed-data restrictions.', 'Continue F1/F3 toward concrete V1; goal incomplete, F4 not ready.']
    update(ROOT/'CONTINUIDADE.json',continuity_edit)
    save_json(out,{'at':stamp,'marker':MARK,'review':pin,'diagnosis':diagnosis,'repair_request':repair,'changes':changes,'continuity':file_info(ROOT/'CONTINUIDADE.json'),'slots':file_info(ROOT/'SLOT_SNAPSHOT.json'),'ledger':file_info(BASE/'state/handoffs/slot_management.json'),'backup_policy':'Exact bytes, same folder, verified temporary and compare-before-write.'})
    def manifest_edit(d):
        paths={Path(e['path']) for e in d['files']}
        paths.update([out,receipt_path,Path(__file__).resolve(),meta_path,Path(diagnosis['path']),Path(repair['path']),ROOT/'F9_IMPORT_CLOSURE_REPAIR_DISPATCH_RECEIPT.json'])
        for folder in ('derivacoes/revisao_f9_likelihood_consumer','proveniencia/diagnostico_f9_ffd6_terminal'):
            paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name and '__pycache__' not in p.parts)
        assert all(p.resolve().is_relative_to(ROOT.resolve()) for p in paths)
        d.update(updated_at=stamp,previous_snapshot=file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),status='PARTIAL_CONSUMER_REVIEW_ACCEPTED_IMPORT_REPAIR_PREPARATION_ACTIVE',files=[file_info(p) for p in sorted(paths,key=lambda p:str(p).casefold())])
    update(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json',manifest_edit)
    print(json.dumps({'root_review':pin,'memory_receipt':file_info(out),'manifest':file_info(ROOT/'MANIFESTO_CONSOLIDACAO_PARCIAL.json'),'nonterminal':len(jobs),'executions':len(tasks)},ensure_ascii=False))


if __name__=='__main__':
    main()
