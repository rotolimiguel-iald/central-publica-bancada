"""Mixed derivative regression, including the actually used Euler-labelled contacts."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7';D=C/'labelled_covariant_xy'
sys.path[:0]=[str(C),str(H)]
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import bilocal_covariant_jet_engine as J
import tensor_euler_yjet_engine_v2 as T
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time();checks=0
    def eq(a,b,label):
        nonlocal checks
        assert s.cancel(a-b)==0,(label,a,b);checks+=1
    metric=[(a,b,c,d) for a in range(4) for b in range(a,4) for c in range(4) for d in range(c,4)]
    ghost=list(product(range(4),repeat=2));ys=[()]+[(i,) for i in range(4)]
    for kind,inds in [('metric',metric),('ghost',ghost)]:
        for ind in inds:
            for o,yw,i in product(range(2),ys,range(4)):
                eq(L.realize(M.cov(kind,o,ind,(i,),yw)),J.xyjet(kind,o,ind,yw,i),(kind,o,ind,yw,i))
        print(json.dumps(dict(stage='offdiagonal',kind=kind,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    # Existing zerojets are not recomputed as new evidence; they are exact regression targets.
    tab=json.loads((H/'bilocal_vector_euler_zerojet/TABLE.json').read_bytes())
    for a,b,c,d in product(range(4),repeat=4):
        val=M.pair_contact('ghost',(a,b),'ghost',(c,d))
        eq(val,s.sympify(tab[str((a,b,c,d))][0]),('vectorEuler',a,b,c,d))
    unit=(0,1,0,1)
    for ind in metric:
        for yw in ys:
            new=M.pair_contact('metric',ind,'metric',unit,yword1=yw)
            old=T.contact(ind,unit,yw,())
            eq(new,old,('metricEuler',ind,yw))
    # Mixed partial endpoints commute after their own index connections are included.
    # Do not infer commuting derivative slots on the same endpoint.
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        scope='Metric covariant and ghost X-contravariant/Y-covariant profiles, one derivative at X and up to one at Y; Euler X carries two more derivatives',
        old_zerojets_preserved=True,prescription_changed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    paths=[Path(__file__),C/'labelled_covariant_xy.py',C/'labelled_bilocal_jet_engine.py',H/'bilocal_covariant_jet_engine.py',H/'bilocal_vector_euler_zerojet/TABLE.json',C/'tensor_euler_yjet_engine_v2.py',D/'results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
