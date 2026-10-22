"""Seal the additive F3.2 byte-lineage evidence without overwriting prior pins."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.2\AUDITORIA_F3_2_C1_a9f3787c.md")
NAMES = [
    "build_f32_r52_bytes_20261008.py",
    "VINCULO_DOCUMENTAL_V1X_R52_BYTES_20261008.json",
    "f9_reader_gate_v1x_r52_bytes.py",
    "f9_runner_v1x_preflight_r52_bytes.py",
    "f9_runner_v1x_staged_r52_bytes.py",
    "test_f9_v1x_r52_bytes_20261008.py",
]
def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
command = [sys.executable, "-B", "-X", "utf8", str(HERE / NAMES[-1])]
start = datetime.now(timezone.utc)
t0 = time.perf_counter()
run = subprocess.run(command, cwd=HERE, capture_output=True, text=True, encoding="utf-8")
seconds = time.perf_counter() - t0
end = datetime.now(timezone.utc)
log = (
    "F3.2 R5.2 byte-lineage synthetic test\n"
    f"start_utc={start.isoformat()}\nend_utc={end.isoformat()}\n"
    f"seconds={seconds:.6f}\npython={sys.version}\n"
    f"command={json.dumps(command, ensure_ascii=False)}\n"
    f"cwd={HERE}\nexit_code={run.returncode}\n"
    "stdout:\n" + run.stdout + "\nstderr:\n" + run.stderr
)
log_path = HERE / "TESTE_F32_R52_BYTES_20261008.log"
with log_path.open("x", encoding="utf-8", newline="\n") as f:
    f.write(log)
if run.returncode != 0 or "Ran 5 tests" not in log or "\nOK" not in log:
    raise SystemExit("synthetic validation failed; log retained")
artifacts = [pin(HERE / n) for n in NAMES] + [pin(log_path)]
binding = json.loads((HERE / NAMES[1]).read_bytes())
result = {
    "schema": "F32_R52_BYTE_LINEAGE_PORTABLE_V1",
    "unit": "F3.2",
    "status": "ENTREGUE_PARA_AUDITORIA_C1",
    "audit_base": pin(AUDIT),
    "nos_vivo": "consultar.py --unidade F3.2 executado antes da producao; reutilizados R4/F3.4, R5/R5.1/R5.2, gate, runner e fontes ja pinadas",
    "ancestor_pins": binding["r52_ancestor_files"],
    "binding_sha256": artifacts[1]["sha256"],
    "spec_sha256": "9c7f05a1821ccb88936c0190934db524f4dca1de20ab2c98c5206a4c157cbb7c",
    "function_sha256": "544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5",
    "new_artifacts": artifacts,
    "test": {
        "count": 5, "passed": 5, "exit_code": run.returncode,
        "full_bundle_relocated": True,
        "each_ancestor_mutation_refused": True,
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
    "note": "Metadados conservam caminhos documentais historicos; toda leitura de arquivo e mapeada sob a raiz do pacote atual. Nenhum valor observado compoe a estatistica. NOT_FALSIFIED nunca e CONFIRMED.",
}
result_path = HERE / "RESULTADO_F32_R52_BYTES_20261008.json"
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
    "titulo": "F3.2 R5.2: releitura dos ancestrais e relocacao integral do pacote",
    "pergunta": "O gate relê bytes de F3.4, R5, R5.1 e R5.2 e conserva a recusa após mover o pacote?",
    "dados": ["quatro ancestrais pinados por bytes/hash", "vinculo e fontes ORDEM_018", "fixture sintetico"],
    "metodo": "Gate novo relê cada ancestral, confere sua derivacao, mapeia as leituras para a raiz do vinculo atual e recusa falta ou alteracao de bytes; 5 testes sinteticos",
    "resultado": "5/5 EXIT 0; copia integral deslocada aceita; cada mutacao ancestral e copia parcial recusadas; modo real recusado antes de ler",
    "veredito": "R52_BYTE_LINEAGE_DOCUMENTARY_ONLY__SYNTHETIC_RUNNER__NO_FREEZE_NO_OPENING",
    "defeito": "Ato do operador X13 e D-H seguem pendentes; esta camada aguarda auditoria c1",
    "nao_refazer": "Ancestrais, vinculo R5.2 antigo, gate e runners antigos permanecem intocados",
    "proximo_passo": "c1 reauditar; nenhum dado real, congelamento ou alteracao do gate",
    "olhou_dados": False,
    "onde": str(HERE),
    "artefatos": [str(result_path)] + [x["path"] for x in artifacts],
    "refs": ["d1.fase9.f3_1_semantica_v1x_leitores"],
    "nota": f"RESULTADO sha256 {result_pin['sha256']}; vinculo {artifacts[1]['sha256']}; teste {artifacts[5]['sha256']}; log {artifacts[6]['sha256']}; NOT_FALSIFIED nunca e CONFIRMED",
}]
map_path = HERE / "MAP_ENTRY_F32_R52_BYTES_20261008.json"
with map_path.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(entry, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")
print(json.dumps({"result": result_pin, "map_entry": pin(map_path), "artifacts": artifacts}, ensure_ascii=False))
