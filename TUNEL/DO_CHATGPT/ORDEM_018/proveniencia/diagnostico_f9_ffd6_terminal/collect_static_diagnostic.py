"""Static post-terminal evidence collection. No candidate imports or Linux processes."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os, re
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
PACKAGE=ROOT/"f9_engine_assembly_integration_preparation"
OUT=Path(__file__).parent
UNC=r"\\wsl.localhost\Ubuntu-24.04"

def atomic(path,raw):
    if path.exists():
        old=path.read_bytes();b=path.with_name(path.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"));b.write_bytes(old);assert b.read_bytes()==old
    t=path.with_name(path.name+".tmp");t.write_bytes(raw);assert t.read_bytes()==raw and raw;os.replace(t,path)

def pin(path):
    b=path.read_bytes();return {"path":str(path),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()},b

inventory=json.loads((PACKAGE/"RUNTIME_INVENTORY.json").read_bytes())
pins={r["path"]:r for r in inventory["pins"]}
relative={
"camb/__init__.py":[(12,20)], "camb/model.py":[(1,9)],"camb/bbn.py":[(1,16)],
"scipy/interpolate/__init__.py":[(188,196)],"scipy/interpolate/_interpolate.py":[(1,18)],
"scipy/special/__init__.py":[(780,790)],"scipy/linalg/__init__.py":[(199,205)],
"scipy/linalg/_misc.py":[(1,8)],"scipy/_lib/_util.py":[(13,22)],
"scipy/_lib/_array_api.py":[(21,49)],"scipy/_external/array_api_compat/numpy/__init__.py":[(1,12)],
"scipy/_external/array_api_compat/_internal.py":[(56,71)],
"numpy/__init__.py":[(624,631),(672,693),(728,739)],
"numpy/f2py/__init__.py":[(12,21)],"numpy/f2py/f2py2e.py":[(13,30)],
"numpy/f2py/crackfortran.py":[(142,157)],
"charset_normalizer/__init__.py":[(24,34)],
}
files={"/opt/lal_env/lib/python3.12/site-packages/"+k:v for k,v in relative.items()}
files.update({"/usr/lib/python3.12/importlib/metadata/__init__.py":[(637,646),(678,703)],
"/usr/lib/python3.12/zipfile/_path/__init__.py":[(146,161),(269,280)],
"/usr/lib/python3.12/importlib/_bootstrap_external.py":[(1074,1135)],
"/usr/lib/python3.12/traceback.py":[(399,415)],
"/usr/lib/python3.12/zipimport.py":[(72,95),(343,347)]})
rows=[]
for path,ranges in files.items():
    meta,raw=pin(Path(UNC+path.replace("/","\\")))
    lines=raw.decode("utf-8").splitlines();expected=pins.get(path)
    rows.append({"runtime_path":path,**meta,"pin_present_in_consumed_inventory":expected is not None,
        "pin_matches":None if expected is None else all(meta[k]==expected[k] for k in ("bytes","sha256")),
        "excerpts":[{"line":n,"text":lines[n-1]} for lo,hi in ranges for n in range(lo,min(len(lines),hi)+1)]})
so="/opt/lal_env/lib/python3.12/site-packages/scipy/special/_ufuncs.cpython-312-x86_64-linux-gnu.so"
meta,raw=pin(Path(UNC+so.replace("/","\\")))
needles=[b"scipy.linalg.cython_lapack",b"scipy.special._ufuncs_cxx",b"scipy._cyutility"]
rows.append({"runtime_path":so,**meta,"pin_present_in_consumed_inventory":True,
    "pin_matches":all(meta[k]==pins[so][k] for k in ("bytes","sha256")),
    "literal_binary_reference_offsets":{v.decode():[m.start() for m in re.finditer(re.escape(v),raw)] for v in needles},
    "interpretation":"Static binary references only; not observed call stack or reconstructed source."})
local=[]
for path in [PACKAGE/"MANIFESTO_PREPARACAO.json",PACKAGE/"CONTRATO_WSL.json",PACKAGE/"RUNTIME_INVENTORY.json",PACKAGE/"worker.py",PACKAGE/"sources/audit_guard.py",PACKAGE/"RUN/CASE/CASE_RESULT.json",PACKAGE/"RUN/CASE/journal.jsonl",ROOT/"proveniencia/revisao_f9_engine_assembly/PARECER_F9_ENGINE_ASSEMBLY.md",ROOT/"proveniencia/revisao_f9_engine_assembly/RECIBO_REVISAO_F9_ENGINE_ASSEMBLY.json",ROOT/"proveniencia/revisao_f9_engine_assembly/MANIFESTO_REVISAO_F9_ENGINE_ASSEMBLY.json"]:
    meta,_=pin(path);local.append(meta)
case=json.loads((PACKAGE/"RUN/CASE/CASE_RESULT.json").read_bytes())
journal=[json.loads(x) for x in (PACKAGE/"RUN/CASE/journal.jsonl").read_bytes().splitlines()]
targets=[]
for e in journal:
    name=e["target"];q=Path(UNC+name.replace("/","\\"))
    try:
        st=q.stat();state={"exists_now_via_UNC":True,"bytes_now":st.st_size}
    except FileNotFoundError:state={"exists_now_via_UNC":False}
    item={"target":name,"sequence":e["sequence"],"pin_present":name in pins,
          "inside_any_admitted_runtime_root":any(name==root or name.startswith(root.rstrip("/")+"/") for root in inventory["roots"]),**state}
    if name.endswith(".pyc") and state["exists_now_via_UNC"]:
        meta,_=pin(q);item["current_hash"]=meta
    targets.append(item)
result={"schema":"F9_FFD6_TERMINAL_STATIC_DIAGNOSTIC_EVIDENCE_V1","at":datetime.now(timezone.utc).isoformat(),
"request_id":case["request_id"],"map_before_last_record":556,"status":"POST_TERMINAL_READ_ONLY_NOT_RETRY",
"local_source_pins":local,"runtime_sources":rows,"runtime_source_count":len(rows),
"all_present_runtime_pins_match":all(r["pin_matches"] is not False for r in rows),
"case_summary":{k:case[k] for k in ["status","solver_calls_attempted","solver_calls_returned","artifacts","module_errors","native_mapping_errors","missing_runtime_probes","error","process","nonce"]},
"journal_equals_snapshot":journal==case["audit_snapshot"]["events"],"denials":journal,"target_metadata_now":targets,
"evidence_limits":["Positive traceback limit8 retains first eight frames, not final eight.","Current UNC absence is not proof of historical state; open audit event does not prove content read.","Binary reference is static dependency evidence, not a fully preserved dynamic stack.","Zero get_background attempts does not claim zero native library initialization."],
"actions":{"candidate_imports":0,"candidate_runs":0,"WSL_processes":0,"solver_calls":0,"allowlist_changes":0,"auth_claim_or_consumed_package_edits":0}}
atomic(OUT/"EVIDENCIA_ESTATICA_FFD6.json",(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode())
print(json.dumps({"evidence":pin(OUT/"EVIDENCIA_ESTATICA_FFD6.json")[0],"runtime_sources":len(rows),"all_pins_match":result["all_present_runtime_pins_match"],"journal_matches":result["journal_equals_snapshot"],"targets":targets},ensure_ascii=False))
