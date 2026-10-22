"""Covariant quadratic primitive candidates for both measured hc contacts.

Keep all scheme parameters free. Compare ordered gauge jets, not flat
symbol substitution. No subtraction is made in the time-ordered products.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import permutations
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from oneform_second_curvature_engine_v2 import oneform_second,loop_gauge
H=Path(__file__).resolve().parent;D=H/'bilocal_curved_contact_primitive';D.mkdir(exist_ok=True)
source=H/'bilocal_XY_extension_contact/results.json';data=json.loads(source.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[Path(__file__),source,H/'oneform_second_curvature_engine_v2.py',H/'spaceform_covariant_jet_engine.py',H/'bilocal_flat_contact_primitive/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Formal covariant hc operator represented by the measured normal-frame contact; primitive family through O(K)',
    method='Symmetric covariant order5/order3 target on one-form, versus order4/order2 Hessian on gauge tensor',
    convention='Remove common i from exp(i p.x); order5 gives + and order3 gives - at flat order',
    modes=['geodesic','coordinate'],parameters='b,c,t never selected',
    caveat='Coordinate completion is treated as a formal covariant completion of its chart coefficients; this does not prove its naturality under change of base point',
    exclusions=['O(K²)','nonlinear extension','W','all diagrams','Lorentzian boundary values'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],full_Q2=False))
cpu=time.process_time();b,c,t=s.symbols('b c t',real=True)
u0,v0,w0=map(s.Rational,data['coefficients_over_C_E']['geodesic'][0])
flat=[v0-c/2,u0/2-b,b,c,w0/2-b-c/2]
zero=[F(0)]*5;checks=[];output={}
def ck(label,expr):
    val=s.expand(expr);assert val==0,(label,val);checks.append(label)
def operators(p,V):
    jet,gauge,symh=oneform_second(V,p)
    @lru_cache(None)
    def symv(word,r,o):
        words=set(permutations(word))
        return sum((jet(w,r,o) for w in words),F())/len(words)
    def target(co,o):
        out=s.zeros(4)
        for i in range(4):
            for j in range(4):
                value=0
                for ko in range(o+1):
                    u,v,w=co[ko]
                    # Explicit fully symmetric differential words, no assumption
                    # that their curvature parts vanish on parallel wave jets.
                    if ko==0:
                        if i==j:value+=u*sum(symv((r,k,k,l,l),r,o) for r in range(4) for k in range(4) for l in range(4))
                        value+=v*sum(symv((j,k,k,l,l),i,o)+symv((i,k,k,l,l),j,o) for k in range(4) for l in range(4))
                        value+=w*sum(symv((i,j,r,k,k),r,o) for r in range(4) for k in range(4))
                    else:
                        if i==j:value+=u*sum(symv((r,k,k),r,0) for r in range(4) for k in range(4))
                        value+=v*sum(symv((j,k,k),i,0)+symv((i,k,k),j,0) for k in range(4))
                        value+=w*sum(symv((i,j,r),r,0) for r in range(4))
                out[i,j]=s.expand(value)
        return out
    return symh,target
# Identify the third-derivative residual in a predeclared O4 basis; verify
# subsequently on all symbolic momenta and polarizations, not these samples.
sample_cases=[((1,0,0,0),(1,0,0,0)),((1,0,0,0),(0,1,0,0)),((1,2,-1,1),(2,-1,1,2))]
sample_data=[]
for p,V in sample_cases:
    symh,target=operators(p,V)
    existing=s.Matrix(loop_gauge(symh,flat,zero,[F(0)]*2,1))
    sample_data.append((p,V,target,existing))
    print('FIT_INPUT',p,V,'cpu',time.process_time()-cpu,flush=True)
for mode in ('geodesic','coordinate'):
    co=[[s.Rational(v) for v in row] for row in data['coefficients_over_C_E'][mode]]
    rows=[];rhs=[]
    for p,V,target,existing in sample_data:
        diff=target(co,1)-existing;p2=sum(v*v for v in p);pv=sum(pp*vv for pp,vv in zip(p,V))
        for i in range(4):
            for j in range(4):
                rows.append([p2*(p[i]*V[j]+p[j]*V[i]),p[i]*p[j]*pv,int(i==j)*p2*pv])
                rhs.append(diff[i,j])
    fit,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix(rhs));assert len(params)==0,params
    d1=fit[0]-t/2;d3=(fit[1]-t)/2;d2=fit[2]/2-d3
    first=list(map(s.expand,[d1,d2,d3,d3,t]))
    output[mode]=dict(flat=list(map(str,flat)),first=list(map(str,first)),
        fitted_residual_G_qq_metric=list(map(str,fit)))
    print('COEFFICIENTS',mode,output[mode],'cpu',time.process_time()-cpu,flush=True)
# Full symbolic p, four independent polarizations. The set of polarized
# exponentials spans arbitrary symmetric derivative jets at the anchor.
p=s.symbols('p0:4')
for r in range(4):
    V=tuple(int(i==r) for i in range(4));symh,target=operators(p,V)
    for mode in ('geodesic','coordinate'):
        first=[s.sympify(v,locals={'b':b,'c':c,'t':t}) for v in output[mode]['first']]
        co=[[s.Rational(v) for v in row] for row in data['coefficients_over_C_E'][mode]]
        for o in (0,1):
            actual=s.Matrix(loop_gauge(symh,flat,first,[F(0)]*2,o));wanted=target(co,o)
            for i in range(4):
                for j in range(4):ck((mode,r,o,i,j),actual[i,j]-wanted[i,j])
    print('SYMBOLIC_POLARIZATION',r,'checks',len(checks),'cpu',time.process_time()-cpu,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='COVARIANT_HC_PRIMITIVE_FAMILIES_THROUGH_FIRST_K_CHECKED',
    checks=len(checks),cpu_seconds=time.process_time()-cpu,families=output,
    proof_basis='Natural parity-even invariant coefficients, symmetrized words; symbolic momenta and all fiber polarizations span normal covariant jets',
    primitive='B_bct=-C_E/2 integral h.N_bct h; s0 B_bct=-A_hc through O(K) under the declared covariant interpretation',
    formal_adjoint_assumptions='Real parallel coefficients; symmetric fiber transpose; complete symmetrization of derivative words; compact support',
    parameters_chosen=False,prescription_changed=False,full_Q2=False,
    caveat='Formal covariant completion of the chart contact; no proof of coordinate-regulator naturality, full QME or nonlinear/cutoff completion')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
