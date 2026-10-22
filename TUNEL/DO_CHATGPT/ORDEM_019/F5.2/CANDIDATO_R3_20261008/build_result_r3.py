"""Finalize F5.2 R3 receipt from bytes and verified map entries."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAP = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
TOOL = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
OUT = ROOT / "RESULTADO_F52_R3_20261008.json"
EXTRACT = HERE / "EXTRACAO_TABELA5_R3_20261008.json"
SOURCE = json.loads(EXTRACT.read_text(encoding="utf-8"))


def pin(p):
    p = Path(p)
    raw = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


verify = subprocess.run([sys.executable, "-X", "utf8", str(TOOL), "verificar"],
                        capture_output=True, text=True, encoding="utf-8", check=False)
if verify.returncode != 0:
    raise RuntimeError(verify.stdout + verify.stderr)
verification = json.loads(verify.stdout)
if not verification["ok"]:
    raise RuntimeError("map verification false")
seqs = {882: ("primordial.fase8_era_da_radiacao", 607),
        883: ("primordial.fase8_era_da_radiacao", 618),
        884: ("cmb.neff_e_rho_mais_p", 606),
        885: ("neff.frozen_v1_08ago", 843)}
found = {}
for line in MAP.read_text(encoding="utf-8").splitlines():
    item = json.loads(line)
    if item["seq"] in seqs:
        assert (item["rota_id"], item["corrige"]) == seqs[item["seq"]]
        assert item["tipo"] == "ERRATA"
        found[item["seq"]] = {"seq": item["seq"], "route": item["rota_id"],
                              "corrects": item["corrige"], "entry_sha256": item["sha"]}
assert set(found) == set(seqs)
artifacts = [pin(HERE / name) for name in (
    "neff_canal.py", "test_neff_r3.py", "TESTES_R3_20261008.log",
    "EXTRACAO_TABELA5_R3_20261008.json", "ERRATAS_MAPA_F52_R3_20261008.json",
    "build_extraction_r3.py", "build_map_errata_r3.py", "build_result_r3.py")]
artifacts.extend(pin(p["path"]) for p in SOURCE["sealed_artefacts_unchanged"])
result = {
 "unit": "F5.2", "claim_event": 380, "status": "ENTREGUE_PARA_REAUDITORIA",
 "summary": "CMB-SPA Table 5 v1/v2 cells extracted from pinned primary-source MathML; historical frozen/V1/map corrections appended; candidate sandbox only.",
 "existing_reused": SOURCE["existing_from_nos_vivo"],
 "values": {"v1_BBN": "2.81 ± 0.12", "v1_free_Yp": "2.99 +0.22/-0.26",
            "v2_BBN": "2.82 ± 0.12", "v2_free_Yp": "2.96 +0.21/-0.24"},
 "primary_source_urls": [s["url"] for s in SOURCE["sources"]],
 "source_anchor": "Table 5, section VII.2.4, CMB-SPA column",
 "map": {"verification": verification, "entries": [found[s] for s in sorted(found)]},
 "tests": {"exit_code": SOURCE["tests"]["exit_code"], "checks": SOURCE["tests"]["checks"]},
 "artifacts": artifacts,
 "limits": SOURCE["limits"] + ["R2 source not modified", "No memory surface modified"],
 "pending": ["c1 independent re-audit", "operator X16 Yp choice", "operator D8 source admission", "c1 candidate installation decision"]
}
with OUT.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps({"result_path": str(OUT), "sha256": pin(OUT)["sha256"],
                  "map_entry_shas": [v["entry_sha256"] for v in result["map"]["entries"]]}, ensure_ascii=False))