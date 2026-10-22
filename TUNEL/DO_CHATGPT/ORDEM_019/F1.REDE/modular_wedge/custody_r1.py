"""Create additive custody of the concrete modular construction."""
from pathlib import Path
import datetime
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
FINAL = {
    "VectorWedge": "20261013T213951_215364Z",
    "SpectralConjugation": "20261013T213929_050015Z",
    "VectorSquare": "20261013T214259_982971Z",
    "CanonicalWedge": "20261013T214813_431261Z",
    "CanonicalOutput": "20261013T215105_011078Z",
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def pin(p):
    return {"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)}

def save(name, data):
    p = BASE / name
    if p.exists():
        raise FileExistsError(p)
    temp = BASE / (name + ".tmp")
    with temp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if temp.read_bytes() != data:
        raise OSError("Byte mismatch")
    temp.rename(p)
    return pin(p)

def main():
    modules, artifacts, dependencies = [], [], {}
    for module, stamp in FINAL.items():
        d = BASE / "attempts" / stamp
        r = json.loads((d / "RECEIPT.json").read_text(encoding="utf-8"))
        if r["exit_code"] != 0:
            raise RuntimeError(module)
        if (d / (module + ".lean")).read_bytes() != (BASE / (module + ".lean")).read_bytes():
            raise RuntimeError("Root differs from compiled copy")
        modules.append({"module": module, "receipt": pin(d / "RECEIPT.json"),
                        "source": pin(d / (module + ".lean")),
                        "start_utc": r["start_utc"], "end_utc": r["end_utc"],
                        "seconds": r["seconds"], "exit_code": r["exit_code"]})
        artifacts += [pin(p) for p in sorted(d.iterdir()) if p.is_file()]
        for pp in r["read_only_dependency_paths"]:
            p = Path(pp)
            if "F1.REDE" in pp and (p / "RECEIPT.json").is_file():
                dependencies[pp] = pin(p / "RECEIPT.json")
    audit = BASE / "attempts" / "20261013T215159_491443Z" / "RECEIPT.json"
    ar = json.loads(audit.read_text(encoding="utf-8"))
    if ar["exit_code"] != 0:
        raise RuntimeError("Axiom probe failed")
    raw = (audit.parent / "AXIOMS.txt").read_text(encoding="utf-8")
    lines = [x for x in raw.splitlines() if "depends on axioms:" in x or "does not depend on any axioms" in x]
    decl = json.loads((BASE / "LOCAL_DECLARATIONS.json").read_text(encoding="utf-8"))
    if len(lines) != decl["count"] or "sorryAx" in raw or "error:" in raw:
        raise RuntimeError("Axiom audit failed")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    for line in lines:
        if "depends on axioms:" in line:
            axs = {x.strip() for x in line.split("[", 1)[1].split("]")[0].split(",")}
            if not axs <= allowed:
                raise RuntimeError(line)
    artifacts += [pin(p) for p in sorted(audit.parent.iterdir()) if p.is_file()]
    artifacts += [pin(p) for p in sorted(BASE.glob("*.py"))]
    artifacts += [pin(BASE / "LOCAL_DECLARATIONS.json")]
    failed = []
    for p in sorted((BASE / "attempts").glob("*/RECEIPT.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        if r["exit_code"] != 0:
            failed.append({"receipt": pin(p), "log": pin(p.parent / "BUILD.log"),
                           "source": pin(p.parent / Path(r["command"][-1]).name)})
    result = {
        "unit": "F1.REDE", "stage": "D1a.2 + concrete D1a.3 spectral output",
        "status": "REAL_COMPILED_SANDBOX__INDEPENDENT_REVIEW_PENDING",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "modules": modules, "axiom_audit": pin(audit),
        "audited_declarations": len(lines), "allowed_axioms": sorted(allowed), "sorry": 0,
        "proved": [
            "Jcandidate antiunitary and involutive on unchanged canonical H1",
            "Jcandidate spectral formula uses xi reflection and transverse q reflection, conjugation and helicity swap",
            "TW maximal multiplier exp(2*pi^2*xi), positive, self-adjoint, dense domain",
            "S=Jcandidate TW closed dense involution; K=Fix(S) is StandardSubspace H1",
            "Delta maximal multiplier exp(4*pi^2*xi), with exact graph Delta=S-adjoint S",
            "spectralOutput inhabits AuditF13v31.D1a3OutputBGL without additional hypotheses",
            "spectralOutput.KWR contains a nonzero vector and S is its Tomita map",
            "same multiplier phase is canonical B0(-2*pi*t)"],
        "not_proved": [
            "geometric Poincare covariance of Jcandidate",
            "physical localization of K as the canonical right wedge",
            "full four-dimensional LightNetData with covariance/isotony/locality",
            "FockCertificate or MaxwellCertificate inhabitant",
            "device continuum refinement equivalence", "H3 from a state"],
        "dependencies": list(dependencies.values()), "artifacts": artifacts,
        "preserved_failed_attempts": failed,
        "scope": {"canonical_H1_changed": False, "kernel_written": False,
                  "production_written": False, "gate_changed": False,
                  "junction_created": False, "new_provider_call": False},
        "semantic_note": "A concrete spectral standard subspace is constructed. The name KWR inside the inherited interface is not a proof of geometric wedge localization. T positivity is supplied separately because the prior interface asks only self-adjointness."
    }
    report = """# F1.REDE — construção modular concreta no H1 canônico

[REAL — Lean 4.31.0, sandbox] As cinco peças listadas no RESULTADO_MODULAR_R1.json compilam com EXIT 0. A auditoria de todas as 75 declarações locais usa somente propext, Classical.choice e Quot.sound, sem sorry. Os logs registram comando, toolchain, LEAN_PATH literal, início, fim, duração e código de saída. Tentativas anteriores ficam preservadas.

A ponte FubiniL2 já revista é reutilizada sem alteração. Phi é a carta de rapidez, seguida pela currificação vetorial e Fourier parcial. O H1 original é preservado.

Jcandidate é antiunitário involutivo: na representação espectral combina reflexão em xi, reflexão transversal q→−q, conjugação complexa e troca das duas componentes de helicidade. A covariância geométrica completa desse operador não é afirmada nesta entrega.

TW é construído, com domínio maximal explícito, como multiplicação por exp(2*pi^2*xi) depois de Phi. Está provado positivo e auto-adjunto. S=Jcandidate TW é involução fechada de domínio denso. K=Fix(S) é construído como StandardSubspace H1, é não nulo, e S é o seu Tomita.

Delta é multiplicação maximal por exp(4*pi^2*xi). A igualdade Delta=S†S é provada pelo grafo inteiro, incluindo ambos os domínios de composição. O mesmo símbolo sigma=4*pi^2*xi dá a fase modular igual ao B0(-2*pi*t) canônico.

O objeto spectralOutput habita efetivamente D1a3OutputBGL, sem acrescentar hipóteses de existência, e spectralOutput_positive fornece a positividade ausente da interface antiga. Não é apenas nova tipagem de uma saída aberta.

[OPEN] Falta a identificação geométrica/localização de K na cunha e a covariância de Poincare completa. Não foi construído um LightNetData completo em quatro dimensões, nem habitantes Fock/Maxwell, nem ponte de refinamento do dispositivo, nem H3 derivado do estado. O nome KWR na interface não carrega esses resultados.

Fontes finais e recibos por módulo estão em attempts/, pinados no resultado. Nada foi integrado ao Nós ou à Bancada, e o gate permanece intacto. Revisão independente segue com outro agente.
"""
    readme = save("RELATORIO_MODULAR_R1.md", report.encode("utf-8"))
    result["report"] = readme
    out = save("RESULTADO_MODULAR_R1.json", (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(out, ensure_ascii=False))
    print(json.dumps(readme, ensure_ascii=False))

if __name__ == "__main__":
    main()
