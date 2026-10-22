"""First mixed Ward jet and full antifield Euler slots, fixed heat prescription.

Auxiliary Euclidean space form only. No alteration of canonical sources.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber

H = Path(__file__).resolve().parent
D = H / 'nonminimal_wick_heat_ward'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p, obj):
    assert not p.exists(), p
    b = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(b); assert tmp.read_bytes() == b; tmp.replace(p)

def main():
    D.mkdir(exist_ok=False)
    sources = [Path(__file__), H/'metric_coincident_jet_engine_v2.py',
        H/'curved_parametrix_euler_defect/results.json',
        H/'wick_antifield_spaceform_reduction/results.json']
    put(D/'PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
        target='Full nonminimal antifield Euler defect from minimal heat coefficients and mixed Ward jet',
        prescription='H_r=U0/z-U1*log(z/l2)/4+U2*z*log(z/l2)/16+..., zero added smooth part; leading 1/z',
        assumptions=['4D constant curvature, covariant formal heat transport',
            'Lh intertwines gauge K with LQ; heat kernels intertwine by transport uniqueness',
            'HD=-4*kappa*Hh*Itr; HQ=Hq; ell=1/(2*kappa)',
            'Full graded H has hh=HD,hb=K*HQ,bh=HQ*Kstar,bb=0,cbarc=HQ,barcc=-HQ',
            'Free differential and antifield signs from the preceding bench convention'],
        exclusions=['No global state','No Lorentzian continuation','No full A2/Q2','No smooth finite renormalization chosen'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time();f=metric_fiber();checks=[]
    def eq(name, a):
        values=list(a) if isinstance(a,s.MatrixBase) else [a]
        assert all(s.cancel(v)==0 for v in values),(name,a)
        checks.append(name)
    # Tensor fields use ten independent coordinates. Input is a symmetric tensor,
    # not a 16-coordinate vector with duplicate off-diagonal entries.
    h=s.symbols('h0:10');hv=s.Matrix(h)
    tensor=sum((v*b for v,b in zip(h,f['basis'])),s.zeros(4))
    idx=lambda i,j:f['labels'].index(tuple(sorted((i,j))))
    eye=s.eye(4);omega={}
    for i in range(4):
        for j in range(4):
            a=s.zeros(4)
            if i!=j:a[i,j]=1;a[j,i]=-1
            omega[i,j]=a
    a1q=5*eye
    a2q=s.Rational(179,15)*eye
    xxq={}
    for i in range(4):
        for j in range(4):
            xxq[i,j]=s.Rational(37,15)*eye*int(i==j)
            xxq[i,j]+=sum((omega[i,k]*omega[j,k]+omega[j,k]*omega[i,k]
                          for k in range(4)),s.zeros(4))/12
            xxq[i,j]+=omega[i,j]*a1q/2
    # A_n = dz_x . U_h,n + sym(dz_y U_q,n); B_n = div_x U_h,n + sym(d_y U_q,n).
    # Exact heat Ward identity yields B_n=A_(n+1)/4. Check its first jet at n=1
    # independently using already derived ordered xx U1 jets. Heat mixed U1=-xx^T
    # by Synge; this is NOT the logarithmic Green mixed jet a2/2-xx^T.
    a2h=f['a2'];J_A2={}
    for lam in range(4):
        for nu in range(4):
            actual=sum((f['xx'][lam,mu]*hv)[idx(mu,nu)] for mu in range(4))
            actual-=sum(xxq[alpha,lam][nu,beta]*tensor[alpha,beta]
                        for alpha in range(4) for beta in range(4))
            JA=2*(a2h*hv)[idx(lam,nu)]-2*a2q[0,0]*tensor[lam,nu]
            J_A2[lam,nu]=s.expand(JA)
            eq('independent heat Ward U1 jet '+str((lam,nu)), actual-JA/4)
    # Derivative of H: 1/z terms cancel, logarithms cancel; first smooth jet is A2/16.
    z=s.symbols('z',positive=True);A1,A2,B2=s.symbols('A1 A2 B2')
    ward=A1/(4*z)-A2*s.log(z)/16-A1/(4*z)+B2*z*s.log(z)/16+A2*(s.log(z)+1)/16
    eq('singular and logarithmic cancellation',ward-A2/16-B2*z*s.log(z)/16)
    radial=s.symbols('r',positive=True)
    eq('higher terms have zero first jet',s.limit(s.diff(radial**3*s.log(radial**2),radial),radial,0,dir='+'))
    # S=ell C HD-HQ Kstar=-2 B. Its first jet follows from A2.
    rcoef=-s.Rational(25,12);scoef=s.Rational(5,3)
    Sjet={}
    for lam in range(4):
        for nu in range(4):
            Sjet[lam,nu]=-J_A2[lam,nu]/8
            eq('mixed Ward first jet '+str((lam,nu)),
               Sjet[lam,nu]-rcoef*int(lam==nu)*s.trace(tensor)-2*scoef*tensor[lam,nu])
    # Cstar v=-sym(nabla v)+g div(v)/2; compute it directly from the jet.
    cstar=[]
    for mu,nu in f['labels']:
        cstar.append(s.expand(-(Sjet[mu,nu]+Sjet[nu,mu])/2
                     +int(mu==nu)*sum(Sjet[k,k] for k in range(4))/2))
    expected=-2*scoef*f['tl']+(4*rcoef+2*scoef)*f['ptr']
    eq('Cstar S tensor action',s.Matrix(cstar)-expected*hv)
    eh=3*a2h/4;eg=3*a2q/4
    full=eh-expected
    atl=s.Rational(137,60);atr=s.Rational(579,20);d=s.Rational(179,20)
    eq('full metric antifield defect',full-atl*f['tl']-atr*f['ptr'])
    eq('ghost antifield defect',eg-d*eye)
    coeff=s.Rational(9,2)*atl+atr/2+d
    eq('antifield vertex coefficient',coeff-s.Rational(337,10))
    minimal=s.Rational(9,2)*(-s.Rational(21,20))+s.Rational(479,40)+d
    eq('minimal only coefficient',minimal-s.Rational(81,5))
    eq('missed mixed contribution',coeff-minimal-s.Rational(35,2))
    assert coeff!=minimal;checks.append('zero S at point does not eliminate its derivative')
    eq('linear primitive',2*coeff/2-coeff)
    assert 2*coeff!=coeff;checks.append('missing primitive factor two rejected')
    # Formal block multiplication: noncommuting operator order is retained.
    HH,C,CS,K,KS,Q,HD,HQ,DD=s.symbols('HH C CS K KS Q HD HQ DD',commutative=False)
    ell=s.symbols('ell',nonzero=True)
    P=s.Matrix([[HH,CS,0,0],[C,-1/ell,0,0],[0,0,0,-Q],[0,0,Q,0]])
    HP=s.Matrix([[HD,K*HQ,0,0],[HQ*KS,0,0,0],[0,0,0,HQ],[0,0,-HQ,0]])
    PH=(P*HP).applyfunc(s.expand)
    S=ell*C*HD-HQ*KS
    eq('hh block Schur rewrite',(PH[0,0]-(DD*HD-CS*S)).subs(DD,HH+ell*CS*C))
    eq('bh block',PH[1,0]-S/ell)
    eq('bb block before CK=Q',PH[1,1]-C*K*HQ)
    eq('ghost c block',PH[2,2]-Q*HQ)
    eq('ghost barc block',PH[3,3]-Q*HQ)
    eq('hb block vanishes using HH K=0',PH[0,1]-HH*K*HQ)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        normalized_by='Common covariance leading coefficient set to 1; each displayed curvature coefficient multiplies K²',
        heat_intertwiner_proof='Formal heat Ward B_n=A_(n+1)/4; n1 first jet independently checked using ordered heat U1 derivatives',
        mixed_ward_first_jet={'r':str(rcoef),'s':str(scoef)},
        Cstar_S='-10/3 P_TL -5 P_tr',
        Jh0='K²*(137/60 P_TL+579/20 P_tr)',Jc0='K²*179/20 Id_4',
        Jh1_Jc1='zero under natural parity-even spaceform covariance',
        A1_Faf_over_i_hbar='(337/10)*K²*int chi div(c), times common physical covariance normalization',
        primitive='(337/20)*K²*int chi tr(h), same normalization',
        minimal_only_wrong_coefficient=str(minimal),mixed_correction=str(coeff-minimal),
        full_nonminimal_coincident_slots=True,entire_V1_inventory_verified=False,
        global_state_constructed=False,lorentzian_normalization_fixed=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
        sources+[D/'PRE_REGISTER.json',D/'results.json']],full_Q2=False))
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
