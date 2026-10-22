"""Audit a received partial reduction and independently contract its missing F².

Coefficients were inferred by subtracting the declared partial form from the
previous local complete form BEFORE this test. The subsequent test uses the
literal F² word contraction, not that subtraction, as its left-hand side.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from functools import lru_cache
import hashlib, json, time, uuid
import sympy as s
from ghost_covariant_word_engine import (
    Q, term, add, scale, derivative, trh, divergence, box, F,
    hessian_terms, evaluate, matrix_unit)
from spaceform_covariant_jet_engine import second_curvature_constant

H = Path(__file__).resolve().parent
D = H/'kimi_ghost_reduction_audit'
D.mkdir(exist_ok=True)
receipt = H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/3979f662-13f0-4848-8948-b9dacb8c590e_delivery.json'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p, b):
    assert not p.exists(), p
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b)
    assert t.read_bytes()==b
    t.replace(p)
def put(name,v):
    new(D/name,json.dumps(v,ensure_ascii=False,indent=2).encode())

remote=json.loads(receipt.read_bytes())
new(D/'KIMI_RESPONSE.md',remote['result']['text'].encode('utf-8'))
put('RECEIPT.json',dict(at=remote['at'],job_id=remote['job_id'],
    execution_task_id=remote['execution_task_id'],stage=remote['stage'],
    usage=remote['result']['usage'],model=remote['result']['model'],
    elapsed_seconds=remote['result']['elapsed_seconds'],
    original_receipt_sha256=sha(receipt),response_sha256=sha(D/'KIMI_RESPONSE.md'),
    cost_usd=None,cost_scope='Kimi subscription; no dollar invoice supplied',
    coordinator_textual_review=remote['local_review']))
sources=[Path(__file__),H/'ghost_covariant_word_engine.py',H/'spaceform_covariant_jet_engine.py',
         H/'ghost_curved_hessian/DERIVACAO.md',D/'KIMI_RESPONSE.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Direct F²/48 contraction versus candidate integrated invariant form',
    explored_before_run=True,full_Q2=False,
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time()

def collector():
    result=defaultdict(Q)
    def quad(left,right,c,k=0):
        for (u,a,b),v in left.items():
            for (w,d,e),z in right.items():
                fac=Q(c)*v*z
                result[(k,a,b,d,e,tuple(reversed(u))+w)]+=(-1)**len(u)*fac
                result[(k,d,e,a,b,tuple(reversed(w))+u)]+=(-1)**len(w)*fac
    return result,quad

literal,q=collector()
for m in range(4):
    for n in range(4):
        for a in range(4):
            for b in range(4):
                q(F(m,n,a,b),F(m,n,b,a),Q(1,48))
literal={k:v for k,v in literal.items() if v}
bt=add(*(box(a,a) for a in range(4)))
du=add(*(derivative(divergence(a),a) for a in range(4)))
def lap(f):
    return add(*(derivative(derivative(f,i),i) for i in range(4)))

# Basis: (Boxh)^2,(Boxt)^2,d Boxt,L BoxL,d²,
# K hBoxh,K L²,K dt,K tBoxt,K²h²,K²t².
def invariant_form(c):
    result,q=collector()
    for a in range(4):
        for b in range(4):
            q(box(a,b),box(a,b),c[0])
            q(term((),a,b),box(a,b),c[5],1)
            q(term((),a,b),term((),a,b),c[9],2)
    q(bt,bt,c[1]);q(du,bt,c[2]);q(du,du,c[4])
    for a in range(4):
        q(divergence(a),lap(divergence(a)),c[3])
        q(divergence(a),divergence(a),c[6],1)
    q(du,trh(),c[7],1);q(trh(),bt,c[8],1);q(trh(),trh(),c[10],2)
    return {k:v for k,v in result.items() if v}

delta=[Q(-1,12),Q(1,24),Q(-1,8),Q(-5,24),Q(-1,24),
       Q(7,12),Q(1,6),Q(5,24),Q(-7,32),Q(-2,3),Q(1,6)]
partial=[Q(1,8),Q(1,32),Q(0),Q(1,4),Q(1,8),
         Q(-7,6),Q(-83,24),Q(-89,24),Q(157,96),Q(28,3),Q(-7,3)]
candidate=invariant_form(delta)
partial_candidate=invariant_form(partial)
whole=hessian_terms()
partial_literal={k:whole.get(k,Q())-literal.get(k,Q()) for k in set(whole)|set(literal)}
partial_literal={k:v for k,v in partial_literal.items() if v}

@lru_cache(None)
def jets(Hkey):
    return second_curvature_constant([list(r) for r in Hkey])
def ev(op,T,A,p,o):
    if o<2:
        return evaluate(op,T,A,p,o)
    jj=jets(tuple(tuple(r) for r in A))
    return sum((c*T[a][b]*jj(w,u,v,2-k) for (k,a,b,u,v,w),c in op.items() if T[a][b]),Q())
checks=[];negative=[]
def ck(name,v):
    assert v==0,(name,v)
    checks.append(name)
labels=[(i,j) for i in range(4) for j in range(i,4)]
for i,l in enumerate(labels):
    for r in labels[i:]:
        T,A=matrix_unit(*l),matrix_unit(*r)
        for order in range(3):
            ck(f'delta_{l}_{r}_{order}',ev(literal,T,A,(1,0,0,0),order)-ev(candidate,T,A,(1,0,0,0),order))
            ck(f'partial_{l}_{r}_{order}',ev(partial_literal,T,A,(1,0,0,0),order)-ev(partial_candidate,T,A,(1,0,0,0),order))
T=[[2,-1,1,0],[-1,0,2,1],[1,2,3,-2],[0,1,-2,1]]
A=[[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]]
for order in range(3):
    ck(f'dense_delta_{order}',ev(literal,T,A,(1,2,-1,3),order)-ev(candidate,T,A,(1,2,-1,3),order))
    ck(f'dense_partial_{order}',ev(partial_literal,T,A,(1,2,-1,3),order)-ev(partial_candidate,T,A,(1,2,-1,3),order))

# Conformal reduction including integrated Bochner identity:
# int (Hess f)^2 = int (Box f)^2 +3K f Box f,
# int grad(f).Box grad(f) = -int (Box f)^2 -3K f Box f.
ck('conformal_p4',4*delta[0]+16*delta[1]+4*delta[2]-delta[3]+delta[4])
ck('conformal_K',-3*delta[3]+4*delta[5]-delta[6]+4*delta[7]+16*delta[8]-Q(1,8))
ck('conformal_K2',4*delta[9]+16*delta[10])

# A direct flat ordered IBP control for the sign printed incorrectly by Kimi.
ll,quad=collector()
for a in range(4):
    quad(divergence(a),lap(divergence(a)),1)
wrong=defaultdict(Q)
for a in range(4):
    for b in range(4):
        f=derivative(lap(divergence(b)),a)
        for (w,u,v),c in f.items():
            wrong[(0,min(a,b),max(a,b),u,v,w)]+=2*c
T=A=matrix_unit(0,1)
correct=evaluate(ll,T,A,(1,0,0,0),0)
incorrect=evaluate(wrong,T,A,(1,0,0,0),0)
ck('IBP_negative_sign',correct+incorrect)
assert correct-incorrect!=0
negative.append(dict(name='positive_IBP_printed_in_model',difference=str(correct-incorrect)))
for order in (0,1,2):
    v=ev(literal,T,A,(1,0,0,0),order)
    assert v!=0,(order,v)
    negative.append(dict(name=f'omitted_delta_order{order}',difference=str(v)))
result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='KIMI_PARTIAL_FORM_VERIFIED_AND_F2_REDUCTION_COMPLETED',
    checks=len(checks),check_names=checks,negative_controls=negative,
    delta_coefficients=list(map(str,delta)),partial_coefficients=list(map(str,partial)),
    basis=['(Boxh)^2','(Boxt)^2','d Boxt','L BoxL','d²','K hBoxh','K L²','K dt','K tBoxt','K²h²','K²t²'],
    conformal_delta='K f Boxf/8 modulo divergences',
    corrected_IBP='integral L BoxL = -integral h^(ab) nabla_a Box nabla^r h_rb',
    analytic_heat_assumptions_inherited=True,full_Q2=False,
    cpu_seconds=time.process_time()-cpu)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    sources+[D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('check_names',)},ensure_ascii=False))
