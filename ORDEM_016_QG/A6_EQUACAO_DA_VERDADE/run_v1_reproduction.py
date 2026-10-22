from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A6_EQUACAO_DA_VERDADE/V1_verificacao_independente/verifica_equacao_da_verdade.py'
DEST = HERE/'D_harness/refeito_V1'
PYTHON = HERE.parent/'A4/symbolic_runtime/Scripts/python.exe'
DEST.mkdir(parents=True, exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def new(path, raw):
    assert not path.exists(), 'Refusing to overwrite: ' + str(path)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(path)

target=DEST/SOURCE.name
if not target.exists():
    new(target, SOURCE.read_bytes())
assert sha(target)==sha(SOURCE)
marker=DEST/'reproduction_started.json'
assert not marker.exists(), 'Prior run exists; inspect it instead of repeating'
new(marker, json.dumps(dict(at=datetime.now(timezone.utc).isoformat(), source_sha256=sha(SOURCE))).encode())
env=os.environ.copy()
env['PYTHONIOENCODING']='utf-8'
start=time.monotonic()
run=subprocess.run([str(PYTHON),'-X','utf8','-B',str(target)],cwd=DEST,env=env,
                   stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
wall=time.monotonic()-start
new(DEST/'reproduction.log',run.stdout)
result_path=DEST/'resultados_V1.json'
result=json.loads(result_path.read_bytes()) if result_path.exists() else None
version=subprocess.check_output([str(PYTHON),'-X','utf8','-c','import sympy; print(sympy.__version__)'],env=env).decode().strip()
receipt=dict(status='REAL_REPRODUCTION', rc=run.returncode, wall_seconds=wall, sympy=version,
             source_sha256=sha(target), original_sha256=sha(SOURCE), log_sha256=sha(DEST/'reproduction.log'),
             result_sha256=sha(result_path) if result else None,
             n_checks=result['n_checks'] if result else None,n_pass=result['n_pass'] if result else None,
             n_controls=result['n_controles'] if result else None,n_detected=result['n_detectados'] if result else None)
new(DEST/'reproduction_receipt.json', json.dumps(receipt,indent=2).encode())
print(json.dumps(receipt),flush=True)
assert run.returncode==0 and result['n_pass']==51 and result['n_detectados']==9
