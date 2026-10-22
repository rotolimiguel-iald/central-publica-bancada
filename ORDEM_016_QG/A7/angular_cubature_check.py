"""Exact degree-eight S3 cubature for the remaining local position bubble."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import permutations,product
from fractions import Fraction
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from one_loop_scale_engine import sphere_average_monomial
H=Path(__file__).resolve().parent;D=H/'angular_cubature';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),reference_sha256=sha(H/'one_loop_scale_engine.py'),
    target='All S3 polynomial moments through degree8 using signed permutation orbits',
    purpose='Exact angular integration of first-curvature metric bubble, no numeric quadrature'))
cpu,wall=process_time(),perf_counter()
seeds=[(1,0,0,0),(1,1,0,0),(1,1,1,0),(1,1,1,1),(2,1,0,0)]
orbits=[sorted({tuple(a*b for a,b in zip(v,signs))
    for v in permutations(seed) for signs in product((-1,1),repeat=4)}) for seed in seeds]
zs=[sum(v*v for v in seed) for seed in seeds]
def orbit_moment(orbit,z,powers):
    if sum(powers)%2:return s.S.Zero
    return sum(s.prod(v**p for v,p in zip(node,powers)) for node in orbit)/s.Integer(len(orbit)*z**(sum(powers)//2))
partitions=[(8,0,0,0),(6,2,0,0),(4,4,0,0),(4,2,2,0),(2,2,2,2)]
M=s.Matrix([[orbit_moment(orb,z,p) for orb,z in zip(orbits,zs)] for p in partitions])
assert M.det()!=0
weights=M.inv()*s.Matrix([sphere_average_monomial(p) for p in partitions])
checks=0
for powers in product(range(9),repeat=4):
    if sum(powers)>8:continue
    # Odd monomials vanish under each full sign orbit; even cases rational.
    if any(p%2 for p in powers):
        actual=0
        for orb in orbits:assert sum(s.prod(v**p for v,p in zip(node,powers)) for node in orb)==0
    else:actual=sum(w*orbit_moment(orb,z,powers) for w,orb,z in zip(weights,orbits,zs))
    assert actual==sphere_average_monomial(powers),(powers,actual)
    checks+=1
nodes=[]
for w,orb,z in zip(weights,orbits,zs):
    for v in orb:nodes.append(dict(vector=v,squared_radius=z,weight=str(w/len(orb))))
assert sum(s.Rational(n['weight']) for n in nodes)==1
fresh(D/'results.json',dict(statute='REAL_EXACT_DEGREE8_ANGULAR_CUBATURE',checks=checks,
    seeds=seeds,orbit_sizes=list(map(len,orbits)),orbit_weights=list(map(str,weights)),
    nodes=nodes,normalization='Mean on unit S3; evaluate polynomial at vector/sqrt(squared_radius)',
    homogeneous_kernel_rule='For degree -4 kernel times Taylor polynomial, multiply value at vector by squared_radius²',
    limitations='Not an arbitrary-function quadrature; only the proven polynomial degree',
    full_Q2=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,node_count=len(nodes),weights=list(map(str,weights)),cpu_seconds=process_time()-cpu)))
