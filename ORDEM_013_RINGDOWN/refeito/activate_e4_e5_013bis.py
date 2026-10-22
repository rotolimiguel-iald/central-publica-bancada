"""Execute only the witnessed deterministic archived E4/E5 package once."""
import sys,os,json,time,subprocess
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'bis/e2_code'))
from registration_guard import checked_registration,contained,sha,publish_new,time_guard

def main():
    reg,digest=checked_registration()
    O=B/'bis/e4_e5_prepare';authpath=B/'bis/E4_E5_AUTHORIZATION_V1.json'
    resultpath=B/'bis/E4_E5_EXECUTION_V1.json';log=B/'bis/E4_E5_EXECUTION_V1.log'
    if any(p.exists() for p in (authpath,resultpath,log,O/'runs/authorized_001')):raise FileExistsError('Prior attempt preserved')
    auth={'status':'AUTHORIZED_BY_PRINCIPAL_AFTER_E2','allowed_task':'E4_E5_DETERMINISTIC_ARCHIVED_CALIBRATION_ONLY',
      'new_test_data_allowed':False,'package_sha256':reg['e4_e5_preparation_pins'],
      'E2_registration_path':str(B/'RINGDOWN_5SIGMA_V1.json'),'E2_registration_sha256':digest,
      'E2_tunnel_witness_path':str(contained(reg['witness_relative_to_Chatgpt'])),
      'E2_tunnel_witness_sha256':sha(contained(reg['witness_relative_to_Chatgpt'])),
      'run_id':'authorized_001','created_utc':datetime.now(timezone.utc).isoformat(),
      'authorizer_sha256':sha(Path(__file__))}
    publish_new(authpath,auth);start=time.perf_counter();failure=None;rc=None
    command=[sys.executable,'-B','-O',str(O/'deterministic_e4_e5.py'),'--execute','--authorization',str(authpath)]
    try:
        with log.open('xb') as f:
            child=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,
              timeout=max(1,time_guard(reg).timestamp()-time.time()-5),
              env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'})
        rc=child.returncode
        if rc:raise RuntimeError('Deterministic child failed, see retained log')
    except Exception as exc:failure={'type':type(exc).__name__,'message':str(exc)}
    value={'status':'EXECUTED_REVIEW_PENDING' if failure is None else 'EXECUTION_FAILED',
      'registration_sha256':digest,'authorization_sha256':sha(authpath),
      'log_sha256':sha(log) if log.exists() else None,'returncode':rc,'failure':failure,
      'wall_seconds':time.perf_counter()-start,'command':command,'finished_utc':datetime.now(timezone.utc).isoformat()}
    publish_new(resultpath,value);print(json.dumps(value))
    if failure:raise SystemExit(2)

if __name__=='__main__':main()
