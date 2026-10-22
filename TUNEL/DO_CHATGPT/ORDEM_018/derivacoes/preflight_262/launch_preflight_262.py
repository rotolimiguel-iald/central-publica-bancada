"""One-shot local launcher; timeout and terminal receipts, no retry."""
from pathlib import Path
import sys,os,json,subprocess,hashlib,time,datetime
ROOT=Path(__file__).resolve().parent
def put(n,obj):
 p=ROOT/n
 if p.exists():raise RuntimeError("Refusing overwrite "+str(p))
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8");t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(b)
 assert t.read_bytes()==b;t.replace(p)
def main():
 protocol=json.loads((ROOT/"PROTOCOLO_PREFLIGHT_262.json").read_bytes())
 for item in protocol["inputs"]:
  b=Path(item["path"]).read_bytes()
  assert len(b)==item["bytes"] and hashlib.sha256(b).hexdigest()==item["sha256"],item["path"]
 for n in ["PREFLIGHT_262_RESULT.json","PREFLIGHT_262_FAILURE.json","PREFLIGHT_262_LAUNCH.json","CLAIM.json"]:
  assert not (ROOT/n).exists(),"Existing or uncertain unit: "+n
 put("CLAIM.json",{"id":protocol["id"],"claimed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"protocol_sha256":hashlib.sha256((ROOT/"PROTOCOLO_PREFLIGHT_262.json").read_bytes()).hexdigest()})
 env=os.environ.copy()
 for k in protocol["threads_env"]:env[k]="1"
 env["PYTHONDONTWRITEBYTECODE"]="1"
 started=time.perf_counter()
 try:
  cp=subprocess.run([sys.executable,"-X","utf8",str(ROOT/"preflight_262.py")],env=env,cwd=ROOT,capture_output=True,text=True,encoding="utf-8",timeout=protocol["max_wall_seconds"],creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
  state={"status":"COMPLETED" if cp.returncode==0 else "FAILED_NO_RETRY","returncode":cp.returncode,"stdout":cp.stdout,"stderr":cp.stderr}
 except subprocess.TimeoutExpired as e:
  state={"status":"TIMEOUT_NO_RETRY","stdout":str(e.stdout),"stderr":str(e.stderr)}
 state["wall_seconds"]=time.perf_counter()-started;state["hard_timeout_seconds"]=protocol["max_wall_seconds"];state["interpreter"]=sys.executable
 put("PREFLIGHT_262_LAUNCH.json",state)
 print(json.dumps(state,ensure_ascii=False))
 if state["status"]!="COMPLETED":raise SystemExit(1)
if __name__=="__main__":main()
