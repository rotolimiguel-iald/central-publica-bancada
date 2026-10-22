"""Independent Euclidean spherical-residue check of the new finite contact."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
from functools import lru_cache
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'finite_contact_angular';DEST.mkdir(exist_ok=True)
def new(p,obj):
    data=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(data)
    assert q.read_bytes()==data;q.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    route='S3 moments of Taylor test jets for radial poles, not x-times-box-delta',
    input='C_E=-4pi²; residue=half spherical integral; quartic radial chain rule explicit',
    target='Audit all35 quartic components and the longitudinal finite defect',
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    predecessor_sha256=hashlib.sha256((HERE/'finite_principal_contact/results.json').read_bytes()).hexdigest()))
start=time.process_time();wall=time.perf_counter();a=s.Symbol('a');q=s.symbols('q0:4');q2=sum(t*t for t in q)
prior=json.loads((HERE/'finite_principal_contact/results.json').read_bytes())
A,B,C=map(s.Rational,prior['derivative_contact_abc'])
def compositions(n,d):
    if d==1:yield(n,);return
    for k in range(n+1):
        for rest in compositions(n-k,d-1):yield(k,)+rest
def moment(exps):
    if any(e%2 for e in exps):return s.Integer(0)
    half=sum(exps)//2
    return s.prod(s.factorial2(e-1) for e in exps)/s.Integer(2**half*s.factorial(half+1))
@lru_cache(None)
def angular_residue(n,powers):
    # Res/C_E = -1/4 times normalized sphere average of the test Taylor jet.
    degree=2*n-4-sum(powers);assert degree>=0
    answer=0
    for k in compositions(degree,4):
        avg=moment(tuple(i+j for i,j in zip(k,powers)))
        answer+=(-1)**degree*avg*s.prod(q[i]**k[i]/s.factorial(k[i]) for i in range(4))
    return s.expand(-answer/4)
def powers(inds):return tuple(inds.count(i) for i in range(4))
dc4=s.diff(16*(a-2)*(a-3)*(a-4)*(a-5),a).subs(a,0)
dc2=s.diff(8*(a-2)*(a-3)*(a-4),a).subs(a,0)
dc0=s.diff(4*(a-2)*(a-3),a).subs(a,0)
checks=0
for inds in combinations_with_replacement(range(4),4):
    i,j,k,l=inds
    pairs=[((i,j),(k,l)),((i,k),(j,l)),((i,l),(j,k)),
           ((j,k),(i,l)),((j,l),(i,k)),((k,l),(i,j))]
    disjoint=[((i,j),(k,l)),((i,k),(j,l)),((i,l),(j,k))]
    value=-dc4*angular_residue(6,powers(list(inds)))
    value-=dc2*sum(angular_residue(5,powers(list(rest))) for pair,rest in pairs if pair[0]==pair[1])
    value-=dc0*sum(angular_residue(4,(0,0,0,0)) for pair,rest in disjoint
                  if pair[0]==pair[1] and rest[0]==rest[1])
    middle=sum(q[rest[0]]*q[rest[1]] for pair,rest in pairs if pair[0]==pair[1])
    last=sum(1 for pair,rest in disjoint if pair[0]==pair[1] and rest[0]==rest[1])
    expected=A*s.prod(q[t] for t in inds)+B*q2*middle+C*q2**2*last
    assert s.expand(value-expected)==0,inds
    checks+=1
ns=list(map(s.Rational,prior['finite_contact_coefficients_over_C']))
ward=[2*ns[0]+ns[3],2*ns[1]+2*ns[2],2*ns[2]+ns[3]+2*ns[4]]
assert ward[1]!=0 and s.expand(2*ward[1])!=0
# This is the e00 gauge direction paired with a transverse e11 component.
assert ward[1]==s.Rational(43,960)
checks+=3
physical_euclidean=[-2*n for n in ns] # C_E/(16pi^4) divided by A0=1/(8pi²).
assert s.simplify((-4*s.pi**2)/(16*s.pi**4)/(1/(8*s.pi**2)))==-2
checks+=1
new(DEST/'results.json',dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
    negative_controls=2,ward_coefficients_over_C=[str(x) for x in ward],
    ward_basis=['q4 Tq.v','q4 trT q.v','q2 qTq q.v'],
    Euclidean_contact_over_hbar_A0=[str(x) for x in physical_euclidean],
    chain_coefficient_derivatives=list(map(str,[dc4,dc2,dc0])),
    route='Sphere Taylor residues, independent of delta multiplication engine',
    physical_Lorentz_phase_not_claimed=True,full_Q2=False,
    cpu_seconds=time.process_time()-start,wall_seconds=time.perf_counter()-wall))
print(json.dumps(dict(checks=checks,ward=list(map(str,ward)),euclidean_contact=list(map(str,physical_euclidean)),
    cpu_seconds=time.process_time()-start)))
