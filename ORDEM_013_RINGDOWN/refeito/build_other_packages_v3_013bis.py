"""Wrap legacy C5 supplements without running any C5 experiment."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,sys
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
rows=[]
for name in ['C7_COHERENT_SOURCE_REPRODUCTION','C7_IMR_RECOVERY_REPRODUCTION','C7_NATIVE_SEOB_WAVEFORM']:
    old=B/name;out=B/(name+'_v3')
    if out.exists():raise FileExistsError(out)
    manifest=json.loads((old/'MANIFEST.json').read_bytes());content={}
    for r in manifest['files']:
        if sha(old/r['path'])!=r['sha256']:raise ValueError('Old bytes changed')
        content[r['path']]=(old/r['path']).read_bytes()
    content['reproduce_legacy.py']=content['reproduce.py'];content['reproduce.py']=(B/'refeito/replay_legacy_in_temporary_v3.py').read_bytes()
    content['historical_README.md']=content['README.md']
    content['README.md']=f'''# {name} v3

NONBLIND archival numerical supplement. No C5 recalibration is authorized by this packaging. The original numerical program is frozen in reproduce_legacy.py, with its limitations intact; current scientific status is the measured C5 wall, not calibrated acceptance. No physical reading is preferred.

`python -B reproduce.py` checks bytes only. To verify preparation without scientific execution, pass `--prepare-only --work-root /short/work --output-root /short/results`. For a later explicitly authorized independent replay, use `--run` with those same roots. All copied inputs and generated working trees are removed in finally; logs and result receipts are outside the package. The output-root receives a new uniquely named directory. Windows MAX_PATH: use short roots or enable long paths; no deep-path success claimed.

R-MOD is [CONJECTURE — management hypothesis, not TGL canon]; Kerr-state and laboratory-partition bridges remain OPEN. Low-SNR positive lnB from prior volume is not detection. Legacy package status PASS refers to its stated numerical comparison only. Original source records/attribution are preserved; this wrapper grants no new licence. Refer to the final English bundle overview for current scope.
'''.encode()
    for n,raw in content.items():write(out/n,raw)
    manifest['supersedes_manifest_sha256']=sha(old/'MANIFEST.json');manifest['files']=[dict(path=n,bytes=len(v),sha256=hashlib.sha256(v).hexdigest()) for n,v in sorted(content.items())]
    write(out/'MANIFEST.json',(json.dumps(manifest,indent=2)+'\n').encode())
    archive=B/'cache'/(out.name+'.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file():z.write(p,out.name+'/'+p.relative_to(out).as_posix())
    cmd=[sys.executable,'-B',str(out/'reproduce.py'),'--prepare-only','--work-root',str(B/'cache'),'--output-root',str(B/'bis/legacy_prepare_v3')]
    run=subprocess.run(cmd,capture_output=True)
    if run.returncode:raise RuntimeError(run.stderr.decode(errors='replace'))
    result=json.loads(run.stdout)
    if not result['temporary_removed']:raise ValueError('Temporary survived')
    rows.append(dict(package=out.name,archive=str(archive.relative_to(B)),archive_sha256=sha(archive),manifest_sha256=sha(out/'MANIFEST.json'),preparation=result))
write(B/'bis/C7_OTHER_V3_BUILD.json',(json.dumps(dict(packages=rows,builder_sha256=sha(Path(__file__))),indent=2)+'\n').encode())
print('PASS',len(rows),'preparations; no scientific rerun')
