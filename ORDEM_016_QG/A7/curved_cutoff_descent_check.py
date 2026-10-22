"""Actual D_t cutoff currents and candidate nonlinear descent, through K^2.

Does not identify this candidate with the full quantum anomaly.
"""
from pathlib import Path
from datetime import datetime, timezone
from time import process_time
import hashlib, json
from curved_cutoff_descent_engine import *

H = Path(__file__).resolve().parent
D = H/'curved_cutoff_descent'
D.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p, v):
    assert not p.exists(), str(p)
    b=json.dumps(v,indent=2).encode(); tmp=p.with_suffix('.tmp')
    tmp.write_bytes(b); assert tmp.read_bytes()==b; tmp.replace(p)
fresh(D/'PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(H/'curved_cutoff_descent_engine.py'),
    target='D_t cutoff Leibniz currents; nonlinear variation s1B_chi; polarized Lie closure of candidate',
    actual_quantum_h2c_identified=False, prescription_changed=False,
    negative_controls=['omit cutoff derivative terms','omit nonlinear variation','wrong bracket sign']))
cpu=process_time(); checks=0; negative={}; samples=[]
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
def constant(c): return {ZERO:F(c)} if c else {}
chi_poly=plus(constant(2),mono((0,),3),mono((2,),-2),mono((0,1),2),mono((1,1),-3),mono((2,2,3),1))
chi=polynomial_jet(lambda ix,o: chi_poly if not o else {},0)
metric=polynomial_jet(spaceform_metric_initial,2)
def hi(ix,o):
    if o:return {}
    a,b=sorted(ix)
    return plus(constant((a+1)*(b+1)),mono((a,),b-2),mono((b,),a+1),
                mono((a,b),F(1,2)),mono(((a+1)%4,b,b),F(-1,3)))
h=polynomial_jet(hi,2)
u_poly=[plus(constant(i-1),mono((i,),i+1),mono((i,(i+1)%4),F(1,2))) for i in range(4)]
v_poly=[plus(constant(2-i),mono(((i+2)%4,),-2),mono((i,i),1)) for i in range(4)]
u=polynomial_jet(lower_vector_initial(u_poly),1)
v=polynomial_jet(lower_vector_initial(v_poly),1)

# Calibrate the existing normal metric/connection in this real-jet engine.
for order in range(3):
    for a,b in product(range(4),repeat=2):
        for word in [(i,) for i in range(4)]+[(0,1),(2,3)]:
            check(metric(word,(a,b),order))
print(json.dumps(dict(stage='metric_parallel',checks=checks,cpu=process_time()-cpu)),flush=True)

# D(chi h) independently starts with multiplied coordinate polynomials.
product_direct=polynomial_jet(lambda ix,o: times(chi_poly,hi(ix,o)),2)
product_rule=scalar_product(chi,h)
for order in range(3):
    for a,b in product(range(4),repeat=2):
        for word in [(),(0,),(2,),(0,1),(1,2),(3,3),(0,1,2)]:
            check(product_direct(word,(a,b),order),product_rule(word,(a,b),order))

for t in [0,1,-2]:
    Dh=ward_operator(h,t); Dch=ward_operator(product_direct,t)
    chDh=scalar_product(chi,Dh); M=localized_operator(chi,h,t)
    # C^{ij}(chi_;ij h+2chi_;i nabla_j h), directly at the tensor slots.
    def excess(word,ix,o):
        if len(word)!=2:return F()
        i,j=word
        return sum((chi((i,j),(),k)*h((),ix,o-k)
                    +chi((i,),(),k)*h((j,),ix,o-k)
                    +chi((j,),(),k)*h((i,),ix,o-k) for k in range(o+1)),F())
    expected=ward_operator(excess,t)
    for order in range(3):
        for a,b in product(range(4),repeat=2):
            comm=Dch((),(a,b),order)-chDh((),(a,b),order)
            check(comm,expected((),(a,b),order))
            check(M((),(a,b),order),chDh((),(a,b),order)+comm/2)
            if comm and 'omit_cutoff' not in negative:
                negative['omit_cutoff']=dict(t=t,order=order,ab=[a,b],missing=str(comm/2))
    # Exact Noether current for A0+s1B; background is inert, chi is inert.
    Gu=lie_tensor(u,metric); Luh=lie_tensor(u,h)
    for order in range(3):
        variation=sum(((Gu((),(a,b),k)+Luh((),(a,b),k))*M((),(a,b),order-k)
                       for k in range(order+1) for a,b in product(range(4),repeat=2)),F())
        current=F(); divergence=F(); nonlinear=F()
        for k in range(order+1):
            for a,b in product(range(4),repeat=2):
                nonlinear+=Luh((),(a,b),k)*M((),(a,b),order-k)
        # c^r J_r plus nabla_a[2c^r(g_rb+h_rb)F^{ab}].
        full=lambda w,ix,o: metric(w,ix,o)+h(w,ix,o)
        for r in range(4):
            for k in range(order+1):
                Jr=sum((M((),(a,b),l)*h((r,),(a,b),order-k-l)
                        -2*pair_product(full,(r,b),M,(a,b),(a,),order-k)
                        if l==0 else M((),(a,b),l)*h((r,),(a,b),order-k-l)
                        for l in range(order-k+1) for a,b in product(range(4),repeat=2)),F())
                current+=u((),(r,),k)*Jr
            for a,b in product(range(4),repeat=2):
                for k in range(order+1):
                    for l in range(order-k+1):
                        m=order-k-l
                        divergence+=2*(u((a,),(r,),k)*full((),(r,b),l)*M((),(a,b),m)
                            +u((),(r,),k)*full((a,),(r,b),l)*M((),(a,b),m)
                            +u((),(r,),k)*full((),(r,b),l)*M((a,),(a,b),m))
        check(variation,current+divergence)
        if nonlinear and 'omit_s1B' not in negative:
            negative['omit_s1B']=dict(t=t,order=order,missing=str(nonlinear))
        samples.append(dict(t=t,order=order,variation=str(variation),current=str(current),divergence=str(divergence),s1B=str(nonlinear)))
    print(json.dumps(dict(stage='cutoff_noether',t=t,checks=checks,cpu=process_time()-cpu)),flush=True)

# Polarized closure includes curvature at the actual tensor jets, not a flat symbol.
bracket=vector_bracket(u,v)
for label,T in [('background',metric),('perturbation',h)]:
    LuLv=lie_tensor(u,lie_tensor(v,T)); LvLu=lie_tensor(v,lie_tensor(u,T)); Lbr=lie_tensor(bracket,T)
    for word in [(),(0,),(2,),(0,1),(1,2),(3,3)]:
        for order in range(3):
            for a,b in product(range(4),repeat=2):
                x=LuLv(word,(a,b),order)-LvLu(word,(a,b),order)
                y=Lbr(word,(a,b),order)
                check(x,y)
                if y and 'wrong_bracket' not in negative:
                    negative['wrong_bracket']=dict(tensor=label,word=list(word),order=order,ab=[a,b],wrong_residual=str(x+y))
    print(json.dumps(dict(stage='lie_closure',tensor=label,checks=checks,cpu=process_time()-cpu)),flush=True)
assert len(negative)==3
fresh(D/'results.json',dict(statute='DERIVED_CUTOFF_AND_NONLINEAR_COMPLETION_OF_CANDIDATE_ONLY',checks=checks,
    negative_controls=negative,samples=samples,cpu_seconds=process_time()-cpu,
    cutoff_operator='M_chi=(chi D_t+D_t chi)/2',
    nonlinear='s1B_chi=<Lie_c h,M_chi h>',
    current='J_r=F^ab nabla_r h_ab-2 nabla_a[(gbar_rb+h_rb)F^ab], F=M_chi h',
    candidate_WZ='s(sB_chi)=0 with sc=c.grad c, sh=Lie_c(gbar+h); follows closure and selfadjoint Hessian',
    actual_h2c_quantum_identified=False,finite_temporal_part_identified=False,full_Q2=False,
    representative_selected=False,prescription_changed=False))
files=[Path(__file__),H/'curved_cutoff_descent_engine.py',H/'spaceform_covariant_jet_engine.py',
       H/'local_quadratic_ward_primitive/results.json',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,negative_controls=len(negative),cpu=process_time()-cpu)))
