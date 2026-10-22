"""Exact signed-orbit S3 cubature through degree12 for full harmonic kernels."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import permutations,product,combinations_with_replacement
from math import gcd
import hashlib,json,time,uuid
import sympy as s
from one_loop_scale_engine import sphere_average_monomial
H=Path(__file__).resolve().parent;D=H/'angular_cubature_degree12';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),degree=12,
 selection='Greedy independent columns from primitive sorted integer seeds maxcoordinate<=4, ordered radius then seed',
 justification='FirstK angular kernel degree<=6, projector degree<=6, so degree12 is required',
 sources=[dict(path=str(p),sha256=sha(p)) for p in (Path(__file__),H/'one_loop_scale_engine.py')]))
cpu=time.process_time()
partitions=sorted({tuple(sorted(p,reverse=True)) for p in product(range(7),repeat=4) if sum(p)==6})
candidates=[q for q in combinations_with_replacement(range(5),4) if any(q) and gcd(*q)==1]
candidates.sort(key=lambda q:(sum(x*x for x in q),q))
@lru_cache(None)
def orbit(seed):
    return tuple(sorted({tuple(a*b for a,b in zip(v,signs)) for v in permutations(seed)
                         for signs in product((-1,1),repeat=4)}))
@lru_cache(None)
def moment(seed,powers):
    points=orbit(seed);z=sum(a*a for a in seed)
    return sum(s.prod(x**e for x,e in zip(v,powers)) for v in points)/s.Integer(len(points)*z**(sum(powers)//2))
selected=[];columns=[];rank=0
for seed in candidates:
    col=s.Matrix([moment(seed,tuple(2*n for n in part)) for part in partitions])
    trial=s.Matrix.hstack(*(columns+[col]));newrank=trial.rank()
    if newrank>rank:selected.append(seed);columns.append(col);rank=newrank
    if rank==len(partitions):break
assert rank==len(partitions)
weights=s.Matrix.hstack(*columns).inv()*s.Matrix([sphere_average_monomial(tuple(2*n for n in p)) for p in partitions])
for seed in selected:
    points=set(orbit(seed))
    for v in points:
        for i in range(4):assert tuple(-a if j==i else a for j,a in enumerate(v)) in points
        assert tuple(sorted(v)) in points
checks=0
for powers in product(range(13),repeat=4):
    if sum(powers)>12:continue
    if any(p%2 for p in powers):actual=0
    else:
        ordered=tuple(sorted(powers,reverse=True))
        actual=sum(w*moment(seed,ordered) for seed,w in zip(selected,weights))
    assert actual==sphere_average_monomial(powers),(powers,actual)
    checks+=1
nodes=[dict(vector=node,squared_radius=sum(q*q for q in seed),weight=str(w/len(orbit(seed))))
       for seed,w in zip(selected,weights) if w for node in orbit(seed)]
assert sum(s.Rational(row['weight']) for row in nodes)==1
result=dict(at=datetime.now(timezone.utc).isoformat(),status='EXACT_S3_DEGREE12_CUBATURE',degree=12,
 checks=checks,seeds=selected,orbit_weights=list(map(str,weights)),orbit_sizes=[len(orbit(q)) for q in selected],
 nodes=nodes,cpu_seconds=time.process_time()-cpu,full_Q2=False,
 rule='Mean on unitS3; integer vectors require explicit homogeneous radial factors',
 parity='Odd moments use verified closure under each sign flip; even moments exactly evaluated')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    (Path(__file__),D/'PRE_REGISTER.json',D/'results.json')]))
print(json.dumps({k:v for k,v in result.items() if k!='nodes'}))
