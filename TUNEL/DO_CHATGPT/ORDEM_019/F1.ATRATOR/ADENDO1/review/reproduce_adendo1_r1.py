"""Independent numerical audit in matrix-unit basis; no canonical execution."""
from pathlib import Path
import ast, datetime, hashlib, json, math, re, time
import numpy as np
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'review'
RESULT=BASE/'numerical/RESULTADOS_ADENDO1_R1.json'
PREREG=BASE/'PREREGISTRO_ADENDO1_R1.json'
TARGET=OUT/'REPRODUCAO_NUMERICA_R1.json'
assert not TARGET.exists()
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); tick=time.perf_counter()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def norm(a):
 a=np.asarray(a); assert np.isfinite(a).all(); return float(np.linalg.norm(a))
def unpack(x):
 a=np.array(x); return a[...,0]+1j*a[...,1]
def write(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
 with Path(p).open('xb') as f:f.write(b)
 assert Path(p).read_bytes()==b
q=load(PREREG); r=load(RESULT)
freeze=load(BASE/'FREEZE_ADENDO1_R1.json')
manifest=load(BASE/'numerical/RUN_MANIFEST_R1.json'); receipt=load(BASE/'numerical/RUN_RECEIPT_R1.json')
assert r['numeric_contract']==q['numeric']
assert r['preregister_sha256']==sha(PREREG)==manifest['preregister_sha256']
assert r['script_sha256']==sha(manifest['script_path'])==manifest['script_sha256']
assert sha(manifest['launcher_path'])==manifest['launcher_sha256']
assert sha(RESULT)==receipt['result_sha256'] and receipt['exit_code']==0
assert freeze['created_utc'] < manifest['created_utc'] < r['started_utc'] < r['finished_utc']
for p in freeze['files']: assert sha(p['path'])==p['sha256']
assert r['sources_before']==r['sources_after'] and r['all_source_pins_unchanged']
for p in r['sources_before']: assert sha(p['path'])==p['sha256']
for v in q['verbatims']:
 raw=Path(v['source']).read_bytes()
 assert raw==Path(v['custody']).read_bytes()==v['verbatim_utf8'].encode('utf-8')
 assert hashlib.sha256(raw).hexdigest()==v['sha256']
source=Path(r['alpha_source']['path']).read_bytes().decode('utf-8-sig')
lines=[s for s in source.splitlines() if s.startswith('ALPHA_FINE_CODATA_2018') and '=' in s]
assert len(lines)==1
alpha=ast.literal_eval(ast.parse(lines[0]).body[0].value)
sealed=[a for a in ast.parse(source).body if isinstance(a,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SEALED_CODATA_ALPHA' for t in a.targets)]
assert len(sealed)==1 and alpha==ast.literal_eval(sealed[0].value)
beta=alpha*math.sqrt(math.e); lam=1-2*beta
assert beta==r['beta_runtime'] and 0<beta<1
atol=q['numeric']['atol']; rtol=q['numeric']['rtol']; tol=atol+rtol
I=np.eye(2,dtype=complex); J=np.array([[0,1],[1,0]],complex); K=np.diag([1,-1]).astype(complex)
basis=[]
for i in range(2):
 for j in range(2):
  e=np.zeros((2,2),complex); e[i,j]=1; basis.append(e)
def superop(fn): return np.column_stack([fn(e).reshape(4) for e in basis])
C=superop(lambda A:J@A@J); E=(np.eye(4)+C)/2
read=lambda A:(A+J@A@J)/2
measured={'J_squared_I':norm(J@J-I),'JKJ_negative_K':norm(J@K@J+K),'AdJ_fixes_J':norm(J@J@J-J),'E_fixes_J':norm(read(J)-J),'E_squared_E':norm(E@E-E),'Ad_E':norm(C@E-E),'E_Ad':norm(E@C-E),'E_K_zero':norm(read(K)),'E_I':norm(read(I)-I)}
for key,val in measured.items():
 assert val<=tol and abs(val-r['A5']['primary_residuals'][key])<=tol
rng=np.random.default_rng(q['numeric']['seed']); randommax=0.0
for _ in range(q['numeric']['random_operators']):
 A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
 randommax=max(randommax,norm(read(read(A))-read(A)),norm(J@read(A)@J-read(A)),norm(read(J@A@J)-read(A)))
assert randommax<=tol
Evals=np.linalg.eigvalsh(E)
assert np.allclose(Evals,[0,0,1,1],atol=atol,rtol=rtol) and r['A5']['E_fixed_dimension']==2
literal=norm(J@J-J); assert literal>tol and literal==r['A5']['literal_diagnostic']['residual']
Jb=2*J; Eb=superop(lambda A:(A+Jb@A@Jb)/2)
controls={'K_identity_JKJ_plus_K':norm(J@I@J+I),'K_identity_EK':norm(read(I)),'J_bad_involution':norm(Jb@Jb-I),'J_bad_E_idempotence':norm(Eb@Eb-Eb),'J_bad_self_reading':norm((Jb+Jb@Jb@Jb)/2-Jb)}
reported=[r['A5']['controls']['K_identity']['JKJ_plus_K'],r['A5']['controls']['K_identity']['E_K_zero_error'],r['A5']['controls']['J_bad_twice_J']['involution_error'],r['A5']['controls']['J_bad_twice_J']['E_idempotence_error'],r['A5']['controls']['J_bad_twice_J']['E_Jbad_error']]
for value,expected in zip(controls.values(),reported): assert value>tol and abs(value-expected)<=tol
# Independent density superoperator in matrix-unit basis, then compare via unitary Pauli change.
S=np.array([[math.sqrt(1-beta),math.sqrt(beta)],[-math.sqrt(beta),math.sqrt(1-beta)]],complex)
D=lambda A:np.diag(np.diag(A))
DC=superop(lambda A:D(S@D(A)@S.conj().T))
Y=np.array([[0,-1j],[1j,0]],complex)
U=np.column_stack([A.reshape(4)/math.sqrt(2) for A in [I,J,Y,K]])
T=np.abs(S)**2
reported_primary={x['id']:x for x in r['primary']}
assert norm(T-unpack(reported_primary['primary_population']['matrices']['T']))<=tol
assert norm(DC-U@unpack(reported_primary['primary_density']['matrices']['T'])@U.conj().T)<=tol
R=np.outer(I.reshape(4),I.reshape(4).conj())/2
assert norm(DC@R-R)<=tol and norm(R@DC-R)<=tol and norm(R@R-R)<=tol
assert norm(np.linalg.matrix_power(DC,4096)-R)<=tol
# Audit every recorded matrix, rederive fixed projection using Hermitian eigendecomposition.
checked=[]
for x in r['primary']+r['A6']['ablations']+[r['A6']['diagnostic_old_readout']]:
 t=unpack(x['matrices']['T']); rr=unpack(x['matrices']['R_evaluated']); d=t.shape[0]
 assert norm(t-t.conj().T)<=tol
 ev,vec=np.linalg.eigh(t); take=np.abs(ev-1)<q['numeric']['rank_threshold']
 intrinsic=vec[:,take]@vec[:,take].conj().T
 assert int(np.sum(take))==x['fixed_dimension']
 assert norm(intrinsic-unpack(x['matrices']['R_intrinsic']))<=tol
 values={'RT':norm(rr@t-rr),'TR':norm(t@rr-rr),'R_squared_R':norm(rr@rr-rr),'R_star_R':norm(rr.conj().T-rr),'R_is_Fix_projection':norm(rr-intrinsic)}
 for k,v in values.items(): assert abs(v-x['residuals'][k])<=tol
 dist=[]
 for item in x['powers']:
  value=norm(np.linalg.matrix_power(t,item['n'])-rr)
  assert abs(value-item['distance_to_readout'])<=tol
  dist.append(value)
 fixed_spectrum=ev[take]; transient=ev[~take]
 a1=norm(rr-intrinsic)<=tol and bool(np.all(np.abs(transient)<1)) and dist[-1]<=tol
 a2=values['RT']<=tol and values['TR']<=tol
 a3=values['R_squared_R']<=tol and values['R_star_R']<=tol and values['R_is_Fix_projection']<=tol
 actual=[a1,a2,a3]; expected=[x[k]=='PASSA' for k in ['A1','A2','A3']]
 assert actual==expected
 checked.append({'id':x['id'],'fixed_dimension':int(np.sum(take)),'A1_A2_A3':actual,'final_distance':dist[-1]})
survivors=[x['id'] for x in r['A6']['ablations'] if x['admissible'] and x['A1_A2_A3_survive']]
assert survivors==r['A6']['surviving_admissible_ablations'] and len(survivors)>0
assert r['A6']['verdict']=='FALHA' and r['A5']['verdict']=='PASSA'
# Actual iteration and partial sums, independently of the constructor's analytic labels.
N=r['A6']['external_affine_control']['iterations']; x=0.; total=0.; increments=[]
for n in range(N):
 assert math.isfinite(x) and x==n
 total+=x; old=x; x=x+1.; increments.append(x-old)
mean=total/N
assert N>0 and all(v==1 for v in increments) and x==N and mean==(N-1)/2
assert x==r['A6']['external_affine_control']['final_x'] and mean==r['A6']['external_affine_control']['cesaro_0_to_N_minus_1']
assert r['A6']['no_support_control']['available_trace']==0 and r['A6']['no_support_control']['required_trace']==1
assert r['A6']['no_support_control']['verdict']=='RECUSA_NAO_VACUIDADE'
pins=[{'path':str(p),'sha256':sha(p)} for p in [PREREG,RESULT,BASE/'FREEZE_ADENDO1_R1.json',BASE/'numerical/RUN_MANIFEST_R1.json',BASE/'numerical/RUN_RECEIPT_R1.json',Path(manifest['script_path']),Path(manifest['launcher_path']),Path(__file__)]]
report={'schema':'F1.ATRATOR.ADENDO1.independent-numeric/v1','verdict':'PASSA_REVISAO','started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-tick,'method':'Independent matrix-unit basis E_ij, eigendecomposition instead of SVD, source alpha reread, actual affine loop; original runner neither imported nor executed','pins':pins,'source_pin_count':len(r['sources_before']),'all_source_pins_reread':True,'frozen_contract_equal':True,'beta_runtime':beta,'lambda_runtime':lam,'A5':{'verdict':'PASSA','residuals':measured,'random_max':randommax,'fixed_eigenvalues':Evals.tolist(),'literal_J_squared_equals_J':'FALHA','literal_residual':literal,'control_residuals':controls},'A6':{'verdict':'FALHA','checked':checked,'survivors':survivors,'identity_alone_suffices':True,'theta_zero_and_beta_zero_coincide':True,'seven_rows_are_not_independent_ablation_evidence':True,'affine_iteration':{'N':N,'final_x':x,'mean':mean,'all_increments_one':True,'divergence_argument':'x_n=n and mean_N=(N-1)/2 for N>0, unbounded as N tends to infinity; outside finite CPTP class'},'no_support':'RECUSA: no normalized trace-one state'},'limits':['A5 readout is E_J on operators, not state readout R.','J is real swap extended complex linearly, not general antiunitary Tomita J.','Controls reject missing hypotheses; they do not falsify under those hypotheses.','Removing a supplied interface does not remove an intrinsic fixed projection.','Finite samples are checks; geometric spectral formulas justify the convergence assertion.','No empirical observation, statistical significance, ontology or gate tested.']}
write(TARGET,report)
print(json.dumps({'verdict':report['verdict'],'A5':report['A5']['verdict'],'A6':report['A6']['verdict'],'sha256':sha(TARGET),'source_pins':report['source_pin_count']},ensure_ascii=False))
