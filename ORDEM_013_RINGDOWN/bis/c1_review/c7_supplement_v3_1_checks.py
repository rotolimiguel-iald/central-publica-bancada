"""Closing check of the three v3_1 wrapper lifecycles; no scientific subprocess."""
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from datetime import datetime, timezone
import ast, hashlib, json, zipfile
B=Path(__file__).resolve().parents[2]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
# Reuse only the previously archived in-memory harness functions; do not import its main.
harness=Path(__file__).with_name('c7_supplement_cleanup_checks.py').read_text(encoding='utf-8')
parsed=ast.parse(harness)
functions=[n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name in {'check_manifest','check_zip'}]
exec(compile(ast.fix_missing_locations(ast.Module(body=functions,type_ignores=[])),'reused_byte_checks','exec'),globals())
fn=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name=='lifecycle_probes')
code=ast.get_source_segment(harness,fn)
before="require(error and error.startswith('PermissionError:') and len(active) == 1, 'Pretry leak not reproduced')"
after="require(error and error.startswith('PermissionError:') and not active and not any(e[0] == 'mkdtemp' for e in events), 'Output failure created temporary')"
require(code.count(before)==1,'Harness anchor mismatch');code=code.replace(before,after)
exec(compile(code,'fixed_window_harness','exec',optimize=1),globals())
build=read(B/'bis/C7_SUPPLEMENTS_V3_1_BUILD.json')
require(build['builder_sha256']==sha(B/'refeito/close_supplement_creation_window_013bis.py'),'Builder receipt')
rows=[]
for r in build['packages']:
    root=B/r['package'];old=B/r['package'].removesuffix('_1')
    m,names=check_manifest(root);om,oldnames=check_manifest(old)
    require(names==oldnames and m['supersedes_manifest_sha256']==sha(old/'MANIFEST.json'),'Package lineage')
    require(sha(root/'MANIFEST.json')==r['manifest_sha256'] and sha(B/r['archive'])==r['sha256'],'Build pins')
    check_zip(B/r['archive'],root,names)
    changed=[n for n in sorted(names) if (root/n).read_bytes()!=(old/n).read_bytes()]
    require(changed==['README.md','reproduce.py'],'Unexpected scientific change')
    records=list((B/'bis/supplement_cleanup_v3_1').glob(root.name+'_*/TEMPORARY_REMOVED.json'))
    require(len(records)==1,'Ambiguous cleanup receipt')
    removed=read(records[0]);intent=read(records[0].with_name('CLEANUP_INTENT.json'))
    work=(B/'cache/supplement_cleanup_v3_1').resolve();temp=Path(removed['temporary']).resolve()
    require(removed['removed'] is True and intent['temporary']==removed['temporary'],'Receipt mismatch')
    require(intent['manifest_sha256']==sha(root/'MANIFEST.json'),'Cleanup package mismatch')
    require(temp.is_relative_to(work) and temp!=work and not temp.exists(),'Temporary confinement/removal')
    log=B/'bis/supplement_cleanup_v3_1'/(root.name+'.log')
    require('FileNotFoundError: Provide --source-root' in log.read_text(encoding='utf-8'),'Wrong negative path')
    probe=lifecycle_probes((root/'reproduce.py').read_text(encoding='utf-8'),root.name)
    rows.append(dict(package=root.name,files=len(names),manifest_sha256=sha(root/'MANIFEST.json'),archive_sha256=sha(B/r['archive']),
        wrapper_sha256=sha(root/'reproduce.py'),changed_files=changed,negative_log_sha256=sha(log),
        removal_receipt_sha256=sha(records[0]),temporary_absent=True,lifecycle_probe=probe))
finalbuilder=B/'refeito/build_final_bundle_v3_3_013bis.py'
bt=ast.parse(finalbuilder.read_text(encoding='utf-8'));main=next(n for n in bt.body if isinstance(n,ast.FunctionDef) and n.name=='main')
selection=next(ast.literal_eval(n.value) for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='packages' for t in n.targets))
result=dict(status='TEMPORARY_CREATION_WINDOW_CLOSED_BUT_MKDIR_BEFORE_CONFINEMENT_REMAINS',utc=datetime.now(timezone.utc).isoformat(),
    no_scientific_run=True,builder_sha256=build['builder_sha256'],build_receipt_sha256=sha(B/'bis/C7_SUPPLEMENTS_V3_1_BUILD.json'),
    final_builder_read_only=dict(path=str(finalbuilder.relative_to(B)),sha256=sha(finalbuilder),selected_packages=selection,
        current_corrected_supplements_selected=all(r['package'] in selection for r in rows)),
    script_sha256=sha(Path(__file__)),rows=rows)
out=Path(__file__).with_name('c7_supplement_v3_1_results.json');raw=(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode()
with out.open('xb') as f:f.write(raw)
require(out.read_bytes()==raw,'Output mismatch')
print(json.dumps(dict(status=result['status'],mock_cases=15,negative_receipts_verified=3,
    final_builder_uses_latest=result['final_builder_read_only']['current_corrected_supplements_selected'])))
