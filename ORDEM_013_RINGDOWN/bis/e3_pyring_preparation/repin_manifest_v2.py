"""Versioned custody successor only; stdlib, AST and byte hashes, no science."""
from pathlib import Path
from datetime import datetime,timezone
import ast,copy,hashlib,json,os,re,time
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
SNAPSHOT=HERE/'snapshots/pre_manifest_v2_001'


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for raw in iter(lambda:f.read(1024*1024),b''):h.update(raw)
    return h.hexdigest()


def publish(path,value):
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    temp=path.with_name(path.name+'.pending')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(raw):raise OSError('Incomplete receipt')
    os.link(temp,path);temp.unlink()


def main():
    started=time.perf_counter()
    successor=HERE/'MANIFEST_v2.json';receipt_path=HERE/'MANIFEST_V2_REPIN_RECEIPT.json'
    if successor.exists() or receipt_path.exists():raise FileExistsError('Version already emitted')
    previous=HERE/'MANIFEST.json'
    if previous.read_bytes()!=(SNAPSHOT/'MANIFEST.json').read_bytes():raise ValueError('Predecessor manifest changed')
    old=json.loads(previous.read_bytes());checks=[]
    for name in ('kerr_model.py','conditioning.py','CONFIG.json','PLAN.md'):
        if (HERE/name).read_bytes()!=(SNAPSHOT/name).read_bytes():raise ValueError('Scientific artifact changed '+name)
    checks.append('Model/conditioning/config/plan byte-identical to predecessor')
    target=ast.dump(ast.parse("sha(HERE/'MANIFEST.json')",mode='eval').body,include_attributes=False)
    class ReplaceHash(ast.NodeTransformer):
        def visit_Call(self,node):
            if ast.dump(node,include_attributes=False)==target:
                return ast.parse("auth['manifest_sha256']",mode='eval').body
            return self.generic_visit(node)
    for name in ('controller.py','runner.py'):
        expected=ReplaceHash().visit(ast.parse((SNAPSHOT/name).read_text()))
        actual=ast.parse((HERE/name).read_text())
        if ast.dump(expected,include_attributes=False)!=ast.dump(actual,include_attributes=False):
            raise ValueError('Unexpected runtime AST change '+name)
    checks.append('Controller/runner AST differs only in verified manifest-hash references')
    # Exercise only two extracted stdlib path functions, no production imports.
    tree=ast.parse((HERE/'custody.py').read_text())
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('contained','selected_manifest')]
    if len(funcs)!=2:raise ValueError('Manifest selector functions missing')
    env={'Path':Path,'HERE':HERE,'re':re}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),'<isolated_manifest_selector>','exec'),env)
    selector_cases=[]
    for auth,wanted in (({},'MANIFEST.json'),({'manifest_filename':'MANIFEST.json'},'MANIFEST.json'),
      ({'manifest_filename':'MANIFEST_v2.json'},'MANIFEST_v2.json'),({'manifest_filename':'MANIFEST_v12.json'},'MANIFEST_v12.json')):
        if env['selected_manifest'](auth)!=HERE/wanted:raise ValueError('Selector positive failed')
        selector_cases.append({'input':auth,'accepted':True})
    for name in ('../MANIFEST_v2.json','sub/MANIFEST_v2.json','MANIFEST_v0.json','MANIFEST_v02.json',
      'MANIFEST_v-1.json','MANIFEST_V2.json','other.json','/tmp/MANIFEST.json',None,2):
        try:env['selected_manifest']({'manifest_filename':name})
        except ValueError:selector_cases.append({'input':name,'accepted':False})
        else:raise ValueError('Unsafe/ambiguous manifest accepted')
    checks.append('14 isolated manifest selector checks passed')
    guard_key='ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py'
    closing_path=B/'bis/e2_review/ACTIVATION_V2_CLOSING_RECEIPT.json'
    closing=json.loads(closing_path.read_bytes());guard_pin=sha(ROOT/guard_key)
    if closing['modified_source']['sha256']!=guard_pin:raise ValueError('Guard differs from final closing receipt')
    pins=dict(old['source_and_config_pins'])
    for name,pin in pins.items():
        actual=sha(ROOT/name)
        if actual!=pin and name!=guard_key:raise ValueError('Unexpected external pin drift '+name)
    pins[guard_key]=guard_pin
    for path in (previous,HERE/'MANIFEST_V2_NOTE.md',closing_path):pins[path.relative_to(ROOT).as_posix()]=sha(path)
    code={}
    for path in HERE.glob('*.py'):
        ast.parse(path.read_text(),filename=str(path));code[path.name]=sha(path)
    manifest=copy.deepcopy(old)
    manifest.update(created_utc=datetime.now(timezone.utc).isoformat(),revision='V2_FINAL_GUARD_REPIN_VERSIONED_SELECTION',
      predecessor={'relative_to_Chatgpt':previous.relative_to(ROOT).as_posix(),'sha256':sha(previous)},
      code_sha256=code,source_and_config_pins=pins,
      activation_scope='COLD_PREPARATION_ONLY; actual authorization/execution by principal after B2/F0-stop and B review',
      authorization_manifest_filename='MANIFEST_v2.json',
      checks=old['checks']+checks,
      science_artifacts_unchanged=['kerr_model.py','conditioning.py','CONFIG.json','PLAN.md'],
      files_written_this_successor=[(HERE/name).relative_to(ROOT).as_posix() for name in
        ('custody.py','controller.py','runner.py','MANIFEST_V2_NOTE.md','repin_manifest_v2.py','MANIFEST_v2.json','MANIFEST_V2_REPIN_RECEIPT.json')]
        +[p.relative_to(ROOT).as_posix() for p in sorted(SNAPSHOT.rglob('*')) if p.is_file()])
    publish(successor,manifest)
    receipt=dict(status='COLD_VERSIONED_SUCCESSOR_READY_FOR_B_REVIEW',created_utc=datetime.now(timezone.utc).isoformat(),
      predecessor_sha256=sha(previous),successor_path=successor.relative_to(ROOT).as_posix(),successor_sha256=sha(successor),
      guard_sha256=guard_pin,checks=checks,selector_cases=selector_cases,
      changed_Kerr_code={name:dict(before=sha(SNAPSHOT/name),after=sha(HERE/name)) for name in ('custody.py','controller.py','runner.py')},
      E2_sources_written=[],science_executed=False,authorization_created=False,
      wall_seconds=time.perf_counter()-started,
      files_written=manifest['files_written_this_successor'])
    publish(receipt_path,receipt)
    for name,pin in pins.items():
        if sha(ROOT/name)!=pin:raise ValueError('Post-write pin drift '+name)
    print(json.dumps({'successor_sha256':sha(successor),'receipt_sha256':sha(receipt_path),
      'guard_sha256':guard_pin,'selector_checks':len(selector_cases),'files_written':len(receipt['files_written']),
      'status':receipt['status']},indent=2))


if __name__=='__main__':main()
