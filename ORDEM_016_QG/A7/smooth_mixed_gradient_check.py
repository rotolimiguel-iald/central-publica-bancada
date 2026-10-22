"""Expose derivative-index antisymmetric terms invisible for constant W."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import hashlib,json,time,uuid
import sympy as s
from smooth_mixed_gradient_engine import gradient_tensor,variable_hessian_component,fiber_metric
from position_metric_bubble_engine import BASIS,LABELS
H=Path(__file__).resolve().parent;D=H/'smooth_mixed_gradient';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(raw)
    assert q.read_bytes()==raw;q.replace(p)
source=H/'flat_mixed_smooth_bubble/results.json'
inputs=[Path(__file__),H/'smooth_mixed_gradient_engine.py',source,
 H/'position_metric_bubble_engine.py',H/'ghost_direct_position_engine.py',
 H/'position_metric_ordered_operator_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Actual gradient bilinear tensor before integrating derivatives past diagonal W',
    method='Exact sparse contractions; compare quadratic constant symbol; retain derivative-index antisymmetric part',
    no_new_prescription=True,sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=[];records={};old=json.loads(source.read_bytes())
def ck(n,v):assert s.expand(v)==0,(n,v);checks.append(n)
p=s.Matrix(s.symbols('p0:4'));p2=p.dot(p);eye=s.eye(4);x=s.symbols('x0:4')
for sector in ['metric_I','metric_T','ghost_I']:
 T=gradient_tensor(sector)
 for a,b,i,j in product(range(10),range(10),range(4),range(4)):
  ck((sector,'transpose',a,b,i,j),s.Rational(T.get((a,b,i,j),0)-T.get((b,a,j,i),0)))
 co=list(map(s.Rational,old['sectors'][sector]['coefficients']))
 for a,A0 in enumerate(BASIS):
  A=s.Matrix(4,4,A0)
  for b,B0 in enumerate(BASIS):
   B=s.Matrix(4,4,B0)
   inv=[p2*s.trace(A*B),p2*s.trace(A)*s.trace(B),
       (p.T*A*p)[0]*s.trace(B)+(p.T*B*p)[0]*s.trace(A),(p.T*A*B*p)[0]]
   actual=-sum(s.Rational(T.get((a,b,i,j),0))*p[i]*p[j] for i in range(4) for j in range(4))
   ck((sector,'constant_symbol',a,b),actual-sum(u*v for u,v in zip(co,inv)))
 anti={key:(value-T.get((key[0],key[1],key[3],key[2]),0))/2 for key,value in T.items()}
 anti={key:value for key,value in anti.items() if value}
 # Construct a detector of the antisymmetric term if one is present.
 negative=None
 if anti:
  (a,b,i,j),value=next(iter(anti.items()))
  h=[s.S.Zero]*10;h[b]=x[j];w=x[i]
  T_sym={key:(v+T.get((key[0],key[1],key[3],key[2]),0))/2 for key,v in T.items()}
  actual=variable_hessian_component(T,a,h,w,x)
  sym=variable_hessian_component(T_sym,a,h,w,x)
  diff=s.expand(actual-sym)
  ck((sector,'negative_value'),diff+s.Rational(value)/fiber_metric(a))
  assert diff!=0
  negative=dict(fiber_output=LABELS[a],fiber_input=LABELS[b],w=str(w),
                h_component=str(h[b]),full=str(actual),symmetric_only=str(sym),difference=str(diff))
 records[sector]=dict(nonzero_components=len(T),derivative_antisymmetric_count=len(anti),
    antisymmetric_detector=negative,
    tensor=[dict(a=a,b=b,i=i,j=j,value=str(v)) for (a,b,i,j),v in sorted(T.items())])
 print(sector,len(T),len(anti),negative,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='VARIABLE_SMOOTH_CONTACT_GRADIENT_TENSOR_EXPLICIT',checks=len(checks),
 cpu_seconds=time.process_time()-cpu,sectors=records,
 bilinear='integral w(Y) partial_i h_A T_ij^{AB} partial_j h_B',
 hessian='(N_w h)_A=-(1/m_A) partial_i(w T_ij^{AB} partial_j h_B)',
 full_Q2=False,prescription_changed=False,
 scope='Flat mixed contact with smooth diagonal value, including its induced gradient; direct smooth firstjet source is separate')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='sectors'},ensure_ascii=False))
