"""Exact matrix checks of the independent KMS counterexample; no regional AQFT claim."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C5'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,put
t0=time.process_time();checks=[]
q=s.symbols('q',nonzero=True);t=s.symbols('t',real=True)
rho=s.diag(s.Rational(1,3),s.Rational(2,3));omega=s.diag(s.sqrt(s.Rational(1,3)),s.sqrt(s.Rational(2,3)))
def U(X,z=q):return s.Matrix([[X[0,0],z*X[0,1]],[X[1,0]/z,X[1,1]]])
def F(A,B,z=q):return A[0,0]*B[0,0]/3+2*A[1,1]*B[1,1]/3+A[0,1]*B[1,0]/(3*z)+2*A[1,0]*B[0,1]*z/3
def eq(name,a,b):
    assert s.simplify(a-b)==0,(name,a,b);checks.append(name)
def mat(name,A,B):
    for i in range(A.rows):
        for j in range(A.cols):eq(f'{name}_{i}_{j}',A[i,j],B[i,j])
units=[]
for i in range(2):
    for j in range(2):
        E=s.zeros(2);E[i,j]=1;units.append(E)
eq('rho_normalized',s.trace(rho),1)
eq('omega_unit',s.trace(omega.H*omega),1)
mat('omega_squared',omega*omega,rho)
mat('omega_fixed',U(omega),omega)
mat('omega_inverse',omega*omega.inv(),s.eye(2))
for i,A in enumerate(units):
    # Right multiplication by Omega is bijective: cyclic and separating.
    mat(f'cyclic_{i}',(A*omega.inv())*omega,A)
    mat(f'injective_inverse_{i}',(A*omega)*omega.inv(),A)
    for j,B in enumerate(units):
        bottom=s.trace((A.H*omega).H*U(B*omega))
        top=s.trace((B.H*omega).H*U(A*omega,1/q))
        eq(f'bottom_boundary_{i}_{j}',F(A,B),bottom)
        eq(f'top_boundary_{i}_{j}',F(A,B,q/2),top)
        # On the unit circle conjugate(q)=1/q.
        lhs=s.trace(U(A).H*U(B)).subs(s.conjugate(q),1/q)
        eq(f'unitary_pair_{i}_{j}',lhs,s.trace(A.H*B))
        mat(f'multiplicativity_{i}_{j}',U(A*B),U(A)*U(B))
q2=s.symbols('q2',nonzero=True)
for i,A in enumerate(units):mat(f'group_{i}',U(U(A,q2),q),U(A,q*q2))
E12=units[1];E21=units[2]
mat('opposite_phase_plus',U(E12),q*E12)
mat('opposite_phase_minus',U(E21),E21/q)
eq('plus_generator',s.diff(s.exp(s.I*t*s.log(2)),t).subs(t,0),s.I*s.log(2))
eq('minus_generator',s.diff(s.exp(-s.I*t*s.log(2)),t).subs(t,0),-s.I*s.log(2))
mat('nontrivial_at_pi_over_log2',U(E12,-1),-E12)
assert -E12!=E12;checks.append('nontrivial_nonzero_matrix')
response=ROOT/'C4/orchestration/DEEPSEEK_KMS_ORIGINAL.md'
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),names=checks,cpu_seconds=time.process_time()-t0,
    response_sha256=sha(response),source_sha256=sha(Path(__file__)),status='EXACT_CAS_FINITE_HILBERT_SCHMIDT_MODEL',
    algebra='Left multiplication by M2(C) on HS=M2(C), not B(HS)',rho='diag(1/3,2/3)',
    substitution='q=exp(i t log2), top z=t+i sends q to q/2',
    universality='matrix-unit checks extend by complex bilinearity or sesquilinearity; right multiplication inverse checked on basis',
    analytic_part='FiniteKMSStrip_v4.lean: entire, uniformly bounded closed strip, order-swapped top, nontrivial phase',
    generator='Derivative generator has eigenvalues +/-i log2; selfadjoint Stone generator +/-log2',
    refutes='Vector KMS plus cyclic/separating does not imply trivial dynamics',
    physical_regional_witness=False,literal_KMSAt_instantiated=False,gate_changed=False,
    opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
put(D/'HS_CAS.json',result)
print(json.dumps(dict(checks=result['checks'],cpu_seconds=result['cpu_seconds'])))
