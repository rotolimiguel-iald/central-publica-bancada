"""Byte custody and documentary manifest only: no symbolic or dynamical execution."""
from pathlib import Path
import datetime
import hashlib
import json

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
ORIGIN=BASE/'pair_covariance_r59'/'oh_correlation'

def pin(path):
    p=Path(path)
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

def write_new(path, data):
    raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    with Path(path).open('xb') as f: f.write(raw)

def main():
    target=OUT/'CUSTODY_R61.json'
    if target.exists(): raise FileExistsError(target)
    manifest=json.loads((ORIGIN/'SOURCE_PINS_R59.json').read_text(encoding='utf8'))
    verified=[]
    for old in manifest['sources']:
        measured=pin(old['path'])
        if measured['sha256']!=old['sha256'] or measured['bytes']!=old['bytes']:
            raise ValueError('Changed source: '+old['path'])
        verified.append({**measured,'role':old['role'],'matched_R59':True})
    sources=OUT/'sources';sources.mkdir(exist_ok=True)
    copies=[]
    for name in ['explore_pairs_r59.py','EXPLORATION_R59.json','SOURCE_PINS_R59.json']:
        origin=ORIGIN/name; dest=sources/name
        raw=origin.read_bytes()
        with dest.open('xb') as f: f.write(raw)
        if dest.read_bytes()!=raw: raise ValueError('Custody mismatch: '+name)
        copies.append({'original':pin(origin),'copy':pin(dest),'byte_identical':True})
    source_json=ORIGIN/'EXPLORATION_R59.json'
    result=json.loads(source_json.read_text(encoding='utf8'))
    raw_fact_summary={
        'source_top_level_keys':list(result),
        'C_L_terms':result['C']['L'],
        'B_L_terms':result['B']['L'],
        'prepared_OH_states':list(result['states']),
        'correction_candidates':result['correction_candidates'],
        'new_symbolic_execution':False,
        'new_numerical_execution':False,
    }
    receipt={
        'status':'CUSTODIED_DOCUMENTARY_CANDIDATE_NOT_INDEPENDENTLY_ACCEPTED',
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'actor':'codex-oh-pair-r61',
        'team_claim':939,
        'mission_reference':r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json',
        'recovery_receipt':pin(BASE/'r4_recovery_authorized_20261017'/'RECOVERY_RESULT.json'),
        'project_start':pin(OUT/'MISSION_PROJECT_START_R61.json'),
        'script':pin(__file__),
        'report':pin(OUT/'RELATORIO_CANDIDATO_R61.md'),
        'copies':copies,
        'verified_sources':verified,
        'raw_fact_summary':raw_fact_summary,
        'limits':[
            'R59 exploration not rerun or independently reproduced.',
            'Eight-dimensional hard-core truncation; no CCR or infinite-bosonic transfer.',
            'Density countermodel in report is analytical interpretation of existing traces.',
            'No beta evaluation, provider, measurement, kernel, canonical-memory, gate or mission mutation.',
            'R4 whole criterion remains open; coordinator owns lease and acceptance.'
        ]
    }
    write_new(target,receipt)
    print(json.dumps({'status':receipt['status'],'custody':pin(target),'sources':len(verified),'copies':len(copies)},ensure_ascii=False))

if __name__=='__main__':main()
