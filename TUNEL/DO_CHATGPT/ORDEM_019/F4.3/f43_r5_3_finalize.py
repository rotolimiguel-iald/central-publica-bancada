"""Write-once R5.3 receipt and map input, reading pins from files."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R52 = ROOT / "RESULTADO_F43_R5_2_20261008.json"
SPEC = ROOT / "PREREGISTRO_F4_3_V4_R5_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3\AUDITORIA_F4_3_C1_a47334e0.md")
MAP_LOG = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
RESULT = ROOT / "RESULTADO_F43_R5_3_20261008.json"
MAP_INPUT = ROOT / "MAPA_F43_R5_3_20261008.json"

def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}
def write_once(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

r52 = json.loads(R52.read_text(encoding="utf-8"))
for reference in r52["sources"] + r52["artifacts"]:
    assert pin(Path(reference["path"]))["sha256"] == reference["sha256"], reference["path"]
spec = json.loads(SPEC.read_text(encoding="utf-8"))
v1 = spec["sources"]["V1"]
assert pin(Path(v1["path"]))["sha256"] == v1["sha256"]
test_path = ROOT / "F43_R5_3_SYNTHETIC_SELFTEST_20261008.json"
test = json.loads(test_path.read_text(encoding="utf-8"))
assert test["n_checks"] == 24
assert test["r5_3_verdict_sha256"] == pin(ROOT / "f43_r5_3_verdict.py")["sha256"]
assert test["r5_3_gate_sha256"] == pin(ROOT / "f43_r5_3_calibrated_gate.py")["sha256"]
cache_path = ROOT / "CACHE_F43_R5_3_REMOVAL_20261008.json"
cache = json.loads(cache_path.read_text(encoding="utf-8"))
assert cache["files_removed"] == 2 and not cache["after_exists"]
assert all(item["path"].endswith(".pyc") for item in cache["before"])
assert not (ROOT / "__pycache__").exists()
seq948 = json.loads(MAP_LOG.read_text(encoding="utf-8").splitlines()[947])
assert seq948["seq"] == 948 and seq948["tipo"] == "RESULTADO"
assert seq948["rota_id"] == "ringdown.modo_unico.degenerescencia"

names = (
    "f43_r5_3_verdict.py", "f43_r5_3_calibrated_gate.py",
    "f43_r5_3_selftest.py", "F43_R5_3_SYNTHETIC_SELFTEST_20261008.json",
    "CACHE_F43_R5_3_REMOVAL_20261008.json",
    "ADENDO_F43_R5_3_ASCII_CACHE_20261008.md",
    "f43_r5_3_finalize.py",
)
result = {
    "unit": "F4.3", "layer": "R5.3", "author": "codex-gerente-tgl",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "ENTREGUE_PARA_AUDITORIA__AWAITING_POWER",
    "claim_event": 554,
    "nos_vivo": "F4.3 consulted before production; V1 ramo B, C7, R5/R5.1/R5.2 reused",
    "sources": [pin(R52), pin(SPEC), pin(Path(v1["path"])), pin(AUDIT)],
    "map_seq948_before": {"seq": seq948["seq"], "sha256": seq948["sha"]},
    "artifacts": [pin(ROOT / name) for name in names],
    "synthetic_checks": test["n_checks"],
    "material_fix": "POWER numeric token is canonical ASCII: [0-9] with re.ASCII and no leading integer zero",
    "cache_generated_pyc_removed": cache["files_removed"],
    "exact_injections_run": False, "observational_data_opened": False,
    "production_receipts_available": 0, "operator_request": "SUSPENDED",
    "gate_moved": False, "memory_touched": False, "bancada_touched": False,
}
write_once(RESULT, result)
row = {
    "tipo": "RESULTADO", "rota_id": "ringdown.modo_unico.degenerescencia",
    "dominio": "RINGDOWN", "titulo": "F4.3 R5.3: poder ASCII canônico e cache gerado removido",
    "pergunta": "A regex do poder recusa Unicode e zeros à esquerda preservando POWER_0P2?",
    "metodo": "Variante nova do gate/veredito R5.2, 24 testes sintéticos, pinos de fontes e inventário do cache",
    "resultado": "POWER_0P2 aceito; Unicode e zeros à esquerda recusados; dois .pyc gerados inventariados e removidos.",
    "veredito": "F43_R5_3_SYNTHETIC_CONTRACT__AWAITING_POWER__NO_DATA_OPENED__GATE_NONE",
    "estatuto": "REAL", "status": "EXAMINADA_COM_DEFEITO", "olhou_dados": False,
    "defeito": "Poder exato, full IMR e recibos de produção ainda ausentes",
    "nao_refazer": "V1, C7 e camadas R5/R5.1/R5.2 preservadas por hash",
    "proximo_passo": "Levantamento ADENDO 001 antes de injeções; pedido ao operador suspenso",
    "onde": str(ROOT),
    "artefatos": [str(RESULT)] + [str(ROOT / name) for name in names],
    "refs": ["ringdown.ramo_b_preregistro_v386"],
}
write_once(MAP_INPUT, row)
print(json.dumps({"result": pin(RESULT), "map_input": pin(MAP_INPUT),
                  "n_checks": test["n_checks"]}, ensure_ascii=False))