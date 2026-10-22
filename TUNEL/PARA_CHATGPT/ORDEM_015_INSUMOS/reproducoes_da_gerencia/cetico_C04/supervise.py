"""Supervisor: runs child.py over a list of items; on crash (rc<0 or !=0) records the crashing label (last precall without return) and restarts from next item."""
import sys,json,subprocess,os,time
items=json.load(open(sys.argv[1])); out=sys.argv[2]; log=out+".jsonl"
if os.path.exists(log): os.remove(log)
i=0; crashes=[]; t0=time.time(); children=0
while i<len(items):
    jobf=out+".job.json"; json.dump({"items":items[i:]},open(jobf,"w"))
    children+=1
    rc=subprocess.run([sys.executable,"-B","child.py",jobf,log],stdout=open(out+".child%d.log"%children,"w"),stderr=subprocess.STDOUT).returncode
    lines=[json.loads(l) for l in open(log)]
    done=sum(1 for l in lines if "return" in l)
    if rc!=0:
        pre=[l for l in lines if "precall" in l]; last=pre[-1]["precall"] if pre else None
        rets={l["return"] for l in lines if "return" in l}
        crashed=last if last not in rets else None
        crashes.append({"rc":rc,"label":crashed,"after_returns":done})
        labels=[it["label"] for it in items]
        i=(labels.index(crashed)+1) if crashed is not None else done
    else: break
res={"n_items":len(items),"returns":done,"crashes":crashes,"children":children,"wall_s":time.time()-t0}
lines=[json.loads(l) for l in open(log)]
from collections import Counter
res["status_counts"]=dict(Counter(l["status"].split(":")[0] for l in lines if "return" in l))
fin=[l["wall_s"] for l in lines if "return" in l and l["status"]=="FINITE_WAVEFORM"]
res["finite_wall_s_mean"]=sum(fin)/len(fin) if fin else None; res["finite_n"]=len(fin)
json.dump(res,open(out+".RESULT.json","w"),indent=1); print(json.dumps(res))
