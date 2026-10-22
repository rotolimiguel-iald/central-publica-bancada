"""Independent derivative/contact check of the stripped Fourier phase."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from curved_harmonic_fourier_engine import coefficients,L
from logarithmic_contact_engine import contact,Q
H=Path(__file__).resolve().parent;D=H/'fourier_phase_convention';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,o):
    p=D/n;assert not p.exists(),p
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'curved_harmonic_fourier_engine.py',H/'logarithmic_contact_engine.py',H/'curved_pair_fourier_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Determine stripped phase for Fourier exp(-ipx) via derivative identity and measured local contacts',
    controls='First derivative of U_n for n=2,3,4; all axes. Fourier multiplier i*p; test wrong phase explicitly.',
    excluded='No alteration or reinterpretation of current pair result before full adjoint convention is verified',
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();p=s.symbols('p0:4',real=True);p2=sum(q*q for q in p);checks=[];negatives=[];rows=[]
def coeff(m,l):return sum(s.Rational(c)*L**j for j,c in enumerate(coefficients(m,l,0)))
for n in (2,3,4):
    m0=2*n-4;m1=m0+1
    scalar=(-s.I)**m0*coeff(m0,0)*p2**(n-2)
    for j in range(4):
        # d_j U_n=-2n*x_j U_(n+1), harmonic degree1.
        differentiated=-2*n*(-s.I)**m1*coeff(m1,1)*p[j]*p2**(n-2)
        local=contact(n,0,(j,)).subs(dict(zip(Q,[s.I*q for q in p])),simultaneous=True)
        residual=s.expand(differentiated-s.I*p[j]*scalar-local)
        assert residual==0,(n,j,residual)
        checks.append(f'derivative_and_contact_n{n}_axis{j}')
        wrong=-2*n*s.I**m1*coeff(m1,1)*p[j]*p2**(n-2)
        wrong_res=s.expand(wrong-s.I*p[j]*scalar-local)
        assert wrong_res.coeff(L)!=0,(n,j)
        negatives.append(f'wrong_i_phase_nonlocal_n{n}_axis{j}')
        rows.append(dict(n=n,axis=j,contact=str(local),wrong_residual=str(wrong_res)))
# Exact phase from Schwinger: (-i)^l times Gamma(a-k) residue (-1)^k.
for m in range(5):
    for l in range(m%2,7,2):
        k=(m-l)//2
        assert s.simplify((-s.I)**l*(-1)**abs(k)-(-s.I)**m)==0
        checks.append(f'Gamma_phase_m{m}_l{l}')
result=dict(at=datetime.now(timezone.utc).isoformat(),status='STRIPPED_PHASE_IDENTIFIED',checks=len(checks),
    negative_controls=len(negatives),check_names=checks,negative_names=negatives,rows=rows,
    conclusion='For Fourier exp(-ip.x), coefficients() multiplies C_E*(-i)^m, not C_E*i^m.',
    impact='curved_harmonic_fourier_engine docstring i^m is wrong for this convention; stripped rational coefficients unchanged. Pair additionally includes ordered adjoint phases and must be audited separately.',
    cpu_seconds=time.process_time()-cpu,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','check_names','negative_names')}))
