"""One-use ROOT decision after independent review; never starts controls."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import json
from audit_inputs import file_info, save_json

ROOT = Path(__file__).resolve().parent
P = ROOT / 'f9_tail_envelope_implementation_v2'
R = ROOT / 'derivacoes/revisao_tail_implementation_v2'

def check(entry):
    actual = file_info(entry['path'])
    assert all(actual[k] == entry[k] for k in ('bytes', 'sha256')), actual['path']
    return actual

def main():
    for folder in (P, ROOT / 'f9_tail_envelope_implementation'):
        for name in ('AUTORIZACAO_ROOT.json', 'CLAIM.json', 'RUN', 'TERMINAL_RECEIPT.json', 'FINALIZATION_FAILURE.json'):
            assert not (folder / name).exists(), str(folder / name)
    assert not (P / 'REVISAO_ROOT.json').exists()
    manifest = json.loads((P / 'MANIFESTO_IMPLEMENTACAO.json').read_bytes())
    review = json.loads((R / 'MANIFESTO_REVISAO_DELTA_V2.json').read_bytes())
    inputs = json.loads((P / 'EXECUTION_INPUTS.json').read_bytes())
    contract = json.loads((P / 'CONTROL_CONTRACT.json').read_bytes())
    assert review['status'] == 'ACCEPT_STATIC_DELTA_FOR_ROOT_DECISION_ON_SYNTHETIC_CONTROLS'
    checked = [check(e) for e in manifest['files'] + inputs['pins'] + review['files'] + [review['source']]]
    assert inputs['request_id'] == contract['request_id'] == manifest['request_id']
    contract_pin = file_info(P / 'CONTROL_CONTRACT.json')
    inputs_pin = file_info(P / 'EXECUTION_INPUTS.json')
    decision = {
        'request_id': contract['request_id'], 'at': datetime.now(timezone.utc).isoformat(),
        'decision': 'ACCEPT_REVIEW_AUTHORIZE_SINGLE_BOUNDED_SYNTHETIC_CONTROL_UNIT',
        'authority': 'Active operator goal ORDEM_018; bounded preparation controls, no observed verdict.',
        'independent_review': file_info(R / 'MANIFESTO_REVISAO_DELTA_V2.json'),
        'contract': contract_pin, 'execution_inputs': inputs_pin,
        'verified_pin_comparisons': len(checked), 'verified_pins': checked,
        'scope': '8 primary and 9 negative synthetic control groups, one fixed child, nominal total30s.',
        'acceptance': 'Actual external exit0 plus matching provisional receipt/hash/identity and no FINALIZATION_FAILURE; no automatic retry.',
        'errata': 'Budget historical hard process budget docstring is subordinate to nominal cooperative contract; no hard OS guarantee. Output caps are post-collection acceptance caps.',
        'physical_certification': False, 'observed_data_authorized': False,
        'remote_calls_authorized': False, 'PE_authorized': False,
        'alternatives': ['Exact rational fixed-grid implementation with provisional receipt and external exit acceptance (selected)', 'Incremental bounded capture and alternative numerical backend (not necessary for this fixed unit)'],
    }
    save_json(P / 'REVISAO_ROOT.json', decision)
    save_json(P / 'AUTORIZACAO_ROOT.json', {
        'request_id': contract['request_id'], 'authorized': True, 'authorized_by': 'ROOT',
        'scope': 'F9_SYNTHETIC_TAIL_CONTROLS_ONLY',
        'contract_sha256': contract_pin['sha256'], 'execution_inputs_sha256': inputs_pin['sha256'],
        'one_execution_only': True, 'total_wall_seconds': 30, 'implementation_review_accepted': True,
        'review': file_info(P / 'REVISAO_ROOT.json'), 'observed_data_authorized': False,
        'created_at': datetime.now(timezone.utc).isoformat(),
    })
    print(json.dumps({'decision': file_info(P / 'REVISAO_ROOT.json'), 'authorization': file_info(P / 'AUTORIZACAO_ROOT.json'), 'checked': len(checked)}))

if __name__ == '__main__':
    main()
