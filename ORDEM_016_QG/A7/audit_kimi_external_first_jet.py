"""Independent exact audit of the received specification, no production edits."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product, permutations
from fractions import Fraction as F
import hashlib, json, time, uuid
import sympy as s
import ghost_direct_position_engine as G
from position_metric_bubble_engine import LABELS, BASIS

H=Path(__file__).resolve().parent
D=H/'kimi_external_first_jet_review'/'local_audit'
D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists()
    raw=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw)
    assert t.read_bytes()==raw;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    response_sha256=sha(D.parent/'RESPONSE.md'),script_sha256=sha(Path(__file__)),
    tests=['Forty derivative ghost channels against existing W1',
           'T10 API counterexample; C3 multiplicity counterexample; Y sign',
           'delta/r tensor pattern enumeration, exact span polynomial identities',
           'moving frame pairing and arbitrary external second-jet control'],
    full_Q2=False,production_changes=False))
start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert a==b,(a,b);checks+=1

for rho in range(4):
    for k,(a,b) in enumerate(LABELS):
        expected=G.empty(20)
        for mu in range(4):
            for nu in range(4):
                v=-F(int((min(mu,nu),max(mu,nu))==(a,b)))
                v+=F(1,2)*int(mu==nu)*int(a==b)
                if v:expected[rho][4*(mu+1)+nu]=v
        actual=G.vertex(BASIS[k])[1][rho]
        eq(actual,expected);assert any(actual)
eq(len(LABELS)+4*len(LABELS),50)
try:G.vertex(tuple([0]*10))
except IndexError:checks+=1;api='IndexError: vertex requires 16 flattened matrix entries'
else:raise AssertionError('Expected T10 API failure')
# C3 as printed, already falsified for a linear functional with val(T01)=1.
c3_left=F(2)*F(1)/2
c3_right=F(2)*F(1,2)+F(2)*F(1,2)
eq(c3_left,1);eq(c3_right,2);assert c3_left!=c3_right

r=s.symbols('r0:4');d=lambda a,b:s.Integer(a==b)
def A(i,j,k):return [d(j,k)*r[i],d(i,j)*r[k]+d(i,k)*r[j],r[i]*r[j]*r[k]]
def B(i,c,j,k):return [d(i,c)*d(j,k),d(i,j)*d(c,k)+d(i,k)*d(c,j),
    d(j,k)*r[i]*r[c],d(i,c)*r[j]*r[k],
    (d(i,j)*r[k]+d(i,k)*r[j])*r[c],
    (d(c,j)*r[k]+d(c,k)*r[j])*r[i],r[i]*r[c]*r[j]*r[k]]
def M(a,b,c,e):return [d(a,b)*d(c,e),d(a,c)*d(b,e)+d(a,e)*d(b,c),
    d(a,b)*r[c]*r[e],r[a]*r[b]*d(c,e),
    (d(a,c)*r[b]+d(b,c)*r[a])*r[e]+(d(a,e)*r[b]+d(b,e)*r[a])*r[c],
    r[a]*r[b]*r[c]*r[e]]
def Ms(*idx):
    v=M(*idx);return [v[0],v[1],v[2]+v[3],v[4],v[5]]
def patterns(slots):
    if not slots:yield ((),());return
    first,*tail=slots
    for pairs,singles in patterns(tail):yield pairs,(first,)+singles
    for other in tail:
        rem=[i for i in tail if i!=other]
        for pairs,singles in patterns(rem):yield ((first,other),)+pairs,singles
def pattern_value(pat,idx):
    pairs,singles=pat
    return s.prod(d(idx[i],idx[j]) for i,j in pairs)*s.prod(r[idx[i]] for i in singles)
swaplast=[(0,1,2),(0,2,1)]
bsym=[(0,1,2,3),(0,1,3,2)]
msym=[(0,1,2,3),(1,0,2,3),(0,1,3,2),(1,0,3,2)]
fullsym=msym+[(p[2],p[3],p[0],p[1]) for p in msym]
point=dict(zip(r,[1,2,-1,1]));bases=[]
for name,n,fun,group,want in [('A',3,A,swaplast,3),('B',4,B,bsym,7),('M',4,M,msym,6),('M_pair_exchange',4,Ms,fullsym,5)]:
    indices=list(product(range(4),repeat=n))
    expr=s.Matrix([fun(*idx) for idx in indices]);numeric=expr.subs(point)
    eq(numeric.rank(),want)
    coeffs=[];pats=list(patterns(list(range(n))))
    for pat in pats:
        target=s.Matrix([s.expand(sum(pattern_value(pat,tuple(idx[i] for i in p)) for p in group)/s.Integer(len(group))) for idx in indices])
        sol,params=numeric.gauss_jordan_solve(target.subs(point))
        eq(params.rows,0)
        # This, rather than the evaluation fit, verifies the global polynomial identity.
        eq([s.expand(v) for v in expr*sol-target],[s.Integer(0)]*len(indices))
        coeffs.append([str(v) for v in sol])
    bases.append(dict(name=name,rank=want,patterns=len(pats),coefficients=coeffs,
        statement='Exact symbolic span for delta/r-built tensors with the stated index symmetries'))

y=s.symbols('Y0:4');X=s.symbols('X0:4');z=sum((a-b)**2 for a,b in zip(X,y))
for i in range(4):eq(s.expand(s.diff(z,y[i])+2*(X[i]-y[i])),0)
t=s.symbols('t');P=s.Matrix([[1,t],[0,1]]);T=s.Matrix([[1,2],[3,4]]);O=s.Matrix([[2,0],[1,-1]])
both=s.expand(s.trace(P.inv()*T*P*P.inv()*O*P));base=s.trace(T*O)
eq(both,base)
one=s.expand(s.trace(P.inv()*T*P*O)-base)
assert one!=0;checks+=1
# Ricci-flat background does not fix arbitrary external h second jets.
h=y[0]**2;origin={a:0 for a in y}
eq(h.subs(origin),0)
for a in y:eq(s.diff(h,a).subs(origin),0)
eq(s.diff(h,y[0],2),2)

result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    ghost_derivative_channels=40,jet_dimension=50,api_counterexample=api,
    multiplicity_C3=dict(left=str(c3_left),right=str(c3_right),verdict='REFUTED'),
    basis_results=bases,Y_derivative='partial_Y z=-2(X-Y), opposite to response section4.1',
    moving_frame=dict(pairing=str(base),consistent_pairing=str(both),one_sided_change=str(one)),
    second_jet='h11=Y0^2 in a flat background has h=Dh=0 at origin but d00h11=2',
    limits='Span conditional on delta/r-built ansatz; no full operator fit, no new curved Ward proof, no Q2',
    production_changes=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [
    Path(__file__),D.parent/'RESPONSE.md',H/'ghost_direct_position_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='basis_results'},ensure_ascii=False))
