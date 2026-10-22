"""Read-only preparation validation: hashes/AST/API shape; no candidate import."""
import ast
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent

def sha(raw):return hashlib.sha256(raw).hexdigest()

def function(tree,name,owner=None):
    sequence=tree.body
    if owner:
        sequence=next(x for x in sequence if isinstance(x,ast.ClassDef) and x.name==owner).body
    return next(x for x in sequence if isinstance(x,ast.FunctionDef) and x.name==name)

def check_call(call,target):
    args=target.args
    positionals=[x.arg for x in args.args]
    if positionals and positionals[0]=='self':positionals=positionals[1:]
    assert len(call.args)<=len(positionals)
    assert all(x.arg is not None for x in call.keywords)
    names={x.arg for x in call.keywords}
    allowed=set(positionals[len(call.args):])|{x.arg for x in args.kwonlyargs}
    assert names<=allowed
    required={x.arg for x,d in zip(args.kwonlyargs,args.kw_defaults) if d is None}
    assert required<=names
    required_pos=len(positionals)-len(args.defaults)
    assert set(positionals[len(call.args):required_pos])<=names

def validate():
    pins=json.loads((BASE/'SOURCE_PINS.json').read_bytes())
    verified=[]
    for role,item in pins.items():
        raw=Path(item['path']).read_bytes()
        assert len(raw)==item['bytes'] and sha(raw)==item['sha256'],role
        verified.append({'role':role,**item})
    trees={name:ast.parse((BASE/name).read_bytes(),filename=name) for name in
           ('controller.py','background_supplier.py','supervisor_port.py')}
    allowed={'hashlib','itertools','json','math','os','pathlib','sys','time','types','abc'}
    imports={}
    for name,tree in trees.items():
        modules=[]
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):modules.extend(x.name for x in n.names)
            elif isinstance(n,ast.ImportFrom):modules.append(n.module)
        assert set(modules)<=allowed,name
        imports[name]=modules
    dependencies={role:ast.parse(Path(pins[role]['path']).read_bytes()) for role in
                  ('theta','node','durable','consumer','engine')}
    contracts={
      'ThetaIntegrator':function(dependencies['theta'],'__init__','ThetaIntegrator'),
      'NodeContext':function(dependencies['node'],'__init__','NodeContext'),
      'DurableStore':function(dependencies['durable'],'__init__','DurableStore'),
      'DurableNodeCallback':function(dependencies['durable'],'__init__','DurableNodeCallback'),
      'prepare_joint':function(dependencies['consumer'],'prepare_joint'),
      'ExistingEngineSupplier':function(trees['background_supplier.py'],'__init__','ExistingEngineSupplier')}
    checks=[]
    for call in (x for x in ast.walk(trees['controller.py']) if isinstance(x,ast.Call)):
        if isinstance(call.func,ast.Attribute) and call.func.attr in contracts:
            check_call(call,contracts[call.func.attr]);checks.append({'target':call.func.attr,'line':call.lineno})
    assert {x['target'] for x in checks}==set(contracts)
    worker=function(dependencies['engine'],'prediction_worker')
    for call in (x for x in ast.walk(trees['background_supplier.py']) if isinstance(x,ast.Call)):
        if isinstance(call.func,ast.Attribute) and call.func.attr=='original_worker':
            check_call(call,worker);checks.append({'target':'prediction_worker','line':call.lineno})
    text=(BASE/'controller.py').read_text(encoding='utf-8')
    assert text.index("ticket=runs.acquire(")<text.index("joint=bindings['consumer'].prepare_joint(")
    assert 'PREPARATION_ONLY_EXECUTION_DENIED' in text
    assert "'QUALIFIED_SUPERVISOR_NOT_IMPLEMENTED'" in (BASE/'supervisor_port.py').read_text()
    assert all(not (BASE/name).exists() for name in ('AUTH.json','CLAIM.json','ROOT_DECISION.json','RUN_CLAIM.json','RUN'))
    return {'schema':'F9_CONTROLLER_STATIC_PREPARATION_CHECKS_V1',
      'status':'STATIC_CHECKS_PASSED_NOT_EXECUTED','source_pins_verified':verified,
      'candidate_ast_parsed':list(trees),'candidate_imports':0,'allowed_stdlib_imports':imports,
      'cross_api_keyword_shapes':checks,'global_claim_before_prepare_joint_source_order':True,
      'default_cli_denies_execution_source_present':True,'supervisor_abstract_raise_source_present':True,
      'no_authorization_or_claim_artifact':True,'observed_reads':False,'solver_calls':0,'WSL':0,
      'limitation':'AST and byte checks only; not invocation, runtime qualification, independent review or proof of semantics'}

if __name__=='__main__':print(json.dumps(validate(),ensure_ascii=False,indent=2))
