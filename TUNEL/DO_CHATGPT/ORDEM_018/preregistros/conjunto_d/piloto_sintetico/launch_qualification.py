"""Launch exactly one contracted P1/P2 run; capture rc/logs/cost. No PE."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
ROOT=Path(__file__).resolve().parent
contract=json.loads((ROOT/"CONTRATO_P0_P2.json").read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for rel,pin in contract["inputs"].items():assert sha(ROOT/rel)==pin["sha256"],rel
assert sha(__file__)==contract["supervisor_sha256"]
assert not (ROOT/"EXECUTION_RECEIPT.json").exists()
cmd=contract["launch_command"]
start=time.perf_counter()
try:
    p=subprocess.run(cmd,capture_output=True,timeout=650,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
    rc=p.returncode;stdout=p.stdout;stderr=p.stderr;status="PROCESS_RETURNED"
except subprocess.TimeoutExpired as exc:
    rc=None;stdout=exc.stdout or b"";stderr=exc.stderr or b"";status="SUPERVISOR_TIMEOUT"
def write(name,raw):
    path=ROOT/name;assert not path.exists();tmp=path.with_name(path.name+".tmp");tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,path);return sha(path)
logs={"stdout_sha256":write("RUN_001.stdout.log",stdout),"stderr_sha256":write("RUN_001.stderr.log",stderr)}
r={"status":status,"finished_utc":datetime.now(timezone.utc).isoformat(),"returncode":rc,"command":cmd,
   "wall_seconds":time.perf_counter()-start,"logs":logs,"contract_sha256":sha(ROOT/"CONTRATO_P0_P2.json"),
   "original_source_checks":[dict(row,unchanged=sha(row["original"])==row["sha256"]) for row in json.loads((ROOT/"CONTRATO_PREFLIGHT.json").read_text())["copied_sources"]],
   "no_PE_authorized":True,"no_D_read_authorized":True}
write("EXECUTION_RECEIPT.json",(json.dumps(r,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps(r,ensure_ascii=False))
print(stdout.decode("utf-8",errors="replace")[-5000:])
print(stderr.decode("utf-8",errors="replace")[-2000:])
