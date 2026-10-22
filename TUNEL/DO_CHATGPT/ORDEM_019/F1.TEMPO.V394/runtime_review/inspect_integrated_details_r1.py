"""Check all non-target top-level AST and new-source embeddings in the real copy."""
from pathlib import Path
import ast,hashlib,json,difflib
HERE=Path(__file__).resolve().parent;UNIT=HERE.parent
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
op=UNIT/'baseline/um.py';np=UNIT/'candidate/um.py'
old=ast.parse(op.read_bytes());new=ast.parse(np.read_bytes())
d=lambda n:ast.dump(n,include_attributes=False)
funcs=lambda t:{n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
of=funcs(old);nf=funcs(new)
changed={'prove_external_ladder','pedras_v393','emit_article','main'}
changed_globals={'UM_VERSION','_EMBEDDED_KERNEL_FILES','_LEAN_THEOREM_FLAGS','_ESQUELETO_STONES'}
added=set(nf)-set(of)
newglobals={'_V394_FORMAL_CONTRACT','_V394_INSCRIPTIONS'}
def filtered(t,isnew):
    out=[]
    for n in t.body:
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and (n.name in changed or isnew and n.name in added):continue
        if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in changed_globals|newglobals:continue
        # Standalone source-module docstrings are inert strings, retained as metadata.
        if isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):continue
        out.append(d(n))
    return out
oldrest=filtered(old,False);newrest=filtered(new,True)
assert oldrest==newrest
checks={}
for rel in ['runtime/time_runtime_v394_r3.py','physical_contract/physical_parameters.py','physical_contract/kms_root_anchor_r2.py']:
    p=UNIT/rel;tr=ast.parse(p.read_bytes());fs=funcs(tr)
    checks[rel]={'pin':pin(p),'definitions':{name:d(node)==d(nf[name]) for name,node in fs.items()}}
    assert all(checks[rel]['definitions'].values())
na={n.targets[0].id:ast.literal_eval(n.value) for n in new.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in newglobals|{'_ESQUELETO_STONES'}}
oa={n.targets[0].id:ast.literal_eval(n.value) for n in old.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='_ESQUELETO_STONES'}
lineage=na['_ESQUELETO_STONES'];previous=oa['_ESQUELETO_STONES']
assert lineage[:len(previous)]==previous and len(lineage)==len(previous)+4
consumer=nf['tempo_frequencia_v394']
writes=[]
for n in ast.walk(consumer):
    if isinstance(n,ast.Assign):
        for target in n.targets:
            if isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) and target.value.id=='core':writes.append(ast.unparse(target))
assert writes==["core['tempo_frequencia_v394']"]
main=nf['main'];calls=[n for n in ast.walk(main) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)]
call_lines={name:[n.lineno for n in calls if n.func.id==name] for name in ['tempo_frequencia_v394','emit_figures','emit_article']}
assert len(call_lines['tempo_frequencia_v394'])==1
assert min(call_lines['emit_figures']+call_lines['emit_article'])>call_lines['tempo_frequencia_v394'][0]
rt2=UNIT/'runtime/time_runtime_v394_r2.py';rt3=UNIT/'runtime/time_runtime_v394_r3.py'
runtime_diff='\n'.join(difflib.unified_diff(rt2.read_text().splitlines(),rt3.read_text().splitlines(),n=2))
result={'candidate':pin(np),'non_target_top_level_ast_identical':True,'retained_top_level_nodes':len(oldrest),
 'new_classes':[x for x in added if isinstance(nf[x],ast.ClassDef)],'embedded_python_sources':checks,
 'old_lineage_prefix_preserved':True,'lineage_added':lineage[len(previous):],
 'consumer_core_write_targets':writes,'main_call_lines':call_lines,
 'inscriptions':{k:{'sha256':v['sha256'],'valid':hashlib.sha256(v['text'].encode()).hexdigest()==v['sha256']} for k,v in na['_V394_INSCRIPTIONS'].items()},
 'runtime_r2_to_r3_diff':runtime_diff,'passed':True,
 'scope':'AST and literal inspection only; the main function was not executed.'}
with (HERE/'INTEGRATED_REVIEW_STATIC_DETAILS_R1.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'result':pin(HERE/'INTEGRATED_REVIEW_STATIC_DETAILS_R1.json'),'checks':checks,'call_lines':call_lines,'runtime_diff':runtime_diff},ensure_ascii=False))
