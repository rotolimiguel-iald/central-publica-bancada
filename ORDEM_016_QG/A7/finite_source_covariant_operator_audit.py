"""Independent angular reconstruction and real-jet Einstein image of source contact."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product,permutations
import ast,hashlib,json,time,uuid
import sympy as s
import curved_source_jet_engine as e
from curved_cutoff_descent_engine import polynomial_jet,lower_vector_initial,mono,plus,ZERO,F
from oneform_second_curvature_engine_v2 import einstein_gauge
H=Path(__file__).resolve().parent;D=H/'finite_source_covariant_operator_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    data=json.dumps(v,ensure_ascii=False,indent=2).encode();tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(p)
source=H/'finite_source_covariant_operator_check_v3.py'
prior=H/'finite_source_covariant_operator_v3/results.json'
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(source),prior_sha256=sha(prior),
    method='No harmonic inversion: explicit S3 projections of raw A and B; all10 symmetric fibers with symbolic p,v; real covariant Einstein image',
    exclusions=['smooth W','causal Lorentz continuation','full Ward coefficient']))
start=time.process_time();checks=[]
def ck(name,value):assert s.expand(value)==0,(name,value);checks.append(name)
# Reuse only the already independently checked ordered connection-jet identity.
old=ast.parse((H/'covariant_source_operator_check.py').read_text('utf-8-sig'))
new=ast.parse(source.read_text('utf-8-sig'))
for name in ('gamma','d3'):
    one=next(n for n in old.body if isinstance(n,ast.FunctionDef) and n.name==name)
    two=next(n for n in new.body if isinstance(n,ast.FunctionDef) and n.name==name)
    assert ast.dump(one,include_attributes=False)==ast.dump(two,include_attributes=False)
ns={'s':s,'e':e}
nodes=[n for n in new.body if isinstance(n,ast.FunctionDef) and n.name in ('gamma','d3','candidate_basis')]
assert len(nodes)==3
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
p=s.Matrix(s.symbols('p0:4'));v=s.Matrix(s.symbols('v0:4'));axes=[s.eye(4)[:,i] for i in range(4)]
@lru_cache(None)
def jet(r,word):return ns['d3'](r,*word,p,v)
@lru_cache(None)
def symjet(r,word,inner=()):
    words=set(permutations(word))
    return tuple(sum(jet(r,w+inner)[o] for w in words)/len(words) for o in range(2))
def terms(f):return s.Poly(s.expand(f.subs(e.z,1)),*e.x).terms()
def moment(ts,word):
    add=tuple(word.count(i) for i in range(4))
    return sum(c*e.spherical_moment(tuple(i+j for i,j in zip(power,add))) for power,c in ts)

result=json.loads(prior.read_bytes());abc=list(map(s.Rational,result['flat_coefficients']));de=list(map(s.Rational,result['curved_coefficients']))
curve=json.loads((H/'finite_curved_source_harmonics_v2/results.json').read_bytes())
ca,cb=map(s.Rational,curve['A_contact_coefficients'])
for a in range(4):
    for b in range(a,4):
        T=s.zeros(4);T[a,b]=T[b,a]=1;out=[0,0]
        for r in range(4):
            ka,_=e.kernel(T,axes[r],axes[0],0);ta=terms(ka)
            for word in product(range(4),repeat=3):
                c=s.Rational(13,288)*moment(ta,word)
                if c:
                    got=symjet(r,word)
                    for o in range(2):out[o]+=c*got[o]
            for i in range(4):
                c=-s.Rational(1,64)*moment(ta,(i,))
                if c:
                    for j in range(4):
                        got=symjet(r,(i,j,j))
                        for o in range(2):out[o]+=c*got[o]
            for k in range(4):
                _,kb=e.kernel(T,axes[r],axes[k],0);tb=terms(kb)
                for i,j in product(range(4),repeat=2):
                    c=-s.Rational(5,48)*moment(tb,(i,j))
                    if c:
                        got=symjet(r,(i,j),(k,))
                        for o in range(2):out[o]+=c*got[o]
                c=s.Rational(5,192)*moment(tb,())
                if c:
                    for i in range(4):
                        got=jet(r,(i,i,k))
                        for o in range(2):out[o]+=c*got[o]
        basis=ns['candidate_basis'](T,p,v)
        ck(f'angular_flat_{a}_{b}',out[0]-sum(c*q[0] for c,q in zip(abc,basis)))
        ck(f'angular_curved_{a}_{b}',out[1]+ca*(v.T*T*p)[0]+cb*s.trace(T)*p.dot(v)
           -sum(c*q[1] for c,q in zip(abc,basis))-2*de[0]*(v.T*T*p)[0]-de[1]*s.trace(T)*p.dot(v))
        print(json.dumps(dict(stage='angular',fiber=[a,b],checks=len(checks),cpu=time.process_time()-start)),flush=True)

af,bf,cf=map(F,abc);df,ef=map(F,de);nonzero=[]
for seed in (1,2):
    c=polynomial_jet(lower_vector_initial([plus({ZERO:F(i-seed)},mono((i,),i+seed),
        mono((i,(i+1)%4),F(1,2)),mono((i,i,(i+2)%4),seed),
        mono((i,i,i,i,i),F(seed,7))) for i in range(4)]),1)
    @lru_cache(None)
    def scalar(w,o):
        value=cf*sum(c(w+(j,j,i),(i,),o) for i in range(4) for j in range(4))
        if o:value+=ef*sum(c(w+(i,),(i,),o-1) for i in range(4))
        return value
    @lru_cache(None)
    def sourcejet(w,a,b,o):
        value=af*sum(c(w+(a,i,i),(b,),o)+c(w+(b,i,i),(a,),o) for i in range(4))
        value+=bf*sum(c(w+(a,b,i),(i,),o) for i in range(4))
        value+=int(a==b)*cf*sum(c(w+(j,j,i),(i,),o) for i in range(4) for j in range(4))
        if o:
            value+=df*(c(w+(a,),(b,),o-1)+c(w+(b,),(a,),o-1))
            value+=ef*int(a==b)*sum(c(w+(i,),(i,),o-1) for i in range(4))
        return value
    for o in range(3):
        for a,b in product(range(4),repeat=2):
            actual=einstein_gauge(sourcejet,(),a,b,o)
            expected=-2*scalar((a,b),o)+2*int(a==b)*sum(scalar((i,i),o) for i in range(4))
            if o:expected+=6*int(a==b)*scalar((),o-1)
            ck(f'Einstein_{seed}_{o}_{a}_{b}',actual-expected)
            if actual and len(nonzero)<3:nonzero.append(dict(seed=seed,order=o,component=[a,b],value=str(actual)))
assert nonzero
out=dict(at=datetime.now(timezone.utc).isoformat(),status='FINITE_SOURCE_ANGULAR_AND_EINSTEIN_AUDIT',
    checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-start,
    pure_gauge_part='G[-7/48 Boxv+13/192 grad(divv)+65K/288 v]',
    nongauge_part='g[Box(divv)/32-29K divv/144]',
    Einstein_image='-2Hess(phi)+2gBox(phi)+6Kg phi, phi=Box(divv)/32-29K divv/144',
    nonzero_controls=nonzero,full_Q2=False,
    scope='Source local operator through explicit firstK; its Einstein image throughK2; no uncomputed new amplitude claimed'))
put('results.json',out)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in
    [Path(__file__),source,prior,H/'curved_source_jet_engine.py',H/'curved_cutoff_descent_engine.py',
     H/'oneform_second_curvature_engine_v2.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in out.items() if k!='check_names'},ensure_ascii=False))
