"""Compute the complete principal R1 tensor polynomial before fitting counterterms."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
import marked_polynomial_engine as p
import general_marked_engine as g
from marked_vertex_engine import marked, BASIS as SBASIS, AXES as SAXES
from metric_principal_vertices import eh_cubic_16k

HERE=Path(__file__).resolve().parent
DEST=HERE/'general_marked';DEST.mkdir(exist_ok=True)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def new(path,data):
    assert not path.exists(),str(path)
    raw=json.dumps(data,ensure_ascii=False,indent=2).encode()
    temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw;temp.replace(path)
fit=HERE/'constant_ghost_completion/results.json'
coeff=[p.QQ(s.Rational(x).p,s.Rational(x).q) for x in json.loads(fit.read_bytes())['full_Z_coefficients']]
def Z(H,k,l,v):
    tr=p.trace(H);hk=p.mv(H,k);hl=p.mv(H,l);hv=p.mv(H,v)
    kk=p.dot(k,k);kl=p.dot(k,l);ll=p.dot(l,l);kv=p.dot(k,v);lv=p.dot(l,v)
    ts=[p.scale(v,tr*kk),p.scale(v,tr*kl),p.scale(v,tr*ll),
        p.scale(v,p.dot(k,hk)),p.scale(v,p.dot(k,hl)),p.scale(v,p.dot(l,hl)),
        p.scale(hv,kk),p.scale(hv,kl),p.scale(hv,ll),
        p.scale(hk,kv),p.scale(hk,lv),p.scale(hl,kv),p.scale(hl,lv),
        p.scale(k,tr*kv),p.scale(k,tr*lv),p.scale(l,tr*kv),p.scale(l,tr*lv),
        p.scale(k,p.dot(v,hk)),p.scale(k,p.dot(v,hl)),p.scale(l,p.dot(v,hk)),p.scale(l,p.dot(v,hl))]
    return [sum((a*t[i] for a,t in zip(coeff,ts)),p.ZERO) for i in range(4)]
def prediction(hi,vi):
    H=g.BASIS[hi];v=p.axes[vi];k=p.P;l=p.Q
    F=p.add(p.scale(v,-p.QQ(3,8)*p.dot(l,l)),p.scale(l,p.dot(l,v)/4))
    E=p.madd(p.mscale(p.itr(H),p.dot(k,k)),p.mscale(p.itr(p.gauge(k,p.C(H,k))),-1))
    BE=p.madd(p.mscale(E,-p.QQ(1,6)),p.mscale(p.I,-p.trace(E)/12))
    return p.madd(p.madd(p.lie(H,k,l,F),p.mscale(p.gauge(p.add(k,l),Z(H,k,l,v)),-1)),
                  p.mscale(BE,p.dot(p.add(k,p.scale(l,p.QQ(1,2))),v)))
def ev(poly,aa,bb,cc):
    return s.expand(poly.as_expr()).subs(dict(zip(s.symbols('a b c'),(aa,bb,cc))))
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources={str(x):sha(x) for x in [Path(__file__),HERE/'general_marked_engine.py',HERE/'marked_vertex_engine.py',HERE/'marked_polynomial_engine.py',fit]},
    goal='Compute 400 arbitrary h*hc components as exact QQ[a,b,c] polynomials; test candidate without refitting',
    momenta='p=a e0,r=b e0+c e1; arbitrary symmetric H,T and vector v',
    extension='O4 covariance and polynomial continuity; cubic total momentum degree 2',
    full_Q2=False))
start,cpu=perf_counter(),process_time();checks=[];fail=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,ok=bool(ok),detail=detail))
    if not ok:fail.append(checks[-1])
# Independent direct cubic evaluations at a != 1 validate homogeneity reconstruction.
qval=s.Matrix([2,-1,1,3]);subs=dict(zip(s.symbols('q0 q1 q2 q3 a'),list(qval)+[2]))
for hi,ji,ki in [(0,4,9),(1,2,7),(4,0,4),(9,8,1),(5,3,6)]:
    sparse=g.cubic_sparse(hi)[ji][ki].as_expr().subs(subs)
    direct=eh_cubic_16k(tuple(SBASIS[hi]),tuple(2*SAXES[0]),tuple(SBASIS[ji]),tuple(-qval),
                         tuple(SBASIS[ki]),tuple(qval-2*SAXES[0]))
    check('cubic_scaling_'+str((hi,ji,ki)),sparse==direct,dict(sparse=str(sparse),direct=str(direct)))
if fail:
    new(DEST/'FAILED.json',dict(checks=checks));raise SystemExit(2)
for hi,ti,vi,aa,bb,cc in [(0,0,0,2,1,3),(1,4,1,1,-2,1),(4,4,0,1,0,0),(5,6,3,3,2,-1),(9,3,2,2,-1,2)]:
    value,gg,mm=g.vertex(hi,ti,vi)
    direct,dg,dm,*_=marked(SBASIS[ti],SBASIS[hi],aa*SAXES[0],bb*SAXES[0]+cc*SAXES[1],SAXES[vi])
    for label,pol,target in [('R1',value,direct),('G',gg,dg),('M',mm,dm)]:
        got=ev(pol,aa,bb,cc)
        check('engine_'+str((hi,ti,vi,label)),got==target,dict(sparse=str(got),direct=str(target)))
if fail:
    new(DEST/'FAILED.json',dict(checks=checks));raise SystemExit(3)
reference=json.loads((HERE/'constant_ghost_full_basis/results.json').read_bytes())
refs={(x['H'],x['T'],x['v']):s.Rational(x['actual']) for x in reference['cases']}
components=[];constant_mismatches=[];degree_mismatches=[]
for hi in range(10):
    for vi in range(4):
        pred=prediction(hi,vi)
        for ti in range(10):
            value,gg,mm=g.vertex(hi,ti,vi);expected=p.inner(g.BASIS[ti],pred);residue=value-expected
            constant=ev(value,1,0,0)
            if constant!=refs[hi,ti,vi] or ev(residue,1,0,0)!=0:
                constant_mismatches.append([hi,ti,vi,str(constant),str(ev(residue,1,0,0))])
            if any(sum(exps[:4])!=0 or sum(exps[4:])!=3 for exps in value):degree_mismatches.append([hi,ti,vi])
            components.append(dict(H=hi,T=ti,v=vi,R1=str(value.as_expr()),G=str(gg.as_expr()),M=str(mm.as_expr()),
                                   candidate=str(expected.as_expr()),residue=str(residue.as_expr())))
    print(json.dumps(dict(H_completed=hi,components=len(components))),flush=True)
result=dict(statute='DERIVED_PRINCIPAL_VERTEX_QQ_POLYNOMIALS' if not constant_mismatches and not degree_mismatches else 'MEDIDA_VALIDATION_FAILURE',
    checks=checks,components=components,component_count=len(components),constant_mismatches=constant_mismatches,
    degree_mismatches=degree_mismatches,candidate_nonzero_residues=sum(x['residue']!='0' for x in components),
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','components')},ensure_ascii=False))
if constant_mismatches or degree_mismatches:raise SystemExit(4)
