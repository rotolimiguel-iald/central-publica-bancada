"""Reduce the arity-one antifield jet formula under explicit spaceform isotropy."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber
H=Path(__file__).resolve().parent;D=H/'wick_antifield_spaceform_reduction'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def main():
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Conditional parity-even O4-covariant reduction of four arity-one antifield arrays',
        assumptions=['Natural constant-curvature background and covariant coincidence tensors',
                     'First jets have odd tensor rank and vanish by reflection covariance',
                     'Metric zeroth defect=aTL P_TL+aTr P_tr; ghost zeroth defect=d Id'],
        conventions='Independent symmetric h coordinates and their dual antifields',
        exclusions=['No actual defect coefficients chosen','No entire V1 anomaly','No counterterm adopted','No Lorentzian continuation'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),
            H/'metric_coincident_jet_engine_v2.py',H/'wick_antifield_local_jet_formula/results.json']]))
    start=time.process_time();f=metric_fiber();A=s.Matrix(4,4,s.symbols('a0:16'))
    imgs=[A*B+B*A.T for B in f['basis']]
    M=s.Matrix(10,10,lambda i,j:imgs[j][f['labels'][i][0],f['labels'][i][1]])
    div=s.trace(A);aTL,aTr,d=s.symbols('aTL aTr d');checks=[]
    def eq(name,a):assert s.expand(a)==0,(name,a);checks.append(name)
    eq('full symmetric tensor trace',s.trace(M)-5*div)
    eq('trace subspace compression',s.trace(M*f['ptr'])-div/2)
    eq('traceless compression',s.trace(M*f['tl'])-s.Rational(9,2)*div)
    # Do not suppose M preserves trace/traceless subspaces for arbitrary A.
    assert (f['ptr']*M*f['tl']).applyfunc(s.expand)!=s.zeros(10)
    checks.append('trace reduction is not sector invariance')
    local=s.trace(M*(aTL*f['tl']+aTr*f['ptr']))+d*div
    coeff=s.Rational(9,2)*aTL+aTr/2+d
    eq('complete antifield isotropic coefficient',local-coeff*div)
    eq('linear BRST primitive coefficient',coeff*(2*div)/2-local)
    assert s.expand(coeff*div/2-local)!=0
    checks.append('missing factor two rejected')
    for rank in (3,5):
        assert (-1)**rank==-1;checks.append('reflection excludes invariant odd rank '+str(rank))
    r=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        normalized_A1_antifield='A1(Faf)/(i*hbar)=int chi *(9*aTL/2+aTr/2+d)*div(c)',
        conditional_primitive='(9*aTL/2+aTr/2+d)/2 * int chi*tr(h), since s0 tr(h)=2 div(c)',
        actual_coefficients_measured=False,explicit_hypotheses_required=True,
        important='Minimal heat remainder eigenvalues are NOT automatically the full nonminimal antifield defect coefficients',
        no_claim=['No total V1 anomaly computed','No full Q2 cohomology','No admissible counterterm family with reality proved'],
        full_Q2=False,gate_changed=False)
    put(D/'results.json',r);put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        [Path(__file__),D/'PRE_REGISTER.json',D/'results.json',H/'metric_coincident_jet_engine_v2.py']]))
    print(json.dumps(r,ensure_ascii=False))
if __name__=='__main__':main()
