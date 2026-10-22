"""Record the operator's explicit E3.2-only GO, then emit an unreviewed draft.

Not an E3.3/TEST/E6 authorization; no independent review is manufactured.
"""
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace
import hashlib,importlib.util,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):return json.loads(p.read_bytes())


def pin(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}


def main():
    manifest=HERE/'PREPARATION_MANIFEST_V1.json'
    if sha(manifest)!='f7599a09dbff1c8400f2adce73917759f5ada8efcdd466707fde7c954f886e2e':raise ValueError('Helper manifest changed')
    frozen=load(manifest)
    for name in ('wall_stage_adapter.py','PREPARATION_PINS.json'):
        if sha(HERE/name)!=frozen['artifacts'][name]['sha256']:raise ValueError('Frozen package changed')
    budget=ROOT/'ORDEM_013_RINGDOWN/ORCAMENTO_40H.json'
    if sha(budget)!='892e416585062eef5229e01c2e8a6c5b8d3c4ee8a10a72798c0ab2034e5f42e4':raise ValueError('Different actual allocation')
    activation=ROOT/'ORDEM_013_RINGDOWN/bis/E3_WALL_BUDGET_ACTIVATION_V1.json'
    event=load(activation);allocation=load(budget)
    if event['status']!='E3_2_WALL_ALLOCATION_REGISTERED' or event['budget_sha256']!=sha(budget):raise ValueError('Activation differs')
    witness=ROOT/allocation['witness_relative_to_Chatgpt']
    if sha(witness)!=event['witness_sha256']:raise ValueError('Witness changed')
    b3=ROOT/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B3_piloto_e_orcamento.md'
    b3manifest=ROOT/'ORDEM_013_RINGDOWN/bis/B3_DELIVERY_MANIFEST.json'
    if sha(b3)!='f8c0a12ab4fe9505392006d9d3dce6938f972eb35a734ad1ea9b38977fb79394' or load(b3manifest)['delivery_sha256']!=sha(b3):raise ValueError('B3 changed')
    pins=load(HERE/'PREPARATION_PINS.json')
    spec=importlib.util.spec_from_file_location('frozen_wall_adapter',HERE/'wall_stage_adapter.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    auth=dict(status='AUTHORIZED_WALL_STAGE_CANDIDATE_AFTER_BUDGET',stage='E3.2',helper_sha256=sha(HERE/'wall_stage_adapter.py'),
        issued_utc=datetime.now(timezone.utc).isoformat(),run_id='e3_2_actual_001',outcome='COMPLETED',
        reason='Registro documental efetivo da alocacao zero nova PE/injecao. COMPLETED refere-se somente ao registro E3.2; calibracao fisica nao paga.',
        registration=pins['E2'],E2_activation=pins['E2_ACTIVATION'],budget=pin(budget),budget_witness=pin(witness),
        predecessor=pins['E2_ACTIVATION'],E6_contract=pins['E6_contract'],E0=pins['E0'],
        principal_notes=[pin(activation),pin(b3),pin(b3manifest)],test_posterior_available=False,new_PE_allowed=False,
        new_injections_allowed=False,cost_per_converged_PE=None,
        authority_kind='OPERATOR_GO_IN_CURRENT_TASK_RECORDED_NOW_NOT_BACKDATED',
        operator_go='MainGOconstructE3.2 walladapter draft fromthisactualallocation only (notE3.3yetuntilRreview).',
        budget_activation_receipt=pin(activation),helper_manifest=pin(manifest),
        E3_3_authorized=False,TEST_authorized=False,E6_authorized=False,
        scope='Only unreviewed E3.2 declaration; finalize and later stages are not performed by this command')
    path=HERE/'E3_2_OPERATOR_GO_RECORD_001.json';helper.publish(path,auth)
    helper.prepare(SimpleNamespace(execute=True,authorization=path,authorization_sha256=sha(path)))
    draft=HERE/'candidates/e3_2_actual_001/ADAPTER_REVIEW_REQUEST.json'
    obj=load(draft)
    if obj['status']!='UNREVIEWED_NOT_E6_RECEIPT' or obj['draft']['bindings']!=[]:raise ValueError('Unexpected draft')
    report=dict(status='E3_2_DRAFT_ISSUED_AWAITING_INDEPENDENT_REVIEW',issued_utc=datetime.now(timezone.utc).isoformat(),
        preparation_manifest=pin(manifest),helper=pin(HERE/'wall_stage_adapter.py'),operator_GO_record=pin(path),draft=pin(draft),
        actual_budget=pin(budget),budget_activation=pin(activation),B3=pin(b3),actual_stage='E3.2',
        actual_E3_3_created=False,actual_TEST_created=False,E6_executed=False,science_executed=False,
        reviewed_adapter_created=False,final_order_completed=False)
    helper.publish(HERE/'E3_2_DRAFT_HANDOFF_001.json',report)
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
