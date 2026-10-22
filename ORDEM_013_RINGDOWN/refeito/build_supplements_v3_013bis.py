"""Repackage three frozen reproduction tools with finally cleanup and external logs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,ast,zipfile
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def change(s,a,b):
    if s.count(a)!=1:raise ValueError('Anchor mismatch '+a)
    return s.replace(a,b)
def write(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
rows=[]
for name in ['C7_POSTERIOR_REPRODUCTION','C7_GWTC3_REPRODUCTION','C7_INJECTION_REPRODUCTION']:
    old=B/name;out=B/(name+'_v3')
    if out.exists():raise FileExistsError(out)
    manifest=json.loads((old/'MANIFEST.json').read_bytes());content={}
    for r in manifest['shipped_files']:
        p=old/r['path']
        if sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes']:raise ValueError('Old package changed')
        content[r['path']]=p.read_bytes()
    s=content['reproduce.py'].decode().replace('\r\n','\n')
    s=change(s,'import tarfile','import tempfile\nimport tarfile')
    s=change(s,"    parser.add_argument('--prepare-only', action='store_true')", "    parser.add_argument('--prepare-only', action='store_true',help='Verify/copy inputs, record preparation, then remove temporary data')\n    parser.add_argument('--work-root',type=Path,required=True)\n    parser.add_argument('--output-root',type=Path,required=True)")
    s=change(s,"    parent = ROOT / 'cache' / ('run_' + args.stage + '_' + stamp)","""    workroot=args.work_root.resolve();workroot.mkdir(parents=True,exist_ok=True)
    outputroot=args.output_root.resolve();outputroot.mkdir(parents=True,exist_ok=True)
    if outputroot.is_relative_to(ROOT.resolve()) or workroot.is_relative_to(ROOT.resolve()):
        raise ValueError('Work/output directories must be outside immutable package')
    parent=Path(tempfile.mkdtemp(prefix='replay_'+args.stage+'_',dir=workroot)).resolve()
    if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe temporary')
    preserved=outputroot/(ROOT.name+'_'+args.stage+'_'+stamp)
    preserved.mkdir()
    completed_normally=False""")
    s=s.replace("download_archive(info, ROOT / 'cache/public' / str(info['record']))", "download_archive(info, parent / 'download_cache' / str(info['record']))")
    start=s.index('    run.mkdir(parents=True)');end=s.index("\n\nif __name__ == '__main__':")
    body=s[start:end].rstrip()
    cleanup='''
    finally:
        # Preserve only generated reports/logs; never retain raw copied inputs.
        try:
            for p in list(parent.glob('*.json'))+list(parent.glob('*.log')):
                if p.is_file() and not p.is_symlink():shutil.copyfile(p,preserved/p.name)
            atomic(preserved/'CLEANUP_INTENT.json',dict(temporary=str(parent),manifest_sha256=sha(ROOT/'MANIFEST.json'),
              scope='Preparation and numeric reports only; not physical certification'))
        finally:
            if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe cleanup target')
            shutil.rmtree(parent)
            if parent.exists():raise RuntimeError('Temporary cleanup failed')
            atomic(preserved/'TEMPORARY_REMOVED.json',dict(removed=True,temporary=str(parent),utc=datetime.now(timezone.utc).isoformat()))
'''
    s=s[:start]+'    try:\n'+''.join('    '+line+'\n' for line in body.splitlines())+cleanup+s[end:]
    ast.parse(s);content['reproduce.py']=s.encode()
    content['historical_README_v1.md']=content['README.md']
    content['README.md']=f'''# {name} v3

NONBLIND, conditional numerical reproduction supplement. This version changes temporary-directory handling, not frozen scientific programs. Historical results retain their original scope and calibration failures. No physical reading is selected. The old README is provenance only; the current bundle overview supersedes its scientific status.

Run `python -B reproduce.py --help` for available stages. Every execution now requires `--work-root /short/work --output-root /short/results`, both outside this package. Supply verified existing inputs with `--source-root /path/to/ORDEM_013_RINGDOWN`, or use the archive-cache/download options explicitly. Inputs are copied to a fresh temporary child, removed in finally on success/failure. Reports and logs survive in output-root. `--prepare-only` checks preparation and removes its temporary tree; it does not leave a prepared work directory.

Windows MAX_PATH: use short roots or enable long paths. No deep-path success is claimed. New cleanup is not a scientific recalibration. Do not run the full injection campaign as part of ORDEM013BIS; C5 is closed. The frozen original numeric replays are preserved in earlier validation receipts. These wrappers can be used independently by a later reviewer.

R-MOD remains [CONJECTURE — management hypothesis, not TGL canon], with Kerr-state and laboratory-partition walls. All catalogue ratios concern the conditional 220 sector with higher Kerr modes; alternatives on the same event are not multiplied. Realization mapping and actual free-source calibration remain OPEN. Occam effects in low-SNR injections are not detections.
'''.encode()
    for n,raw in content.items():write(out/n,raw)
    manifest['supersedes_manifest_sha256']=sha(old/'MANIFEST.json')
    manifest['updated_utc']=datetime.now(timezone.utc).isoformat();manifest['cleanup_scope']='Fresh temporary child removed in finally; reports outside package'
    manifest['shipped_files']=[dict(path=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in sorted(content.items())]
    write(out/'MANIFEST.json',(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode())
    archive=B/'cache'/(name+'_v3.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file():z.write(p,out.name+'/'+p.relative_to(out).as_posix())
    rows.append(dict(package=out.name,archive=str(archive.relative_to(B)),archive_sha256=sha(archive),manifest_sha256=sha(out/'MANIFEST.json'),scope='Repackaged; no scientific campaign rerun'))
write(B/'bis/C7_SUPPLEMENTS_V3_BUILD.json',(json.dumps(dict(packages=rows,builder_sha256=sha(Path(__file__))),indent=2)+'\n').encode())
print(json.dumps(rows))
