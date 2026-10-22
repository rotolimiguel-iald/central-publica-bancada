"""Seal the bounded F3.6 preparation without reading observational data."""

from datetime import datetime
import hashlib
import json
from pathlib import Path

base = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.6")
worker = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\d1_camb\v3\tgl_camb_worker_v3.py")
pipeline = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\d1_camb\v3\d1_v3_pipeline.py")
manifest = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\d1_camb\v3\MANIFESTO_D1_V3.json")
sources = [
    worker, pipeline, manifest,
    Path(r"C:\IALD\Central de Patentes\work\qg_o_que_falta_20260922\SINTESE.md"),
    Path(r"C:\IALD\Central de Patentes\work\qg_o_que_falta_20260922\MAPA_VERIFICADO_COM_CETICOS.txt"),
    Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_019_ADENDO_003_programa_rebaseado.md"),
    Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_019_ADENDO_004_correcoes_do_critico.md"),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


selftest = json.loads((base / "SELFTEST.json").read_text(encoding="utf-8-sig"))
assert selftest["all_passed"] is True
assert selftest["physical_asimov_run"] is False
assert selftest["observational_data_opened"] is False
historical = json.loads(manifest.read_text(encoding="utf-8"))
assert sha(worker) == historical["arquivos"][worker.name]
assert sha(pipeline) == historical["arquivos"][pipeline.name]

pins = [{"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)} for p in sources]
local = [base / n for n in ("PRE_REGISTRO_CONDICIONAL.md", "portao_poder.py", "SELFTEST.json")]
pins += [{"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)} for p in local]
result = {
    "unit": "F3.6",
    "created_at": datetime.now().astimezone().isoformat(),
    "status": "AGUARDA_OPERADOR",
    "veredito": "F36_CONDITIONAL_PREREG_AND_PURE_GATE_READY__FOUR_MODEL_INPUTS_PENDING__NO_PHYSICAL_ASIMOV__NO_OBSERVED_DATA",
    "estatutos": {"existing_route": "REAL_DOCUMENTAL", "power_gate": "REAL_LOGICAL_SELFTEST",
                  "cpl_physics": "INPUT_PENDING", "sigma_beta_marginalized": "NOT_MEASURED"},
    "already_exists": ["d1.controle2_w0wa seq 52", "D1 V3 original worker and injection",
                       "C16 synopsis and skeptical correction", "control 1 jackknife"],
    "pending_model_inputs": ["CPL contribution to total Phi", "phantom crossing absolute-value rule",
                             "primitive boundary and H0 closure", "w0/wa priors and off-Lambda fiducials"],
    "power_rule": "sigma(beta|w0,wa) >= ALPHA_FINE_CODATA_2018*sqrt(e) -> UNDERPOWERED_DO_NOT_OPEN_DATA",
    "power_ratio": None,
    "physical_asimov_executed": False,
    "injection_recovery_executed": False,
    "observational_data_opened": False,
    "criterion_of_board_met": False,
    "originals_modified": False,
    "source_pins": pins,
    "next_step": "Operator fixes four model inputs; then freeze and hash CPL worker, run synthetic injection/Asimov in sandbox, apply pre-data gate; observed-data opening remains a separate operator act.",
}
out = base / "RESULTADO.json"
assert not out.exists()
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
pins.append({"path": str(out), "bytes": out.stat().st_size, "sha256": sha(out)})
hashes = base / "HASHES.json"
assert not hashes.exists()
hashes.write_text(json.dumps({"unit": "F3.6", "pins": pins}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"result": str(out), "result_sha256": sha(out),
                  "hashes": str(hashes), "hashes_sha256": sha(hashes),
                  "sources": len(sources), "selftest_cases": len(selftest["cases"])}, ensure_ascii=False))
