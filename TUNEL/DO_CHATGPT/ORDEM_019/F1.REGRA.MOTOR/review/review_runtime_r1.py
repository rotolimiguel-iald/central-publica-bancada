"""Independent parity-channel oracle and custody audit for the frozen finite motor."""
from pathlib import Path
import ast, datetime, hashlib, importlib.util, json, math, subprocess, sys, time
import numpy as np
from scipy.linalg import expm

OUT = Path(__file__).resolve().parents[1]
REVIEW = Path(__file__).resolve().parent
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
DEST = REVIEW / ('runtime_' + STAMP)
DEST.mkdir(exist_ok=False)
START = datetime.datetime.now(datetime.timezone.utc).isoformat()
TIMER = time.perf_counter()
CHECKS = []
def h(data): return hashlib.sha256(data).hexdigest()
def pin(path):
    p = Path(path); b = p.read_bytes()
    return {'path': str(p), 'sha256': h(b), 'bytes': len(b)}
def new(name, data):
    if not isinstance(data, bytes): data=(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
    with (DEST/name).open('xb') as f: f.write(data)
def check(name, condition, **details):
    CHECKS.append({'name':name,'passed':bool(condition),**details})
    assert condition, name
def load(path): return json.loads(Path(path).read_bytes())

freeze_path = OUT/'runtime/freezes/20261014T142932_627224Z.json'
original_result_path = OUT/'runtime/runs/20261014T142949_979804Z/RESULT.json'
try:
    frozen = load(freeze_path)
    for e in frozen['files']:
        p=OUT/e['relative_path']; b=p.read_bytes()
        check('frozen_'+e['relative_path'],h(b)==e['sha256'] and len(b)==e['bytes'])
    spec=load(OUT/'PREREGISTRO_R1.json'); manifest=load(OUT/'SOURCE_MANIFEST.json')
    original=load(original_result_path)
    check('freeze_precedes_execution',frozen['created_utc'] < original['start_utc'])
    seal=load(OUT/'sources/um_absoluto_selo.json')
    proof=load(OUT/'sources/tgl_kernel_proof_manifest.json')
    bancada=load(OUT/'BANCADA_STATE_R1.json')['canonical']
    check('seal_proof_formal_source_link',seal['formal_source_hash']==proof['formal_source_hash'],value=seal['formal_source_hash'])
    check('bancada_um_identity',h((OUT/'sources/um.py').read_bytes())==bancada['um_py_sha256'])
    check('bancada_seal_identity',h((OUT/'sources/um_absoluto_selo.json').read_bytes())==bancada['seal_sha256'])
    src=ast.parse((OUT/'sources/um.py').read_bytes()); ext=ast.parse((OUT/'sources/actual_consumer_functions.py').read_bytes())
    funcs=manifest['functions']; orig_nodes={n.name:n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in funcs}
    ex_nodes={n.name:n for n in ext.body if isinstance(n,ast.FunctionDef)}
    check('five_exact_AST_functions',set(orig_nodes)==set(ex_nodes)==set(funcs) and all(ast.dump(orig_nodes[k])==ast.dump(ex_nodes[k]) for k in funcs))
    assignments=[n for n in ext.body if isinstance(n,ast.Assign)]
    check('no_other_extracted_toplevel',len(ext.body)==6 and len(assignments)==1 and assignments[0].targets[0].id=='SEALED_CODATA_ALPHA')
    alpha=ast.literal_eval(assignments[0].value)
    check('runtime_beta_not_literal',original['beta_runtime']==alpha*math.sqrt(math.e))
    command=[sys.executable,'-B','-X','utf8',str(OUT/'runtime/run_rule_motor.py'),'--replay',str(freeze_path)]
    replay_start=datetime.datetime.now(datetime.timezone.utc).isoformat(); rt=time.perf_counter()
    proc=subprocess.run(command,cwd=DEST,capture_output=True)
    new('REPLAY_STDOUT.log',proc.stdout); new('REPLAY_STDERR.log',proc.stderr)
    replay_handle=json.loads(proc.stdout.decode().strip().splitlines()[-1]); replay_path=Path(replay_handle['result']); replay=load(replay_path)
    new('REPLAY_RECEIPT.json',{'command':command,'cwd':str(DEST),'start_utc':replay_start,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-rt,'exit_code':proc.returncode,'result':pin(replay_path)})
    check('independent_process_replay',proc.returncode==0 and replay['passed'] and replay['checks_passed']==76)
    for artifact in original['artifacts']:
        p=OUT/artifact['relative_path']; b=p.read_bytes()
        check('artifact_'+p.name,h(b)==artifact['sha256'] and len(b)==artifact['bytes'])
    trajectory_path=original_result_path.parent/'TRAJECTORY.jsonl'
    replay_trajectory=replay_path.parent/'TRAJECTORY.jsonl'
    check('trajectory_reproduced_byte_for_byte',trajectory_path.read_bytes()==replay_trajectory.read_bytes())
    rows=[json.loads(line) for line in trajectory_path.read_bytes().splitlines()]
    previous='0'*64
    for i,item in enumerate(rows):
        q={k:v for k,v in item.items() if k!='sha256'}
        computed=h(json.dumps(q,ensure_ascii=False,separators=(',',':'),sort_keys=True,allow_nan=False).encode())
        assert item['index']==i and item['previous_sha256']==previous and item['sha256']==computed
        previous=computed
    check('hash_chain_complete',len(rows)==241 and previous==original['trajectory_last_hash'])
    # Independent representation: random-unitary parity channel and analytic spectrum.
    Z=np.diag([1.,1.,-1.,-1.]); I=np.eye(16)
    gamma=alpha*math.sqrt(math.e)/2
    generator=gamma/2*(np.kron(Z,Z)-I)
    psi=np.array([1,1j,1,-1j])/2; initial=np.outer(psi,psi.conj())
    target=np.array(spec['target_real'])+1j*np.array(spec['target_imag'])
    errors=[]; eigen_errors=[]; rule_errors=[]
    for item in rows:
        r=item['record']; u=r['exposure']; t=u/gamma
        state=np.array(r['state_real'])+1j*np.array(r['state_imag'])
        predicted=(expm(t*generator)@initial.reshape(-1)).reshape(4,4)
        errors.append(float(np.linalg.norm(state-predicted)))
        expected_eigen=np.array([0,0,(1-math.exp(-u))/2,(1+math.exp(-u))/2])
        eigen_errors.append(float(np.linalg.norm(np.linalg.eigvalsh(state)-expected_eigen)))
        direct_read=(state+Z@state@Z)/2
        rule_errors.append(float(np.linalg.norm(direct_read-target)))
        assert r['read_rule'] and not r['raw_rule'] and r['verdict']=='SATISFACTION_ADMITTED'
    check('parity_expm_oracle',max(errors)<1e-12,maximum=max(errors))
    check('analytic_density_spectrum',max(eigen_errors)<1e-12,maximum=max(eigen_errors))
    check('direct_reading_verdict',max(rule_errors)<1e-12,maximum=max(rule_errors))
    check('generator_nullity_eight',np.linalg.matrix_rank(generator,tol=1e-10)==8)
    # General states and linear operators, beyond the preregistered trajectory.
    specmod=importlib.util.spec_from_file_location('reviewed_runtime',OUT/'runtime/run_rule_motor.py'); mod=importlib.util.module_from_spec(specmod); specmod.loader.exec_module(mod)
    env,parts,records=mod.load_actual(); result,captured=mod.capture_consumer(env,parts)
    rng=np.random.default_rng(714010); residuals=[]; covariance=[]
    B=np.zeros((4,4),complex)
    for sl in (slice(0,2),slice(2,4)):
        a=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); q,_=np.linalg.qr(a); B[sl,sl]=q
    for _ in range(12):
        a=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); state=a@a.conj().T; state/=np.trace(state)
        for u in (0,.173,1.719,7.33):
            predicted=(expm(u/gamma*generator)@state.reshape(-1)).reshape(4,4)
            actual=captured['recognize_flow'](state,u/gamma)
            residuals.append(float(np.linalg.norm(actual-predicted)))
            covariance.append(float(np.linalg.norm(captured['recognize_flow'](B@state@B.conj().T,u/gamma)-B@actual@B.conj().T)))
    check('random_state_expm_oracle_48',max(residuals)<1e-12,maximum=max(residuals))
    check('block_unitary_covariance_48',max(covariance)<1e-12,maximum=max(covariance))
    retained=np.eye(4)/4; motor=mod.RuleMotor(captured,target,spec,parts['external_ladder']['per_theorem'])
    check('independent_fixed_state_rejected',motor.evaluate(retained,3.0)['verdict']=='SATISFACTION_REFUSED')
    check('zero_contrast_not_unique_truth',np.linalg.norm(captured['recognize'](retained)-retained)==0 and np.linalg.norm(retained-target)>spec['tol_rule'])
    for bad in (np.float64('nan'),np.float64('inf'),np.bool_(True),-np.finfo(float).tiny):
        try: motor.evaluate(initial,bad)
        except mod.ContractError: pass
        else: raise AssertionError('independent invalid scalar accepted')
    check('independent_scalar_types_refused',True)
    # Frozen inputs are rechecked after all execution; no science-source rewrite.
    for e in frozen['files']: assert h((OUT/e['relative_path']).read_bytes())==e['sha256']
    check('all_frozen_inputs_unchanged',True)
    passed=True; error=None
except Exception as exc:
    passed=False; error=repr(exc)
summary={'passed':passed,'scope':'FINITE_SYNTHETIC_RUNTIME_ONLY','checks':CHECKS,'checks_passed':sum(c['passed'] for c in CHECKS),'error':error,'start_utc':START,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-TIMER,'script':pin(__file__),'freeze':pin(freeze_path),'original_result':pin(original_result_path),'scope_notes':['u=Gamma*t removes beta from the trajectory versus exposure; beta determines reference time only.','Reading rule already holds at u=0; raw state converges while reading stays fixed.','Fixed algebra has complex dimension8, not a unique fixed state.','Continuous time, finite-dimensional synthetic model; no physical data or production installation.'],'artifacts':[pin(p) for p in sorted(DEST.iterdir()) if p.is_file()]}
new('REVIEW_RUNTIME_R1.json',summary)
print(json.dumps({'passed':passed,'result':str(DEST/'REVIEW_RUNTIME_R1.json'),'checks':summary['checks_passed'],'error':error}))
raise SystemExit(0 if passed else 1)
