"""Exact A5.d charge harness on vacuum/one/two-packet sectors.

This is a controlled charge model, not the physical AQFT stress tensor T0.
No full Fock representation, CCR implementation or entropy theorem is asserted.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time
import sympy as s

HERE = Path(__file__).resolve().parent
started = time.perf_counter()
cpu_started = time.process_time()
u, eps = s.symbols('u eps', real=True)
k = s.symbols('k', positive=True)
checks = []

def check(name, actual, expected):
    residual = s.simplify(actual-expected)
    ok = residual == s.zeros(*residual.shape) if isinstance(residual, s.MatrixBase) else residual == 0
    checks.append({'name':name, 'actual':str(actual), 'expected':str(expected),
                   'residual':str(residual), 'pass':bool(ok)})
    if not ok:
        raise AssertionError(name+': '+str(residual))

# f is normalized on positive momenta. Phi=f tensor f is normalized and symmetric.
f = 2*s.sqrt(k)*s.exp(-k)
f_norm = s.integrate(f**2, (k,0,s.oo))
check('one_packet_normalization', f_norm, 1)
check('symmetric_two_packet_normalization', f_norm**2, 1)
check('one_packet_first_momentum', s.integrate(k*f**2,(k,0,s.oo)), 1)

# The positive-frequency profile comes from the elementary Laplace transform.
a = s.symbols('a', positive=True)
laplace = s.integrate(k*s.exp(-a*k),(k,0,s.oo))
check('laplace_kernel_real_positive_parameter', laplace, 1/a**2)
# Complex parameter evaluation is verified independently by an antiderivative
# and exponential decay, not by claiming the previous real hypothesis suffices.
F = -s.exp(-(1+s.I*u)*k)*(k/(1+s.I*u)+1/(1+s.I*u)**2)
check('complex_laplace_antiderivative', s.diff(F,k), k*s.exp(-(1+s.I*u)*k))
check('complex_laplace_lower_endpoint', F.subs(k,0), -1/(1+s.I*u)**2)
check('exponential_decay_envelope', s.simplify(s.exp(-(1+s.I*u)*k)*s.conjugate(s.exp(-(1+s.I*u)*k))), s.exp(-2*k))
check('complex_laplace_upper_endpoint_norm_squared',s.limit(s.simplify(F*s.conjugate(F)),k,s.oo),0)
g = 1/(s.sqrt(s.pi)*(1+s.I*u)**2)

# Exact normal-ordered quadratic matrix on |0>,|1_f>,|2_f>.
# The lowering matrix is a truncation; no full CCR is claimed at its upper edge.
lower = s.Matrix([[0,1,0],[0,0,s.sqrt(2)],[0,0,0]])
raise_ = lower.T
number = raise_*lower
vac = s.Matrix([1,0,0]); phi = s.Matrix([0,0,1])
check('two_body_number',number*phi,2*phi)
check('vacuum_two_body_orthogonality',(vac.T*phi)[0],0)
check('two_body_not_coherent',lower*phi,s.sqrt(2)*s.Matrix([0,1,0]))
q = g**2*(lower**2)+s.conjugate(g)**2*(raise_**2)+2*s.simplify(g*s.conjugate(g))*number
check('stress_hermitian',q.conjugate().T,q)
check('vacuum_stress_subtraction',(vac.T*q*vac)[0],0)
check('vacuum_pair_matrix_element',(vac.T*q*phi)[0],s.sqrt(2)*g**2)
check('two_body_diagonal_stress',(phi.T*q*phi)[0],4/(s.pi*(1+u**2)**2))

pair_re = s.simplify(s.re(s.expand_complex(g**2)))
pair_im = s.simplify(s.im(s.expand_complex(g**2)))
occ = 1/(s.pi*(1+u**2)**2)
Ir = s.integrate(u*pair_re,(u,0,s.oo))
Ii = s.integrate(u*pair_im,(u,0,s.oo))
Io = s.integrate(u*occ,(u,0,s.oo))
Jr = s.integrate(u*pair_re,(u,-s.oo,0))
Ji = s.integrate(u*pair_im,(u,-s.oo,0))
Jo = s.integrate(u*occ,(u,-s.oo,0))
check('half_line_pair_real',Ir,-1/(6*s.pi))
check('half_line_pair_imaginary',Ii,0)
check('half_line_occupation',Io,1/(2*s.pi))
check('full_line_pair_real',Ir+Jr,0)
check('full_line_pair_imaginary',Ii+Ji,0)
check('full_line_occupation',Io+Jo,0)
check('pair_first_absolute_moment',2*s.integrate(u*occ,(u,0,s.oo)),1/s.pi)

Hplus = s.simplify(2*s.pi*((Ir+s.I*Ii)*lower**2+(Ir-s.I*Ii)*raise_**2+2*Io*number))
Hminus = s.simplify(-2*s.pi*((Jr+s.I*Ji)*lower**2+(Jr-s.I*Ji)*raise_**2+2*Jo*number))
Kcompression = s.simplify(Hplus-Hminus)
check('unilateral_matrix',Hplus,s.Matrix([[0,0,-s.sqrt(2)/3],[0,2,0],[-s.sqrt(2)/3,0,4]]))
check('bilateral_compression',Kcompression,s.zeros(3))

psi = (vac+eps*phi)/s.sqrt(1+eps**2)
check('perturbed_normalization',(psi.T*psi)[0],1)
check('noncoherence_minor',(lower*psi)[1]*psi[0]-(lower*psi)[0]*psi[1],s.sqrt(2)*eps/(1+eps**2))
expect = s.simplify((psi.T*Hplus*psi)[0])
check('unilateral_expectation',expect,(-2*s.sqrt(2)*eps/3+4*eps**2)/(1+eps**2))
check('unilateral_first_order',s.diff(expect,eps).subs(eps,0),-2*s.sqrt(2)/3)
check('bilateral_first_order',s.diff((psi.T*Kcompression*psi)[0],eps).subs(eps,0),0)
check('normalization_does_not_change_linear_coefficient',s.diff(expect,eps).subs(eps,0),s.diff(((vac+eps*phi).T*Hplus*(vac+eps*phi))[0],eps).subs(eps,0))
psi_i = (vac+s.I*eps*phi)/s.sqrt(1+eps**2)
check('relative_phase_control',s.diff((psi_i.conjugate().T*Hplus*psi_i)[0],eps).subs(eps,0),0)
Hdiag=s.diag(*Hplus.diagonal())
check('removed_pair_term_control',s.diff((psi.T*Hdiag*psi)[0],eps).subs(eps,0),0)
check('perturbation_sign_control',s.diff(expect.subs(eps,-eps),eps).subs(eps,0),2*s.sqrt(2)/3)

result = dict(status='REAL_EXACT_CHARGE_HARNESS',at=datetime.now(timezone.utc).isoformat(),
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),sympy_version=s.__version__,
    checks=checks,count=len(checks),all_passed=all(c['pass'] for c in checks),
    formulas=dict(f=str(f),g=str(g),Hplus=str(Hplus),Hminus=str(Hminus),
                  expectation=str(expect),first_order=str(-2*s.sqrt(2)/3)),
    wall_seconds=time.perf_counter()-started,cpu_seconds=time.process_time()-cpu_started,
    scope=['Vacuum/one/two-packet charge compression with stated normal-ordered quadratic rule.',
           'A nonzero normalized unilateral first derivative is exhibited; bilateral first derivative vanishes.',
           'The zero bilateral compression does not assert the full boost operator is zero.',
           'No physical T0, complete AQFT net, local covariance, entropy derivative or gate is supplied.',
           'Complex Laplace upper-endpoint vanishing also uses exponential decay against a linear polynomial.'])
out=HERE/'two_body_first_order_exact_v2.json'
raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8')
if out.exists():
    backup=out.with_name(out.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(out.read_bytes())
temp=out.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.replace(out)
print(json.dumps({'count':result['count'],'all_passed':result['all_passed'],
                  'unilateral_first_order':result['formulas']['first_order'],
                  'wall_seconds':result['wall_seconds'],'output':str(out)}))
