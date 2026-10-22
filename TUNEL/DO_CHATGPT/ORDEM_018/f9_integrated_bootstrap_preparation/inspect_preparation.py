"""Run only static parsing and byte comparisons; imports no candidate module."""
import ast
import hashlib
import json
from pathlib import Path
import difflib

ROOT=Path(__file__).resolve().parent

def pin(path):
    raw=path.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def function(file,name,cls=None):
    tree=ast.parse((ROOT/file).read_bytes(),filename=file)
    body=tree.body
    if cls:body=next(x for x in body if isinstance(x,ast.ClassDef) and x.name==cls).body
    return next(x for x in body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name==name)

def signature(n):
    return {'positional':[a.arg for a in n.args.posonlyargs+n.args.args],
            'keyword_only':[a.arg for a in n.args.kwonlyargs],
            'required_keyword_only':[a.arg for a,d in zip(n.args.kwonlyargs,n.args.kw_defaults) if d is None]}

def report():
    result={'schema':'F9_BOOTSTRAP_STATIC_INSPECTION_V1','status':'STATIC_ONLY_NOT_QUALIFIED',
            'candidate_imports':0,'candidate_executions':0,'solver_calls':0,'observed_files_opened':0,
            'python':[],'json':[],'source_lineage':[],'ABIs':[],'preserved_controller_functions':[]}
    for p in sorted(ROOT.glob('*.py')):
        tree=ast.parse(p.read_bytes(),filename=str(p));result['python'].append({'name':p.name,**pin(p),'AST':'PARSED','nodes':len(tree.body)})
    for p in sorted(ROOT.glob('*.json')):
        json.loads(p.read_bytes());result['json'].append({'name':p.name,'JSON':'PARSED'})
    lineage=json.loads((ROOT/'SOURCE_LINEAGE.json').read_bytes())
    for item in lineage['sources']:
        actual=pin(Path(item['source']));assert actual=={k:item[k] for k in ('bytes','sha256')},item['role']
        if item['derivation']=='EXACT_BYTES':assert (ROOT/item['copy']).read_bytes()==Path(item['source']).read_bytes(),item['role']
        result['source_lineage'].append({'role':item['role'],'checked':True,**actual})
    source_map=json.loads((ROOT/'COPIED_SOURCE_MAP.json').read_bytes());pins=json.loads((ROOT/'SOURCE_PINS.json').read_bytes())
    for role,expected in pins.items():assert pin(ROOT/source_map[role])=={k:expected[k] for k in ('bytes','sha256')},role
    result['controller_source_pins_verified']=len(pins)
    old=ROOT.parent/'f9_controller_preparation'/'controller.py';new=ROOT/'controller.py'
    for name in ('_grid','_verify_bindings','_preparation'):
        a=next(n for n in ast.parse(old.read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name==name)
        b=function('controller.py',name);assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False),name
        result['preserved_controller_functions'].append(name)
    diff=''.join(difflib.unified_diff(old.read_text().splitlines(True),new.read_text().splitlines(True),fromfile='39f88/controller.py',tofile='d72f/controller.py'))
    assert diff==(ROOT/'CONTROLLER_DELTA.diff').read_text();result['controller_diff_exact']=True
    for name in ('admit','checkpoint','process_identity','terminal_audit'):
        a=signature(function('supervisor_port.py',name,'QualifiedSupervisor'));b=signature(function('integrated_supervisor.py',name,'IntegratedSupervisor'))
        assert a==b,name;result['ABIs'].append({'interface':'QualifiedSupervisor.'+name,'signature':a,'matches':True})
    targets={
      ('synthetic_inputs','build'):('synthetic_inputs.py','build',None),
      ('controller','run_once'):('controller.py','run_once',None),
      (None,'RuntimePolicy'):('guard_runtime.py','__init__','RuntimePolicy'),
      (None,'IntegratedSupervisor'):('integrated_supervisor.py','__init__','IntegratedSupervisor'),
      (None,'NativeProgressWindow'):('native_progress.py','__init__','NativeProgressWindow'),
      (None,'exchange'):('native_progress.py','exchange',None),
      (None,'verify'):('integrated_reference.py','verify',None)}
    for caller in ('bootstrap.py','integrated_supervisor.py','integrated_parent.py'):
        for n in ast.walk(ast.parse((ROOT/caller).read_bytes())):
            if not isinstance(n,ast.Call):continue
            key=(None,n.func.id) if isinstance(n.func,ast.Name) else ((n.func.value.id,n.func.attr) if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) else None)
            if key not in targets:continue
            file,name,cls=targets[key];sig=signature(function(file,name,cls));keywords={k.arg for k in n.keywords}
            assert None not in keywords and keywords<=set(sig['positional']+sig['keyword_only']),(caller,key,keywords)
            assert set(sig['required_keyword_only'])<=keywords,(caller,key,'missing kwonly')
            result['ABIs'].append({'caller':caller,'line':n.lineno,'target':file+':'+name,'keywords_match':True})
    recipe=json.loads((ROOT/'INPUT_RECIPE_PROPOSAL.json').read_bytes());meta=json.loads((ROOT/'family_metadata.json').read_bytes())
    assert len(meta['family_labels'])==len({x['label'] for x in meta['family_labels']})==600
    assert (recipe['first_level'],recipe['last_level'])==(1,2)
    assert recipe['family_metadata_sha256']==pin(ROOT/'family_metadata.json')['sha256']
    assert recipe['resources']['max_callback_calls']==600*125 and recipe['resources']['max_solver_calls']==125
    assert recipe['observed_access'] is False and recipe['synthetic']['data_kind']=='SYNTHETIC'
    result['recipe_full_family_count']=600;result['recipe_nominal_nodes']=125
    result['I02_review_status']=json.loads((ROOT/'I02_REVIEW_RECEIPT.json').read_bytes())['status']
    result['backups']=[{'name':p.name,**pin(p)} for p in sorted(ROOT.glob('*.bak_*'))]
    assert not list(ROOT.glob('*.tmp_*'))
    result['limitations']=['No module imports or scientific runs; AST is not semantic/runtime proof.',
      'Current Linux runtime/filesystem/resources and independent complete integration review remain required.',
      'External ROOT authority/stable unit binding absent by design; no execution issued.']
    return result

if __name__=='__main__':
    print(json.dumps(report(),ensure_ascii=False,indent=2))
