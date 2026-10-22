"""Create an immutable receipt for the scalar orbital rotation construction."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ["OrbitalSpatialLorentzR2", "OrbitalSpatialPoincareR2",
           "OrbitalOrientedBoostR1", "OrbitalLorentzAuditR1"]
OUTPUT = BASE / "FINAL_SPATIAL_POINCARE_RECEIPT_R1.json"
REPORT = BASE / "SPATIAL_POINCARE_R1.md"

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
    "Every real spatial orthogonal Q is embedded by an actual group homomorphism in the existing TGLExt.LorentzGrp. Preservation of the existing eta4 is proved from the scalar product, not a new input field.",
    "Translations and spatial transformations form the actual semidirect subgroup of TGLExt.PoincareGroup. Their unitary product law on the original H1 is proved.",
    "Conjugating the existing B0 by Q gives a strongly continuous boost group in the rotated direction. Its covariance is with the actual conjugate Lorentz element on spacetime translations.",
    "This construction reuses the original H1, U1, B0, orbitalMeasure and the proved scalar spatial inverse pullback action."
]
limits = [
    "The action is scalar on the two helicity coordinates; no Wigner helicity phase is supplied. The scalar and photon networks are not identified.",
    "The different conjugate boost groups are built, but this receipt does not yet establish a representation of every Lorentz element or all relations among mixed rotation/boost words.",
    "CanonicalNetInput receives no complete field from this step: K, K_mono, K_local, K_translate, K_boost and wedge_glue remain to be constructed jointly. Translation covariance is an operator identity, not a proof of K_translate for a global net.",
    "The helicity integer and its plus/minus-one property may be chosen as labels, but this does not construct the Wigner representation. A photon network also needs its helicity cocycle and independence of wedge transport; scalar wedge transport requires its own stabilizer and locality arguments.",
    "Independent mathematical review is pending with the parent. Nothing in production, canonical memory or the gate is changed."
]
report = "# Subgrupo espacial de Poincaré e boosts conjugados — candidato R1\n\n"
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
          "previous_receipt": pin(BASE / "FINAL_ORBITAL_CONTINUITY_RECEIPT_R1.json"), "accepted": accepted, "all_local_decl_count": len(decls),
          "all_local_declarations": [{"name": n, "axioms": list(filter(None, a.split(',')))} for n, a in decls],
          "zero_sorry": True, "axioms_only_trio": True,
          "failed_attempts_preserved": failed, "checked_dependencies_and_artifacts": list(checked.values()),
          "scripts": [pin(__file__), pin(BASE / "build_orbital_r1.py")],
          "report": pin(REPORT), "production_modified": False,
          "memory_modified": False, "gate_modified": False,
          "independent_review": "PENDING_PARENT"}
write_new(OUTPUT, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"receipt": pin(OUTPUT), "count": len(decls), "failed_attempts": len(failed)}, ensure_ascii=False))
