from pathlib import Path
import sys,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'D4'
x=json.loads((R/'D3prime/contract_fixed_01.json').read_bytes())
args=[sys.executable,'-X','utf8','-B',str(R/'A8/compile_a8_isolated_12g_v3.py'),x['kernel'],str(D/sys.argv[1]),sys.argv[2],*x['lean_path'].split(';')]
raise SystemExit(subprocess.call(args))
