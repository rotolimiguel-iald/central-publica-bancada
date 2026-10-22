"""Exact graded descent for a natural top density, not an anomaly coefficient."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'natural_density_descent';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
src=HERE.parents[1]/'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md'
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    primary_local_source_sha256=sha(src),target='(s+d)[rho product_mu(c^mu+dx^mu)]=0 in4D',
    assumptions='rho even natural density,s rho=c.drho+(div c)rho; s c^mu=c^nu partial_nu c^mu; total grading',
    significance='A_I has bidegree(4,0), not(4,4); descent total degree4; not anomaly ghost1/form4'))
start,cpu=perf_counter(),process_time();rho=s.Symbol('rho');dr=s.symbols('drho0:4')
# Odd c0..3, dx0..3 (4..7), derivative ghosts j(mu,nu)=8+4mu+nu.
def atom(i):return {(i,):s.S.One}
def clean(a):return {k:s.expand(v) for k,v in a.items() if s.expand(v)!=0}
def plus(*items):
    z={}
    for x in items:
        for k,v in x.items():z[k]=z.get(k,0)+v
    return clean(z)
def scale(a,n):return clean({k:n*v for k,v in a.items()})
def mul(a,b):
    z={}
    for ka,va in a.items():
        for kb,vb in b.items():
            seq=ka+kb
            if len(set(seq))<len(seq):continue
            sign=(-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))
            key=tuple(sorted(seq));z[key]=z.get(key,0)+sign*va*vb
    return clean(z)
def jet(mu,nu):return atom(8+4*mu+nu)
def deriv(a,kind,include_div=True):
    assert kind in ('s','d');out={};base=0 if kind=='s' else 4
    drho=plus(*(scale(atom(base+i),dr[i]) for i in range(4)))
    if kind=='s' and include_div:drho=plus(drho,*(scale(jet(i,i),rho) for i in range(4)))
    for seq,coef in a.items():
        # Inputs contain rho only; derivative jets appear only in outputs.
        assert not any(s.diff(coef,x) for x in dr)
        out=plus(out,mul(scale(drho,s.diff(coef,rho)),{seq:s.S.One}))
        for n,t in enumerate(seq):
            if t>=8:raise AssertionError('Derivative of ghost jets not required in this checker')
            if t<4:
                val=plus(*(mul(atom(base+j),jet(t,j)) for j in range(4)))
                out=plus(out,scale(mul(mul({seq[:n]:coef},val),{seq[n+1:]:s.S.One}),(-1)**n))
    return out
omega={():rho}
for i in range(4):omega=mul(omega,plus(atom(i),atom(i+4)))
pieces=[{k:v for k,v in omega.items() if sum(4<=x<8 for x in k)==q} for q in range(5)]
checks=[];neg=[]
for q in range(5):
    assert not plus(deriv(pieces[q],'s'),deriv(pieces[q-1],'d') if q else {})
    checks.append('descent_q'+str(q))
assert not deriv(pieces[4],'d');checks.append('top_horizontal_derivative')
assert not plus(deriv(omega,'s'),deriv(omega,'d'));checks.append('total_cycle')
assert pieces[0]=={(0,1,2,3):rho};checks.append('bottom_ghost4_form0')
assert pieces[4]=={(4,5,6,7):rho};checks.append('top_ghost0_form4')
for q,piece in enumerate(pieces):
    assert all(sum(x<4 for x in seq)==4-q for seq in piece)
checks.append('all_total_degrees_four')
assert plus(deriv(omega,'s',False),deriv(omega,'d'));neg.append('omit_density_divergence')
wrong={():rho}
for i in range(4):wrong=mul(wrong,plus(atom(i),scale(atom(i+4),-1)))
assert plus(deriv(wrong,'s'),deriv(wrong,'d'));neg.append('wrong_horizontal_shift_sign')
# Correct incoming page degrees at the anomaly position.
incoming=[]
for page in range(1,5):
    source=(page,4-page);image=(source[0]+1-page,source[1]+page)
    assert image==(1,4)
    wrong_source=(1+page,4-page);bad=(wrong_source[0]+1-page,wrong_source[1]+page)
    assert bad==(2,4)
    incoming.append(dict(page=page,source=source,target=image,wrong_source=wrong_source,wrong_target=bad))
checks.append('incoming_sources_total_degree4')
assert (4+1-4,0+4)==(1,4);checks.append('potential_d4_from_actual_bottom_degree')
out=dict(statute='DERIVED_NATURAL_DENSITY_EXPLICIT_DESCENT_TOTAL_FOUR',checks=checks,negative_controls=neg,
    components=[dict(form=q,ghost=4-q,terms=[dict(odd=list(k),coefficient=str(v)) for k,v in part.items()]) for q,part in enumerate(pieces)],
    incoming=incoming,identity='s omega_q+d omega_(q-1)=0;omega=rho product(c+dx)',
    spectral_scope='An explicit total lift kills outgoing differentials of this class, including its potentially allowed d4; projection to form0 detects non-exactness if bottom is not s-exact',
    no_anomaly_coefficient=True,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',out);print(json.dumps({k:v for k,v in out.items() if k!='components'},ensure_ascii=False))
