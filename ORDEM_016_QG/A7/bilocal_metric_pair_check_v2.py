"""Run the metric endpoint-divergence control at the same fixed point as ghost."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from fractions import Fraction as F
import bilocal_metric_pair_engine_v2 as E
import position_metric_ordered_operator_engine as M
H=Path(__file__).resolve().parent;D=H/'bilocal_metric_pair_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_metric_pair_engine_v2.py',H/'bilocal_metric_pair_engine.py',H/'bilocal_ghost_pair_engine.py',
 H/'bilocal_covariant_jet_engine.py',H/'bilocal_first_curvature_engine.py',
 H/'position_metric_ordered_operator_engine.py',H/'metric_curvature_vertices.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Actual metric loop B0/B1 and both firstK potential vertices in Y Ward divergence',
 point=[1,0,0,0],external_h='e11 in local orthonormal frame',external_Dh=0,
 normalization='Raw metric contraction /16; combine separately with -1/2 and ghost',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();checks=[]
assert isinstance(E.frob(E.empty(1),E.empty(1))/16,float)
assert isinstance(F(E.frob(E.empty(1),E.empty(1)),16),F)
checks.append(('empty_sum_float_regression',))
point=(1,0,0,0);J=E.MetricPointJets(point)
G0,G1,GL,d0,d1=M.green_integer(point)
for order in (0,1):
    actual=J.matrix(order);refs=(G0,[{} for _ in range(50)]) if order==0 else (G1,GL)
    den=d0 if order==0 else d1
    for ell in (0,1):
        for i in range(50):
            for j in range(50):
                v=actual[ell][i].get(j,F())-F(refs[ell][i].get(j,0),den)
                assert v==0,(order,ell,i,j,v);checks.append((order,ell,i,j))
    print('METRIC_GREEN_MATCH',order,len(checks),'cpu',time.process_time()-cpu,flush=True)
def progress(o,b,row):print(json.dumps(dict(order=o,b=b,value=list(map(str,row)),cpu=time.process_time()-cpu)),flush=True)
values,J=E.metric_ward_point(point,E.tensor(1,1),progress,jets=J)
for o in (0,1):
    for row in values[o]:
        for value in row:
            assert isinstance(value,F),(o,value,type(value));checks.append(('exact_output_type',))
    for b in (1,2,3):
        assert values[o][b]==(0,0),(o,b,values[o][b]);checks.append(('axial_parity',o,b))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='METRIC_LOOP_Y_DIVERGENCE_POINT_EXACT_MEASURED',
 checks=len(checks),cpu_seconds=time.process_time()-cpu,
 values=[[[str(t) for t in row] for row in rows] for rows in values],
 log_basis=['1','log(mu²x²)'],point=point,external_tensor='e11',external_Dh=0,
 full_Q2=False,source=False,tadpole=False,distribution_extension=False,
 scope='Raw metric pair with both potential insertions, endpoint IBP, hX jet only')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
