"""Check the full free inverse and the ordered localized mixed-current insertion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from fractions import Fraction as F
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion,current_terms
from position_metric_bubble_engine import BASIS,LABELS
from metric_principal_vertices import eh_quadratic_8k
from full_loop_extension_engine import x,z,Q,dx

H=Path(__file__).resolve().parent;D=H/'mixed_b_h_current_v3';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw)
    assert t.read_bytes()==raw;t.replace(p)
source=H.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'mixed_b_h_current_engine_v3.py',source]],
    targets=['Two-sided 14x14 bosonic inverse, arbitrary derivative symbols and kappa',
             'Raw EH normalization at two independent exact momenta',
             'Current jet polynomial against direct Lie derivative',
             'Ordered mixed-current contraction rational vs symbolic; extension'],
    diagram_symmetry_factor='NOT_INSERTED',Q2=False))
start=time.process_time();checks=0
def eq(a,b=0):
    global checks
    if isinstance(a,s.MatrixBase):assert all(s.cancel(v)==0 for v in a-b)
    else:assert s.cancel(a-b)==0,(a,b,s.cancel(a-b))
    checks+=1

p=s.symbols('p0:4');kappa=s.symbols('kappa',nonzero=True);pp=sum(t*t for t in p)
gram=s.diag(*[1 if a==b else 2 for a,b in LABELS]);tr=s.Matrix([int(a==b) for a,b in LABELS])
itr=s.eye(10)-tr*tr.T/2;S=itr*gram.inv()
G=s.Matrix(10,4,lambda a,nu:p[LABELS[a][0]]*int(LABELS[a][1]==nu)+p[LABELS[a][1]]*int(LABELS[a][0]==nu))
C=s.Matrix(4,10,lambda nu,a:sum(p[mu]*BASIS[a][4*mu+nu] for mu in range(4))-p[nu]*sum(BASIS[a][4*i+i] for i in range(4))/2)
E=-pp*itr+itr*G*C;Hp=gram*E/(4*kappa)
P=Hp.row_join(-C.T).col_join(C.row_join(-2*kappa*s.eye(4)))
inverse_numerator=(-4*kappa*S).row_join(G).col_join((-G.T).row_join(s.zeros(4)))
eq(C*G,pp*s.eye(4));eq(E*G,s.zeros(10,4));eq(C*S,G.T/2)
eq(P*inverse_numerator,pp*s.eye(14));eq(inverse_numerator*P,pp*s.eye(14))
# p is a real differential symbol above. Raw vertices use a Fourier pair p,-p.
for point in [(1,2,-1,1),(2,-1,3,1)]:
    en=(gram*E).subs(dict(zip(p,point)))
    for a,A in enumerate(BASIS):
        for b,B in enumerate(BASIS):eq(eh_quadratic_8k(A,point,B,tuple(-v for v in point)),-2*en[a,b])

mom=s.symbols('u0:4');kmom=s.symbols('v0:4');eta=(1,2,-1,1)
for r in range(4):
    terms=current_terms(r,eta)
    for nu in range(4):
        for a,A in enumerate(BASIS):
            h=lambda i,j:A[4*i+j]
            direct=sum(eta[mu]*(mom[r]*h(mu,nu)+kmom[mu]*h(r,nu)+kmom[nu]*h(mu,r)
                -s.Rational(mu==nu,2)*(mom[r]*sum(h(i,i) for i in range(4))+2*sum(h(r,j)*kmom[j] for j in range(4)))) for mu in range(4))
            jet=sum(s.Rational(c)*s.prod(mom[i] for i in pw)*s.prod(kmom[i] for i in kw)
                for (n,b,pw,kw),c in terms.items() if n==nu and b==a)
            eq(s.expand(jet),s.expand(direct))

point=(1,2,-1,1);probe=(2,1,0,0);rows=[]
def ev(f):return f.subs(dict(zip(x,point))).subs(z,sum(t*t for t in point))
for lam,et in [((0,0,0,0),(0,0,0,0)),((0,0,0,0),(1,0,0,0)),((1,-1,0,0),(1,0,0,0))]:
    a=MixedCurrentInsertion(BASIS[LABELS.index((1,1))],0,lam,et)
    b=MixedCurrentInsertion(BASIS[LABELS.index((1,1))],0,lam,et,point)
    for kw in sorted({key[-1] for key in a.terms}):
        for ex in [-1,0,1,2,3]:
            f=a.raw(ex,kw)
            for word in [(),(0,),(1,)]:
                symbolic=f
                for i in word:symbolic=dx(symbolic,i)
                eq(ev(symbolic),b.raw(ex,kw,word))
            eq(b.raw(ex,kw),b.raw(ex,kw,exchange=True))
    kernel=a.off_diagonal();eq(ev(kernel),b.off_diagonal())
    eq(b.off_diagonal(),b.off_diagonal(exchange=True))
    extension=a.extension_contact()
    if not any(et):eq(kernel,0);eq(extension,0)
    else:assert ev(kernel)!=0;checks+=1
    rows.append(dict(lambda_x=lam,eta_y=et,ordered_kernel=str(kernel),
        ordered_at_point=str(ev(kernel)),ordered_contact=str(extension),
        ordered_contact_at_probe=str(extension.subs(dict(zip(Q,probe))))))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    free_inverse='GD=-4kappa S/Q; Ghb=G/Q; Gbh=-G^T/Q; Gbb=0 in real differential symbols with formal adjoints',
    normalization='Negative stored Fourier V3/(16kappa) times GD times Ghb gives +1/4 per ordered contraction relative to GQ scalar',
    exchange='Two ordered contractions equal; do not insert sum and vertex1/2 independently',
    point=point,contact_probe=probe,contact_unit='CE=-4pi²',rows=rows,
    full_Q2=False,scope='Flat auxiliary metric/ghost normalization and single mixed current diagram; no overall Ward weight')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'mixed_b_h_current_engine_v3.py',source,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,cpu_seconds=result['cpu_seconds'],rows=[{k:v for k,v in row.items() if k not in ['ordered_kernel','ordered_contact']} for row in rows])))
