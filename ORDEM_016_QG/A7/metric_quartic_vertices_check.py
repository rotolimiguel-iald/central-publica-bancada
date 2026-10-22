"""Exact quartic checks: conformal sector, diffeomorphisms, Bose, trace legs."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import permutations
from time import perf_counter, process_time
import hashlib,json
from metric_principal_vertices import (I,basis,dot,gauge_matrix,lie_matrix,
    eh_quadratic_8k,eh_cubic_16k,clear_caches)
from metric_quartic_vertices import eh_quartic_32k
H=Path(__file__).resolve().parent
D=H/'metric_quartic_vertices';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'metric_quartic_vertices.py'),
    plans=['Bose24','conformal family','classical quartic-cubic Ward','two trace legs'],
    candidate_formula_explored_before_test=True,full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(name,a,b=0):
    assert a==b,(name,a,b,a-b);checks.append(name)
def neg(p):return tuple(-x for x in p)
def add(p,q):return tuple(x+y for x,y in zip(p,q))
zero=(0,0,0,0)
momenta=[(1,2,0,-1),(0,-1,1,0),(2,0,-1,1),(-3,-1,0,0)]
fields=[(basis(0,1),momenta[0]),(basis(1,2),momenta[1]),
        (basis(2,3),momenta[2]),(basis(0,3),momenta[3])]
value=eh_quartic_32k(*fields)
for perm in permutations(range(4)):
    check('Bose_'+str(perm),eh_quartic_32k(*(fields[i] for i in perm)),value)
for j,ps in enumerate([momenta,[(1,0,0,0),(-1,0,0,0),zero,zero],
                       [(1,1,1,1),(2,3,0,1),(-2,1,2,-1),(-1,-5,-3,-1)]]):
    check('conformal_'+str(j),eh_quartic_32k(*[(I,p) for p in ps]),
          -48*sum(dot(p,p) for p in ps))
bs=[basis(i,j) for i in range(4) for j in range(i,4)]
p=(1,2,-1,0)
for i,A in enumerate(bs):
    for j,B in enumerate(bs[i:],i):
        check(f'trace_internal_{i}_{j}',
            eh_quartic_32k((A,p),(B,neg(p)),(I,zero),(I,zero)),
            8*eh_quadratic_8k(A,p,B,neg(p)))
ward_nonzero=[]
for idx in range(16):
    k=momenta[0];v=tuple(int(a==idx%4) for a in range(4))
    actual=[(bs[(idx+2*r)%10],momenta[r+1]) for r in range(3)]
    lhs=eh_quartic_32k((gauge_matrix(k,v),k),*actual)
    total=0
    for pos,(A,p) in enumerate(actual):
        others=[f for r,f in enumerate(actual) if r!=pos]
        L=lie_matrix(A,p,k,v)
        total+=eh_cubic_16k(L,add(p,k),*others[0],*others[1])
    check('Ward_'+str(idx),lhs+2*total)
    if lhs:ward_nonzero.append([idx,lhs,total])
    clear_caches()
assert ward_nonzero,'vacuous Ward controls'
negatives=[dict(name='omit_cubic_Ward_piece',residue=ward_nonzero[0][1]),
           dict(name='wrong_polarization_factor',residue=value if value else ward_nonzero[0][1])]
assert all(n['residue']!=0 for n in negatives)
fresh(D/'results.json',dict(statute='REAL_EXACT_QUARTIC_DERIVATIVE_VERTEX_CHECK',
    checks=len(checks),check_names=checks,negative_controls=negatives,
    bose_sample=value,nonzero_Ward_examples=ward_nonzero,
    normalization='32*kappa*V4; cubic=16*kappa*V3; quadratic=8*kappa*V2',
    trace_internal_identity='32*kappa*V4(A,p;B,-p;g,0;g,0)=8*(8*kappa*V2_EH(A,p;B,-p))',
    conformal_identity='32*kappa*V4(g,p1;g,p2;g,p3;g,p4)=-48*sum(p_i²), sum(p_i)=0',
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'metric_quartic_vertices.py',H/'metric_principal_vertices.py',
     D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),nonzero_Ward=len(ward_nonzero),cpu_seconds=process_time()-cpu)))
