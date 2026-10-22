"""Seal the accepted matrix candidate without replacing any previous evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

BASE = Path(__file__).resolve().parent
def pin(path):
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def fresh(path, data):
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.stat().st_size == len(data)
    os.rename(tmp, path)

source = BASE / "TimeGravitonMatrix.lean"
accepted = BASE / "attempts" / "003"
build = json.loads((accepted / "RECEIPT.json").read_text(encoding="utf-8"))
assert build["exit_code"] == 0
assert pin(source)["sha256"] == build["source_sha256"]
assert source.read_bytes() == (accepted / "TimeGravitonMatrix.lean").read_bytes()
src = source.read_text(encoding="utf-8")
stdout = (accepted / "STDOUT.log").read_text(encoding="utf-8")
requested = re.findall(r"^#print axioms (\S+)$", src, re.M)
observed = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", stdout)
axioms = {name: [a.strip() for a in ax.split(",") if a.strip()] for name, ax in observed}
assert len(requested) == len(set(requested)) == len(axioms) == 42
assert set(requested) == set(axioms)
assert all(set(xs) <= {"propext", "Classical.choice", "Quot.sound"} for xs in axioms.values())
assert not re.search(r"\b(sorry|admit|sorryAx)\b", src)
assert "sorryAx" not in stdout
assert not re.search(r"^\s*axiom\s", src, re.M)
originals = json.loads((BASE / "SOURCES_R1.json").read_text(encoding="utf-8"))
for original in originals:
    assert pin(Path(original["path"]))["sha256"] == original["sha256"]
attempts = []
for folder in sorted((BASE / "attempts").iterdir()):
    receipt = json.loads((folder / "RECEIPT.json").read_text(encoding="utf-8"))
    attempts.append({"attempt": folder.name, "build": receipt,
        "artifacts": [pin(p) for p in sorted(folder.iterdir()) if p.is_file()]})

scope = [
    "[REAL] Exact M2 bridge: C = diag(1,i) is star of the existing phaseGate; C sigma_x C* = sigma_y; transported Hlig is i V0 genK.",
    "[REAL] Eg is a concrete complex-linear two-block pinching, idempotent, trace preserving, unital; it fixes P+/P- and kills root+/root-.",
    "[REAL] The spectral coordinate transport identifies Eg with existing diagExpect and PostoAdendo.nameOp rhoStar by theorem, not by a hypothesis field.",
    "[REAL] The normalized source vector has density P+; its C-transport has density PxMinus and Eg reads I/2. P+ and P- are distinct; positive V0/hbar have witnesses.",
    "[REAL] Existing angular family has root phases exp(+/-2 i theta); substituting theta=(V0/hbar)t gives frequency 2 Omega. The Hamiltonian generator normalization is exact.",
    "[REAL] Hpos = V0 I + Hg = 2 V0 P-. A real-amplitude jump a P- yields (a^2/2)(Eg-Id). This theorem does not itself fix a physically.",
    "[OPEN in this module] Equality to a matrix exponential, norm-continuous GKLS flow, complete positivity, dimension of the fixed algebra and physical calibration are not asserted by this module; the sibling flow and physical contract have separate receipts.",
    "[SCOPE] No universal zero-energy convention, unique universal attractor, continuous global network, observed data, empirical confirmation or gate change is claimed. The angular phase is a reading; dissipative convergence belongs to the separate dynamics.",
]
report = "# Ponte matricial v394 — recibo de sandbox\n\n" + "\n\n".join(scope)
report += "\n\n## Build aceito\n\n"
report += f"Tentativa 003: EXIT 0, {build['seconds']:.6f} s; 42 declarações, somente propext/Classical.choice/Quot.sound; zero sorry/admit/axiom novo. A fonte final é `TimeGravitonMatrix.lean`; importar `TimeGravitonMatrix` pelo diretório `attempts/003`.\n"
report += "\nAs tentativas 001 e 002 falharam por expansão de táticas; seus fontes, logs completos e recibos estão preservados. A versão antiga em `TGLExt/TimeGravitonMatrix.lean` pertence à tentativa 001 e não é a candidata aceita. Os avisos da tentativa 003 são de simp/táticas não usados, sem erro de prova.\n"
report += "\nA fonte e o .olean aceitos ficam imutáveis. Nova correção exige arquivo/tentativa novos. O registro do quadro, mapa e memória cabe à coordenação sob a reivindicação 839.\n"
fresh(BASE / "RELATORIO_MATRIX_R1.md", report.encode("utf-8"))
receipt = {
    "unit": "F1.TEMPO.V394", "subtask": "formal_matrix", "claim": 839,
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS_SANDBOX_AWAITING_INDEPENDENT_REVIEW",
    "accepted_attempt": "003", "build": build,
    "accepted_artifacts": [pin(source), pin(accepted / "TimeGravitonMatrix.olean"),
        pin(accepted / "BUILD.log"), pin(accepted / "STDOUT.log"), pin(accepted / "RECEIPT.json"),
        pin(BASE / "SOURCES_R1.json"), pin(BASE / "RELATORIO_MATRIX_R1.md"), pin(Path(__file__))],
    "declarations_count": len(requested), "declarations": axioms,
    "sorry_admit_or_axiom_declarations": 0, "scope": scope,
    "canonical_source_hashes_unchanged": originals,
    "warning_count": stdout.count(": warning:"), "attempt_history": attempts,
    "production_or_kernel_writes": False,
    "independent_review": "Pending coordination; builder receipt is not independent review.",
}
fresh(BASE / "FINAL_MATRIX_RECEIPT_R1.json", (json.dumps(receipt, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))
print(json.dumps({"receipt": pin(BASE / "FINAL_MATRIX_RECEIPT_R1.json"), "source": pin(source),
                  "olean": pin(accepted / "TimeGravitonMatrix.olean"), "count": len(requested)}, ensure_ascii=False))
