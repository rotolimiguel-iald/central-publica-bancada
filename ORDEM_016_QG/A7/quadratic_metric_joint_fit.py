"""Keep B fixed and permit exactly the homogeneous freedom in Z."""
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
HERE=Path(__file__).resolve().parent;DEST=HERE/'quadratic_metric_joint';DEST.mkdir(exist_ok=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def new(path,data):
    assert not path.exists(),str(path);b=json.dumps(data,ensure_ascii=False,indent=2).encode()
    t=path.with_name(path.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(path)
source=HERE/'general_marked/results.json'
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources={str(x):sha(x) for x in [Path(__file__),HERE/'quadratic_metric_engine.py',HERE/'ghost_primitive_engine.py',source,
                                   HERE/'quadratic_metric_fit/results.json']},
    target='Measured residue=-2A2(H,K_rv)-K_(p+r) DeltaZ, with DeltaZ bracket homogeneous and six constant coefficients zero',
    ansatz='57 quadratic metric contractions +21 ghost contractions under all homogeneous constraints',
    fixed='All measured vertices and the quadratic-antifield B are unchanged',full_Q2=False))
start,cpu=perf_counter(),process_time();r=json.loads(source.read_bytes())
saved={(x['H'],x['T'],x['v']):p.R.from_expr(s.sympify(x['residue'])) for x in r['components']}
rows=[];rhs=[];equations=[];COLS=78
def append(target,cols,kind):
    assert len(cols)==COLS
    keys=set(target)
    for c in cols:keys.update(c)
    for key in sorted(keys):rows.append([s.Rational(c.get(key,0)) for c in cols]);rhs.append(s.Rational(target.get(key,0)))
    equations.append((target,cols,kind))
for hi,H in enumerate(g.BASIS):
    for vi,v in enumerate(p.axes):
        As,names=a2.terms(H,p.P,p.gauge(p.Q,v),p.Q)
        zs=z1.terms(H,p.P,p.Q,v)
        for ti,T in enumerate(g.BASIS):
            cols=[-2*p.inner(T,A) for A in As]+[-p.inner(T,p.gauge(p.add(p.P,p.Q),z)) for z in zs]
            append(saved[hi,ti,vi],cols,'R1')
for v in p.axes:
    for w in p.axes:
        za=z1.terms(p.gauge(p.P,v),p.P,p.Q,w);zb=z1.terms(p.gauge(p.Q,w),p.Q,p.P,v)
        for n in range(4):append(p.ZERO,[p.ZERO]*57+[a[n]-b[n] for a,b in zip(za,zb)],'bracket')
for idx in [0,3,6,9,13,17]:
    cols=[p.ZERO]*78;cols[57+idx]=p.ONE;append(p.ZERO,cols,'constant')
M=s.Matrix(rows);y=s.Matrix(rhs);red,piv=DomainMatrix.from_Matrix(M.row_join(y)).to_field().rref()
mat=red.to_Matrix();consistent=(78 not in piv)
result=dict(statute='DERIVED_PRINCIPAL_QUADRATIC_METRIC_JOINT_COMPLETION' if consistent else 'MEDIDA_BV_ANSATZ_STILL_INCOMPLETE',
    rows=M.rows,columns=78,rank=len([i for i in piv if i<78]),augmented_rank=len(piv),
    basis_names=names,full_Q2=False,gate_changed=False)
if consistent:
    coeff=[s.S.Zero]*78
    for row,col in enumerate(piv):coeff[col]=mat[row,78]
    qq=[p.QQ(int(x.p),int(x.q)) for x in coeff]
    assert all(t==sum((c*v for c,v in zip(qq,cols)),p.ZERO) for t,cols,_ in equations)
    result.update(A2_coefficients=list(map(str,coeff[:57])),DeltaZ_coefficients=list(map(str,coeff[57:])),
                  polynomial_checks=len(equations),choice='Free coefficients zero; one representative')
else:
    result['interpretation']='The fixed quadratic-antifield ansatz is not enough for these measured R1 components. This does not prove nontrivial full BV cohomology.'
result.update(cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
