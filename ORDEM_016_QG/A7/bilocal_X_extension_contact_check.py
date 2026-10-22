"""X-stage extension contact after Y has been integrated off diagonal.

This isolates one required stage. It is not the original full bilocal Ward
contact, whose regulator derivatives at Y are deliberately still missing.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import json,hashlib,time,uuid
import sympy as s
import einstein_radial_aux_engine as E
import logarithmic_contact_engine as R
H=Path(__file__).resolve().parent;D=H/'bilocal_X_extension_contact';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[H/'bilocal_full_external_pair/results.json',H/'source_einstein_radial_aux/results.json',
        H/'bilocal_bulk_ward_closure/results.json',H/'einstein_radial_aux_engine.py',
        H/'logarithmic_contact_engine.py',Path(__file__)]
loop=json.loads(inputs[0].read_bytes());source=json.loads(inputs[1].read_bytes())
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    prescription='FP_a[(1-a)mu^(2a)z^a]; Euclidean C_E=-4pi²',
    target='R(C0)-divX R(C1)+EinsteinX R(C), after off-diagonal Y integration',
    method='Off-diagonal identity removes a0; take coefficient of a of commutators, then meromorphic residue',
    includes=['X derivative on regulator','frame conversion','volume coefficient at firstK'],
    excludes=['Y endpoint regulator contacts','W','tadpoles','K2','higher arities','Lorentz boundary value'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],full_Q2=False))
cpu=time.process_time();a=s.Symbol('a');x=E.x;z=E.radial_z;Q=R.Q
def de(i,j):return s.Integer(i==j)
def frame(i,j):return (z*de(i,j)-x[i]*x[j])/6
def reduce(f):
    num,den=s.fraction(s.cancel(s.expand(f)))
    return s.cancel(s.rem(num,E.Z-z,x[0])/den)
c1=[[s.Rational(loop['coefficients']['ghost']['C1'][o][i])-s.Rational(loop['coefficients']['metric']['C1'][o][i])/2
     for i in range(7)] for o in (0,1)]
sc=[[s.Rational(t) for t in row] for row in source['source_coefficients']]
@lru_cache(None)
def fourth(o,i,b,c,r):
    ts=[de(i,r)*de(b,c),de(i,b)*de(c,r)+de(i,c)*de(b,r),de(b,c)*x[i]*x[r],
        de(i,r)*x[b]*x[c],de(i,b)*x[c]*x[r]+de(i,c)*x[b]*x[r],
        de(b,r)*x[i]*x[c]+de(c,r)*x[i]*x[b],x[i]*x[b]*x[c]*x[r]]
    return sum(v*t/z**(n-o) for v,t,n in zip(c1[o],ts,[4,4,5,5,5,5,6]))
def source_field(o,r):
    A,B,C=sc[o]
    return s.Matrix(4,4,lambda i,j:(A*de(i,j)*x[r]+B*(de(i,r)*x[j]+de(j,r)*x[i]))/z**(4-o)+C*x[i]*x[j]*x[r]/z**(5-o))
@lru_cache(None)
def sphere_monomial(powers):
    if any(v%2 for v in powers):return s.Integer(0)
    m=sum(powers)//2
    return s.prod(s.factorial2(v-1) for v in powers)/s.Integer(2**m*s.factorial(m+1))
@lru_cache(None)
def radial_residue(n,powers):
    degree=2*n-4-sum(powers)
    if degree<0:return s.Integer(0)
    test=s.Poly(s.expand((-sum(Q[i]*x[i] for i in range(4)))**degree),*x)
    return s.expand(-sum(co*sphere_monomial(tuple(pp[i]+powers[i] for i in range(4)))
                         for pp,co in test.terms())/(4*s.factorial(degree)))
checked=set()
def contact(f, independent=False):
    out=0
    for term in s.expand(f).as_ordered_terms():
        if not term:continue
        power=term.as_powers_dict().get(z,s.Integer(0))
        assert power.is_Integer and power<=0,(term,power)
        n=int(-power)
        pol=s.Poly(s.expand(term*z**n),*x)
        for powers,co in pol.terms():
            assert co.is_Rational,(co,term)
            expected=R.residue(n,powers,(1,1,1,1))
            if (n,powers) not in checked:
                alt=radial_residue(n,powers)
                assert s.expand(alt-expected)==0,(n,powers,alt,expected)
                checked.add((n,powers))
            out+=co*(radial_residue(n,powers) if independent else expected)
    return s.expand(out)
values={};checks=[];negatives=[]
for r in range(4):
    image=E.einstein([source_field(0,r),source_field(1,r)],[2*a*xx/z for xx in x])
    # Only a^1 contributes because the rational homogeneous distributions have simple poles.
    comm=[mat.applyfunc(lambda v:s.expand(v).coeff(a,1)) for mat in image]
    frames=[comm[0],(comm[1]+s.Matrix(4,4,lambda i,j:sum(frame(i,t)*comm[0][t,j]+frame(j,t)*comm[0][i,t] for t in range(4)))).applyfunc(s.expand)]
    density=[]
    for o in (0,1):
        entries=s.Matrix(4,4,lambda i,j:s.expand(frames[o][i,j]-2*sum(x[k]*fourth(o,k,i,j,r) for k in range(4))/z))
        density.append(entries)
    weighted=[density[0],(density[1]-z*density[0]/2).applyfunc(s.expand)]
    for o in (0,1):
        for i in range(4):
            for j in range(4):
                f=s.expand(weighted[o][i,j])
                got=contact(f)
                alt=contact(f,True)
                assert s.expand(got-alt)==0
                assert s.expand(got-contact(reduce(f)))==0,'Residue must respect z=X²'
                checks.append([o,i,j,r])
                values[str((o,i,j,r))]=str(got)
    if r==0:
        nv=contact(weighted[1][1,1])-contact(density[1][1,1])
        if nv!=0:negatives.append(dict(name='omit_volume_firstK',residual_over_C=str(nv)))
        loop_only=-2*sum(x[k]*fourth(0,k,1,1,r) for k in range(4))/z
        ns=contact(weighted[0][1,1])-contact(loop_only)
        if ns!=0:negatives.append(dict(name='omit_Einstein_regulator_commutator',residual_over_C=str(ns)))
    print('SOURCE_INDEX',r,'checks',len(checks),'residue_monomials',len(checked),'cpu',time.process_time()-cpu,flush=True)
# Extract the three invariant coefficients at each differential order.
q2=sum(t*t for t in Q);coeffs=[]
for o in (0,1):
    u,v,w=s.symbols('u v w');d=2-o
    equations=[]
    for i,j,r in [(1,1,0),(0,1,1),(0,0,0)]:
        pred=u*de(i,j)*Q[r]*q2**d+v*(de(i,r)*Q[j]+de(j,r)*Q[i])*q2**d+w*Q[i]*Q[j]*Q[r]*q2**(d-1)
        equations += s.Poly(s.expand(pred-s.sympify(values[str((o,i,j,r))])),*Q).coeffs()
    sol=s.solve(equations,(u,v,w),dict=True);assert len(sol)==1,sol
    coeffs.append([str(sol[0][t]) for t in (u,v,w)])
    for i in range(4):
        for j in range(4):
            for r in range(4):
                pred=sol[0][u]*de(i,j)*Q[r]*q2**d+sol[0][v]*(de(i,r)*Q[j]+de(j,r)*Q[i])*q2**d+sol[0][w]*Q[i]*Q[j]*Q[r]*q2**(d-1)
                assert s.expand(pred-s.sympify(values[str((o,i,j,r))]))==0
                checks.append(['O4',o,i,j,r])
result=dict(at=datetime.now(timezone.utc).isoformat(),status='X_STAGE_CONTACT_AFTER_Y_INTEGRATION_MEASURED',
    checks=len(checks),residue_monomials_checked=len(checked),cpu_seconds=time.process_time()-cpu,
    coefficients_over_C_E=coeffs,C_E='-4pi²',
    invariant_basis='[delta_ab q_r(q²)^(2-o), (delta_ar q_b+delta_br q_a)(q²)^(2-o), q_a q_b q_r(q²)^(1-o)]',
    q_means='coordinate derivatives acting on delta at origin, orthonormal test components paired with dvolX',
    negative_controls=negatives,values=values,full_Q2=False,Y_regulator_contacts_included=False,
    caveat='Intermediate contact: no inference that this is the complete Ward anomaly or its cohomology class')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='values'}))
