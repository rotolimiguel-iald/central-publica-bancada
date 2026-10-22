"""Independent spherical-moment contact check and literal derivative reconstruction."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
import sympy as s
import curved_source_jet_engine as e
from logarithmic_contact_engine import differentiated,A,Q
from oneform_second_curvature_engine_v2 import einstein_gauge
from curved_cutoff_descent_engine import polynomial_jet,lower_vector_initial,lie_tensor,spaceform_metric_initial,mono,plus,ZERO,F
H=Path(__file__).resolve().parent;D=H/'finite_curved_source_harmonics_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    assert not p.exists();b=json.dumps(v,indent=2).encode();q=p.with_suffix('.tmp')
    q.write_bytes(b);assert q.read_bytes()==b;q.replace(p)
source=H/'finite_curved_source_harmonics_v2/results.json';prior=json.loads(source.read_bytes())
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    prior_sha256=sha(source),method='S3 l=1 projection /8; literal radial derivatives; covariant E acting on resulting local source'))
cpu=process_time();checks=0;negative={};q2=sum(t*t for t in e.x);q=s.Matrix(Q);I=s.eye(4);X=s.Matrix(e.x);p=I[:,0]
def check(a,b=0):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
def parse(v):return s.sympify(v,locals={**dict(zip(map(str,e.x),e.x)),**dict(zip(map(str,Q),Q)),str(e.z):e.z,str(e.L):e.L})
def normal_numerator(f):
    f=s.expand(f)
    if f==0:return s.Integer(0)
    n=max(-term.as_powers_dict().get(e.z,0) for term in s.Add.make_args(f))
    return s.expand(s.expand(f*e.z**n).subs(e.z,q2))
def reconstruct(rows):
    out=0
    for row in rows:
        harmonic=parse(row['harmonic']);b=row['base_power']
        for powers,coef in s.Poly(harmonic,*e.x).terms():
            indices=tuple(i for i,k in enumerate(powers) for _ in range(k))
            terms=differentiated(b,indices,(1,1,1,1))
            for r,value in enumerate(map(s.Rational,row['derivative_radial_coefficients'])):
                if not value:continue
                for (power,xs),c in terms.items():
                    out+=coef*value*s.prod(e.x[i]**xs[i] for i in range(4))/e.z**power*sum(
                        s.binomial(r,k)*s.diff(c,A,k).subs(A,0)*e.L**(r-k) for k in range(r+1))
    return s.expand(out)
for row in prior['profiles']:
    a,b=row['T'];T=s.zeros(4);T[a,b]=T[b,a]=1;v=I[:,row['v']]
    correction=-e.z*T/6-(X*X.T*T+T*X*X.T)/6
    rawA,rawB=e.kernel(T,v,p,1);extraA,extraB=e.kernel(correction,v,p,0)
    kernelA,kernelB=s.expand(rawA+extraA),s.expand(rawB+extraB)
    check(kernelA.coeff(e.L,1))
    angular=sum(e.average(kernelA*e.x[i])*Q[i]/8 for i in range(4))
    check(angular,parse(row['A_contact_over_C']))
    check(normal_numerator(reconstruct(row['A'])-kernelA))
    check(normal_numerator(reconstruct(row['B'])-kernelB))
    check(e.average(kernelB.coeff(e.L,1)))
    if kernelB.has(e.L) and 'omit_logs' not in negative:
        negative['omit_logs']=dict(T=[a,b],v=row['v'],nonzero_log_numerator=str(normal_numerator(kernelB.coeff(e.L,1))))
    without_density=sum(e.average(rawA*e.x[i])*Q[i]/8 for i in range(4))
    if s.expand(without_density-angular)!=0 and 'omit_density' not in negative:
        negative['omit_density']=dict(T=[a,b],v=row['v'],finite_contact_error=str(s.expand(without_density-angular)))
    if len(negative)==2 and checks%25==0:
        print(json.dumps(dict(stage='reconstruction',checks=checks,cpu=process_time()-cpu)),flush=True)
assert len(negative)==2

# Independent application of the physical Einstein Hessian to the local source.
# No Fourier phase stripped: coefficient is K*(-13 G-19 g div)/96.
metric=polynomial_jet(spaceform_metric_initial,2)
for seed in [1,2]:
    c=polynomial_jet(lower_vector_initial([plus({ZERO:F(i-seed)},mono((i,),i+seed),
              mono((i,(i+1)%4),F(1,2)),mono((i,i,(i+2)%4),seed)) for i in range(4)]),1)
    G=lie_tensor(c,metric)
    def div(w,o):return sum(c(w+(i,),(i,),o) for i in range(4))
    def sourcejet(w,a,b,o):
        if not o:return F()
        return -F(13,96)*G(w,(a,b),o-1)-F(19,96)*int(a==b)*div(w,o-1)
    for o in [1,2]:
        for a in range(4):
            for b in range(4):
                actual=einstein_gauge(sourcejet,(),a,b,o)
                target=F(19,48)*(div((a,b),o-1)-int(a==b)*sum(div((i,i),o-1) for i in range(4)))
                if o>=2:target-=F(19,16)*int(a==b)*div((),o-2)
                check(actual,target)
fresh(D/'results.json',dict(statute='DERIVED_FINITE_CURVED_SOURCE_CONTACT_AUDITED',checks=checks,
    negative_controls=negative,cpu_seconds=process_time()-cpu,
    local_source_difference_over_C='DeltaR(v)=-K[13G(v)+19g div(v)]/96',
    Einstein_image_over_C='E DeltaR=19K[Hess(divv)-g Box(divv)-3K g divv]/48',
    differential_reference='Harmonic radial representation specified in prior profiles; not assumed BRST preserving',
    scope='Geometric firstK source component only; higher-order terms in E-image do not include uncomputed secondK source',
    full_Q2=False,prescription_changed=False,smooth_reference_included=False))
files=[Path(__file__),source,H/'logarithmic_contact_engine.py',H/'curved_source_jet_engine.py',H/'curved_cutoff_descent_engine.py',
       H/'oneform_second_curvature_engine_v2.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,negative_controls=negative,cpu=process_time()-cpu)))
