"""Free Euler insertion: graph arity and regulator-allocation contact diagnostic."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations,permutations
import hashlib,json,time,uuid
import sympy as s
from logarithmic_contact_engine import residue,Q
from position_metric_bubble_engine import BASIS,LABELS

H=Path(__file__).resolve().parent;D=H/'free_euler_insertion_contact';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Euler insertion acts on a contracted line, not on the complete two-line product',
    prescription='Existing pair R=FP[(1-a)mu^(2a)z^a * product]. Probe split f=z^(tau*a-1),g=z^((1-tau)*a-1) BEFORE Euler differentiation.',
    parameter='tau is a diagnostic allocation, not a new model parameter or adopted normalization',
    normalization='All polynomial contacts divided by CE=-4*pi^2 as in existing residue engine',
    scope='Free full (h,b) inverse plus scalar simple-pole collapsed-line contacts and graph counts; no full WZ sum',
    script_sha256=sha(Path(__file__)),sources=[dict(path=str(p),sha256=sha(p)) for p in [H/'mixed_b_h_current_check_v3.py',H/'logarithmic_contact_engine.py']]))
start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert s.cancel(a-b)==0,(a,b);checks+=1
p=s.symbols('p0:4');kap=s.symbols('kappa',nonzero=True);pp=sum(v*v for v in p)
gram=s.diag(*[1 if i==j else 2 for i,j in LABELS]);tr=s.Matrix([int(i==j) for i,j in LABELS])
itr=s.eye(10)-tr*tr.T/2;S=itr*gram.inv()
G=s.Matrix(10,4,lambda A,r:p[LABELS[A][0]]*int(LABELS[A][1]==r)+p[LABELS[A][1]]*int(LABELS[A][0]==r))
C=s.Matrix(4,10,lambda r,A:sum(p[m]*BASIS[A][4*m+r] for m in range(4))-p[r]*sum(BASIS[A][4*i+i] for i in range(4))/2)
E=-pp*itr+itr*G*C;Hp=gram*E/(4*kap)
metric=(Hp*(-4*kap*S)).applyfunc(s.expand)
auxiliary=(C.T*G.T).applyfunc(s.expand)
for i in range(10):
    for j in range(10):eq(metric[i,j]+auxiliary[i,j],pp*int(i==j))
omitted=(metric-pp*s.eye(10)).applyfunc(s.expand)
assert omitted!=s.zeros(10);checks+=1
# This is a polynomial identity for any scalar kernel: no use of box f=0.
for v in Hp*G:eq(v,0)
for v in -4*kap*C*S+2*kap*G.T:eq(v,0)

a,tau,z=s.symbols('a tau z');q2=sum(q*q for q in Q)
signature=(1,1,1,1)
def finite(coefficient,n,powers=(0,0,0,0)):
    # Kernels in this check vanish to at least order a, so only their simple pole contributes.
    assert s.expand(coefficient).subs(a,0)==0
    return s.expand(s.diff(coefficient,a).subs(a,0)*residue(n,powers,signature))
def radial_box(f):return s.expand(4*z*s.diff(f,z,2)+8*s.diff(f,z))
f=z**(tau*a-1);g=z**((1-tau)*a-1)
box_coefficient=4*tau*a*(tau*a-1)
eq(s.simplify(radial_box(f)/z**(tau*a-2)),box_coefficient)
left=finite(box_coefficient,3)
right=finite(4*(1-tau)*a*((1-tau)*a-1),3)
eq(left,tau*q2/8);eq(right,(1-tau)*q2/8)
eq(left+right,q2/8)
eq(left.subs(tau,0),0);eq(left.subs(tau,1),q2/8)
eq(left.subs(tau,s.Rational(1,2)),q2/16)
rows=[]
for j in range(4):
    powers=tuple(int(i==j) for i in range(4))
    # Euler first, then derivative on the second internal line.
    on_second=finite(box_coefficient*2*((1-tau)*a-1),4,powers)
    # Derivative on Euler line; the two terms sum to total derivative after extension.
    on_first=finite(box_coefficient*2*(tau*a-2),4,powers)
    eq(on_second,tau*Q[j]*q2/24)
    eq(on_first,tau*Q[j]*q2/12)
    eq(on_first+on_second,Q[j]*left)
    assert s.expand(on_second-Q[j]*left)!=0;checks+=1
    rows.append(dict(j=j,derivative_on_ghost=str(on_second),derivative_on_euler=str(on_first)))

# Arity only, independent of derivative labels or graded signs.
def allowed(u,v):return (u,v) in [('h','h'),('h','b'),('b','h'),('c','barc'),('barc','c')]
def matchings(left,right,n):
    out=[]
    for ii in combinations(range(len(left)),n):
        for jj in permutations(range(len(right)),n):
            if all(allowed(left[i],right[j]) for i,j in zip(ii,jj)):
                out.append(dict(edges=list(zip(ii,jj)),
                    external_left=[left[i] for i in range(len(left)) if i not in ii],
                    external_right=[right[j] for j in range(len(right)) if j not in jj]))
    return out
vertex=['barc','h','c']
antifield_current=matchings(['hdagger','c','c'],vertex,2)
assert not antifield_current;checks+=1
euler_graphs={t:matchings([t,'c','c'],vertex,2) for t in ['h','b']}
for t,graphs in euler_graphs.items():
    assert len(graphs)==2;checks+=1
    for graph in graphs:
        assert graph['external_left']==['c'] and graph['external_right']==['c'];checks+=1
af_vertex=matchings(['hdagger','h','c'],vertex,2)
assert len(af_vertex)==1 and af_vertex[0]['external_left']==['hdagger'];checks+=1

result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    free_euler_identity='P_hh N_hh + P_hb N_bh = box*I_10, for arbitrary scalar kernel; auxiliary contribution cannot be omitted',
    scalar_contacts=dict(euler_first=str(left),euler_second=str(right),sum=str(s.expand(left+right)),derivatives=rows),
    pair_extension_unchanged='z^(tau*a-1)*z^((1-tau)*a-1)=z^(a-2) for z>0; allocation affects insertion differentiated before multiplication',
    conclusion='Ordinary pair finite part does not by itself specify the time-ordered free-Euler composite insertion. Need an explicit compatible EOM normalization; no allocation selected here.',
    graphs=dict(antifield_current_two_line=antifield_current,euler_current_two_line=euler_graphs,antifield_vertex_two_line=af_vertex),
    not_claimed=['No graded Wick weights computed by the arity enumerator','No gravitational WZ defect canceled','No distributional delta*f multiplication defined','No Lorentzian continuation'],
    full_Q2=False,gate_changed=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(v),sha256=sha(v)) for v in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
