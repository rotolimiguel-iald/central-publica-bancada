from pathlib import Path
from datetime import datetime,timezone
import sys,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'D5'
sys.path.insert(0,str(R))
from prepare_part_d import save
if not (D/'START.json').exists():save(D/'START.json',dict(at=datetime.now(timezone.utc).isoformat(),timebox_hours=10,scope='D5 dilation geometry, clock rescaling, conditional network modular selfsimilarity'))
x=json.loads((R/'D4/theorems_01.json').read_bytes())
paths=[str(R/'D4'),str(R/'D6'),*x['lean_path'].split(';')]
args=[sys.executable,'-X','utf8','-B',str(R/'A8/compile_a8_isolated_12g_v3.py'),x['kernel'],str(D/sys.argv[1]),sys.argv[2],*paths]
raise SystemExit(subprocess.call(args))
