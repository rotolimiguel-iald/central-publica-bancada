"""Static/AST/hash verification only. Does not import candidates or run tests."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'proveniencia'))
from audit_provenance import atomic,metadata
OLD=OUT.parent/'p3_init_qualified_003'
DST=OUT/'candidate'
checks=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
def tree(p):
    return ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
def dump(node):
    return ast.dump(node,include_attributes=False)
def fn(t,name):
    return next(x for x in ast.walk(t) if isinstance(x,ast.FunctionDef) and x.name==name)
def call_name(node):
    return ast.unparse(node.func) if isinstance(node,ast.Call) else None
def selected_calls(t,names):
    return sorted(dump(x) for x in ast.walk(t) if isinstance(x,ast.Call) and call_name(x) in names)
asts={}
for p in sorted(OUT.rglob('*.py')):
    asts[str(p.relative_to(OUT))]=tree(p)
    check('syntax:'+str(p.relative_to(OUT)),True)
old_source=tree(OLD/'src/pseob_source.py')
new_source=tree(DST/'src/pseob_source.py')
class StripSourceAudit(ast.NodeTransformer):
    def visit_FunctionDef(self,node):
        if node.name in {'set_audit_checkpoint','audit_checkpoint'}:return None
        return self.generic_visit(node)
    def visit_Assign(self,node):
        if any(isinstance(t,ast.Name) and t.id=='AUDIT_CHECKPOINT' for t in node.targets):return None
        return self.generic_visit(node)
    def visit_Expr(self,node):
        if isinstance(node.value,ast.Call) and call_name(node.value)=='audit_checkpoint':return None
        return self.generic_visit(node)
check('source_ast_exact_after_removing_only_audit_instrumentation',
      dump(old_source)==dump(StripSourceAudit().visit(copy.deepcopy(new_source))))
check('source_signature_exact',dump(fn(old_source,'pseob_frequency_domain').args)==dump(fn(new_source,'pseob_frequency_domain').args))
d=tree(DST/'driver_p3.py');od=tree(OLD/'driver_p3.py')
l=tree(DST/'launch_p3.py');ol=tree(OLD/'launch_p3.py')
for t,label in [(d,'driver'),(l,'supervisor')]:
    body=fn(t,'main').body
    check(label+'_entrypoint_preparation_refusal',isinstance(body[0],ast.Raise) and 'PREPARATION_ONLY' in ast.unparse(body[0]))
check('audit_policy_predicates_exact',
      [dump(x.test) for x in ast.walk(fn(d,'audit')) if isinstance(x,ast.If)]==
      [dump(x.test) for x in ast.walk(fn(od,'audit')) if isinstance(x,ast.If)])
def allowlist(t):
    rows=[]
    for x in ast.walk(t):
        if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='allowed_data' for a in x.targets):rows.append(dump(x))
        if isinstance(x,ast.AugAssign) and isinstance(x.target,ast.Name) and x.target.id=='allowed_data':rows.append(dump(x))
        if isinstance(x,ast.Call) and call_name(x)=='allowed_data.add':rows.append(dump(x))
    return sorted(rows)
check('allowlist_assignments_and_exact_ASD_exception_unchanged',allowlist(d)==allowlist(od))
for name in ['resource.setrlimit','signal.setitimer','source.set_deadline',
             'generator','failures.wrap','build_B','verify_analytic_state',
             'bilby.gw.likelihood.GravitationalWaveTransient','dynesty.NestedSampler',
             'sampler.sample','compute_integrals','parameters','likelihood.log_likelihood_ratio']:
    check('driver_call_preserved:'+name,selected_calls(d,{name})==selected_calls(od,{name}))
for name in ['subprocess.Popen','p.wait','os.killpg']:
    check('supervisor_process_limit_preserved:'+name,selected_calls(l,{name})==selected_calls(ol,{name}))
source=(DST/'src/pseob_source.py').read_text()
check('source_import_checkpoint_before_temporal',
      source.index('audit_checkpoint("source_after_imports")')>source.index('from bilby.gw.source import') and
      source.index('audit_checkpoint("source_after_imports")')<source.index('validate_time_contract(mass_1'))
check('late_temporal_import_checkpoint_before_bounds',
      source.index('from temporal_contract import')<source.index('audit_checkpoint("source_before_temporal")')<source.index('validate_time_contract(mass_1'))
check('checkpoint_before_new_lal_dictionary',
      source.index('audit_checkpoint("source_before_dictionary")')<source.index('dictionary=lal.CreateDict()'))
check('checkpoint_before_waveform_dispatch',
      source.index('audit_checkpoint("source_before_waveform")')<source.index('result=lal_binary_black_hole('))
post = next(x for x in ast.walk(fn(new_source,"pseob_frequency_domain")) if isinstance(x,ast.Try)).finalbody[-1]
check("post_native_checkpoint_in_finally",isinstance(post,ast.Expr) and isinstance(post.value,ast.Call) and call_name(post.value)=="audit_checkpoint" and post.value.args[0].value=="source_after_waveform")
driver=(DST/'driver_p3.py').read_text()
logl=fn(d,'logl')
logl_text=ast.unparse(logl)
check('pre_ll_checkpoint_precedes_parameters',logl_text.index("checkpoint('pre_likelihood')")<logl_text.index('last_parameters = parameters'))
check('evaluate_wraps_entire_float_LL','guard.evaluate(lambda: float(likelihood.log_likelihood_ratio(last_parameters)))' in logl_text)
for phase in ['initialization_ready','sampler_returned','final_before_diagnostics','final_before_result','final_after_result']:
    check('driver_checkpoint:'+phase,'checkpoint("'+phase+'")' in driver)
check('terminal_latch_overrides_partial','if guard.snapshot()["latched"]:\n            status="AUDIT_VIOLATION"' in driver)
check('journal_preopened_before_hook',driver.index('PreopenedJournal(journal_path)')<driver.index('sys.addaudithook(audit)'))
check('journal_fixed_job_path','journal_path=out/"AUDIT_EVENTS.jsonl"' in driver)
g=tree(DST/'audit_guard.py');guard_text=(DST/'audit_guard.py').read_text()
false_latches=[x for x in ast.walk(g) if isinstance(x,ast.Assign) and any(ast.unparse(t)=='self._latched' for t in x.targets) and isinstance(x.value,ast.Constant) and x.value.value is False]
check('one_false_latch_assignment_in_entire_module',len(false_latches)==1)
# Locate the unique constructor containing the false assignment.
check('only_false_latch_assignment_in_AuditLatch_init',any(false_latches[0] in list(ast.walk(x)) for x in ast.walk(g) if isinstance(x,ast.FunctionDef) and x.name=='__init__'))
deny_text=ast.unparse(fn(g,'deny'))
check('latch_set_before_journal',deny_text.index('self._latched = True')<deny_text.index('self._writer('))
check('first_event_set_before_journal',deny_text.index('self._first = row')<deny_text.index('self._writer('))
check('journal_failure_is_retained_and_reraised','self._journal_error' in deny_text and any(isinstance(x,ast.Raise) and x.exc is None for x in ast.walk(fn(g,'deny'))))
ev=fn(g,'evaluate')
check('evaluate_post_checkpoint_on_exception_and_success',sum(1 for x in ast.walk(ev) if isinstance(x,ast.Call) and call_name(x)=='self.checkpoint' and x.args and isinstance(x.args[0],ast.Constant) and x.args[0].value=='post_likelihood')==2)
for field in ['sequence','event','target','mode','flags','reason','phase','likelihood_calls_at_event','native_attempts_completed_at_event','monotonic_ns','unix_time_ns']:
    check('audit_event_field:'+field,'"'+field+'"' in guard_text)
launch=(DST/'launch_p3.py').read_text()
check('supervisor_reads_journal_after_process_wait',launch.index('p.wait(')<launch.index('journal=jp.read_bytes()'))
check('supervisor_stops_on_rejected_assessment','if not decision["accepted"]:\n            break' in launch)
check('supervisor_propagates_campaign_exit','return campaign_exit(assessments,len(c["jobs"]))' in launch and 'sys.exit(main())' in launch)
a=(DST/'result_acceptance.py').read_text()
for key in ['CHILD_PROCESS_FAILURE','RESULT_MISSING_OR_MALFORMED','AUDIT_LATCH_DIRTY','AUDIT_JOURNAL_NONEMPTY_OR_MISSING','AUDIT_JOURNAL_PIN','BLOCKED_OPERATIONS','CALL_LIMIT_OR_TYPE','BUDGET_COUNTER','MISSING_CHECKPOINT_']:
    check('supervisor_invariant:'+key,key in a)
suite=tree(OUT/'tests/test_audit_guard_doubles.py')
test_names=[x.name for x in ast.walk(suite) if isinstance(x,ast.FunctionDef) and x.name.startswith('test_')]
imports=[]
for x in ast.walk(suite):
    if isinstance(x,ast.Import):imports.extend(z.name for z in x.names)
    if isinstance(x,ast.ImportFrom):imports.append(x.module)
check('suite_imports_only_stdlib_and_pure_guard',set(imports)<={'pathlib','copy','hashlib','json','sys','unittest','audit_guard','result_acceptance'},imports)
check('suite_no_eval_exec_importlib_subprocess',not any(isinstance(x,ast.Call) and call_name(x) in {'eval','exec','__import__','subprocess.run','subprocess.Popen'} for x in ast.walk(suite)))
check('no_new_contract_authorization_or_claim_files',not any(p.name in {'CONTRATO_P3.json','AUTORIZACAO_COORDENACAO.json','CLAIM.json'} for p in OUT.rglob('*') if p.is_file()))
baseline=json.loads((OUT/'SOURCES_BASELINE.json').read_text())
for row in baseline['originals']:
    now,_=metadata(Path(row['path']))
    check('original_preserved:'+Path(row['path']).name,now['sha256']==row['sha256'] and now['bytes']==row['bytes'])
result=dict(status='STATIC_CHECKS_COMPLETE' if all(x['passed'] for x in checks) else 'STATIC_FAILURE',
            created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            checks=checks,check_count=len(checks),failed=[x for x in checks if not x['passed']],
            prepared_test_count=len(test_names),prepared_test_names=test_names,
            suite_executed=False,candidate_modules_imported=False,native_calls=0,likelihood_calls=0,
            sampler_calls=0,source_calls=0,initialization_executed=False,
            tests_passed_count=None,scientific_runtime_verified=False,
            files=[metadata(p)[0] for p in sorted(OUT.rglob('*.py'))])
atomic(OUT/'STATIC_VERIFICATION.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','check_count','failed','prepared_test_count','suite_executed']},ensure_ascii=False))
if result['failed']:sys.exit(2)
