"""Test one explicitly typed assembly; a nonzero off-diagonal value is not Q2."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
from fractions import Fraction as F
import json,hashlib,time,uuid
import sympy as s
from full_eh_localized_loop_engine import FullEHLoop
from localized_ghost_boundary_engine import FullGhostLoop
from flat_loop_cutoff_engine import tensor
from metric_current_insertion_engine_v2 import CurrentInsertion
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion
from ghost_current_insertion_engine import GhostCurrentInsertion
from localized_source_boundary_engine import source_reduced,einstein
from full_loop_extension_engine import x,z,dx
H=Path(__file__).resolve().parent;D=H/'ward_current_assembly_diagnostic';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),script_sha256=sha(Path(__file__)),
    candidate='pair+source+metric_current/2+one_ordered_mixed_current+complete_ghost_current',
    rationale='Euclidean cumulant/current weights derived independently; check raw-density mapping, not fit any weight',
    includes='Current located at Y with external ghost at Y and ordinary vertex at X',
    excludes='Current located at X with h external and internal ghost; diagonal, curvature, state smoothness, higher arities',
    expected_interpretation='If nonzero away from diagonal, this candidate is not yet the complete Ward identity, never a local anomaly',
    retuning_permitted=False))
start=time.process_time();point=(1,2,-1,1);T=tensor(1,1)
current_rows=json.loads((H/'classical_current_jets/results.json').read_bytes())['rows']
def jets(v):return {word:s.prod(v[i] for i in word) for n in range(4) for word in combinations_with_replacement(range(4),n)}
def ev(f):return s.cancel(f.subs(dict(zip(x,point))).subs(z,sum(v*v for v in point)))
out=[]
for lam,eta in [((0,0,0,0),(0,0,0,0)),((0,0,0,0),(1,0,0,0)),((1,-1,0,0),(1,0,0,0))]:
    X,Y=jets(lam),jets(eta)
    pair=FullGhostLoop(point,T).full_localized(0,X,Y)-F(1,2)*FullEHLoop(point,T).full_localized(0,X,Y)
    C=s.Matrix(4,4,lambda a,b:source_reduced(a,b,0,eta))
    source=ev(einstein(C,lambda f,i:dx(f,i)+lam[i]*f)[1,1])
    metric=CurrentInsertion(T,lam,eta,current_rows,point).off_diagonal()
    mixed=MixedCurrentInsertion(T,0,lam,eta,point).off_diagonal()
    ghost=GhostCurrentInsertion(T,0,lam,eta,point).off_diagonal()
    candidate=s.cancel(pair+source+metric/2+mixed+ghost)
    row=dict(lambda_x=lam,eta_y=eta,pair=str(pair),source=str(source),metric_current=str(metric),
             ordered_mixed_current=str(mixed),ghost_current=str(ghost),candidate_residual=str(candidate))
    out.append(row);print(json.dumps(row),flush=True)
assert out[0]['candidate_residual']=='0'
assert any(s.Rational(row['candidate_residual'])!=0 for row in out[1:])
result=dict(at=datetime.now(timezone.utc).isoformat(),cpu_seconds=time.process_time()-start,rows=out,
    verdict='CANDIDATE_ASSEMBLY_INCOMPLETE_OFF_DIAGONAL',full_Q2=False,weights_refitted=False,
    next='Trace each action-density/current placement, including opposite-endpoint current insertions, before identifying a diagonal anomaly')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(cpu_seconds=result['cpu_seconds'],verdict=result['verdict'])))
