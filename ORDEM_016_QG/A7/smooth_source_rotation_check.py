"""Exhaustive algebraic W-source contraction and rotation/strain separation."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'smooth_source_rotation';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists(),p
    raw=json.dumps(obj,indent=2).encode();tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
inputs=[Path(__file__),H/'smooth_source_contact_check.py',H/'smooth_reference_transport_audit/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='General coincident W contraction in original source vertex; exact strain plus rotation decomposition',
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs],
    excluded=['physical state construction','derivatives of W','curved full loop','full Q2']))
cpu=time.process_time();checks=0
def ck(x,y=0):
    global checks
    value=s.expand(x-y) if isinstance(x,s.Basic) or isinstance(y,s.Basic) else x-y
    assert value==0,value;checks+=1
labels=[(a,b) for a in range(4) for b in range(a,4)]
ix={x:i for i,x in enumerate(labels)}
wlabels=[(i,j) for i in range(10) for j in range(i,10)]
for wi,(left,right) in enumerate(wlabels):
    def w(a,b,c,d):
        i,j=sorted((ix[tuple(sorted((a,b)))],ix[tuple(sorted((c,d)))]))
        return int((i,j)==(left,right))
    S=[[sum(w(a,m,r,m) for m in range(4)) for r in range(4)] for a in range(4)]
    def r(a,b,j,c):
        return -F(int(j==b)*S[a][c]+int(j==a)*S[b][c]
                  +w(a,j,b,c)+w(b,j,a,c)-2*w(a,b,j,c),4)
    for a,b in labels:
        slots=[(a,b)] if a==b else [(a,b),(b,a)]
        for j in range(4):
            for c in range(4):
                original=-F(1,2)*sum(int(j==v)*w(u,m,c,m)
                    +int(j==m)*w(u,m,v,c)-int(v==m)*w(u,m,j,c)
                    for u,v in slots for m in range(4))
                predicted=sum(r(u,v,j,c) for u,v in slots)
                ck(original,predicted)

# Full symbolic relation, coefficient by coefficient in M_jr=grad_j c_r.
ws=s.symbols('w0:55');wm=dict(zip(wlabels,ws))
def w(a,b,c,d):
    i,j=sorted((ix[tuple(sorted((a,b)))],ix[tuple(sorted((c,d)))]))
    return wm[i,j]
S=s.Matrix(4,4,lambda a,r:sum(w(a,m,r,m) for m in range(4)))
def r(a,b,j,c):
    return -(int(j==b)*S[a,c]+int(j==a)*S[b,c]
             +w(a,j,b,c)+w(b,j,a,c)-2*w(a,b,j,c))/4
def L(A):
    crossed=s.Matrix(4,4,lambda a,b:sum(w(a,j,b,c)*A[j,c] for j in range(4) for c in range(4)))
    direct=s.Matrix(4,4,lambda a,b:sum(w(a,b,j,c)*A[j,c] for j in range(4) for c in range(4)))
    return -(S*A+A*S+2*crossed-2*direct)/8
for j in range(4):
    for c in range(4):
        M=s.zeros(4);M[j,c]=1;G=M+M.T;omega=(M-M.T)/2
        actual=s.Matrix(4,4,lambda a,b:r(a,b,j,c))
        expected=L(G)-(omega*S-S*omega)/4
        for a in range(4):
            for b in range(4):ck(actual[a,b],expected[a,b])

# Lie derivative of a parallel covariant S, retaining rotation as well as strain.
ms=s.symbols('m0:16');M=s.Matrix(4,4,ms);strain=(M+M.T)/2;omega=(M-M.T)/2
lie=M*S+S*M.T
for a in range(4):
    for b in range(4):ck(lie[a,b],(strain*S+S*strain+omega*S-S*omega)[a,b])
control_S=s.diag(1,0,0,0);control_M=s.zeros(4);control_M[1,0]=1
control_omega=(control_M-control_M.T)/2
control=-(control_omega*control_S-control_S*control_omega)[0,1]/4
assert control==-s.Rational(1,8)
result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='GENERAL_W_SOURCE_CONTRACTION_AND_ROTATION_OBSTRUCTION_CHECKED',
    checks=checks,cpu_seconds=time.process_time()-cpu,W_basis_dimension=55,
    original_vertex_checks=55*10*16,
    decomposition='R_W(M)=L_W(M+M^T)-[Omega,S]/4, Omega=(M-M^T)/2, S_ar=sum_m W_am|rm',
    L='L_W(H)=-(S H+H S+2 W_cross(H)-2 W_direct(H))/8',
    Lie_S='Lie_c S at a covariantly constant jet is {strain,S}+[Omega,S]',
    negative_control_omitted_rotation=str(control),
    interpretation='Algebraic field redefinition alone suffices only when S is scalar; anisotropic reference transport must retain rotational data',
    limitation='No assertion that arbitrary algebraic W is an admissible state or that transforming W alone enforces BRST compatibility',
    full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
