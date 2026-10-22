"""One fixed consumer after two existing successful receipts; no retry."""
from pathlib import Path
import json,subprocess,sys,time
P=Path(__file__).resolve().parent
parents=[P/'attempts/20261016T101042_627006Z/RECEIPT.json',P/'attempts/20261016T101244_736785Z/RECEIPT.json']
print(json.dumps({'waiting_for':[str(p) for p in parents]}),flush=True)
for p in parents:
    while not p.exists():time.sleep(15)
    r=json.loads(p.read_bytes())
    assert r['exit_code']==0 and r['readonly_dependencies_unchanged'], str(p)
raise SystemExit(subprocess.call([sys.executable,'-B','-X','utf8',str(P/'build_coefficient_stream_r4.py'),'CanonicalFockPolarRightClosureOrderR5.lean'],cwd=P))
