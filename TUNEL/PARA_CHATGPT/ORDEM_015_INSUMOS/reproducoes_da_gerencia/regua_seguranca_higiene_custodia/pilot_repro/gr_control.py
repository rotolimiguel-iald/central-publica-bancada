import json,subprocess,sys,os,glob
here=os.path.dirname(os.path.abspath(__file__))
rows=[]
for p in glob.glob(os.path.join(here,"sweep_fmax1024_*.json")): rows+=json.load(open(p))["rows"]
ab=[r for r in rows if r["rc"]==-6][:24]
out=[]
for r in ab:
    res={}
    for mode in ("zero","deformed"):
        pr=subprocess.run([sys.executable,"-B",os.path.join(here,"worker_gr.py"),json.dumps(r["params"]),"1024",mode],capture_output=True,text=True,timeout=300,env=dict(os.environ,OMP_NUM_THREADS="1"))
        res[mode]=pr.returncode
    out.append(dict(seed=r["seed"],rc_zero_deformation=res["zero"],rc_deformed_again=res["deformed"]))
    print(out[-1],flush=True)
from collections import Counter
print("SUMMARY zero-deformation rc:",Counter(o["rc_zero_deformation"] for o in out),"| deformed rerun rc:",Counter(o["rc_deformed_again"] for o in out))
json.dump(out,open(os.path.join(here,"gr_control.json"),"w"),indent=1)
