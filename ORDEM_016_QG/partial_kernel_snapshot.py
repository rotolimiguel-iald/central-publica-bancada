"""Copy only manifest-listed v371 scientific kernel and its existing build."""
from pathlib import Path
import json, shutil
from prepare_part_d import save, write, sha, R

S=R/'FECHAMENTO_PARCIAL'
source=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
kernel=source/'tgl_kernel'
dest=S/'kernel_v371'
manifest=source/'tgl_kernel_proof_manifest.json'
um=source/'um.py'
pin=json.loads((R/'D6/UM_PIN_RECEIPT.json').read_bytes())
assert sha(um)==pin['sha256'], 'v371 source changed'
data=json.loads(manifest.read_bytes())
assert not dest.exists(), 'Reuse existing snapshot; never overwrite'
dest.mkdir()
files=[];failures=[]
for rel,expected in data['formal_files_sha256'].items():
    p=kernel/rel
    if not p.is_relative_to(kernel):raise ValueError(rel)
    if not p.is_file():failures.append(dict(path=rel,reason='missing'));continue
    actual=sha(p)
    if actual!=expected:failures.append(dict(path=rel,expected=expected,actual=actual));continue
    out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,out);assert sha(out)==actual
    files.append(dict(path=rel,sha256=actual))
assert not failures, failures
build=[]
for branch in ['TGL','TGLExt']:
    for p in sorted((kernel/'.lake/build/lib/lean'/branch).rglob('*')):
        if not p.is_file() or not (p.suffix.startswith('.olean') or p.suffix=='.ilean'):continue
        rel=p.relative_to(kernel);out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,out);build.append(dict(path=str(rel),sha256=sha(out)))
for module in ['TGL','TGLExt']:
    for p in sorted((kernel/'.lake/build/lib/lean').glob(module+'.*')):
        if not (p.suffix.startswith('.olean') or p.suffix=='.ilean'):continue
        out=dest/p.relative_to(kernel);out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,out);build.append(dict(path=str(p.relative_to(kernel)),sha256=sha(out)))
write(S/'kernel_proof_manifest_origin.json',manifest.read_bytes())
save(S/'KERNEL_SNAPSHOT.json',dict(source=str(kernel),destination=str(dest),
    version='v371',um_sha256=sha(um),manifest_sha256=sha(manifest),formal_sources=files,
    copied_build=build, build_scope='Existing canonical oleans copied and hashed; not rebuilt by this copy',
    failures=failures,canonical_written=False))
print(json.dumps(dict(source_files=len(files),build_files=len(build),bytes=sum(p.stat().st_size for p in dest.rglob('*') if p.is_file()),snapshot_sha256=sha(S/'KERNEL_SNAPSHOT.json'))))
