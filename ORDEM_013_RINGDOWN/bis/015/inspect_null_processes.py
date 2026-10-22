"""Inspect only PIDs recorded by this null-campaign supervisor."""
from pathlib import Path
from datetime import datetime,timezone
import json
d=Path(__file__).resolve().parent/'nulls_campaign_001'
rows=[]
for p in d.glob('*_PROCESS.json'):
    r=json.loads(p.read_bytes());folder=Path('/proc')/str(r['pid'])
    if not folder.exists():rows.append(dict(cell=r['cell'],pid=r['pid'],state='exited'));continue
    cmd=(folder/'cmdline').read_bytes().replace(b'\0',b' ').decode()
    if 'e2_code_v1_1_2/null_runner.py' not in cmd or r['cell'] not in cmd:
        rows.append(dict(cell=r['cell'],pid=r['pid'],state='PID_REUSED_NOT_INSPECTED'));continue
    rows.append(dict(cell=r['cell'],pid=r['pid'],status=[s for s in (folder/'status').read_text().splitlines()
        if s.startswith(('Name:','State:','VmRSS:','Threads:'))]))
print(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),rows=rows)))
