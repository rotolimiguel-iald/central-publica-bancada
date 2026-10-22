"""Custody of a completed concrete light-ray construction; no new build."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")

def pin(path: Path) -> dict:
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def save(path: Path, b: bytes) -> None:
    with path.open("xb") as f:
        f.write(b)
    if path.read_bytes() != b:
        raise OSError(f"Byte verification failed: {path}")

def main() -> None:
    receipts = sorted((BASE / "attempts").glob("*/RECEIPT.json"))
    receipt = json.loads(receipts[-1].read_text(encoding="utf-8"))
    if receipt["exit_code"] != 0:
        raise RuntimeError("Latest build failed")
    source = BASE / "ConcreteLightRayNet.lean"
    source_text = source.read_text(encoding="utf-8")
    if re.search(r"\b(sorry|admit)\b", source_text):
        raise RuntimeError("Proof placeholder in source")
    output = (receipts[-1].parent / "AXIOMS.txt").read_text(encoding="utf-8")
    reports = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
    locals_ = re.findall(r"^LOCAL_DECL\t([^\t]+)\t(.*)$", output, re.M)
    if len(reports) != 15 or not locals_:
        raise RuntimeError("Expected declarations were not audited")
    for name, axioms in reports + locals_:
        if set(a.strip() for a in axioms.split(",") if a.strip()) - {"propext", "Classical.choice", "Quot.sound"}:
            raise RuntimeError(f"Unexpected axiom: {name}")
    sources = [
        "TGLExt/O16/FourierStandardTransport_v3.lean",
        "TGLExt/O16/LightRayGaussianDensity_v2.lean",
        "TGLExt/O16/FourierLightRayBridge.lean",
        "TGLExt/O16/RetaDeLuzBorchersAudited.lean",
        "TGLExt/ContinuousModularStandardSubspace.lean",
        "TGLExt/ContinuousModularDomain.lean",
        "TGLExt/ContinuousModularReconstruction.lean",
        "TGLExt/V350L2CharacterMultiplier.lean",
        ".lake/packages/mathlib/Mathlib/Topology/Algebra/Module/ClosedSubmodule.lean",
        "lake-manifest.json",
    ]
    result = {
        "unit": "F1.REDE", "scope": "one-particle standard-subspace net on the real light ray",
        "status": "DERIVED_SANDBOX_PASS_PENDING_INDEPENDENT_REVIEW",
        "build": receipt, "source": pin(source), "build_receipt": pin(receipts[-1]),
        "print_axioms_count": len(reports), "all_local_declarations_audited": len(locals_),
        "axiom_reports": [{"name": n, "axioms": a.strip()} for n, a in reports],
        "local_declarations": [{"name": n, "axioms": a.strip()} for n, a in locals_],
        "sources": [pin(KERNEL / s) for s in sources],
        "attempts": [pin(p) for p in receipts],
        "artifacts": [pin(p) for p in sorted(BASE.rglob("*")) if p.is_file()],
        "passed": {
            "concrete_standard_subspace_family": "K_a=U(a)K_0; K_0=rapidityStandardSubspace(2*pi^2)",
            "isotony": "a<=b implies K_b subset K_a",
            "translation_covariance": "U(t)K_a=K_(t+a), both membership and mapEquiv equality",
            "dilation_covariance": "D(s)f belongs K_(exp(-s)*a) iff f belongs K_a",
            "nonvacuity": "Each K_a is not bottom and has a nonzero member; no new hypothesis",
            "four_dimensional_negative_control": "Any translation lift through a single linear coordinate has a nonzero kernel",
        },
        "not_claimed": ["full 4D Wigner representation", "faithful 4D translations", "Fock realization", "von Neumann algebra net", "stress tensor", "H3 derived from state"],
        "new_scientific_hypotheses": [],
        "graph_consultation": "F1.REDE absent from current Nos Vivo graph; existing O16 source files read directly",
        "memory_reference": r"C:\IALD\Central de Patentes\work\rede_quantica_20261013\ACOM_REFERENCE.json",
        "memory_project_context": "404cb362-730c-5dbd-a0ad-7d0855ffcce4",
        "writes": "new sandbox light_ray files only; no junction, original, board or memory mutation",
    }
    lines = [
        "# F1.REDE — família concreta da reta de luz",
        f"[DERIVED — candidato em sandbox] PASSA: EXIT 0; {len(reports)} #print axioms e {len(locals_)} declarações locais auditadas; somente o trio; zero sorry.",
        "K_a=U(a)K_0 foi construído como StandardSubspace por transporte complexo contínuo; K_0 é rapidityStandardSubspace(2π²) do O16.",
        "Isotonia provada: a≤b implica K_b⊆K_a, consumindo halfline_isotony do O16.",
        "Covariância exata por translação: U(t)K_a=K_(t+a), incluindo igualdade dos subespaços transportados.",
        "Covariância exata por dilatação: D(s)f∈K_(exp(-s)a) sse f∈K_a.",
        "A invariância de K_0 por D foi provada pela fórmula de Fourier, preservação do domínio de Tomita e conjugação da fase; nenhuma hipótese científica nova.",
        "Não vacuidade: cada K_a≠⊥ e possui vetor não nulo, por ciclicidade e fidelidade já provada de U.",
        "Controle negativo reutilizado: uma única coordenada nula não dá translações fiéis em ℝ⁴.",
        "Não constrói representação Wigner 4D, segunda quantização/Fock, rede de álgebras, tensor T nem H3 a partir do estado.",
        f"Build final {receipts[-1].parent.name}: {receipt['seconds']:.6f} s; início/fim explícitos, comando, toolchain e LEAN_PATH em BUILD.log e RESULTADO_LIGHT_RAY_R1.json.",
        "Todas as tentativas anteriores e seus bytes estão preservados; fontes e artefatos pinados por script.",
        "ACOM próprio projetado; Nós Vivo ainda não indexa F1.REDE. Foram lidas as pedras existentes diretamente.",
        "Somente arquivos novos em light_ray; nada instalado ou escrito em produção, memória, quadro ou gate.",
    ]
    report = BASE / "RELATORIO_LIGHT_RAY_R1.md"
    save(report, ("\n".join(lines) + "\n").encode("utf-8"))
    result["report"] = pin(report)
    result_path = BASE / "RESULTADO_LIGHT_RAY_R1.json"
    save(result_path, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"source": pin(source), "result": pin(result_path), "report": pin(report),
                      "print_axioms": len(reports), "local_declarations": len(locals_)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
