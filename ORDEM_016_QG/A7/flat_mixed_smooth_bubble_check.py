"""Compute constant-smooth mixed bubble extension contacts from existing vertices.

Only the flat, coincident isotropic smooth jets; no adjusted normalization.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from functools import lru_cache
import hashlib,json,time,uuid
import sympy as s
import position_metric_ordered_operator_engine as M
import ghost_direct_position_engine as G
from position_metric_bubble_engine import empty,lincomb,frob,sandwich,transpose,LABELS,BASIS
H=Path(__file__).resolve().parent;D=H/'flat_mixed_smooth_bubble';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists(),p
    raw=json.dumps(obj,indent=2).encode();tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
inputs=[Path(__file__),H/'position_metric_ordered_operator_engine.py',
        H/'ghost_direct_position_engine.py',H/'position_metric_bubble_engine.py',
        H/'smooth_source_contact/results.json',H/'smooth_reference_transport_audit/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Finite contact shift of flat mixed singular/smooth h-h bubbles in the fixed radial extension',
    fixed_input='R(partial_Xi partial_Yj z^-1)-partial_Xi partial_Yj z^-1=+C_E delta_ij delta/4',
    normalization='same contraction metric /16 and combined -metric/2+ghost as bilocal calculation',
    sectors=['metric W_I','metric W_T','ghost W_G=I'],
    convention='real derivative symbols: external q=-p gives -p_i p_j after contact pairing',
    comparison='N G+E R_W, preserving original source sign; no fitting to cancellation',
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],
    exclusions=['W derivatives','curvature','other local diagrams','full Q2']))
cpu=time.process_time();checks=[];records={}
def delta(a,b):return int(a==b)
def inner(A,B):return sum(a*b for a,b in zip(A,B))
def tr(A):return sum(A[4*i+i] for i in range(4))
def matrix(A):return s.Matrix(4,4,A)
def invs(A,B,p):
    A=matrix(A);B=matrix(B);v=s.Matrix(p);p2=v.dot(v)
    return [p2*s.trace(A*B),p2*s.trace(A)*s.trace(B),
            (v.T*A*v)[0]*s.trace(B)+(v.T*B*v)[0]*s.trace(A),(v.T*A*B*v)[0]]
@lru_cache(None)
def vertex(kind,A):return M.vertex_data(A) if kind=='metric' else G.vertex(A)

def contact_matrices(sector):
    metric=sector.startswith('metric');n=10 if metric else 4;size=5*n
    smooth=empty(size);contact=empty(size)
    for a in range(n):
        for b in range(n):
            if metric:
                i,j=LABELS[a];k,l=LABELS[b]
                identity=F(delta(i,k)*delta(j,l)+delta(i,l)*delta(j,k),2)
                trace=delta(i,j)*delta(k,l)
                fiber=identity-F(trace,2)
                w=identity if sector=='metric_I' else trace
            else:fiber=delta(a,b);w=fiber
            if w:smooth[a][b]=w
            for i in range(4):
                if fiber:contact[n*(i+1)+a][n*(i+1)+b]=F(fiber,4)
    return smooth,contact

for sector in ['metric_I','metric_T','ghost_I']:
    kind='metric' if sector.startswith('metric') else 'ghost';metric=kind=='metric'
    W,J=contact_matrices(sector)
    factor=F(-1,32) if metric else F(1)
    @lru_cache(None)
    def bilinear(A,B,p):
        ax=vertex(kind,A);by=vertex(kind,B)
        A1=lincomb(*[(p[i],ax[1][i]) for i in range(4)])
        B1=lincomb(*[(-p[i],by[1][i]) for i in range(4)])
        if not metric:B1=transpose(B1)
        return factor*(frob(sandwich(J,A1,W),B1)+frob(sandwich(W,A1,J),B1))
    # Terms with an undifferentiated external field must not be silently lost.
    for A in BASIS:
        ax=vertex(kind,A)[0]
        mixed=lincomb((1,sandwich(J,ax,W)),(1,sandwich(W,ax,J)))
        assert all(not row for row in mixed),(sector,'nonzero undifferentiated external slot')
        checks.append((sector,'external_undifferentiated_zero'))
    p0=(1,0,0,0)
    rows=[invs(A,B,p0) for A in BASIS for B in BASIS]
    rhs=[s.Rational(bilinear(A,B,p0)) for A in BASIS for B in BASIS]
    sol,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix(rhs));assert len(params)==0
    for i,(row,value) in enumerate(zip(rows,rhs)):
        assert s.expand(sum(a*b for a,b in zip(row,sol))-value)==0
        checks.append((sector,'fiber',i))
    # Held-out nonaxial momenta and dense symmetric fibers.
    A=(2,1,-1,3,1,0,2,-2,-1,2,1,0,3,-2,0,-1)
    B=(0,2,0,-1,2,1,3,0,0,3,-2,1,-1,0,1,4)
    for p in [(1,2,-1,1),(2,-1,0,3)]:
        actual=bilinear(A,B,p);expected=sum(a*b for a,b in zip(invs(A,B,p),sol))
        assert actual==expected,(sector,p,actual,expected)
        checks.append((sector,'nonaxial',p))
    records[sector]=dict(coefficients=list(map(str,sol)))
    print('MIXED',sector,list(map(str,sol)),'cpu',time.process_time()-cpu,flush=True)

# Reconstruct N and compare source in the common real-derivative convention.
p=s.Matrix(s.symbols('p0:4'));I=s.eye(4);p2=p.dot(p)
def gauge(v):return p*v.T+v*p.T
def einstein(h):
    c=h*p-p*s.trace(h)/2
    return -p2*h+I*p2*s.trace(h)/2+p*c.T+c*p.T-I*p.dot(c)
for sector,record in records.items():
    a,b,c,d=map(s.Rational,record['coefficients'])
    def N(h):return a*p2*h+b*p2*s.trace(h)*I+c*(p*p.T*s.trace(h)+I*(p.T*h*p)[0])+d*(p*(h*p).T+(h*p)*p.T)/2
    if sector=='metric_I':la,lb=-s.Rational(1,2),-s.Rational(1,8)
    elif sector=='metric_T':la,lb=-s.Rational(1,2),s.Rational(1,4)
    else:la=lb=s.S.Zero
    def L(h):return la*h+lb*I*s.trace(h)
    residual=[]
    for r in range(4):
        g=gauge(I[:,r]);value=N(g)+einstein(L(g))
        for i in range(4):
            for j in range(4):
                v=s.expand(value[i,j])
                if v!=0:residual.append(dict(r=r,i=i,j=j,value=str(v)))
    record['Ward_NG_plus_ER_nonzero_components']=residual
    record['Ward_contact_cancels_with_source']=not residual
result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='FLAT_CONSTANT_SMOOTH_MIXED_BUBBLE_CONTACTS_MEASURED',
    checks=len(checks),cpu_seconds=time.process_time()-cpu,sectors=records,
    invariant_basis=['p²trAB','p²trA trB','pAp trB+pBp trA','pABp'],
    units='over C_E, common propagator prefactors stripped; real derivative symbols',
    covariance='Isotropic W, invariant vertex contractions; held-out dense/nonaxial evaluations',
    normalization_adjusted=False,full_Q2=False,
    limitation='Contact shift versus a derivative-defined reference; excludes W derivatives/curvature/tadpoles/other arities')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
