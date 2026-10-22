"""Independent finite-matrix identities and read-only recovery comparison."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
OUT=HERE.parent.parent
checks=[]
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def check(name,condition,detail):
    checks.append({'name':name,'pass':bool(condition),'detail':detail})
    assert condition,name
def eq(a,b):
    return (a-b).applyfunc(s.simplify)==s.zeros(*a.shape)

eye=s.eye(2); lowering=s.Matrix([[0,1],[0,0]])
z=s.diag(1,-1); xx=lowering+lowering.H
k=s.kronecker_product
ai=k(lowering,eye,eye); ao=k(eye,lowering,eye); sm=k(eye,eye,lowering)
sp=sm.H; Zi=k(z,eye,eye); Zaux=k(eye,eye,z)
wc,w,g,Om,ki,ko,gam,gp,lam=s.symbols('wc w g Om ki ko gam gp lam', real=True)
H=wc*(ai.H*ai+ao.H*ao)+w*(sp*sm)+g*(ai.H*sm+sp*ai)+Om*(sp+sm)
J=ao.H*sm+sp*ai
jumps=[ai,ao,sm,Zaux,J]
rates=[ki,ko,gam,gp,lam]
def dissipator(j,A):
    square=j.H*j
    return j.H*A*j-(square*A+A*square)/2
def adjoint(A):
    ans=s.I*(H*A-A*H)
    for rate,j in zip(rates,jumps):ans+=rate*dissipator(j,A)
    return ans.applyfunc(s.expand)
C=ai*ao;B=ai.H*ao
LC=adjoint(C);LB=adjoint(B)
targetC=(-(ki+ko+lam)/2-2*s.I*wc)*C-s.I*g*Zi*ao*sm
targetB=-(ki+ko+lam)*B/2+s.I*g*Zi*ao*sp
check('full_adjoint_C',eq(LC,targetC),'All Hamiltonian and five dissipators retained; no term removed by rate fitting.')
check('full_adjoint_B',eq(LB,targetB),'B=a_i^dagger a_out; the two optical wc terms cancel only for this B and shared wc.')
check('holographic_dissipator',eq(dissipator(J,C),-C/2) and eq(dissipator(J,B),-B/2),'D_J^dagger(C)=-C/2 and D_J^dagger(B)=-B/2 only in the stated 2x2x2 model.')
check('finite_generator_structure',eq(H,H.H) and eq(adjoint(s.eye(8)),s.zeros(8)),'Hermitian H for real parameters and L^dagger(I)=0. Finite GKLS requires nonnegative rates.')
check('cutoff_commutator',eq(ai*ai.H-ai.H*ai,Zi) and not eq(Zi,s.eye(8)),'[a_i,a_i^dagger]=Z_i, not I: no transfer to the unbounded bosonic CCR/GKLS follows.')
D=k(z,xx,xx)
check('countermodel_D',eq(D,D.H) and eq(D*D,s.eye(8)) and s.trace(D)==0,'D is Hermitian involution with eigenvalues +/-1, four each.')
eps=s.symbols('epsilon',real=True)
rho_plus=(s.eye(8)+eps*D)/8;rho_minus=(s.eye(8)-eps*D)/8
def partial_aux(rho):
    return s.Matrix(4,4,lambda i,j:sum(rho[2*i+t,2*j+t] for t in range(2)))
check('same_full_optical_reduction',eq(partial_aux(rho_plus),s.eye(4)/4) and eq(partial_aux(rho_minus),s.eye(4)/4),'Both full optical reductions are I4/4, stronger than equality of selected optical moments.')
check('positive_density_family',D.eigenvals()=={-1:4,1:4} and s.trace(rho_plus)==1 and s.trace(rho_minus)==1,'Spectra of rho+/- are (1+epsilon)/8 and (1-epsilon)/8, each fourfold; positive for |epsilon|<=1, distinct derivatives for epsilon*g!=0.')
check('initial_C_B_zero',all(s.simplify(s.trace(rho*A))==0 for rho in [rho_plus,rho_minus] for A in [C,B]),'C(0)=B(0)=0 in both states.')
check('D_adjoint_contractions',s.simplify(s.trace(D*LC))==-2*s.I*g and s.simplify(s.trace(D*LB))==2*s.I*g,'Tr(D L^dagger C)=-2ig; Tr(D L^dagger B)=2ig.')
derivatives=[s.simplify(s.trace(rho*A)) for rho in [rho_plus,rho_minus] for A in [LC,LB]]
check('distinct_initial_derivatives',derivatives==[-s.I*g*eps/4,s.I*g*eps/4,s.I*g*eps/4,-s.I*g*eps/4],
      'rho+: (Cdot,Bdot)=(-ig epsilon/4,+ig epsilon/4); rho- reverses both. No universal reduced-state-only closure over arbitrary correlated joint preparations.')

R=OUT/'r4_recovery_authorized_20261017'
def projection(name):
    x=json.loads((R/name).read_text(encoding='utf-8'))
    assert x['exit_code']==0 and x['result']['ok']
    return x['result']['result']['projection']
before=projection('BEFORE_RESULT.json');after=projection('AFTER_RESULT.json')
old={x['id']:x for x in before['active']};new={x['id']:x for x in after['active']}
check('recovery_identity',all(before[f]==after[f] for f in ['context_id','scope','objective','objective_sha256','constraints']),
      'Context, scope, objective hash and constraints are unchanged; revision460 ->462 for invalidate+claim.')
fields=['criterion','depends_on','evidence','review_evidence']
check('recovery_criteria_and_evidence',set(old)==set(new) and all(old[t].get(f)==new[t].get(f) for t in old for f in fields),
      'Every active criterion, dependency and source/review evidence preserved exactly.')
check('recovery_R5_and_settled',old['R5']==new['R5'] and before['settled']==after['settled'],
      'R5 complete record and all settled requirements unchanged byte-equivalent at JSON data level.')
check('recovery_R4_lease',new['R4']['lease']['id']=='dc77ee82-5303-491f-8515-62bc3e2a5248' and new['R4']['lease']['owner']=='codex-gerente-tgl' and new['R4']['status']=='working',
      'R4 new root lease and working status; no acceptance.')
check('recovery_dependents',new['R3']['status']==old['R3']['status']=='needs_revalidation' and new['R10']['status']==old['R10']['status']=='needs_revalidation',
      'R3/R10 remain in revalidation; no new satisfaction.')
recovery=json.loads((R/'RECOVERY_RESULT.json').read_text(encoding='utf-8'))
check('recovery_authorization_pin',recovery['authorization']==pin(R/'AUTORIZACAO_OPERADOR.json'),
      'Recorded direct human authorization and its pin match; this review makes no administrative transition.')
sources=[OUT/'pair_covariance_r59/oh_correlation/EXPLORATION_R59.json',OUT/'pair_covariance_r59/oh_correlation/explore_pairs_r59.py',R/'RECOVERY_RESULT.json',R/'BEFORE_RESULT.json',R/'AFTER_RESULT.json',R/'AUTORIZACAO_OPERADOR.json']
result={'status':'PASS','reviewer':'codex-mission-memory-review','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'checks':checks,'count':len(checks),'source_pins':[pin(p) for p in sources],'script':pin(__file__),
        'scope':'No original script imported/executed; no trajectory, providers, source changes, mission mutation or acceptance. Finite 8-dimensional model only.'}
dest=HERE/'INDEPENDENT_RESULT_R61.json'
with dest.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','count':len(checks),'output':pin(dest)},ensure_ascii=False))
