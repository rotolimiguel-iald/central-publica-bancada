"""Directed ghost finite pair: independent fiber selection and exact O4 checks."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from finite_ghost_pair_engine import finite_node,F,BASIS
H=Path(__file__).resolve().parent;D=H/'finite_ghost_pair';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)

def inv(a,b,p,order):
    A=s.Matrix(4,4,BASIS[a]);B=s.Matrix(4,4,BASIS[b]);q=s.Matrix(p)
    if order==2:return [s.trace(A*B),s.trace(A)*s.trace(B)]
    return [q.dot(q)*s.trace(A*B),q.dot(q)*s.trace(A)*s.trace(B),
        (q.T*A*q)[0]*s.trace(B),(q.T*B*q)[0]*s.trace(A),(q.T*A*B*q)[0]]

p=(1,0,0,0);selected=[];rows=[]
for a in reversed(range(10)):
    for b in reversed(range(10)):
        row=inv(a,b,p,1)
        if s.Matrix(rows+[row]).rank()>len(rows):selected.append((a,b));rows.append(row)
        if len(rows)==5:break
    if len(rows)==5:break
assert len(rows)==5
holdouts=[(0,0),(1,1),(0,4),(4,0)]
assert not any(pair in selected for pair in holdouts)
sources=[Path(__file__),H/'finite_ghost_pair_engine.py',H/'ghost_direct_position_engine.py',
    H/'finite_angular_contact_engine.py',H/'position_metric_ordered_operator_engine.py',
    H/'angular_cubature/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Actual directed ghost pair finite contact relative to same harmonic reference as metric pair',
    fit_pairs=selected,unused_pairs=holdouts,nonaxis=dict(pair=[1,3],p=[1,2,-1,1]),
    K2_fit_pairs=[[8,8],[7,9]],K2_unused_pairs=[[0,0],[4,0]],
    inputs=['fixed R','directed Wick contraction','ordered covariant jets','S3 cubature degree8'],
    excluded=['full Ward anomaly','smooth W','finite tadpole normalization'],
    sources=[dict(path=str(q),sha256=sha(q)) for q in sources]))
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
cpu=time.process_time();values=[];cache={};checks=[]
def evaluate(a,b,p,order):
    key=(a,b,p,order)
    if key in cache:return cache[key]
    total=[F() for _ in range(4)]
    for i,node in enumerate(nodes):
        out=finite_node(BASIS[a],BASIS[b],p,tuple(node['vector']),order)
        for j in range(4):total[j]+=F(node['weight'])*out[j]
        if i%64==0:print(json.dumps(dict(order=order,pair=[a,b],node=i,cpu=time.process_time()-cpu)),flush=True)
    result=sum(total);cache[key]=result
    row=dict(order=order,pair=[a,b],p=p,pieces=list(map(str,total)),value=str(result))
    values.append(row);print(json.dumps(row),flush=True)
    return result
def ck(label,got,expected):
    assert s.Rational(got)==expected,(label,got,expected)
    checks.append(label)
data=s.Matrix([s.Rational(evaluate(a,b,p,1)) for a,b in selected])
c1=list(s.Matrix(rows).inv()*data)
for a,b in holdouts:ck(f'K1_unused_{a}_{b}',evaluate(a,b,p,1),sum(c*v for c,v in zip(c1,inv(a,b,p,1))))
np=(1,2,-1,1)
ck('K1_nonaxis',evaluate(1,3,np,1),sum(c*v for c,v in zip(c1,inv(1,3,np,1))))
zero=(0,0,0,0)
c2=[s.Rational(evaluate(8,8,zero,2))/2,s.Rational(evaluate(7,9,zero,2))]
for a,b in [(0,0),(4,0)]:ck(f'K2_unused_{a}_{b}',evaluate(a,b,zero,2),sum(c*v for c,v in zip(c2,inv(a,b,zero,2))))
metric=json.loads((H/'finite_metric_pair/results.json').read_bytes())
combined1=[-s.Rational(m)/2+g for m,g in zip(metric['first_K_coefficients'],c1)]
combined2=[-s.Rational(m)/2+g for m,g in zip(metric['second_K_coefficients'],c2)]
result=dict(at=datetime.now(timezone.utc).isoformat(),status='DIRECTED_GHOST_PAIR_FINITE_CONTACT_MEASURED',
    checks=len(checks),check_names=checks,values=values,first_K_coefficients=list(map(str,c1)),
    second_K_coefficients=list(map(str,c2)),first_K_exchange_defect=str(c1[2]-c1[3]),
    common_raw_convention_combination_K1=list(map(str,combined1)),
    common_raw_convention_combination_K2=list(map(str,combined2)),
    combination_scope='-metric_raw/2+ghost_direct; NO finite tadpoles, source, smooth W or causal phases',
    first_K_basis=metric['first_K_basis'],second_K_basis=metric['second_K_basis'],
    cpu_seconds=time.process_time()-cpu,full_Q2=False,gate_changed=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q))
    for q in sources+[D/'PRE_REGISTER.json',D/'results.json',H/'finite_metric_pair/results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('values','check_names')},ensure_ascii=False))
