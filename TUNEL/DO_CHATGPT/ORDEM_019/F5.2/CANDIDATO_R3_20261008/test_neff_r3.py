"""Focused checks for F5.2 R3's pinned Table 5 reader."""
from pathlib import Path
import hashlib
import neff_canal as n

expected = {
    ("v1", "BBN_CONSISTENCY"): (2.81, 0.12, 0.12),
    ("v1", "FREE"): (2.99, 0.22, 0.26),
    ("v2", "BBN_CONSISTENCY"): (2.82, 0.12, 0.12),
    ("v2", "FREE"): (2.96, 0.21, 0.24),
}
rows = n.opcoes_yp_v1_v2()
assert len(rows) == 4
assert {(r["version"], r["yp"]):
        (r["N_eff_obs"], r["sigma_plus"], r["sigma_minus"])
        for r in rows} == expected
assert all(r["cell_id"] and r["source_sha256"] for r in rows)
print("PASS four CMB-SPA cells extracted from pinned v1/v2 MathML")

result = n.canal()
assert result["opcoes_CMB_SPA_Yp_v1_v2"] == rows
assert result["opcoes_CMB_SPA_Yp"] == [r for r in rows if r["version"] == "v2"]
assert 2.97 not in [r["N_eff_obs"] for r in result["medidas"]]
assert "OPEN" in result["escolha_Yp"]
assert result["source_admission"] == "D8_PENDING"
assert result["candidate_state"] == "SANDBOX_ONLY_NOT_INSTALLED"
print("PASS R2 calculation reused, wrong CMB-SPA row excluded, X16/D8 open")

try:
    n.extract_table5("v2", Path(__file__))
except ValueError as exc:
    assert "SHA-256 divergente" in str(exc)
else:
    raise AssertionError("wrong source bytes were accepted")
print("PASS source-byte mismatch fails closed")

try:
    n.extract_table5("v3")
except ValueError as exc:
    assert "Only pinned" in str(exc)
else:
    raise AssertionError("unpinned version was accepted")
print("PASS unpinned version fails closed")

for version, (path, pin) in n.PAGES.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pin
assert hashlib.sha256(n.R2.read_bytes()).hexdigest() == n.R2_SHA256
print("PASS R2 candidate and both source files remain pinned")