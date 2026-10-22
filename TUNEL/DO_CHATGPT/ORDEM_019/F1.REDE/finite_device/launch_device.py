"""Launch the preregistered run once, preserving the execution record."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,x):
    with p.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(x,f,ensure_ascii=False,indent=2,allow_nan=False); f.write("\n")

def main():
    for name in ["RUN_MANIFEST_DEVICE_R1.json","RUN_DEVICE_R1.log","RUN_RECEIPT_DEVICE_R1.json","RESULTADO_DEVICE_R1.json"]:
        if (BASE/name).exists(): raise FileExistsError(name)
    freeze=BASE/"FREEZE_DEVICE_R1.json"; fr=json.loads(freeze.read_text(encoding="utf-8"))
    if sha(BASE/"run_finite_device.py")!=fr["runner"]["sha256"]: raise RuntimeError("Frozen runner changed")
    command=[sys.executable,"-B","-X","utf8",str(BASE/"run_finite_device.py")]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write_new(BASE/"RUN_MANIFEST_DEVICE_R1.json",{"command":command,"cwd":str(BASE),"started_utc":start,"freeze_sha256":sha(freeze),"launcher_sha256":sha(Path(__file__))})
    t0=time.perf_counter(); r=subprocess.run(command,cwd=BASE,capture_output=True); seconds=time.perf_counter()-t0
    end=datetime.datetime.now(datetime.timezone.utc).isoformat()
    head={"command":command,"started_utc":start,"finished_utc":end,"seconds":seconds,"exit_code":r.returncode}
    log=BASE/"RUN_DEVICE_R1.log"
    with log.open("xb") as f: f.write((json.dumps(head,ensure_ascii=False,indent=2)+"\nSTDOUT+STDERR\n").encode()+r.stdout+r.stderr)
    result=BASE/"RESULTADO_DEVICE_R1.json"
    write_new(BASE/"RUN_RECEIPT_DEVICE_R1.json",{**head,"log_sha256":sha(log),"result_sha256":sha(result) if result.exists() else None,"freeze_sha256":sha(freeze)})
    print(r.stdout.decode("utf-8","replace")); print(r.stderr.decode("utf-8","replace"))
    print(json.dumps(head,ensure_ascii=False)); raise SystemExit(r.returncode)

if __name__ == "__main__": main()
