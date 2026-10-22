"""Inspect pinned documentary deliveries and persist the next bounded request."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sqlite3
import uuid
from audit_inputs import file_info, save_json

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[2] / 'IALD_ORQUESTRACAO_20260923'
MANAGER = '01a070fc-9484-7e13-a654-c6b5f61093a4'


def check_pin(pin, parent=None, allow_backup=False):
    p = Path(pin['path'])
    if not p.is_absolute():
        p = parent / p
    order = ROOT.parents[1] / 'PARA_CHATGPT/ORDEM_018_o_discriminante.md'
    assert p.resolve().is_relative_to(ROOT.resolve()) or p.resolve() == order.resolve(), str(p)
    actual = file_info(p)
    if all(actual[k] == pin[k] for k in ('bytes', 'sha256')):
        return {'expected': pin, 'resolved': actual, 'historical_backup': False}
    assert allow_backup, str(p)
    for backup in sorted(p.parent.glob(p.name + '.bak_*')):
        candidate = file_info(backup)
        if all(candidate[k] == pin[k] for k in ('bytes', 'sha256')):
            return {'expected': pin, 'resolved': candidate, 'historical_backup': True,
                    'current_accumulator': actual}
    raise AssertionError('No byte-exact source version found: ' + str(p))


def manifest(rel):
    p = ROOT / rel
    value = json.loads(p.read_bytes())
    rows = value.get('files', value.get('artifacts'))
    assert isinstance(rows, list) and rows
    verified = [check_pin(x, p.parent) for x in rows]
    return {'manifest': file_info(p), 'entries': len(verified), 'verified': verified}


def main():
    out = ROOT / 'RECIBO_ROOT_INVENTARIO_CALIBRACAO_ENVELOPE_V2_CONSOLIDACAO.json'
    assert not out.exists(), 'Inspect existing receipt; do not repeat this milestone.'
    now = datetime.now(timezone.utc).isoformat()
    checked = {name: manifest(rel) for name, rel in {
        'D_inventory': 'preregistros/conjunto_d/d_calibration_member_inventory/MANIFESTO_ENTREGA.json',
        'tail_V2': 'f9_tail_envelope_proposal_v2/MANIFESTO_PROPOSTA_V2.json',
        'tail_original_review': 'derivacoes/revisao_tail_envelope/MANIFESTO_REVISAO_SNAPSHOT498.json',
        'tail_V2_review': 'derivacoes/revisao_tail_envelope/MANIFESTO_ACEITE_DELTA_V2.json',
        'provisional_consolidation': 'proveniencia/consolidacao_018/MANIFESTO_CONSOLIDACAO_PROVISORIA.json',
    }.items()}
    sources = json.loads((ROOT / 'proveniencia/consolidacao_018/FONTES_E_PINS.json').read_bytes())
    historical = [check_pin(x, allow_backup=True) for x in sources['sources']]
    summary = json.loads((ROOT / 'preregistros/conjunto_d/d_calibration_member_inventory/RESUMO_INVENTARIO.json').read_bytes())
    request_path = ROOT / 'D_CALIBRATION_MEMBER_INVENTORY_REQUEST.json'
    old_request = request_path.read_bytes()
    old_value = json.loads(old_request)
    assert summary['request_id'] == old_value['request_id']
    assert summary['total_archive_bytes'] <= old_value['limits']['max_total_archive_bytes']
    assert all(x['bytes'] <= old_value['limits']['max_archive_bytes_each'] for x in summary['archive_summaries'])
    assert summary['science_data_opening_authorized'] is False
    assert summary['contracts_holds_V1_edited'] is False
    assert summary['automatic_download_retries'] == 0
    receipt = {'at': now, 'status': 'DOCUMENTARY_DELIVERIES_VERIFIED_NOT_SCIENTIFIC_ADOPTION',
               'manifests': checked, 'provisional_source_versions': historical,
               'calibration_member_inventory': summary,
               'tail_delta': 'F9 d0 with positive lower statistic is INVALID/null before resource/tail/aggregation; d>0 and models/alpha unchanged; implementation preparation delegated separately.',
               'consolidation_scope': 'Snapshot500 accepted as a provisional report with versioned accumulator sources; F1/F3 and mission remain incomplete.',
               'official_manager_identity': MANAGER,
               'official_manager_delivery': 'a178d269 delivery received through official send_message_to_thread, map504',
               'map_sequences': [498, 500, 501, 502, 503, 504],
               'ROOT_read': ['Inventory note', 'Consolidation report', 'Tail V2 contract and cases', 'Independent V2 review'],
               'science_rerun': False, 'new_provider_calls': 0, 'data_opened_for_verdict': False}
    save_json(out, receipt)
    receipt_pin = file_info(out)
    old_value.update(status='RESPONDED_DOCUMENTARY_DELIVERY_VERIFIED', response_received_at=now,
                     response_manifest=checked['D_inventory']['manifest'], root_receipt=receipt_pin, map_seq=504)
    assert request_path.read_bytes() == old_request
    save_json(request_path, old_value)

    new_path = ROOT / 'F9_MM_MODEL_PREPARATION_REQUEST.json'
    assert not new_path.exists()
    request = {'request_id': str(uuid.uuid4()), 'created_at': now, 'status': 'PREPARED_NOT_SENT',
               'manager_thread_id': MANAGER,
               'scope': 'Documentary and symbolic specification of the five F9 MM/maser error terms; no observed central values, likelihood, scientific execution or remote provider calls.',
               'source_draft': file_info(ROOT / 'f9_consolidated_draft/RASCUNHO_F9_CONSOLIDADO.md'),
               'source_resolver': file_info(ROOT / 'f9_consolidated_draft/RESOLUTOR_F9.json'),
               'source_calibration': file_info(ROOT / 'f9_calibration_bound/CALIBRATION_BOUND_CANDIDATE.json'),
               'output_folder': str(ROOT / 'f9_mm_model_preparation'),
               'alternatives_required': ['Gaussian experiment conditional on published reported errors',
                                         'Primitive measurement model with exact/nonlinear transformation and calibrated inference'],
               'deliverables': ['Pinned source/formula/error semantics and symbolic five-row specification with units/Jacobians',
                                'Which covariance terms are fixed, estimated, asymmetric, dependent or unresolved; no inference of missing correlations',
                                'Concrete recommended preparation and alternative with consequences for common covariance/support and tail bound; not ratification',
                                'Candidate contract and independent synthetic control plan only; no execution'],
               'limits': {'remote_calls': 0, 'new_downloads': 0, 'scientific_executions': 0, 'central_values_opened': 0},
               'no_repeat_request': True, 'data_opening_authorized': False,
               'reason': 'Existing consolidated F9 preparation lists these five terms as a concrete unresolved model component; resolves a prerequisite without opening the composite.'}
    save_json(new_path, request)

    with sqlite3.connect((BASE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        jobs = [dict(x) for x in db.execute("SELECT id,request_id,stage,execution_task_id,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled') ORDER BY created_at,id")]
        tasks = [dict(x) for x in db.execute("SELECT id,status,execution_constraints FROM tasks WHERE status IN ('queued','running') ORDER BY created_at,id")]
    snapshot_path = ROOT / 'SLOT_SNAPSHOT.json'
    old = snapshot_path.read_bytes(); snapshot = json.loads(old)
    snapshot.update(checked_at=now, nonterminal=jobs, executions=tasks, next_state='needs_attention',
                    next_error='Geração canônica diferente da autorizada no pedido.',
                    dispatch='none; original job pin preserved; existing failed/uncertain units not reopened')
    assert snapshot_path.read_bytes() == old
    save_json(snapshot_path, snapshot)
    slots_path = BASE / 'state/handoffs/slot_management.json'
    old = slots_path.read_bytes(); slots = json.loads(old)
    slots['last_checked_at'] = now
    slots['queue_read_error'].update(at=now, operation='next', receipt='needs_attention_without_job_id_due_get_validation', dispatch='none')
    slots['ordem018_D_calibration_member_inventory_request'] = old_value
    slots['ordem018_F9_MM_model_preparation_request'] = request
    slots['ordem018_discriminante_slot_request']['latest_check'] = {
        'at': now, 'queue_state': 'needs_attention', 'nonterminal': len(jobs), 'active_executions': len(tasks),
        'new_provider_calls': 0, 'no_repeat_request': True, 'snapshot': file_info(snapshot_path),
        'useful_work': 'Received D member inventory; new distinct F9 MM specification prepared for manager; three local subagents preparing/reviewing independently.'}
    assert slots_path.read_bytes() == old
    save_json(slots_path, slots)
    print(json.dumps({'receipt': receipt_pin, 'manifest_entries': {k: v['entries'] for k, v in checked.items()},
                      'source_versions': len(historical), 'backups_resolved': sum(x['historical_backup'] for x in historical),
                      'new_request': request, 'queue_nonterminal': len(jobs), 'active_executions': len(tasks)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
