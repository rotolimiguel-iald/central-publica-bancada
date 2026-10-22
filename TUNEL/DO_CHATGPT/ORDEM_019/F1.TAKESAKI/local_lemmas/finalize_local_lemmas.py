"""Pin the already completed build without running another compilation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")


def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def write_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
    if path.read_bytes() != data:
        raise OSError(f"Verification failed: {path}")


def main() -> None:
    receipts = sorted((BASE / "attempts").glob("*/RECEIPT.json"))
    build = json.loads(receipts[-1].read_text(encoding="utf-8"))
    if build["exit_code"] != 0:
        raise RuntimeError("The latest attempt did not pass")
    output = (receipts[-1].parent / "AXIOMS.txt").read_text(encoding="utf-8")
    statements = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
    if len(statements) != 5:
        raise RuntimeError("Unexpected theorem count")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    for name, axioms in statements:
        if set(axioms.split(", ")) - allowed:
            raise RuntimeError(f"Unexpected axioms: {name}")
    source = BASE / "TakesakiAlgebraicCore.lean"
    if re.search(r"\b(sorry|admit|axiom)\b", source.read_text(encoding="utf-8")):
        raise RuntimeError("Forbidden proof placeholder or axiom keyword")
    manifest = KERNEL / "lake-manifest.json"
    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    mathlib = [p for p in manifest_data["packages"] if p["name"] == "mathlib"]
    if len(mathlib) != 1:
        raise RuntimeError("Mathlib pin missing or ambiguous")
    sources = [
        KERNEL / "TGLExt/GlobalLiftLadder.lean",
        KERNEL / "TGLExt/TheScaleHasNoFixedPoint.lean",
        KERNEL / ".lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Exp.lean",
        BASE.parent.parent / "F1.2/sandbox/F12Completion/V351DualScalingBridge.lean",
        manifest,
    ]
    result = {
        "status": "DERIVED_SANDBOX_PASS_PENDING_INDEPENDENT_REVIEW",
        "unit": "F1.TAKESAKI", "five_theorems_pass": True,
        "axiom_reports": [{"name": n, "axioms": a.split(", ")} for n, a in statements],
        "forbidden_proof_tokens": 0,
        "build_receipt": pin(receipts[-1]), "build": build,
        "mathlib_manifest_entry": mathlib[0],
        "existing_sources_read": [pin(p) for p in sources],
        "failed_attempts_preserved": [pin(p) for p in receipts[:-1]],
        "all_local_artifacts": [pin(p) for p in sorted(BASE.rglob("*")) if p.is_file()],
        "scope": "Algebraic obstruction and conditional reweighting; no general crossed-product or trace construction.",
        "nonvacuity": "Explicit two-coordinate real algebraic model, phi(Q(0,1))=1; no operator-algebra claim.",
        "analytic_obligation": "Prove domain-valid covariance of Q and identify phi with the correct dual weight.",
        "not_changed": ["um.py", "kernel", "production_bench", "memory", "board", "gate"],
    }
    report = "\n".join([
        "# F1.TAKESAKI — núcleo algébrico local",
        "[DERIVED — candidato em sandbox, aguardando revisão independente] PASSA: 5 teoremas, EXIT 0, somente propext/Classical.choice/Quot.sound, zero sorry.",
        "Reuso: a obstrução para s>0 já existe em GlobalLiftLadder.DualScalingData.fixed_tau_zero; a escala v351 já foi ligada à Fundação pela F1.2.",
        "(a) Se tau(1)>0 é real, theta(1)=1 e tau(theta x)=exp(-s)tau(x), então s=0. Não se aplica a tau(1)=infinito.",
        "(b) Para tau=phi∘Q, invariância de phi + homogeneidade de phi + Q(theta x)=exp(-s)•theta(Q x) implicam a escala.",
        "A covariância e o domínio de Q continuam sendo a obrigação analítica; nenhuma invariância simples da identidade os fornece neste arquivo.",
        "Controle negativo: identidade em ℝ preserva o funcional identidade, mas não admite a lei de escala para s≠0.",
        "Não vacuidade algébrica: theta_s(x,y)=(x,exp(-s)y), phi(x,y)=x, Q(x,y)=(y,0), com phi(Q(0,1))=1.",
        "Não se constrói produto cruzado, peso dual, traço canônico, operador afiliado nem ligação nova ao v351; o modelo ℝ² não os representa por teorema.",
        "A primeira tentativa falhou só porque modelTheta precisava de noncomputable; fonte e logs dessa tentativa foram preservados.",
        f"Build final: {receipts[-1].parent.name}; {build['seconds']:.6f} s; início {build['start_utc']}; fim {build['end_utc']}.",
        "RESULTADO_LOCAL_R1.json contém comando literal, LEAN_PATH, versão, todos os pins locais e fontes reutilizadas.",
        "Nenhuma escrita fora desta pasta local_lemmas; sem junção NTFS, provedor ou instalação.",
    ]) + "\n"
    write_new(BASE / "RELATORIO_LOCAL_R1.md", report.encode("utf-8"))
    result["report"] = pin(BASE / "RELATORIO_LOCAL_R1.md")
    result_path = BASE / "RESULTADO_LOCAL_R1.json"
    write_new(result_path, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"source": pin(source), "report": result["report"], "result": pin(result_path),
                      "build_receipt": result["build_receipt"], "mathlib_rev": mathlib[0].get("rev")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
