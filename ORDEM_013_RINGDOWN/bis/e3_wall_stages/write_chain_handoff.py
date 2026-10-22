"""Custody-only handoff after all three independent reviews; no E6 execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):return json.loads(p.read_bytes())


def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))


def check(ref):
    p=(ROOT/ref['path']).resolve()
    if not p.is_relative_to(ROOT) or sha(p)!=ref['sha256']:raise ValueError('Changed pin')
    return p


def main():
    refs={};details={};previous=load(HERE/'PREPARATION_PINS.json')['E2_ACTIVATION']
    for stage,run in [('E3.2','e3_2_actual_001'),('E3.3','e3_3_actual_001'),('TEST','test_actual_001')]:
        folder=HERE/'candidates'/run;p=folder/'ADAPTER_REVIEWED.json';row=load(p)
        review=load(check(row['review']));artifact=load(check(row['artifact']))
        request=folder/'ADAPTER_REVIEW_REQUEST.json';fin=load(folder/'FINALIZATION_RECEIPT.json')
        if review['status']!='ACCEPTED_FOR_E6_MAPPING' or review['blocking_findings'] or review['request_sha256']!=sha(request):raise ValueError('Review absent')
        if row['predecessor']!=previous or fin['final_adapter']!=pin(p) or fin['E6_executed']:raise ValueError('Chain differs')
        for k in ('bindings','timeline','predecessor','outcome','stage','registration_sha256'):
            if row[k]!=review[k]:raise ValueError('Review scope differs')
        check(row['predecessor']);previous=pin(p);refs[stage]=previous
        details[stage]=dict(outcome=row['outcome'],timeline_kind=row['timeline']['kind'],bindings=len(row['bindings']),
            review=row['review'],artifact=row['artifact'],issued_utc=row['issued_utc'],reviewed_utc=review['reviewed_utc'],
            finalization=pin(folder/'FINALIZATION_RECEIPT.json'),request=pin(request))
        if stage=='TEST':
            if len(row['bindings'])!=180 or len(artifact['rows'])!=180:raise ValueError('Coverage differs')
            if any(r['summary']!={'test_data_present':False,'verdict':'AWAITING_DATA'} or
                any(v is not None for v in r['metrics'].values()) or r['gate']['correction_over_sigma_physical'] is not None
                for r in artifact['rows']):raise ValueError('Unexpected physical readout')
    manifest=HERE/'PREPARATION_MANIFEST_V1.json'
    for name in ('wall_stage_adapter.py','PREPARATION_PINS.json','PREPARATION.md'):
        if sha(HERE/name)!=load(manifest)['artifacts'][name]['sha256']:raise ValueError('Preparation changed')
    value=dict(status='THREE_REVIEWED_DOCUMENTARY_ADAPTERS_READY_FOR_PRINCIPAL',created_utc=datetime.now(timezone.utc).isoformat(),
        reviewed_stages=refs,details=details,preparation_manifest=pin(manifest),helper=pin(HERE/'wall_stage_adapter.py'),
        authority='Operator GO in current task: finalize exact independent reviews and prepare next through TEST; E6 stays with main',
        preparation_fixtures={'passed':45,'total':45,'source':pin(HERE/'FIXTURE_RESULTS_V2.json')},
        physical_calibration_paid=False,test_posterior_available=False,cost_per_converged_PE=None,
        TEST_cells=180,TEST_verdict='AWAITING_DATA',E6_executed=False,E7_extraction_executed=False,science_executed=False,order_completed=False)
    target=HERE/'STAGE_CHAIN_HANDOFF_V1.json';raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    tmp=target.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw) or len(raw)>25_000_000:raise ValueError('Size')
    os.link(tmp,target);tmp.unlink()
    print(json.dumps(dict(handoff=pin(target),reviewed_stages=refs)))


if __name__=='__main__':main()
