"""Immutable evidence receipt for the preregistered ADENDO1 Lean candidates."""
import datetime, hashlib, json, pathlib, re
base=pathlib.Path(__file__).resolve().parent
unit=base.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta=lambda p:dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
fragment=(base.parent/"sources/VERBATIMS_DOCSTRING_FRAGMENT_R1.txt").read_bytes()
prereg=base.parent/"PREREGISTRO_ADENDO1_R1.json"
preg=json.loads(prereg.read_text(encoding="utf-8"))
assert sha(prereg)=="724b3e7b1b3bc73ed32ea3c637513a918c508a627fe983a30407ed5750ef10be"
old=unit/"lean_candidate/TheSingularityReadsTheAttractor.lean"
copy=base/"TheSingularityReadsTheAttractorAdendo1.lean"
assert copy.read_bytes().count(fragment+b"\n")==1
assert copy.read_bytes().replace(fragment+b"\n",b"",1)==old.read_bytes()
accepted=[]
all_attempts=[]
for name,index in [("TheSingularityReadsTheAttractorAdendo1","001"),("TheLightReadsItself","002")]:
 src=base/(name+".lean")
 b=src.read_bytes(); text=b.decode("utf-8")
 assert not re.search(r"\b(?:sorry|admit|axiom)\b",text)
 assert b.count(fragment)==1
 spans=[]
 for v in preg["verbatims"]:
  vp=pathlib.Path(v["custody"]); vb=vp.read_bytes()
  assert sha(vp)==v["sha256"]
  start=b.index(vb)
  spans.append(dict(id=v["id"],sha256=sha(vp),byte_range=[start,start+len(vb)]))
 out=base/"attempts"/name/index
 rec=json.loads((out/"RECEIPT.json").read_text(encoding="utf-8"))
 assert rec["exit_code"]==0 and rec["source_sha256"]==sha(src)
 assert (out/src.name).read_bytes()==b
 log=(out/"BUILD.log").read_text(encoding="utf-8")
 matches=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log,re.S)
 expected=re.findall(r"^#print axioms (.+)$",text,re.M)
 assert len(matches)==len(expected)
 axioms=[]
 for decl,axs in matches:
  names=[n.strip() for n in axs.split(",") if n.strip()]
  assert set(names)<=set(["propext","Classical.choice","Quot.sound"])
  axioms.append(dict(declaration=decl,axioms=names))
 accepted.append(dict(source=meta(src),attempt=index,receipt=meta(out/"RECEIPT.json"),build_log=meta(out/"BUILD.log"),olean=meta(out/(name+".olean")),printed_declarations=len(axioms),theorems_in_source=len(re.findall(r"^theorem ",text,re.M)),axioms=axioms,sorry_tokens=0,verbatim_spans=spans))
 for d in sorted((base/"attempts"/name).iterdir()):
  rr=json.loads((d/"RECEIPT.json").read_text(encoding="utf-8"))
  full=json.dumps(rr,ensure_ascii=False,indent=2).encode()+b"\n\n--- LEAN STDOUT + STDERR ---\n"+(d/"BUILD.log").read_bytes()
  with (d/"BUILD_COMPLETE_R1.log").open("xb") as f:f.write(full)
  all_attempts.append(dict(name=name,attempt=d.name,exit_code=rr["exit_code"],receipt=meta(d/"RECEIPT.json"),source_snapshot=meta(d/src.name),build_log=meta(d/"BUILD.log"),complete_build_log=meta(d/"BUILD_COMPLETE_R1.log")))
report={"schema":"F1.ATRATOR.ADENDO1.lean/v1","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"BUILT_IN_SANDBOX_AWAITING_INDEPENDENT_REVIEW","preregister":meta(prereg),"build_driver":meta(base/"build_adendo1.py"),"finalize_script":meta(pathlib.Path(__file__)),"original_A1_A4":meta(old),"original_recovered_byte_for_byte_by_removing_fragment":True,"accepted":accepted,"all_attempts":all_attempts,"scope":{"A1_A4":"Original proof body bytes preserved exactly; integral verbatims added in a fresh candidate.","A5":"PASSA: exact canonical real Pair/conjJ; readJ projects the function space onto the adJ-invariant part, fixes J and identity, and kills pairK. No independent reader parameter; no physical observer theorem.","A6":"FALHA of universal necessity for A1+A2+A3: identity dynamics and intrinsic identity projection satisfy all three, with fixed-space dimension two.","separation":"readJ acts on functions/operators; reading from A1-A4 acts on states. The angular matrix projection remains a separately typed reused theorem.","limits":"No ontological proof, no empirical creditation, no gate. Finite exact witnesses only; no Tomita antiunitary identification."},"failure_history":"TheLightReadsItself/001 failed at CLM identity iteration simplification only. Source and output retained; Lean emitted error-recovery sorryAx in that failed log. The accepted 002 log has only the trio and no sorryAx. No source ever used an explicit sorry/admit/axiom.","production_changed":False}
with (base/"FINAL_LEAN_ADENDO1_R1.json").open("x",encoding="utf-8",newline="\n") as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({"receipt":meta(base/"FINAL_LEAN_ADENDO1_R1.json"),"accepted":[{"source":v["source"],"printed_declarations":v["printed_declarations"],"theorems_in_source":v["theorems_in_source"]} for v in accepted]},ensure_ascii=False,indent=2))
