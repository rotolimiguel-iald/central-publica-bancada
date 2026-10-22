"""Off-plane direct-loop checks and an independent graded generator check."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
import marked_polynomial_engine as p
import quadratic_metric_engine as a2
import ghost_primitive_engine as z1
import bv_gradient_engine as bv
from marked_vertex_engine import marked
HERE=Path(__file__).resolve().parent;DEST=HERE/'bv_gradient_audit';DEST.mkdir(exist_ok=True)
def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def new(path,o):
    assert not path.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=path.with_name(path.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(path)
fit=HERE/'bv_gradient_fit/results.json';r=json.loads(fit.read_bytes())
base=HERE/'constant_ghost_completion/results.json';z=json.loads(base.read_bytes())
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    fit_sha256=sha(fit),base_sha256=sha(base),
    target='Direct Sympy loops at three fixed non-axis momentum pairs; no refitting. Graded skew-fiber primitive independently.',
    scope='Principal UV coefficient only; not finite causal anomaly'))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def qq(x):x=s.Rational(x);return p.QQ(int(x.p),int(x.q))
ca=list(map(qq,r['A2_coefficients']));cz=[qq(x)+qq(y) for x,y in zip(z['full_Z_coefficients'],r['DeltaZ_coefficients'])]
cd=list(map(qq,r['gradient_coefficients']))
def pv(x):return [p.R.ground_new(qq(v)) for v in x]
def pm(x):return [pv(row) for row in x]
def expr(x):return s.cancel(x.as_expr())
def predict(H,k,l,v):
    F=p.add(p.scale(v,-p.QQ(3,8)*p.dot(l,l)),p.scale(l,p.dot(l,v)/4))
    zs=z1.terms(H,k,l,v);Z=[sum((c*w[j] for c,w in zip(cz,zs)),p.ZERO) for j in range(4)]
    E=bv.einstein(H,k);BE=p.madd(p.mscale(E,-p.QQ(1,6)),p.mscale(p.I,-p.trace(E)/12))
    As,_=a2.terms(H,k,p.gauge(l,v),l);ds=bv.terms(E,l,v)
    correction=[[sum((-2*c*A[i][j] for c,A in zip(ca,As)),p.ZERO) for j in range(4)] for i in range(4)]
    grad=[[sum((c*D[i][j] for c,D in zip(cd,ds)),p.ZERO) for j in range(4)] for i in range(4)]
    pred=p.madd(p.madd(p.lie(H,k,l,F),p.mscale(p.gauge(p.add(k,l),Z),-1)),
         p.mscale(BE,p.dot(p.add(k,p.scale(l,p.QQ(1,2))),v)))
    return p.madd(p.madd(pred,correction),grad),grad
cases=[
 dict(H=[[1,1,0,0],[1,0,0,0],[0,0,2,0],[0,0,0,-1]],T=[[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]],p=[1,2,0,0],r=[-1,0,1,0],v=[1,0,1,-1]),
 dict(H=[[0,0,0,1],[0,1,1,0],[0,1,0,0],[1,0,0,2]],T=[[1,1,0,0],[1,0,0,1],[0,0,-1,0],[0,1,0,0]],p=[1,0,-1,2],r=[0,2,1,1],v=[0,1,-1,2]),
 dict(H=[[2,0,1,0],[0,-1,0,0],[1,0,1,0],[0,0,0,0]],T=[[0,0,0,1],[0,2,0,0],[0,0,1,0],[1,0,0,-1]],p=[0,1,2,-1],r=[2,-1,0,1],v=[2,1,0,-1])]
for ci,case in enumerate(cases):
    H,T,k,l,v=[case[x] for x in ['H','T','p','r','v']]
    pred,grad=predict(pm(H),pv(k),pv(l),pv(v));expected=expr(p.inner(pm(T),pred));gradient=expr(p.inner(pm(T),grad))
    actual,*_=marked(s.Matrix(T),s.Matrix(H),s.Matrix(k),s.Matrix(l),s.Matrix(v))
    assert expected==actual,(ci,expected,actual)
    checks.append(dict(case=ci,actual=str(actual),expected=str(expected),gradient=str(gradient),inputs=case))
    if gradient:
        assert expected-gradient!=actual;neg.append('omit_gradient_'+str(ci))
        assert expected-2*gradient!=actual;neg.append('reverse_gradient_'+str(ci))
    print(json.dumps(dict(case=ci,actual=str(actual),gradient=str(gradient))),flush=True)
# Independent three-dimensional exterior algebra: u_i odd, d odd, E_i even.
E=s.symbols('E0:3');x,y,zs=s.symbols('x y z');C=s.Matrix([[0,x,y],[-x,0,zs],[-y,-zs,0]])
def clean(a):return {k:s.expand(v) for k,v in a.items() if s.expand(v)!=0}
def plus(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,0)+v
    return clean(out)
def mono(seq,coefficient):
    if len(set(seq))!=len(seq):return {}
    sign=(-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))
    return {tuple(sorted(seq)):coefficient*sign}
def delta(a,graded=True):
    out={}
    for seq,coef in a.items():
        for n,t in enumerate(seq):
            if t<3:out=plus(out,{seq[:n]+seq[n+1:]:coef*E[t]*((-1)**n if graded else 1)})
    return out
psi={};target={}
for i in range(3):
    for j in range(3):
        psi=plus(psi,mono((i,3,j),C[i,j]/2));target=plus(target,mono((i,3),C[i,j]*E[j]))
assert delta(psi)==target and not delta(delta(psi))
assert delta(psi,graded=False)!=target;neg.append('ordinary_instead_of_graded_derivative')
assert all(len(k)==3 for k in psi) and all(len(k)==2 for k in target)
result=dict(statute='DERIVED_PRINCIPAL_BV_COMPLETION_AUDITED_OFF_PLANE',cases=checks,
    direct_loop_checks=len(checks),graded_checks=3,negative_controls=neg,
    graded_identity='delta(1/2 u_A C_AB d u_B)=u_A C_AB d E_B, C^T=-C,delta u=E',
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False))
