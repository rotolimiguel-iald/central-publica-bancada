from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,time,json
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha
receipts=[]
cases=[('rite',[])] if '--rite-only' in sys.argv else [('legacy',['--legacy']),('rite',[])]
for label,extra in cases:
    path='/mnt/c/'+str(D/'run_tests.py')[3:].replace('\\','/')
    cmd=['wsl.exe','--','env','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1',
        '/opt/lal_env/bin/python','-B',path]+extra
    start=time.perf_counter();at=datetime.now(timezone.utc).isoformat()
    p=subprocess.run(cmd,capture_output=True,timeout=120)
    stem=label+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    log=D/(stem+'.log');write(log,p.stdout+b'\nSTDERR\n'+p.stderr)
    rec=dict(at=at,command=cmd,returncode=p.returncode,wall_seconds=time.perf_counter()-start,
        log=str(log),log_sha256=sha(log),parsed_summary=None)
    for line in p.stdout.decode('utf-8','replace').splitlines():
        try:
            v=json.loads(line)
            if isinstance(v,dict) and 'tests' in v:rec['parsed_summary']=v
        except ValueError:pass
    save(D/(stem+'.json'),rec);receipts.append(rec);print(json.dumps(rec),flush=True)
    if p.returncode:print(p.stderr.decode('utf-8','replace')[-10000:]);break
sys.exit(0 if len(receipts)==len(cases) and all(r['returncode']==0 for r in receipts) else 1)
