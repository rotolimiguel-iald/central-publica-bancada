"""Hash-only preparation freeze; no stage creation or scientific execution."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
E6=HERE.parent/'e6_prepare_v3'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):return json.loads(p.read_bytes())


def pin(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))


def write(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>25_000_000:raise ValueError('Size')
    pending=p.with_name(p.name+'.pending')
    with pending.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if pending.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(pending,p);pending.unlink()


def main():
    sources=load(E6/'SOURCE_PINS.json')['sources']
    closing=HERE.parent/'e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json'
    review=load(closing)
    if review['status']!='BLOCKERS_CLOSED_PREPARATION_ONLY' or review['blocking_findings']:raise ValueError('E6 preparation review open')
    manifest=E6/'PREPARATION_MANIFEST_V3.json'
    if sha(manifest)!=review['manifest_sha256']:raise ValueError('E6 manifest differs')
    for name,digest in review['package_sha256'].items():
        if sha(E6/name)!=digest:raise ValueError('Frozen E6 package differs')
    preserved={}
    for dirname,filename in [('e6_prepare_v2','PREPARATION_MANIFEST_V2.json'),('e6_prepare_v3','PREPARATION_MANIFEST_V3.json')]:
        path=HERE.parent/dirname/filename
        for name,item in load(path)['artifacts'].items():
            if sha(path.parent/name)!=item['sha256']:raise ValueError('Preservation failed '+dirname+'/'+name)
        preserved[dirname]=pin(path)
    pins=dict(schema='E3_WALL_STAGE_PREPARATION_PINS_V1',E6_contract=pin(E6/'CONTRACT.json'),
        E6_manifest=pin(manifest),E6_review=pin(closing),E6_code=pin(E6/'generate_reach_table.py'))
    for name in ('E0','E2','E2_ACTIVATION'):
        ref=sources[name]
        if sha(ROOT/ref['path'])!=ref['sha256']:raise ValueError('Source differs '+name)
        pins[name]=pin(ROOT/ref['path'])
    write(HERE/'PREPARATION_PINS.json',pins)
    result=load(HERE/'FIXTURE_RESULTS_V2.json')
    if result['passed']!=result['total'] or result['code_sha256']!=sha(HERE/'wall_stage_adapter.py'):raise ValueError('Fixtures/code differ')
    ast.parse((HERE/'wall_stage_adapter.py').read_bytes())
    artifacts={}
    for p in sorted(HERE.rglob('*')):
        if p.is_file():
            if p.stat().st_size>25_000_000:raise ValueError('Size')
            artifacts[p.relative_to(HERE).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
    target=HERE/'PREPARATION_MANIFEST_V1.json'
    write(target,dict(schema='E3_WALL_STAGE_PREPARATION_MANIFEST_V1',status='FROZEN_FOR_INDEPENDENT_REVIEW',
        frozen_utc=datetime.now(timezone.utc).isoformat(),artifacts=artifacts,preserved_E6=preserved,
        fixtures={'passed':result['passed'],'total':result['total']},science_executed=False,
        actual_stage_receipts_created_at_freeze=False,E6_authorized=False,
        runtime_candidates_excluded='Created after freeze only under separate principal GO; never part of these preparation fixtures'))
    print(json.dumps(dict(manifest=pin(target),helper=pin(HERE/'wall_stage_adapter.py'),pins=pin(HERE/'PREPARATION_PINS.json'),fixtures=result['passed'])))


if __name__=='__main__':main()
