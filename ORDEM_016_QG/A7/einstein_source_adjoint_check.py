"""Compute source(E test,c) without substituting a flat E into a curved symbol."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
from einstein_source_adjoint_engine import source_adjoint
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'einstein_source_adjoint';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'einstein_source_adjoint_engine.py',H/'einstein_test_field_engine.py',H/'einstein_test_field/results.json',
 H/'source_flat_full_fourier/results.json',H/'curved_harmonic_fourier_engine.py',H/'curved_source_jet_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Full singular source evaluated at Einstein-adjoint tensor test through first K',
 identity='E=-Box Itr-1/2 Itr G Gdagger Itr+2K Id+K g tr is formally self-adjoint on compact tests',
 method='E acts on the full RNC parallel tensor plane, then raising and volume; raw source kernels; Fischer Fourier with original regulator',
 checks='flat against full Fourier source; firstK three invariants and independent nonaxis holdout',
 exclusions=['full cutoff hierarchy','W','tadpole','higher arities','full Q2'],sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();prior=json.loads((H/'source_flat_full_fourier/results.json').read_bytes());data=[];checks=[]
fixtures=[(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))];p=(1,0,0,0)
def run(ti,p,v,order):
    T=s.Matrix(4,4,BASIS[ti]);value=source_adjoint(T,p,v,order)
    row=dict(order=order,T=ti,p=p,v=v,full=list(map(str,value)))
    data.append(row);print(json.dumps(dict(**row,cpu=time.process_time()-cpu)),flush=True)
    return value
for ti,v in fixtures:
    value=run(ti,p,v,0);ref=next(r for r in prior['values'] if r['label']=='Einstein_'+str(ti))
    for j in range(3):assert value[j]==s.Rational(ref['full'][j]);checks.append('flat_'+str((ti,j)))
def basis(ti,p,v):
    T=s.Matrix(4,4,BASIS[ti]);p=s.Matrix(p);v=s.Matrix(v)
    return [p.dot(p)*(p.T*T*v)[0],(p.T*T*p)[0]*p.dot(v),p.dot(p)*s.trace(T)*p.dot(v)]
fit=s.Matrix([basis(ti,p,v) for ti,v in fixtures]).inv()*s.Matrix([run(ti,p,v,1) for ti,v in fixtures])
p=(1,2,-1,1);v=(2,-1,1,3);value=run(4,p,v,1);pred=s.Matrix([basis(4,p,v)])*fit
for j in range(3):assert value[j]==pred[j],(j,value[j],pred[j]);checks.append('nonaxis_'+str(j))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FIRSTK_SOURCE_ADJOINT_BULK_SYMBOL_MEASURED',
 coefficients=[[str(fit[i,j]) for j in range(3)] for i in range(3)],basis=['p2 Tpv','pTp pv','p2 trT pv'],
 log_basis=['1','FourierLog','FourierLog^2'],values=data,checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-cpu,
 full_Q2=False,scope='Explicit adjoint source bulk symbol only, before pair/tadpole/W/higher arities')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('values','check_names')}))
