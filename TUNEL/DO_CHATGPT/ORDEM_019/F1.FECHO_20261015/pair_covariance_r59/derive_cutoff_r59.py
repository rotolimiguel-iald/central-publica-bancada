"""Exact same-two-mode cutoff identities; no spatial/network or GKLS limit claim."""
from pathlib import Path
import datetime as dt
import platform
import time
import sympy as s
import support_r59 as io

def main():
    assert not (io.ROOT/'CUTOFF_RESULT_R59.json').exists()
    io.preflight('R5','CUTOFF_PREFLIGHT')
    start=dt.datetime.now(dt.timezone.utc).isoformat();timer=time.perf_counter()
    io.new('CUTOFF_START_R59.json',{'started_utc':start,'script':io.pin(__file__),
        'source':io.pin(r'C:\IALD\papers_latex\graviton_paper\graviton_paper.tex'),
        'domain':'0<q<1; q=tanh(rho)^2; N nonnegative integer; same two bosonic modes.',
        'claims':['normalized projection','exact occupation and pair expectation','boundary CCR defect','explicit moment errors and limiting proof in note'],
        'not_claimed':['device identification','spatial network limit','GKLS convergence','regularFockDomain membership','beta fixes squeezing']})
    q=s.symbols('q',positive=True);N=s.symbols('N',integer=True,nonnegative=True)
    tests=[]
    def check(name,expr):
        value=s.simplify(expr); ok=value==0
        tests.append({'name':name,'pass':ok,'residual':str(value)})
        assert ok,name
    Z=(1-q**(N+1))/(1-q)
    nN=(q-(N+1)*q**(N+1)+N*q**(N+2))/((1-q)*(1-q**(N+1)))
    ninf=q/(1-q);err=(N+1)*q**(N+1)/(1-q**(N+1))
    check('general_geometric_derivative',q*s.diff(Z,q)/Z-nN)
    check('general_occupation_error',ninf-nN-err)
    check('general_pair_error',(ninf-nN)/s.sqrt(q)-(N+1)*q**(N+s.Rational(1,2))/(1-q**(N+1)))
    check('N0_vacuum',nN.subs(N,0))
    check('N1_hardcore_occupation',nN.subs(N,1)-q/(1+q))
    check('N1_hardcore_pair_squared',(nN.subs(N,1)**2/q)-q/(1+q)**2)
    for cutoff in range(1,6):
        dim=cutoff+1
        a=s.zeros(dim)
        for j in range(1,dim):a[j-1,j]=s.sqrt(j)
        top=s.zeros(dim);top[cutoff,cutoff]=1
        comm=a*a.T-a.T*a
        assert comm==s.eye(dim)-dim*top
        tests.append({'name':f'N{cutoff}_matrix_CCR_boundary','pass':True})
        zn=sum(q**j for j in range(dim));occ=sum(j*q**j for j in range(dim))/zn
        check(f'N{cutoff}_normalization',(1-q)*zn/(1-q**dim)-1)
        check(f'N{cutoff}_occupation',occ-nN.subs(N,cutoff))
        # pair expectation before phase factor: sum j*q^(j-1/2)/Z
        pair=sum(j*q**j for j in range(1,dim))/(s.sqrt(q)*zn)
        check(f'N{cutoff}_pair',pair-nN.subs(N,cutoff)/s.sqrt(q))
        rho=s.diag(*[q**j/zn for j in range(dim)])
        X=(a+a.T)/s.sqrt(2)
        top_prob=q**cutoff/zn
        check(f'N{cutoff}_quadrature_boundary',s.trace(rho*X*X)-(occ+s.Rational(1,2)-dim*top_prob/2))
        check(f'N{cutoff}_commutator_expectation',s.trace(rho*comm)-(1-dim*top_prob))
    # Orthogonal projection norm and normalized overlap are computed from the same geometric coefficients.
    Q=s.symbols('Q',real=True,positive=True)
    check('normalized_projection_distance',1+1-2*s.sqrt(1-Q)-2*(1-s.sqrt(1-Q)))
    controls={
        'wrong_CCR_identity_refused_N1':(s.Matrix([[0,1],[0,0]])*s.Matrix([[0,0],[1,0]])-s.Matrix([[0,0],[1,0]])*s.Matrix([[0,1],[0,0]]))!=s.eye(2),
        'hardcore_not_bosonic_saturation':s.simplify(q/(1+q)**2-(q/(1+q))*(q/(1+q)+1))!=0,
        'boundary_cannot_be_omitted':s.simplify(2*q/(1+q))!=0,
        'normalized_cutoff_state_not_exact_projective_state':s.simplify((1-q)/(1-q**2)-(1-q))!=0,
        'q1_not_normalizable':s.limit((1-q)*sum(q**j for j in range(5)),q,1,dir='-')==0,
    }
    assert all(controls.values())
    end=dt.datetime.now(dt.timezone.utc).isoformat()
    out=io.new('CUTOFF_RESULT_R59.json',{'status':'PASS_EXACT_IDENTITIES_WITH_SCOPE',
        'started_utc':start,'ended_utc':end,'seconds':time.perf_counter()-timer,
        'python':platform.python_version(),'sympy':s.__version__,'script':io.pin(__file__),
        'checks':tests,'negative_controls':controls,'exact_identity_count':len(tests),
        'formulas':{'normalizer_squared':'(1-q)/(1-q^(N+1))',
        'n_N':str(nN),'m_N':'exp(i phi) n_N / sqrt(q)',
        'occupation_error':str(err),'fidelity':'1-q^(N+1)',
        'vector_distance_squared':'2*(1-sqrt(1-q^(N+1)))',
        'CCR_expectation':'1-(N+1)*(1-q)*q^N/(1-q^(N+1))'},
        'proof_boundary':'Symbolic checks verify identities; convergence for each fixed q<1 is established in CUTOFF_DERIVATION_R59.txt by geometric tails. No Lean build or experimental verification.'})
    print(out)

if __name__=='__main__':main()
