"""One bounded supervisor, sequential contained children, no strain or PE."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,signal,subprocess,sys,time,resource
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent


def save(path,obj):
    with path.open('xb') as handle:handle.write((json.dumps(obj,indent=2,allow_nan=False)+'\n').encode())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true');parser.add_argument('--cases',nargs='*');args=parser.parse_args()
    plan=json.loads((HERE/'PLAN_INPUTS.json').read_bytes());deadline=datetime.fromisoformat(plan['deadline_utc']).timestamp()
    labels=['PRIOR_REPLAY'] if args.replay else args.cases
    folder=HERE/'cases';folder.mkdir(exist_ok=True)
    if not labels:raise ValueError('Explicit cases required')
    if len(list(folder.glob('*.CONTROLLER.json')))+len(labels)>plan['max_sequential_waveform_children']:raise ValueError('Child count cap')
    for label in labels:
        if deadline-time.time()<10:raise TimeoutError('Diagnostic wall exhausted')
        target=folder/(label+'.CONTROLLER.json')
        if target.exists():raise FileExistsError('No repeated case')
        started=time.perf_counter();usage=resource.getrusage(resource.RUSAGE_CHILDREN)
        cmd=[sys.executable,'-B',str(HERE/'diagnostic_child.py')]+(['--replay'] if args.replay else ['--case',label])
        with (folder/(label+'.log')).open('xb') as log:
            child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env=os.environ.copy())
            timeout=min(plan['per_child_wall_cap_seconds'],deadline-time.time()-5)
            timed_out=False
            try:child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out=True;os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=3)
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        result={'label':label,'returncode':child.returncode,'timed_out':timed_out,'wall_seconds':time.perf_counter()-started,
                'child_cpu_seconds':after.ru_utime+after.ru_stime-usage.ru_utime-usage.ru_stime,'finished_utc':datetime.now(timezone.utc).isoformat(),
                'log_sha256':hashlib.sha256((folder/(label+'.log')).read_bytes()).hexdigest(),'core_dumps_disabled_in_child':True,
                'source_waveform_calls_only_no_strain_PE':True}
        save(target,result);print(json.dumps(result),flush=True)


if __name__=='__main__':main()
