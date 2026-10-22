"""Bounded WSL child group; blind logs stay on disk, analyst output only."""
import argparse,json,os,signal,subprocess,sys,time,resource
from pathlib import Path
from datetime import datetime,timezone
from registration_guard import checked_registration,time_guard,output_path,sha

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--job',required=True);args=parser.parse_args()
    if os.name!='posix':raise RuntimeError('Registered controller requires WSL POSIX process groups')
    reg,digest=checked_registration()
    if args.job not in reg['pe_jobs']:raise ValueError('Unknown registered job')
    cfg=reg['pe_jobs'][args.job]
    if cfg['sampler']['workers']<1 or cfg['sampler']['workers']>28:raise ValueError('Worker budget outside registered range')
    out=output_path(cfg['output_directory_name']+'_controller.json')
    log=output_path(cfg['output_directory_name']+'_private.log')
    if out.exists() or log.exists():raise FileExistsError('Controller destination already used')
    deadline=time_guard(reg).timestamp();started=time.time();stop=min(deadline,started+cfg['wall_budget_seconds'])
    command=[sys.executable,'-B',str(Path(__file__).with_name('pe_runner.py')),'--job',args.job]
    status='UNKNOWN';killed=False
    before=resource.getrusage(resource.RUSAGE_CHILDREN)
    with log.open('xb') as f:
        child=subprocess.Popen(command,stdout=f,stderr=subprocess.STDOUT,start_new_session=True,
          env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'})
        try:
            while child.poll() is None:
                if time.time()>=stop:
                    killed=True;os.killpg(child.pid,signal.SIGTERM)
                    try:child.wait(timeout=10)
                    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
                    break
                time.sleep(.5)
        finally:
            if child.poll() is None:
                os.killpg(child.pid,signal.SIGTERM)
                try:child.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    status='BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR' if killed else 'CHILD_COMPLETED_REQUIRES_REVIEW' if child.returncode==0 else 'CHILD_FAILED'
    result={'status':status,'job':args.job,'registration_sha256':digest,'started_utc':datetime.fromtimestamp(started,timezone.utc).isoformat(),
      'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.time()-started,
      'children_user_cpu_seconds':after.ru_utime-before.ru_utime,'children_system_cpu_seconds':after.ru_stime-before.ru_stime,
      'returncode':child.returncode,'private_log_sha256':sha(log),'private_log_bytes':log.stat().st_size,
      'blind':cfg['mode']=='blind_test','log_policy':'Do not inspect blind private log/result; analyst output is offset-censored.',
      'controller_code_sha256':sha(Path(__file__))}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result))
if __name__=='__main__':main()
