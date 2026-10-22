"""Seal the F1.2 completion in new files without replacing earlier evidence."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


ROOT = Path(__file__).resolve().parent
SANDBOX = ROOT / "sandbox"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F1.2\sandbox\F12Audit\AuditProbe.lean")
P = {
    "new_stone": SANDBOX / "F12Completion" / "AgapeNonVacuity.lean",
    "bridge_copy": SANDBOX / "F12Completion" / "V351DualScalingBridge.lean",
    "bridge_original": SANDBOX / "V351DualScalingBridge.lean",
    "matrix_original": SANDBOX / "MatrixInnerGauge.lean",
    "new_log": SANDBOX / "BUILD_AgapeNonVacuity.log",
    "bridge_log": SANDBOX / "BUILD_V351DualScalingBridge.log",
    "new_olean": SANDBOX / "build" / "F12Completion" / "AgapeNonVacuity.olean",
    "bridge_olean": SANDBOX / "build" / "F12Completion" / "V351DualScalingBridge.olean",
    "build_result": SANDBOX / "BUILD_COMPLETION_RESULT.json",
    "audit_probe": AUDIT,
    "fundacao": NOS / "Fundacao.lean",
    "trace_construction": NOS / "V351RegularCoreTraceConstruction.lean",
    "result_previous": ROOT / "RESULTADO.json",
    "result_first_backup": ROOT / "RESULTADO.json.bak_20261007_202321_641734",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_atomic(path: Path, raw: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"Existing evidence must not be replaced: {path}")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        tmp = Path(stream.name)
    if tmp.stat().st_size != len(raw):
        raise OSError(f"Temporary file truncated: {tmp}")
    os.link(tmp, path)
    tmp.unlink()
    if path.read_bytes() != raw:
        raise OSError(f"Evidence byte mismatch: {path}")


expected = {
    "bridge_original": "7dbe2d9a45971d636f05fac5fdf04dce4d3674a8cbd421fc89fe3e6700b63514",
    "matrix_original": "ab21d46c059fc7e192d682bf38e987c6113dd540d2e1eb5f5e73a7660cac50e9",
    "audit_probe": "408f426d055e6db7c9983b1d5de73d4e3c8fd66ef72c3333dc464af43dea7dcf",
    "fundacao": "66332d58fd216317ec5196a64a7aa670c87dcaa5edc59f57a5506bc621d3e073",
    "trace_construction": "f741525cfa335d89221834fdb01e3f3c6b8efa435b107f0a355cc5679fe06b40",
    "result_previous": "cbb7866c194ddb5079a41fc59fa0b826240cd3469c09d9a48a74a7046ed3c99b",
    "result_first_backup": "e1b5e4d4530818cfd43d60f32cea5310b549adc37bdce1e36a762c6e02f30da6",
}
for label, hash_expected in expected.items():
    actual = digest(P[label])
    if actual != hash_expected:
        raise RuntimeError(f"Changed input {label}: {actual}")
if P["bridge_copy"].read_bytes() != P["bridge_original"].read_bytes():
    raise RuntimeError("The delivered bridge copy is not byte identical")

build = json.loads(P["build_result"].read_text(encoding="utf-8"))
if len(build["steps"]) != 2 or any(step["exit_code"] != 0 for step in build["steps"]):
    raise RuntimeError("Build did not finish successfully")
axiom_log = P["new_log"].read_text(encoding="utf-8")
declarations = ("F12Completion.finiteTracePositive_has_positive", "F12Completion.agape_on_v351_core")
for name in declarations:
    expected_line = f"'{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
    if expected_line not in axiom_log:
        raise RuntimeError(f"Missing exact axiom report: {name}")
if "error:" in axiom_log.lower() or "warning:" in axiom_log.lower():
    raise RuntimeError("Lean reported an error or warning")
for label in ("new_stone", "bridge_copy"):
    if re.search(r"\b(sorry|admit|axiom)\b", P[label].read_text(encoding="utf-8")):
        raise RuntimeError(f"Forbidden token in {label}")

axioms_path = ROOT / "AXIOMAS_FECHO_V351_AGAPE_20261008.txt"
new_atomic(axioms_path, P["bridge_log"].read_bytes() + P["new_log"].read_bytes())

diagnostic_path = ROOT / "DIAGNOSTICO_FECHO_V351_AGAPE_20261008.md"
diagnostic = """# F1.2 — não vacuidade e Fundação no core regular v351

**[REAL]** `F12Completion.finiteTracePositive_has_positive` obtains `A : FiniteTracePositive P` with `0 < tau A` from the v351 trace's semifiniteness and faithfulness. The proof starts with `positiveUnit P` to rule out a zero trace, but the resulting finite-trace witness is **not** the unit: the audit proves the unit has infinite trace and lies outside this subcone.

**[REAL]** `F12Completion.agape_on_v351_core` applies `TGLExt.Fundacao.agape` to `TGLV351.regularCoreDualScalingData P` and that witness. This links the v351 term to the Foundation in the current Nós package. The bridge's `theta` is the dual action and `tau` is the v351 trace, as in the audited previous delivery. The two new theorems compile with only `propext`, `Classical.choice`, and `Quot.sound`.

**[OPEN]** The original criterion's matrix crossed product `M_n ⋊_σ ℝ`, its L² construction, von Neumann closure, and intertwining equivalence are not constructed here. The Agape conclusion applies to the finite-trace positive subcone of the regular core. It does not make the structure `DualScalingData` non-vacuous in arbitrary types; the new witness does so for this instance.

**Custody.** The old bridge has four new declarations, the separate matrix gauge file has six, and this stone adds two theorems. Old files registered as evidence remain unchanged. The previous `RESULTADO.json` and its original backup are separately pinned in the new manifest; this document corrects their descriptions beside them. The source of the auditor's two proven lemmas is credited by its measured hash. Build imports only current Nós kernel caches and reproduces the bridge byte for byte in this sandbox. Neither the Nós source nor `um.py` was modified.
""".encode("utf-8")
new_atomic(diagnostic_path, diagnostic)

files = dict(P)
files.update({"axioms": axioms_path, "diagnostic": diagnostic_path})
manifest = {
    "unit": "F1.2",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "files": {
        label: {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}
        for label, path in files.items()
    },
}
manifest_path = ROOT / "HASHES_FECHO_V351_AGAPE_20261008.json"
new_atomic(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

result = {
    "unit": "F1.2",
    "kind": "FECHO_REBASE_V351_NONVACUITY_FOUNDATION",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "status": "REAL_COMPILED_CONDITIONAL_ON_SITE_PROFILE",
    "theorems": list(declarations),
    "build": {"exit_codes": [0, 0], "lean_version": "4.31.0", "axioms": ["propext", "Classical.choice", "Quot.sound"], "sorry_or_admit_or_new_axiom": False},
    "previous_delivery": {"bridge_declarations": 4, "matrix_declarations": 6, "total_declarations": 10},
    "new_declarations": 2,
    "nonvacuity": "exists finite-trace positive A with tau(A)>0; witness is not the unit",
    "foundation": "Fundacao.agape applied to regularCoreDualScalingData P and the positive witness",
    "scope": "regular v351 finite-trace positive core; matrix crossed product still OPEN",
    "nos_original_changed": False,
    "um_py_changed": False,
    "gate_changed": False,
    "old_evidence_overwritten": False,
    "manifest": {"path": str(manifest_path), "sha256": digest(manifest_path)},
    "diagnostic": {"path": str(diagnostic_path), "sha256": digest(diagnostic_path)},
}
result_path = ROOT / "RESULTADO_FECHO_V351_AGAPE_20261008.json"
new_atomic(result_path, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"result": str(result_path), "result_sha256": digest(result_path), "manifest": str(manifest_path), "manifest_sha256": digest(manifest_path)}, ensure_ascii=False))
