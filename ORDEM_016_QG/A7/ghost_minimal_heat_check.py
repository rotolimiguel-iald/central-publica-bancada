"""Audit a fixed-background ghost reduction, without varying the background."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
from ghost_minimal_heat_engine import *
HOM=Path(__file__).resolve().parent;DEST=HOM/'ghost_minimal_heat';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,v):
    raw=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 script_sha256=sha(Path(__file__)),engine_sha256=sha(HOM/'ghost_minimal_heat_engine.py'),
 flat_result_sha256=sha(HOM/'ghost_bubble/results.json'),
 scope='Fixed-background C_g Lie_c(g+h); minimalization by left multiplication only; local log heat trace, not finite determinant',
 acceptance=['Recover original full vertex as symbolic polynomial',
 'Recover all five prior flat bubble coefficients and 55 polarizations without fitting a normalization',
 'Check explicit curvature commutators for the reduced zeroth coefficient',
 'Keep logarithmic trace cyclicity and local heat classification as analytic assumptions, not CAS claims'],
 backgrounds_not_varied=True,full_Q2=False,gate_changed=False))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,e):
    good=all(s.expand(v)==0 for v in e) if isinstance(e,s.MatrixBase) else s.expand(e)==0
    assert good,(name,e);checks.append(name)
def reject(name,e):
    assert s.simplify(e)!=0,(name,e);neg.append(dict(name=name,value=str(s.factor(e))))
hs=s.symbols('h0:10');labels=[(a,b) for a in range(4) for b in range(a,4)]
H=s.zeros(4)
for a,(i,j) in enumerate(labels):H[i,j]=H[j,i]=hs[a]
p=s.Matrix(s.symbols('p0:4'));k=s.Matrix(s.symbols('k0:4'))
check('full_symbolic_vertex_not_just_principal',vertex_reduced(H,p,k)-vertex_direct(H,p,k))
AA=first_order(H,p);B=zeroth_order(H,p)
check('flat_divergence_A_equals_B_plus_boxH',sum((s.I*p[i]*AA[i] for i in range(4)),s.zeros(4))-B+p.dot(p)*H)

# R^a_bmn = K(delta_am delta_bn - delta_an delta_bm), used independently
# on each covariant h index and on the contravariant ghost index.
K=s.symbols('K');dd=lambda a,b:s.Integer(a==b)
R=lambda a,b,m,n:K*(dd(a,m)*dd(b,n)-dd(a,n)*dd(b,m))
for nu in range(4):
 for rho in range(4):
    ch=sum(-R(a,mu,mu,rho)*H[a,nu]-R(a,nu,mu,rho)*H[mu,a]
           for mu in range(4) for a in range(4))
    cv=sum(H[mu,a]*R(a,rho,mu,nu) for mu in range(4) for a in range(4))
    check(f'hessian_commutator_h_{nu}_{rho}',ch-4*K*H[rho,nu]+K*s.trace(H)*dd(rho,nu))
    check(f'ghost_derivative_commutator_{nu}_{rho}',cv-K*(s.trace(H)*dd(nu,rho)-H[nu,rho]))
    check(f'zeroth_curvature_sum_{nu}_{rho}',ch+cv-3*K*H[nu,rho])

# Check the remaining curvature correction in div A. The two commutators
# of h have interchanged external indices and cancel because h is symmetric.
for nu in range(4):
 for rho in range(4):
    comm=lambda u,v:sum(-R(a,mu,mu,u)*H[a,v]-R(a,v,mu,u)*H[mu,a]
           for mu in range(4) for a in range(4))
    check(f'curved_divA_commutators_cancel_{nu}_{rho}',comm(rho,nu)-comm(nu,rho))

# Separate pointwise normal-coordinate control with h coordinate-constant.
# At x=0, rough Laplacian on c has -K c, and B(h)=-2K h.
gamma=lambda a,b,c,j:-(dd(a,c)*dd(b,j)+dd(a,b)*dd(c,j)-2*dd(b,c)*dd(a,j))*K/3
normal_lap_c=s.Matrix(4,4,lambda a,b:sum(gamma(a,i,b,i) for i in range(4)))
normal_B=s.Matrix(4,4,lambda nu,rho:-sum(gamma(a,mu,mu,rho)*H[a,nu] for a in range(4) for mu in range(4)))
check('normal_vector_laplacian_connection',normal_lap_c+K*s.eye(4))
check('normal_constant_h_B',normal_B+2*K*H)
check('normal_constant_h_curvature_cancels_in_original_vertex',H*(normal_lap_c+3*K*s.eye(4))+normal_B)

old=json.loads((HOM/'ghost_bubble/results.json').read_bytes())
coef=[s.Rational(v) for v in old['coefficients_over_angular_factor']]
units={ij:basis(*ij) for ij in labels};p0=(1,0,0,0)
for i,left in enumerate(labels):
 for right in labels[i:]:
    A,J=units[left],units[right]
    check('flat_heat_vs_bubble_'+str(left)+'_'+str(right),flat_heat_cross(A,J,p0)-sum(a*b for a,b in zip(coef,invariants(A,J,p0))))
A=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
J=s.Matrix([[2,-1,1,0],[-1,0,2,1],[1,2,3,-2],[0,1,-2,1]])
p1=(1,2,-1,1)
check('dense_nonaxial_control',flat_heat_cross(A,J,p1)-sum(a*b for a,b in zip(coef,invariants(A,J,p1))))
check('exchange_control',flat_heat_cross(A,J,p1)-flat_heat_cross(J,A,tuple(-v for v in p1)))
check('parallel_scalar_perturbation_flat',flat_heat_cross(s.eye(4),s.eye(4),(0,0,0,0)))

# A useful failure control: the endomorphism term alone is insufficient.
p0=s.Matrix(p0);A=units[(1,2)];E=(zeroth_order(A,p0)+A)/2
reject('omit_connection_curvature_in_flat_heat',flat_heat_cross(A,A,p0)-s.trace(E*E))
reject('ghost_heat_bubble_assumed_transverse',flat_heat_cross(units[(0,0)],units[(0,0)],p0))
reject('omit_curvature_B_correction_normal_chart',2*K)

result=dict(statute='DERIVED_COVARIANT_GHOST_REDUCTION_WITH_EXACT_ALGEBRA;CONDITIONAL_INTEGRATED_HEAT_RESIDUE',
 checks=len(checks),check_names=checks,negative_controls=neg,
 flat_coefficients=[str(v) for v in coef],
 Q_reduced='Q(h)=(I+h)(box+3K)+A^mu nabla_mu+B',
 A='A^lambda_nu,rho=nabla_rho h^lambda_nu+nabla^lambda h_rho,nu-nabla_nu h^lambda_rho+delta^lambda_nu C_rho(h)',
 B='B_nu,rho=nabla_rho C_nu(h)',divergence_A='nabla_mu A^mu=B+box h',
 integrated_quadratic_heat='tr{5K[-h B-A_mu A^mu/4]+(B-box h)^2/8+F_mu,nu F^mu,nu/48+Omega0_mu,nu[A^mu,A^nu]/24}',
 F='F_mu,nu=nabla_mu A_nu-nabla_nu A_mu',
 boundary_discarded='Compactly supported perturbations; integrated residue modulo covariant divergences only',
 assumptions_not_CAS_proved=['Local Laplace-type heat coefficient classification modulo divergences',
 'Cyclicity of logarithmic symbol residue; multiplication by I+h has no logarithmic residue',
 'Perturbative inverse I+h around h=0; no claim of global invertibility for all fields'],
 finite_causal_part_computed=False,curved_tensor_coefficients_fully_reduced=False,
 full_Q2=False,gate_changed=False,wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
files=[Path(__file__),HOM/'ghost_minimal_heat_engine.py',DEST/'PRE_REGISTER.json',DEST/'results.json']
new(DEST/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False))
