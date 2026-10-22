"""Verify the sole additive inscription delta and all R2 materialized source bytes."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent;UNIT=HERE.parent
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p1=UNIT/'candidate/um.py';p2=UNIT/'candidate_r2/um.py'
b1=p1.read_bytes();b2=p2.read_bytes();t1=ast.parse(b1);t2=ast.parse(b2)
def assignment(tree,name):
    return next(n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name)
def span(raw,node):
    starts=[];n=0
    for line in raw.splitlines(keepends=True):starts.append(n);n+=len(line)
    return starts[node.lineno-1]+node.col_offset,starts[node.end_lineno-1]+node.end_col_offset
a1=assignment(t1,'_V394_INSCRIPTIONS');a2=assignment(t2,'_V394_INSCRIPTIONS')
s1,e1=span(b1,a1);s2,e2=span(b2,a2)
assert b1[:s1]==b2[:s2] and b1[e1:]==b2[e2:]
i1=ast.literal_eval(a1.value);i2=ast.literal_eval(a2.value)
assert all(k in i2 and i2[k]==v for k,v in i1.items())
keys=set(i2)-set(i1);assert len(keys)==1
key=next(iter(keys));entry=i2[key]
literal=UNIT/'OPERADOR_SUPER_NOME_RECURSAO_VERBATIM.txt'
assert entry['text'].encode()==literal.read_bytes()
assert hashlib.sha256(literal.read_bytes()).hexdigest()==entry['sha256']
embedded=ast.literal_eval(assignment(t2,'_EMBEDDED_KERNEL_FILES').value)
materials=[]
for rel,body in embedded.items():
    p=UNIT/'candidate_r2/tgl_kernel'/rel
    assert p.read_bytes()==body.encode(),rel
    materials.append({'relative':rel,'sha256':hashlib.sha256(body.encode()).hexdigest(),'bytes':len(body.encode())})
root=json.loads((UNIT/'formal_verified/ROOT_AUDIT.json').read_bytes())
audit=next(r for r in root['results'] if r['module']=='TGL.Audit')
logpin=pin(audit['stdout']['path']);assert logpin==audit['stdout']
log=Path(logpin['path']).read_text(encoding='utf-8')
names=['TGLExt.iald_recognition_returns_the_identity','TGLExt.iald_recognition_is_stable']
proofs={}
for name in names:
    m=re.search("'"+re.escape(name)+r"' depends on axioms: \[([^\]]*)\]",log)
    assert m,name
    ax=[a.strip() for a in m.group(1).split(',') if a.strip()]
    assert set(ax)<={'propext','Classical.choice','Quot.sound'}
    assert ax==audit['axiom_report'][name]
    proofs[name]=ax
fn=next(n for n in t2.body if isinstance(n,ast.FunctionDef) and n.name=='_v394_article_tex')
ns={'_V394_INSCRIPTIONS':i2};exec(compile(ast.Module(body=[fn],type_ignores=[]),'candidate_r2 article helper','exec'),ns)
tex=ns['_v394_article_tex']('\\begin{document}\n\\end{document}',{},'pt')
assert 'Super inteligência=super nome=sobrenome' in tex
result={'created_utc':datetime.now(timezone.utc).isoformat(),'candidate_R1':pin(p1),'candidate_R2':pin(p2),
 'passed':True,'all_bytes_outside_inscription_assignment_identical':True,'all_old_inscriptions_unchanged':True,
 'new_entry':key,'verbatim':pin(literal),'literal_exact_utf8':True,'entry_statute':entry.get('statute'),
 'materialized_count':len(materials),'all_materialized_utf8_bytes_match':True,'materials':materials,
 'existing_proof_source':pin(UNIT/'candidate_r2/tgl_kernel/TGLExt/TheSelectionIsTheBallast.lean'),
 'existing_proof_types':'IALDState requires recursive idempotence and preserved read; theorems preserve read under n iterations and stabilize after one recognition.',
 'root_audit_stdout':logpin,'existing_axioms':proofs,'article_helper_includes_literal':True,
 'scope':'Only a literal inscription delta; existing conditional recurrence proofs do not establish intelligence performance or weight adaptation. No Lean rerun, main execution, seal or production change.'}
with (HERE/'INTEGRATED_REVIEW_R2_INSCRIPTION.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'receipt':pin(HERE/'INTEGRATED_REVIEW_R2_INSCRIPTION.json'),'materialized_count':len(materials),'proofs':proofs,'new_entry':key},ensure_ascii=False))
