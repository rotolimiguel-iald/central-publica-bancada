import json
import subprocess
import sys
from pathlib import Path

BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
sys.path.insert(0,str(BASE))
from iald_orchestrator.worker_identity import require_expected_identity

if __name__ == '__main__':
    require_expected_identity()
    name=sys.argv[1]
    if name not in {'kimi_ram','mimo_domains'}: raise ValueError('Unknown unit')
    here=Path(__file__).resolve().parent
    out=here/(name+'.result.json')
    if out.exists(): raise ValueError('Result already recorded; inspect instead of repeating')
    r=subprocess.run([sys.executable,'-X','utf8',str(BASE/'transport_cli.py')],
        input=(here/(name+'.submit.json')).read_bytes(),capture_output=True,check=False)
    if r.returncode: raise RuntimeError(r.stderr.decode('utf-8','replace')[-1000:])
    d=json.loads(r.stdout)
    temp=out.with_suffix('.new');temp.write_bytes(r.stdout);temp.replace(out)
    print(json.dumps({k:d.get(k) for k in ('id','request_id','status','error')},ensure_ascii=False))
