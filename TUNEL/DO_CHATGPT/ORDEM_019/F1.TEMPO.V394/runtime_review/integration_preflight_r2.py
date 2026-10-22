"""Check corrected preflight refusal using three local fixtures; no real integration."""
from pathlib import Path
import ast, hashlib, json, shutil, os, sys
BASE=Path(__file__).resolve().parent;UNIT=BASE.parent;ROOT=UNIT.parents[4]
SCRIPT=ROOT/'work/rede_quantica_20261013/integrate_time_v394.py'
REL=Path('Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394')
oldroot=BASE/'integration_fixture'
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def new(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(value))
    return pin(p)
def snapshot(p):return {str(f.relative_to(p)):(pin(f)['sha256'],f.stat().st_mtime_ns) for f in p.rglob('*') if f.is_file()}
cases=[]
tree=ast.parse(SCRIPT.read_text(encoding='utf-8'))
nodes=[n for n in tree.body if not (isinstance(n,ast.ImportFrom) and n.module=='diary_r1') and not isinstance(n,ast.If)]
for label in ('existing_receipt','changed_candidate','partial_module'):
    root=BASE/('preflight_'+label);out=root/REL
    out.mkdir(parents=True)
    if label=='existing_receipt':
        (out/'INTEGRATION_R1.json').write_bytes(b'{"fixture":true}')
    else:
        for rel in ('baseline/um.py','candidate/um.py','formal_verified/FORMAL_MANIFEST.json'):
            p=out/rel;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes((oldroot/REL/rel).read_bytes())
        if label=='partial_module':
            (out/'candidate/um.py').write_bytes((out/'baseline/um.py').read_bytes())
            (out/'candidate/tgl_kernel').mkdir()
            (out/'candidate/tgl_kernel/TimeFixture.lean').write_bytes(b'partial')
    ns={'ROOT':root,'new':new,'pin':pin,'__file__':str(SCRIPT),'__name__':'preflight_fixture'}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SCRIPT)+' [preflight fixture]','exec'),ns)
    before=snapshot(root)
    try:ns['main']()
    except Exception as exc:outcome={'type':type(exc).__name__,'message':str(exc)}
    else:outcome={'type':None}
    after=snapshot(root)
    cases.append({'name':label,'refused':outcome['type'] is not None,'unchanged':before==after,'outcome':outcome})
assert all(c['refused'] and c['unchanged'] for c in cases)
new(BASE/'INTEGRATION_PREFLIGHT_R2_REVIEW.json',{'source':pin(SCRIPT),'cases':cases,'passed':True,'fixture_only':True})
print(json.dumps({'result':pin(BASE/'INTEGRATION_PREFLIGHT_R2_REVIEW.json'),'cases':cases},ensure_ascii=False))
