"""Check the exact numerator degree requested by the independent review.

No loop extraction is rerun: inspect the five numerator families on the full
multilinear polarization basis, whose coverage was already established.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import hashlib,json
from marked_polynomial_engine import (R,ONE,ZERO,axes,P,Q,marked_numerators,triangle_numerator)
H=Path(__file__).resolve().parent;D=H/'marked_actual_degree';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'marked_polynomial_engine.py'),
    objective='Inspect actual q-degree <=5 in all five numerator families on 160 basis polarizations',
    no_UV_integral_recomputed=True,full_Q2=False))
cpu,wall=process_time(),perf_counter();families=['left_ghost','left_metric','right_ghost','right_metric','triangle']
maximum={key:-1 for key in families};counts={key:0 for key in families};witnesses={}
def degree(poly):return max((sum(e[:4]) for e in poly),default=-1)
checks=0
for ti,(a,b) in enumerate(( (a,b) for a in range(4) for b in range(a,4))):
    T=[[ONE if (i,j) in [(a,b),(b,a)] else ZERO for j in range(4)] for i in range(4)]
    for vi,v in enumerate(axes):
        for wi,w in enumerate(axes):
            lg,lm=marked_numerators(T,Q,w,P,v)
            rg,rm=marked_numerators(T,P,v,Q,w)
            nums=[lg,lm,rg,rm,triangle_numerator(T,P,v,Q,w)]
            for key,num in zip(families,nums):
                d=degree(num);assert d<=5,(ti,vi,wi,key,d)
                if d>maximum[key]:maximum[key]=d;witnesses[key]=[ti,vi,wi]
                if num:counts[key]+=1
                checks+=1
# The checked criterion explicitly refuses degree six, unlike a looser radial
# extraction bound that might still evaluate it without the simplex audit.
bad=R.from_dict({(6,0,0,0,0,0,0):1});assert degree(bad)==6
fresh(D/'results.json',dict(statute='REAL_EXACT_ACTUAL_NUMERATOR_DEGREE_AUDIT',checks=checks,
    maximum_q_degree_by_family=maximum,nonzero_counts=counts,witnesses=witnesses,
    degree_six_mutation_rejected=True,no_UV_integral_recomputed=True,full_Q2=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,maximum=maximum,cpu_seconds=process_time()-cpu)))
