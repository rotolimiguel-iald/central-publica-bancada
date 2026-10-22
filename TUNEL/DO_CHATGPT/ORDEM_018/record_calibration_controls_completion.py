"""Verify existing control receipts and documentary manifests; no control rerun."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sqlite3
from audit_inputs import file_info, save_json
from reconcile_documentary_milestone_20261006 import verify_manifest

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')

def main():
    out = ROOT / 'RECIBO_ROOT_CONTROLES_COTA_CONCLUIDOS.json'
    assert not out.exists(), 'Receipt already created; inspect it, do not rerun.'
    p = ROOT / 'f9_calibration_bound/controls_preparation'
    read = lambda x: json.loads(x.read_bytes())
    contract, auth = read(p/'PROTOCOLO_EXATO.json'), read(p/'AUTORIZACAO_ROOT.json')
    claim, process, result = read(p/'CLAIM.json'), read(p/'RUN/PROCESS.json'), read(p/'RUN/RESULT.json')
    worker = result['detail']['worker']
    rid = contract['request_id']
    assert all(v['request_id'] == rid for v in (auth, claim, process, result, worker))
    pin = file_info(p/'PROTOCOLO_EXATO.json')
    assert all(v['contract_sha256'] == pin['sha256'] for v in (auth, claim, process))
    assert auth['authorized'] is True and auth['scope'] == 'C01_C08_SYNTHETIC_ONLY_ONCE'
    assert result['status'] == worker['status'] == 'PASS' and result['returncode'] == 0
    assert 0 < result['wall_including_cleanup_s'] <= auth['max_wall_seconds'] == 30
    assert json.loads(result['stdout']) == worker and result['stderr'] == ''
    assert result['pid_supervisor'] == process['pid_supervisor'] == claim['pid_supervisor']
    assert result['pid_worker'] == process['pid_worker']
    assert worker['monte_carlo'] == 0 and worker['observed_data'] is False
    assert result['scientific_observed_data'] is False and result['retry_allowed'] is False
    assert [v['id'] for v in worker['results']] == [v['id'] for v in contract['cases']]
    assert len(worker['results']) == 8 and all(v['result']['status'] == 'PASS' for v in worker['results'])
    pins = []
    for expected in contract['execution_pins']:
        actual = file_info(expected['path'])
        assert all(actual[k] == expected[k] for k in ('bytes','sha256'))
        pins.append(actual)
    cases = []
    for row in worker['results']:
        v = dict(row['result'])
        if 'tails' in v:
            v['tails'] = [{'df': t['df'], 't': t['t'], 'exact_intervals_in_pinned_receipt': True} for t in v['tails']]
        cases.append({'id':row['id'], 'result':v})
    draft = verify_manifest(ROOT/'f9_consolidated_draft/MANIFESTO_ENTREGA.json')
    guard = verify_manifest(ROOT/'preregistros/conjunto_d/audit_guard_repair_preparation/MANIFESTO_PREPARACAO.json')
    receipt = {
        'checked_at':datetime.now(timezone.utc).isoformat(),
        'status':'EIGHT_FIXED_SYNTHETIC_CONTROLS_PASSED_ONCE',
        'request_id':rid,
        'evidence':[file_info(p/n) for n in ('PROTOCOLO_EXATO.json','AUTORIZACAO_ROOT.json','REVISAO_ROOT_PRE_EXECUCAO.json','CLAIM.json','RUN/PROCESS.json','RUN/RESULT.json')],
        'execution_pins_rechecked':pins,
        'worker_pid':result['pid_worker'], 'supervisor_pid':result['pid_supervisor'],
        'worker_wall_s':worker['wall_s'], 'supervisor_wall_s':result['wall_including_cleanup_s'],
        'worker_returncode':result['returncode'], 'cases':cases,
        'scope':'Eight deterministic cases only. C05 uses supplied synthetic minima enclosures; C06 is an analytic covariance counterexample; C08 certifies five fixed tails. This is not a production global optimizer, arbitrary-tail implementation, full F9 calibration or physical evidence.',
        'claim_consumed':True, 'retry_authorized':False,
        'observed_data_opened':False, 'D_opened':False, 'new_PE':False, 'provider_calls':0,
        'documentary_delivery_integrity':{'F9_draft':draft,'audit_guard_preparation':guard},
        'reviews':'ROOT read consolidated draft, supervisor/controls and pure guard modules. Independent reviews of draft and guard are in progress; integrity is not scientific acceptance.'
    }
    save_json(out, receipt)
    with sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro', uri=True) as db:
        db.row_factory=sqlite3.Row
        jobs=[dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks=[dict(x) for x in db.execute("SELECT id,status,execution_constraints FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    snapshot_path=ROOT/'SLOT_SNAPSHOT.json'
    old=snapshot_path.read_bytes(); snapshot=json.loads(old)
    snapshot.update({'checked_at':receipt['checked_at'],'nonterminal':jobs,'executions':tasks,'next_state':'needs_attention','next_error':'Geração canônica diferente da autorizada no pedido.'})
    assert snapshot_path.read_bytes()==old
    save_json(snapshot_path,snapshot)
    slots_path=BASE/'state/handoffs/slot_management.json'
    old=slots_path.read_bytes();slots=json.loads(old)
    slots['last_checked_at']=receipt['checked_at']
    slots['queue_read_error'].update({'at':receipt['checked_at'],'operation':'next','receipt':'needs_attention_without_job_id_due_get_validation','dispatch':'none'})
    slots['ordem018_discriminante_slot_request']['latest_check']={'at':receipt['checked_at'],'queue_state':'needs_attention','queue_error':snapshot['next_error'],'nonterminal':len(jobs),'active_executions':len(tasks),'no_repeat_request':True,'new_provider_calls':0,'snapshot':file_info(snapshot_path)}
    slots['ordem018_calibration_controls_result']={'request_id':rid,'status':receipt['status'],'receipt':file_info(out),'opening_authorized':False,'provider_calls':0}
    assert slots_path.read_bytes()==old
    save_json(slots_path,slots)
    print(json.dumps({'receipt':file_info(out),'cases':len(cases),'status':receipt['status'],'wall_s':result['wall_including_cleanup_s'],'documentary_entries':{'F9':draft['entries'],'guard':guard['entries']},'queue_nonterminal':len(jobs),'active_executions':len(tasks)}))

if __name__=='__main__':
    main()
