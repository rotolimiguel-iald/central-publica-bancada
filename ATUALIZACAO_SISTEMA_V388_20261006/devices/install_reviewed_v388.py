"""Install reviewed sealed v388 bytes only. No scientific or device code imports/executions."""
from pathlib import Path
import os, json, hashlib, datetime, uuid, traceback, ast
ROOT=Path(__file__).resolve().parent
CENTRAL=Path(r"C:\IALD\Central de Patentes")
VAULT=CENTRAL/"vault/originals_copy"
STAGE=ROOT/"stage"
REVIEW=ROOT.parent/"science_audit/devices_review"
PLAN=ROOT/"PLANO_INSTALACAO_COMPLETO.json"
DELIVERY=ROOT/"MANIFESTO_ENTREGA_V388.json"
ATTEMPT=str(uuid.uuid4())
STAMP=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PROGRESS=ROOT/"install_progress"
events=[];installed=[];backups=[];temporary_dirs={}
phase="START"
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {"path":str(p),"bytes":len(b),"sha256":digest(b)}
def same(p,e):
 q=pin(p)
 if q["bytes"]!=e["bytes"] or q["sha256"]!=e["sha256"]:
  raise RuntimeError("Pin mismatch: "+str(p))
 return q
def contained(p,root):
 r=root.resolve();q=p.resolve(strict=False)
 if not q.is_relative_to(r):raise RuntimeError("Path escapes root: "+str(p))
 return q
def no_reparse(p):
 for q in (p,*p.parents):
  if q.exists() and getattr(q.lstat(),"st_file_attributes",0)&0x400:
   raise RuntimeError("Reparse point forbidden: "+str(q))
def atomic_new(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():raise RuntimeError("No overwrite: "+str(p))
 temp=p.with_name("."+p.name+".tmp_"+ATTEMPT)
 with temp.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
 if temp.read_bytes()!=b:raise RuntimeError("Temporary write mismatch")
 if p.exists():raise RuntimeError("Concurrent destination")
 os.rename(temp,p)
def save_new(p,o):
 atomic_new(p,(json.dumps(o,ensure_ascii=False,indent=2)+"\n").encode())
def event(event_name,**details):
 e={"seq":len(events)+1,"utc":now(),"attempt_id":ATTEMPT,"event":event_name,**details}
 save_new(PROGRESS/(f"{len(events)+1:04d}_{event_name}.json"),e);events.append(e)
def cas(entry):
 dst=Path(entry["live_destination"]);no_reparse(dst)
 old=entry.get("current")
 if old is None:
  if dst.exists():raise RuntimeError("Expected absent destination appeared: "+str(dst))
 else:same(dst,old)
def rename_directory(source,target):
 # Both resolved absolute paths must be siblings within exactly the designated custody root.
 s=contained(source,VAULT);t=contained(target,VAULT)
 if s.parent!=VAULT.resolve() or t.parent!=VAULT.resolve():
  raise RuntimeError("Custody rename is not a direct sibling operation")
 no_reparse(source);no_reparse(target)
 if target.exists():raise RuntimeError("Concurrent custody directory; stop, never overlay")
 event("BEFORE_CUSTODY_RENAME",source=str(s),target=str(t))
 os.rename(source,target)
 event("AFTER_CUSTODY_RENAME",source=str(s),target=str(t))
def main():
 global phase
 if (ROOT/"INSTALL_ATTEMPT.json").exists() or (ROOT/"RECIBO_INSTALACAO_V388.json").exists():
  raise RuntimeError("Existing installation attempt/result: inspect, never automatic replay")
 no_reparse(ROOT);no_reparse(CENTRAL);no_reparse(VAULT)
 if CENTRAL.resolve()!=CENTRAL.absolute() or VAULT.resolve()!=VAULT.absolute():
  raise RuntimeError("Unexpected custody root resolution")
 review_manifest=json.loads((REVIEW/"MANIFESTO_REVISAO.json").read_bytes())
 review_pins=[]
 for e in review_manifest["files"]:
  q=contained(Path(e["path"]),REVIEW);review_pins.append(same(q,e))
 delivery_pin=same(DELIVERY,review_manifest["source_delivery_manifest"])
 delta=json.loads((REVIEW/"REVISAO_DELTA_FINAL.json").read_bytes())
 if delta["unresolved_blockers"] or not delta["all_1823_member_pins"] or not delta["unified_plan_exact"]:
  raise RuntimeError("Independent final review has unresolved blockers")
 delivery=json.loads(DELIVERY.read_bytes())
 for e in delivery["members"]:
  q=contained(ROOT/e["relative"],ROOT);same(q,e)
 plan=json.loads(PLAN.read_bytes())
 by_rel={e["relative"]:e for e in delivery["members"]}
 plan_pin=same(PLAN,by_rel["PLANO_INSTALACAO_COMPLETO.json"])
 inv=json.loads((ROOT/"INVENTARIO_DISPOSITIVOS.json").read_bytes())
 expected_regular={
  (CENTRAL/"patents/_formula_completa/ADENDO_V388_METADATA.json").resolve(),
  (CENTRAL/"patents/_formula_completa/tgl_formula_completa.py").resolve()}
 for d in inv["devices"]:
  m=Path(d["bundle_manifest"]["path"]).resolve()
  expected_regular.update((m,m.with_name(m.name.replace(".manifest.json",".py"))))
 if len(expected_regular)!=34:raise RuntimeError("Wrong regular-file allowlist")
 custody={name:[] for name in ("tgl_kernel_v388","um_unificado_v388")}
 regular=[];seen=set();preflight=[]
 mapping=plan["mapping"]
 if len(mapping)!=1267:raise RuntimeError("Wrong mapping count")
 phase="PREFLIGHT_ALL_1267"
 for e in mapping:
  src=contained(Path(e["staged"]["path"]),STAGE);no_reparse(src);same(src,e["staged"])
  dst=contained(Path(e["live_destination"]),CENTRAL);no_reparse(dst)
  if dst in seen:raise RuntimeError("Duplicate destination")
  seen.add(dst)
  if dst.is_relative_to(VAULT.resolve()):
   rel=dst.relative_to(VAULT.resolve())
   if len(rel.parts)<2 or rel.parts[0] not in custody:raise RuntimeError("Unexpected custody scope")
   if e["policy"]!="CREATE_NEW_VERSION_ONLY_STOP_IF_EXISTS":raise RuntimeError("Wrong custody policy")
   custody[rel.parts[0]].append(e)
   if dst.exists():raise RuntimeError("Concurrent custody file")
  elif dst in expected_regular:
   if e["policy"]!="BACKUP_EXACT_BYTES_THEN_VERIFY_TEMP_AND_ATOMIC_REPLACE":raise RuntimeError("Wrong regular policy")
   regular.append(e);cas(e)
  else:raise RuntimeError("Destination not explicitly admitted")
  preflight.append({"destination":str(dst),"staged":e["staged"],"prior":e.get("current"),"passed":True})
 if sum(map(len,custody.values()))!=1233 or len(regular)!=34:raise RuntimeError("Wrong partition counts")
 if {Path(e["live_destination"]).resolve() for e in regular}!=expected_regular:raise RuntimeError("Regular set differs")
 for name in custody:
  dst=VAULT/name
  if dst.exists():raise RuntimeError("Concurrent v388 custody exists; reconcile")
  temp=VAULT/("."+name+".installing_"+ATTEMPT)
  if temp.exists():raise RuntimeError("Temporary custody path exists")
  contained(temp,VAULT);temporary_dirs[name]=temp
 # No production mutation occurred before the complete preflight above.
 decision={"attempt_id":ATTEMPT,"stage_id":plan["stage_id"],"utc":now(),
  "decision_origin":"/root coordination message explicitly approving internal reviewed v388 installation",
  "decision":"INSTALL_REVIEWED_SEALED_V388_BYTES_ONLY",
  "scope":"1267 mapped destinations: 1233 new custody files, 2 shared files, 32 FINAL files/manifests",
  "plan":plan_pin,"review_manifest":pin(REVIEW/"MANIFESTO_REVISAO.json"),"review_members":review_pins,
  "delivery_manifest":delivery_pin,"sealed_um_sha256":json.loads((STAGE/"patents/_formula_completa/ADENDO_V388_METADATA.json").read_bytes())["source_um_sha256"],
  "excluded":["changed live um.py","scientific execution","device/runners/full candidate imports","network/public release","shared memory/ledger"],
  "atomicity":"Per-file replacement and per-directory rename only; not a multi-file transaction"}
 save_new(ROOT/"ROOT_INSTALL_DECISION.json",decision)
 save_new(ROOT/"INSTALL_ATTEMPT.json",{"attempt_id":ATTEMPT,"utc":now(),"pid":os.getpid(),"status":"STARTED_AFTER_FULL_PREFLIGHT","plan":plan_pin,"retry":"NO_AUTOMATIC_REPLAY"})
 save_new(ROOT/"PREFLIGHT_INSTALACAO_V388.json",{"attempt_id":ATTEMPT,"utc":now(),"all_passed":True,"mapping_count":len(preflight),"existing_destinations":sum(e.get("current") is not None for e in mapping),"items":preflight})
 event("PREFLIGHT_COMPLETE",mappings=1267,existing_files=33,new_regular_files=1,new_custody_files=1233)
 phase="BUILD_CUSTODY_TEMPORARIES"
 for name,entries in custody.items():
  temp=temporary_dirs[name];temp.mkdir()
  for e in entries:
   src=Path(e["staged"]["path"]);raw=src.read_bytes()
   if digest(raw)!=e["staged"]["sha256"] or len(raw)!=e["staged"]["bytes"]:raise RuntimeError("Stage changed")
   rel=Path(e["live_destination"]).resolve().relative_to((VAULT/name).resolve())
   q=contained(temp/rel,temp);atomic_new(q,raw);same(q,e["staged"])
  expected={Path(e["live_destination"]).resolve().relative_to((VAULT/name).resolve()).as_posix() for e in entries}
  actual={q.relative_to(temp).as_posix() for q in temp.rglob("*") if q.is_file()}
  if actual!=expected:raise RuntimeError("Temporary custody is not complete/exact")
  event("CUSTODY_TEMP_COMPLETE",name=name,path=str(temp.resolve()),files=len(entries))
 phase="BACKUP_ALL_EXISTING_33"
 for e in regular:
  cas(e)
  if e.get("current") is not None:
   dst=Path(e["live_destination"]);raw=dst.read_bytes()
   if digest(raw)!=e["current"]["sha256"] or len(raw)!=e["current"]["bytes"]:raise RuntimeError("Concurrent existing change")
   backup=dst.with_name(dst.name+".bak_v388_"+STAMP+"_"+ATTEMPT)
   contained(backup,CENTRAL);atomic_new(backup,raw);same(backup,e["current"])
   backups.append({"destination":str(dst),"backup":pin(backup),"original_pin":e["current"]})
 event("ALL_BACKUPS_VERIFIED",count=len(backups),backups=backups)
 # Recheck all preconditions again before any visible destination publication.
 for name in custody:
  if (VAULT/name).exists():raise RuntimeError("Concurrent custody after staging")
 for e in regular:cas(e)
 phase="PUBLISH_KERNEL_FIRST"
 rename_directory(temporary_dirs["tgl_kernel_v388"],VAULT/"tgl_kernel_v388")
 installed.extend(str(Path(e["live_destination"])) for e in custody["tgl_kernel_v388"])
 phase="PUBLISH_UM_SECOND"
 rename_directory(temporary_dirs["um_unificado_v388"],VAULT/"um_unificado_v388")
 installed.extend(str(Path(e["live_destination"])) for e in custody["um_unificado_v388"])
 phase="ATOMIC_REGULAR_FILE_INSTALL"
 # Metadata before shared module; thereafter each FINAL and its manifest, preserving plan order.
 for e in regular:
  dst=Path(e["live_destination"]);src=Path(e["staged"]["path"]);raw=src.read_bytes()
  if digest(raw)!=e["staged"]["sha256"] or len(raw)!=e["staged"]["bytes"]:raise RuntimeError("Stage drift")
  cas(e)
  temp=dst.with_name("."+dst.name+".installing_"+ATTEMPT)
  contained(temp,CENTRAL);no_reparse(temp)
  with temp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
  same(temp,e["staged"]);cas(e)
  event("BEFORE_FILE_PUBLISH",destination=str(dst),temporary=str(temp),expected=e["staged"])
  if e.get("current") is None:
   os.rename(temp,dst) # Windows refuses replacing a concurrently created destination.
  else:
   os.replace(temp,dst)
  same(dst,e["staged"]);installed.append(str(dst))
  event("AFTER_FILE_READBACK",destination=str(dst),pin=pin(dst))
 phase="READBACK_ALL_1267"
 readback=[same(Path(e["live_destination"]),e["staged"]) for e in mapping]
 for b in backups:same(Path(b["backup"]["path"]),b["original_pin"])
 matrix=[]
 for d in inv["devices"]:
  m=Path(d["bundle_manifest"]["path"]);f=m.with_name(m.name.replace(".manifest.json",".py"))
  md=json.loads(m.read_bytes());fp=pin(f)
  if md["final_bytes"]!=fp["bytes"] or md["final_sha256"]!=fp["sha256"]:raise RuntimeError("Final metadata readback mismatch")
  matrix.append({"device":d["device_directory"],"FINAL":fp,"manifest":pin(m),"shared_layer":pin(CENTRAL/"patents/_formula_completa/tgl_formula_completa.py"),
   "typed_addendum":"v388","base_beta0":"PRESERVED","mu":"OPEN","status":"INSTALLED_BYTES_VERIFIED_NOT_DEVICE_EXECUTED","device_runtime_executed":False,"historic_results_and_seals":"NOT_TARGETED_OR_WRITTEN"})
 event("ALL_DESTINATIONS_READBACK_COMPLETE",count=len(readback),backups=len(backups),devices=len(matrix))
 phase="COMPLETE"
 receipt={"attempt_id":ATTEMPT,"stage_id":plan["stage_id"],"utc":now(),"status":"INSTALLED_ALL_1267_BYTES_VERIFIED",
  "pid":os.getpid(),"plan":plan_pin,"review_manifest":pin(REVIEW/"MANIFESTO_REVISAO.json"),
  "decision":pin(ROOT/"ROOT_INSTALL_DECISION.json"),"preflight":pin(ROOT/"PREFLIGHT_INSTALACAO_V388.json"),
  "installed_count":len(readback),"installed":readback,"backups":backups,"device_matrix":matrix,
  "new_custody_roots":[str(VAULT/"tgl_kernel_v388"),str(VAULT/"um_unificado_v388")],
  "publication_order":["tgl_kernel_v388","um_unificado_v388","shared metadata","shared module","16 FINALs and manifests"],
  "atomicity":"Per-directory rename/per-file replacement; no multi-file atomicity promised. All final pins were read back.",
  "cas_scope":"Hash/size preflight for every existing destination and immediately before replacement; no OS-wide transaction.",
  "snapshot":"v388 sealed e64; changed live um.py was not read/imported/copied",
  "beta0":"UNCHANGED","mu":"OPEN","v386_custody":"NOT_MODIFIED",
  "execution":{"um_py":0,"Lean":0,"devices":0,"runners":0,"full_candidate_imports":0,"network":0,"public_release":0},
  "not_claimed":["Scientific confirmation","Fresh device runtime results","Public release","Changed live um.py installed"]}
 save_new(ROOT/"RECIBO_INSTALACAO_V388.json",receipt)
 print(json.dumps({"status":receipt["status"],"attempt_id":ATTEMPT,"pid":os.getpid(),"installed":len(readback),"backups":len(backups),"devices":len(matrix),"receipt":pin(ROOT/"RECIBO_INSTALACAO_V388.json")},ensure_ascii=False))
if __name__=="__main__":
 try:main()
 except BaseException as exc:
  failure={"attempt_id":ATTEMPT,"utc":now(),"status":"STOPPED_FAILURE_REQUIRES_INSPECTION_NO_AUTOMATIC_RETRY","phase":phase,"pid":os.getpid(),
   "exception_type":type(exc).__name__,"message":str(exc),"traceback":traceback.format_exc(),
   "installed_recorded_count":len(installed),"installed_recorded_paths":installed,"backups":backups,
   "temporary_dirs":{k:str(v) for k,v in temporary_dirs.items()},"last_event":events[-1] if events else None,
   "no_multi_file_atomicity":True,"action":"Inspect physical state and recorded identities; do not relaunch automatically"}
  result=ROOT/"RECIBO_INSTALACAO_V388.json"
  if not result.exists():
   try:save_new(result,failure)
   except BaseException as persist_error:print("Could not persist terminal receipt:",repr(persist_error))
  print(json.dumps(failure,ensure_ascii=False))
  raise SystemExit(1)
