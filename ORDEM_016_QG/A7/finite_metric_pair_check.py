"""Fit O(4) local finite pair contact and check unused fibers/momenta."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time
import uuid
import sympy as s
from finite_metric_pair_engine import finite_node, F, BASIS

H=Path(__file__).resolve().parent
D=H/'finite_metric_pair'
D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists(),p
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)

def invariants(a,b,p,order):
    A=s.Matrix(4,4,BASIS[a]);B=s.Matrix(4,4,BASIS[b]);q=s.Matrix(p)
    if order==2:return [s.trace(A*B),s.trace(A)*s.trace(B)]
    return [q.dot(q)*s.trace(A*B),q.dot(q)*s.trace(A)*s.trace(B),
            (q.T*A*q)[0]*s.trace(B),(q.T*B*q)[0]*s.trace(A),(q.T*A*B*q)[0]]

p=(1,0,0,0)
selected=[];rows=[]
for a in range(10):
    for b in range(10):
        row=invariants(a,b,p,1)
        if s.Matrix(rows+[row]).rank()>len(rows):
            selected.append((a,b));rows.append(row)
        if len(rows)==5:break
    if len(rows)==5:break
assert len(rows)==5
sources=[Path(__file__),H/'finite_metric_pair_engine.py',H/'finite_angular_contact_engine.py',
         H/'position_metric_ordered_operator_engine.py',H/'angular_cubature/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Raw metric finite pair contact relative to harmonic differential reference, K1 and K2',
    fit_pairs=selected,holdouts=[[1,1],[0,4],[4,0],[5,5]],
    nonaxis_pair=[1,3],nonaxis_p=[1,2,-1,1],
    curvature2_pairs=[[1,1],[0,4],[0,0],[4,0]],
    exclusions=['tadpole finite normalization','smooth W','full Ward sum','physical Lorentz phase'],
    sources=[dict(path=str(q),sha256=sha(q)) for q in sources]))
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
start=time.process_time();cache={};values=[];checks=[]
def evaluate(a,b,p,order):
    key=(a,b,p,order)
    if key in cache:return cache[key]
    total=[F() for _ in range(4)]
    for i,node in enumerate(nodes):
        got=finite_node(BASIS[a],BASIS[b],p,tuple(node['vector']),order)
        for j in range(4):total[j]+=F(node['weight'])*got[j]
        if i%32==0:print(json.dumps(dict(order=order,pair=[a,b],node=i,cpu=time.process_time()-start)),flush=True)
    value=sum(total)
    row=dict(order=order,pair=[a,b],p=p,pieces=list(map(str,total)),value=str(value))
    values.append(row);cache[key]=value
    print(json.dumps(row),flush=True)
    return value

def check(label,got,expected):
    assert s.Rational(got)==expected,(label,str(got),str(expected))
    checks.append(label)

data=[s.Rational(evaluate(a,b,p,1)) for a,b in selected]
coef=list(s.Matrix(rows).inv()*s.Matrix(data))
for a,b in [(1,1),(0,4),(4,0),(5,5)]:
    check(f'K1_fiber_{a}_{b}',evaluate(a,b,p,1),sum(c*v for c,v in zip(coef,invariants(a,b,p,1))))
nonaxis=(1,2,-1,1)
check('K1_nonaxis',evaluate(1,3,nonaxis,1),sum(c*v for c,v in zip(coef,invariants(1,3,nonaxis,1))))
zero=(0,0,0,0)
c2=[s.Rational(evaluate(1,1,zero,2))/2,s.Rational(evaluate(0,4,zero,2))]
for a,b in [(0,0),(4,0)]:
    check(f'K2_fiber_{a}_{b}',evaluate(a,b,zero,2),sum(c*v for c,v in zip(c2,invariants(a,b,zero,2))))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='RAW_PAIR_COMPONENT_MEASURED',
    checks=len(checks),check_names=checks,values=values,
    first_K_coefficients=list(map(str,coef)),second_K_coefficients=list(map(str,c2)),
    first_K_basis=['p²trAB','p²trA trB','pAp trB','pBp trA','pABp'],
    second_K_basis=['trAB','trA trB'],
    first_K_exchange_defect=str(coef[2]-coef[3]),
    normalization='Raw metric pair; contact / C; existing factor1/16; Wick -1/2 not yet applied',
    cpu_seconds=time.process_time()-start,full_Q2=False,gate_changed=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('values','check_names')},ensure_ascii=False))
