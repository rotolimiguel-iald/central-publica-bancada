"""Independent static metadata review; never import candidates or start Linux."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, struct, sys
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
P=ROOT/"f9_engine_import_closure_repair_preparation"
OLD=ROOT/"f9_engine_assembly_integration_preparation"
OUT=ROOT/"proveniencia/revisao_f9_import_closure_repair"
checks=[]; sources={}
def pin(b):return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def read(p):
 b=p.read_bytes();sources[str(p)]=pin(b);return b
def obj(p):return json.loads(read(p))
def check(name,ok,detail=None):
 checks.append({"name":name,"pass":bool(ok),"detail":detail})
 if not ok: raise AssertionError(name)
def json_out(name,data):
 p=OUT/name; b=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode()
 assert not p.exists(),str(p)
 tmp=p.with_name(p.name+".tmp");tmp.write_bytes(b);assert tmp.read_bytes()==b;os.replace(tmp,p)
manifest=obj(P/"MANIFESTO_PREPARACAO.json");contract=obj(P/"CONTRATO_WSL.json")
oldcontract=obj(OLD/"CONTRATO_WSL.json")
for item in manifest["files"]:
 check("manifest:"+item["path"],pin(read(P/item["path"]))=={k:item[k] for k in ("bytes","sha256")})
for item in contract["local_pins"]:
 check("local_pin:"+item["relative_path"],pin(read(P/item["relative_path"]))=={k:item[k] for k in ("bytes","sha256")})
inv=obj(P/"RUNTIME_INVENTORY.json");prev=obj(OLD/"RUNTIME_INVENTORY.json")
new={x["path"]:x for x in inv["pins"]};old={x["path"]:x for x in prev["pins"]}
ev=obj(P/"DEPENDENCY_CLOSURE_EVIDENCE.json");dyn=obj(P/"DYNAMIC_CODEC_EVIDENCE.json")
check("5074_old_pins_unchanged",len(old)==5074 and all(new.get(k)==v for k,v in old.items()))
added={k:v for k,v in new.items() if k not in old}
check("27_exact_new_pins",len(added)==27 and added=={x["path"]:x for x in ev["new_runtime_pins"]})
check("roots_only_two",set(inv["roots"])-set(prev["roots"])=={"/opt/lal_env/lib/python3.12/site-packages/charset_normalizer","/opt/lal_env/lib/python3.12/site-packages/charset_normalizer-3.5.1.dist-info"} and set(prev["roots"])<=set(inv["roots"]))
for key in ("limits","linux_pins","windows_pins"):
 check("unchanged:"+key,contract[key]==oldcontract[key])
for key in ("loader_alias_checks_required","alias_resolution_metadata","unresolved_native_dependencies"):
 check("unchanged_runtime:"+key,inv[key]==prev[key])
check("exact_absent_probe_only",inv["exact_absent_probe_paths"]==["/usr/lib/python312.zip"])
check("builtin_unicodedata_only",inv["required_builtin_modules"]==["unicodedata"])
for f in ("common.py","linux_control.py","launch_windows.py"):
 before=read(OLD/f).decode()
 expected=before.replace(OLD.name,P.name).replace(oldcontract["request_id"],contract["request_id"])
 check("only_rebase:"+f,read(P/f).decode()==expected)
for f in P.rglob("*.py"):
 ast.parse(read(f),filename=str(f))
check("candidate_AST_only",True)
lineage=obj(P/"SOURCE_LINEAGE.json")
for f in lineage["exact_unchanged_copies"]:
 check("exact_copy:"+f,read(P/f)==read(OLD/f))
check("configuration_only_identity",{k:v for k,v in obj(P/"EFFECTIVE_CONFIGURATION.json").items() if k!="request_id"}=={k:v for k,v in obj(OLD/"EFFECTIVE_CONFIGURATION.json").items() if k!="request_id"})
for marker in ("AUTORIZACAO_ROOT.json","CLAIM.json","RUN","RESULT.json"):
 check("not_created:"+marker,not(P/marker).exists())
# Direct Windows reads of finite Linux paths: no WSL executable or candidate code.
prefix=r"\\wsl.localhost\Ubuntu-24.04"
def host(s):return Path(prefix+s.replace("/","\\"))
def linuxread(s):return read(host(s))
for path,record in added.items():
 check("UNC:"+path,pin(linuxread(path))=={k:record[k] for k in ("bytes","sha256")})
for item in ev["cache_headers"]:
 b=linuxread(item["path"]);flags,mtime,size=struct.unpack("<III",b[4:16])
 source=item["path"].replace("/__pycache__/","/").replace(".cpython-312.pyc",".py")
 sb=linuxread(source)
 check("cache_header:"+source,b[:4].hex()==item["magic_hex"] and flags==item["flags"]==0 and mtime==item["timestamp_header"]==int(host(source).stat().st_mtime) and size==item["source_size_header"]==len(sb))
# Names of modules, direct imports and dynamic sites collected independently with AST.
actual_edges=[];dynamic=[]
for path in sorted(k for k in added if k.endswith(".py")):
 text=linuxread(path).decode("utf-8");tree=ast.parse(text,filename=path)
 for node in ast.walk(tree):
  if isinstance(node,ast.Import):
   actual_edges.extend((path,node.lineno,a.name) for a in node.names)
  elif isinstance(node,ast.ImportFrom):
   target=("charset_normalizer."+node.module if node.level==1 and node.module else node.module)
   if target:actual_edges.append((path,node.lineno,target))
  elif isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="import_module":
   dynamic.append({"path":path,"line":node.lineno,"expression":ast.get_source_segment(text,node)})
check("59_import_edges",sorted(actual_edges)==sorted((x["source"],x["line"],x["target"]) for x in ev["import_edges"]),len(actual_edges))
# Build metadata is data, not interpreter execution.
builtin_records=ev["builtin_metadata"]
for key in ("sysconfig","inittab"):
 item=builtin_records[key]
 path=item["path"]; b=linuxread(path)
 check("builtin_metadata:"+key,pin(b)=={k:item[k] for k in ("bytes","sha256")})
 if key=="inittab": check("builtin_inittab_literal",b'{"unicodedata", PyInit_unicodedata}' in b)
 else:
  t=ast.parse(b);value=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=="build_time_vars" for x in n.targets))
  check("builtin_build_names","unicodedata" in value["MODBUILT_NAMES"].split())
constant_path="/opt/lal_env/lib/python3.12/site-packages/charset_normalizer/constant.py"
tree=ast.parse(linuxread(constant_path));n=next(n for n in tree.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id=="_KNOWN_MB_CLASSES")
check("known_provider_frozenset_shape",isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=="frozenset" and len(n.value.args)==1 and not n.value.keywords)
providers=ast.literal_eval(n.value.args[0])
check("six_exact_CJK",providers=={"_codecs_cn","_codecs_hk","_codecs_iso2022","_codecs_jp","_codecs_kr","_codecs_tw"})
for name in sorted(providers):
 candidates=[x for path,x in old.items() if Path(path).name.startswith(name+".cpython-312-") and path.endswith(".so")]
 check("single_CJK:"+name,len(candidates)==1)
 item=candidates[0];check("CJK_pin:"+name,pin(linuxread(item["path"]))=={k:item[k] for k in ("bytes","sha256")})
try:host("/usr/lib/python312.zip").lstat()
except FileNotFoundError:check("ZIP_lstat_absent_snapshot",True)
else:check("ZIP_lstat_absent_snapshot",False)
check("manifest_unchanged_end",pin(read(P/"MANIFESTO_PREPARACAO.json"))==pin(json.dumps(manifest).encode()) if False else sources[str(P/"MANIFESTO_PREPARACAO.json")]==pin((P/"MANIFESTO_PREPARACAO.json").read_bytes()))
data={"at_utc":datetime.now(timezone.utc).isoformat(),"status":"STATIC_METADATA_REVIEW_ONLY","checks":checks,"sources":sources,"dynamic_import_sites_independent":dynamic,"scope":{"candidate_imports":0,"WSL_processes_started":0,"solver_calls":0,"controls_executed":0,"AUTH_CLAIM_created":0,"all_old_runtime_files_rehashed":False}}
json_out("EVIDENCIA_REVISAO_ESTATICA.json",data)
print(json.dumps({"checks":len(checks),"passed":all(c["pass"] for c in checks),"sources":len(sources),"output":str(OUT/"EVIDENCIA_REVISAO_ESTATICA.json")}))
