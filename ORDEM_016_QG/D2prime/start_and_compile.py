from pathlib import Path
from datetime import datetime,timezone
import sys,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'D2prime'
sys.path.insert(0,str(R))
from prepare_part_d import save,sha
if not (D/'START.json').exists():save(D/'START.json',dict(at=datetime.now(timezone.utc).isoformat(),timebox_hours=10,scope='D2prime Maxwell expectation on selected photon net, inherited forged-tensor rejection')))
x=json.loads((R/'D1prime/photon_03.json').read_bytes())
paths=[str(R/'A1/probes'),*x['lean_path'].split(';')]
args=[sys.executable,'-X','utf8','-B',str(R/'A8/compile_a8_isolated_12g_v3.py'),x['kernel'],str(D/sys.argv[1]),sys.argv[2],*paths]
raise SystemExit(subprocess.call(args))
