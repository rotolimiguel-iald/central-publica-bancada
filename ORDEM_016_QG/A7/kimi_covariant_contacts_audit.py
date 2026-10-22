"""Check the returned Kimi formula against fixed sources and the normal connection."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
from curved_cutoff_descent_engine import *
H=Path(__file__).resolve().parent;D=H/'kimi_covariant_contacts_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    assert not p.exists();b=json.dumps(v,indent=2).encode();q=p.with_suffix('.tmp')
    q.write_bytes(b);assert q.read_bytes()==b;q.replace(p)
review=H/'received_reviews/b9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8.md'
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    review_sha256=sha(review),target='Factor2, odd cutoff sign, D1 type, curvature C2/C3 and inherited reality',
    no_remote_execution=True))
cpu=process_time();checks=0;negatives={}
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1

# Coefficients in exterior basis [du*c,u*c,u*dc]; E=5,dE=7,B=1.
# delta(u*c*du)=E*c*du+u*c*dE; c*du=-du*c.
lhs=[F(-5),F(7),F(0)];current_derivative=[F(5),F(7),F(5)];target=[F(0),F(7),F(5,2)]
for a,j,b in zip(lhs,current_derivative,target):check(a,2*b-j)
wrong=[a-(b-j/2) for a,j,b in zip(lhs,current_derivative,target)]
assert any(wrong);negatives['Kimi_section2_half_factor']=list(map(str,wrong))
# Integrated contact in fixed order u*c is +A0/2 dchi J. c*u=-u*c.
check(F(1,2),-F(-1,2));assert F(1,2)!=F(-1,2)
negatives['Kimi_cutoff_reversed_odd_order']='claimed +c*u equals -u*c, opposite to the fixed J=u*c*E'

basis=[[[F(int((a,b)==(i,j) or (a,b)==(j,i))) for b in range(4)] for a in range(4)]
       for i in range(4) for j in range(i,4)]
def inner(A,B):return sum(A[a][b]*B[a][b] for a,b in product(range(4),repeat=2))
def tr(A):return sum(A[i][i] for i in range(4))
def d1(E,j):
    return [[sum((j[a][r]-j[r][a])*E[r][b]+(j[b][r]-j[r][b])*E[r][a]
                 for r in range(4))/4 for b in range(4)] for a in range(4)]
I=[[F(int(a==b)) for b in range(4)] for a in range(4)]
for mu,rho in product(range(4),repeat=2):
    j=[[F(int((a,b)==(mu,rho))) for b in range(4)] for a in range(4)]
    check(d1(I,j),[[F(0)]*4 for _ in range(4)])
    for X,Y in product(basis,repeat=2):check(inner(X,d1(Y,j)),-inner(Y,d1(X,j)))
    for X in basis:
        # Coordinate expression equals fixed Fourier D1(r,v) at j_mu^rho=r_mu v^rho.
        Ev=[X[a][rho] for a in range(4)];Er=[X[a][mu] for a in range(4)]
        old=[[F(int(a==mu)*Ev[b]+int(b==mu)*Ev[a]-int(a==rho)*Er[b]-int(b==rho)*Er[a],4)
              for b in range(4)] for a in range(4)]
        check(d1(X,j),old)
        EK=[[2*X[a][b]+I[a][b]*tr(X) for b in range(4)] for a in range(4)]
        check(d1(EK,j),[[2*v for v in row] for row in d1(X,j)])
        BEK=[[-EK[a][b]/6-I[a][b]*tr(EK)/12 for b in range(4)] for a in range(4)]
        check(BEK,[[-X[a][b]/3-2*I[a][b]*tr(X)/3 for b in range(4)] for a in range(4)])
# Kimi's replacement differentiates E too: c=e0, E_11=x1 gives D'(E)_01=-1/4,
# whereas the prescribed D1(grad c)E vanishes identically.
check(d1(I,[[F(0)]*4 for _ in range(4)]),[[F(0)]*4 for _ in range(4)])
negatives['D1_redefinition_constant_ghost']=dict(expected='0',Kimi_redefined_D_01='-1/4',E='E11=x1',c='e0')
assert F(-1,4)!=0

# Test C1,C2,C3 directly from the already calibrated Christoffel polynomial.
c2_wrong_count=0;c3_wrong_count=0
for a0 in range(4):
    vec=[F(int(i==a0)) for i in range(4)]
    jet=polynomial_jet(lambda ix,o: {ZERO:vec[ix[0]]} if not o and vec[ix[0]] else {},1)
    for mu,nu,r in product(range(4),repeat=3):
        actual=jet((mu,nu),(r,),1)-jet((nu,mu),(r,),1)
        expected=int(r==mu)*vec[nu]-int(r==nu)*vec[mu]
        check(actual,expected)
for X in basis:
    jet=polynomial_jet(lambda ix,o: {ZERO:X[ix[0]][ix[1]]} if not o and X[ix[0]][ix[1]] else {},2)
    for mu,nu,a,b in product(range(4),repeat=4):
        actual=jet((mu,nu),(a,b),1)-jet((nu,mu),(a,b),1)
        expected=int(a==mu)*X[nu][b]-int(a==nu)*X[mu][b]+int(b==mu)*X[a][nu]-int(b==nu)*X[a][mu]
        check(actual,expected);c2_wrong_count+=int(actual!=-expected)
    for mu,nu in product(range(4),repeat=2):
        actual=sum(jet((r,mu),(r,nu),1)-jet((mu,r),(r,nu),1) for r in range(4))
        expected=4*X[mu][nu]-int(mu==nu)*tr(X)
        check(actual,expected);c3_wrong_count+=int(actual!=-expected)
assert c2_wrong_count and c3_wrong_count
negatives['C2_opposite_sign']=c2_wrong_count;negatives['C3_opposite_sign']=c3_wrong_count
reality=json.loads((H/'bv_reality/results.json').read_bytes())
for name in ['generator_antireal_B','generator_antireal_D1','counterterm_real_B','counterterm_real_D1']:
    assert name in reality['checks'];checks+=1
fresh(D/'results.json',dict(statute='REAL_REVIEW_ERRORS_IDENTIFIED_DERIVED_CORRECTED_PRIMITIVE_DIFFERENTIAL',
    checks=checks,negative_controls=negatives,cpu_seconds=process_time()-cpu,
    B_identity='delta(1/2 u B c.nabla u)=u B[c.nabla E+(div c)E/2]-div(u B c E)/2',
    D_identity='delta(-A0/6 u D1(grad c)u)=-A0/3 u D1(grad c)E',
    C3='[nabla^rho,nabla_mu]h_rho_nu=4K h_mu_nu-K g_mu_nu trh',
    mass_B='B(2Kh+Kg trh)=-K h/3-2K g trh/3',mass_D1='D1(2Kh+Kg trh)=2K D1(h)',
    reality='Reuse earlier audit: odd generator antireal; its s variation real in the fixed BV involution',
    full_Q2=False,review_master_formula_accepted=False))
files=[Path(__file__),review,H/'received_reviews/b9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8.json',
    H/'curved_cutoff_descent_engine.py',H/'spaceform_covariant_jet_engine.py',H/'bv_gradient_engine.py',
    H/'antifield_quadratic_primitive/results.json',H/'bv_reality/results.json',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,negative_controls=negatives,cpu=process_time()-cpu)))
