"""Independent static integration review and isolated consumer fixtures; no main run."""
import ast
import copy
import datetime
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parent
W = Path(r'C:\IALD\Central de Patentes\work\rede_quantica_20261013')

def pin(p):
    p = Path(p)
    raw = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def put(p, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with p.open('xb') as f:
        f.write(raw)
    assert p.read_bytes() == raw

preflight_path = P/'NETWORK_CONSUMER_PREFLIGHT_R1.json'
preflight = read(preflight_path)
for key in ['runtime', 'plan', 'script']:
    assert pin(preflight[key]['path']) == preflight[key]
assert preflight['passed'] and len(preflight['checks']) == 13 and all(x['passed'] for x in preflight['checks'])
plan = read(preflight['plan']['path'])
runtime = Path(preflight['runtime']['path'])
baseline = P/'candidate_r3/um.py'
baseline_before = pin(baseline)
tree = ast.parse(baseline.read_bytes())
functions = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}
assignments = {n.targets[0].id:n.value for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
old_flags = ast.literal_eval(assignments['_LEAN_THEOREM_FLAGS'])
declarations = sorted(set(plan['theorems']) - set(old_flags.values()))
ladder_node = next(n.value for n in functions['prove_external_ladder'].body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ext_flags' for t in n.targets))
ladder = ast.literal_eval(ladder_node)
assert len(ladder) == len(set(ladder)) == 7171
expected = 7171 + len(declarations)
rows = plan['modules'] + [{'relative': plan['audit_relative'], 'transposed_source': plan['audit']}]
sources, hashes = {}, {}
for row in rows:
    src = Path(row['transposed_source']['path'])
    assert pin(src) == row['transposed_source']
    text = src.read_text(encoding='utf-8')
    assert hashlib.sha256(text.encode('utf-8')).hexdigest() == row['transposed_source']['sha256'], 'Embedding would normalize pinned bytes'
    sources[row['relative']] = text
    hashes[row['relative']] = row['transposed_source']['sha256']

contract = {'declarations':declarations, 'source_sha256':hashes, 'expected_ladder':expected,
            'constructed_components':['ISOLATED_REVIEW_FIXTURE'], 'open_joint_contract':['OPEN']}
runtime_tree = ast.parse(runtime.read_bytes())
assert [n.name for n in runtime_tree.body if isinstance(n, ast.FunctionDef)] == ['rede_fock_v394']
assert all(isinstance(n, (ast.FunctionDef, ast.Expr)) for n in runtime_tree.body)
ns = {'_V394_NETWORK_CONTRACT':contract, '_EMBEDDED_KERNEL_FILES':sources}
exec(compile(runtime_tree, str(runtime), 'exec'), ns)
valid = {'kernel_formalization': {'all_verified':True, 'axiom_report':{n:['propext','Classical.choice','Quot.sound'] for n in declarations}},
         'external_ladder': {'n_theorems_clean':expected,'n_theorems_expected':expected},
         'regra_quadratica_v394':{'all_verified':True}, 'existing_gate':'UNCHANGED'}
checks=[]

def run(name, mutate=None, expected_accept=False):
    core = copy.deepcopy(valid)
    if mutate:
        mutate(core)
    before = copy.deepcopy(core)
    result = ns['rede_fock_v394'](core)
    actual = result['all_verified']
    del core['rede_fock_v394']
    passed = actual is expected_accept and core == before and result['whole_certificate_inhabited'] is False and result['does_not_gate_core'] is True
    checks.append({'name':name, 'passed':passed, 'accepted':actual, 'verdict':result['verdict']})
    assert passed, name

first = declarations[0]
run('valid_synthetic', expected_accept=True)
run('missing_declaration', lambda c: c['kernel_formalization']['axiom_report'].pop(first))
for name, value in [('sorry', ['sorryAx']), ('non_string', [True]), ('non_list', 'propext'), ('null_axioms', None)]:
    run(name, lambda c,v=value: c['kernel_formalization']['axiom_report'].__setitem__(first,v))
for name,value in [('integer_verification',1),('missing_verification',None),('false_verification',False)]:
    run(name,lambda c,v=value:c['kernel_formalization'].__setitem__('all_verified',v))
for name,value in [('wrong_ladder',expected-1),('boolean_ladder',True),('nan_ladder',float('nan')),('float_ladder',float(expected))]:
    run(name,lambda c,v=value:c['external_ladder'].__setitem__('n_theorems_clean',v))
run('quadratic_refusal',lambda c:c['regra_quadratica_v394'].__setitem__('all_verified',False))
key=next(iter(sources));old=sources[key]
sources[key]=old+'\n-- changed\n';run('source_mutation')
del sources[key];run('missing_source')
sources[key]=old
old_declarations=contract['declarations'];contract['declarations']=[];run('empty_declarations');contract['declarations']=old_declarations
old_hashes=contract['source_sha256'];contract['source_sha256']={};run('empty_source_contract');contract['source_sha256']=old_hashes
run('restored',expected_accept=True)

integrator=W/'integrate_network_v394_r4.py'
itext=integrator.read_text(encoding='utf-8');itree=ast.parse(itext)
assert "assert changed == ['_v394_article_tex', 'compile_pdf', 'main', 'prove_external_ladder']" in itext
assert "assert compiled['passed'] and compiled['plan'] == pin(plan_path)" in itext
assert "for result in compiled['modules']:" in itext
# Execute only the new in-memory preflight AST; never call main or its writes.
ibody=next(n.body for n in itree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
start=next(i for i,n in enumerate(ibody) if isinstance(n,ast.Assert) and "compiled['passed']" in ast.unparse(n))
end=next(i for i,n in enumerate(ibody) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='dest' for t in n.targets))
guard_tree=ast.Module(body=ibody[start:end],type_ignores=[])
guard=compile(guard_tree,str(integrator)+':preflight-only','exec')
base_compiled={'passed':True,'plan':preflight['plan'],'modules':[
    {'module':r['module'],'source':r['transposed_source']} for r in plan['modules']] + [
    {'module':plan['audit_module'],'source':plan['audit'],'axiom_report':{n:['propext','Classical.choice','Quot.sound'] for n in plan['theorems']}}]}
guard_checks=[]
def guard_run(name,mutate=None,accept=False):
    c=copy.deepcopy(base_compiled)
    if mutate:mutate(c)
    try:
        exec(guard,{'compiled':c,'plan':plan,'plan_path':Path(preflight['plan']['path']),'pin':pin})
        accepted=True
    except (AssertionError,KeyError,TypeError):accepted=False
    guard_checks.append({'name':name,'accepted':accepted,'passed':accepted is accept})
    assert accepted is accept,name
guard_run('complete_synthetic_manifest',accept=True)
guard_run('empty_modules',lambda c:c.__setitem__('modules',[]))
guard_run('duplicate_module',lambda c:c['modules'].__setitem__(0,copy.deepcopy(c['modules'][1])))
guard_run('missing_audit',lambda c:c['modules'].pop())
guard_run('wrong_source_pin',lambda c:c['modules'][0]['source'].__setitem__('sha256','0'*64))
guard_run('missing_audit_declaration',lambda c:c['modules'][-1]['axiom_report'].pop(plan['theorems'][0]))
guard_run('extra_audit_declaration',lambda c:c['modules'][-1]['axiom_report'].__setitem__('Unexpected',[]))
guard_run('sorry_in_audit',lambda c:c['modules'][-1]['axiom_report'].__setitem__(plan['theorems'][0],['sorryAx']))
guard_run('reordered_modules_valid',lambda c:c['modules'].reverse(),accept=True)
assert baseline_before == pin(baseline)
out={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic',
     'verdict':'PASSA_PREPARACAO_ESTATICA_CANDIDATO_AINDA_NAO_EXAMINADO','consumer_checks':checks,'all_consumer_checks_passed':all(x['passed'] for x in checks),'integrator_preflight_checks':guard_checks,
     'existing_preflight_checks_verified':13,'expected_new_flags':len(declarations),'expected_ladder':expected,'source_files_verified':len(rows),
     'sources':[pin(integrator),pin(runtime),pin(preflight_path),preflight['plan'],baseline_before,pin(W/'compile_network_bundle_r4b.py')],
     'material_findings':[], 'resolved_findings':[{'id':'N1','severity':'MEDIUM','component':'integrator preflight','observation':'A versão lida inicialmente aceitava passed=True com plan correto e modules=[] nos predicados do manifesto. O construtor corrigiu antes de executar o integrador.','resolution':'A versão pinada por esta revisão exige nomes únicos exatamente plan.modules mais audit_module, pins fonte↔plano e audit final com conjunto exato das declarações. Nove controles sobre o trecho AST real passam, inclusive lista vazia, duplicata e ausência do audit final.'}],
     'static_checks':['Offsets de AST são bytes UTF-8, coerentes com edições em raw bytes; aplicada ordem reversa com recusa de sobreposição.','Mudanças em funções existentes limitadas por assert AST a quatro nomes; ausência de remoções fora desses nomes também é checada por comparação.','Hooks de consumidor vêm depois de regra_quadratica e antes de figuras/artigos; resultado vai ao selo.','Destinação é candidate_r4 nova; new escreve temporário exclusivo e renomeia; kernel original não é destino.','Fontes do plano desta rodada preservam exatamente os bytes ao serem embutidas.','Consumidor recusa evidência parcial, axiomas não permitidos, booleanos/NaN na escada, fonte alterada e contratos vazios.','Escopo conserva whole_certificate_inhabited=False e OPEN para polar/KMS/contrato conjunto.'],
     'pending':['Revisão do candidato efetivamente gerado e de sua AST; o integrador não foi executado nesta revisão.','Consumo de relatório real compilado e rito integral em etapa própria.'],
     'no_main_import_or_execution':True,'no_production_memory_or_gate_changes':True,'script':pin(__file__)}
put(B/'REVISAO_ESTATICA_R1.json',out)
print(json.dumps({'receipt':pin(B/'REVISAO_ESTATICA_R1.json'),'consumer_checks':len(checks),'integrator_checks':len(guard_checks),'passed':True,'expected_ladder':expected,'resolved_finding':'N1'},ensure_ascii=False))
