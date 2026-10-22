"""Build candidate channel custody and modules; never modify Bancada originals."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

UNIT = Path(__file__).resolve().parents[1]
STAGE = UNIT / "candidate"
OUT = Path(__file__).resolve().parent
ORDER = UNIT.parent
BENCH = Path(r"C:\IALD\Bancada_Um")
AUDIT = json.loads((ORDER / "F0.3.B1/channels_inventory/CHANNEL_AUDIT_R1.json").read_bytes())
if (OUT / "BUILD_CHANNELS_RECEIPT_R1.json").exists():
    raise FileExistsError("build receipt exists; do not overwrite")
copies = []

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pinned(path, expected):
    raw = Path(path).read_bytes()
    if sha(raw) != expected:
        raise ValueError("source changed: " + str(path))
    return raw

def new(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
    if path.read_bytes() != raw:
        raise OSError("written bytes differ")
    return {"path":str(path),"sha256":sha(raw),"bytes":len(raw)}

def copy_source(path, raw, group):
    dest = STAGE / "fontes_externas" / group / Path(path).name
    record = new(dest, raw)
    copies.append({"source":str(path), **record})
    return {"relative_path":dest.relative_to(STAGE).as_posix(),"sha256":record["sha256"],
            "bytes":record["bytes"],"origin":str(path)}

def json_bytes(value):
    return (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8")

def replace_candidate(path, raw):
    if path.exists():
        backup = path.with_name(path.name + ".baseline")
        if not backup.exists():
            new(backup,path.read_bytes())
    temporary = path.with_name(path.name + ".tmp_channels_r1")
    new(temporary, raw)
    temporary.replace(path)

# Reuse the already audited F5.2 R3 pinned pages and unchanged frozen source.
frozen_info = AUDIT["files"]["neff_frozen"]
neff_sources = {"frozen":copy_source(frozen_info["path"],pinned(frozen_info["path"],frozen_info["sha256"]),"F5.2")}
r3_path = ORDER / "F5.2/CANDIDATO_R3_20261008/neff_canal.py"
r3_raw = pinned(r3_path, AUDIT["files"]["neff_candidate_r3"]["sha256"])
for node in ast.parse(r3_raw.decode("utf-8-sig")).body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id == "PAGES" for t in node.targets):
        for key,value in zip(node.value.keys,node.value.values,strict=True):
            version = ast.literal_eval(key)
            path = ast.literal_eval(value.elts[0].args[0])
            expected = ast.literal_eval(value.elts[1])
            neff_sources["table5_"+version] = copy_source(path,pinned(path,expected),"F5.2")
if set(neff_sources) != {"frozen","table5_v1","table5_v2"}:
    raise ValueError("F5.2 source extraction incomplete")
neff_manifest = {"schema":"iald.f5_2.channel_sources.v1","unit":"F0.3.B2","sources":neff_sources,
                 "reused_candidate_sha256":sha(r3_raw),"source_admission":"D8_PENDING","yp_selection":"X16_OPEN",
                 "obsolete_frozen_row":"Preserved only as historical source bytes; never emitted as CMB-SPA",
                 "calendar_policy":"No historical calendar emitted; no operational forecast"}
neff_raw = json_bytes(neff_manifest)
new(STAGE/"bancada/neff_fontes_f52.json",neff_raw)
neff_path = STAGE/"bancada/neff_canal.py"
neff_code = neff_path.read_text(encoding="utf-8")
if neff_code.count("__NEFF_MANIFEST_PIN__") != 1:
    raise ValueError("N_eff source is not the expected unpinned template")
replace_candidate(neff_path,neff_code.replace("__NEFF_MANIFEST_PIN__",sha(neff_raw)).encode("utf-8"))

# R8 is inert approved custody, copied verbatim into staging only.
r8_entries = {Path(x["path"]).name:x for x in AUDIT["copied_r8_sources"]}
local_entries = {}
for name,item in r8_entries.items():
    if name == "v369_um_absoluto.json":
        continue
    local_entries[name] = copy_source(item["path"],pinned(item["path"],item["sha256"]),"F7.2")
old_info = AUDIT["files"]["manifest_v2"]
old_raw = pinned(old_info["path"],old_info["sha256"])
old = json.loads(old_raw)
clock_entry = old["documents"]["clock_v369_result"]
clock_raw = pinned(clock_entry["path"],clock_entry["sha256"])
requirement = json.loads(clock_raw)["core"]["clock_test_result_v369"]["five_sigma_requirement"]
snapshot = {"schema":"iald.historical_projection.v369.v1","source_json_sha256":sha(clock_raw),
            "source_json_bytes":len(clock_raw),"source_json_path":clock_entry["path"],
            "extraction_path":"core.clock_test_result_v369.five_sigma_requirement", "requirement":requirement,
            "scope":"HISTORICAL_V369_CONDITIONAL_PROJECTION_NOT_CURRENT_OBSERVATION"}
snapshot_path = STAGE / "fontes_externas/F7.2/historical_clock_v369.json"
snapshot_raw = json_bytes(snapshot)
new(snapshot_path,snapshot_raw)
clock_local = {"relative_path":snapshot_path.relative_to(STAGE).as_posix(),"sha256":sha(snapshot_raw),"bytes":len(snapshot_raw),
               "origin":clock_entry["path"],"historical_source_sha256":sha(clock_raw)}
manifest = {"schema":"iald.f7_2.channel_sources.v4","unit":"F7.2","candidate_unit":"F0.3.B2",
            "primary_article_pdfs_custodied":True,"raw_experimental_data_custodied":False,
            "scripts":[],"documents":{},"primary_pdfs":[],"context_sources":[],
            "clock_v369_projection":old["clock_v369_projection"],"historical_source_sha256":sha(clock_raw),
            "rejected_publisher_html":old["rejected_publisher_html"],
            "corrective_manifest":{
                "custody_only_not_runtime_claim":True,"R8_copy":"RATIFIED_C1_EVENT_313",
                "JUNO_Eq6_anchor":"Section III.B; the published bound is Eq.13 and Table I",
                "TABELA_V3_header":"V3 historical table; the V2 wording in its pinned header is superseded by this manifest",
                "LITERATURA_authorship":"Where the pinned historical text says mensagem do operador, read mensagem da gerencia c1",
                "source_stage":"SELF_CONTAINED_RELATIVE_CUSTODY_CANDIDATE_NOT_DEPLOYMENT_RECEIPT"}}
for item in old["scripts"]:
    manifest["scripts"].append({"name":item["name"],**local_entries[item["name"]]})
for key,item in old["documents"].items():
    name = Path(item["path"]).name
    if key == "clock_v369_result":
        manifest["documents"][key] = clock_local
    else:
        if key == "channel_power_table":
            name = "TABELA_DE_PODER_POR_CANAL_V3.md"
        manifest["documents"][key] = local_entries[name]
for item in old["primary_pdfs"]:
    manifest["primary_pdfs"].append({k:v for k,v in item.items() if k not in {"path","sha256","bytes"}} | local_entries[item["name"]])
for name in ("Ternes_Pagliaroli_Villante_2025_arxiv_2503.04573v1.pdf","LITERATURA_POS_JUNHO_F7_2_20261008.md"):
    manifest["context_sources"].append(local_entries[name])
manifest_raw = json_bytes(manifest)
new(STAGE/"bancada/neutrino_fontes_f72_b2.json",manifest_raw)

loader = '''"""Self-contained F7.2 source inventory. No events, likelihood, fit or TGL limit.

This candidate consumes immutable relative R8 custody plus a provenance-pinned
historical v369 projection. Published model limits are not transferred to TGL.
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
from pathlib import Path
import re
from .canonical import require_current
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name("neutrino_fontes_f72_b2.json")
MANIFEST_SHA256 = "__PIN__"
JUNO_NAME = "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"
REJECTED_HTML = frozenset({"Kovachy_2015_Nature_abstract.html","Fein_2019_NaturePhysics_abstract.html"})
class FonteRecusada(ValueError):
    """A source identity or structural check failed."""
def _source(entry, *, python_source=False, pdf=False):
    if not isinstance(entry,dict):
        raise FonteRecusada("source entry is not an object")
    relative,pin,size = (entry.get(k) for k in ("relative_path","sha256","bytes"))
    if (not isinstance(relative,str) or not isinstance(pin,str) or not re.fullmatch(r"[0-9a-f]{64}",pin,re.ASCII)
            or type(size) is not int or size <= 0):
        raise FonteRecusada("source path/pin/size invalid")
    path = (ROOT/relative).resolve()
    if not path.is_relative_to((ROOT/"fontes_externas/F7.2").resolve()):
        raise FonteRecusada("source path escapes custody")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FonteRecusada(f"source unavailable: {path.name}") from exc
    if hashlib.sha256(raw).hexdigest() != pin or len(raw) != size:
        raise FonteRecusada(f"source hash/size differs: {path.name}")
    if pdf and (len(raw)<1000 or not raw.startswith(b"%PDF-")):
        raise FonteRecusada("invalid substantive PDF bytes")
    if python_source:
        try:
            ast.parse(raw.decode("utf-8-sig"))
        except (UnicodeError,SyntaxError) as exc:
            raise FonteRecusada("script is not parseable source") from exc
    return raw,{"path":str(path),"sha256":pin,"bytes":size,"origin":entry.get("origin"),
                "ast_parsed":python_source,"pdf_header_valid":pdf}
def _load_sources(manifest_path=MANIFEST):
    try:
        raw = Path(manifest_path).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=MANIFEST_SHA256:
            raise FonteRecusada("manifest hash differs")
        manifest=json.loads(raw)
        if (manifest["schema"]!="iald.f7_2.channel_sources.v4" or manifest["unit"]!="F7.2"
                or manifest["primary_article_pdfs_custodied"] is not True or manifest["raw_experimental_data_custodied"] is not False):
            raise FonteRecusada("manifest identity/custody differs")
        scripts,docs,pdfs,doc_raw={},{},{},{}
        for entry in manifest["scripts"]:
            name=entry["name"]
            if name in scripts:
                raise FonteRecusada("duplicate script")
            _,scripts[name]=_source(entry,python_source=True)
        for name,entry in manifest["documents"].items():
            doc_raw[name],docs[name]=_source(entry)
        for entry in manifest["primary_pdfs"]:
            name=entry["name"]
            if name in pdfs:
                raise FonteRecusada("duplicate PDF")
            _,source=_source(entry,pdf=True)
            pdfs[name]={**source,"name":name,"channel":entry["channel"],"url":entry["url"],"matter_validation":entry["validated_matter"]}
        for entry in manifest["context_sources"]:
            _source(entry,pdf=entry["relative_path"].lower().endswith(".pdf"))
        snapshot=json.loads(doc_raw["clock_v369_result"])
        if (snapshot["schema"]!="iald.historical_projection.v369.v1"
                or snapshot["source_json_sha256"]!=manifest["historical_source_sha256"]
                or snapshot["extraction_path"]!="core.clock_test_result_v369.five_sigma_requirement"):
            raise FonteRecusada("historical clock provenance differs")
        projection=manifest["clock_v369_projection"]
        required=snapshot["requirement"]
        for key in ("ghz_N_needed","hbar_omega_needed_eV_at_todays_sigma"):
            value=required[key]
            if type(value) not in (int,float) or not math.isfinite(value) or value<=0 or value!=projection[key]:
                raise FonteRecusada("clock projection values differ")
        if (required["platform"]!="sr87_kim2025" or projection["platform"]!=required["platform"]
                or projection["kind"]!="CONDITIONAL_5SIGMA_PROJECTION"):
            raise FonteRecusada("clock projection kind/platform differs")
        return scripts,docs,pdfs,projection,MANIFEST_SHA256
    except FonteRecusada:
        raise
    except (OSError,UnicodeError,json.JSONDecodeError,KeyError,TypeError,ValueError) as exc:
        raise FonteRecusada("manifest/source structure unreadable") from exc

'''
old_code_info = AUDIT["files"]["neutrino_v2"]
old_code = pinned(old_code_info["path"],old_code_info["sha256"]).decode("utf-8")
body = old_code[old_code.index("def canal("):]
body = body.replace('    scripts, docs, pdfs, clock_projection, manifest_hash = _load_sources(Path(manifest_path))',
                    '    current = require_current("neutrino_canal_f72_v2", root=ROOT)\n    scripts, docs, pdfs, clock_projection, manifest_hash = _load_sources(Path(manifest_path))')
body = body.replace('"Sec. IV.B; Eq. (6), Eq. (13), Table I"','"Sec. III.B; Eq. (6); Eq. (13), Table I"')
body = body.replace('"READ_ONLY_SOURCE_PROVENANCE_V2"','"READ_ONLY_SOURCE_PROVENANCE_B2"')
body = body.replace('"manifest_sha256": manifest_hash,','"manifest_sha256": manifest_hash, "current_contract": current,\n        "served_contract": "F7_2_B2_SELF_CONTAINED", "requested_endpoint": "neutrino_canal_f72_v2",\n        "likelihood_available": False, "detector_response_available": False, "tgl_operator_mapping": "OPEN",')
new_code=(loader.replace("__PIN__",sha(manifest_raw))+body).encode("utf-8")
ast.parse(new_code.decode("utf-8"))
replace_candidate(STAGE/"bancada/neutrino_canal_v2.py",new_code)
alias='''"""Legacy endpoint alias to the corrected self-contained F7.2 inventory.

The old implementation survives in baseline custody, not as a competing live
table. The served contract and requested endpoint are explicit in the result.
"""
from .neutrino_canal_v2 import FonteRecusada, MANIFEST, canal as _current

def canal(manifest_path=MANIFEST):
    result = _current(manifest_path=manifest_path)
    return {**result, "requested_endpoint":"neutrino_canal_f72", "legacy_alias":True}
'''
replace_candidate(STAGE/"bancada/neutrino_canal.py",alias.encode("utf-8"))
outputs=[]
for name in ("neff_canal.py","neff_fontes_f52.json","neutrino_canal.py","neutrino_canal_v2.py","neutrino_fontes_f72_b2.json"):
    path=STAGE/"bancada"/name
    raw=path.read_bytes()
    outputs.append({"path":str(path),"sha256":sha(raw),"bytes":len(raw)})
receipt={"unit":"F0.3.B2","claim_event":632,"utc":datetime.now(timezone.utc).isoformat(),"copies":copies,
         "outputs":outputs,"historical_clock_snapshot":str(snapshot_path),"bancada_modified":False,
         "mode":"STAGING_ONLY","scientific_fit_run":False,"canonical_api":"require_current/read_alpha from root versioner"}
info=new(OUT/"BUILD_CHANNELS_RECEIPT_R1.json",json_bytes(receipt))
print(json.dumps({"receipt":info,"copied_files":len(copies),"outputs":outputs},ensure_ascii=False,indent=2))
