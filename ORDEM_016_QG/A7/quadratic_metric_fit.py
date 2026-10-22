"""Fit the measured general R1 residue, without changing its fixed inputs."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from sympy.polys.matrices import DomainMatrix
import marked_polynomial_engine as p
import general_marked_engine as g
import quadratic_metric_engine as a2
HERE=Path(__file__).resolve().parent;DEST=HERE/'quadratic_metric_fit';DEST.mkdir(exist_ok=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def new(path,data):
    assert not path.exists(),str(path);b=json.dumps(data,ensure_ascii=False,indent=2).encode()
    t=path.with_name(path.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(path)
source=HERE/'general_marked/results.json'
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources={str(x):sha(x) for x in [Path(__file__),HERE/'quadratic_metric_engine.py',source]},
    target='R1 - (Lie_F H - K Z_new + B[(p+r/2).v E]) = -2 A2(H,p;K_r v,r)',
    ansatz='57 listed contractions symmetrized under exchange(H,p)<->(J,r)',
    not_assumed='Existence or completeness; inconsistent system is a measured negative result',full_Q2=False))
start,cpu=perf_counter(),process_time();r=json.loads(source.read_bytes())
saved={(x['H'],x['T'],x['v']):p.R.from_expr(s.sympify(x['residue'])) for x in r['components']}
rows=[];rhs=[];equations=[]
for hi,H in enumerate(g.BASIS):
    for vi,v in enumerate(p.axes):
        As,names=a2.terms(H,p.P,p.gauge(p.Q,v),p.Q)
        for ti,T in enumerate(g.BASIS):
            cols=[-2*p.inner(T,A) for A in As];target=saved[hi,ti,vi]
            keys=set(target)
            for c in cols:keys.update(c)
            for key in sorted(keys):
                rows.append([s.Rational(c.get(key,0)) for c in cols]);rhs.append(s.Rational(target.get(key,0)))
            equations.append((target,cols))
M=s.Matrix(rows);y=s.Matrix(rhs);dm=DomainMatrix.from_Matrix(M.row_join(y)).to_field()
red,piv=dm.rref();mat=red.to_Matrix();consistent=(57 not in piv)
result=dict(statute='DERIVED_PRINCIPAL_QUADRATIC_METRIC_COMPLETION' if consistent else 'MEDIDA_FIXED_Z_B_QUADRATIC_ANSATZ_INCONSISTENT',
    rows=M.rows,columns=57,rank=len([i for i in piv if i<57]),augmented_rank=len(piv),
    basis_names=names,full_Q2=False,gate_changed=False)
if consistent:
    coeff=[s.S.Zero]*57
    for row,col in enumerate(piv):coeff[col]=mat[row,57]
    qq=[p.QQ(int(x.p),int(x.q)) for x in coeff]
    assert all(t==sum((c*v for c,v in zip(qq,cols)),p.ZERO) for t,cols in equations)
    result.update(coefficients=list(map(str,coeff)),polynomial_checks=len(equations),
                  nonzero_coefficients=[dict(index=i,name=names[i],value=str(x)) for i,x in enumerate(coeff) if x],
                  choice='Free coefficients zero, one local representative, not canonical')
else:
    result['next']='Use the six already allowed homogeneous Z directions, preserving bracket and constant-ghost identity; do not change loop data'
result.update(cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result)
print(json.dumps(result,ensure_ascii=False),flush=True)
