"""Byte-only v389 bundle preparation/verification. Never import a FINAL or runner."""
from pathlib import Path, PurePosixPath
import ast, base64, io, json, os, sys, zipfile, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_custody_layer import ROOT, OLD, STAGE, LAYER, META388, META389, pin, put, save
CENTRAL = ROOT.parent.parent.parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

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
    installed = json.loads((OLD / "RECIBO_INSTALACAO_V388.json").read_bytes())
    if installed["status"] != "INSTALLED_ALL_1267_BYTES_VERIFIED":
        raise RuntimeError("Expected installed v388 receipt")
    if (ROOT / "RECIBO_PREPARACAO_BUNDLES.json").exists():
        raise RuntimeError("Already prepared")
    union, devices = {}, []
    for dev in installed["device_matrix"]:
        final, manifest = Path(dev["FINAL"]["path"]), Path(dev["manifest"]["path"])
        for path, expected in [(final, dev["FINAL"]), (manifest, dev["manifest"])]:
            pp = pin(path)
            if (pp["bytes"],pp["sha256"]) != (expected["bytes"],expected["sha256"]):
                raise RuntimeError("Production v388 drift; do not overlay")
        values, declared, members = inspect_bundle(final, manifest)
        if members[LAYER] != (OLD / "stage" / LAYER).read_bytes():
            raise RuntimeError("Installed v388 layer differs")
        for rel, raw in members.items():
            if rel in union and union[rel] != raw:
                raise RuntimeError("Conflicting shared member")
            union[rel] = raw
        runner = CENTRAL / values["RUNNER_REL"]
        if runner.read_bytes() != members[values["RUNNER_REL"]]:
            raise RuntimeError("Runner source drift")
        devices.append({"device_directory":dev["device"],"FINAL":pin(final),"manifest":pin(manifest),
                        "runner":pin(runner),"runner_rel":values["RUNNER_REL"],"patent_id":values["PATENT_ID"],"slug":values["SLUG"]})
    if len(devices) != 16:
        raise RuntimeError("Expected exact 16 devices")
    for rel, raw in sorted(union.items()):
        if rel not in (LAYER, META388):
            put(STAGE / rel, raw)
    official = OLD / "reference_tools/build_final_code.py"
    put(ROOT / "reference_tools/build_final_code.py", official.read_bytes())
    put(STAGE / "tools/build_final_code.py", official.read_bytes())
    save("RECIBO_PREPARACAO_BUNDLES.json",{
        "stage_id":json.loads((ROOT/"IDENTIDADE_ESTAGIO.json").read_bytes())["stage_id"],
        "devices":devices,"unique_existing_members":len(union),
        "existing_dependencies_opaque":True,"no_new_legal_or_private_archive":True,
        "official_packager":pin(STAGE/"tools/build_final_code.py"),
        "device_or_science_execution":False,"source_install_receipt":pin(OLD/"RECIBO_INSTALACAO_V388.json")})
    print(json.dumps({"devices":16,"unique_members":len(union),"packager":pin(STAGE/"tools/build_final_code.py")}))

def verify():
    prep=json.loads((ROOT/"RECIBO_PREPARACAO_BUNDLES.json").read_bytes())
    rows=[];mapping=[]
    for dev in prep["devices"]:
        of,om=Path(dev["FINAL"]["path"]),Path(dev["manifest"]["path"])
        for f,e in [(of,dev["FINAL"]),(om,dev["manifest"]),(Path(dev["runner"]["path"]),dev["runner"])]:
            pp=pin(f)
            if pp["sha256"]!=e["sha256"] or pp["bytes"]!=e["bytes"]:raise RuntimeError("Live baseline drift")
        ov,od,old=inspect_bundle(of,om)
        nm=STAGE/"patents"/dev["device_directory"]/om.name
        nf=nm.with_name(nm.name.replace(".manifest.json",".py"))
        nv,nd,new=inspect_bundle(nf,nm)
        if set(new)!=set(old)|{META389}:raise RuntimeError("Unexpected new members")
        changed=sorted(x for x in old if old[x]!=new[x])
        if changed!=sorted([LAYER,META388]):raise RuntimeError("Unexpected changed members")
        for name,raw in new.items():
            if raw!=(STAGE/name).read_bytes():raise RuntimeError("Stage member differs")
        for k in ["PATENT_ID","SLUG","RUNNER_REL"]:
            if ov[k]!=nv[k]:raise RuntimeError("Identity changed")
        if new[nv["RUNNER_REL"]]!=Path(dev["runner"]["path"]).read_bytes():raise RuntimeError("Runner changed")
        # Official packager reports LF length before Windows newline translation.
        before=pin(nm);raw=nm.read_bytes();backup=nm.with_name(nm.name+".bak_packager_bytes")
        put(backup,raw)
        pp=pin(nf);nd["final_bytes"]=pp["bytes"];nd["final_sha256"]=pp["sha256"]
        revised=(json.dumps(nd,ensure_ascii=False,indent=1)+"\n").encode()
        tmp=nm.with_name(nm.name+".tmp_reconciled")
        put(tmp,revised)
        if nm.read_bytes()!=raw:raise RuntimeError("Stage manifest changed before CAS")
        os.replace(tmp,nm)
        if nm.read_bytes()!=revised:raise RuntimeError("Manifest readback differs")
        inspect_bundle(nf,nm)
        rows.append({"device":dev["device_directory"],"FINAL":pin(nf),"manifest":pin(nm),
                     "original_manifest_before_byte_reconciliation":before,
                     "manifest_backup":pin(backup),"member_count":len(new),
                     "changed_members":changed,"added_members":[META389],
                     "unchanged_members":len(old)-2,"runner_preserved":True,
                     "all_pins_checked":True,"device_executed":False})
        for f in [nf,nm]:
            live=CENTRAL/f.relative_to(STAGE)
            mapping.append({"staged":pin(f),"live_destination":str(live),"current":pin(live),
                            "policy":"BACKUP_EXACT_BYTES_THEN_VERIFY_TEMP_AND_ATOMIC_REPLACE"})
    save("RECIBO_BUNDLES_V389.json",{"stage_id":prep["stage_id"],"status":"16_STATIC_BUNDLES_VERIFIED_NOT_EXECUTED",
         "devices":rows,"device_count":len(rows),"official_packager":prep["official_packager"],
         "limit":"Bundles depend on the separately installed Central custody; not an embedded full cofre.",
         "scientific_or_device_execution":False,"installed":False})
    save("PLANO_INSTALACAO_FINALS.json",{"stage_id":prep["stage_id"],"status":"PROPOSAL_ONLY","mapping":mapping})
    print(json.dumps({"verified":len(rows),"report":pin(ROOT/"RECIBO_BUNDLES_V389.json")}))

if __name__=="__main__":
    {"prepare":prepare,"verify":verify}[sys.argv[1]]()
