"""Finite extension of the actual first-K geometric antifield-source kernels.

Density transport included. Smooth W and full Ward sum remain outside this
calculation, explicitly. The existing analytic pair prescription is unchanged.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
import sympy as s
import curved_source_jet_engine as e
from finite_harmonic_extension_engine import represent,Q
H=Path(__file__).resolve().parent;D=H/'finite_curved_source_harmonics';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    assert not p.exists();b=json.dumps(v,indent=2).encode();q=p.with_suffix('.tmp')
    q.write_bytes(b);assert q.read_bytes()==b;q.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    engine_sha256=sha(H/'finite_harmonic_extension_engine.py'),
    target='Actual firstK A and B source kernels, geometric singular part plus external density transport',
    prescription='R=FP[(1-a)mu^(2a)z^a .], already fixed; differential harmonic form is only a computational representation',
    excluded=['smooth W not zeroed','no complete Ward anomaly claim','no counterterm selected']))
cpu=process_time();checks=0;I=s.eye(4);X=s.Matrix(e.x);q=s.Matrix(Q);p=I[:,0]
def check(a,b=0):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
def kernels(T,v,p):
    correction=-e.z*T/6-(X*X.T*T+T*X*X.T)/6
    a,b=e.kernel(T,v,p,1);c,d=e.kernel(correction,v,p,0)
    return s.expand(a+c),s.expand(b+d)
def serialize(rows):
    return [{k: ([str(v) for v in value] if isinstance(value,tuple) else str(value) if isinstance(value,s.Basic) else value)
             for k,value in row.items()} for row in rows]
outputs=[];rows=[];values=[];nonzero=0
for a in range(4):
    for b in range(a,4):
        T=s.zeros(4);T[a,b]=T[b,a]=1
        for vi in range(4):
            v=I[:,vi];A,B=kernels(T,v,p)
            ra,ca=represent(A);rb,cb=represent(B)
            check(cb)
            # Return coefficients of q for a fully covariant source-contact fit.
            for qi in range(4):
                rows.append([s.diff((q.T*T*v)[0],Q[qi]),s.diff(s.trace(T)*q.dot(v),Q[qi])])
                values.append(s.diff(ca,Q[qi]))
            nonzero+=int(ca!=0)
            outputs.append(dict(T=[a,b],v=vi,A=serialize(ra),B=serialize(rb),A_contact_over_C=str(ca),B_contact_over_C=str(cb)))
        print(json.dumps(dict(fiber=[a,b],cases=len(outputs),checks=checks,cpu=process_time()-cpu)),flush=True)
fit,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix(values));assert len(params)==0
check(s.Matrix(rows)*fit,s.Matrix(values)) if False else None
for a,b in zip(s.Matrix(rows)*fit,values):check(a,b)
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
v=s.Matrix([2,-1,1,3]);p=s.Matrix([1,2,-1,1]);A,B=kernels(T,v,p)
ra,ca=represent(A);rb,cb=represent(B)
check(ca,fit[0]*(q.T*T*v)[0]+fit[1]*s.trace(T)*q.dot(v));check(cb)
assert nonzero
fresh(D/'results.json',dict(statute='DERIVED_ACTUAL_GEOMETRIC_SOURCE_PAIR_FINITE_HARMONIC_REPRESENTATION_FIRST_K',
    checks=checks,cases=len(outputs)+1,contact_basis=['q.T.v','trT q.v'],A_contact_coefficients=list(map(str,fit)),
    B_contact='0 relative to its displayed harmonic differential representation',
    nonzero_A_cases=nonzero,profiles=outputs,dense_holdout=dict(A_contact=str(ca),B_contact=str(cb)),
    cpu_seconds=process_time()-cpu,scope='Coordinate pair kernels with covariant external density; before anchored-leg adjoints',
    excludes='Smooth reference W, curvature commutators from moving distributional derivatives to ghost, full metric+ghost+source Ward sum',
    analytic_residue_identity_is_input=True,full_Q2=False,prescription_changed=False))
files=[Path(__file__),H/'finite_harmonic_extension_engine.py',H/'logarithmic_contact_engine.py',H/'curved_source_jet_engine.py',
       H/'covariant_source_density/results.json',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,cases=len(outputs)+1,coefficients=list(map(str,fit)),cpu=process_time()-cpu)))
