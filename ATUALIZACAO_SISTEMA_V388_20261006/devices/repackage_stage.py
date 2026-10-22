"""Local packaging only. Never import or execute a device or scientific module."""
from pathlib import Path, PurePosixPath
import ast, base64, hashlib, io, json, os, sys, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parents[2]
STAGE = ROOT / "stage"
LAYER = "patents/_formula_completa/tgl_formula_completa.py"
META = "patents/_formula_completa/ADENDO_V388_METADATA.json"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(path):
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": sha(b)}

def put(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == raw:
            return
        raise RuntimeError("Refusing overwrite: " + str(path))
    temp = path.with_name(path.name + ".tmp_new")
    if temp.exists():
        raise RuntimeError("Unexpected temporary file")
    temp.write_bytes(raw)
    if temp.read_bytes() != raw:
        raise RuntimeError("Temporary bytes differ")
    os.replace(temp, path)

def save(name, obj):
    put(ROOT / name, (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode())

def literals(path):
    tree = ast.parse(path.read_bytes(), filename=str(path))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"PATENT_ID","SLUG","RUNNER_REL","COMBINED_SHA256","MANIFEST","_B64"}:
                    values[target.id] = ast.literal_eval(node.value)
    if len(values) != 6:
        raise RuntimeError("Incomplete final header")
    return values

def inspect_bundle(final, manifest):
    values = literals(final)
    declared = json.loads(manifest.read_bytes())
    if values["MANIFEST"] != declared["files"]:
        raise RuntimeError("Python/JSON manifest disagreement")
    payload = base64.b64decode(values["_B64"], validate=True)
    if sha(payload) != values["COMBINED_SHA256"] or sha(payload) != declared["combined_sha256"]:
        raise RuntimeError("Combined hash mismatch")
    members = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        names = z.namelist()
        expected = [e["path"] for e in declared["files"]]
        if len(names) != len(set(names)) or set(names) != set(expected) or len(expected) != len(set(expected)):
            raise RuntimeError("Missing, extra or duplicate ZIP entries")
        for e in declared["files"]:
            rel = PurePosixPath(e["path"])
            if rel.is_absolute() or ".." in rel.parts or "\\" in str(rel) or ":" in str(rel):
                raise RuntimeError("Unsafe member path")
            if rel.parts[0] not in ("patents", "Patentes"):
                raise RuntimeError("Outside admitted engineering layout")
            if any(x in str(rel).lower() for x in ("iald_stack_v7", "iald_psion_state", ".env", "token_huggin")):
                raise RuntimeError("Confidential member")
            raw = z.read(str(rel))
            if len(raw) != e["bytes"] or sha(raw) != e["sha256"]:
                raise RuntimeError("Member pin mismatch")
            members[str(rel)] = raw
    return values, declared, members

def prepare():
    inv = json.loads((ROOT / "INVENTARIO_DISPOSITIVOS.json").read_bytes())
    if (ROOT / "RECIBO_PREPARACAO_BUNDLES.json").exists():
        raise RuntimeError("Preparation already persisted; no replay")
    union = {}
    inventory = []
    for dev in inv["devices"]:
        m = Path(dev["bundle_manifest"]["path"])
        if pin(m)["sha256"] != dev["bundle_manifest"]["sha256"]:
            raise RuntimeError("Original manifest drift")
        final = m.with_name(m.name.replace(".manifest.json", ".py"))
        v, declared, members = inspect_bundle(final, m)
        runner = Path(dev["runner"]["path"])
        if members[v["RUNNER_REL"]] != runner.read_bytes():
            raise RuntimeError("Bundle runner differs from current source")
        if members[LAYER] != (ROOT / "baseline/tgl_formula_completa.py").read_bytes():
            raise RuntimeError("Original layer pin mismatch")
        for rel, raw in members.items():
            if rel in union and union[rel] != raw:
                raise RuntimeError("Conflicting shared member")
            union[rel] = raw
        inventory.append({"device_directory":dev["device_directory"],"original_final":pin(final),
                          "original_manifest":pin(m),"members":len(members),"combined_sha256":v["COMBINED_SHA256"],
                          "runner_current_equal":True,"runtime_called":False})
    for rel, raw in sorted(union.items()):
        if rel != LAYER:
            put(STAGE / rel, raw)
    official = ROOT / "reference_tools/build_final_code.py"
    put(STAGE / "tools/build_final_code.py", official.read_bytes())
    save("RECIBO_PREPARACAO_BUNDLES.json",{
        "stage_id":inv["stage_id"],"status":"PACKAGING_INPUTS_PREPARED",
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "devices":inventory,"unique_legacy_dependencies":len(union),
        "unique_legacy_bytes":sum(map(len,union.values())),"opaque_existing_metadata_preserved":True,
        "dependencies_materialized":len(union)-1,
        "official_packager":pin(STAGE/"tools/build_final_code.py"),
        "packager_unmodified":True,"new_layer":pin(STAGE/LAYER),"new_metadata":pin(STAGE/META),
        "scientific_execution":False,"candidate_imports":False,"device_execution":False,
        "other_archive_access":False,"note":"Existing bundle members preserved as opaque bytes; no body interpretation or new legal archive."})
    print("Prepared 16 bundles; legacy unique dependencies:",len(union))

def verify():
    inv=json.loads((ROOT/"INVENTARIO_DISPOSITIVOS.json").read_bytes())
    preparation=json.loads((ROOT/"RECIBO_PREPARACAO_BUNDLES.json").read_bytes())
    reports=[]; mapping=[]
    metadata=json.loads((STAGE/META).read_bytes())
    cofre=STAGE/"vault/originals_copy/um_unificado_v388"
    kernel=STAGE/"vault/originals_copy/tgl_kernel_v388"
    for e in metadata["custody_pins"]:
        p=(cofre if e["base"]=="um" else kernel)/e["relative"]
        if pin(p)["sha256"]!=e["sha256"] or pin(p)["bytes"]!=e["bytes"]:
            raise RuntimeError("Custody metadata mismatch")
    for dev in inv["devices"]:
        om=Path(dev["bundle_manifest"]["path"]); of=om.with_name(om.name.replace(".manifest.json",".py"))
        ov,od,old=inspect_bundle(of,om)
        nm=STAGE/"patents"/dev["device_directory"]/om.name
        nf=nm.with_name(nm.name.replace(".manifest.json",".py"))
        nv,nd,new=inspect_bundle(nf,nm)
        if set(new)!=set(old)|{META}:
            raise RuntimeError("Unexpected dependency-set change")
        changed=[r for r in old if old[r]!=new[r]]
        if changed!=[LAYER]:
            raise RuntimeError("Only shared layer may change: "+str(changed))
        for rel,raw in new.items():
            if raw!=(STAGE/rel).read_bytes():
                raise RuntimeError("Stage/bundle mismatch")
        if new[nv["RUNNER_REL"]]!=Path(dev["runner"]["path"]).read_bytes():
            raise RuntimeError("Runner changed")
        if (nv["RUNNER_REL"],nv["PATENT_ID"],nv["SLUG"])!=(ov["RUNNER_REL"],ov["PATENT_ID"],ov["SLUG"]):
            raise RuntimeError("Device identity changed")
        reports.append({"device_directory":dev["device_directory"],"final":pin(nf),"manifest":pin(nm),
                        "bundle_combined_sha256":nv["COMBINED_SHA256"],"n_files":len(new),
                        "all_member_pins_match":True,"all_stage_bytes_match":True,
                        "only_changed_member":LAYER,"only_added_member":META,
                        "runner_matches_live":True,"custody_pins_from_added_metadata_match":len(metadata["custody_pins"]),
                        "candidate_imported":False,"runner_executed":False,"scientific_verdict_recomputed":False})
        for p in (nf,nm):
            live=CENTRAL/p.relative_to(STAGE)
            mapping.append({"staged":pin(p),"live_destination":str(live),"current":pin(live),
                            "policy":"BACKUP_EXACT_BYTES_THEN_VERIFY_TEMP_AND_ATOMIC_REPLACE"})
    save("RECIBO_BUNDLES_V388.json",{"stage_id":inv["stage_id"],"status":"16_FINALS_REPACKAGED_STATIC_BYTE_VERIFICATION_ONLY",
         "created_utc":datetime.now(timezone.utc).isoformat(),"devices":reports,"device_count":len(reports),
         "sources":pin(ROOT/"RECIBO_PREPARACAO_BUNDLES.json"),"official_packager":preparation["official_packager"],
         "scientific_functions_called":0,"runners_executed":0,"candidates_imported":0,
         "installed":False,"public_release":False,"results_and_seals_changed":False,
         "limitation":"No runtime validation. Final bundles continue to rely on Central custody via the unchanged lookup interface; custody files are staged separately, not silently embedded."})
    save("PLANO_INSTALACAO_FINALS.json",{"stage_id":inv["stage_id"],"status":"REVIEWABLE_NOT_INSTALL_AUTHORIZATION","mapping":mapping})
    print(json.dumps({"verified_devices":len(reports),"final_receipt":pin(ROOT/"RECIBO_BUNDLES_V388.json"),"installation_plan":pin(ROOT/"PLANO_INSTALACAO_FINALS.json")},ensure_ascii=False))

if __name__=="__main__":
    if sys.argv[1:] == ["prepare"]: prepare()
    elif sys.argv[1:] == ["verify"]: verify()
    else: raise SystemExit("Expected prepare or verify; never runs devices")
