"""Independent numerical audit; no import or execution of the submitted runner."""
from pathlib import Path
import ast,datetime,decimal,difflib,hashlib,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
N=ROOT/'numerical'; OUT=ROOT/'review'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def new(p,o):
 with Path(p).open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2,allow_nan=False)
p=json.loads((ROOT/'PREREGISTRO_R1.json').read_text())
r=json.loads((N/'RESULTADOS_NUMERICOS_R3.json').read_text())
pins=[]
for item in p['source_pins']:
 actual=sha(item['path']);assert actual==item['sha256'];pins.append({'path':item['path'],'sha256':actual})
for k in (1,2,3):
 receipt=json.loads((N/f'RUN_RECEIPT_R{k}.json').read_text())
 assert receipt['script_sha256']==sha(N/f'run_optical_r{k}.py')
 assert receipt['log_sha256']==sha(N/f'RUN_R{k}.log')
 assert receipt['preregister_sha256']==sha(ROOT/'PREREGISTRO_R1.json')
 assert receipt['exit_code']==(0 if k==3 else 1)
 if k==3:assert receipt['result_sha256']==sha(N/'RESULTADOS_NUMERICOS_R3.json')
 assert p['created_utc']<receipt['started_utc']<receipt['finished_utc']
um=next(i for i in p['source_pins'] if Path(i['path']).name=='um.py')
text=Path(um['path']).read_bytes().decode('utf-8-sig')
lines=[s for s in text.splitlines() if s.startswith('ALPHA_FINE_CODATA_2018 =')];assert len(lines)==1
alpha_literal=lines[0].split('=',1)[1].strip(); alpha=ast.literal_eval(alpha_literal)
a=ast.parse(text)
sealed=[v for v in a.body if isinstance(v,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SEALED_CODATA_ALPHA' for t in v.targets)]
assert len(sealed)==1 and ast.literal_eval(sealed[0].value)==alpha
beta=alpha*math.sqrt(math.e);lam=1-2*beta;assert beta==r['beta_runtime']
I=np.eye(2);R=np.ones((2,2))/2;T=np.array([[1-beta,beta],[beta,1-beta]])
S=np.array([[math.sqrt(1-beta),math.sqrt(beta)],[-math.sqrt(beta),math.sqrt(1-beta)]])
basis=[]
for i in range(2):
 for j in range(2):
  a=np.zeros((2,2));a[i,j]=1;basis.append(a)
def dephase(a):return np.diag(np.diag(a))
def primary(a):return dephase(S@dephase(a)@S.T)
def rotated(a):
 b=S@a@S.T
 return S.T@(math.exp(-1)*b+(1-math.exp(-1))*dephase(b))@S
def mat(fn):return np.column_stack([fn(b).flatten() for b in basis])
M=mat(primary);Md=mat(rotated);Rd=mat(lambda a:S.T@dephase(S@a@S.T)@S)
Rho=np.zeros((4,4));Rho[np.ix_([0,3],[0,3])]=.5
models={'primary_population':(T,R,1),'primary_density':(M,Rho,1),'identity_population':(I,I,2),'rotated_dephasing':(Md,Rd,2)}
checks={}
for name,(m,proj,fd) in models.items():
 vals,vecs=np.linalg.eigh(m);d=m.shape[0];sel=abs(vals-1)<1e-10;Rp=vecs[:,sel]@vecs[:,sel].T
 assert sel.sum()==fd==r['models'][name]['fixed_dimension']
 residuals={k:float(np.linalg.norm(v,2)) for k,v in {'RT':proj@m-proj,'TR':m@proj-proj,'RR':proj@proj-proj,'spectral':proj-Rp}.items()}
 assert max(residuals.values())<=1e-10
 eigstored=np.array(r['models'][name]['eigenvalues']);assert np.max(abs(vals-eigstored))<1e-14
 last=float(np.linalg.norm(np.linalg.matrix_power(m,4096)-proj,2));assert last<=1e-10
 means=[]
 for n in p['numerics']['cesaro_lengths']:
  accum=np.zeros_like(m);power=np.eye(d)
  for k in range(n):accum+=power;power=power@m
  distance=float(np.linalg.norm(accum/n-proj,2))
  expected=next(x for x in r['models'][name]['cesaro'] if x['N']==n)['distance_to_R']
  assert abs(distance-expected)<=1e-10
  means.append({'N':n,'distance_to_R':distance,'submitted_distance_to_R':expected})
 checks[name]={'fixed_dimension':int(fd),'eigenvalues':vals.tolist(),'residuals':residuals,'distance_4096_independent':last,'distance_4096_submitted':r['models'][name]['powers'][-1]['distance_to_R'],'cesaro':means}
# Independent recurrence for the affine control, rather than assigning outcomes from labels.
x=0.;acc=0.;actual={};means={}
for n in range(4097):
 if n in p['numerics']['powers']:actual[n]=x
 if n in p['numerics']['cesaro_lengths']:means[n]=acc/n
 acc+=x;x=x+1.
assert all(v==n for n,v in actual.items())
assert all(v==(n-1)/2 for n,v in means.items())
# High precision bound for the EXACT real channel, distinct from floating point accumulated error.
with decimal.localcontext() as c:
 c.prec=110;D=decimal.Decimal
 b=D(alpha_literal)*D(1).exp().sqrt();l=1-2*b;bound=l**4096
 exact_cesaro=(1-l**4096)/(4096*(1-l))
 high={'beta':str(b),'lambda':str(l),'exact_operator_error_at_4096':str(bound),'exact_cesaro_error_at_4096':str(exact_cesaro),'digits':110}
# Save complete diffs and assert that scientific code from beta through the matrices/checks is unchanged.
old=(N/'run_optical_r1.py').read_text();current=(N/'run_optical_r3.py').read_text()
def scientific_tail(t):
 s=t[t.index('    beta = float(alpha * math.sqrt(math.e))'):]
 s=s.replace('RESULTADOS_NUMERICOS_R1.json','RESULTADOS_NUMERICOS_R3.json')
 s=s.replace("'alpha':alpha,","'alpha':alpha,'alpha_assignment_line':alpha_source_line,'alpha_reader_scope':'Unique unindented source line in embedded module; cross-checked with wrapper SEALED_CODATA_ALPHA AST top level',") if "'alpha_assignment_line'" not in s else s
 return s
assert scientific_tail(old)==scientific_tail(current)
with (OUT/'DIFF_RUNNER_R1_R3.txt').open('x',encoding='utf-8',newline='\n') as f:f.writelines(difflib.unified_diff(old.splitlines(True),current.splitlines(True),fromfile='run_optical_r1.py',tofile='run_optical_r3.py'))
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit':'independent_no_runner_import','status':'PASSA','pins':pins,'preregister_sha256':sha(ROOT/'PREREGISTRO_R1.json'),'result_sha256':sha(N/'RESULTADOS_NUMERICOS_R3.json'),'runner_sha256':sha(N/'run_optical_r3.py'),'script_sha256':sha(__file__),'alpha_literal':alpha_literal,'beta_runtime':beta,'models':checks,'affine':{'trajectory':actual,'cesaro':means,'A1_direct':'FALHA_ESPERADA','A1_cesaro':'FALHA_ESPERADA'},'high_precision_exact_channel':high,'scientific_tail_R1_R3_identical_after_output_metadata_normalization':True,'scope':'Finite synthetic equations and implementation only; no physical creditation and no Lean review'}
new(OUT/'REPRODUCAO_NUMERICA_R1.json',result)
print(json.dumps({'status':result['status'],'beta_runtime':beta,'models':{k:{'fixed_dimension':v['fixed_dimension'],'distance_4096':v['distance_4096_independent']} for k,v in checks.items()},'high_precision':high},indent=2))
