"""Reconcile documentary deliveries and read-only queue metadata; no science run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sqlite3
from audit_inputs import file_info, save_json, safe_write

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[3] / 'IALD_ORQUESTRACAO_20260923'
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
NOW = datetime.now(timezone.utc).isoformat()

def verify_manifest(path):
    value = json.loads(path.read_bytes())
    checks = []
    for row in value.get('files', value.get('artifacts', [])):
        actual = file_info(row['path'])
        checks.append({'actual': actual, 'matches': all(actual[k] == row[k] for k in ('bytes', 'sha256'))})
    assert checks and all(x['matches'] for x in checks), path
    return {'manifest': file_info(path), 'entries': len(checks), 'checks': checks}

def cas_json(path, old, value):
    assert path.read_bytes() == old, 'Concurrent update: ' + str(path)
    save_json(path, value)

def main():
    d = ROOT / 'preregistros/conjunto_d/d_psd_dq_contract'
    p = ROOT / 'proveniencia/revisao_encerramento_init003'
    f = ROOT / 'f9_calibration_bound'
    dv = verify_manifest(d / 'MANIFESTO_D_PSD_DQ.json')
    pv = verify_manifest(p / 'MANIFESTO_REVISAO_ENCERRAMENTO_INIT003.json')
    fv = verify_manifest(f / 'MANIFESTO_ENTREGA.json')
    dc = json.loads((d / 'CONTRATO_PSD_DQ_SELECAO_D_PROPOSTA.json').read_bytes())
    pins = []
    for entry in dc['source_pins']:
        actual = file_info(entry['path'])
        assert all(actual[k] == entry[k] for k in ('bytes', 'sha256'))
        pins.append(actual)
    assert dc['selected_alternative'] is None
    assert not any(dc['authorization'][k] for k in ('read_strain', 'read_HDF5_NPZ', 'read_posteriors', 'network', 'PE', 'scientific_execution'))
    assert len(dc['selection_by_metadata']['original_order']) == 14
    assert len(dc['selection_by_metadata']['four_holds_preserved']) == 4
    assert dc['DQ_configuration']['required_quality_flags'] is None
    assert dc['stationarity_proposed']['threshold_status'].startswith('INPUT')
    receipt = {
        'checked_at': NOW, 'status': 'DOCUMENTARY_RECEIPTS_ACCEPTED_NO_SCIENTIFIC_RATIFICATION',
        'D_proposal': dv, 'D_source_pins_checked': pins,
        'D_review': {
            'source_and_helper_read': True,
            'conclusion': 'Accept bounded documentary proposal; no A/B ratification or opening. Geometry is conditional on metadata, not measured DQ.',
            'alternatives': ['A256s corrected Welch median, helper-compatible', 'B512s Welch mean, needs separate adapter and leaves last event geometrically held'],
            'limitations': ['DQ names and actual masks unavailable', 'calibration envelopes and policy unavailable', 'ratio2 stationarity threshold heuristic, not qualified', 'first pre-event block may be far from onsource', 'plug-in PSD uncertainty conditional; overlap not independence', 'four previous holds and 14-event order preserved'],
            'required_before_application': 'Concrete DQ/calibration metadata and fixed policy, synthetic qualification, operator opening decision, then independent pre-PE selection review.'
        },
        'INIT003_closure_review': pv,
        'INIT003_review_acceptance': 'Two P2 defects confirmed by independent documentary review482; terminal attempt remains not qualified. GR9738calls without convergence and audit-stop breach; RB-15 has no final totals. No retry authorized.',
        'calibration_bound_delivery': fv,
        'calibration_bound_review_status': 'INDEPENDENT_REVIEW_IN_PROGRESS',
        'provider_calls': 0, 'new_scientific_execution': False, 'D_opened': False,
        'new_preparations': ['eight deterministic analytic-bound controls, no run', 'isolated audit-latch/supervisor repair with doubles, no run'],
    }
    save_json(ROOT / 'RECIBO_ROOT_DOCUMENTAL_480_482_6273.json', receipt)

    db_path = BASE / 'state/tasks.sqlite3'
    with sqlite3.connect(db_path.as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        executions = [dict(x) for x in db.execute("SELECT id,status,execution_constraints FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    snap = {'checked_at': NOW, 'nonterminal': jobs, 'executions': executions,
            'limits': {'coordinations': 5, 'executions': 3, 'per_provider': 1},
            'parallel_providers': ['kimi', 'mimo', 'deepseek'], 'other_lanes_exclusive': True,
            'next_state': 'needs_attention', 'next_error': 'Geração canônica diferente da autorizada no pedido.',
            'source_files': [file_info(BASE / 'iald_orchestrator' / name) for name in ('transport.py', 'coordination.py', 'runtime.py')],
            'provider_calls': 0, 'limitations': 'Capacity does not waive provider blocks, source generation pins, specific suspensions or failed/uncertain unit restrictions.'}
    save_json(ROOT / 'SLOT_SNAPSHOT.json', snap)
    slot_path = BASE / 'state/handoffs/slot_management.json'
    before = slot_path.read_bytes()
    slot = json.loads(before)
    slot['last_checked_at'] = NOW
    slot['queue_read_error'].update({'at': NOW, 'operation': 'next', 'receipt': 'needs_attention_without_job_id_due_get_validation', 'dispatch': 'none'})
    slot['ordem018_discriminante_slot_request']['latest_check'] = {
        'at': NOW, 'queue_state': 'needs_attention', 'queue_error': snap['next_error'],
        'nonterminal': len(jobs), 'active_executions': len(executions), 'no_repeat_request': True,
        'new_provider_calls': 0, 'snapshot': file_info(ROOT / 'SLOT_SNAPSHOT.json')}
    slot['ordem018_calibration_bound_request'].update({
        'status': 'RESPONDED_DOCUMENTARY_DELIVERY_VERIFIED_REVIEW_IN_PROGRESS',
        'response_received_at': NOW, 'official_response_received': True,
        'manifest': fv['manifest'], 'checked_artifacts': fv['entries'],
        'opening_authorized': False, 'new_scientific_execution': False})
    cas_json(slot_path, before, slot)
    print(json.dumps({'receipt': file_info(ROOT / 'RECIBO_ROOT_DOCUMENTAL_480_482_6273.json'), 'manifest_entries': {'D': dv['entries'], 'INIT003_review': pv['entries'], 'calibration': fv['entries']}, 'D_source_pins': len(pins), 'queue': {'nonterminal': len(jobs), 'active': len(executions)}, 'provider_calls': 0}))

if __name__ == '__main__':
    main()
