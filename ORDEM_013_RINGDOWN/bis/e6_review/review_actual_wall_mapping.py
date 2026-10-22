"""Record an independently inspected E3.3/TEST documentary wall mapping.

Reads only pinned metadata; writes this review area. Never calls stage producers.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
HELPER = BASE / 'bis/e3_wall_stages'
SEEN = {}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(p):
    p = Path(p).resolve()
    raw = p.read_bytes()
    require(len(raw) <= 25_000_000, 'Metadata size')
    h = hashlib.sha256(raw).hexdigest()
    SEEN[p] = h
    return h


def load(p):
    sha(p)
    return json.loads(Path(p).read_bytes())


def checked(ref):
    require(set(ref) == {'path', 'sha256'}, 'Exact pin')
    p = (ROOT / ref['path']).resolve()
    require(p.is_relative_to(ROOT.resolve()) and p.suffix in ('.json', '.md'), 'Metadata path')
    require(not any('PRIVATE' in x.upper() or 'SECRET' in x.upper() for x in p.parts), 'Private path')
    require(sha(p) == ref['sha256'], 'Pin mismatch: ' + ref['path'])
    return p


def utc(t):
    value = datetime.fromisoformat(t.replace('Z', '+00:00'))
    require(value.utcoffset() is not None, 'Aware time')
    return value.astimezone(timezone.utc)


def fresh(p, raw):
    tmp = p.with_name(p.name + '.pending')
    with tmp.open('xb') as f:
        f.write(raw)
    require(tmp.read_bytes() == raw, 'Write verification')
    os.link(tmp, p)
    tmp.unlink()


def main():
    stage = sys.argv[1]
    require(stage in ('E3.3', 'TEST'), 'Explicit actual wall stage')
    request = Path(sys.argv[2]).resolve()
    require(request.is_relative_to((HELPER / 'candidates').resolve()), 'Actual candidate area')
    q = load(request); d = q['draft']; request_hash = sha(request)
    auth_string = q['authorization_path'].replace('\\', '/')
    if auth_string.startswith('/mnt/c/'):
        auth_string = 'C:/' + auth_string[len('/mnt/c/'):]
    authpath = Path(auth_string).resolve()
    require(authpath.is_relative_to(HELPER.resolve()), 'Helper GO path')
    require(sha(authpath) == q['authorization_sha256'], 'GO pin')
    auth = load(authpath)
    require(q['status'] == 'UNREVIEWED_NOT_E6_RECEIPT' and d['schema'] == 'E6_REVIEWED_STAGE_V2', 'Draft identity')
    require(d['stage'] == auth['stage'] == stage, 'Stage identity')
    require(auth['status'] == 'AUTHORIZED_WALL_STAGE_CANDIDATE_AFTER_BUDGET', 'Principal GO status')
    require(sha(HELPER / 'wall_stage_adapter.py') == q['helper_sha256'] == auth['helper_sha256'], 'Helper identity')
    for key in ('registration', 'E2_activation', 'budget', 'budget_witness', 'predecessor', 'E6_contract', 'E0'):
        checked(auth[key])
    require(auth['principal_notes'], 'Actual principal notes')
    for ref in auth['principal_notes']:
        checked(ref)
    require(all(auth[k] is False for k in ('test_posterior_available', 'new_PE_allowed', 'new_injections_allowed'))
            and auth['cost_per_converged_PE'] is None, 'Wall authorization scope')
    require(d['outcome'] == auth['outcome'] and d['outcome'] in ('PARTIAL', 'BLOCKED', 'UNAVAILABLE'), 'Wall outcome')
    reg = load(checked(auth['registration'])); act = load(checked(auth['E2_activation']))
    budget = load(checked(auth['budget'])); contract = load(checked(auth['E6_contract']))
    require(auth['registration']['path'] == 'ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json', 'E2 identity path')
    require(auth['budget']['path'] == reg['allocation_policy']['relative_to_Chatgpt'], 'Active budget slot')
    require(d['registration_sha256'] == auth['registration']['sha256'] == budget['parent_registration_sha256'] == act['registration_sha256'], 'Registration links')
    require(act['status'] == 'E2_ACTIVATION_COMPLETE' and budget['status'] == 'REGISTERED_ZERO_NEW_PE_MEASURED_INSTRUMENT_WALL', 'Activated wall allocation')
    jobs = load(checked({'path': budget['jobs_relative_to_Chatgpt'], 'sha256': budget['jobs_sha256']}))
    require(jobs['jobs'] == {} and jobs['schema_version'] == 'E2_PE_JOBS_V2' and jobs['parent_registration_sha256'] == d['registration_sha256'], 'No new jobs')
    witness = checked(auth['budget_witness']).read_text(encoding='utf-8-sig')
    require(re.findall(r'^allocation_sha256: ([0-9a-f]{64})\s*$', witness, re.M) == [auth['budget']['sha256']], 'Witness allocation')
    require(re.findall(r'^registered_utc: (\S+)\s*$', witness, re.M) == [budget['registered_utc']], 'Witness time')

    require(d['predecessor'] == auth['predecessor'], 'Actual predecessor')
    predpath = checked(d['predecessor']); pred = load(predpath)
    require(pred['stage'] == ('E3.2' if stage == 'E3.3' else 'E3.3') and pred['registration_sha256'] == d['registration_sha256'], 'Sequential predecessor')
    pred_review = load(checked(pred['review']))
    require(pred_review['status'] == 'ACCEPTED_FOR_E6_MAPPING' and pred_review['blocking_findings'] == [], 'Predecessor reviewed')
    for key in ('stage', 'registration_sha256', 'bindings', 'outcome', 'timeline', 'predecessor'):
        require(pred_review[key] == pred[key], 'Predecessor review field: ' + key)
    require(pred_review['artifact_sha256'] == pred['artifact']['sha256'], 'Predecessor artifact review pin')
    finalization = load(predpath.parent / 'FINALIZATION_RECEIPT.json')
    require(finalization['status'] == 'REVIEW_BOUND_NOT_E6_EXECUTED' and finalization['E6_executed'] is False, 'Predecessor finalization status')
    require(checked(finalization['final_adapter']) == predpath and finalization['review'] == pred['review'], 'Finalized predecessor identity')
    pred_request = load(checked(finalization['first_issuance_request']))
    require(finalization['first_issuance_request']['sha256'] == pred_review['request_sha256'], 'First declaration reviewed')
    require(pred == dict(pred_request['draft'], review=pred['review']), 'Finalization changed reviewed draft')
    pred_evidence = load(checked(pred['timeline']['evidence']))
    require(checked(pred['artifact']) == checked(pred['timeline']['evidence']), 'Predecessor wall artifact/evidence')

    source = load(checked(d['artifact']))
    require(d['timeline'] == {'kind': 'NO_EXECUTION', 'evidence': d['artifact'], 'recorded_utc_pointer': '/recorded_utc',
                             'reason_pointer': '/reason', 'predecessor_evidence_sha256_pointer': '/predecessor_evidence_sha256'}, 'Wall timeline, no execution times')
    require(source['schema'] == 'E3_WALL_SOURCE_V1' and source['status'] == 'NO_EXECUTION' and source['stage'] == stage, 'Wall source identity')
    require(source['predecessor_evidence_sha256'] == pred['timeline']['evidence']['sha256'], 'Source predecessor evidence')
    for key in ('registration', 'budget', 'budget_witness', 'principal_notes'):
        require(source[key] == auth[key], 'Source scope: ' + key)
    require(source['E0_floor_source'] == auth['E0'], 'Historical source identity')
    require(source['reason'] == auth['reason'] and isinstance(source['reason'], str) and source['reason'].strip(), 'Real documented reason')
    require(source['cost_per_converged_PE'] is None and source['test_posterior_available'] is False, 'No physical claims')
    if stage == 'E3.3':
        require(pred['timeline']['kind'] == 'ALLOCATION_REGISTERED' and pred['timeline']['evidence'] == auth['budget'], 'Actual registered allocation')
        require(source['rows'] == d['bindings'] == [], 'No E3.3 recovery measurements')
        previous_time = pred_evidence['registered_utc']
    else:
        require(pred['timeline']['kind'] == 'NO_EXECUTION' and pred_evidence['budget'] == auth['budget'], 'Same allocation E3.3 wall')
        previous_time = pred_evidence['recorded_utc']
        e0 = load(checked(auth['E0']))
        floors = {row['reading']: (i, row) for i, row in enumerate(e0['systematic_conditions'])}
        rows = source['rows']; bindings = d['bindings']
        expected_keys = {(route, reading, group) for route in contract['routes'] for reading in contract['readings'] for group in contract['data_groups']}
        require(len(rows) == len(bindings) == len(expected_keys), 'Actual wall mapping completeness')
        seen = set()
        for i, (row, binding) in enumerate(zip(rows, bindings)):
            key = tuple(row[k] for k in ('route', 'reading', 'data_group'))
            require(key in expected_keys and key not in seen, 'Actual wall cell identity'); seen.add(key)
            require(all(binding[k] == row[k] for k in ('route', 'reading', 'data_group', 'scope')), 'Binding row identity')
            require(row['reading_statute'] == contract['reading_statutes'][row['reading']], 'Reading statute')
            require(set(row['metrics']) == set(contract['metrics']) and all(v is None for v in row['metrics'].values()), 'All science metrics absent')
            require(row['summary'] == {'test_data_present': False, 'verdict': 'AWAITING_DATA'}, 'No observed test')
            gate = row['gate']; require(gate['color'] == 'red' and gate['decision_reviewed'] is False, 'Unpaid physical gate')
            require(all(gate[k] is False for k in contract['paid_flags']), 'No paid scientific flags')
            require(all(gate[k] is None for k in ('sigma_c_calibrated', 'sigma_sys_df', 'sigma_jit_recovered', 'correction_over_sigma_physical')), 'No physical calibration/ratio')
            require(binding['gate_pointer'] == '/rows/' + str(i) + '/gate' and binding['test_summary_pointer'] == '/rows/' + str(i) + '/summary', 'Exact wall pointers')
            units = contract['semantic_units'][row['route']]
            require(set(binding['metrics']) == set(contract['metrics']), 'Mapped metrics complete')
            for k, spec in binding['metrics'].items():
                require(spec == {'pointer': '/rows/' + str(i) + '/metrics/' + k, 'unit': units[k][0] if units[k] else 'INAPPLICABLE_NULL'}, 'Literal metric mapping')
            require(gate['units'] == {k: units[k][0] if units[k] else 'INAPPLICABLE_NULL' for k in contract['gate_fields']}, 'Gate mapping labels')
            if row['route'] == 'TAU220_POPULATION':
                ix, floor = floors[row['reading']]
                require(gate['floor5_INPUT'] == floor['floor5_INPUT'] and gate['floor15_sensitivity'] == floor['floor15_INPUT'], 'Historical floors copied exactly')
                require(row['historical_floor_context'] == {'source': auth['E0'], 'pointer': '/systematic_conditions/' + str(ix), 'statute': 'INPUT_HISTORICAL_NOT_CALIBRATION'}, 'Floor provenance')
            else:
                require(gate['floor5_INPUT'] is None and gate['floor15_sensitivity'] is None and row['historical_floor_context'] is None, 'No floor channel transport')
        require(seen == expected_keys, 'No selected readings')
    now = datetime.now(timezone.utc)
    require(utc(act['finished_utc']) <= utc(previous_time) <= utc(source['recorded_utc']) <= utc(d['issued_utc']) <= now, 'Documentary sequence')
    require(utc(pred['issued_utc']) <= utc(pred_review['reviewed_utc']) <= utc(finalization['published_utc']) <= utc(auth['issued_utc']) <= utc(source['recorded_utc']), 'Reviewed predecessor before next declaration')
    for path, pin in SEEN.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == pin, 'Input changed during review')
    review = dict(status='ACCEPTED_FOR_E6_MAPPING', stage=stage, registration_sha256=d['registration_sha256'],
        artifact_sha256=d['artifact']['sha256'], blocking_findings=[], reviewed_utc=datetime.now(timezone.utc).isoformat(),
        bindings=d['bindings'], outcome=d['outcome'], reviewer='R — Codex independent stage mapping reviewer, separate from W/helper producer',
        timeline=d['timeline'], predecessor=d['predecessor'], request_sha256=request_hash,
        request_path=request.relative_to(ROOT).as_posix(), helper_sha256=q['helper_sha256'], authorization_sha256=q['authorization_sha256'],
        checked_metadata_sha256={path.relative_to(ROOT).as_posix():h for path,h in SEEN.items()}, review_code_sha256=sha(Path(__file__)),
        scope='Actual documentary NO_EXECUTION wall mapping only; no physical calibration or observational test paid.',
        temporal_interpretation='recorded_utc is actual wall documentation only; no scientific start/end invented. issued_utc is preserved first declaration; finalization records later review-binding publication separately.',
        E6_execution_authorized=False, actual_E6_executed=False, new_science_executed=False, physical_calibration_paid=False)
    filename = ('E3_3' if stage == 'E3.3' else 'TEST') + '_ACTUAL_MAPPING_REVIEW_V1'
    path = HERE / (filename + '.json')
    fresh(path, (json.dumps(review, ensure_ascii=False, indent=2) + '\n').encode())
    md = '# ' + stage + ' — revisão independente do mapeamento real\n\n[REAL] **ACCEPTED_FOR_E6_MAPPING**, sem bloqueantes neste recorte. Outcome ' + d['outcome'] + ', timeline NO_EXECUTION: documentação da parede, não campanha científica.\n\n'
    md += 'Conferidos pins do pedido/GO/helper, orçamento ativo/testemunha/jobs vazios, predecessor finalizado/revisado, notas vinculadas, artefato, cronologia documental e bindings. Sem horários de execução inventados, alto poder exigido, mudança de E2 ou ciência.\n\n'
    md += ('E3.3 não contém resultados de recuperação; bindings e rows vazios.\n\n' if stage == 'E3.3' else 'TEST preserva todos os bindings documentais, dados ausentes, AWAITING_DATA, gate vermelho e métricas físicas null. Pisos históricos INPUT só em tau220, com igualdade e ponteiros conferidos.\n\n')
    md += 'A autorização de revisão sequencial do operador já foi dada. Este review pode ser vinculado pelo produtor ao pedido exato; não é autorização E6. Nenhum helper prepare/finalize real ou E6 foi executado pelo revisor; sem seed/offset/posterior de teste/strain/PE/MC. NOT_FALSIFIED nunca é CONFIRMED.\n\n'
    md += 'Pedido SHA256: `' + request_hash + '`.\n\nArtefato SHA256: `' + d['artifact']['sha256'] + '`.\n\nReview JSON SHA256: `' + sha(path) + '`.\n\nRevisado: ' + review['reviewed_utc'] + '.\n'
    fresh(HERE / (filename + '.md'), md.encode())
    print(json.dumps({'status': review['status'], 'stage': stage, 'review_path': str(path), 'review_sha256': sha(path),
                      'request_sha256': request_hash, 'bindings': len(d['bindings']), 'checked_inputs': len(review['checked_metadata_sha256'])}))


if __name__ == '__main__':
    main()
