"""Failure-path cleanup controls without recomputing a scientific campaign."""
from pathlib import Path
import json,subprocess,sys,hashlib
B=Path(__file__).resolve().parents[1]
work=B/'cache/supplement_cleanup_v3';work.mkdir()
reports=B/'bis/supplement_cleanup_v3';reports.mkdir()
rows=[]
for name in ['C7_POSTERIOR_REPRODUCTION_v3','C7_GWTC3_REPRODUCTION_v3','C7_INJECTION_REPRODUCTION_v3']:
    root=B/name;manifest=json.loads((root/'MANIFEST.json').read_bytes());stage=next(iter(manifest['stages']))
    # Deliberately absent source: the original implementation would have left copied assets behind.
    command=[sys.executable,'-B',str(root/'reproduce.py'),stage,'--prepare-only','--work-root',str(work),'--output-root',str(reports),'--source-root',str(B/'cache/INTENTIONALLY_ABSENT_SOURCE')]
    p=subprocess.run(command,capture_output=True)
    log=reports/(name+'.log')
    with log.open('xb') as f:f.write(p.stdout+p.stderr)
    if p.returncode==0 or b'FileNotFoundError' not in p.stderr:raise ValueError('Expected input-refusal path not reached')
    if list(work.iterdir()):raise ValueError('Leaked temporary data')
    preserved=list(reports.glob(name+'_*'))
    removed=[r/'TEMPORARY_REMOVED.json' for r in preserved if r.is_dir()]
    if len(removed)!=1 or not json.loads(removed[0].read_bytes())['removed']:raise ValueError('Missing cleanup receipt')
    rows.append(dict(package=name,expected_failure=True,temporary_removed=True,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),command=command))
out=B/'bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json'
with out.open('xb') as f:f.write((json.dumps(dict(status='PASS_FAILURE_PATH_CLEANUP',rows=rows),indent=2)+'\n').encode())
print('PASS',len(rows))
