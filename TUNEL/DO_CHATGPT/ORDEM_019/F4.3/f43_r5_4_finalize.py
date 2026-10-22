"""Write-once F4.3 R5.4 evidence and map input from verified bytes."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R53 = ROOT / "RESULTADO_F43_R5_3_20261008.json"
SPEC = ROOT / "PREREGISTRO_F4_3_V4_R5_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3\AUDITORIA_F4_3_C1_a9f3787c.md")
MAP_LOG = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
RESULT = ROOT / "RESULTADO_F43_R5_4_20261008.json"
MAP_INPUT = ROOT / "MAPA_F43_R5_4_20261008.json"
def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}
def write_once(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

r53 = json.loads(R53.read_text(encoding="utf-8"))
for reference in r53["sources"] + r53["artifacts"]:
    assert pin(Path(reference["path"]))["sha256"] == reference["sha256"], reference["path"]
spec = json.loads(SPEC.read_text(encoding="utf-8"))
v1 = spec["sources"]["V1"]
assert pin(Path(v1["path"]))["sha256"] == v1["sha256"]
test_path = ROOT / "F43_R5_4_SYNTHETIC_SELFTEST_20261008.json"
test = json.loads(test_path.read_text(encoding="utf-8"))
assert test["n_checks"] == 30
assert test["r5_4_verdict_sha256"] == pin(ROOT / "f43_r5_4_verdict.py")["sha256"]
assert test["r5_4_gate_sha256"] == pin(ROOT / "f43_r5_4_calibrated_gate.py")["sha256"]
assert not (ROOT / "__pycache__").exists()
seq957 = json.loads(MAP_LOG.read_text(encoding="utf-8").splitlines()[956])
assert seq957["seq"] == 957 and seq957["tipo"] == "RESULTADO"
assert seq957["rota_id"] == "ringdown.modo_unico.degenerescencia"
names = (
    "f43_r5_4_verdict.py", "f43_r5_4_calibrated_gate.py",
    "f43_r5_4_selftest.py", "F43_R5_4_SYNTHETIC_SELFTEST_20261008.json",
    "ADENDO_F43_R5_4_NOTACAO_P_20261008.md", "f43_r5_4_finalize.py",
)
result = {
    "unit": "F4.3", "layer": "R5.4", "author": "codex-gerente-tgl",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "ENTREGUE_PARA_AUDITORIA__AWAITING_POWER",
    "claim_event": 570,
    "nos_vivo": "F4.3 consulted before production; V1, C7, R5 through R5.3 reused",
    "sources": [pin(R53), pin(SPEC), pin(Path(v1["path"])), pin(AUDIT)],
    "map_seq957_before": {"seq": seq957["seq"], "sha256": seq957["sha"]},
    "artifacts": [pin(ROOT / name) for name in names],
    "synthetic_checks": 30,
    "material_fix": "atomic POWER only ASCII P notation with exactly one fractional digit",
    "exact_injections_run": False, "observational_data_opened": False,
    "production_receipts_available": 0, "operator_request": "SUSPENDED",
    "gate_moved": False, "memory_touched": False, "bancada_touched": False,
}
write_once(RESULT, result)
row = {
    "tipo": "RESULTADO", "rota_id": "ringdown.modo_unico.degenerescencia",
    "dominio": "RINGDOWN", "titulo": "F4.3 R5.4: token POWER só P com uma casa decimal",
    "pergunta": "A interface R5.4 recusa ponto e duas casas preservando o exemplo 0P2 do V1?",
    "metodo": "Variante nova do gate/veredito R5.3, 30 testes sintéticos, pinos de fontes",
    "resultado": "0P2 e 4P9 aceitos; 4.9 e 4P09 recusados; Unicode e zeros iniciais seguem recusados.",
    "veredito": "F43_R5_4_SYNTHETIC_CONTRACT__AWAITING_POWER__NO_DATA_OPENED__GATE_NONE",
    "estatuto": "REAL", "status": "EXAMINADA_COM_DEFEITO", "olhou_dados": False,
    "defeito": "Poder exato, full IMR e recibos de produção ainda ausentes",
    "nao_refazer": "V1, C7 e R5/R5.1/R5.2/R5.3 preservados por hash",
    "proximo_passo": "Levantamento ADENDO 001 antes de injeções; pedido ao operador suspenso",
    "onde": str(ROOT),
    "artefatos": [str(RESULT)] + [str(ROOT / name) for name in names],
    "refs": ["ringdown.ramo_b_preregistro_v386"],
}
write_once(MAP_INPUT, row)
print(json.dumps({"result": pin(RESULT), "map_input": pin(MAP_INPUT),
                  "n_checks": test["n_checks"]}, ensure_ascii=False))