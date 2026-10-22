"""Verify off-shell localized cubic BV flux without setting total momentum zero."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from fractions import Fraction as F
from localized_brst_flux_engine import v2,green_current,cubic_bv_flux,add,neg,dot
from position_metric_bubble_engine import BASIS

H=Path(__file__).resolve().parent;D=H/'localized_brst_flux';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'localized_brst_flux_engine.py',H/'metric_principal_vertices.py',H/'metric_boundary_current_engine.py',H/'full_localized_vertices_delivery/manifest.json',H/'antifield_vertex/DERIVACAO_FONTE.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Full quadratic Green current and off-shell cubic BV cutoff flux',
 warning='Classical h2c sector only; not free-BRST primitive alone, not quantum Q2',full_Q2=False))
start=time.process_time();checks=0;rows=[];negative=[]
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
p=(1,2,-1,1);q=(2,-1,0,3);k=(0,1,1,0);c=(2,-1,1,3)
for ia,A in enumerate(BASIS):
 for ib,B in enumerate(BASIS):
    J=green_current(A,p,B,q)
    eq(dot(add(p,q),J),v2(A,p,B,q)-v2(A,neg(q),B,q))
    # Alternate momenta exercise the same degree-two current on a second point.
    pp=(-2,1,3,0);qq=(0,1,-1,2)
    eq(dot(add(pp,qq),green_current(A,pp,B,qq)),v2(A,pp,B,qq)-v2(A,neg(qq),B,qq))
    f=cubic_bv_flux(A,p,B,q,c,k)
    eq(f['ward_lhs'],f['divergence'])
    eq(f['ward_lhs'],-dot(neg(f['total']),f['current']))
    z=cubic_bv_flux(A,p,B,q,c,neg(add(p,q)))
    eq(z['ward_lhs'],0)
    if f['density_flux']!=f['ward_lhs']:
        negative.append(dict(fibers=[ia,ib],omit_green_current_defect=str(f['density_flux']-f['ward_lhs'])))
    if f['ward_lhs']:
        rows.append(dict(fibers=[ia,ib],current=list(map(str,f['current'])),
          lhs=str(f['ward_lhs']),divergence=str(f['divergence']),cubic=str(f['cubic']),euler=str(f['euler'])))
 assert checks==50*(ia+1)
 print('FLUX_FIBER',ia,'checks',checks,'cpu',time.process_time()-start,flush=True)
assert rows and negative;checks+=2
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 total_momentum=add(p,q,k),nonzero_cases=rows,negative_controls=negative,full_Q2=False,
 identity='V3(Gc,U,V)+2<EU,LV>+2<EV,LU> = Q.J_BV, J_BV=2c V2-2Jgreen(LU,V)-2Jgreen(LV,U)',
 scope='Off-shell classical cubic BV boundary current; same raw normalizations; not all localized master equation terms')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,cpu_seconds=result['cpu_seconds'],nonzero_cases=len(rows),negative_controls=len(negative),example=rows[0])))
