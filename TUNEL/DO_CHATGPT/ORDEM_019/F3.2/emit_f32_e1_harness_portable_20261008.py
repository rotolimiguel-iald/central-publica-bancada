"""Record the portable F3.2 test harness and its measured synthetic run."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.2\AUDITORIA_F3_2_C1_ac633f5a.md")
HARNESS = HERE / "test_f9_v1x_e1_bytes_portable_20261008.py"
PINNED = {
    HERE / "VINCULO_DOCUMENTAL_V1X_E1_BYTES_20261008.json": "f6e7840e28071a524035c49196c989b0fe871ac27685e0f26bac1a7aa24376b6",
    HERE / "f9_reader_gate_v1x_e1_bytes.py": "6e00478c91dc59fe92c72a9deec5dbc3040309043762461cb98aa0e4b237449e",
    HERE / "test_f9_v1x_e1_bytes_20261008.py": "a52deec8df4274663f0aceede3e3e3f669071a2faf4e61fcde7293758b3e592c",
}
def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
for path, digest in PINNED.items():
    if pin(path)["sha256"] != digest:
        raise SystemExit(f"prior pin changed: {path}")
command = [sys.executable, "-B", "-X", "utf8", str(HARNESS)]
before = sorted(p.name for p in Path(tempfile.gettempdir()).glob("f32_e1_bytes_*"))
start = datetime.now(timezone.utc)
tick = time.perf_counter()
run = subprocess.run(command, cwd=HERE, capture_output=True, text=True, encoding="utf-8")
seconds = time.perf_counter() - tick
end = datetime.now(timezone.utc)
after = sorted(p.name for p in Path(tempfile.gettempdir()).glob("f32_e1_bytes_*"))
log = (
    "F3.2 portable harness, synthetic-only\n"
    f"start_utc={start.isoformat()}\nend_utc={end.isoformat()}\n"
    f"seconds={seconds:.6f}\npython={sys.version}\n"
    f"command={json.dumps(command, ensure_ascii=False)}\n"
    f"cwd={HERE}\nexit_code={run.returncode}\n"
    f"temp_residual_before={json.dumps(before)}\n"
    f"temp_residual_after={json.dumps(after)}\n"
    "stdout:\n" + run.stdout + "\nstderr:\n" + run.stderr
)
log_path = HERE / "TESTE_F32_E1_HARNESS_PORTABLE_20261008.log"
with log_path.open("x", encoding="utf-8", newline="\n") as f:
    f.write(log)
if run.returncode != 0 or "Ran 7 tests" not in log or "\nOK" not in log or before != after or after:
    raise SystemExit("portable harness validation failed; log retained")
result = {
    "schema": "F32_E1_PORTABLE_HARNESS_FINAL_V1",
    "unit": "F3.2",
    "status": "ENTREGUE_PARA_AUDITORIA_C1",
    "audit_base": pin(AUDIT),
    "nos_vivo": "consultar.py --unidade F3.2 executado; reutilizados vinculo E1, cinco elos, gate e runner auditados",
    "change_scope": "somente harness novo, log e recibos; nenhum gate, spec, fonte, memoria, Bancada ou dado real editado",
    "harness": pin(HARNESS),
    "test_log": pin(log_path),
    "prior_pins_unchanged": [pin(path) for path in PINNED],
    "checks": {
        "synthetic_tests": 7,
        "passed": 7,
        "exit_code": run.returncode,
        "self_relocation_subprocess": True,
        "failure_before_mkdtemp_no_leak": True,
        "failure_after_mkdtemp_no_leak": True,
        "failure_during_copy_no_leak": True,
        "f32_e1_bytes_temp_residual": after,
        "mutations_refused": 5,
        "partial_relocation_refused": True,
        "real_mode_refused_before_read": True,
    },
    "boundary": {
        "source_admission": "[OPEN] D-H",
        "executor_semantics": "[OPEN] X13",
        "v2_frozen": False,
        "data_opened": False,
        "verdict": None,
        "gate_changed": False,
        "memory_changed": False,
    },
    "note": "Depois desta camada, F3.1/F3.2 aguardam atos do operador X13/D-H; NOT_FALSIFIED nunca e CONFIRMED.",
}
result_path = HERE / "RESULTADO_F32_E1_HARNESS_PORTABLE_20261008.json"
with result_path.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")
result_pin = pin(result_path)
entry = [{
    "rota_id": "d1.fase9.f3_2_r1_hash_gate",
    "dominio": "D1_FUNDO_COSMOLOGICO",
    "tipo": "RESULTADO",
    "status": "EM_CURSO",
    "estatuto": "REAL harness sintetico; OPEN X13 e D-H",
    "titulo": "F3.2: harness E1 relocavel e sem vazamento de TEMP",
    "pergunta": "A suite roda de uma copia deslocada e limpa TEMP inclusive se a montagem falhar?",
    "dados": ["vinculo E1 f6e7840e", "gate E1 6e00478c", "fixture sintetico"],
    "metodo": "Novo harness resolve sufixos ORDEM_018/ORDEM_019 na raiz corrente; mkdtemp sob try/finally; injeta falhas antes, apos e durante copia; executa a si mesmo deslocado",
    "resultado": "7/7 EXIT 0; autoexecucao deslocada passa; zero f32_e1_bytes_* residual; cinco mutacoes recusadas",
    "veredito": "PORTABLE_HARNESS_PASS__NO_TEMP_LEAK__SYNTHETIC_ONLY",
    "defeito": "X13 e D-H seguem atos do operador; nenhuma outra camada F3.1/F3.2 sem despacho",
    "nao_refazer": "Gate, spec, vinculo E1 e harness anterior permanecem pinados",
    "proximo_passo": "c1 reauditar esta ultima camada; aguardar operador para X13/D-H",
    "olhou_dados": False,
    "onde": str(HERE),
    "artefatos": [str(result_path), str(HARNESS), str(log_path)],
    "refs": ["d1.fase9.f3_1_semantica_v1x_leitores"],
    "nota": f"RESULTADO sha256 {result_pin['sha256']}; harness {pin(HARNESS)['sha256']}; log {pin(log_path)['sha256']}; NOT_FALSIFIED nunca e CONFIRMED",
}]
map_path = HERE / "MAP_ENTRY_F32_E1_HARNESS_PORTABLE_20261008.json"
with map_path.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(entry, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")
print(json.dumps({"result": result_pin, "harness": pin(HARNESS), "log": pin(log_path),
                  "map_entry": pin(map_path)}, ensure_ascii=False))
