"""Check contact via explicit regulator differentiation, independent of C_D table."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from opposite_endpoint_contact_engine import OppositeEndpointContact
from full_loop_extension_engine import x,z,Q,dx,terms
from logarithmic_contact_engine import residue
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent;D=H/'opposite_endpoint_contact_independent';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists();raw=json.dumps(obj,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
start=time.process_time();checks=0;a=s.Symbol('regulator');out=[]
for label,r,lam,eta in [((1,1),0,(1,-1,0,0),(1,0,0,0)),((0,2),2,(0,1,-1,0),(1,0,0,-1))]:
    graph=OppositeEndpointContact(LABELS.index(label),r,lam,eta)
    for kind in ['metric','mixed']:
        direct=s.Integer(0)
        for (pw,cw),f in graph.raw_blocks(kind).items():
            g=f
            # z^-a O[z^a f]; constant exponentials lambda/eta retained.
            for i in pw:g=s.expand(-dx(g,i)-2*a*x[i]*g/z-lam[i]*g)
            for i in cw:g=s.expand(dx(g,i)+2*a*x[i]*g/z-eta[i]*g)
            linear=s.expand(g).coeff(a,1)
            direct+=sum(c*residue(n,p,(1,1,1,1)) for n,p,c in terms(linear))
        direct=s.expand(direct.subs({Q[i]:Q[i]-lam[i] for i in range(4)},simultaneous=True))
        table=graph.extension_contact(kind)
        assert s.expand(direct-table)==0;checks+=1
        row=dict(h=label,c=r,kind=kind,lambda_x=lam,eta_y=eta,polynomial=str(table),
            independent_regulator_equal=True,blocks=len(graph.raw_blocks(kind)),cpu_seconds=time.process_time()-start)
        out.append(row);print(json.dumps({k:v for k,v in row.items() if k!='polynomial'}),flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,rows=out,
    scope='Current-X rational contact normalized by CE, two tensors/two ghosts; no logarithmic generalization',full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'results.json']]))
