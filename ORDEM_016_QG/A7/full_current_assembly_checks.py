"""Predetermined nonaxial/tensor controls of all current placements."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,time,uuid
import sympy as s
from full_eh_localized_loop_engine import FullEHLoop
from localized_ghost_boundary_engine import FullGhostLoop
from position_metric_bubble_engine import BASIS,LABELS
from classical_current_jet_engine import current_coefficients,split_word
from metric_current_insertion_engine_v2 import CurrentInsertion
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion
from ghost_current_insertion_engine import GhostCurrentInsertion
from opposite_endpoint_current_engine import OppositeEndpointCurrent
from localized_source_boundary_engine import source_reduced,einstein
from full_loop_extension_engine import x,z,dx

H=Path(__file__).resolve().parent;D=H/'full_current_assembly_checks';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)

@lru_cache(None)
def rows_for(r):
    rows=[]
    for a in range(10):
        for b in range(a,10):
            data=[]
            for m,c in current_coefficients(a,b,r).items():
                pw,qw,kw=split_word(m)
                data.append(dict(pword=pw,qword=qw,kword=kw,current=list(map(str,c))))
            rows.append(dict(a=a,b=b,coefficients=data))
    return rows

def jets(v):return {word:s.prod(v[i] for i in word) for n in range(4) for word in combinations_with_replacement(range(4),n)}
cases=[
    ((0,1),0,(1,0,-1,0),(0,1,0,1),(2,-1,1,3)),
    ((2,2),0,(0,0,0,0),(1,-1,1,0),(1,2,-1,1)),
    ((0,3),1,(1,0,0,-1),(0,1,-1,0),(-1,1,2,3)),
    ((1,1),1,(1,-1,0,0),(0,0,0,0),(2,1,-1,1)),
    ((1,2),2,(0,1,-1,0),(1,0,0,-1),(1,-2,3,1)),
    ((3,3),2,(1,1,-1,0),(-1,0,1,1),(-2,1,1,2)),
    ((0,0),3,(0,0,0,0),(0,0,0,0),(1,3,2,-1)),
    ((2,3),3,(1,-1,1,-1),(1,0,-1,1),(3,1,-1,2)),
]
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),cases=cases,
    weights='pair=ghost-metric/2; source; Ymetric/2+Ymixed+Yghost; Xmetric+Xmixed',
    no_refitting=True,stop_on_nonzero=False,full_Q2=False,script_sha256=sha(Path(__file__))))
start=time.process_time();out=[]
for n,(label,r,lam,eta,point) in enumerate(cases):
    a=LABELS.index(label);T=BASIS[a];X,Y=jets(lam),jets(eta)
    pair=FullGhostLoop(point,T).full_localized(r,X,Y)-F(1,2)*FullEHLoop(point,T).full_localized(r,X,Y)
    Hsource=s.Matrix(4,4,lambda i,j:source_reduced(i,j,r,eta))
    source=einstein(Hsource,lambda f,i:dx(f,i)+lam[i]*f)[label[0],label[1]]
    # Contract the symmetric external tensor: off-diagonal basis has two entries.
    multiplicity=1 if label[0]==label[1] else 2
    source=s.cancel(multiplicity*source.subs(dict(zip(x,point))).subs(z,sum(v*v for v in point)))
    metric=CurrentInsertion(T,lam,eta,rows_for(r),point).off_diagonal()
    mixed=MixedCurrentInsertion(T,r,lam,eta,point).off_diagonal()
    ghost=GhostCurrentInsertion(T,r,lam,eta,point).off_diagonal()
    opposite=OppositeEndpointCurrent(a,r,lam,eta,point)
    xm=opposite.off_diagonal('metric');xb=opposite.off_diagonal('mixed')
    total=s.cancel(pair+source+metric/2+mixed+ghost+xm+xb)
    row=dict(case=n,h=label,c=r,lambda_x=lam,eta_y=eta,point=point,
        pair=str(pair),source=str(source),Ymetric=str(metric),Ymixed=str(mixed),Yghost=str(ghost),
        Xmetric=str(xm),Xmixed=str(xb),residual=str(total),cpu_seconds=time.process_time()-start)
    out.append(row);put(f'case_{n}.json',row);print(json.dumps(row),flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),cases=out,cpu_seconds=time.process_time()-start,
    sampled_zero_count=sum(s.Rational(row['residual'])==0 for row in out),sampled_case_count=len(out),
    full_Q2=False,gate_changed=False,weights_refitted=False,
    proof_scope='Exact finite controls, not universal identity in external jets')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
