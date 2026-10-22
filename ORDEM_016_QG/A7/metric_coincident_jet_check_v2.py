"""Verify radial-frame derivation of coincident logarithmic Green jets."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import json,hashlib
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber
from metric_principal_vertices import basis,eh_quadratic_8k,trace,inner,mv,dot
H=Path(__file__).resolve().parent;D=H/'metric_coincident_jet_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'metric_coincident_jet_engine_v2.py'),
    supersedes_engine_sha256=sha(H/'metric_coincident_jet_engine.py'),
    supersedes_check_sha256=sha(H/'metric_coincident_jet_check.py'),
    correction='Build all xx[i,j] before consulting transposed xx[j,i]; v1 raised KeyError',
    plan=['radial frame connection from metric and tetrad', 'matrix heat recurrence',
          'Synge mixed derivatives', 'equation of Green contraction','scalar comparison',
          'external derivative quartic tadpole'],
    symbolic_candidate_derived_before_verification=True,finite_state_part=False,full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a):
    values=list(a) if isinstance(a,s.MatrixBase) else [a]
    assert all(s.expand(v)==0 for v in values),(n,a)
    checks.append(n)
x=s.Matrix(s.symbols('x0:4'));z=(x.T*x)[0];I=s.eye(4)
N=z*I-x*x.T
# g=e.T*e, with radial coframe e=R+(sin(sqrt(K)r)/(sqrt(K)r))*T.
e1=-N/6;e2=z*N/120;ei1=N/6;ei2=7*z*N/360
check('coframe_recovers_g_K',2*e1+N/3)
check('coframe_recovers_g_K2',2*e2+e1*e1-2*z*N/45)
check('coframe_inverse_K2',e2+ei2+e1*ei1)
gamma1=[];gamma2=[];A1=[];A2=[]
for i in range(4):
    g1=s.Matrix(4,4,lambda a,b:-(int(a==i)*x[b]+int(a==b)*x[i]-2*int(i==b)*x[a])/3)
    g2=s.Matrix(4,4,lambda a,b:-z*(x[i]*int(a==b)+x[b]*int(a==i))/45
        -2*z*x[a]*int(i==b)/15+8*x[a]*x[i]*x[b]/45)
    a1=g1-e1.diff(x[i]);a2=g2+e1*g1+g1*ei1-e2.diff(x[i])-e1.diff(x[i])*ei1
    L=s.Matrix(4,4,lambda a,b:x[a]*int(i==b)-int(a==i)*x[b])
    check(f'radial_connection_linear_{i}',a1-L/2)
    check(f'radial_connection_cubic_{i}',a2+z*L/24)
    gamma1.append(g1);gamma2.append(g2);A1.append(a1);A2.append(a2)
check('radial_gauge',sum((x[i]*A1[i] for i in range(4)),s.zeros(4)))
check('connection_divergence_K',sum((A1[i].diff(x[i]) for i in range(4)),s.zeros(4)))
div2=sum((A2[i].diff(x[i]) for i in range(4)),s.zeros(4))
for i in range(4):
    for j in range(4):
        div2+=N[i,j]*A1[j].diff(x[i])/3
        if i==j:
            div2-=sum((gamma1[i][k,j]*A1[k] for k in range(4)),s.zeros(4))
check('covariant_connection_divergence_K2',div2)
f=metric_fiber();om=f['omega'];E=f['E'];eye=s.eye(10)
conn=[sum((x[j]*om[j,i]/2 for j in range(4)),s.zeros(10)) for i in range(4)]
# Radial transport (r*d_r+1) a1 = u0^-1 (nabla²+E)u0.
# Scalar source at K²r² is -z/20, recovered from radial u0 and metric.
r,K=s.symbols('r K')
u0=1+K*r*r/4+19*K*K*r**4/480
radial=s.diff(u0,r,2)+3*(1/r-K*r/3-K*K*r**3/45)*s.diff(u0,r)
source=s.series(radial/u0,K,0,3).removeO().expand()
check('scalar_radial_source_K2',source.coeff(K,2)+r*r/20)
source2=-z*eye/20+sum((a*a for a in conn),s.zeros(10))
a1off2=source2/3
check('matrix_radial_transport_degree2',
      sum((x[i]*a1off2.diff(x[i]) for i in range(4)),s.zeros(10))+a1off2-source2)
# U1=K(E+2I)+K²[(z/4)(E+2I)+a1off2].
U1second=z*(E+2*eye)/4+a1off2
lap=sum((U1second.diff(x[i],2) for i in range(4)),s.zeros(10))
check('a2_from_recurrence',(lap+E*f['a1'])/2-f['a2'])
for i in range(4):
    for j in range(4):
        calc=U1second.diff(x[i],x[j])+om[i,j]*f['a1']/2
        check(f'ordered_xx_U1_{i}_{j}',calc-f['xx'][i,j])
        # Bidifferentiated exp(-sigma/2t) contributes +g_ij U2/(2t).
        check(f'Synge_heat_mixed_{i}_{j}',
              int(i==j)*f['a2']/2-f['xx'][j,i]-f['mixed'][i,j])
        c=f['mixed'][i,j]*f['S0']
        check(f'fiber_spatial_reciprocity_{i}_{j}',c-(f['mixed'][j,i]*f['S0']).T)
check('Omega2_on_traceless',f['om2']+16*f['tl'])
check('Omega_annihilates_a1',sum((a*f['a1'] for a in om.values()),s.zeros(10)))
check('Green_equation_contracted',sum((f['mixed'][i,i] for i in range(4)),s.zeros(10))-E*f['a1'])
check('undifferentiated_covariance',f['a1']*f['S0']+2*f['g']*f['g'].T)
# Scalar comparison including arbitrary potential, independent radial source.
mass=s.symbols('E')
scalar_a2=mass**2/2+2*K*mass+29*K*K/s.Integer(15)
scalar_xx=K*mass/2+29*K*K/s.Integer(30)
check('scalar_mixed',scalar_a2/2-scalar_xx-mass*(mass+2*K)/4)
check('scalar_Green_equation',4*(scalar_a2/2-scalar_xx)-mass*(mass+2*K))
# External derivatives: J0=K*a1*S0, factor 1/16 from 1/2*4k/(32k).
# Quartic identity already verified independently in metric_quartic_vertices.
bs=[basis(i,j) for i in range(4) for j in range(i,4)];p=(1,2,-1,0);pn=tuple(-v for v in p)
for a,A in enumerate(bs):
    for b,B in enumerate(bs[a:],a):
        pa=dot(p,mv(A,p));pb=dot(p,mv(B,p));ab=dot(mv(A,p),mv(B,p))
        expected=-2*dot(p,p)*inner(A,B)+2*dot(p,p)*trace(A)*trace(B)-2*(pa*trace(B)+pb*trace(A))+4*ab
        check(f'external_derivative_tadpole_{a}_{b}',-eh_quadratic_8k(A,p,B,pn)-expected)
fresh(D/'results.json',dict(statute='DERIVED_RADIAL_HEAT_RECURRENCE_AND_EXACT_CAS',
    checks=len(checks),check_names=checks,
    mixed_log_over_A0='L_ij=delta_ij*(-2/3 P_TL+12 P_tr)*K²-(1/12)*sum_k{Omega_ik,Omega_jk}',
    undifferentiated_log_over_A0='a1=8K P_tr; physical GH=4kappa*D^-1*I_tr',
    single_derivative_log='0 in the invariant space-form reference',
    tadpole_external_gradient_over_hbar_A0_K=['-2','2','-2','4'],
    tadpole_invariants=['p²trAB','p²trA trB','pAp trB+pBp trA','pABp'],
    internal_derivative_tadpole_not_yet_contracted=True,
    analytic_scope='Auxiliary Euclidean local log heat expansion; no causal finite state part',
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'metric_coincident_jet_engine_v2.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu_seconds=process_time()-cpu)))
