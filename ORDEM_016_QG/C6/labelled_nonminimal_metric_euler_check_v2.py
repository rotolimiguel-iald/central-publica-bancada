"""Check full hh Schur block without dropping mixed Ward lines before extension."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import sys,time,json
import sympy as s
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'C6';H=ROOT/'A7'
sys.path[:0]=[str(C),str(H)]
import labelled_nonminimal_metric_euler as N
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
from deliver_nonminimal_wick_and_mimo_audit import sha,put


def main():
    out=C/'nonminimal_metric_euler_check_v2';out.mkdir(exist_ok=False)
    start=time.process_time();checks=0
    def eq(a,b,label):
        nonlocal checks
        num,den=s.fraction(s.cancel(s.expand(a-b)))
        num=s.expand(num.subs(T.B.w,sum((x-y)**2 for x,y in zip(T.x,T.y))))
        assert num==0,(label,num);checks+=1
    def same(a,b,label):
        nonlocal checks
        residual=L.clean(tuple(a)+tuple((-c,p,w) for c,p,w in b))
        assert not residual,(label,residual);checks+=1
    labels=[(a,b) for a in range(4) for b in range(a,4)]
    # Flat Ward identity must vanish as a labelled expression, before any realization.
    nonzero_labelled_mixed=0
    for nu,(c,d) in product(range(4),labels):
        for xw in [()]+[(i,) for i in range(4)]:
            same(N.mixed_ward(0,nu,c,d,xw),(),('flat mixed Ward',nu,c,d,xw))
        # First curvature ordinary Ward identity vanishes away from diagonal.
        # This is not permission to remove its labelled contact contribution.
        eq(L.realize(N.mixed_ward(1,nu,c,d)),0,('first mixed offdiagonal',nu,c,d))
        nonzero_labelled_mixed+=bool(N.mixed_ward(1,nu,c,d))
    print(json.dumps(dict(stage='mixedWard',checks=checks,nonzero_labelled_mixed=nonzero_labelled_mixed,cpu_seconds=time.process_time()-start)),flush=True)
    table={};mixed_changes=[]
    # First side labelled block; metric (01,01) is the scalar spectator f/2 at leading order.
    spectator=(0,1,0,1)
    for (a,b),(c,d) in product(labels,repeat=2):
        ind=(a,b,c,d)
        idcoef=(T.delta(a,c)*T.delta(b,d)+T.delta(a,d)*T.delta(b,c))/2
        lap=[]
        for i in range(4):lap.append((idcoef,T.F,(i,i)))
        same(N.euler(0,ind),L.clean(lap),('flat full Euler',ind))
        eq(L.realize(N.euler(1,ind)),0,('full Euler offdiagonal K',ind))
        value=N.pair_contact(ind,'metric',spectator)
        correction=-L.pair(N.cstar_mixed(1,ind),(),M.cov('metric',0,spectator),())
        assert not value.free_symbols
        checks+=1
        table[str(ind)]=dict(full=str(value),mixed_correction=str(correction))
        if correction!=0:mixed_changes.append(dict(ind=ind,value=str(correction)))
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        nonzero_labelled_mixed=nonzero_labelled_mixed,nonzero_mixed_contacts=len(mixed_changes),mixed_witnesses=mixed_changes[:10],
        scope='Densitized full nonminimal PH_hh zerojet, first curvature, metric spectator01,01; no vertices or temporal weights',
        full_Q2=False,gate_changed=False)
    put(out/'results.json',result);put(out/'TABLE.json',table)
    paths=[Path(__file__),C/'labelled_nonminimal_metric_euler.py',C/'labelled_covariant_xy.py',C/'labelled_bilocal_jet_engine.py',H/'nonminimal_wick_heat_ward_check.py',out/'results.json',out/'TABLE.json']
    put(out/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
