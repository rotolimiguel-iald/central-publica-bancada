"""Unify immutable releases and additive evidence without changing calculations."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import zipfile
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(8*1024*1024):
            h.update(block)
    return h.hexdigest()


def main():
    out=ROOT/'C7_DELIVERY_BUNDLE_VALIDATION.json'
    if out.exists():
        raise FileExistsError('Preserve delivered bundle')
    basic=json.loads((ROOT/'C7_PACKAGE_VALIDATION.json').read_bytes())
    supplements=json.loads((ROOT/'C7_SUPPLEMENTS_VALIDATION.json').read_bytes())
    old=json.loads((ROOT/'C7_GWTC3_REPRODUCTION_VALIDATION.json').read_bytes())
    sources=[dict(archive=basic['archive'],sha256=basic['archive_sha256'],
                  old_prefix='TGL_RINGDOWN',new_prefix='C7_INDEPENDENT')]
    sources += [dict(archive=p['archive'],sha256=p['sha256'],old_prefix=p['package'],new_prefix=p['package'])
                for p in supplements['packages']]
    sources.append(dict(archive=old['archive'],sha256=old['sha256'],old_prefix=old['package'],new_prefix=old['package']))
    contents={}

    def add(name, raw):
        rel=PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or '\\' in name:
            raise ValueError('Unsafe bundle path')
        if name in contents and contents[name]!=raw:
            raise ValueError('Different bytes under same name: '+name)
        contents[name]=raw

    for source in sources:
        path=ROOT/source['archive']
        if sha(path)!=source['sha256']:
            raise ValueError('Source archive changed')
        source['bytes']=path.stat().st_size
        with zipfile.ZipFile(path) as handle:
            if handle.testzip() is not None:
                raise ValueError('Source CRC failed')
            for name in handle.namelist():
                parts=PurePosixPath(name).parts
                if parts[0]!=source['old_prefix']:
                    raise ValueError('Unexpected archive prefix')
                new='/'.join([source['new_prefix'],*parts[1:]])
                add(new,handle.read(name))
    audit=json.loads((ROOT/'C7_REQUIREMENTS_AUDIT.json').read_bytes())
    for name,row in audit['evidence'].items():
        path=ROOT/name
        if path.stat().st_size!=row['bytes'] or sha(path)!=row['sha256']:
            raise ValueError('Evidence changed after requirement audit: '+name)
        add(name,path.read_bytes())
    for name in ['C7_REQUIREMENTS_AUDIT.json','C7_REQUIREMENTS_AUDIT.md','C7_DELIVERY_OVERVIEW.md',
                 'C7_GWTC3_REPRODUCTION_VALIDATION.json','C0_ADENDO_ESCOPO_LITERATURA.md']:
        add(name,(ROOT/name).read_bytes())
    add('README.md',(ROOT/'C7_DELIVERY_OVERVIEW.md').read_bytes())
    verifier='''"""Verify every shipped byte before running this research delivery."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_bytes())
for row in manifest['files']:
    rel=PurePosixPath(row['path'])
    if rel.is_absolute() or '..' in rel.parts or chr(92) in row['path']:
        raise ValueError('Unsafe manifest path')
    path=(root/row['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Missing or escaped file: '+row['path'])
    raw=path.read_bytes()
    if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
        raise ValueError('Changed file: '+row['path'])
print(json.dumps(dict(status='PASS',files=len(manifest['files']),scope='Byte custody, not scientific or physical certification')))
'''
    add('verify_delivery.py',verifier.encode('utf-8'))
    files=[dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
           for name,raw in sorted(contents.items())]
    manifest=dict(status='CONDITIONAL_RESEARCH_DELIVERY',created_utc=datetime.now(timezone.utc).isoformat(),
                  source_archives=sources,files=files,scientific_calibration='NOT_PASSED',
                  original_program_modified=False,physical_confirmation_claimed=False)
    add('MANIFEST.json',json.dumps(manifest,indent=2,ensure_ascii=False).encode('utf-8'))
    archive=ROOT/'cache/TGL_RINGDOWN_DELIVERY_v1.zip'
    if archive.exists():
        raise FileExistsError('Preserve earlier bundle')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as handle:
        for name,raw in sorted(contents.items()):
            handle.writestr('TGL_RINGDOWN_DELIVERY/'+name,raw)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    fresh=ROOT/'cache'/('delivery_fresh_'+stamp)
    fresh.mkdir()
    with zipfile.ZipFile(archive) as handle:
        if handle.testzip() is not None:
            raise ValueError('Bundle CRC failed')
        for name,raw in contents.items():
            data=handle.read('TGL_RINGDOWN_DELIVERY/'+name)
            if data!=raw:
                raise ValueError('Repacked bytes changed')
            path=fresh/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
    process=subprocess.run([sys.executable,'-B',str(fresh/'verify_delivery.py')],cwd=fresh,
                           capture_output=True,text=True)
    if process.returncode:
        raise RuntimeError(process.stderr)
    result=json.loads(process.stdout)
    if result['status']!='PASS' or result['files']!=len(files):
        raise ValueError('Fresh bundle verifier failed')
    record=dict(status='PASS',date_utc=datetime.now(timezone.utc).isoformat(),
                archive=archive.relative_to(ROOT).as_posix(),bytes=archive.stat().st_size,
                sha256=sha(archive),members=len(contents),manifest_sha256=sha(fresh/'MANIFEST.json'),
                fresh_directory=fresh.relative_to(ROOT).as_posix(),fresh_verifier=result,
                source_archives=sources,unchanged_repacked_bytes=True,
                science_not_rerun_again='Source calculation replays are preserved; this check verifies repackaging only',
                generator_sha256=sha(Path(__file__)))
    atomic_json(out,record)
    print(json.dumps({k:v for k,v in record.items() if k!='source_archives'}))


if __name__=='__main__':
    main()
