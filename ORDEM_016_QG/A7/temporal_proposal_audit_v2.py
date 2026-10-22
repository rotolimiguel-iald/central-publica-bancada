# Supersedes failed symbolic normal-form check; predecessor SHA256 d0d6c769eb122c4bf8f2b15b1896669c870caaeee872b9763812597929bb09e6
"""Check the actual scaling/geometry errors in the received prescription."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'temporal_proposal_audit_v2';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
response=HERE/'received_reviews/ba337b71-5345-44e7-8481-04a24ba1569e.md'
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    response_sha256=sha(response),targets=['FLRW cosine is not Lorentz spaceform with spherical slices',
    'superficial degree is sd minus transverse dimension, not sd','nonunique extension at arity3'],
    unchanged='No choice of a replacement physical horizon; no temporal prescription frozen'))
start,cpu=perf_counter(),process_time();r=s.symbols('r',real=True);lam=s.symbols('lambda',positive=True)
ac=2*s.cos(r/2);ah=2*s.cosh(r/2)
def spaceform_defect(a):return s.simplify(s.expand_trig(a*s.diff(a,r,2)-s.diff(a,r)**2-1))
cos_defect=s.trigsimp(spaceform_defect(ac));cosh_defect=s.simplify(spaceform_defect(ah))
assert cos_defect==-2 and cosh_defect==0
# Equality of temporal/spatial sectional curvatures requires this zero,
# independently of flipping the overall Riemann sign convention.
temporal=s.simplify(s.diff(ac,r,2)/ac);spatial=s.trigsimp((1+s.diff(ac,r)**2)/ac**2)
assert s.trigsimp(s.expand_trig(s.expand((temporal-spatial)*ac**2)))==-2
graphs=[]
for n in range(2,7):
    internal=n;derivative_degree=2*n;sd=2*internal+derivative_degree;dimension=4*(n-1)
    omega=sd-dimension;assert omega==4
    graphs.append(dict(vertices=n,internal_lines=internal,derivatives_all_internal=derivative_degree,
                       sd_bound=sd,transverse_dimension=dimension,extension_order_bound=omega))
# Concrete arity3 counterexample to 'n>=3 automatically unique':
# f(x)=|x|^-8 in the eight relative coordinates. Its critical extension
# finite part is not unique: t+c delta_8 has the same restriction/scaling.
x=s.symbols('x0:8',real=True);f=sum(z*z for z in x)**(-4)
scaled=f.subs({z:lam*z for z in x},simultaneous=True)
assert s.simplify(scaled-lam**(-8)*f)==0
assert 8-4*(3-1)==0
eps=s.symbols('eps',positive=True)
critical=s.integrate(1/lam,(lam,eps,1));assert s.simplify(critical+s.log(eps))==0
result=dict(statute='REAL_LOCAL_REJECTION_OF_TEMPORAL_PROPOSAL_AS_COMPLETE',
    cosine_defect=str(cos_defect),cosh_control=str(cosh_defect),
    temporal_section_factor=str(temporal),spatial_section_factor=str(spatial),
    cycle_counting=graphs,arity3_counterexample='|x|^-8 on R8: sd8 equals diagonal codim8; t+c delta8 is not unique',
    checks_passed=10,negative_claims_refuted=3,
    documentary_issues=['multiplet omits barc but contains b and calls it minimal',
      'sqrt(kappa) changes fixed normalization and is not real for allowed kappa<0',
      'E_max2 unsupported; quantum valence filtration measured previously',
      'mu, parametrix and finite local coefficient hierarchy not specified by numerical/formula values'],
    temporal_prescription_fixed=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False))
