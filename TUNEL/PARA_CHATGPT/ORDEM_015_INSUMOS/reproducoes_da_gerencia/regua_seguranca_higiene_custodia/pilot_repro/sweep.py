import subprocess, sys, json, os, time, concurrent.futures as cf
here=os.path.dirname(os.path.abspath(__file__)); py=sys.executable
N=int(sys.argv[1]); fmax=sys.argv[2]; workers=int(sys.argv[3]); base=int(sys.argv[4])
def run(seed):
    t=time.perf_counter()
    try:
        pr=subprocess.run([py,"-B",os.path.join(here,"worker.py"),str(seed),fmax],capture_output=True,text=True,timeout=600,env=dict(os.environ,OMP_NUM_THREADS="1",PYTHONDONTWRITEBYTECODE="1"))
        rc=pr.returncode; out=pr.stdout; err=pr.stderr
    except subprocess.TimeoutExpired as e:
        rc="TIMEOUT"; out=(e.stdout or ""); err=(e.stderr or "")
    params=next((l[7:] for l in out.splitlines() if l.startswith("PARAMS")),None)
    res=next((l[7:] for l in out.splitlines() if l.startswith("RESULT")),None)
    xlal=[l for l in err.splitlines() if "XLAL Error" in l][:3]
    return dict(seed=seed,rc=rc,wall=time.perf_counter()-t,params=json.loads(params) if params else None,result=json.loads(res) if res else None,xlal_first=xlal, err_tail=err.strip().splitlines()[-3:] if err.strip() else [])
rows=[]
with cf.ThreadPoolExecutor(workers) as ex:
    for r in ex.map(run,range(base,base+N)): rows.append(r); print(r["seed"],r["rc"],round(r["wall"],1),(r["result"] or {}).get("ok"),(r["xlal_first"][:1]),flush=True)
from collections import Counter
summ=dict(N=N,fmax=fmax,rc_counter=dict(Counter(str(r["rc"]) for r in rows)),ok_counter=dict(Counter(str((r["result"] or {}).get("ok")) for r in rows)),
          segv=[r["seed"] for r in rows if r["rc"]==-11],abort=[r["seed"] for r in rows if r["rc"]==-6],
          xlal_kinds=dict(Counter(r["xlal_first"][0].split(":")[-1].strip()[:80] for r in rows if r["xlal_first"])))
json.dump(dict(summary=summ,rows=rows),open(os.path.join(here,f"sweep_fmax{fmax}_base{base}_N{N}.json"),"w"),indent=1)
print("SUMMARY",json.dumps(summ))
