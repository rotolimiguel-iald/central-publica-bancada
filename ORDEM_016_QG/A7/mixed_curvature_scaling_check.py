"""Check that explicit first-curvature single-line jets are subcritical.

Only singular/smooth mixed contact before external Ward derivatives.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
from logarithmic_contact_engine import residue
H=Path(__file__).resolve().parent;D=H/'mixed_curvature_scaling';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(raw);assert q.read_bytes()==raw;q.replace(p)
inputs=[Path(__file__),H/'bilocal_first_curvature_engine.py',H/'logarithmic_contact_engine.py',
 H/'smooth_firstjet_source/results.json',H/'smooth_general_fiber/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Explicit K1 Hadamard single-line jets with at most one derivative per endpoint; test subcritical scaling before smooth multiplication',
 normal_chart='Y anchored only after XY differentiation',
 exclusions=['singular-singular products','external Ward derivatives after extension','full Q2','Lorentzian normalization'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=0;maxsd=-999;terms=0;components=0
@lru_cache(None)
def jet(f,i,j):
    if j>=0:f=B.derivative(f,'Y',j)
    if i>=0:f=B.derivative(f,'X',i)
    return B.anchored(f)
def inspect(f,label,limit):
    global checks,maxsd,terms
    for term in s.Add.make_args(s.expand(f)):
        if not term:continue
        powers=term.as_powers_dict();xp=tuple(int(powers.get(t,0)) for t in B.x)
        n=-int(powers.get(B.w,0));ell=int(powers.get(B.L,0))
        sd=2*n-sum(xp)
        assert sd<=limit,(label,term,sd,limit)
        assert all(q>=0 for q in xp) and ell in (0,1)
        checks+=1;terms+=1;maxsd=max(maxsd,sd)
        # Analytic-residue polynomial vanishes below the critical degree;
        # a log differentiates a regular analytic family, not a missing pole.
        assert residue(n,xp,(1,1,1,1))==0,(label,term)
        checks+=1
labels=[(a,b) for a in range(4) for b in range(a,4)]
for kind in ['ghost','metric']:
    fibers=[(a,b) for a in range(4) for b in range(4)] if kind=='ghost' else [(a,b,c,d) for a,b in labels for c,d in labels]
    for fiber in fibers:
        f=(B.ghost if kind=='ghost' else B.metric)(1,*fiber)
        for i in range(-1,4):
            for j in range(-1,4):
                inspect(jet(f,i,j),(kind,fiber,i,j),int(i>=0)+int(j>=0))
                components+=1
    print(kind,'components',components,'cpu',time.process_time()-cpu,flush=True)

# Density/normal-frame correction O(K*r²) times the critical leading jet
# is also subcritical. Every quadratic monomial is tested, all16 XY jets.
for a in range(4):
 for b in range(a,4):
  for i in range(4):
   for j in range(4):
    inspect(B.x[a]*B.x[b]*jet(1/B.w,i,j),('quadratic_multiplier',a,b,i,j),2)

# Counter: external differentiation can raise a previously integrable
# expression to a contact. Do not extend this result beyond the derivative cap.
from logarithmic_contact_engine import contact
low=contact(0,1,(0,0))
high=contact(0,1,(0,0,0,0))
assert low==0 and high!=0,(low,high)
checks+=2
result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='K1_MIXED_SINGLE_LINE_JETS_SUBCRITICAL_BEFORE_WARD',
 checks=checks,cpu_seconds=time.process_time()-cpu,components=components,
 monomials_checked=terms,max_scaling_degree=maxsd,
 negative_control=dict(second_derivative_log=str(low),fourth_derivative_log=str(high)),
 conclusion='Explicit K1 single-line corrections add no critical extension contact under the specified derivative cap; curvature still enters covariant N_W, E, G and Ward derivatives',
 full_Q2=False,all_curvature_orders_computed=False,
 restriction='Not a claim that logs never generate contact, nor that the full mixed Ward anomaly is curvature-independent')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
