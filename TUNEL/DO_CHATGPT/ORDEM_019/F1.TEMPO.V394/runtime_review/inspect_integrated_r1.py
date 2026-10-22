"""Read-only AST/byte comparison of isolated baseline and integrated candidate."""
from pathlib import Path
from datetime import datetime,timezone
import ast,difflib,hashlib,json
HERE=Path(__file__).resolve().parent;UNIT=HERE.parent
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
oldp=UNIT/'baseline/um.py';newp=UNIT/'candidate/um.py'
old=oldp.read_text(encoding='utf-8');new=newp.read_text(encoding='utf-8')
ot=ast.parse(old);nt=ast.parse(new)
def key(n,i):
    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):return type(n).__name__+':'+n.name
    if isinstance(n,ast.Assign):return 'Assign:'+','.join(ast.unparse(t) for t in n.targets)
    if isinstance(n,ast.AnnAssign):return 'AnnAssign:'+ast.unparse(n.target)
    return type(n).__name__+':'+str(i)
def table(tree):return {key(n,i):n for i,n in enumerate(tree.body)}
om=table(ot);nm=table(nt)
oldfunc={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)}
newfunc={n.name:n for n in nt.body if isinstance(n,ast.FunctionDef)}
dump=lambda n:ast.dump(n,include_attributes=False)
changed_functions=[k for k in oldfunc if k in newfunc and dump(oldfunc[k])!=dump(newfunc[k])]
removed_functions=sorted(set(oldfunc)-set(newfunc));added_functions=sorted(set(newfunc)-set(oldfunc))
assigns=lambda t:{n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
oa=assigns(ot);na=assigns(nt)
changed_assignments=[k for k in oa if k in na and dump(oa[k])!=dump(na[k])]
removed_assignments=sorted(set(oa)-set(na));added_assignments=sorted(set(na)-set(oa))
oe=ast.literal_eval(oa['_EMBEDDED_KERNEL_FILES']);ne=ast.literal_eval(na['_EMBEDDED_KERNEL_FILES'])
changed_embedded=[k for k in oe if k in ne and oe[k]!=ne[k]]
added_embedded=sorted(set(ne)-set(oe));removed_embedded=sorted(set(oe)-set(ne))
imports=''.join('import '+r[:-5].replace('/','.')+'\n' for r in added_embedded)
actual_imports={k:[s for s in ne[k].splitlines() if s.startswith('import TGLExt.TimeGraviton')] for k in changed_embedded}
glue_checks={
    'old_aggregator_is_prefix':ne['TGLExt.lean'].startswith(oe['TGLExt.lean']),
    'old_audit_is_suffix':ne['TGL/Audit.lean'].endswith(oe['TGL/Audit.lean']),
    'only_four_new_module_imports':all(len(v)==4 for v in actual_imports.values()),
}
materialized=[]
for k in added_embedded+changed_embedded:
    p=UNIT/'candidate/tgl_kernel'/k
    materialized.append({'relative':k,'pin':pin(p),'embedded_sha256':hashlib.sha256(ne[k].encode()).hexdigest(),
                         'bytes_match':p.read_bytes()==ne[k].encode()})
of=ast.literal_eval(oa['_LEAN_THEOREM_FLAGS']);nf=ast.literal_eval(na['_LEAN_THEOREM_FLAGS'])
flags={'old_count':len(of),'new_count':len(nf),'added':{k:nf[k] for k in nf.keys()-of.keys()},
       'removed':sorted(of.keys()-nf.keys()),'changed_old':[k for k in of if k in nf and of[k]!=nf[k]]}
def stringlists(node):
    return [ast.literal_eval(x) for x in ast.walk(node) if isinstance(x,ast.List) and all(isinstance(v,ast.Constant) and isinstance(v.value,str) for v in x.elts)]
ol=max(stringlists(oldfunc['prove_external_ladder']),key=len);nl=max(stringlists(newfunc['prove_external_ladder']),key=len)
contract=ast.literal_eval(na['_V394_FORMAL_CONTRACT']);inscriptions=ast.literal_eval(na['_V394_INSCRIPTIONS'])
ladder={'old_count':len(ol),'new_count':len(nl),'old_prefix_preserved':nl[:len(ol)]==ol,
        'added_equals_new_flags':set(nl[len(ol):])==set(flags['added']),
        'no_duplicates':len(nl)==len(set(nl)),'contract_expected':contract['expected_ladder']}
main_diff='\n'.join(difflib.unified_diff(ast.get_source_segment(old,oldfunc['main']).splitlines(),
    ast.get_source_segment(new,newfunc['main']).splitlines(),fromfile='baseline/main',tofile='candidate/main',n=5))
small_diffs={name:'\n'.join(difflib.unified_diff(ast.get_source_segment(old,oldfunc[name]).splitlines(),ast.get_source_segment(new,newfunc[name]).splitlines(),n=3))
 for name in changed_functions if name!='main' and name!='prove_external_ladder'}
receipt=json.loads((UNIT/'INTEGRATION_R1.json').read_bytes())
result={'created_utc':datetime.now(timezone.utc).isoformat(),'baseline':pin(oldp),'candidate':pin(newp),
 'receipt_matches':pin(oldp)==receipt['baseline'] and pin(newp)==receipt['candidate'],
 'changed_old_functions':changed_functions,'removed_functions':removed_functions,'added_functions':added_functions,
 'changed_assignments':changed_assignments,'removed_assignments':removed_assignments,'added_assignments':added_assignments,
 'embedded_old_count':len(oe),'embedded_new_count':len(ne),'changed_old_embedded':changed_embedded,
 'added_embedded':added_embedded,'removed_embedded':removed_embedded,'glue_checks':glue_checks,
 'materialized':materialized,'flags':flags,'ladder':ladder,
 'operator_inscriptions':{k:{'sha256':v['sha256'],'hash_valid':hashlib.sha256(v['text'].encode()).hexdigest()==v['sha256'],'text':v['text']} for k,v in inscriptions.items()},
 'main_diff':main_diff,'small_diffs':small_diffs,
 'scope':'Static/read-only actual isolated candidate; no um.py execution and no gate decision.'}
data=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
with (HERE/'INTEGRATED_REVIEW_AST_R1.json').open('x',encoding='utf-8') as f:f.write(data)
print(json.dumps({k:result[k] for k in ('receipt_matches','changed_old_functions','removed_functions','added_functions','changed_assignments','added_assignments','changed_old_embedded','added_embedded','ladder','glue_checks')},ensure_ascii=False))
print(main_diff)
print(json.dumps(small_diffs,ensure_ascii=False))
