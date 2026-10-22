"""Record the explicit principal GO using hashes read from the actual artifacts."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
ROOT=B.parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def main():
    if (HERE/'E7_EXECUTION_INDEPENDENT_REVIEW.json').exists():raise FileExistsError('No duplicate review')
    manifest=json.loads((HERE/'PREPARATION_MANIFEST.json').read_bytes())
    for row in manifest['files']:
        if sha(HERE/row['name'])!=row['sha256']:raise ValueError('Frozen preparation differs')
    files={'e6_result':'bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.json',
           'e6_review':'bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json',
           'authorization':'bis/E7_FINAL_AUTHORIZATION_V1.json',
           'execution_receipt':'bis/E7_FINAL_EXECUTION_V1.json',
           'posterior':'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json',
           'e7_result':'bis/E7_FULLSAMPLE_RESULT_V1.json'}
    inputs={k:{'relative_to_Chatgpt':(B/v).relative_to(ROOT).as_posix(),
               'sha256':sha(B/v),'bytes':(B/v).stat().st_size} for k,v in files.items()}
    receipt=json.loads((B/files['execution_receipt']).read_bytes())
    if receipt['status']!='E7_EXECUTED_NO_PHYSICAL_TEST' or receipt['failure'] is not None:
        raise ValueError('E7 execution not completed')
    obj={'status':'GO_E7_REVIEW_AFTER_E6','created_utc':datetime.now(timezone.utc).isoformat(),
         'registration_sha256':sha(B/'RINGDOWN_5SIGMA_V1.json'),
         'verifier_sha256':sha(HERE/'verify_e7_execution.py'),'inputs':inputs,
         'authorization_basis':'Explicit principal GO in current conversation after actual E7 completion; one review under frozen PLAN.md,600s/min(stop)-10s.',
         'materializer_sha256':sha(Path(__file__))}
    path=HERE/'GO_E7_REVIEW_V1.json'
    raw=(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode()
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps({'go_sha256':sha(path),'verifier_sha256':obj['verifier_sha256'],'inputs':inputs}))

if __name__=='__main__':main()
