"""Generate new receipt/auditor scripts; no canonical or memory write."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent
modules = [
    "ScreenCocycleMatrixR4", "ScreenCircularCoefficientsR1",
    "ScreenLorentzTransportR7", "ScreenLorentzCocycleR3", "ScreenMatrixMultiplierR4",
    "ScreenLorentzRepresentationR3", "ScreenTransportContinuityR5",
    "ScreenMultiplierContinuityR3", "ScreenPoincareCovarianceR2",
    "ScreenStrongContinuityR6", "NullFrameDetRootR4", "ScreenOrientationDetRootR3",
    "ScreenPhysicalHelicityR2", "ScreenCircularBasisR2", "ScreenHelicityRepresentationR3",
    "ScreenHelicityDiagonalR2", "ScreenFutureHelicityR1"]
audit_name = "ScreenLorentzAuditR2"
audit = (base / "LorentzFutureAuditR1.lean").read_text(encoding="utf-8")
audit = audit.replace("import LorentzFutureRepresentationR1", "import ScreenFutureHelicityR1")
audit = re.sub(r"let roots : List Name := \[.*?\]", "let roots : List Name := [" +
               ", ".join("`" + m for m in modules) + "]", audit, flags=re.S)
source = (base / "assemble_future_lorentz_r1.py").read_text(encoding="utf-8")
source = re.sub(r"MODULES = \[.*?\]", "MODULES = " + repr(modules + [audit_name]), source, count=1, flags=re.S)
source = source.replace("FINAL_FUTURE_LORENTZ_RECEIPT_R1.json", "FINAL_SCREEN_LORENTZ_RECEIPT_R1.json")
source = source.replace("FUTURE_LORENTZ_R1.md", "SCREEN_LORENTZ_R1.md")
source = source[:source.index("scope = [")] + r'''
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
    "scripts": [pin(__file__),pin(BASE / "prepare_screen_receipt_r1.py"),pin(BASE / "build_orbital_r1.py")],
    "report": pin(REPORT), "production_modified": False, "memory_modified": False,
    "gate_modified": False, "independent_review": "PENDING_PARENT"}
write_new(OUTPUT,(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"receipt":pin(OUTPUT),"count":len(decls),"accepted":len(accepted),"failed_attempts":len(failed)},ensure_ascii=False))
'''
for name, text in [(audit_name + ".lean", audit), ("assemble_screen_lorentz_r1.py", source)]:
    p = base / name
    with p.open("xb") as f:
        f.write(text.encode("utf-8"))
    print(p)
