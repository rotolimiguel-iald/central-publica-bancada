"""Independent checks of the completed Kimi answer, no remote execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
from logarithmic_contact_engine import contact, residue, Q

H = Path(__file__).resolve().parent
D = H/'kimi_finite_ward_audit'
cpu = time.process_time()
q2 = sum(x*x for x in Q)
checks = []
def check(name, got, expected):
    assert s.expand(got-expected) == 0, (name, got, expected)
    checks.append(name)
def put(name, value):
    p = D/name
    assert not p.exists(), p
    b = json.dumps(value, indent=2, ensure_ascii=False).encode()
    t = p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b)
    assert t.read_bytes() == b
    t.replace(p)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

put('AUDIT_PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    tests=['Meromorphic derivative contact engine versus pure-power recurrences',
           'Independent Fourier finite constants via scalar Schwinger formula',
           'Provided T7 symbolic defect without patching the answer',
           'Plane-wave linearized Euler versus erroneous Weyl substitution',
           'Image and kernel of actual symmetric flat Ward symbol'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in
        (Path(__file__),D/'ANSWER.md',D/'provided_check.py',H/'logarithmic_contact_engine.py')]))

recurrences = []
for n in range(2,9):
    rnext = residue(n+1,(0,0,0,0),(1,1,1,1))
    box_contact = sum(contact(n,0,(i,i)) for i in range(4))
    check('Box contact n='+str(n), box_contact, 4*(2*n-1)*rnext)
    for i in range(4):
        check('gradient contact '+str((n,i)), contact(n,0,(i,)),
              4*(n-1)*residue(n+1,tuple(int(j==i) for j in range(4)),(1,1,1,1)))
    recurrences.append(dict(n=n, RBox_minus_BoxR=str(box_contact)))

# The comparison is of constants, with q2 the DIFFERENTIAL symbol.
# The common Fourier log L cancels. R(U_n) has a Schwinger coefficient
# proportional to [L+H_(n-2)+H_(n-1)-1], whereas D_n retains only L.
reference_shifts = {}
for n in range(2,9):
    r = residue(n,(0,0,0,0),(1,1,1,1))
    shift = (s.harmonic(n-1)+s.harmonic(n-2)-1)*r
    reference_shifts[str(n)] = str(s.expand(shift))
    if n>=3:
        prior = s.sympify(reference_shifts[str(n-1)])
        denominator = 4*(n-1)*(n-2)
        via_recursion = (q2*prior + sum(contact(n-1,0,(i,i)) for i in range(4)))/denominator
        check('reference shift n='+str(n), shift, via_recursion)
check('R3-D3',s.sympify(reference_shifts['3']),-3*q2/64)
check('R4-D4',s.sympify(reference_shifts['4']),-7*q2*q2/2304)

D2,D3,delta,C = s.symbols('D2 D3 delta C')
provided_T7 = s.expand((D3+s.Rational(3,8)*C*delta)-s.Rational(3,64)*C*8*delta-D2)
assert provided_T7 == D3-D2 and provided_T7 != 0
checks.append('provided T7 fails with independent symbols')
# The correct zD3 identity has D2 on the right, not D3.
check('T7 with named zD3 identity', (D2+s.Rational(3,8)*C*delta)-s.Rational(3,64)*C*8*delta,D2)

def ric(A,p):
    return (p.dot(p)*A+p*p.T*s.trace(A)-p*(A*p).T-(A*p)*p.T)/2
def scalar(A,p): return p.dot(p)*s.trace(A)-(p.T*A*p)[0]
def riem(A,p):
    return {(i,j,k,l): (p[j]*p[k]*A[i,l]+p[i]*p[l]*A[j,k]
                        -p[j]*p[l]*A[i,k]-p[i]*p[k]*A[j,l])/2
            for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
p=s.Matrix([1,0,0,0]);A=s.zeros(4);A[1,2]=A[2,1]=1
curv=riem(A,p);norm=sum(t*t for t in curv.values());ricnorm=s.trace(ric(A,p)**2);R=scalar(A,p)
check('linearized Euler quadratic for transverse fixture',norm-4*ricnorm+R**2,0)
wrong=s.expand(norm-2*ricnorm+R**2/3)
assert wrong == 1
checks.append('false Weyl substitution has nonzero counterexample')

a,b,c,d,e=s.symbols('a b c d e');v=s.Matrix([2,-1,1,3]);p=s.Matrix([1,2,-1,1])
entries=s.symbols('h0:10');labels=[(i,j) for i in range(4) for j in range(i,4)]
T=s.Matrix(4,4,lambda i,j: entries[labels.index((min(i,j),max(i,j)))])
G=p*v.T+v*p.T;p2=p.dot(p)
F=a*s.trace(G*T)*p2**2+b*s.trace(G)*s.trace(T)*p2**2
F+=c*((p.T*G*p)[0]*s.trace(T)+(p.T*T*p)[0]*s.trace(G))*p2
F+=d*(p.T*G*T*p)[0]*p2+e*(p.T*G*p)[0]*(p.T*T*p)[0]
ward = s.Matrix([2*a+d,2*c+d+2*e,2*b+2*c])
basis = s.Matrix([p2**2*(p.T*T*v)[0],p2*(p.T*T*p)[0]*p.dot(v),p2**2*s.trace(T)*p.dot(v)])
check('symmetric flat Ward map',F,ward.dot(basis))
matrix=ward.jacobian([a,b,c,d,e]);assert matrix.rank()==3 and len(matrix.nullspace())==2
checks.append('Ward map rank3 kernel2')
for quadratic in (s.trace(ric(G,p)*ric(T,p)),scalar(G,p)*scalar(T,p)):
    check('covariant quadratic is Ward neutral',quadratic,0)

result=dict(at=datetime.now(timezone.utc).isoformat(),status='PARTIAL_ACCEPTANCE_WITH_MEASURED_ERRORS',
    checks=len(checks),check_names=checks,recurrences=recurrences,
    reference_shifts_over_C=reference_shifts,provided_T7_defect=str(provided_T7),
    Euler_fixture=dict(Riemann_squared=str(norm),Ricci_squared=str(ricnorm),scalar_squared=str(R**2),
                       erroneous_replacement_defect=str(wrong)),
    flat_Ward_matrix=str(matrix),cpu_seconds=time.process_time()-cpu,
    limitations=['No full STI or WZ proof inferred from linearized Ricci invariance',
                 'Scalar reference conversion is flat; curved nonlocal remainders remain',
                 'Image rank computed only for the explicitly displayed flat symmetric symbol',
                 'No D2 counterterm adopted, no prescription or gate changed'],full_Q2=False)
put('audit_results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ('check_names','recurrences')},ensure_ascii=False))
