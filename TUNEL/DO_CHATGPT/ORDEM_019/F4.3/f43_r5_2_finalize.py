"""Write-once F4.3 R5.2 evidence and map input. Does not register or open data."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R5_RESULT = ROOT / "RESULTADO_F43_R5_20261008.json"
R51_RESULT = ROOT / "RESULTADO_F43_R5_1_20261008.json"
SPEC = ROOT / "PREREGISTRO_F4_3_V4_R5_20261008.json"
MAP_LOG = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
RESULT = ROOT / "RESULTADO_F43_R5_2_20261008.json"
MAP_INPUT = ROOT / "MAPA_F43_R5_2_20261008.json"
def pinned(path: Path) -> dict:
    body = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest()}
def write_once(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

r5 = json.loads(R5_RESULT.read_text(encoding="utf-8"))
r51 = json.loads(R51_RESULT.read_text(encoding="utf-8"))
spec = json.loads(SPEC.read_text(encoding="utf-8"))
for reference in r5["artifacts"] + r51["artifacts"] + r51["sources"]:
    path = Path(reference["path"])
    assert pinned(path)["sha256"] == reference["sha256"], path
v1 = spec["sources"]["V1"]
assert pinned(Path(v1["path"]))["sha256"] == v1["sha256"]
test_path = ROOT / "F43_R5_2_SYNTHETIC_SELFTEST_20261008.json"
test = json.loads(test_path.read_text(encoding="utf-8"))
assert test["n_checks"] == 16
assert test["r5_2_verdict_sha256"] == pinned(ROOT / "f43_r5_2_verdict.py")["sha256"]
assert test["r5_2_gate_sha256"] == pinned(ROOT / "f43_r5_2_calibrated_gate.py")["sha256"]
seq930 = json.loads(MAP_LOG.read_text(encoding="utf-8").splitlines()[929])
assert seq930["seq"] == 930 and seq930["tipo"] == "ERRATA" and seq930["corrige"] == 928
assert seq930["rota_id"] == "ringdown.modo_unico.degenerescencia"
new_names = (
    "f43_r5_2_verdict.py", "f43_r5_2_calibrated_gate.py",
    "f43_r5_2_selftest.py", "F43_R5_2_SYNTHETIC_SELFTEST_20261008.json",
    "ADENDO_F43_R5_2_TOKENS_20261008.md", "f43_r5_2_finalize.py",
)
result = {
    "unit": "F4.3", "layer": "R5.2", "author": "codex-gerente-tgl",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "ENTREGUE_PARA_AUDITORIA__AWAITING_POWER",
    "claim_event": 528,
    "nos_vivo": "F4.3 consulted before production; V1 ramo B, C7, R5 and R5.1 reused",
    "sources": [pinned(R5_RESULT), pinned(R51_RESULT), pinned(SPEC), pinned(Path(v1["path"]))],
    "map_seq930_before": {"seq": seq930["seq"], "sha256": seq930["sha"],
                           "tipo": seq930["tipo"], "corrige": seq930["corrige"]},
    "artifacts": [pinned(ROOT / name) for name in new_names],
    "synthetic_checks": test["n_checks"],
    "material_fixes": [
        "V1 POWER_0P2_OF_5_SIGMA house notation accepted",
        "bare NOT_FALSIFIED_UNDERPOWERED refused",
        "local diagnostic n<10 carries INSUFFICIENT_SAMPLE",
        "full-prefix and composed V1 tokens refused with documented atomic-token contract",
    ],
    "exact_injections_run": False, "observational_data_opened": False,
    "production_receipts_available": 0, "operator_request": "SUSPENDED",
    "gate_moved": False, "memory_touched": False, "bancada_touched": False,
}
write_once(RESULT, result)
artifacts = [str(RESULT), str(ROOT / "ADENDO_F43_R5_2_TOKENS_20261008.md")]
shared = {
    "rota_id": "ringdown.modo_unico.degenerescencia", "dominio": "RINGDOWN",
    "estatuto": "REAL", "status": "EXAMINADA_COM_DEFEITO",
    "olhou_dados": False, "onde": str(ROOT),
    "refs": ["ringdown.ramo_b_preregistro_v386"],
    "nao_refazer": "V1, C7, R5 e R5.1 preservados por hash; só camadas ao lado",
    "proximo_passo": "Levantamento ADENDO 001 antes da campanha de injeções exatas; pedido ao operador suspenso",
}
map_rows = [
    {**shared, "tipo": "ERRATA", "corrige": 930,
     "titulo": "F4.3 seq 930: R5.1 é camada aditiva",
     "pergunta": "A classificação ERRATA da seq 930 expressa o papel da R5.1?",
     "metodo": "Leitura da seq 930 e do resultado R5.1 pinado",
     "resultado": "A R5.1 é uma camada nova de calibração; a classificação documental correta é RESULTADO. A seq 930 permanece intacta.",
     "veredito": "SEQ930_CLASSIFICATION_CORRECTED_ALONGSIDE",
     "defeito": "Seq 930 traz tipo ERRATA e corrige 928 para camada aditiva",
     "artefatos": artifacts},
    {**shared, "tipo": "RESULTADO",
     "titulo": "F4.3 R5.2: token V1 em notação P e amostra insuficiente",
     "pergunta": "A interface aceita a grafia V1 POWER_0P2 e recusa tokens incompletos sem abrir dados?",
     "metodo": "Cópias novas do veredito e gate R5.1, 16 testes sintéticos, pins de fontes",
     "resultado": "Aceita P, recusa UNDERPOWERED sem sufixo e prefixos compostos, marca n<10; produção segue sem os sete recibos.",
     "veredito": "F43_R5_2_SYNTHETIC_CONTRACT__AWAITING_POWER__NO_DATA_OPENED__GATE_NONE",
     "defeito": "Campanha exata, full IMR e recibos de produção ainda ausentes",
     "artefatos": artifacts + [str(ROOT / name) for name in new_names[:4]]},
]
write_once(MAP_INPUT, map_rows)
print(json.dumps({"result": pinned(RESULT), "map_input": pinned(MAP_INPUT),
                  "synthetic_checks": test["n_checks"]}, ensure_ascii=False))