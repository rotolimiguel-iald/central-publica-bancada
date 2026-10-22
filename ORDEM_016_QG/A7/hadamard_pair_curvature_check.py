"""First-curvature one-pair Hadamard profiles and their local derivative contacts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'hadamard_pair_curvature';DEST.mkdir(exist_ok=True)
def new(name,obj):
    p=DEST/name;assert not p.exists();b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    method='Mellin heat integral for V0, u0 Van Vleck expansion, fixed logarithmic extension maps',
    scope='Parallel-frame product before tensor contractions, to linear curvature; not the complete curved loop',
    smooth_remainder='W_A and W_B retained as independent local data, not set to zero',
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    contacts_sha256=hashlib.sha256((HERE/'logarithmic_contact/results.json').read_bytes()).hexdigest(),
    heat_sha256=hashlib.sha256((HERE/'spaceform_heat/results.json').read_bytes()).hexdigest()))
cpu=time.process_time();K,z,e,eps=s.symbols('K z e eps',positive=True);checks=0
# The normalized Green coefficient from heat t^j is
# Gamma(1-j)*(z/4)^(j-1)/4. A1=E+R/6=E+2K on this fixed space form.
assert s.simplify(s.gamma(1)*(z/4)**(-1)/4-1/z)==0;checks+=1
mellin=s.series(s.gamma(-eps)*(z/4)**eps/4,eps,0,1).removeO().expand()
log_coefficient=s.expand(mellin).coeff(eps,0).coeff(s.log(z))
assert log_coefficient==-s.Rational(1,4);checks+=1
u0=(s.sqrt(K*z)/s.sin(s.sqrt(K*z)))**s.Rational(3,2)
u0_first=s.series(u0,z,0,2).removeO().expand()
assert u0_first==1+K*z/4;checks+=1
# Independent first-curvature radial equation: connection terms beyond the
# transported identity first enter at higher curvature for this coincidence term.
L=s.log(z);a=-(e+2*K)/4
f=1/z+a*L
radial=4*z*s.diff(f,z,2)+(8-2*K*z)*s.diff(f,z)+e*f
assert s.expand(radial).coeff(z,-1)==0;checks+=1

maps=json.loads((HERE/'logarithmic_contact/results.json').read_bytes())['maps']
def map_terms(n,ell,order):
    row=next(r for r in maps if (r['n'],r['log_power'],r['derivative_order'])==(n,ell,order))
    return {(t['laplacians'],t['q2_power']):s.Rational(t['coefficient']) for t in row['terms']}
eigenvalues={'metric_traceless':-2*K,'metric_trace':6*K,'ghost':3*K}
rows=[]
from itertools import combinations_with_replacement
for left,right in combinations_with_replacement(eigenvalues,2):
    a1sum=eigenvalues[left]+eigenvalues[right]+4*K
    profile_log=-a1sum/4
    contact_rows=[]
    for order in [3,4]:
        scalar=map_terms(1,0,order);logs=map_terms(1,1,order)
        result={key:s.expand(K*scalar[key]/2+profile_log*logs[key]) for key in scalar}
        contact_rows.append(dict(order=order,terms=[dict(laplacians=j,q2_power=p,coefficient=str(c)) for (j,p),c in result.items()]))
        checks+=1
    rows.append(dict(left=left,right=right,profile_inverse_z_geometric=str(K/2),
        profile_log_over_z=str(profile_log),geometric_contacts=contact_rows,
        smooth_W_contact='(W_left tensor I + I tensor W_right) times map(n=1,ell=0); do not discard'))
# Tensor scalarization is detected already in the logarithmic coefficient.
assert eigenvalues['metric_traceless']+2*K==0
assert eigenvalues['ghost']+2*K!=0
assert eigenvalues['metric_trace']+2*K!=eigenvalues['metric_traceless']+2*K
# At fourth order the metric-traceless/ghost pair is not just a scalar mass shift.
row=next(r for r in rows if r['left']=='metric_traceless' and r['right']=='ghost')
terms=row['geometric_contacts'][1]['terms']
assert [s.sympify(t['coefficient'],locals={'K':K}) for t in terms]==[-37*K/384,-K/3072]
checks+=1
new('results.json',dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,negative_controls=2,
    normalized_profile='I/z + (K/4)I - (E+2K I)/4 log(mu^2 z) + W0 + higher jets',
    normalized_pair='I/z^2 + ((K/2)I + W_A tensor I + I tensor W_B)/z - (E_A tensor I + I tensor E_B +4K I)/4 *log(mu^2 z)/z + higher jets',
    rows=rows,unknown_smooth_remainders_retained=True,
    full_fiber_bitensor_or_vertices_included=False,full_curved_Q2=False,
    cpu_seconds=time.process_time()-cpu))
print(json.dumps(dict(checks=checks,profiles=len(rows),cpu_seconds=time.process_time()-cpu)))
