"""Operator-authorized review binding and next documentary draft; never E6."""
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace
import argparse,hashlib,importlib.util,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RUNS={'E3.2':'e3_2_actual_001','E3.3':'e3_3_actual_001','TEST':'test_actual_001'}
AUTH={'E3.2':'E3_2_OPERATOR_GO_RECORD_001.json','E3.3':'E3_3_OPERATOR_GO_RECORD_001.json','TEST':'TEST_OPERATOR_GO_RECORD_001.json'}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):return json.loads(p.read_bytes())


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage',choices=tuple(RUNS),required=True)
    p.add_argument('--review',type=Path,required=True);p.add_argument('--review-sha256',required=True);args=p.parse_args()
    manifest=HERE/'PREPARATION_MANIFEST_V1.json'
    if sha(manifest)!='f7599a09dbff1c8400f2adce73917759f5ada8efcdd466707fde7c954f886e2e':raise ValueError('Manifest changed')
    for name in ('wall_stage_adapter.py','PREPARATION_PINS.json'):
        if sha(HERE/name)!=load(manifest)['artifacts'][name]['sha256']:raise ValueError('Helper changed')
    spec=importlib.util.spec_from_file_location('frozen_wall_adapter',HERE/'wall_stage_adapter.py')
    h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    folder=HERE/'candidates'/RUNS[args.stage];request=folder/'ADAPTER_REVIEW_REQUEST.json'
    h.finalize(SimpleNamespace(execute=True,request=request,request_sha256=sha(request),review=args.review,review_sha256=args.review_sha256))
    reviewed=h.pin(folder/'ADAPTER_REVIEWED.json');next_stage={'E3.2':'E3.3','E3.3':'TEST'}.get(args.stage)
    next_ref=None
    if next_stage:
        prior_auth=load(HERE/AUTH[args.stage]);auth=dict(prior_auth)
        auth.update(stage=next_stage,issued_utc=datetime.now(timezone.utc).isoformat(),run_id=RUNS[next_stage],
            outcome='UNAVAILABLE',predecessor=reviewed,
            reason=('Sem execucao de campanha de recuperacao E3.3: alocacao ativa sem novas PE/injecoes; calibracao fisica nao paga.'
                if next_stage=='E3.3' else 'Sem posterior independente de teste: AWAITING_DATA em todas as celulas, campos fisicos null.'),
            operator_go='Main authorizes finalize eachrealstage onceRcloses exactpins, thenprepare next automatically, allthree untilTEST. NeverE6run; maintakesE6.',
            scope='Only documentary wall/TEST-absence draft after exact predecessor review; no science and no E6 execution',
            E3_3_authorized=next_stage=='E3.3',TEST_authorized=next_stage=='TEST',E6_authorized=False,
            prior_stage_review=h.pin(args.review))
        path=HERE/AUTH[next_stage];h.publish(path,auth)
        h.prepare(SimpleNamespace(execute=True,authorization=path,authorization_sha256=sha(path)))
        next_ref=h.pin(HERE/'candidates'/RUNS[next_stage]/'ADAPTER_REVIEW_REQUEST.json')
    report=dict(status='REVIEW_BOUND_NEXT_DRAFT_PENDING' if next_stage else 'ALL_DOCUMENTARY_STAGES_REVIEW_BOUND_NO_E6',
        recorded_utc=datetime.now(timezone.utc).isoformat(),stage=args.stage,reviewed_adapter=reviewed,
        review=h.pin(args.review),next_stage=next_stage,next_draft=next_ref,science_executed=False,E6_executed=False,order_completed=False)
    h.publish(HERE/(RUNS[args.stage].upper()+'_ADVANCE_HANDOFF.json'),report)
    print(json.dumps(report))


if __name__=='__main__':main()
