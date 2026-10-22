"""Build one new R57 candidate with existing Lean caches read only."""
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from derive_polarization_r57 import ROOT, new, pin, preflight

source = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'MiguelFixedBoundaryScalarReadingR57.lean')
preflight()
stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
attempt = ROOT / 'builds' / stamp
attempt.mkdir(parents=True, exist_ok=False)
lean = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
paths = [kernel / '.lake/build/lib/lean']
paths += sorted((kernel / '.lake/packages').glob('*/.lake/build/lib/lean'))
env = dict(os.environ, LEAN_PATH=';'.join(map(str, paths)))
cmd = [str(lean), '-M', '4096', str(source), '-o', str(attempt / (source.stem+'.olean'))]
start = dt.datetime.now(dt.timezone.utc).isoformat()
record = {'source': pin(source), 'runner': pin(__file__), 'command': cmd,
          'cwd': str(ROOT), 'LEAN_PATH': env['LEAN_PATH'], 'start_utc': start,
          'toolchain': subprocess.run([str(lean), '--version'], capture_output=True, text=True).stdout.strip()}
new(attempt.relative_to(ROOT) / 'START.json', record)
timer = time.perf_counter()
with (attempt / 'BUILD.log').open('xb') as log:
    process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env, cwd=ROOT)
    print(json.dumps({'pid': process.pid, 'attempt': str(attempt), 'source': record['source']}, ensure_ascii=False), flush=True)
    exit_code = process.wait()
elapsed = time.perf_counter() - timer
raw = (attempt / 'BUILD.log').read_text(encoding='utf-8')
record.update(end_utc=dt.datetime.now(dt.timezone.utc).isoformat(), seconds=elapsed,
              exit_code=exit_code, log=pin(attempt / 'BUILD.log'), axioms=raw,
              source_has_sorry='sorry' in source.read_text(encoding='utf-8'),
              olean=pin(attempt / (source.stem+'.olean')) if (attempt / (source.stem+'.olean')).exists() else None)
receipt = new(attempt.relative_to(ROOT) / 'RESULT.json', record)
print(json.dumps({'receipt': receipt, 'exit_code': exit_code, 'seconds': elapsed, 'log': raw}, ensure_ascii=False), flush=True)
sys.exit(exit_code)
