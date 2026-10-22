"""Fit six constant-ghost Z coefficients, preserving the measured bracket.

The proposed quadratic-antifield coefficient B is fixed before fitting.
An inconsistent augmented system is recorded, not repaired by changing R1.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
import marked_polynomial_engine as pe
from marked_vertex_engine import marked,AXES,gauge
HERE=Path(__file__).resolve().parent;DEST=HERE/'constant_ghost_completion';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    raw=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    vertex_sha256=sha(HERE/'marked_vertex_engine.py'),bracket_sha256=sha(HERE/'ghost_bracket_primitive/results.json'),
    target='Find Z homogeneous freedom compatible with R1=-KZ+B[(p.v)E] at l=0 and fixed B1',
    fixed_B='B(A)=-A/6-I trA/12',selection='Seven listed polarizations for6coefficients, then exact bracket coefficient equations',
    failure='Record inconsistent rank and stop this ansatz; no fitted changes to loops or B1'))
start,cpu=perf_counter(),process_time();p=AXES[0];zero=s.zeros(4,1)
def H(i,j):
    h=s.zeros(4);h[i,j]=h[j,i]=1;return h
def E(h):
    C=h*p-p*s.trace(h)/2
    return p.dot(p)*(h-s.eye(4)*s.trace(h)/2)-(p*C.T+C*p.T-s.eye(4)*p.dot(C))
def terms(h,v):
    return [v*s.trace(h)*p.dot(p),v*(p.dot(h*p)),h*v*p.dot(p),h*p*p.dot(v),p*s.trace(h)*p.dot(v),p*v.dot(h*p)]
# (metric H, ghost v, source T), one extra equation is an overdetermination check.
spec=[(H(1,1),AXES[0],H(0,0)),(H(2,2),AXES[1],H(0,1)),
      (H(1,1),AXES[1],H(0,1)),(H(0,0),AXES[1],H(0,1)),
      (H(0,1),AXES[0],H(0,1)),(H(0,1),AXES[1],H(0,0)),
      (H(0,0),AXES[0],H(0,0))]
rows=[];rhs=[];samples=[]
for hi,(h,v,T) in enumerate(spec):
    actual,*_=marked(T,h,p,zero,v)
    eh=E(h);bv=p.dot(v)*(-eh/6-s.eye(4)*s.trace(eh)/12)
    rows.append([-s.trace(T*gauge(p,z)) for z in terms(h,v)])
    rhs.append(actual-s.trace(T*bv))
    samples.append(dict(case=hi,R1=str(actual),BV=str(s.trace(T*bv)),target=str(rhs[-1])))
A=s.Matrix(rows);r=s.Matrix(rhs);rank=A.rank();aug=A.row_join(r).rank()
print(json.dumps(dict(stage='constant',rank=rank,augmented_rank=aug,samples=samples)),flush=True)
result=dict(statute='MEASURED_CONSTANT_GHOST_COMPLETION_SYSTEM',samples=samples,
    constant_rank=rank,constant_augmented_rank=aug,full_Q2=False,gate_changed=False)
if rank==aug:
    sol,params=A.gauss_jordan_solve(r);assert not params
    result['constant_Z_coefficients']=list(map(str,sol))
    # Build the complete bracket equations from its already verified polynomial coefficients.
    def zterms(h,k,l,v):
        hk,hl,hv=pe.mv(h,k),pe.mv(h,l),pe.mv(h,v);tr=pe.trace(h)
        kk,kl,ll=pe.dot(k,k),pe.dot(k,l),pe.dot(l,l);kv,lv=pe.dot(k,v),pe.dot(l,v)
        return ([pe.scale(v,tr*x) for x in (kk,kl,ll)]+
                [pe.scale(v,x) for x in (pe.dot(k,hk),pe.dot(k,hl),pe.dot(l,hl))]+
                [pe.scale(hv,x) for x in (kk,kl,ll)]+
                [pe.scale(hk,kv),pe.scale(hk,lv),pe.scale(hl,kv),pe.scale(hl,lv)]+
                [pe.scale(k,tr*kv),pe.scale(k,tr*lv),pe.scale(l,tr*kv),pe.scale(l,tr*lv)]+
                [pe.scale(k,pe.dot(v,hk)),pe.scale(k,pe.dot(v,hl)),pe.scale(l,pe.dot(v,hk)),pe.scale(l,pe.dot(v,hl))])
    def F(k,v):return pe.add(pe.scale(v,-pe.QQ(3,8)*pe.dot(k,k)),pe.scale(k,pe.dot(k,v)/4))
    def df(p,v,r,w):
        return pe.add(pe.add(pe.bracket(p,F(p,v),r,w),pe.bracket(p,v,r,F(r,w))),
                      pe.scale(F(pe.add(p,r),pe.bracket(p,v,r,w)),-1))
    saved=json.loads((HERE/'ghost_bracket_primitive/results.json').read_bytes())
    tri={(x['v'],x['w'],x['Y']):pe.R.from_expr(s.sympify(x['triangle'])) for x in saved['triangle_basis']}
    M=[];y=[];equations=[]
    for vi,v in enumerate(pe.axes):
        for wi,w in enumerate(pe.axes):
            za=zterms(pe.gauge(pe.P,v),pe.P,pe.Q,w);zb=zterms(pe.gauge(pe.Q,w),pe.Q,pe.P,v)
            cols=[pe.add(x,pe.scale(y,-1)) for x,y in zip(za,zb)];dd=df(pe.P,v,pe.Q,w)
            for n in range(4):
                target=tri[vi,wi,n]-dd[n];cs=[x[n] for x in cols];keys=set(target)
                for x in cs:keys.update(x)
                for key in keys:M.append([s.Rational(x.get(key,0)) for x in cs]);y.append(s.Rational(target.get(key,0)))
                equations.append((target,cs))
    for idx,val in zip([0,3,6,9,13,17],sol):
        row=[0]*21;row[idx]=1;M.append(row);y.append(val)
    M=s.Matrix(M);y=s.Matrix(y);rr=M.rank();aa=M.row_join(y).rank()
    result.update(bracket_combined_rank=rr,bracket_combined_augmented_rank=aa)
    if rr==aa:
        x,pars=M.gauss_jordan_solve(y);x=[s.cancel(v.subs({p:0 for p in pars})) for v in x]
        coeff=[pe.QQ(int(v.p),int(v.q)) for v in x]
        assert all(target==sum((c*z for c,z in zip(coeff,cs)),pe.ZERO) for target,cs in equations)
        assert A*sol==r
        result.update(full_Z_coefficients=list(map(str,x)),remaining_free_parameters=len(pars),
                      symbolic_bracket_checks=len(equations),statute='DERIVED_BRACKET_COMPATIBLE_Z_MATCHES_SELECTED_CONSTANT_GHOST_COMPONENTS')
    else:result['statute']='MEDIDA_FIXED_B_AND_BRACKET_CONSTANT_GHOST_CONDITIONS_INCONSISTENT'
else:result['statute']='MEDIDA_CONSTANT_GHOST_FIXED_B_ANSATZ_INCONSISTENT'
result.update(cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False))
