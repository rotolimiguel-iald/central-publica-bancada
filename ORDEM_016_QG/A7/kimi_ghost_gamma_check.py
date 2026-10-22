"""Locate the exact mixed-curvature error in tr(B-Boxh)^2/8."""
from pathlib import Path
from datetime import datetime,timezone
from collections import defaultdict
from functools import lru_cache
import hashlib,json,time,uuid
from ghost_covariant_word_engine import *
from spaceform_covariant_jet_engine import second_curvature_constant
H=Path(__file__).resolve().parent;OUT=H/'kimi_ghost_gamma';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=OUT/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Direct gamma versus corrected ordered invariant representative',
    correction_inferred_before_run=True,script_sha256=sha(Path(__file__)),
    source_sha256=sha(H/'kimi_ghost_reduction_audit/KIMI_RESPONSE.md')))
cpu=time.process_time()
def coll():
    result=defaultdict(Q)
    def q(l,r,c,k=0):
        for (u,a,b),v in l.items():
            for (w,d,e),z in r.items():
                fac=Q(c)*v*z
                result[(k,a,b,d,e,tuple(reversed(u))+w)]+=(-1)**len(u)*fac
                result[(k,d,e,a,b,tuple(reversed(w))+u)]+=(-1)**len(w)*fac
    return result,q
direct,q=coll()
for a in range(4):
    for b in range(4):q(D(a,b),D(b,a),Q(1,8))
def reduced(corrected):
    op,q=coll();tau=trh();bt=add(*(box(a,a) for a in range(4)))
    u=[divergence(a) for a in range(4)]
    psi=add(*(derivative(u[a],a) for a in range(4)))
    q(psi,psi,Q(1,8));q(bt,bt,Q(1,32))
    for a in range(4):
        lapu=add(*(derivative(derivative(u[a],i),i) for i in range(4)))
        q(u[a],lapu,Q(1,4));q(u[a],u[a],Q(7,8),1)
        for b in range(4):q(box(a,b),box(a,b),Q(1,8))
    q(psi,tau,Q(9 if corrected else 5,8),1)
    q(tau,bt,Q(-5 if corrected else -1,32),1)
    return op
right=reduced(True);wrong=reduced(False)
@lru_cache(None)
def j2(A):return second_curvature_constant([list(r) for r in A])
def ev(op,T,A,o):
    if o<2:return evaluate(op,T,A,(1,0,0,0),o)
    jj=j2(tuple(tuple(r) for r in A))
    return sum(c*T[a][b]*jj(w,u,v,2-k) for (k,a,b,u,v,w),c in op.items() if c and T[a][b])
checks=[];negative=[];labels=[(a,b) for a in range(4) for b in range(a,4)]
for i,l in enumerate(labels):
    for r in labels[i:]:
        T,A=matrix_unit(*l),matrix_unit(*r)
        for o in range(3):
            v=ev(direct,T,A,o)-ev(right,T,A,o)
            assert v==0,(l,r,o,v)
            checks.append((l,r,o))
            old=ev(direct,T,A,o)-ev(wrong,T,A,o)
            if old:negative.append(dict(left=l,right=r,order=o,residual=str(old)))
result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='MIXED_CURVATURE_GAMMA_CORRECTION_VERIFIED',checks=len(checks),
    negative_controls=negative,cpu_seconds=time.process_time()-cpu,
    corrected='tr(B-Boxh)^2/8 = [Psi²+2 LBoxL+(Box tau)^2/4+(Boxh)^2+K(7L²+9Psi tau-5tau Box tau/4)]/8 modulo divergences',
    model_values_replaced=['5Psi tau -> 9Psi tau','-tau Box tau/4 -> -5tau Box tau/4'],
    correction_to_model='K(Psi tau/2-tau Box tau/8)',
    conformal_and_TT_blind_to_correction=True,full_Q2=False)
put('results.json',result)
sources=[Path(__file__),H/'ghost_covariant_word_engine.py',H/'spaceform_covariant_jet_engine.py',OUT/'PRE_REGISTER.json',OUT/'results.json']
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources]))
print(json.dumps({k:v for k,v in result.items() if k!='negative_controls'}));print('NEGATIVE_CONTROLS',len(negative))
