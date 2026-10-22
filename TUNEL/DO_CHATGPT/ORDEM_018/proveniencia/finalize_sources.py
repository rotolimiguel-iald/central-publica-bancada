"""Static F1 checks. Scientific source files are never imported or executed."""
from pathlib import Path
import ast, datetime, hashlib, json, re, zipfile, xml.etree.ElementTree as ET
from audit_provenance import atomic, metadata, OUT

records = {}
for file in sorted(OUT.glob('*.json')):
    value = json.loads(file.read_text(encoding='utf-8'))
    if isinstance(value, dict) and 'source' in value and 'sha256' in value['source']:
        src = value['source']
        entry = records.setdefault(src['path'], {'source_at_read':src, 'evidence_files':[]})
        entry['evidence_files'].append(file.name)
verified=[]
for path, record in records.items():
    meta, raw = metadata(Path(path))
    assert meta['sha256']==record['source_at_read']['sha256'], path
    verified.append(dict(meta, evidence_files=record['evidence_files'], unchanged_since_read=True))
atomic(OUT/'MANIFESTO_FONTES_F1.json',json.dumps({
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Fontes científicas realmente lidas nesta auditoria; não é inventário de todo o acervo.',
    'source_count':len(verified),'sources':verified,
    'timestamps_note':'mtime e metadados OOXML são evidência documental local, não carimbo de publicação imutável.'
},ensure_ascii=False,indent=2)+'\n')

main=Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py')
meta,raw=metadata(main)
source=raw.decode('utf-8-sig')
tree=ast.parse(source)
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='predict_H0_zero_free')
assignments={}
for node in fn.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name):
                assignments[target.id]=node
def deps(name, visiting=None):
    visiting=set() if visiting is None else visiting
    if name in visiting: return set()
    if name not in assignments: return {name}
    visiting=visiting|{name}
    return set().union(*(deps(n.id,visiting) for n in ast.walk(assignments[name].value) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)))
prediction_deps=sorted(deps('H0_b'))
assert not {'H0_local_obs','sigma_local'} & set(prediction_deps)
assert {'H0_local_obs','sigma_local'} <= deps('tension_b')
checks={
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'method':'ast.parse only; no scientific import, eval, compile or execution.',
    'source':meta,
    'function':{'name':fn.name,'first_line':fn.lineno,'last_line':fn.end_lineno,'text':ast.get_source_segment(source,fn)},
    'H0_b_static_dependencies':prediction_deps,
    'observation_in_prediction_dependencies':False,
    'observation_in_comparison_dependencies':True,
    'scope_warning':'Conservative textual dependency closure within this function. External input choices, prior model selection and published chronology are not certified by this check.',
    'beta_definitions':[
        {'line':n.lineno,'source':ast.get_source_segment(source,n)}
        for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'ALPHA_FINE_CODATA_2018','SQRT_E','BETA_TGL'} for t in n.targets)
    ]
}
cruz=Path(r'C:\IALD\Artigo\Haja_Luz\TGL_Espelho_invertido\TGL_v11_1_CRUZ_original.py')
cruzmeta,cruzraw=metadata(cruz)
cruztext=cruzraw.decode('utf-8-sig')
cruztree=ast.parse(cruztext)
h0node=next(n for n in ast.walk(cruztree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='chi2_H0' for t in n.targets))
checks['cruz_H0']={'source':cruzmeta,'line':h0node.lineno,'expression':ast.get_source_segment(cruztext,h0node),'names':sorted({n.id for n in ast.walk(h0node.value) if isinstance(n,ast.Name)}),'beta_dependency_in_expression':False}
docx=Path(r'C:\IALD\IMac LA\Física - TGL\Validação\TGL_v11_1_CRUZ.docx')
docmeta,docraw=metadata(docx)
with zipfile.ZipFile(docx) as z:
    root=ET.fromstring(z.read('word/document.xml'))
paras=[''.join(n.itertext()) for n in []]
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paras=[''.join(t.text or '' for t in n.findall('.//w:t',ns)) for n in root.findall('.//w:p',ns)]
norm=lambda t:'\n'.join(x.rstrip() for x in t.splitlines()).strip()
a,b=norm('\n'.join(paras)),norm(cruztext)
checks['cruz_january_vs_june']={'docx_source':docmeta,'py_source':cruzmeta,'normalization':'rstrip each line, LF, strip outer whitespace','equal_normalized_text':a==b,'docx_normalized_sha256':hashlib.sha256(a.encode()).hexdigest(),'py_normalized_sha256':hashlib.sha256(b.encode()).hexdigest(),'docx_normalized_lines':len(a.splitlines()),'py_normalized_lines':len(b.splitlines())}
atomic(OUT/'VERIFICACOES_ESTATICAS_F1.json',json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verified_sources':len(verified),'prediction_dependencies':prediction_deps,'same_cruz':checks['cruz_january_vs_june']['equal_normalized_text'],'H0_names':checks['cruz_H0']['names']},ensure_ascii=False,indent=2))
