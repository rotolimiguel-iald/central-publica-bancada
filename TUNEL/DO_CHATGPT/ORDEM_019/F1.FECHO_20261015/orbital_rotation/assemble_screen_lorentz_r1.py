"""Create an immutable receipt for the scalar orbital rotation construction."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
MODULES = ['ScreenCocycleMatrixR4', 'ScreenCircularCoefficientsR1', 'ScreenLorentzTransportR7', 'ScreenLorentzCocycleR3', 'ScreenMatrixMultiplierR4', 'ScreenLorentzRepresentationR3', 'ScreenTransportContinuityR5', 'ScreenMultiplierContinuityR3', 'ScreenPoincareCovarianceR2', 'ScreenStrongContinuityR6', 'NullFrameDetRootR4', 'ScreenOrientationDetRootR3', 'ScreenPhysicalHelicityR2', 'ScreenCircularBasisR2', 'ScreenHelicityRepresentationR3', 'ScreenHelicityDiagonalR3', 'ScreenFutureHelicityR2', 'ScreenLorentzAuditR2']
OUTPUT = BASE / "FINAL_SCREEN_LORENTZ_RECEIPT_R1.json"
REPORT = BASE / "SCREEN_LORENTZ_R1.md"

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
    "The real transverse screen coefficient matrix is derived from the actual massless momentum transport and Minkowski pairing. Its unitary, identity and cocycle laws are proved, with no representation or cocycle assumed as a field.",
    "The measurable matrix multiplier and the existing invariant mass-shell measure yield an actual unitary representation on the unchanged canonical H1. Strong continuity is proved by pointwise screen continuity and dominated convergence, with a 4*norm(f)^2 bound.",
    "Translation covariance, the Poincare product and exact agreement with the existing longitudinal B0 are proved. Every future Lorentz matrix is included through the already proved generation theorem.",
    "The determinant-one condition on the actual four-dimensional Lorentz matrix implies orientation of the transverse screen. The unit-modulus phase and its cocycle are then derived from the existing O16 formulas.",
    "The normalized fixed unitary C=(sqrt(2))^-1[[1,1],[i,-i]] is lifted to H1 and proved to commute with U1 and B0. The physical circular action is C^-1 U_screen C, not a relabeling of the scalar orbital action.",
    "For proper transformations the circular action is proved almost everywhere to be diag(zeta,conj(zeta)) followed by inverse momentum transport. The two helicity phases follow from the actual screen eigenvectors."
]
limits = [
    "The construction is an operator representation, not yet a localized real-subspace net. None of the joint CanonicalNetInput K, K_mono, K_local, K_translate, K_boost or exact wedge_glue obligations is claimed paid by this block alone.",
    "The canonical standard KWR, its nontriviality, Tomita operator, modular boost and Fock realization already exist and are reused; they are not reconstructed or classified as absent.",
    "A covariance proof for transport of KWR, independence of the chosen wedge transport and the appropriate localization theorem remain separate. The fixed circular basis does not by itself prove the geometric J intertwiner or an irreducible Wigner classification.",
    "The FutureLorentz product wrapper carries the explicit future-product condition hLM, as in the preceding accepted block. The representation homomorphism itself is already proved on the generated subgroup, so no generator-word relation is assumed.",
    "Almost-everywhere statements exclude the null chart axis, whose measure-zero property is proved. No physical measurement, nature test or empirical credibility is inferred.",
    "The parent supplied the two determinant modules; their independent semantic review is included. Independent review of this assembled screen block remains with the parent."
]
report = "# Cociclo físico da tela e representação circular — candidato R1\n\n"
report += "[REAL — compilado em sandbox; revisão independente do conjunto pendente.]\n\n"
report += "## Construção\n\n" + "\n".join("- " + s for s in scope)
report += "\n\n## Alcance e obrigações restantes\n\n" + "\n".join("- " + s for s in limits)
report += f"\n\n## Evidência\n\n{len(accepted)} compilações aceitas, incluindo o auditor de todas as {len(decls)} declarações locais (privadas e auxiliares incluídas), só o trio; zero sorry nas fontes aceitas. As {len(failed)} tentativas recusadas do diretório estão preservadas e pinadas. Comando, toolchain, LEAN_PATH literal, início, fim, segundos e exit constam dos recibos.\n"
report += "\nReaproveitamento dirigido: F1.REDE/CONSTRUCAO_CONTINUA_R1 e CONTRATO_REDE_R2; semirretas em ConcreteLightRayNet; KWR/Tomita em CanonicalOutput. A passagem para a rede global precisa consumir esses termos e provar a identificação localizada, sem rede nula nem nova hipótese equivalente ao resultado.\n"
write_new(REPORT, report.encode("utf-8"))
result = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "unit": "F1.FECHO_20261015", "claim": 845,
    "status": "COMPILED_CANDIDATE_INDEPENDENT_REVIEW_PENDING", "statute": "REAL",
    "scope": scope, "limits": limits,
    "previous_receipt": pin(BASE / "FINAL_FUTURE_LORENTZ_RECEIPT_R1.json"),
    "orientation_independent_semantic_review": pin(BASE / "SCREEN_ORIENTATION_SEMANTIC_REVIEW_SKEPTIC_R1.json"),
    "accepted": accepted, "all_local_decl_count": len(decls),
    "all_local_declarations": [{"name": n, "axioms": list(filter(None, a.split(',')))} for n,a in decls],
    "zero_sorry": True, "axioms_only_trio": True,
    "failed_attempts_preserved": failed, "checked_dependencies_and_artifacts": list(checked.values()),
    "scripts": [pin(__file__),pin(BASE / "prepare_screen_receipt_r2.py"),pin(BASE / "build_orbital_r1.py")],
    "report": pin(REPORT), "production_modified": False, "memory_modified": False,
    "gate_modified": False, "independent_review": "PENDING_PARENT"}
write_new(OUTPUT,(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"receipt":pin(OUTPUT),"count":len(decls),"accepted":len(accepted),"failed_attempts":len(failed)},ensure_ascii=False))
