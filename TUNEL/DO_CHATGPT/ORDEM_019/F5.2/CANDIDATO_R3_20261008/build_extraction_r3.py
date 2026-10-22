"""Write a fresh, read-only-source extraction receipt for F5.2 R3."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import neff_canal as n

HERE = Path(__file__).resolve().parent
FROZEN = Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py")
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.6.E1\AUDITORIA_F3_6_E1_C1_a4f6da3d.md")
TEST = HERE / "test_neff_r3.py"
CODE = HERE / "neff_canal.py"
LOG = HERE / "TESTES_R3_20261008.log"
OUT = HERE / "EXTRACAO_TABELA5_R3_20261008.json"


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exclusive(p: Path, data: bytes) -> None:
    with p.open("xb") as f:
        f.write(data)
        f.flush()
    if p.read_bytes() != data:
        raise RuntimeError(f"written bytes differ: {p}")


run = subprocess.run([sys.executable, "-B", "-X", "utf8", str(TEST)],
                     capture_output=True, text=True, encoding="utf-8", check=False)
log = (f"command: {sys.executable} -B -X utf8 {TEST}\n"
       f"exit_code: {run.returncode}\nstdout:\n{run.stdout}stderr:\n{run.stderr}")
exclusive(LOG, log.encode("utf-8"))
if run.returncode != 0:
    raise SystemExit(run.returncode)
rows = n.opcoes_yp_v1_v2()
output = n.canal()
receipt = {
    "unit": "F5.2", "layer": "R3_20261008", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "status": "SANDBOX_CANDIDATE__NOT_INSTALLED__D8_X16_OPEN__GATE_UNTOUCHED",
    "existing_from_nos_vivo": ["08/08 N_eff calendar and frozen", "Fase 8 V1", "SO 2.655", "F5.2 R2 candidate audited with caveats"],
    "audit_source": {"path": str(AUDIT), "sha256": digest(AUDIT), "finding": "v1 beside v2, extract v2 values from pinned bytes, errata on seq 606/607/618/843"},
    "sources": [
        {"version": ver, "url": f"https://arxiv.org/html/2506.20707{ver}",
         "anchor": "Table 5, section VII.2.4, CMB-SPA column; official arXiv page independently checked",
         "custody_path": str(path), "custody_sha256": digest(path),
         "note": "Local cached HTML byte pin; no assertion of byte identity with live arXiv page"}
        for ver, (path, _pin) in n.PAGES.items()
    ],
    "extracted_rows": rows,
    "old_line": "2.97 ± 0.12 CMB-SPA in frozen line 46 and V1 JSON line 136 is a mixed non-existent Table 5 row; v1 2.97 +0.40/-0.64 is SPT-3G D1 alone with free Yp",
    "sealed_artefacts_unchanged": [
        {"path": str(FROZEN), "sha256": digest(FROZEN)},
        {"path": str(V1), "sha256": digest(V1)}
    ],
    "candidate": {"path": str(CODE), "sha256": digest(CODE),
                  "r2_path": str(n.R2), "r2_sha256": digest(n.R2)},
    "tests": {"path": str(TEST), "sha256": digest(TEST), "log_path": str(LOG),
              "log_sha256": digest(LOG), "exit_code": run.returncode,
              "checks": 5},
    "channel_checks": {"delta_N_eff": output["delta_N_eff"],
                       "beta_runtime": output["beta_runtime"],
                       "bad_line_excluded_from_measures": all(x["N_eff_obs"] != 2.97 for x in output["medidas"]),
                       "choice_Yp": output["escolha_Yp"],
                       "source_admission": output["source_admission"]},
    "limits": ["No Yp choice", "No D8 admission", "No source or frozen edit", "No Bancada installation", "No nature-data opening", "No gate change"]
}
exclusive(OUT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"extraction_path": str(OUT), "extraction_sha256": digest(OUT),
                  "candidate_sha256": digest(CODE), "tests_exit": run.returncode,
                  "frozen_sha256": digest(FROZEN), "v1_sha256": digest(V1)}, ensure_ascii=False))