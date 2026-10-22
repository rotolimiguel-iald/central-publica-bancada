"""Activate reviewed computational continuation within the original Kerr deadline."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,argparse,subprocess,os,time
B=Path(__file__).resolve().parents[1];R=B.parent
sys.path.insert(0,str(B/'bis/e2_code'))
from registration_guard import checked_registration,sha,publish_new,time_guard

def strict(path):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate metadata key')
            result[key]=value
        return result
    def bad(value):raise ValueError('Nonfinite metadata')
    return json.loads(path.read_bytes(),object_pairs_hook=pairs,parse_constant=bad)

def main():
    p=argparse.ArgumentParser();p.add_argument('--review-sha256',required=True);args=p.parse_args()
    reg,digest=checked_registration();folder=B/'bis/e3_kerr_continuation';manifest=folder/'MANIFEST.json'
    reviewpath=B/'bis/e3_pyring_review/KERR_CONTINUATION_REVIEW.json'
    if sha(reviewpath)!=args.review_sha256:raise ValueError('Independent review changed')
    review=strict(reviewpath)
    if review['status']!='KERR_CONTINUATION_DELTA_CLOSED' or review['blocking_findings']!=[] or review['manifest_sha256']!=sha(manifest):
        raise ValueError('Continuation not independently closed')
    if review['authorizer_sha256']!=sha(Path(__file__)):raise ValueError('Authorizer changed after review')
    original=B/'cache/E3_KERR220_CALIBRATION_V1';envelope=strict(original/'ENVELOPE.json')
    configuration=strict(manifest)
    if configuration['original_envelope_stop_utc']!=envelope['stop_utc']:raise ValueError('Original deadline changed')
    priorcost=strict(original/'COST.json')
    if len(priorcost['runs'])!=2 or any(r['cleanup']['group_absent'] is not True for r in priorcost['runs']):raise ValueError('Prior groups not closed')
    firstauth=strict(B/'bis/E3_KERR_AUTHORIZATION_V1.json')
    if firstauth['E2_registration_sha256']!=digest:raise ValueError('Prior authorization registration differs')
    f0=B/'bis/F0_CLOSED_20260922T215825Z.json';b2=R/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md'
    if sha(f0)!=firstauth['F0_receipt_sha256'] or sha(b2)!=firstauth['B2_delivery_sha256']:raise ValueError('F0/B2 changed')
    deadline=min(time_guard(reg),datetime.fromisoformat(envelope['stop_utc']))
    if datetime.now(timezone.utc)>=deadline:raise TimeoutError('Original shared Kerr envelope expired')
    authpath=B/'bis/E3_KERR_AUTHORIZATION_V2.json';log=B/'bis/E3_KERR_LAUNCH_V2.log';receipt=B/'bis/E3_KERR_LAUNCH_V2.json'
    if any(p.exists() for p in (authpath,log,receipt)):raise FileExistsError('Continuation attempt already exists')
    auth={'status':'CALIBRATION_ONLY_REVIEWED','manifest_filename':'MANIFEST.json','manifest_sha256':sha(manifest),
      'approved_utc':datetime.now(timezone.utc).isoformat(),'valid_until_utc':deadline.isoformat(),
      'reviewer':'Beauvoir independent delta review; principal applies existing GO',
      'review_sha256':sha(reviewpath),'parent_authorization_sha256':sha(B/'bis/E3_KERR_AUTHORIZATION_V1.json'),
      'parent_cost_sha256':sha(original/'COST.json'),'original_envelope_sha256':sha(original/'ENVELOPE.json'),
      'E2_registration_sha256':digest,'authorizer_sha256':sha(Path(__file__)),
      'scope':'Known calibration event; prior failed attempts immutable; no change to convergence/prior/data; original absolute deadline retained'}
    publish_new(authpath,auth);start=time.perf_counter();error=None;rc=None
    command=[sys.executable,'-B',str(folder/'controller.py'),'--authorization',str(authpath)]
    try:
        with log.open('xb') as f:
            result=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,
              env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'})
        rc=result.returncode
        if rc:error={'type':'ChildFailure','returncode':rc}
    except Exception as exc:error={'type':type(exc).__name__,'message':str(exc)}
    value={'status':'COMPLETED_REVIEW_PENDING' if error is None else 'FAILED_OR_PARTIAL','returncode':rc,'error':error,
      'registration_sha256':digest,'authorization_sha256':sha(authpath),'log_sha256':sha(log) if log.exists() else None,
      'original_absolute_deadline':deadline.isoformat(),'wall_seconds':time.perf_counter()-start,
      'finished_utc':datetime.now(timezone.utc).isoformat(),'command':command,
      'scope':'Controller rc0 is not accepted posterior; inspect variant/convergence/comparison. No competing outer timeout.'}
    publish_new(receipt,value);print(json.dumps(value))
    if error:raise SystemExit(2)
if __name__=='__main__':main()
