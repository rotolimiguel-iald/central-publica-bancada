"""Exact dyadic 2x2 controls on Hilbert-Schmidt space; not a net theorem."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time
D=Path(__file__).resolve().parent
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def adj(a):return tuple(tuple(complex(a[j][i]).conjugate() for j in range(2)) for i in range(2))
def scale(z,a):return tuple(tuple(z*x for x in row) for row in a)
def inner(a,b):return sum(complex(a[i][j]).conjugate()*b[i][j] for i in range(2) for j in range(2))
def norm2(a):return inner(a,a).real
def diff(a,b):return tuple(tuple(a[i][j]-b[i][j] for j in range(2)) for i in range(2))
def serial(a):return [[[complex(z).real,complex(z).imag] for z in row] for row in a]
def main():
    start=time.process_time()
    eye=((1,0),(0,1));v=((0,1),(1,0));omega=((2,0),(0,1));inv=((.5,0),(0,1));rho=mul(omega,omega);rhoinv=mul(inv,inv)
    # Actual normalized vector is omega/sqrt(5); the common factor cancels from S and Delta.
    basis=[tuple(tuple(int(i==a and j==b) for j in range(2)) for i in range(2)) for a in range(2) for b in range(2)]
    realbasis=basis+[scale(1j,x) for x in basis]
    U=lambda x:mul(v,x);Uinv=U
    J=adj;S=lambda x:mul(mul(inv,adj(x)),omega)
    delta=lambda x:mul(mul(rho,x),rhoinv)
    half=lambda x:mul(mul(omega,x),inv)
    omega2=U(omega)
    # S' is calculated directly from the new pair, not defined by U S U*.
    # If y=A omega', then A=y omega'^-1, hence S'y=A* omega'.
    inv2=mul(inv,v)
    S2=lambda y:mul(adj(mul(y,inv2)),omega2)
    J2=lambda y:mul(mul(v,adj(y)),v)
    delta2=lambda y:mul(mul(mul(mul(v,rho),v),y),rhoinv)
    half2=lambda y:mul(mul(mul(mul(v,omega),v),y),inv)
    tests=[]
    def check(name,truth):
        assert truth,name;tests.append(dict(name=name,passed=True))
    check('U_nontrivial',U(eye)!=eye)
    check('reference_not_fixed',omega2!=omega)
    check('normalization_same',norm2(omega)==norm2(omega2)==5)
    check('U_unitary_on_real_basis',all(inner(U(a),U(b))==inner(a,b) for a in realbasis for b in realbasis))
    check('left_algebra_normalized',all(U(mul(a,Uinv(x)))==mul(mul(mul(v,a),v),x) for a in realbasis for x in realbasis))
    check('old_pair_tomita_rule',all(S(mul(a,omega))==mul(adj(a),omega) for a in realbasis))
    check('new_pair_tomita_rule',all(S2(mul(a,omega2))==mul(adj(a),omega2) for a in realbasis))
    check('old_polar_factorization',all(S(x)==J(half(x)) for x in realbasis))
    check('new_polar_factorization',all(S2(x)==J2(half2(x)) for x in realbasis))
    check('new_J_involution',all(J2(J2(x))==x for x in realbasis))
    check('new_J_antiunitary',all(inner(J2(a),J2(b))==inner(b,a) for a in realbasis for b in realbasis))
    check('positive_new_half',all(inner(x,half2(x)).real>0 for x in realbasis))
    check('new_half_square',all(half2(half2(x))==delta2(x) for x in realbasis))
    check('recognized_S_intertwines',all(U(S(x))==S2(U(x)) for x in realbasis))
    check('recognized_J_intertwines',all(U(J(x))==J2(U(x)) for x in realbasis))
    check('recognized_Delta_intertwines',all(U(delta(x))==delta2(U(x)) for x in realbasis))
    x=basis[1]
    badJ=diff(U(J(Uinv(x))),J(x));badDelta=diff(U(delta(Uinv(x))),delta(x))
    check('wrong_reference_J_fails',norm2(badJ)==2)
    check('wrong_reference_Delta_fails',norm2(badDelta)==9)
    result=dict(status='FINITE_CONTROL_PASSED',at=datetime.now(timezone.utc).isoformat(),tests=tests,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cpu_seconds=time.process_time()-start,
        U_description='Left multiplication by Pauli X',normalized_reference='diag(2,1)/sqrt(5)',new_reference='U omega',
        witness_e12=serial(x),wrong_reference_J_defect_squared=norm2(badJ),wrong_reference_Delta_defect_squared=norm2(badDelta),
        arithmetic='Dyadic real and imaginary components, exactly representable here. Basis checks are finite computational controls, not a Lean theorem.',
        scope='Not preserving the pair can fail. U omega != omega alone does not force failure when omega_prime=U omega. No AQFT net existence or J/Delta uniqueness theorem claimed.')
    p=D/'FINITE_CONTROL_001.json';raw=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    print(json.dumps({k:result[k] for k in ('status','cpu_seconds','wrong_reference_J_defect_squared','wrong_reference_Delta_defect_squared')}|{'tests':len(tests)}))
if __name__=='__main__':main()
