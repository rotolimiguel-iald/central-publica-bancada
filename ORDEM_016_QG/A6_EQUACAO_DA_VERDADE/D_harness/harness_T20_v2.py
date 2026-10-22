"""Independent A6.D2 harness. Exact linear algebra plus bounded numerical checks.

Does not import the V1 harness or its results. Runs only in this benchmark directory.
Finite grids are measurements, not universal analytic proofs.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, random, time, traceback
import sympy as sp
import mpmath as mp

HERE=Path(__file__).resolve().parent
PLAN=HERE/'D2_PRE_REGISTRO.json'
CONFIG=json.loads(PLAN.read_bytes())
R=sp.Rational
s,t=sp.symbols('s t',real=True,nonnegative=True)
I=sp.eye(5);Z=sp.zeros(5);checks=[];controls=[];intervals=[];matrix_trials=[];inputs={}
start=time.monotonic();cpu_start=time.process_time()

def check(name, condition, detail=None):
    ok=bool(condition)
    checks.append(dict(name=name,ok=ok,detail=detail))
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)
    assert ok,name

def control(name, property_holds, detail):
    detected=not bool(property_holds)
    controls.append(dict(name=name,property_holds=bool(property_holds),detected=detected,detail=detail))
    print(('DETECTED ' if detected else 'MISSED ')+name,flush=True)
    assert detected,name

def zero(M): return all(sp.simplify(e)==0 for e in M)
def encode_matrix(M): return [[str(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
def same_space(A,B): return A.rank()==B.rank()==A.row_join(B).rank()
def col_basis(vectors): return sp.Matrix.hstack(*vectors)

def run():
    rng=random.Random(CONFIG['seed'])
    u=[sp.Matrix(v) for v in [[1,2,0,-1,1],[2,-1,1,0,0],[-3,1,7,10,11]]]
    D=[u[0].T.col_join(2*u[0].T),u[1].T,u[2].T.col_join(u[2].T).col_join(sp.zeros(1,5))]
    H=sum((d.T*d for d in D),Z)
    stacked=sp.Matrix.vstack(*D)
    F=col_basis(stacked.nullspace());K=col_basis(H.nullspace())
    P=F*(F.T*F).inv()*F.T;Q=I-P
    x=sp.Matrix(sp.symbols('x0:5',real=True))
    table={(a,b):1-(a-b)**2 for a in [0,1] for b in [0,1]}
    check('S1 truth table and bivalence',all(v==int(a==b) and v in (0,1) for (a,b),v in table.items()))
    check('S2 individual kernels and intersection',[len(d.nullspace()) for d in D]==[4,4,4] and F.cols==2)
    check('S2 penalty kernel equality',same_space(F,K))
    check('S2 quadratic form identity',sp.expand((x.T*H*x)[0]-sum((d*x).dot(d*x) for d in D))==0)
    check('S2 selfadjointness',H.T==H)
    eigen=H.eigenvals();spectrum=sorted(eigen.keys())
    check('S2 exact nonnegative spectrum',sum(eigen.values())==5 and all(v>=0 for v in spectrum),str(eigen))
    check('S2 orthogonal projector',P*P==P and P.T==P and P.rank()==2 and P!=Z and P!=I)
    check('S2 mutual annihilation',H*P==Z and P*H==Z)
    # Spectral projectors computed from H by Lagrange polynomials, independently of u*u^T.
    projectors={}
    for lam in spectrum:
        E=I
        for mu in spectrum:
            if mu!=lam: E=E*(H-mu*I)/(lam-mu)
        projectors[lam]=E
    check('S2 spectral projectors resolve identity',sum(projectors.values(),Z)==I and projectors[0]==P)
    check('S2 projectors diagonalize H',all(H*E==lam*E and E.T==E for lam,E in projectors.items()) and
          all(A*B==(A if la==lb else Z) for la,A in projectors.items() for lb,B in projectors.items()))
    def flow(q): return sum((sp.exp(-q*lam)*E for lam,E in projectors.items()),Z)
    T=flow(s)
    check('S2 initial condition',flow(0)==I)
    check('S2 actual flow ODE',zero(T.diff(s)+H*T))
    check('S2 Taylor coefficients through order 12',all(sum(((-lam)**n*E for lam,E in projectors.items()),Z)==(-H)**n for n in range(13)))
    check('S2 semigroup',zero(flow(s)*flow(t)-flow(s+t)))
    check('S2 conserved readout',zero(P*T-P) and zero(T*P-P))
    check('S2 preserved and decaying decomposition',zero(T-P-T*Q))
    moving=u[1]
    check('S2 nonfixed content changes',Q*moving==moving and zero(T*moving-sp.exp(-6*s)*moving) and sp.exp(-6)!=1)
    # New rational random matrices, not the two seeds or matrices of V1.
    C=sp.Matrix.vstack(*(v.T for v in u))
    weights=[sp.Matrix(2,3,lambda i,j:R(rng.randint(-4,4),rng.randint(1,5))) for _ in range(3)]
    Dg=[W*C for W in weights];G=sum((d.T*d for d in Dg),Z)
    Gstack=sp.Matrix.vstack(*Dg);Fg=col_basis(Gstack.nullspace());Pg=Fg*(Fg.T*Fg).inv()*Fg.T
    check('S2 random exact penalty/kernel',G.T==G and same_space(col_basis(G.nullspace()),Fg) and Pg*G==Z)
    check('S2 random quadratic certificate',sp.expand((x.T*G*x)[0]-sum((d*x).dot(d*x) for d in Dg))==0)
    small=sum((W.T*W for W in weights),sp.zeros(3))
    minors=[small[:i,:i].det() for i in range(1,4)]
    check('S2 random strict positivity on row space',C.rank()==3 and all(v>0 for v in minors),[str(v) for v in minors])
    # Inertia: congruence of positive definite small matrix through rank-3 C gives 3 positive/2 zero eigenvalues.
    check('S2 random exact inertia',G.rank()==3 and len(G.nullspace())==2)
    powers=I
    series=I
    series_ok=True
    for n in range(1,16):
        powers=powers*G
        series += (-s)**n*powers/sp.factorial(n)
        series_ok=series_ok and zero(Pg*series-Pg)
    check('S2 random series projection orders 0..15',series_ok)
    check('S3 entrywise limit',zero(T.applyfunc(lambda a:sp.limit(a,s,sp.oo))-P))
    positive=[v for v in spectrum if v>0];gap=min(positive)
    check('S3 gap is attained, constant-one operator bound certificate',gap==6 and all(v>=gap for v in positive) and projectors[gap].rank()>0)
    l1=lambda v:(P*v).dot(P*v)
    l2=lambda v:v.dot(v)
    check('S3 continuous reader factors and conserved',sp.simplify(l1(T*x)-l1(x))==0 and sp.simplify(l1(P*x)-l1(x))==0)
    check('S3 continuous reader neither factors nor conserved',l2(P*moving)!=l2(moving) and sp.simplify(l2(flow(1)*moving)-l2(moving))!=0)
    s0=R(2,5)
    check('S3 single positive sample and iterates',zero(flow(s0)**3-flow(3*s0)) and sp.simplify(l1(flow(s0)*x)-l1(x))==0 and sp.simplify(l2(flow(s0)*moving)-l2(moving))!=0)
    check('S4 range equals fixed space',same_space(col_basis((P-I).nullspace()),col_basis(P.columnspace())))
    check('S4 iterated projection n=1..8',all(P**n==P for n in range(1,9)))
    pairs=[]
    for n in range(CONFIG['exact_pair_count']):
        a=sp.Matrix([R(rng.randint(-9,9),rng.randint(1,7)) for _ in range(5)])
        d=sp.Matrix([R(rng.randint(-9,9),rng.randint(1,7)) for _ in range(5)])
        b=a+Q*d if n%2==0 else a+d
        lhs=P*a==P*b;rhs=P*(a-b)==sp.zeros(5,1)
        pairs.append(dict(a=encode_matrix(a),b=encode_matrix(b),lhs=lhs,rhs=rhs))
    check('S4 48 rational pairs equivalence',all(a['lhs']==a['rhs'] for a in pairs) and any(a['lhs'] for a in pairs) and any(not a['lhs'] for a in pairs))
    check('S4 ker P equals F orthogonal complement',same_space(col_basis(P.nullspace()),col_basis(F.T.nullspace())))
    check('S5 zero reading derivative but nonzero content derivative',zero((P*T*x).diff(s)) and not zero((T*moving).diff(s)))
    z=sp.symbols('z',real=True);a=2/(sp.exp(z/2)+sp.exp(-z/2));q=(sp.exp(z)-1)/(sp.exp(z)+1)
    check('S5 profile differential identities',sp.simplify(sp.diff(a,z)+a*q/2)==0 and sp.simplify(sp.diff(q,z)-a*a/2)==0)
    check('S5 profile origin',tuple(sp.simplify(v.subs(z,0)) for v in [sp.diff(a,z),sp.diff(q,z),sp.diff(a,z,2)])==(0,R(1,2),R(-1,4)))
    p,k=sp.symbols('p k',positive=True);r=sp.sqrt((2*p-1)**2+4*k*sp.exp(-2*s))
    rho=sp.Matrix([[p,sp.sqrt(k)*sp.exp(-s)],[sp.sqrt(k)*sp.exp(-s),1-p]])
    sig=sp.diag(p,1-p)
    pin=lambda M:sp.diag(M[0,0],M[1,1])
    check('S6 dephasing and equation',pin(rho)==sig and zero(rho.diff(s)+rho-pin(rho)))
    Es=sp.diag(1,0,0,1);Is=sp.eye(4);Ds=Is-Es
    check('S6 Hilbert-Schmidt orthogonal projection and penalty',Es*Es==Es and Es.conjugate().T==Es and Ds.conjugate().T*Ds==Is-Es)
    check('S6 full superoperator exponential',zero((-s*(Is-Es)).exp()-Es-sp.exp(-s)*(Is-Es)))
    check('S6 exact cross entropy',sp.simplify(-(rho*sp.diag(sp.log(p),sp.log(1-p))).trace()+p*sp.log(p)+(1-p)*sp.log(1-p))==0)

    l=sp.symbols('lambda');characteristic=rho.charpoly(l).as_expr()
    check('S6 eigenvalue polynomial',sp.simplify(characteristic-((l-R(1,2))**2-r*r/4))==0)
    S=-((1+r)/2*sp.log((1+r)/2)+(1-r)/2*sp.log((1-r)/2))
    rate=2*k*sp.exp(-2*s)/r*(sp.log(1+r)-sp.log(1-r))
    # Differentiate first; verify logarithm differences in the real positive domain.
    check('S6 symbolic entropy derivative',sp.simplify(sp.expand_log(sp.diff(S,s)-rate,force=True))==0)
    check('S6 positive-domain algebra',sp.expand(1-r*r-4*(p*(1-p)-k*sp.exp(-2*s)))==0)
    mp.iv.dps=CONFIG['interval_precision']
    iv=mp.iv
    def ir(q): return iv.mpf(int(sp.numer(q)))/iv.mpf(int(sp.denom(q)))
    parameter_pairs=[(R(1,2),R(99,400)),(R(1,3),R(1,25)),(R(9,10),R(891,10000)),(R(1,7),R(1,10))]
    for pp,kk in parameter_pairs:
        assert 0<kk<pp*(1-pp)
        for j in range(CONFIG['interval_points_per_parameter_pair']):
            ss=R(10*j,CONFIG['interval_points_per_parameter_pair']-1)
            pi,ki,si=ir(pp),ir(kk),ir(ss)
            radius=iv.sqrt((2*pi-1)**2+4*ki*iv.exp(-2*si))
            assert radius.a>0 and radius.b<1
            derivative=2*ki*iv.exp(-2*si)/radius*iv.ln((1+radius)/(1-radius))
            ok=bool(derivative.a>0)
            intervals.append(dict(p=str(pp),k=str(kk),s=str(ss),radius=str(radius),rate=str(derivative),strict_positive=ok))
    check('S6 interval derivative grid',len(intervals)>=64 and all(e['strict_positive'] for e in intervals),len(intervals))
    check('S6 degenerate zero-coherence states constant',all(sp.diag(pp,1-pp).diff(s)==sp.zeros(2) for pp in [R(1,2),R(1,3)]))
    mp.mp.dps=CONFIG['matrix_precision']
    def mpval(v):
        return mp.mpc(str(sp.re(v).evalf(60)),str(sp.im(v).evalf(60)))
    def mpmat(M): return mp.matrix([[mpval(M[i,j]) for j in range(M.cols)] for i in range(M.rows)])
    for pp,kk in parameter_pairs:
        for denom in [1,2,5]:
            cc=sp.sqrt(kk)*(3+4*sp.I)/5
            state=sp.Matrix([[pp,cc/denom],[sp.conjugate(cc)/denom,1-pp]])
            V,L=state.diagonalize(normalize=False)
            logstate=V*sp.diag(*(sp.log(L[j,j]) for j in range(2)))*V.inv()
            logref=sp.diag(sp.log(pp),sp.log(1-pp))
            assert zero(state*V-V*L) and zero(V*L*V.inv()-state)
            sm=mpmat(state);lr=mpmat(logstate);ls=mpmat(logref)
            rel=sm*(lr-ls);Dvalue=rel[0,0]+rel[1,1]
            values,_=mp.eighe(sm)
            sent=-sum(e*mp.log(e) for e in values)
            pv=mp.mpf(str(pp.p))/mp.mpf(str(pp.q))
            refsent=-pv*mp.log(pv)-(1-pv)*mp.log(1-pv)
            residual=abs(Dvalue-(refsent-sent))
            ok=residual<=mp.mpf(CONFIG['residual_tolerance'])
            matrix_trials.append(dict(p=str(pp),k=str(kk),s='log('+str(denom)+')',state=encode_matrix(state),
                diagonalizer=encode_matrix(V),eigenvalues=[str(L[j,j]) for j in range(2)],
                logstate=encode_matrix(logstate),relative_entropy=mp.nstr(Dvalue,52),entropy=mp.nstr(sent,52),
                residual=mp.nstr(residual,52),ok=ok))
    check('S6 exact matrix logarithm vs independent numeric eigen-entropy',all(e['ok'] for e in matrix_trials),len(matrix_trials))
    f=F[:,0];g=F[:,1]-F[:,0]*(F[:,0].dot(F[:,1])/F[:,0].dot(F[:,0]))
    control('N1 altered kernel mode conserves old readout',zero(P*(sp.exp(-f.dot(f))*f)-P*f),'Hprime=H+f*f.T, f in ker H')
    control('N2 constant reader distinguishes identities',P*f!=P*sp.zeros(5,1) and 1!=1,'Px differs, constant reader identical')
    cut=H+g*g.T
    control('N3 pruning preserves full fixed space',len(cut.nullspace())==F.cols,'nonzero fixed mode removed; new nullity='+str(len(cut.nullspace())))
    ob=P+f*u[0].T/u[0].dot(u[0])
    assert ob*ob==ob and H*ob==Z
    control('N4 oblique projection conserves readout',ob*H==Z and zero(ob*T-ob),'P^2=P, HP=0; PH nonzero')
    signed=D[0].T*D[0]-D[1].T*D[1]
    control('N5a signed penalty preserves intersection and sum-of-squares',same_space(col_basis(signed.nullspace()),F) and
            sp.expand((x.T*signed*x)[0]-sum((d*x).dot(d*x) for d in D))==0,'signed/omitted penalties; old sum identity fails')
    E1,E2,E3=[v*v.T/v.dot(v) for v in u]
    Tb=P+sp.exp(-3*s)*E1+sp.exp(3*s)*E2+sp.exp(-5*s)*E3
    reader=lambda v:(u[0].dot(v)/u[0].dot(u[0]))*(u[1].dot(v)/u[1].dot(u[1]))
    assert zero(P*Tb-P) and sp.simplify(reader(Tb*x)-reader(x))==0
    control('N5b every conserved continuous reader factors',reader(P*(u[0]+u[1]))==reader(u[0]+u[1]),'indefinite generator, conserved product=1 vs projected product=0')
    assert zero(Q*T*moving-sp.exp(-6*s)*moving) and sp.exp(-6*s).is_positive
    control('N6 conserved discontinuous indicator factors',int(Q*P*moving!=sp.zeros(5,1))==int(Q*moving!=sp.zeros(5,1)),'nonzero-mode indicator conserved for finite s but 0 after projection')
    control('N7 nonbinary inputs yield bits',1-R(1,2)**2 in (0,1) and 1-2**2 in (0,1),'outputs 3/4 and -3')
    bad=sp.Matrix([[R(1,2),R(3,5)],[R(3,5),R(1,2)]])
    control('N8 invalid density is positive',all(v>=0 for v in bad.eigenvals()),str(bad.eigenvals()))
    inputs.update(u=[encode_matrix(v) for v in u],D=[encode_matrix(d) for d in D],H=encode_matrix(H),P=encode_matrix(P),
         random_weights=[encode_matrix(w) for w in weights],random_D=[encode_matrix(d) for d in Dg],random_H=encode_matrix(G),
         small_positive_matrix=encode_matrix(small),positive_minors=[str(v) for v in minors],pairs=pairs,
         spectrum={str(k):v for k,v in eigen.items()},spectral_projectors={str(k):encode_matrix(v) for k,v in projectors.items()})

error=None
try:
    run()
except Exception:
    error=traceback.format_exc();print(error,flush=True)
result=dict(status='PASS' if error is None else 'FAIL',at=datetime.now(timezone.utc).isoformat(),
            checks=checks,controls=controls,intervals=intervals,matrix_trials=matrix_trials,inputs=inputs,error=error,
            configuration=CONFIG,plan_sha256=hashlib.sha256(PLAN.read_bytes()).hexdigest(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            versions=dict(sympy=sp.__version__,mpmath=mp.__version__),
            wall_seconds=time.monotonic()-start,cpu_seconds=time.process_time()-cpu_start)
dest=HERE/(Path(__file__).stem+'_results.json')
assert not dest.exists(),'Preserve prior run; create versioned source for a correction'
raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8')
temp=dest.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.replace(dest)
print(json.dumps(dict(status=result['status'],checks=len(checks),controls=len(controls),intervals=len(intervals),matrix_trials=len(matrix_trials))),flush=True)
raise SystemExit(0 if error is None else 1)
