"""Documentary continuation delta only. No launcher, sampler, or sample reads."""
import ast,copy,hashlib,json,math,time
from pathlib import Path
from datetime import datetime,timezone,timedelta
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
OLD=B/'bis/e3_pyring_preparation';NEW=B/'bis/e3_kerr_continuation'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def diff(a,b,prefix=''):
    if isinstance(a,dict) and isinstance(b,dict):
        out={}
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out[prefix+k]=[a.get(k),b.get(k)]
            else:out.update(diff(a[k],b[k],prefix+k+'.'))
        return out
    return {} if a==b else {prefix.rstrip('.'):[a,b]}
def main():
    started=time.perf_counter();cpu=time.process_time();checks=[]
    result_path=HERE/'KERR_CONTINUATION_REVIEW.json'
    if result_path.exists():raise FileExistsError(result_path)
    def check(name,ok,detail=None):
        if not ok:raise RuntimeError(name)
        checks.append(dict(name=name,passed=True,detail=detail))
    manifest=load(NEW/'MANIFEST.json');parent=load(OLD/'MANIFEST_v3.json')
    mhash=sha(NEW/'MANIFEST.json')
    check('requested_manifest_hash',mhash=='e9c777586c6c148d47d93e0dc082b28d7b370062c90babb9316ccbb855ed00d3')
    check('parent_manifest_pin',sha(OLD/'MANIFEST_v3.json')==manifest['parent_manifest_sha256'])
    check('five_runtime_files_exact_set',set(manifest['code_sha256'])=={'conditioning.py','controller.py','custody.py','kerr_model.py','runner.py'})
    check('no_unpinned_python_in_copy',{p.name for p in NEW.glob('*.py')}==set(manifest['code_sha256']))
    for n,h in manifest['code_sha256'].items():check('byte_identity_'+n,sha(NEW/n)==sha(OLD/n)==h==parent['code_sha256'][n])
    oldcfg=load(OLD/'CONFIG.json');cfg=load(NEW/'CONFIG.json');delta=diff(oldcfg,cfg)
    check('exact_three_config_changes',delta==manifest['changes'] and set(delta)=={'sampler.maxcall','variants','output_relative_to_Chatgpt'},delta)
    check('new_cap_and_single_branch',cfg['sampler']['maxcall']==3000000 and cfg['variants']==['public_psd'])
    check('wall_caps_unchanged',cfg['wall_envelope_seconds']==7200 and cfg['variant_wall_seconds']['public_psd']==1800)
    for name,h in manifest['source_and_config_pins'].items():
        p=(ROOT/name).resolve()
        if not p.is_relative_to(ROOT.resolve()) or p.suffix.lower() in ('.h5','.hdf5','.gwf'):raise RuntimeError('Forbidden data read in delta review')
        check('pin_'+name,sha(p)==h)
    authorizer=B/'refeito/activate_kerr_continuation_013bis.py';ahash=sha(authorizer)
    check('builder_pin',sha(B/'refeito/prepare_kerr_continuation_013bis.py')==manifest['script_sha256'])
    original=B/'cache/E3_KERR220_CALIBRATION_V1'
    envelope=load(original/'ENVELOPE.json');cost=load(original/'COST.json');conv=load(original/'public_psd/CONVERGENCE.json')
    failure=load(original/'welch/FAILURE.json');diag=load(B/'bis/e3_kerr_failure_diagnostic/DIAGNOSTIC.json')
    auth=load(B/'bis/E3_KERR_AUTHORIZATION_V1.json');reg=B/'RINGDOWN_5SIGMA_V1.json'
    check('original_authorization_chain',sha(B/'bis/E3_KERR_AUTHORIZATION_V1.json')==envelope['authorization_sha256'] and auth['E2_registration_sha256']==sha(reg))
    check('F0_unchanged',sha(B/'bis/F0_CLOSED_20260922T215825Z.json')==auth['F0_receipt_sha256'])
    check('B2_unchanged',sha(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md')==auth['B2_delivery_sha256'])
    check('prior_cleanup_receipts',len(cost['runs'])==2 and all(r['cleanup']['group_absent'] is True for r in cost['runs']))
    check('partial_not_accepted',conv['status']=='PARTIAL_MAXCALL_NOT_ACCEPTED' and conv['accepted_for_analysis'] is False and conv['before_add_live'] is True)
    check('partial_independent_metadata_failures',conv['ncall']>=oldcfg['sampler']['maxcall'] and conv['delta_logz']>=oldcfg['sampler']['dlogz'] and conv['posterior_samples']<oldcfg['sampler']['minimum_posterior_samples'])
    check('Welch_failure_retained',failure['status']=='FAILED_NO_ACCEPTED_COMPARISON' and diag['cond_observations'][0]['condition_number']>1e12)
    deadline=datetime.fromisoformat(envelope['stop_utc'])
    check('same_absolute_deadline',manifest['original_envelope_stop_utc']==envelope['stop_utc'] and deadline.tzinfo is not None)
    check('not_expired_at_review',datetime.now(timezone.utc)<deadline)
    projected=conv['cost']['wall_seconds']*cfg['sampler']['maxcall']/conv['ncall']
    check('linear_projection_arithmetic',math.isclose(projected,manifest['cost_projection_INPUT']['linear_3million_call_projection_seconds'],rel_tol=1e-14))
    tree=ast.parse(authorizer.read_text());mainnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    tests=[n for n in mainnode.body if isinstance(n,ast.If)]
    # Evaluate ONLY original guard predicates with artificial metadata, never main.
    gate=next(n.test for n in tests if 'review[\'status\']' in ast.unparse(n.test))
    authgate=next(n.test for n in tests if 'review[\'authorizer_sha256\']' in ast.unparse(n.test))
    priorgate=next(n.test for n in tests if 'priorcost' in ast.unparse(n.test))
    envgate=next(n.test for n in tests if 'configuration' in ast.unparse(n.test))
    def predicate(node,**values):return eval(compile(ast.Expression(node),'<isolated guard predicate>','eval'),dict(Path=Path,__file__=str(authorizer),sha=lambda p: ahash if Path(p)==authorizer else mhash,manifest=NEW/'MANIFEST.json',**values))
    review=dict(status='KERR_CONTINUATION_DELTA_CLOSED',blocking_findings=[],manifest_sha256=mhash,authorizer_sha256=ahash)
    check('review_gate_positive',not predicate(gate,review=review) and not predicate(authgate,review=review))
    for name,value in [('status','OPEN'),('blocking_findings',['BLOCKER']),('manifest_sha256','0'*64),('authorizer_sha256','0'*64)]:
        bad=dict(review);bad[name]=value
        check('review_gate_negative_'+name,predicate(authgate if name=='authorizer_sha256' else gate,review=bad))
    check('deadline_substitution_refused',predicate(envgate,configuration={'original_envelope_stop_utc':'2099-01-01'},envelope=envelope))
    badcost=copy.deepcopy(cost);badcost['runs'][0]['cleanup']['group_absent']=False
    check('prior_live_group_receipt_refused',predicate(priorgate,priorcost=badcost))
    check('prior_missing_run_refused',predicate(priorgate,priorcost={'runs':cost['runs'][:1]}))
    calls=[n for n in ast.walk(mainnode) if isinstance(n,ast.Call)]
    runs=[n for n in calls if isinstance(n.func,ast.Attribute) and ast.unparse(n.func)=='subprocess.run']
    check('single_controller_no_outer_timeout',len(runs)==1 and not any(k.arg=='timeout' for k in runs[0].keywords))
    deadline_node=next(n.value for n in mainnode.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='deadline' for t in n.targets))
    for label,hard in [('hard_later',deadline+timedelta(days=1)),('hard_earlier',deadline-timedelta(seconds=20))]:
        selected=eval(compile(ast.Expression(deadline_node),'<deadline expression>','eval'),dict(time_guard=lambda reg:hard,reg={},datetime=datetime,envelope=envelope))
        check(label+'_deadline_min',selected==min(hard,deadline))
    for name,h in manifest['code_sha256'].items():check('final_source_'+name,sha(NEW/name)==h)
    check('final_manifest_authorizer',sha(NEW/'MANIFEST.json')==mhash and sha(authorizer)==ahash)
    result=dict(status='KERR_CONTINUATION_DELTA_CLOSED',blocking_findings=[],manifest_sha256=mhash,authorizer_sha256=ahash,
        created_utc=datetime.now(timezone.utc).isoformat(),scope='Documentary computational delta and isolated metadata predicates; no launcher or scientific execution',
        config_diff=delta,runtime_code_sha256=manifest['code_sha256'],checks=checks,check_count=len(checks),
        original_deadline_utc=envelope['stop_utc'],prior_partial_metadata={k:conv[k] for k in ('status','ncall','delta_logz','threshold','posterior_samples','ess','accepted_for_analysis')},
        historical_Welch=dict(condition_number=diag['cond_observations'][0]['condition_number'],threshold=1e12,scope='Existing diagnostic receipt read only; no recalculation'),
        cost=dict(prior_controller_wall_seconds=cost['wall_seconds'],prior_public_runner_wall_seconds=conv['cost']['wall_seconds'],
          forecast_new_attempt_seconds=projected,forecast_old_total_plus_new_seconds=cost['wall_seconds']+projected,
          forecast_status='INPUT_LINEAR_COST_ONLY_NOT_CONVERGENCE_GUARANTEE',new_public_attempt_cap_seconds=1800,
          scope='Fresh restart with same seed, not state resume. Earlier cost is retained. 1800s is per new attempt; sum of attempts is not asserted capped at1800. Original absolute two-hour envelope limits all attempts.'),
        review_wall_seconds=time.perf_counter()-started,review_parent_cpu_seconds=time.process_time()-cpu,
        script_sha256=sha(__file__),builder_sha256=sha(B/'refeito/prepare_kerr_continuation_013bis.py'),
        input_metadata_pins={str(p.relative_to(ROOT)):sha(p) for p in [original/'ENVELOPE.json',original/'COST.json',original/'public_psd/CONVERGENCE.json',original/'welch/FAILURE.json',B/'bis/E3_KERR_AUTHORIZATION_V1.json',reg]},
        limits=['No partial samples inspected or used for comparison','No PSD, prior, seed, SNR or source selection','Welch remains a failed branch; public-only result cannot establish PSD robustness','Cleanup absence is witnessed by prior receipts; no independent live process sweep here','Kerr reproduction equivalent and E3.1 scientific acceptance remain unpaid','Zero controller exit still requires variant/convergence review'],
        scientific_execution=False,launcher_executed=False,authorization_created=False)
    save(result_path,result)
    report=f'''# Kerr: fechamento do delta de continuação

[REAL — bytes/metadados e predicados finitos; INPUT — projeção de custo; OPEN — execução e convergência]

**Delta fechado, sem bloqueantes no escopo solicitado.** Manifesto `{mhash}`; ativador `{ahash}`. Foram{len(checks)} verificações, sem executar launcher/controller ou ciência. Os cinco fontes runtime são byte-idênticos aos originais. CONFIG difere somente em maxcall1m→3m, variants→public_psd e output→cacheV2; priors, seed, dados, PSD e critérios permanecem iguais.

Deadline absoluto preservado: **{envelope['stop_utc']}**. O ativador reduz a validade a min(deadline original, orçamento E2); o controlador idêntico recebe esse limite, portanto não renova duas horas. O ramo público mantém1800s por tentativa. Isso não é um teto cumulativo1800s somando a tentativa anterior: o teto compartilhado é o deadline absoluto original. O custo anterior não desaparece.

Os metadados do parcial confirmam ncall={conv['ncall']}, delta_logz={conv['delta_logz']} contra0,1 e N={conv['posterior_samples']} contra1000. ESS={conv['ess']} não compensa essas falhas. Nenhuma amostra foi aberta ou comparada. Welch permanece falha pelo condicionamento registrado, sem relaxar limiar/refazer PSD; só público não pode ser chamado robustez PSD paga.

Projeção linear: {conv['cost']['wall_seconds']:.6f}s×3000000/{conv['ncall']}={projected:.6f}s para a nova tentativa. É reinício com mesma seed, não retomada de estado; custo total anterior+essa projeção={cost['wall_seconds']+projected:.6f}s, sem promessa de convergência nem custo uniforme. O principal deve somar custos realizados, incluindo tentativas/diagnóstico, no marco.

E2/F0/B2 e autorização original conferiram em hashes; os dois recibos de cleanup declaram grupos ausentes. Não executei varredura de processos. O ativador exige status/hash deste review, hash próprio, deadline igual ao original e grupos fechados nos recibos; preserva tentativas existentes e não impõe timeout externo concorrente. Predicados negativos de parecer/pin/autor/deadline/grupo foram conferidos isoladamente, sem chamar main.

**PAGO:** delta computacional/custódia. **NÃO PAGO:** resultado convergido, comparação científica e equivalência GWOSC/C00_AR/PSD/versão. Execução futura continua ato do principal; retorno0 não aceita posterior.

Recibo KERR_CONTINUATION_REVIEW.json SHA256 `{sha(result_path)}`. Custo próprio: {result['review_wall_seconds']:.6f}s parede e {result['review_parent_cpu_seconds']:.6f}s CPU. Nenhuma fonte/manifesta anterior foi alterada.
'''
    save(HERE/'KERR_CONTINUATION_REVIEW.md',report)
    print(json.dumps(dict(status=result['status'],checks=len(checks),manifest_sha256=mhash,authorizer_sha256=ahash,receipt_sha256=sha(result_path),review_wall_seconds=result['review_wall_seconds'])))
if __name__=='__main__':main()
