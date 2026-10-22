"""Reject differentiation-by-profile rewriting; retain the frozen labelled extension."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';D=ROOT/'C6'
sys.path[:0]=[str(D),str(H)]
import labelled_bilocal_jet_engine as L
import tensor_euler_yjet_engine as old
import bilocal_covariant_jet_engine as J
from balanced_tensor_transport_engine import balanced_euler_line
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    t=time.process_time();checks=0
    words=[()]+[(i,) for i in range(4)]+list(product(range(4),repeat=2))
    inds=[(a,b,c,d) for a in range(4) for b in range(a,4) for c in range(4) for d in range(c,4)]
    for word in words:
        for ind in inds:
            for order in (0,1):
                assert s.expand(L.realize(L.metric(order,ind,word))-J.yjet('metric',order,ind,word))==0,(word,ind,order)
                checks+=1
    for mu,nu,r in product(range(4),repeat=3):
        A=L.scalar(0,((1,mu),));B=L.scalar(0,((0,r),(1,nu)))
        val=sum(L.pair(A,((0,k),(0,k)),B,()) for k in range(4))
        expect=balanced_euler_line((mu,),tuple(sorted((nu,r))))
        assert s.expand(val-expect)==0,(mu,nu,r,val,expect)
        checks+=1
    # The old table for differentiated tensor lines is NOT in the original labelled prescription.
    ind=(0,1,0,1);A=L.metric(0,ind,(0,));B=L.unit(())
    flat=sum(L.pair(A,((0,k),(0,k)),B,()) for k in range(4))
    naive=sum(old.T.PD(old.profile(0,ind,(0,)),((0,k),(0,k)),old.unit(()),()) for k in range(4))
    assert s.expand(flat-naive)!=0
    r=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-t,
        old_flat=str(naive),label_preserving_flat=str(flat),difference=str(s.expand(flat-naive)),
        old_yjet_table_status='DIFFERENT_EXTENSION_NOT_ADOPTED',old_yjet_audit_scope='algebraic covariance tests do not establish equality of extensions',
        zerojet_tensor_unchanged=True,new_family_claimed=False,full_Q2=False,gate_changed=False)
    put(D/'LABELLED_REGRESSION.json',r);put(D/'LABELLED_REGRESSION_MANIFEST.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'labelled_bilocal_jet_engine.py',D/'tensor_euler_yjet_engine.py',D/'LABELLED_REGRESSION.json']]))
    print(json.dumps(r),flush=True)
if __name__=='__main__':main()
