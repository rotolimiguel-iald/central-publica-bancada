"""Stage sealed v389 files and a documentary layer delta; no scientific imports."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast, json, hashlib, os, difflib

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent.parent / "ATUALIZACAO_SISTEMA_V388_20261006/devices"
N = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
STAGE = ROOT / "stage"
LAYER = "patents/_formula_completa/tgl_formula_completa.py"
META388 = "patents/_formula_completa/ADENDO_V388_METADATA.json"
META389 = "patents/_formula_completa/ADENDO_V389_METADATA.json"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}

def put(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == raw:
            return
        raise RuntimeError("Existing different stage file: " + str(path))
    tmp = path.with_name(path.name + ".tmp_new")
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.read_bytes() != raw:
        raise RuntimeError("Temporary bytes differ")
    os.rename(tmp, path)
    if path.read_bytes() != raw:
        raise RuntimeError("Final bytes differ")

def save(name, obj):
    put(ROOT / name, (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode())

def safe_rel(name):
    rel = PurePosixPath(name)
    if rel.is_absolute() or ".." in rel.parts or "\\" in name or ":" in name:
        raise RuntimeError("Unsafe source path")
    if any(x in name.lower() for x in ("iald_stack_v7", "iald_psion_state", ".env", "token_huggin", "password")):
        raise RuntimeError("Confidential path refused")
    return rel

def prepare():
    if (ROOT / "MANIFESTO_COFRE_ESTAGIO.json").exists():
        raise RuntimeError("Preparation already persisted; inspect instead of repeating")
    identity = json.loads((ROOT / "IDENTIDADE_ESTAGIO.json").read_bytes())
    seal_raw = (N / "um_absoluto_selo.json").read_bytes()
    seal = json.loads(seal_raw)
    if seal["um_version"] != "v389":
        raise RuntimeError("Exact v389 seal required")
    um = STAGE / "vault/originals_copy/um_unificado_v389"
    kernel = STAGE / "vault/originals_copy/tgl_kernel_v389"
    copies = []
    def copy(src, dst, kind, expected=None):
        raw = src.read_bytes()
        if expected is not None and digest(raw) != expected:
            raise RuntimeError("Sealed source pin differs: " + str(src))
        put(dst, raw)
        oldrel = dst.relative_to(STAGE).as_posix().replace("_v389/", "_v388/")
        oldf = OLD / "stage" / oldrel
        copies.append({"source":pin(src),"destination":pin(dst),
                       "stage_relative":dst.relative_to(ROOT).as_posix(),"kind":kind,
                       "byte_identical":True,
                       "comparison_v388": "SAME" if oldf.exists() and oldf.read_bytes()==raw else
                                          "CHANGED" if oldf.exists() else "NEW_NAME",
                       "previous_stage":str(oldf) if oldf.exists() else None})
    for name, expected in seal["sha256"].items():
        rel = safe_rel(name)
        copy(N / rel, um / rel, "SEALED_ARTIFACT_BYTES", expected)
    copy(N / "um_absoluto_selo.json", um / "um_absoluto_selo.json", "SEAL", digest(seal_raw))
    for name in ["HANDOFF_CUSTODIA_CONJUNTA_v383_v389.md", "rodada_v389_stdout.txt"]:
        copy(N / name, um / name, "DOCUMENTARY_HANDOFF_OR_RECORDED_STDOUT")
    proof_raw = (um / "tgl_kernel_proof_manifest.json").read_bytes()
    proof = json.loads(proof_raw)
    for name, expected in proof["formal_files_sha256"].items():
        rel = safe_rel(name)
        copy(N / "tgl_kernel" / rel, kernel / rel, "FORMAL_SOURCE_NOT_RECOMPILED", expected)
    copy(N / "tgl_kernel_proof_manifest.json", kernel / "tgl_kernel_proof_manifest.json",
         "FORMAL_MANIFEST", seal["sha256"]["tgl_kernel_proof_manifest.json"])
    exam_root = Path(r"C:\IALD\Central de Patentes\work\exame_v388").resolve()
    for row in seal["text_label_errata_v389"]["files"].values():
        src = Path(row["path"]).resolve()
        if src.parent != exam_root:
            raise RuntimeError("Unexpected exam document root")
        copy(src, um / "exame_v388" / src.name, "PINNED_ERRATA_DOCUMENT", row["sha256"])
    if (N / "um_absoluto_selo.json").read_bytes() != seal_raw:
        raise RuntimeError("Seal changed during staging")
    for item in copies:
        if pin(Path(item["source"]["path"])) != item["source"]:
            raise RuntimeError("Source changed during staging")
    save("MANIFESTO_COFRE_ESTAGIO.json",{
        "schema":"V389_INTERNAL_CUSTODY_STAGE_V1","stage_id":identity["stage_id"],
        "utc":datetime.now(timezone.utc).isoformat(),"status":"STAGED_NOT_INSTALLED",
        "source_seal":pin(N/"um_absoluto_selo.json"),"copied_count":len(copies),"copies":copies,
        "formal_files":len(proof["formal_files_sha256"]),
        "formal_lean_files":sum(x.endswith(".lean") for x in proof["formal_files_sha256"]),
        "comparison_counts":{k:sum(x["comparison_v388"]==k for x in copies) for k in ["SAME","CHANGED","NEW_NAME"]},
        "um_Lean_devices_science_executed":False,
        "scope":"Same seal/formal source custody as v388 plus three pinned examination/erratum documents; not full public custody or runtime cache."})
    oldlayer = (OLD / "stage" / LAYER).read_bytes()
    put(ROOT / "baseline/tgl_formula_completa.py", oldlayer)
    oldmeta = json.loads((OLD / "stage" / META388).read_bytes())
    newmeta = json.loads(json.dumps(oldmeta))
    newmeta["custody_version"] = "v389"
    newmeta["concept_version"] = "v388"
    newmeta["source_um_sha256"] = seal["sha256"]["um.py"]
    newmeta["status"] = "STAGED_DOCUMENTARY_UPDATE_NOT_INSTALLED"
    for row in newmeta["custody_pins"]:
        p = (um if row["base"]=="um" else kernel) / row["relative"]
        pp = pin(p); row.update(bytes=pp["bytes"], sha256=pp["sha256"])
    core = json.loads((um / "um_absoluto.json").read_bytes())["core"]
    priorcore = json.loads((OLD / "stage/vault/originals_copy/um_unificado_v388/um_absoluto.json").read_bytes())["core"]
    changes = [k for k in sorted(set(core)|set(priorcore)) if core.get(k)!=priorcore.get(k)]
    err = seal["text_label_errata_v389"]
    meta389 = {
        "schema":"DEVICE_LAYER_V389_TEXT_LABEL_ADDENDUM_V1","status":"STAGED_NOT_INSTALLED",
        "custody_version":"v389","conceptual_beta_API":"v388_unchanged","source_um_sha256":seal["sha256"]["um.py"],
        "custody_pins":newmeta["custody_pins"],
        "source_core_key":"text_label_errata_v389",
        "source_verdict":err["verdict"],"source_reported_all_verified":err["all_verified"],
        "seal_label":err["seal"],
        "ledger_reported":err["ledger"],
        "text_sites_reported_ok":err["text_sites_ok"],
        "statute":"DECLARADO in sealed source; byte custody verified here, no recomputation",
        "no_calculation_changed_claim":"SOURCE_DECLARED; scientific audit is independent",
        "beta0_unchanged":True,"mu_per_device":"OPEN","physical_verdict_allowed":False,
        "new_scientific_or_device_run":False}
    put(STAGE/META388,(json.dumps(newmeta,ensure_ascii=False,indent=2)+"\n").encode())
    put(STAGE/META389,(json.dumps(meta389,ensure_ascii=False,indent=2)+"\n").encode())
    layer=oldlayer.decode("utf-8")
    tree=ast.parse(layer)
    constant=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="V388_METADATA_SHA256" for t in x.targets))
    layer=layer.replace(ast.get_source_segment(layer,constant),'V388_METADATA_SHA256 = "'+pin(STAGE/META388)["sha256"]+'"')
    layer=layer.replace('version != 388 or cf.get("cofre") != "um_unificado_v388"',
                        'version != 389 or cf.get("cofre") != "um_unificado_v389"')
    layer=layer.replace('v388 additive package requires its exact reviewed custody version',
                        'v388 concept addendum requires exact reviewed v389 custody')
    layer=layer.replace('"version": "v388",','"version": "v388",\n        "custody_version": "v389",')
    addition = '\n\nV389_METADATA_SHA256 = "'+pin(STAGE/META389)["sha256"]+'"\n\n'+'''def _adendo_v389_no_cofre(cf):
    """Pinned text/label errata only; no new calculation or device verdict."""
    meta_path = Path(__file__).with_name("ADENDO_V389_METADATA.json")
    if _sha(meta_path) != V389_METADATA_SHA256:
        raise RuntimeError("v389 metadata pin mismatch")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    version, cofre, kernel = _cofre_corrente()
    if version != 389 or cf.get("cofre") != "um_unificado_v389":
        raise RuntimeError("Exact reviewed v389 custody required")
    for pin in meta["custody_pins"]:
        path = (cofre if pin["base"] == "um" else kernel) / pin["relative"]
        if _sha(path) != pin["sha256"] or path.stat().st_size != pin["bytes"]:
            raise RuntimeError("v389 custody pin mismatch: " + pin["relative"])
    return {
        "version": "v389", "source_um_sha256": meta["source_um_sha256"],
        "metadata_sha256": V389_METADATA_SHA256,
        "source_core_key": meta["source_core_key"],
        "source_verdict": meta["source_verdict"],
        "seal_label": meta["seal_label"],
        "ledger_reported": meta["ledger_reported"],
        "statute": meta["statute"],
        "beta_API_version_preserved": "v388",
        "physical_scale_mu_status": "OPEN_PER_DEVICE_AND_RITE",
        "kernel_recompiled_here": False, "legacy_results_recomputed": False,
        "physical_verdict_allowed": False,
    }
'''
    assert layer.count("\nUSOS = {")==1
    layer=layer.replace("\nUSOS = {",addition+"\nUSOS = {")
    needle='"adendo_v388": _adendo_v388_no_cofre(cf),'
    assert layer.count(needle)==1
    layer=layer.replace(needle,needle+'\n        "adendo_v389": _adendo_v389_no_cofre(cf),')
    ast.parse(layer)
    put(STAGE/LAYER,layer.encode("utf-8"))
    fresh_tree=ast.parse(layer); old_tree=ast.parse(oldlayer)
    od={x.name:ast.dump(x,include_attributes=False) for x in old_tree.body if isinstance(x,ast.FunctionDef)}
    nd={x.name:ast.dump(x,include_attributes=False) for x in fresh_tree.body if isinstance(x,ast.FunctionDef)}
    modified=[k for k in od if od[k]!=nd.get(k)]
    if set(modified)!={"camada","_adendo_v388_no_cofre"}:raise RuntimeError("Unexpected old function change")
    save("RECIBO_DELTA_CAMADA.json",{"stage_id":identity["stage_id"],"old":pin(ROOT/"baseline/tgl_formula_completa.py"),
         "new":pin(STAGE/LAYER),"old_functions_modified":modified,
         "new_functions":sorted(set(nd)-set(od)),"numerical_functions_AST_unchanged":True,
         "core_fields_changed":changes,"physical_reinterpretation":False,"execution":False})
    put(ROOT/"DELTA_CAMADA_V389.diff","".join(difflib.unified_diff(oldlayer.decode().splitlines(True),layer.splitlines(True),fromfile="v388/tgl_formula_completa.py",tofile="v389/tgl_formula_completa.py")).encode())
    print(json.dumps({"custody_files":len(copies),"formal_files":len(proof["formal_files_sha256"]),"layer":pin(STAGE/LAYER),"core_fields_changed":changes},ensure_ascii=False))

if __name__=="__main__":
    prepare()
