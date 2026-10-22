"""Curvature-relevant logarithmic contact maps, not a full curved graph amplitude."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import hashlib,json,time,uuid
import sympy as s
from logarithmic_contact_engine import contact,direct_laurent_contact,Q,lap
HERE=Path(__file__).resolve().parent;DEST=HERE/'logarithmic_contact';DEST.mkdir(exist_ok=True)
def new(name,obj):
    p=DEST/name;assert not p.exists();b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    prescription='R=FP[(1-a)mu^(2a)z^a u], unchanged from tensor_extension',
    target='Derivative contacts for z^-n log(mu^2 z)^ell, n=0,1,2; ell=0,1,2; derivative order2,3,4',
    scope='Local homogeneous/logarithmic building blocks only; no curved graph numerator inferred',
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    engine_sha256=hashlib.sha256((HERE/'logarithmic_contact_engine.py').read_bytes()).hexdigest(),
    cpu_budget_seconds=180))
cpu=time.process_time();wall=time.perf_counter();checks=0;maps=[]
for n in [0,1,2]:
    for ell in [0,1,2]:
        for order in [2,3,4]:
            indices=list(combinations_with_replacement(range(4),order))
            target_degree=order+2*n-4
            # Orthogonal covariance allows precisely these trace maps at these ranks.
            traces=[j for j in range(order//2+1) if j+n-2>=0]
            cs=s.symbols('b0:'+str(len(traces)))
            eqs=[]
            values=[]
            for inds in indices:
                p=s.prod(Q[i] for i in inds)
                row=[]
                for j in traces:
                    f=p
                    for _ in range(j):f=lap(f)
                    row.append(sum(t*t for t in Q)**(j+n-2)*f)
                actual=contact(n,ell,inds)
                expected=sum(c*f for c,f in zip(cs,row))
                eqs.extend(s.Poly(s.expand(actual-expected),*Q).coeffs())
                values.append((inds,row,actual))
            solutions=s.solve(eqs,cs,dict=True) if cs else [{}]
            assert len(solutions)==1,(n,ell,order,solutions)
            solution=solutions[0]
            assert all(c in solution for c in cs),(n,ell,order,'nonunique map')
            for label,signature in [('Euclidean',(1,1,1,1)),('Lorentz',(1,-1,-1,-1))]:
                q2=sum(signature[i]*Q[i]**2 for i in range(4))
                for inds in indices:
                    p=s.prod(Q[i] for i in inds);expected=0
                    for c,j in zip(cs,traces):
                        f=p
                        for _ in range(j):f=lap(f,signature)
                        expected+=solution[c]*q2**(j+n-2)*f
                    actual=contact(n,ell,inds,signature)
                    assert s.expand(actual-expected)==0,(n,ell,order,label,inds)
                    assert actual==direct_laurent_contact(n,ell,inds,signature)
                    checks+=2
            maps.append(dict(n=n,log_power=ell,derivative_order=order,
                output_degree=target_degree,terms=[dict(laplacians=j,q2_power=j+n-2,coefficient=str(solution[c])) for c,j in zip(cs,traces)]))
            if time.process_time()-cpu>180:raise RuntimeError('CPU timebox')
def box_contact(n,ell,power):
    terms={():s.Integer(1)}
    for _ in range(power):
        out={}
        for inds,c in terms.items():
            for i in range(4):
                key=tuple(sorted(inds+(i,i)));out[key]=out.get(key,0)+c
        terms=out
    return s.expand(sum(c*contact(n,ell,inds) for inds,c in terms.items()))
q2=sum(t*t for t in Q)
special=[(1,0,1,-1),(1,1,1,0),(1,1,2,s.Rational(3,2)*q2),
         (0,1,2,-4),(0,2,2,-8)]
for n,ell,power,expected in special:
    assert s.expand(box_contact(n,ell,power)-expected)==0;checks+=1
assert box_contact(0,2,2)!=0 # Drop logarithmic poles: false zero.
assert box_contact(1,1,1)==0 and box_contact(1,0,1)!=0 # Cannot reuse log-free contact.
new('results.json',dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,negative_controls=2,
    maps=maps,closed_formula='-sum_j Res(T_j)*(c_j^(ell+1)(0)/(ell+1)+1_(ell>=1)*c_j^(ell)(0))',
    unchanged_prescription=True,curved_graph_coefficients_computed=False,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall))
print(json.dumps(dict(checks=checks,maps=len(maps),cpu_seconds=time.process_time()-cpu)),flush=True)
