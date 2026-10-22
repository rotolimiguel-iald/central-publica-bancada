"""Assemble full EH localized metric bubbles and retain nonzero boundary flux."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from fractions import Fraction as F
from flat_loop_cutoff_engine import FlatLoop,tensor
from full_eh_localized_loop_engine import FullEHLoop

H=Path(__file__).resolve().parent;D=H/'full_eh_localized_loop';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'full_eh_localized_loop_engine.py',H/'localized_eh_cubic_engine.py',H/'localized_eh_cubic/manifest.json',H/'flat_loop_cutoff/manifest.json']
for parent in ['localized_eh_cubic','flat_loop_cutoff']:
 for row in json.loads((H/parent/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Full EH correction at both metric loop vertices; all cutoff derivatives required by adjunction',
 scope='Off diagonal flat kernels; boundary flux need not vanish; not quantum anomaly or causal extension',full_Q2=False))
cpu=time.process_time();checks=0;point=(1,2,-1,1);zero=(0,)*4;zh=((0,)*4,)*4
previous=json.loads((H/'flat_loop_cutoff/results.json').read_bytes());rows=[]
cases=[('constant',{():1},{():1}),('Y_gradient',{():1},{():1,(0,):1}),
 ('XY_gradient',{():1,(0,):1,(1,):-1},{():1,(0,):1}),
 ('Y_hessian',{():1},{():1,(0,0):1,(0,1):2,(1,1):-1}),
 ('X_hessian',{():1,(0,0):1,(0,1):2,(1,1):-1},{():1}),
 ('Y_third_jet',{():1},{():1,(0,0,1):1})]
for a,b in [(1,1),(0,1)]:
 engine=FullEHLoop(point,tensor(a,b));ghost=FlatLoop('ghost',point,tensor(a,b));mult=1 if a==b else 2
 old=next(v for v in previous['rows'] if v['kind']=='metric' and (v['a'],v['b'])==(a,b))
 for label,xj,yj in cases:
    full=[engine.full_localized(r,xj,yj)/mult for r in range(4)]
    gx=tuple(xj.get((i,),0) for i in range(4));gy=tuple(yj.get((i,),0) for i in range(4))
    hy=tuple(tuple(yj.get(tuple(sorted((i,j))),0) for j in range(4)) for i in range(4))
    gg=[engine.localized(r,1,gx,1,gy,hy)/mult for r in range(4)]
    gh=[ghost.localized(r,1,gx,1,gy,hy)/mult for r in range(4)]
    if label=='constant':assert full==gg and all(g-m/2==0 for g,m in zip(gh,full));checks+=8
    if label in [v['case'] for v in old['cutoffs']]:
      expected=list(map(F,next(v['values'] for v in old['cutoffs'] if v['case']==label)))
      assert gg==expected;checks+=4
    assert all(isinstance(v,F) for v in full);checks+=4
    row=dict(a=a,b=b,case=label,full_metric=list(map(str,full)),GammaGamma=list(map(str,gg)),
      metric_boundary_correction=[str(v-w) for v,w in zip(full,gg)],
      ghost_minus_half_full_metric=[str(g-m/2) for g,m in zip(gh,full)])
    rows.append(row);put(str(a)+str(b)+'_'+label+'.json',row)
    print('FULL_LOOP',a,b,label,'cpu',time.process_time()-cpu,flush=True)
assert any(F(v) for row in rows for v in row['metric_boundary_correction']);checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,point=point,rows=rows,
 full_Q2=False,gate_changed=False,scope='Full EH flat off-diagonal cubic bubble localization; no source/cutoff BRST current/extension summed')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
