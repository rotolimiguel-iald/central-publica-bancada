"""Activate the independently reviewed calibration after B2 and F0 closure."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,sys,subprocess,time,os
B=Path(__file__).resolve().parents[1];R=B.parent
sys.path.insert(0,str(B/'bis/e2_code'))
from registration_guard import checked_registration,sha,publish_new,time_guard

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--manifest-sha256',required=True)
    p.add_argument('--review',required=True);p.add_argument('--review-sha256',required=True)
    p.add_argument('--f0-receipt',required=True);a=p.parse_args()
    reg,digest=checked_registration();folder=B/'bis/e3_pyring_preparation'
    manifest=(folder/a.manifest).resolve();review=(B/'bis/e3_pyring_review'/a.review).resolve()
    if manifest.parent!=folder or review.parent!=B/'bis/e3_pyring_review':raise ValueError('Only local manifest/review filenames')
    if sha(manifest)!=a.manifest_sha256 or sha(review)!=a.review_sha256:raise ValueError('Reviewed bytes changed')
    f0=(B/'bis'/a.f0_receipt).resolve()
    if f0.parent!=B/'bis':raise ValueError('Local F0 receipt required')
    closed=json.loads(f0.read_bytes())
    if closed['status']!='F0_OWNED_DIAGNOSTIC_JOBS_CLOSED__ANNEX_ONLY' or closed['after_processes'] or closed['registration_sha256']!=digest:
        raise ValueError('F0 not closed under this registration')
    b2=R/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md'
    if sha(b2)!=closed['B2_delivery_sha256']:raise ValueError('B2 changed')
    deadline=time_guard(reg);authpath=B/'bis/E3_KERR_AUTHORIZATION_V1.json'
    auth={'status':'CALIBRATION_ONLY_REVIEWED','manifest_filename':a.manifest,'manifest_sha256':sha(manifest),
      'approved_utc':datetime.now(timezone.utc).isoformat(),'valid_until_utc':deadline.isoformat(),
      'reviewer':'Beauvoir independent preparation review; principal applies existing GO after reading',
      'review_path':review.relative_to(R).as_posix(),'review_sha256':sha(review),
      'F0_receipt_sha256':sha(f0),'B2_delivery_sha256':sha(b2),'E2_registration_sha256':digest,
      'exposure':'NONBLIND_CALIBRATION_ONLY','scope':'Measured reproduction attempt; source/PSD/strain identity remains OPEN',
      'authorizer_sha256':sha(Path(__file__))}
    log=B/'bis/E3_KERR_LAUNCH_V1.log';receipt=B/'bis/E3_KERR_LAUNCH_V1.json'
    if any(p.exists() for p in (authpath,log,receipt)):raise FileExistsError('Prior launch attempt preserved')
    publish_new(authpath,auth);start=time.perf_counter();rc=None;error=None
    command=[sys.executable,'-B',str(folder/'controller.py'),'--authorization',str(authpath)]
    try:
        with log.open('xb') as f:
            child=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,
              env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'})
        rc=child.returncode
        if rc:error={'type':'ChildFailure','returncode':rc}
    except Exception as exc:error={'type':type(exc).__name__,'message':str(exc)}
    value={'status':'EXECUTION_COMPLETED_REVIEW_PENDING' if error is None else 'EXECUTION_FAILED_OR_PARTIAL',
      'error':error,'returncode':rc,'command':command,'registration_sha256':digest,
      'authorization_sha256':sha(authpath),'log_sha256':sha(log),'wall_seconds':time.perf_counter()-start,
      'finished_utc':datetime.now(timezone.utc).isoformat(),
      'scope':'A zero launcher return code is not posterior acceptance; inspect every variant and convergence. Kerr counter counts calls initiated after its guard, unlike PE entry counter.'}
    publish_new(receipt,value);print(json.dumps(value))
    if error:raise SystemExit(2)

if __name__=='__main__':main()
