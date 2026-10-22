"""Exact induced connection curvature traces, separate from heat-kernel/QME claims."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'connection_curvature';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),inputs_sha256=sha(HERE/'model_inputs/DERIVACAO_OPERADORES.md'),
    conventions='Euclidean tangent contractions; R^rho_sigma_mu_nu=K(delta^rho_mu delta_sigma_nu-delta^rho_nu delta_sigma_mu)',
    target='tr(Omega_mu_nu Omega^mu_nu) on T* and S2T*, no scalar-mass replacement',
    open='No Wick map of entire Lorentz operator, no a4 formula imported, no curved self-energy or QME computed'))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,value):
    if isinstance(value,s.MatrixBase):ok=all(s.expand(x)==0 for x in value)
    else:ok=s.expand(value)==0
    assert ok,(name,value);checks.append(name)
def reject(name,value):
    assert s.expand(value)!=0,name;neg.append(name)
K=s.symbols('K',real=True);d=4;I=s.eye(d)
labels=[(i,j) for i in range(d) for j in range(i,d)]
bs=[]
for i,j in labels:
    H=s.zeros(d);H[i,j]=H[j,i]=1;bs.append(H)
G=s.Matrix(10,10,lambda i,j:s.trace(bs[i]*bs[j]))
def induced(om):
    images=[om*H+H*om.T for H in bs]
    return s.Matrix(10,10,lambda a,b:images[b][labels[a][0],labels[a][1]])
tracevec=s.zeros(10,1)
for a,(i,j) in enumerate(labels):
    if i==j:tracevec[a]=1
Em=-2*K*s.eye(10)+2*K*tracevec*tracevec.T
Eg=3*K*I
sumghost=0;summetric=0;sumfull=0
swap=s.zeros(16)
for i in range(d):
    for j in range(d):swap[d*i+j,d*j+i]=1
Ps=(s.eye(16)+swap)/2;Pa=(s.eye(16)-swap)/2
sumanti=0
for mu in range(d):
    for nu in range(mu+1,d):
        om=s.zeros(d);om[mu,nu]=K;om[nu,mu]=-K
        sm=induced(om)
        full=s.kronecker_product(om,I)+s.kronecker_product(I,om)
        check(f'full_symmetric_trace_{mu}_{nu}',s.trace(sm*sm)-s.trace(Ps*full*full))
        check(f'curvature_preserves_trace_{mu}_{nu}',sm*tracevec)
        check(f'curvature_skew_metric_{mu}_{nu}',sm.T*G+G*sm)
        check(f'endomorphism_commutes_{mu}_{nu}',Em*sm-sm*Em)
        # Sum over ordered mu,nu, each antisymmetric pair counted twice.
        sumghost+=2*s.trace(om*om);summetric+=2*s.trace(sm*sm)
        sumfull+=2*s.trace(full*full);sumanti+=2*s.trace(Pa*full*full)
check('vector_curvature_trace',sumghost+24*K**2)
check('symmetric_curvature_trace',summetric+144*K**2)
check('tensor_split',sumfull-summetric-sumanti)
check('symmetric_index_d_plus_2',summetric-(d+2)*sumghost)
check('antisymmetric_index_d_minus_2',sumanti-(d-2)*sumghost)
check('metric_E_trace',s.trace(Em)+12*K)
check('metric_E_square',s.trace(Em*Em)-72*K**2)
check('ghost_E_trace',s.trace(Eg)-12*K)
check('ghost_E_square',s.trace(Eg*Eg)-36*K**2)
reject('ten_independent_scalars_would_have_zero_connection_curvature',summetric)
reject('unsymmetrized_sixteen_tensor_components',sumfull-summetric)
reject('forgetting_ordered_pair_factor',summetric/2+144*K**2)
result=dict(statute='REAL_EXACT_FIBER_CURVATURE_CONTRACTIONS',
    vector_rank=4,metric_rank=10,trace_Omega2_vector=str(sumghost),
    trace_Omega2_symmetric=str(summetric),trace_Omega2_antisymmetric=str(sumanti),
    trace_E_metric=str(s.trace(Em)),trace_E2_metric=str(s.trace(Em*Em)),
    trace_E_vector=str(s.trace(Eg)),trace_E2_vector=str(s.trace(Eg*Eg)),
    half_metric_minus_ghost_Omega2=str(summetric/2-sumghost),
    checks_passed=len(checks),checks=checks,negative_controls=neg,
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    heat_kernel_a4_not_computed=True,curved_ward_not_computed=True,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
