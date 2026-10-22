"""I02 independent metadata/AST review; no imports or execution of candidates."""
from pathlib import Path
import ast,datetime,hashlib,json,os
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
PKG=ROOT/"f9_node_coupling_preparation"
OUT=ROOT/"proveniencia/revisao_f9_node_coupling"
checks=[];pins={}
def check(name,ok,detail=None):
 checks.append({"check":name,"passed":bool(ok),"detail":detail})
 if not ok: raise AssertionError(name)
def pin(path):
 p=Path(path);raw=p.read_bytes();r={"path":str(p),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()};pins[str(p)]=r;return r
def verify(rec,label):
 got=pin(rec["path"]);check(label,all(got[k]==rec[k] for k in got),got)
def emit(name,doc):
 p=OUT/name;raw=(json.dumps(doc,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8");assert not p.exists(),str(p)
 t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==raw;os.replace(t,p);assert p.read_bytes()==raw;return pin(p)
initial=json.loads((OUT/"SNAPSHOT_INICIAL.json").read_bytes())
for i,r in enumerate(initial["pins"]):verify(r,f"initial_unchanged_{i}")
m=json.loads((PKG/"MANIFESTO_PREPARACAO.json").read_bytes());c=json.loads((PKG/"CONTRATO_API.json").read_bytes());lin=json.loads((PKG/"SOURCE_LINEAGE.json").read_bytes())
check("request_identity",m["request_id"]==c["request_id"]==lin["request_id"]=="1fe78df6-efb2-4c57-93bd-499ad85d8b15")
for i,r in enumerate(m["members"]):verify(r,f"member_{i}")
for i,r in enumerate(m["immediate_byte_backups"]):verify(r,f"backup_{i}")
for name,r in c["source_pins"].items():verify(r,"source_"+name)
verify(lin["request"],"original_request");verify(lin["metadata_process"]["executable"],"metadata_runtime")
check("lineage_sources_match",lin["sources"]==c["source_pins"])
check("eight_members",len(m["members"])==8)
check("sixteen_sources",len(c["source_pins"])==16)
trees={}
for name in ("node_adapter.py","durable_nodes.py","prepare_static.py"):
 raw=(PKG/name).read_bytes();tree=ast.parse(raw,filename=str(PKG/name));trees[name]=tree
 check("ast_"+name,True,{"nodes":len(list(ast.walk(tree)))})
 imports=sorted({a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}|{n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module})
 check("stdlib_imports_"+name,set(imports)<={"math","base64","datetime","hashlib","json","os","pathlib","uuid","ast","sys"},imports)
a=(PKG/"node_adapter.py").read_text(encoding="utf-8");d=(PKG/"durable_nodes.py").read_text(encoding="utf-8")
sp=next(ast.literal_eval(n.value) for n in trees["node_adapter.py"].body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="SOURCE_PINS" for t in n.targets))
check("literal_source_pins_from_AST",sp==c["source_pins"])
for name in ("assemble_five","integrate_at_fixed_theta","profile_at_fixed_theta"):
 count=sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr==name for n in ast.walk(trees["node_adapter.py"]))
 check("one_callsite_"+name,count==1,count)
check("no_theta_run",not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="run" for n in ast.walk(trees["node_adapter.py"])))
check("exact_theta_hash_reused","self.t.canonical_conditional_sha256(conditional)" in a)
check("descriptor_reconstructed","expected = self._validator()._descriptor(key)" in a and "key == (*nums, n)" in a)
check("actual_assembly_before_precision",a.index("assembly_sha = c._sha(assembly_raw)")<a.index("precision_raw = c._canonical"))
check("profile_separate", "artifacts['profile_json']" in a and "return envelope, artifacts" in a)
check("single_supplier_callsite",sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="self" and n.func.attr=="supplier" for n in ast.walk(trees["durable_nodes.py"]))==1)
check("guard_call_order",d.index("self._guard('NODE_ACCESS'")<d.index("node = store.acquire")<d.index("bg = store.acquire")<d.index("self._guard('BACKGROUND_EXECUTION'")<d.index("payload = self.supplier(request)")<d.index("self._guard('BACKGROUND_ACCEPTANCE'")<d.index("store.commit(bg, payload)")<d.index("ctx.compute(")<d.index("store.commit(node, artifacts)"))
check("exclusive_claim_before_return","self._exclusive_write(claim_path, raw)" in d and "os.O_EXCL | os.O_NOFOLLOW" in d)
check("fsync_and_no_overwrite_link","os.fsync(fd)" in d and "os.link(temporary, destination, follow_symlinks=False)" in d)
check("no_replace_or_unlink",not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in {"replace","unlink","remove","rmdir"} for n in ast.walk(trees["durable_nodes.py"])))
check("platform_refusal","os.name != 'posix'" in d)
check("cache_files_validated","ctx.c._keys(node['payload'], expected_files" in d and "ctx.validate(envelope" in d)
check("cache_usage_zero","envelope['receipt']['background_calls_this_callback'] = 0" in d)
check("guard_no_boolean","if self.guard(phase, payload) is not None:" in d)
check("no_subprocess_or_network_imports",not any(isinstance(n,ast.Import) and any(x.name in {"subprocess","socket","requests"} for x in n.names) for t in trees.values() for n in ast.walk(t)))
check("no_self_manifest_member",str(PKG/"MANIFESTO_PREPARACAO.json") not in [r["path"] for r in m["members"]])
check("exact_envelope_contract",c["callback_envelope_exact_keys"]==["conditional_result","receipt"])
check("supplier_contract",c["supplier_result_exact_keys"]==["packet_json","result_json","receipt_json"] and c["supplier_calls_per_owned_background_claim_maximum"]==1)
for name in ("AUTH.json","CLAIM.json","ROOT_DECISION.json","RUN_CLAIM.json","RUN","__pycache__"):
 check("not_present_"+name,not (PKG/name).exists())
manifest_pin=pin(PKG/"MANIFESTO_PREPARACAO.json")
for r in initial["pins"]:check("final_initial_stable_"+Path(r["path"]).name,pin(r["path"])==r)
evidence={"schema":"I02_INDEPENDENT_STATIC_REVIEW_V1","request_id":m["request_id"],"reviewer":"chatgpt-codex/ordem-018/proveniencia","at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"map_before":610,"source_manifest_initial_final":manifest_pin,"status":"STATIC_ACCEPTANCE_WITH_TRUSTED_BOUNDARIES_NO_RUNTIME_QUALIFICATION","checks_count":len(checks),"checks":checks,"pins":list(pins.values()),"material_blockers":[],"nonblocking_observation":"Compatibility joint prediction_admission vs theta assembly_admission is enforced at evaluate_five, after possible background consumption. Contract already assigns context checks to external NODE_ACCESS; concrete precheck is a recommendation, not an implemented guard or new permission.","candidate_imports":0,"candidate_executions":0,"scientific_or_numeric_controls":0,"store_instances":0,"AUTH_created":False,"CLAIM_created":False,"observed_reads":0,"WSL":0,"remote":0,"scope":"Only byte/hash/AST/metadata and manual source review. No tests of candidate semantics executed."}
emit("EVIDENCIA_ESTATICA_I02.json",evidence)
members=[pin(OUT/name) for name in ["SNAPSHOT_INICIAL.json","MAPA_ANTES.json","verificar_metadados_i02.py","PARECER_I02.md","EVIDENCIA_ESTATICA_I02.json"]]
review=emit("MANIFESTO_REVISAO_I02.json",{"schema":"I02_INDEPENDENT_REVIEW_MANIFEST_V1","request_id":m["request_id"],"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_manifest":manifest_pin,"status":"STATIC_REVIEW_ONLY_NO_AUTHORIZATION","checks_count":len(checks),"members":members,"map_after":"MAPA_DEPOIS.json kept outside manifest to avoid self-reference"})
print(json.dumps({"checks_count":len(checks),"all_passed":all(x["passed"] for x in checks),"report":pin(OUT/"PARECER_I02.md"),"manifest":review,"source_manifest":manifest_pin},ensure_ascii=False))
