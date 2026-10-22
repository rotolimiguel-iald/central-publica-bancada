"""Exact checks and diagnostic, keeping the pre-existing assembly immutable."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement,product
from fractions import Fraction as F
import json,hashlib,time,uuid
import sympy as s
from opposite_endpoint_current_engine import OppositeEndpointCurrent,external_adjoint
from full_loop_extension_engine import x,z
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent;D=H/'opposite_endpoint_current';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists();raw=json.dumps(obj,indent=2).encode()
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    candidate='previous_candidate_residual+metric_current_at_X+mixed_current_at_X',
    scope='Flat off-diagonal two-contraction current placement; not full Q2',
    current_real_scale='+Jraw/(16kappa)',metric_propagator='-4kappa*S*f',
    b_h_propagator='-Gtranspose(d)*f',weights_refitted=False,
    script_sha256=sha(Path(__file__)),engine_sha256=sha(H/'opposite_endpoint_current_engine.py')))
start=time.process_time();checks=0
p=s.symbols('p0:4');lam=(1,-1,0,0);eta=(1,0,0,0)
for n in range(3):
    for hw in combinations_with_replacement(range(4),n):
        for cw in [()]+[(i,) for i in range(4)]:
            actual=sum(v*s.prod(p[i] for i in word) for word,v in external_adjoint(hw,cw,lam,eta).items())
            expected=s.prod(-(p[i]+lam[i]) for i in hw)*s.prod(p[i]-eta[i] for i in cw)
            assert s.expand(actual-expected)==0;checks+=1
previous=json.loads((H/'ward_current_assembly_diagnostic/results.json').read_bytes())['rows']
point=(1,2,-1,1);rows=[]
for old in previous:
    lam=tuple(old['lambda_x']);eta=tuple(old['eta_y'])
    graph=OppositeEndpointCurrent(LABELS.index((1,1)),0,lam,eta,point)
    values={kind:graph.off_diagonal(kind) for kind in ['metric','mixed']}
    for kind,v in values.items():
        expr=graph.symbolic_after_product(kind)
        exact=expr.subs(dict(zip(x,point))).subs(z,sum(v*v for v in point))
        assert s.cancel(exact-s.Rational(v.numerator,v.denominator))==0;checks+=1
    residual=s.Rational(old['candidate_residual'])+sum(values.values())
    row=dict(lambda_x=lam,eta_y=eta,previous_residual=old['candidate_residual'],
        metric_at_X=str(values['metric']),mixed_at_X=str(values['mixed']),
        assembled_residual=str(residual),metric_terms=len(graph.metric),mixed_terms=len(graph.mixed),
        second_h_derivative_terms=sum(len(key[0])==2 for key in graph.metric))
    rows.append(row);print(json.dumps(row),flush=True)
    if not any(lam):assert all(v==0 for v in values.values());checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),rows=rows,checks=checks,
    cpu_seconds=time.process_time()-start,full_Q2=False,gate_changed=False,weights_refitted=False,
    all_sampled_residuals_zero=all(s.Rational(row['assembled_residual'])==0 for row in rows),
    proof_scope='Exact evaluation of sampled configurations and jet-adjoint identities, not universal Ward closure')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'opposite_endpoint_current_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,cpu_seconds=result['cpu_seconds'],all_sampled_residuals_zero=result['all_sampled_residuals_zero'])))
