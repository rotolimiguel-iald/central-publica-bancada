"""Create an immutable receipt for the scalar orbital rotation construction."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ["OrbitalGeneratedMeasureR2", "OrbitalGeneratedUnitaryR3",
           "OrbitalGeneratedCovarianceR3", "OrbitalGeneratedAuditR1"]
OUTPUT = BASE / "FINAL_GENERATED_LORENTZ_RECEIPT_R1.json"
REPORT = BASE / "GENERATED_LORENTZ_R1.md"

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
    "The subgroup generated in the actual LorentzGrp by all real spatial orthogonal transformations and the longitudinal boost is constructed. Every element and inverse has a measure-preserving mass-shell lift, proved by subgroup closure.",
    "The explicit action shellAction(L,p)=momentumOf(L*shellMomentum(p)) agrees almost everywhere with every such lift. Injectivity of shellMomentum proves uniqueness, so mixed words giving the same Lorentz matrix give the same L2 operator.",
    "Inverse pullback on the original H1 is a genuine LinearIsometryEquiv and a group homomorphism. Its spatial and longitudinal generators are exactly the existing scalarOrthogonalH1 and B0, not merely isomorphic copies.",
    "The Lorentz group and generated subgroup carry the induced matrix topology. Strong continuity is proved with the explicit continuous pullback family and local regularity of the existing orbital measure.",
    "The representation satisfies actual U1 translation covariance for every element, and the resulting representation of the semidirect Poincare subgroup has the correct product law."
]
limits = [
    "This receipt does not assert that the generated subgroup exhausts all future Lorentz transformations. The decomposition is subsequent work and not silently included here.",
    "Spatial generators include orthogonal reflections. The action is scalar on both complex coordinates, not the induced photon helicity representation. The name H1 is the unchanged canonical type and does not by itself fix physical helicity.",
    "CanonicalNetInput receives no completed field: a global K with isotony, locality, translation/boost covariance and the exact wedge_glue still needs construction. Operator covariance alone is not net covariance.",
    "PhotonCharacterCocycle.screen_phase_cocycle is reusable but still requires its explicit ScreenOrientationMeasured obligation; F1.3 also records the global-helicity obligation. Neither is discharged by this scalar representation.",
    "Independent review is pending with the parent; all production, canonical memory and the gate stay unchanged."
]
report = "# Representação escalar do subgrupo de Lorentz gerado — candidato R1\n\n"
report += "[REAL — compilado em sandbox; revisão independente pendente.]\n\n"
report += "## Construção\n\n" + "\n".join("- " + s for s in scope)
report += "\n\n## Alcance\n\n" + "\n".join("- " + s for s in limits)
report += f"\n\n## Evidência\n\nQuatro compilações aceitas, incluindo auditor de todas as {len(decls)} declarações locais (privadas e auxiliares incluídas), só o trio; zero sorry nas fontes aceitas. As {len(failed)} tentativas recusadas estão preservadas e pinadas no recibo. Comandos, LEAN_PATH literal, início/fim, segundos e saída estão nos recibos de cada tentativa.\n"
report += "\nA construção reaproveita orbitalMeasure, energia, orbitalTranslation e U1 canônicos. Nenhuma invariância de medida é premissa adicionada ao resultado: ela decorre da carta euclidiana, da preservação de volume e da invariância da energia.\n"
write_new(REPORT, report.encode("utf-8"))
result = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
          "unit": "F1.FECHO_20261015", "claim": 845,
          "status": "COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING",
          "statute": "REAL", "scope": scope, "limits": limits,
          "previous_receipt": pin(BASE / "FINAL_SPATIAL_POINCARE_RECEIPT_R1.json"), "accepted": accepted, "all_local_decl_count": len(decls),
          "all_local_declarations": [{"name": n, "axioms": list(filter(None, a.split(',')))} for n, a in decls],
          "zero_sorry": True, "axioms_only_trio": True,
          "failed_attempts_preserved": failed, "checked_dependencies_and_artifacts": list(checked.values()),
          "scripts": [pin(__file__), pin(BASE / "build_orbital_r1.py")],
          "report": pin(REPORT), "production_modified": False,
          "memory_modified": False, "gate_modified": False,
          "independent_review": "PENDING_PARENT"}
write_new(OUTPUT, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"receipt": pin(OUTPUT), "count": len(decls), "failed_attempts": len(failed)}, ensure_ascii=False))
