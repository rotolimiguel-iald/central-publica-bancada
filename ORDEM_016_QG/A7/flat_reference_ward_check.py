"""Calculate the previously uncounted flat reference contribution to Ward."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from flat_reference_metric_engine import finite_node as metric
from flat_reference_ghost_engine import finite_node as ghost
from flat_reference_weight_engine import reference_coefficient,full_finite_coefficient,scalar_reference_local
from finite_angular_contact_engine import coefficient
from finite_harmonic_extension_engine_v2 import represent,Q
from curved_source_jet_engine import kernel
from position_metric_bubble_engine import BASIS

H=Path(__file__).resolve().parent;D=H/'flat_reference_ward';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    data=json.dumps(v,indent=2,ensure_ascii=False).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(data);assert t.read_bytes()==data;t.replace(p)
sources=[Path(__file__),H/'flat_reference_weight_engine.py',H/'flat_reference_inputs_manifest.json',
 H/'finite_pair_ward/results.json',H/'finite_relative_normalization_v2/LIGACAO_DOS_SINAIS.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Flat harmonic reference to common R(U2); evaluate actual metric/ghost/source before any subtraction',
 fixtures=[(1,[0,1,0,0]),(4,[1,0,0,0]),(0,[1,0,0,0])],
 nonaxis=dict(T=4,p=[1,2,-1,1],v=[2,-1,1,3]),
 scope='Euclidean local flat component only; no higher curvature/tadpole/W/causal hierarchy',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
for m in range(5):
    for l in range(m%2,m+1,2):
        assert s.simplify(coefficient(m,l,0)+reference_coefficient(m,l)-full_finite_coefficient(m,l))==0
        checks.append('Schwinger_scalar_'+str((m,l)))
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
prior=json.loads((H/'finite_pair_ward/results.json').read_bytes())
data=[]
def einstein(T,p):
    p=s.Matrix(p);p2=p.dot(p)
    return p2*T-p*(T*p).T-(T*p)*p.T+p*p.T*s.trace(T)+s.eye(4)*((p.T*T*p)[0]-p2*s.trace(T))
def source(T,p,v):
    a,b=kernel(T,s.Matrix(v),s.Matrix(p),0)
    ar,ac=represent(a);br,bc=represent(b)
    ra=scalar_reference_local(ar);rb=scalar_reference_local(br)
    sub=dict(zip(Q,p))
    # A gives three ghost derivatives, B two plus the explicit ghost momentum.
    return s.expand(-(ra+rb).subs(sub)),s.expand(-(ac+bc).subs(sub))
def basis(ti,p,v):
    T=s.Matrix(4,4,BASIS[ti]);p=s.Matrix(p);v=s.Matrix(v);p2=p.dot(p)
    return [p2**2*(p.T*T*v)[0],p2*(p.T*T*p)[0]*p.dot(v),p2**2*s.trace(T)*p.dot(v)]
def run(ti,p,v):
    G=tuple(p[a]*v[b]+p[b]*v[a] for a in range(4) for b in range(4));T=BASIS[ti]
    mt=F();gh=F()
    for n,node in enumerate(nodes):
        weight=F(node['weight']);x=tuple(node['vector'])
        mt+=weight*sum(metric(G,T,p,x,0));gh+=weight*sum(ghost(G,T,p,x,0))
    es,contact=source(einstein(s.Matrix(4,4,T),p),p,v)
    value=-s.Rational(mt)/2+s.Rational(gh)+es
    row=dict(T=ti,p=p,v=v,metric=str(mt),ghost=str(gh),Einstein_source_reference=str(es),
             Einstein_source_contact=str(contact),reference_Ward=str(value))
    data.append(row);print(json.dumps(dict(**row,cpu=time.process_time()-cpu)),flush=True)
    return value,contact
p=(1,0,0,0);fixtures=[(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))]
values=[];rows=[]
for ti,v in fixtures:
    value,es=run(ti,p,v);values.append(value);rows.append(basis(ti,p,v))
    ref=next(x for x in prior['values'] if x['order']==0 and x['T']==ti)
    assert es==s.Rational(ref['Einstein_source'])
    checks.append('source_E_flat_'+str(ti))
fit=list(s.Matrix(rows).inv()*s.Matrix(values))
np=(1,2,-1,1);nv=(2,-1,1,3);value,_=run(4,np,nv)
assert value==sum(a*b for a,b in zip(fit,basis(4,np,nv)))
checks.append('nonaxis_reference_prediction')
partial=list(map(s.Rational,prior['partial_Ward_coefficients']['0']))
total=[s.expand(a+b) for a,b in zip(partial,fit)]
old=[s.Rational(187,1920),-s.Rational(33,160),s.Rational(73,960)]
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FLAT_REFERENCE_WARD_COMPONENT_MEASURED',
 checks=len(checks),check_names=checks,reference_coefficients=list(map(str,fit)),
 contact_coefficients=list(map(str,partial)),total_flat_finite_coefficients=list(map(str,total)),
 prior_global_P4_reference_coefficients=list(map(str,old)),
 difference_from_prior_global_P4=list(map(str,[a-b for a,b in zip(total,old)])),
 bases=['p4 Tpv','p2 pTp pv','p4 trT pv'],values=data,cpu_seconds=time.process_time()-cpu,
 full_Q2=False,scope='Same raw-pair analytic R, flat contact plus scalar reference; no curvature/W/tadpole/higher arities')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('values','check_names')}))
