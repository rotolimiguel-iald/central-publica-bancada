"""Test the two derived skew-fiber terms, preserving fixed measured inputs."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from sympy.polys.matrices import DomainMatrix
import marked_polynomial_engine as p
import general_marked_engine as g
import quadratic_metric_engine as a2
import ghost_primitive_engine as z1
import bv_gradient_engine as bv
HERE=Path(__file__).resolve().parent;DEST=HERE/'bv_gradient_fit';DEST.mkdir(exist_ok=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def new(path,data):
    assert not path.exists(),str(path);b=json.dumps(data,ensure_ascii=False,indent=2).encode()
    t=path.with_name(path.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(path)
source=HERE/'general_marked/results.json'
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources={str(x):sha(x) for x in [Path(__file__),HERE/'bv_gradient_engine.py',source,HERE/'quadratic_metric_joint/results.json']},
    target='Measured residue=-2A2-K DeltaZ+d1 D1(E,r,v)+d2 D2(E,r,v)',
    derivation='D1=1/2[sym(r,Ev)-sym(v,Er)],D2=1/2[sym(v,r)trE-I(v.Er)]; skew in the symmetric fiber pairing',
    constraints='DeltaZ bracket homogeneous,constant sixcoefficients zero; loops and constant B fixed',full_Q2=False))
start,cpu=perf_counter(),process_time();r=json.loads(source.read_bytes())
saved={(x['H'],x['T'],x['v']):p.R.from_expr(s.sympify(x['residue'])) for x in r['components']}
rows=[];rhs=[];equations=[];COLS=80;skew_checks=0
for E in g.BASIS:
    for T in g.BASIS:
        for v in p.axes:
            es=bv.terms(E,p.Q,v);ts=bv.terms(T,p.Q,v)
            for x,y in zip(es,ts):
                assert p.inner(T,x)+p.inner(E,y)==0;skew_checks+=1
def append(target,cols,kind):
    assert len(cols)==COLS;keys=set(target)
    for c in cols:keys.update(c)
    for key in sorted(keys):rows.append([s.Rational(c.get(key,0)) for c in cols]);rhs.append(s.Rational(target.get(key,0)))
    equations.append((target,cols,kind))
for hi,H in enumerate(g.BASIS):
    for vi,v in enumerate(p.axes):
        As,names=a2.terms(H,p.P,p.gauge(p.Q,v),p.Q);zs=z1.terms(H,p.P,p.Q,v)
        ds=bv.terms(bv.einstein(H,p.P),p.Q,v)
        for ti,T in enumerate(g.BASIS):
            cols=[-2*p.inner(T,A) for A in As]+[-p.inner(T,p.gauge(p.add(p.P,p.Q),z)) for z in zs]+[p.inner(T,D) for D in ds]
            append(saved[hi,ti,vi],cols,'R1')
for v in p.axes:
    for w in p.axes:
        za=z1.terms(p.gauge(p.P,v),p.P,p.Q,w);zb=z1.terms(p.gauge(p.Q,w),p.Q,p.P,v)
        for n in range(4):append(p.ZERO,[p.ZERO]*57+[a[n]-b[n] for a,b in zip(za,zb)]+[p.ZERO]*2,'bracket')
for idx in [0,3,6,9,13,17]:
    cols=[p.ZERO]*80;cols[57+idx]=p.ONE;append(p.ZERO,cols,'constant')
M=s.Matrix(rows);y=s.Matrix(rhs);red,piv=DomainMatrix.from_Matrix(M.row_join(y)).to_field().rref()
mat=red.to_Matrix();consistent=(80 not in piv)
result=dict(statute='DERIVED_PRINCIPAL_BV_GRADIENT_COMPLETION' if consistent else 'MEDIDA_GRADIENT_BV_ANSATZ_INCOMPLETE',
    rows=M.rows,columns=80,rank=len([i for i in piv if i<80]),augmented_rank=len(piv),
    basis_names=names,skew_fiber_checks=skew_checks,full_Q2=False,gate_changed=False)
if consistent:
    coeff=[s.S.Zero]*80
    for row,col in enumerate(piv):coeff[col]=mat[row,80]
    qq=[p.QQ(int(x.p),int(x.q)) for x in coeff]
    assert all(t==sum((c*v for c,v in zip(qq,cols)),p.ZERO) for t,cols,_ in equations)
    result.update(A2_coefficients=list(map(str,coeff[:57])),DeltaZ_coefficients=list(map(str,coeff[57:78])),
                  gradient_coefficients=list(map(str,coeff[78:])),polynomial_checks=len(equations),
                  choice='Free coefficients zero; one representative, not canonical')
else:result['interpretation']='No solution in this expanded finite ansatz; no conclusion on full BV cohomology'
result.update(cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
