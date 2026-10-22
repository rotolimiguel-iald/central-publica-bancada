"""Connect existing Gaussian/Wick signs to the measured finite contacts; no new loop."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'finite_relative_normalization';DEST.mkdir(exist_ok=True)
def new(name,obj):
    p=DEST/name;assert not p.exists();b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
wick=json.loads((HERE/'marked_vertex_independent/results.json').read_bytes())
assert sha(HERE/'marked_vertex_independent_check.py')==wick['source_sha256']
for name in ['mixed_bubble_Wick_sign','effective_bubble_after_Q_inverse_minus']:
    assert name in wick['checks']
new('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    method='Compose already checked Wick/externalization sign, -logZ, inverse propagators and source iU',
    scope='Previously adopted Euclidean/formal 1PI convention, not an unperformed Lorentzian causal continuation',
    existing_wick_checks_reused=['mixed_bubble_Wick_sign','effective_bubble_after_Q_inverse_minus'],
    sources={str(p):sha(p) for p in [HERE/'marked_vertex_independent/results.json',
        HERE/'antifield_vertex/PRE_REGISTER.json',HERE/'metric_bubble_v2/results.json',
        HERE/'finite_antifield_contact_v3/results.json']},
    script_sha256=sha(Path(__file__))))
cpu=time.process_time();kap,hbar,A0=s.symbols('kappa hbar A0',nonzero=True)
# Ordered source T U h eta and antighost interaction bareta V h c.
# Existing audit gives externalization*Wick=+1. The connected two-vertex
# contribution to Gamma=-hbar logZ is negative. Q^{-1} has another minus.
source_weight=s.simplify((-hbar)*(4*kap)*(-1)*s.I)
assert source_weight==4*s.I*kap*hbar
tree_hstar_c=s.I;einstein_weight=1/(4*kap)
relative=s.simplify(einstein_weight*source_weight/(hbar*tree_hstar_c))
assert relative==1
# The Fourier conversion cannot introduce a rank-dependent relative sign.
conversions=[]
for degree in [3,4]:
    factor=s.simplify((-s.I)**degree*s.I**degree)
    assert factor==1;conversions.append(dict(degree=degree,factor=str(factor)))
prior=json.loads((HERE/'finite_antifield_contact_v3/results.json').read_bytes())
lam=s.Symbol('lambda')
coefs=[s.sympify(c).subs(lam,relative) for c in prior['combined_hc_coefficients']]
assert coefs==[s.Rational(187,1920),s.Rational(73,960),-s.Rational(33,160)]
raw_ward_prefactor=-2*s.I*hbar*A0
new('results.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_weight=str(source_weight),relative_lambda=str(relative),
    hc_coefficients=list(map(str,coefs)),basis=prior['combined_basis'],
    Euclidean_raw_contact_Ward_prefactor=str(raw_ward_prefactor),
    Fourier_rank_factors=conversions,checks=5,existing_Wick_results_reused=True,
    new_loop_integrals=0,full_Lorentzian_time_ordered_amplitude_calculated=False,
    full_curved_Q2=False,cpu_seconds=time.process_time()-cpu))
print(json.dumps(dict(relative_lambda=str(relative),hc_coefficients=list(map(str,coefs)),
    source_weight=str(source_weight),cpu_seconds=time.process_time()-cpu)))
