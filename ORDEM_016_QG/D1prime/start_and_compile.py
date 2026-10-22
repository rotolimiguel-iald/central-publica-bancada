from pathlib import Path
from datetime import datetime,timezone
import sys,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'D1prime'
sys.path.insert(0,str(R))
from prepare_part_d import save,sha
start=D/'START.json'
if not start.exists():save(start,dict(at=datetime.now(timezone.utc).isoformat(),timebox_hours=16,scope='D1prime photon +/-1; inherit C4; no old spin2 branch',adendo_sha256=sha(R.parent/'TUNEL/PARA_CHATGPT/ADENDO_016_003c_o_campo_e_a_luz_D1_D3_revistos.md')))
prior=json.loads((R/'C4/transverse_03.json').read_bytes())
args=[sys.executable,'-X','utf8','-B',str(R/'A8/compile_a8_isolated_12g_v3.py'),prior['kernel'],str(D/sys.argv[1]),sys.argv[2],*prior['lean_path'].split(';')]
raise SystemExit(subprocess.call(args))
