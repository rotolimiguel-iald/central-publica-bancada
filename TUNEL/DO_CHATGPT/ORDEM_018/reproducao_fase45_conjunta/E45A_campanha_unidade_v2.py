"""Single-unit guard for the explicitly authorized historical E45A campaign. No automatic batch."""
import sys,json,pathlib,os,hashlib,datetime,subprocess,time,math,traceback
ROOT=pathlib.Path(__file__).resolve().parent
CAMP=ROOT/"E45A_CONTINUACAO_CAMPANHA_V2.json"
STATE=ROOT/"E45A_ESTADO_CAMPANHA_V2.json"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write_state(d):
 old=STATE.read_bytes();backup=STATE.with_name(STATE.name+".bak_"+datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
 backup.write_bytes(old);assert backup.read_bytes()==old
 b=(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
 temp=STATE.with_suffix(".tmp");temp.write_bytes(b);assert temp.read_bytes()==b;os.replace(temp,STATE)
def save_new(p,b):
 assert not p.exists(),str(p);t=p.with_suffix(p.suffix+".tmp");t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def main():
 assert len(sys.argv)==2,"Give one authorized index, never a batch."
 index=int(sys.argv[1]);camp=json.loads(CAMP.read_bytes());state=json.loads(STATE.read_bytes())
 assert sha(pathlib.Path(__file__))==camp["controller_sha256"],"controller pin"
 assert state["campaign_sha256"]==sha(CAMP),"campaign pin"
 assert state["status"]=="READY" and state["next_index"]==index,"campaign is not ready for this unit; no retry"
 unit=camp["units"][index];name=unit["result_name"];resultpath=ROOT/name
 assert not resultpath.exists(),"result already exists; do not rerun"
 for f in camp["source_pins"]:assert sha(ROOT/f["name"])==f["sha256"],"input pin "+f["name"]
 state["status"]="RUNNING";state["current_index"]=index
 state["units"][index].update(status="DISPATCHING_NO_RETRY",started_utc=stamp(),result_absent=True)
 write_state(state);wall=time.perf_counter()
 try:
  args=[r"C:\Python314\python.exe","-X","utf8",str(ROOT/"E45A_aceleracao_exata.py"),"grid",unit["family"],unit["model"],str(unit["n"]),"--max-seconds","600"]
  # Exactly one process. Timeout is terminal; no fallback/retry.
  run=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=630)
  prefix=ROOT/("E45A_UNIDADE_%02d"%index)
  save_new(prefix.with_suffix(".stdout.txt"),run.stdout);save_new(prefix.with_suffix(".stderr.txt"),run.stderr)
  assert resultpath.exists(),"child produced no result; uncertain/failed, do not repeat"
  result=json.loads(resultpath.read_bytes());source=camp["source_pins"];source_map={x["name"]:x["sha256"] for x in source}
  checks={"exit_zero":run.returncode==0,"complete":result.get("status")=="EXACT_SINGLE_GRID_COMPLETE_NO_VERDICT" and result.get("observational_integral_completed") is True,
   "unit_identity":(result["family"],result["model"],result["n"])==(unit["family"],unit["model"],unit["n"]),
   "total_processed":result["total_nodes"]==result["processed_nodes"]==unit["n"]**(4 if unit["model"]=="livre" else 3),
   "finite_counts":0<result["finite_nodes"]<=result["total_nodes"] and 0<result["backgrounds_evaluated"]<=unit["n"]**3,
   "finite_lnZ":math.isfinite(result["lnZ"]) if result.get("lnZ") is not None else False,
   "wall_limit":result["resources"]["wall"]<600,"memory_limit":result["resources"]["peak_bytes"]<536870912,
   "code_pin":result["code_sha256"]==source_map["E45A_aceleracao_exata.py"],"protocol_pin":result["protocol_sha256"]==source_map["E45A_PROTOCOLO.json"],
   "validation_pin":result["validation_sha256"]==source_map["E45A_VALIDACAO.json"],
   "no_refit":result["fits_rerun"] is False,"no_originals":result["originals_executed"] is False,"no_MCMC":result["monte_carlo"] is False,
   "no_scientific_verdict":result["scientific_verdict"] is None}
  assert all(checks.values()),checks
  old=json.loads((ROOT/"P45_ALVOS_HISTORICOS.json").read_bytes())[unit["family"]]["evidencia"]["lnZ"][unit["model"]]
  item=dict(status="COMPLETE_VERIFIED",finished_utc=stamp(),command=args,result_sha256=sha(resultpath),result_bytes=resultpath.stat().st_size,
   checks=checks,lnZ=result["lnZ"],archive_n25_lnZ=old,difference_from_archive_n25=result["lnZ"]-old,
   counts={k:result[k] for k in ("total_nodes","processed_nodes","finite_nodes","backgrounds_evaluated")},resources=result["resources"],controller_wall=time.perf_counter()-wall,
   output_files=[str(prefix.with_suffix(".stdout.txt")),str(prefix.with_suffix(".stderr.txt"))])
  state["units"][index].update(item);state["next_index"]=index+1;state["current_index"]=None
  state["status"]="COMPLETE" if index+1==len(camp["units"]) else "READY"
  write_state(state)
  print(json.dumps({"index":index,"unit":unit,"receipt":item,"next_index":state["next_index"],"campaign_status":state["status"]},ensure_ascii=False))
  return 0
 except BaseException as error:
  state["status"]="STOPPED_NO_RETRY";state["units"][index].update(status="FAILED_OR_UNCERTAIN_NO_RETRY",error=repr(error),traceback=traceback.format_exc(),finished_utc=stamp())
  write_state(state);print(json.dumps({"index":index,"status":state["status"],"error":repr(error)},ensure_ascii=False));return 2
if __name__=="__main__":raise SystemExit(main())

