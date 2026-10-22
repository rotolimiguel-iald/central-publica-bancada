"""Extend cleanup protection to the first fallible step after temporary creation."""
from pathlib import Path
import json,hashlib,zipfile,ast,subprocess,sys
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
records=[]
for base in ['C7_POSTERIOR_REPRODUCTION','C7_GWTC3_REPRODUCTION','C7_INJECTION_REPRODUCTION']:
    old=B/(base+'_v3');out=B/(base+'_v3_1')
    if out.exists():raise FileExistsError(out)
    m=json.loads((old/'MANIFEST.json').read_bytes());content={}
    for r in m['shipped_files']:
        p=old/r['path']
        if sha(p)!=r['sha256']:raise ValueError('Old package changed')
        content[r['path']]=p.read_bytes()
    s=content['reproduce.py'].decode();a=s.index("    parent=Path(tempfile.mkdtemp(");b=s.index('        run.mkdir(parents=True)',a)
    s=s[:a]+'''    preserved=outputroot/(ROOT.name+'_'+args.stage+'_'+stamp)
    preserved.mkdir()
    parent=Path(tempfile.mkdtemp(prefix='replay_'+args.stage+'_',dir=workroot)).resolve()
    run = parent / 'ORDEM_013_RINGDOWN'
    try:
        if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe temporary')
'''+s[b:]
    ast.parse(s);content['reproduce.py']=s.encode()
    content['README.md']+=b'\nRevision v3_1: output-directory preconditions now precede temporary creation; all subsequent preparation is protected by finally. Frozen calculation assets are unchanged.\n'
    for n,raw in content.items():new(out/n,raw)
    m['supersedes_manifest_sha256']=sha(old/'MANIFEST.json');m['shipped_files']=[dict(path=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for n,raw in sorted(content.items())]
    new(out/'MANIFEST.json',(json.dumps(m,indent=2)+'\n').encode())
    archive=B/'cache'/(out.name+'.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file():z.write(p,out.name+'/'+p.relative_to(out).as_posix())
    work=B/'cache/supplement_cleanup_v3_1';logs=B/'bis/supplement_cleanup_v3_1';work.mkdir(exist_ok=True);logs.mkdir(exist_ok=True)
    cmd=[sys.executable,'-B',str(out/'reproduce.py'),next(iter(m['stages'])),'--prepare-only','--work-root',str(work),'--output-root',str(logs),'--source-root',str(B/'cache/INTENTIONALLY_ABSENT_SOURCE')]
    p=subprocess.run(cmd,capture_output=True);new(logs/(out.name+'.log'),p.stdout+p.stderr)
    if p.returncode==0 or b'FileNotFoundError' not in p.stderr or list(work.iterdir()):raise ValueError('Missing-input cleanup failed')
    records.append(dict(package=out.name,archive=str(archive.relative_to(B)),sha256=sha(archive),manifest_sha256=sha(out/'MANIFEST.json'),expected_failure_test=True,temporary_removed=True))
new(B/'bis/C7_SUPPLEMENTS_V3_1_BUILD.json',(json.dumps(dict(packages=records,builder_sha256=sha(Path(__file__))),indent=2)+'\n').encode())
print('PASS',len(records))
