"""Seal the additive F3.2 E1 byte-lineage evidence; write new paths only."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.2\AUDITORIA_F3_2_C1_a181bf67.md")
E1 = HERE.parent / "F3.1" / "PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"
NAMES = [
    "build_f32_e1_bytes_20261008.py",
    "VINCULO_DOCUMENTAL_V1X_E1_BYTES_20261008.json",
    "f9_reader_gate_v1x_e1_bytes.py",
    "f9_runner_v1x_preflight_e1_bytes.py",
    "f9_runner_v1x_staged_e1_bytes.py",
    "test_f9_v1x_e1_bytes_20261008.py",
]
def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
command = [sys.executable, "-B", "-X", "utf8", str(HERE / NAMES[-1])]
start = datetime.now(timezone.utc)
tic = time.perf_counter()
run = subprocess.run(command, cwd=HERE, capture_output=True, text=True, encoding="utf-8")
seconds = time.perf_counter() - tic
end = datetime.now(timezone.utc)
log = (
    "F3.2 F3.1.E1 projection byte-lineage synthetic test\n"
    f"start_utc={start.isoformat()}\nend_utc={end.isoformat()}\n"
    f"seconds={seconds:.6f}\npython={sys.version}\n"
    f"command={json.dumps(command, ensure_ascii=False)}\n"
    f"cwd={HERE}\nexit_code={run.returncode}\n"
    "stdout:\n" + run.stdout + "\nstderr:\n" + run.stderr
)
log_path = HERE / "TESTE_F32_E1_BYTES_20261008.log"
with log_path.open("x", encoding="utf-8", newline="\n") as f:
    f.write(log)
if run.returncode != 0 or "Ran 5 tests" not in log or "\nOK" not in log:
    raise SystemExit("synthetic validation failed; log retained")
artifacts = [pin(HERE / n) for n in NAMES] + [pin(log_path)]
binding = json.loads((HERE / NAMES[1]).read_bytes())
assert binding["draft_v2"]["sha256"] == pin(E1)["sha256"]
assert binding["spec_sha256"] == "406d9d2dde90d6d250d71938ffbaaf3b881fdd459629630770cdc27c0d52bf58"
result = {
    "schema": "F32_E1_BYTE_LINEAGE_PORTABLE_V1",
    "unit": "F3.2",
    "status": "ENTREGUE_PARA_AUDITORIA_C1",
    "audit_base": pin(AUDIT),
    "nos_vivo": "consultar.py --unidade F3.2 executado antes da producao; reutilizados F3.4/R5/R5.1/R5.2, E1 FECHADA, gate documental, runner e fontes pinadas",
    "projection_e1": pin(E1),
    "ancestor_pins": binding["r52_ancestor_files"],
    "binding_sha256": artifacts[1]["sha256"],
    "spec_sha256": binding["spec_sha256"],
    "function_sha256": "544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5",
    "new_artifacts": artifacts,
    "test": {
        "count": 5, "passed": 5, "exit_code": run.returncode,
        "full_bundle_relocated": True,
        "five_lineage_mutations_refused": True,
        "partial_relocation_refused": True,
        "wrong_source_root_refused": True,
        "real_mode_refused_before_documentary_read": True,
    },
    "boundary": {
        "status": "[REAL] verificacao documental por bytes e ensaio sintetico",
        "source_admission": "[OPEN] D-H",
        "executor_semantics": "[OPEN] X13",
        "v2_frozen": False,
        "data_opened": False,
        "verdict": None,
        "gate_changed": False,
        "memory_changed": False,
        "bancada_changed": False,
    },
    "note": "A spec E1 e pinada por 406d9d2d; a fonte da funcao permanece 544f60ef. A R5.2 antiga 9c7f05a1 segue historica e seus bytes sao relidos. NOT_FALSIFIED nunca e CONFIRMED.",
}
result_path = HERE / "RESULTADO_F32_E1_BYTES_20261008.json"
with result_path.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")
result_pin = pin(result_path)
entry = [{
    "rota_id": "d1.fase9.f3_2_r1_hash_gate",
    "dominio": "D1_FUNDO_COSMOLOGICO",
    "tipo": "RESULTADO",
    "status": "EM_CURSO",
    "estatuto": "REAL documental e sintetico; OPEN D-H, X13 e abertura",
    "titulo": "F3.2: projecao F3.1.E1 ligada por bytes ao gate portatil",
    "pergunta": "O gate usa a spec 406d9d2d da E1 e relê seus bytes com a linhagem historica completa?",
    "dados": ["F3.1.E1 fechada, sha256 81a97092", "F3.4, R5, R5.1 e R5.2 historicos", "fixture sintetico"],
    "metodo": "Novo vinculo e gate pinam E1, relêem cinco arquivos e suas relacoes derived_from, verificam fontes sob raiz deslocada; cinco testes sinteticos",
    "resultado": "5/5 EXIT 0; E1 spec 406d9d2d; cinco mutacoes e relocacao parcial recusadas; modo real recusado",
    "veredito": "E1_BYTE_LINEAGE_DOCUMENTARY_ONLY__SYNTHETIC_RUNNER__NO_FREEZE_NO_OPENING",
    "defeito": "X13 e D-H seguem atos do operador; c1 reaudita esta variante",
    "nao_refazer": "R5.2 antiga, F3.1.E1 e pinos F3.2 anteriores permanecem intactos",
    "proximo_passo": "c1 reauditar; nenhum dado real, congelamento ou mudanca de gate",
    "olhou_dados": False,
    "onde": str(HERE),
    "artefatos": [str(result_path)] + [x["path"] for x in artifacts],
    "refs": ["d1.fase9.f3_1_semantica_v1x_leitores"],
    "nota": f"RESULTADO sha256 {result_pin['sha256']}; vinculo {artifacts[1]['sha256']}; gate {artifacts[2]['sha256']}; teste {artifacts[5]['sha256']}; log {artifacts[6]['sha256']}; NOT_FALSIFIED nunca e CONFIRMED",
}]
map_path = HERE / "MAP_ENTRY_F32_E1_BYTES_20261008.json"
with map_path.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(entry, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")
print(json.dumps({"result": result_pin, "map_entry": pin(map_path), "artifacts": artifacts}, ensure_ascii=False))
