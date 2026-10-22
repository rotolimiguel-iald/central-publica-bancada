"""Create an immutable receipt for the scalar orbital rotation construction."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ["OrbitalSpatialMeasureR1", "OrbitalSpatialUnitaryR3",
           "OrbitalQuarterTurnR4", "OrbitalQuarterCovarianceR1", "OrbitalAuditR1"]
OUTPUT = BASE / "FINAL_ORBITAL_ROTATION_RECEIPT_R1.json"
REPORT = BASE / "ORBITAL_ROTATION_R1.md"

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

def write_new(p, b):
    if p.exists():
        raise RuntimeError(f"Existing output refused: {p}")
    tmp = p.with_name(p.name + ".tmp")
    with tmp.open("xb") as f:
        f.write(b)
    if tmp.read_bytes() != b:
        raise RuntimeError("Temporary bytes differ")
    tmp.rename(p)

if OUTPUT.exists() or REPORT.exists():
    raise RuntimeError("Existing final evidence refused before assembly")

receipts = [(p, json.loads(p.read_text(encoding="utf-8")))
            for p in sorted((BASE / "attempts").glob("*/RECEIPT.json"))]
accepted, checked = [], {}
for mod in MODULES:
    src = BASE / (mod + ".lean")
    srcpin = pin(src)
    if re.search(r"\bsorry\b", src.read_text(encoding="utf-8")):
        raise RuntimeError("Sorry token refused")
    matches = [(p, r) for p, r in receipts if r["exit_code"] == 0
               and Path(r["source"]["path"]).stem == mod
               and r["source"]["sha256"] == srcpin["sha256"]]
    if not matches:
        raise RuntimeError(f"No accepted compilation: {mod}")
    rp, r = matches[-1]
    if not r["readonly_dependencies_unchanged"]:
        raise RuntimeError("Dependencies changed during compilation")
    for entry in [r["source"], *r["dependencies"], *r["artifacts"]]:
        if pin(entry["path"])["sha256"] != entry["sha256"]:
            raise RuntimeError(f"Pin differs: {entry['path']}")
        checked[entry["path"]] = entry
    accepted.append({"module": mod, "source": srcpin, "receipt": pin(rp),
                     "exit_code": r["exit_code"], "seconds": r["seconds"],
                     "start_utc": r["start_utc"], "end_utc": r["end_utc"],
                     "LEAN_PATH": r["LEAN_PATH"], "toolchain": r["toolchain"]})

audit_dir = Path(accepted[-1]["receipt"]["path"]).parent
audit = (audit_dir / "AXIOMS.txt").read_text(encoding="utf-8")
decls = re.findall(r"^LOCAL_DECL\t([^\t\r\n]+)\t([^\r\n]*)", audit, re.M)
counts = re.findall(r"^AUDITED_COUNT\t([0-9]+)", audit, re.M)
if len(counts) != 1 or len(decls) != int(counts[0]) or not decls:
    raise RuntimeError("Incomplete all-local audit")
trio = {"propext", "Classical.choice", "Quot.sound"}
for name, ax in decls:
    if not set(filter(None, ax.split(","))) <= trio:
        raise RuntimeError(f"Non-trio declaration: {name}")

failed = []
for rp, r in receipts:
    if r["exit_code"] != 0:
        failed.append({"receipt": pin(rp), "exit_code": r["exit_code"],
                       "source": pin(r["source"]["path"]),
                       "log": pin(rp.parent / "BUILD.log")})

scope = [
    "For any real orthogonal spatial transformation Q, the existing orbitalMeasure m is preserved, including m=0.",
    "The inverse pullback is a complex linear isometric equivalence on the existing orbital L2 space; identity and composition laws are proved.",
    "scalarSpatialH1 has exactly TGLExt.ImportedSQ.H1 as both source and target; the auxiliary Euclidean chart only proves measure invariance.",
    "A concrete proper quarter turn (q0,q1,p)->(p,q1,-q0) moves the longitudinal axis; its coordinate matrix has determinant one.",
    "The quarter-turn operator intertwines the original U1 translations with a->(a0,-a2,a1,a3), including the conjugation formulation."
]
limits = [
    "This is the scalar orbital action, identical on the two helicity coordinates; no momentum-dependent Wigner phase or physical helicity representation is supplied.",
    "No full Lorentz or Poincare group representation, strong continuity in the spatial transformation, transported wedge net or global localization is claimed.",
    "No existing Remaining input field is removed solely because these component theorems exist.",
    "This receipt records construction and compilation. Independent mathematical review remains pending with the parent; no production or canonical installation."
]
report = "# Rotação orbital no mesmo H1 — candidato R1\n\n"
report += "[REAL — compilado em sandbox; revisão independente pendente.]\n\n"
report += "## Construção\n\n" + "\n".join("- " + s for s in scope)
report += "\n\n## Alcance\n\n" + "\n".join("- " + s for s in limits)
report += f"\n\n## Evidência\n\nCinco compilações aceitas, incluindo auditor de todas as {len(decls)} declarações locais (privadas e auxiliares incluídas), só o trio; zero sorry nas fontes aceitas. As {len(failed)} tentativas recusadas estão preservadas e pinadas no recibo. Comandos, LEAN_PATH literal, início/fim, segundos e saída estão nos recibos de cada tentativa.\n"
report += "\nA construção reaproveita orbitalMeasure, energia, orbitalTranslation e U1 canônicos. Nenhuma invariância de medida é premissa adicionada ao resultado: ela decorre da carta euclidiana, da preservação de volume e da invariância da energia.\n"
write_new(REPORT, report.encode("utf-8"))
result = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
          "unit": "F1.FECHO_20261015", "claim": 845,
          "status": "COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING",
          "statute": "REAL", "scope": scope, "limits": limits,
          "accepted": accepted, "all_local_decl_count": len(decls),
          "all_local_declarations": [{"name": n, "axioms": list(filter(None, a.split(',')))} for n, a in decls],
          "zero_sorry": True, "axioms_only_trio": True,
          "failed_attempts_preserved": failed, "checked_dependencies_and_artifacts": list(checked.values()),
          "scripts": [pin(__file__), pin(BASE / "build_orbital_r1.py")],
          "report": pin(REPORT), "production_modified": False,
          "memory_modified": False, "gate_modified": False,
          "independent_review": "PENDING_PARENT"}
write_new(OUTPUT, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"receipt": pin(OUTPUT), "count": len(decls), "failed_attempts": len(failed)}, ensure_ascii=False))
