"""Archive only manifest-listed handoff files; test a clean extracted consumer."""
from pathlib import Path,PurePosixPath
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    package=ROOT/'C7_INDEPENDENT';manifest=json.loads((package/'MANIFEST.json').read_bytes())
    names=[r['path'] for r in manifest['files']]+['MANIFEST.json','C6_REPRODUCTION_RESULT.json']
    for row in manifest['files']:
        if hashlib.sha256((package/row['path']).read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Shipped file changed: '+row['path'])
    replay=json.loads((package/'C6_REPRODUCTION_RESULT.json').read_bytes())
    if replay['status']!='PASS' or not replay['all_windows_recomputed_from_strain']:
        raise ValueError('Fresh strain reproduction not established')
    archive=ROOT/'cache/TGL_RINGDOWN_INDEPENDENT_v1.zip'
    if archive.exists():raise FileExistsError('Preserve previous release')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name in names:z.write(package/name,arcname='TGL_RINGDOWN/'+name)
    directory=Path(tempfile.mkdtemp(prefix='package_clean_',dir=ROOT/'cache'))
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise ValueError('Archive CRC failed')
        for item in z.infolist():
            parts=PurePosixPath(item.filename)
            if parts.is_absolute() or '..' in parts.parts:raise ValueError('Unsafe archive member')
            target=directory.joinpath(*parts.parts);target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(z.read(item))
    clean=directory/'TGL_RINGDOWN';env=dict(os.environ);env.pop('PYTHONPATH',None)
    reports=[]
    for script in ('verify_manifest.py','run_demo.py'):
        proc=subprocess.run([sys.executable,'-B',str(clean/script)],cwd=clean,env=env,text=True,capture_output=True)
        if proc.returncode:raise RuntimeError(proc.stderr)
        result=json.loads(proc.stdout)
        reports.append(dict(script=script,status='PASS',
            details=result if script=='verify_manifest.py' else {k:result[k] for k in ('beta_runtime','relative_R_B_waveform_change','numpy_version')}))
    atomic_json(ROOT/'C7_PACKAGE_VALIDATION.json',dict(status='PASS',
        archive=str(archive.relative_to(ROOT)),bytes=archive.stat().st_size,
        archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        manifest_sha256=hashlib.sha256((package/'MANIFEST.json').read_bytes()).hexdigest(),
        archive_members=len(names),clean_copy_checks=reports,
        clean_copy=str(clean.relative_to(ROOT)),registered_strain_reproduction=replay,
        packaged_raw_strain=False,packaged_canonical_program=False,
        incomplete='Full posterior-release and injection regeneration not automated end-to-end in v1; README states remaining work.',
        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    print(json.dumps(dict(status='PASS',bytes=archive.stat().st_size,archive_members=len(names),clean_checks=len(reports))))

if __name__=='__main__':main()
