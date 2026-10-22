from pathlib import Path
from datetime import datetime,timezone
import sys,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'D3prime'
sys.path.insert(0,str(R))
from prepare_part_d import save
if not (D/'START.json').exists():save(D/'START.json',dict(at=datetime.now(timezone.utc).isoformat(),timebox_hours=8,scope='D3prime conjugated form; angular fixedness and physical momentum separated'))
x=json.loads((R/'D6/scalar_04.json').read_bytes())
args=[sys.executable,'-X','utf8','-B',str(R/'A8/compile_a8_isolated_12g_v3.py'),x['kernel'],str(D/sys.argv[1]),sys.argv[2],*x['lean_path'].split(';')]
raise SystemExit(subprocess.call(args))
