"""Curvature commutators and independent coordinate Euler/IBP check."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
H=Path(__file__).resolve().parent;D=H/'bilocal_covariant_jets_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_covariant_jet_engine.py',H/'bilocal_first_curvature_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Covariant Y jets before anchoring and Ward divergence versus coordinate Euler variation',
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();checks=[];negative=[]
def ck(n,v):
    value=E.anchor(v);assert value==0,(n,value);checks.append(n)
def R(c,b,i,j):return B.d(c,i)*B.d(b,j)-B.d(c,j)*B.d(b,i)
for kind,inds in [('ghost',[(a,b) for a in range(4) for b in range(4)]),
                  ('metric',[(a,b,c,d) for a in range(4) for b in range(a,4) for c in range(4) for d in range(c,4)])]:
    for indices in inds:
        slots=(1,) if kind=='ghost' else (2,3)
        for i,j in [(0,1),(1,3)]:
            actual=E.yjet(kind,1,indices,(i,j))-E.yjet(kind,1,indices,(j,i))
            expected=0
            for pos in slots:
                for c in range(4):
                    ids=indices[:pos]+(c,)+indices[pos+1:]
                    expected-=R(c,indices[pos],i,j)*E.raw(kind,0,ids)
            ck(f'Ycomm_{kind}_{indices}_{i}_{j}',actual-expected)
    print(kind,'commutators_checked',len(checks),flush=True)

# Independent Euler expression: expand the actual covariant derivatives of
# c inside the weak pairing, retain sqrt(g), then integrate coordinate jets.
y=B.y;K=s.Symbol('K');volume=1-K*sum(t*t for t in y)/2
def trunc(f):return s.expand(f).coeff(K,0)+K*s.expand(f).coeff(K,1)
def b0(o,a,b):
    return s.Integer((a+1)*(b+1)+(o+1))*(1+y[(a+b)%4]+y[a]*y[b])
def b1(o,j,a,b):
    return s.Integer((j+1)*(a+b+2)+o+1)*(1+y[j]+y[a]*y[b])
expected=E.coordinate_yward(b0,b1)
def W0(a,b):return b0(0,a,b)+K*b0(1,a,b)
def W1(j,a,b):return b1(0,j,a,b)+K*b1(1,j,a,b)
for b in range(4):
    # Coefficients of c_b, partial_i c_b, partial_i partial_j c_b.
    c0=0;c1=[s.Integer(0)]*4;c2=[[s.Integer(0) for _ in range(4)] for _ in range(4)]
    for a in range(4):
        c1[a]+=2*W0(a,b)
        for r in range(4):
            c0-=2*K*W0(a,r)*E.gamma(y,b,a,r)
        for j in range(4):
            c2[j][a]+=2*W1(j,a,b)
            for r in range(4):
                c0-=2*K*W1(j,a,r)*s.diff(E.gamma(y,b,a,r),y[j])
                c1[j]-=2*K*W1(j,a,r)*E.gamma(y,b,a,r)
                c1[r]-=2*K*W1(j,a,b)*E.gamma(y,r,j,a)
                c1[a]-=2*K*W1(j,a,r)*E.gamma(y,b,j,r)
    euler=trunc(volume*c0)
    for i in range(4):
        euler-=s.diff(trunc(volume*c1[i]),y[i])
        for j in range(4):euler+=s.diff(trunc(volume*c2[i][j]),y[i],y[j])
    for o in (0,1):ck(f'weak_Euler_{o}_{b}',s.expand(euler).coeff(K,o)-expected[o][b])
    naive=0
    for a in range(4):
        naive-=B.derivative(b0(1,a,b),'Y',a)
        for j in range(4):naive+=B.derivative(B.derivative(b1(1,j,a,b),'Y',j),'Y',a)
    diff=E.anchor(expected[1][b]-2*naive)
    assert diff!=0
    negative.append(dict(name=f'omit_connection_derivatives_{b}',residual=str(diff)))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='BILOCAL_Y_COMMUTATORS_AND_WARD_IBP_CHECKED',
    checks=len(checks),check_names=checks,negative_controls=negative,cpu_seconds=time.process_time()-cpu,
    full_Q2=False,actual_loop_vertices_inserted=False,
    scope='Covariant derivative engine and generic pairing reduction; explicit rational polynomial test fields')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'}))
