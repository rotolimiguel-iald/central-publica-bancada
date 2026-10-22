"""Verify archive bytes and a deliberately corrupted disposable package copy."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    receipt=json.loads((ROOT/'C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json').read_bytes())
    package=ROOT/receipt['package']; archive=ROOT/receipt['archive']
    manifest=json.loads((package/'MANIFEST.json').read_bytes())
    if sha(archive)!=receipt['sha256'] or sha(package/'MANIFEST.json')!=receipt['manifest_sha256']:
        raise ValueError('Package archive custody changed')
    names=[r['path'] for r in manifest['files']]+['MANIFEST.json']
    with zipfile.ZipFile(archive) as z:
        if sorted(z.namelist())!=sorted(names):
            raise ValueError('Archive payload differs from manifest')
        for row in manifest['files']:
            original=(package/row['path']).read_bytes()
            if hashlib.sha256(original).hexdigest()!=row['sha256'] or len(original)!=row['bytes']:
                raise ValueError('Manifest byte mismatch:'+row['path'])
            if z.read(row['path'])!=original:
                raise ValueError('Archive differs from tested package:'+row['path'])
    disposable=ROOT/'cache'/('native_package_tamper_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    disposable.mkdir()
    for name in names:
        (disposable/name).write_bytes((package/name).read_bytes())
    target=disposable/'tgl_native_ringdown.py'
    altered=target.read_bytes()+b'\n# Deliberate corruption of a disposable verification copy only.\n'
    temp=target.with_suffix('.tmp');temp.write_bytes(altered)
    if temp.stat().st_size!=len(altered):raise ValueError('Short tamper-copy write')
    temp.replace(target)
    result=subprocess.run([sys.executable,'-I','-B',str(disposable/'reproduce.py')],cwd=disposable,capture_output=True,text=True)
    refused=result.returncode!=0 and 'Package integrity failed:tgl_native_ringdown.py' in result.stderr
    output=dict(status='PASS_ARCHIVE_AND_TAMPER_REJECTION' if refused else 'FAIL_PACKAGE_INTEGRITY_TEST',
        files_verified=len(names),tamper_rejected=refused,tamper_exit_code=result.returncode,
        tamper_error=result.stderr[-2000:],archive_sha256=sha(archive),manifest_sha256=sha(package/'MANIFEST.json'),
        original_package_unchanged=all(sha(package/r['path'])==r['sha256'] for r in manifest['files']),
        scope='Byte/manifest integrity and fail-closed rejection; not scientific validation',
        source_sha256=sha(Path(__file__)))
    path=ROOT/'C7_NATIVE_SEOB_INTEGRITY_VALIDATION.json'
    if path.exists():raise FileExistsError(path)
    raw=(json.dumps(output,indent=2)+'\n').encode();tmp=path.with_suffix('.tmp');tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError('Short receipt write')
    tmp.replace(path)
    print(json.dumps({k:v for k,v in output.items() if k!='tamper_error'}))
    if not refused:raise ValueError('Corrupted copy was not rejected by the consumer')


if __name__=='__main__':main()
