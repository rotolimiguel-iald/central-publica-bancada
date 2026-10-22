"""Create provenance from artifact bytes, never copied or remembered hashes."""
from pathlib import Path
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
CENTRAL = BASE.parents[1]
RUNNER = CENTRAL / "patents/BR102026003450-9_SUPERCONDUTOR/runner"
sources = [(RUNNER / "one_supercondutor.py", "ACOM; H_min=I-q_F; double lock; finite pinching"),
           (RUNNER / "_super_core/skygrid_sim/acom.py", "Canonical square-root/sign reconstruction"),
           (RUNNER / "_super_core/skygrid_sim/tgl_core.py", "Runtime beta=ALPHA_FINE_CODATA_2018*sqrt(e)")]
data = {"scope": "Adaptação computacional finita. Q_admissible mapeia provedores por política nova de engenharia; não é o q_F original. Sem confirmação física, Lean recompilado ou ganho de desempenho medido.",
        "sources": [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "role": role} for p, role in sources]}
target = BASE / "provenance.json"
if target.exists():
    raise SystemExit("Provenance already exists; review changes instead of silently repinning.")
payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
temp = target.with_suffix(".tmp")
temp.write_bytes(payload)
assert temp.read_bytes() == payload
os.replace(temp, target)
print(json.dumps({"sources_read": len(sources), "provenance_bytes": target.stat().st_size}))
