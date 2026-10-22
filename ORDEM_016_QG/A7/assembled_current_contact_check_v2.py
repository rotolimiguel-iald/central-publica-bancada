"""Measured contact polynomial of the specified flat bilocal Ward sector."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from full_loop_extension_engine import SymbolicRawLoop,loop_contact,Q
from position_metric_bubble_engine import BASIS,LABELS
from metric_current_insertion_engine_v3 import CurrentInsertion
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion
from ghost_current_insertion_engine import GhostCurrentInsertion
from opposite_endpoint_contact_engine import OppositeEndpointContact
from localized_source_boundary_engine import source_extension

H=Path(__file__).resolve().parent;D=H/'assembled_current_contact_v2';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists();raw=json.dumps(obj,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
cases=[((0,0,0,0),(0,0,0,0)),((0,0,0,0),(1,0,0,0)),((1,-1,0,0),(1,0,0,0))]
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),cases=cases,h=[1,1],c=0,
    extension='FP[(1-a)mu^(2a)z^a f], normalized by C_E=-4pi^2',
    assembly='ghost_pair-metric_pair/2+source+Ymetric/2+Ymixed+Yghost+Xmetric+Xmixed',
    claim='A local polynomial in one flat bilocal sector, NOT fullQ2',
    script_sha256=sha(Path(__file__)),opposite_engine_sha256=sha(H/'opposite_endpoint_contact_engine.py')))
start=time.process_time();rows=[];T=BASIS[LABELS.index((1,1))]
currents=json.loads((H/'classical_current_jets/results.json').read_bytes())['rows']
qvalue=dict(zip(Q,(1,2,-1,1)))
for n,(lam,eta) in enumerate(cases):
    parts={}
    parts['ghost_pair']=loop_contact(SymbolicRawLoop('ghost',T,lam,eta),0)
    parts['metric_pair']=loop_contact(SymbolicRawLoop('metric',T,lam,eta),0)
    parts['source']=source_extension(0,lam,eta)[1,1]
    parts['Ymetric']=CurrentInsertion(T,lam,eta,currents).extension_contact()
    parts['Ymixed']=MixedCurrentInsertion(T,0,lam,eta).extension_contact()
    parts['Yghost']=GhostCurrentInsertion(T,0,lam,eta).extension_contact()
    opposite=OppositeEndpointContact(LABELS.index((1,1)),0,lam,eta)
    parts['Xmetric']=opposite.extension_contact('metric')
    parts['Xmixed']=opposite.extension_contact('mixed')
    total=s.expand(parts['ghost_pair']-parts['metric_pair']/2+parts['source']+parts['Ymetric']/2+
        parts['Ymixed']+parts['Yghost']+parts['Xmetric']+parts['Xmixed'])
    assert s.Poly(total,*Q).total_degree()<=5
    if not any(lam):assert parts['Xmetric']==parts['Xmixed']==0
    if not any(eta):assert parts['Ymetric']==parts['Ymixed']==parts['Yghost']==0
    row=dict(case=n,lambda_x=lam,eta_y=eta,parts={k:str(v) for k,v in parts.items()},
        polynomial=str(total),parts_at_q={k:str(v.subs(qvalue)) for k,v in parts.items()},
        value_at_q=str(total.subs(qvalue)),cpu_seconds=time.process_time()-start)
    rows.append(row);put(f'case_{n}.json',row)
    print(json.dumps({k:v for k,v in row.items() if k not in ['parts']}),flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),rows=rows,cpu_seconds=time.process_time()-start,
    Q2_complete=False,gate_changed=False,renormalization_changed=False,
    scope='Selected component of flat contact after all computed current placements; tadpoles/smooth/curved/higher sectors remain')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'opposite_endpoint_contact_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
