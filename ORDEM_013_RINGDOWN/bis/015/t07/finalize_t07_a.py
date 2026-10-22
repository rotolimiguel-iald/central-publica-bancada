"""Audit the four source-free local T07(a) searches without promoting them to z."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
START = json.loads((ROOT / "T07_START.json").read_bytes())
REG_BYTES = (ROOT / "T07_REGISTRATION.json").read_bytes()
REG = json.loads(REG_BYTES)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(ROOT / "source_free_local.py") == REG["runner_sha256"]
assert sha(ROOT / "T07_REGISTRATION.json") == START["registration_sha256"]
names = ("R_B", "R_MOD", "R_RAIZ_0", "R_LIN")
rows = []
for name in names:
    path = ROOT / "results" / (name + ".json")
    result = json.loads(path.read_bytes())
    assert result["reading"].replace("-", "_") == name
    assert result["registered_sha256"] == START["registration_sha256"]
    assert result["evaluations"] == 501
    assert result["invalid_evaluations"] == 0
    assert all(not stage["success"] for stage in result["stages"])
    assert all(control["finite"] for control in result["controls"])
    assert result["best"]["coordinates"] is not None
    rows.append({
        "reading": result["reading"],
        "result_sha256": sha(path),
        "evaluations": result["evaluations"],
        "optimizer_converged": False,
        "candidate_residual_norm_8192": result["controls"][0]["candidate_residual_norm"],
        "candidate_residual_norm_16384": result["controls"][1]["candidate_residual_norm"],
        "a0_same_source_squared_residual": result["a0_same_source_squared_residual"],
        "wall_seconds": result["wall_seconds"],
    })

started = datetime.fromisoformat(START["registered_utc"].replace("Z", "+00:00"))
ended = datetime.fromtimestamp(
    (ROOT / "results" / "R_LIN.json").stat().st_mtime, tz=timezone.utc
)
elapsed = (ended - started).total_seconds()
assert 0 < elapsed < START["hardcap_wall_seconds"]
assert len(rows) == 4
report = {
    "status": "T07_A_MEDIDA_PARTIAL_LOCAL_CONSTRUCTIVE_SEARCH",
    "statute": "REAL_FOR_LOCAL_NUMBERS_OPEN_FOR_Z_FREE_AND_PHYSICAL_INFERENCE",
    "started_utc": started.isoformat(),
    "ended_utc_from_last_output_mtime": ended.isoformat(),
    "machine_hours_conservative_start_to_last_output": elapsed / 3600,
    "runner_sha256": sha(ROOT / "source_free_local.py"),
    "registration_sha256": sha(ROOT / "T07_REGISTRATION.json"),
    "log_sha256": sha(ROOT / "T07_RUN_v2.log"),
    "python_environment": "/opt/pycbc_env/bin/python; pre-run /opt/lal_env failed missing pycbc",
    "python_exit_code": 0,
    "rows": rows,
    "meaning": "Each valid a=0 source candidate bounds the global minimum residual from above for the pinned 8192 objective; 16384 is a numerical sensitivity check. No optimizer converged.",
    "a0_control": "Same-source a=0 against a=0, squared residual; not a free-source search.",
    "missing_acceptance": ["converged or certified z_free", "calibrated physical significance", "T07(b) public-strain rho table"],
    "gate_changed": False,
}
target = ROOT / "T07_A_RESULT.json"
raw = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
assert sha(target) == hashlib.sha256(raw).hexdigest()

lines = [
    "[REAL — medição local; OPEN — z_free e inferência física]",
    "",
    "# ORDEM 015, T07(a): busca de fonte livre",
    "",
    "Quatro leituras concluíram com rc 0 e candidatos finitos. Nenhuma das oito etapas Powell convergiu: todas atingiram maxfev. O valor é a norma residual de um candidato a=0 contra o alvo a=1 na fonte registrada, SEOBNRv4HM/O4/SNR40; é limite superior construtivo do mínimo global do objetivo numérico, não limite inferior, z calibrado, exclusão de GR ou σ. O controle a=0/a=0 é na mesma fonte e está ao quadrado; não se compara diretamente às normas da tabela.",
    "",
    "| Leitura | Norma 8192 | Norma 16384 | Avaliações | Convergência | SHA256 resultado |",
    "|---|---:|---:|---:|---|---|",
]
for row in rows:
    lines.append(
        f"| {row['reading']} | {row['candidate_residual_norm_8192']:.9g} | "
        f"{row['candidate_residual_norm_16384']:.9g} | {row['evaluations']} | NÃO | "
        f"`{row['result_sha256']}` |"
    )
lines += [
    "",
    f"Tempo de máquina conservador: {elapsed / 3600:.6f} h, do recibo de início ao último arquivo. Log `T07_RUN_v2.log`: `{report['log_sha256']}`. Runner: `{report['runner_sha256']}`. Registro: `{report['registration_sha256']}`. JSON consolidado: `{sha(target)}`.",
    "",
    "O teto de uma hora foi respeitado por controle externo de timeout. O hash do runner foi conferido depois da execução. O revisor Kimi fez análise estática do texto apresentado; seu parecer não executa nem prova o cálculo. Sem T07(b), a tabela de ρ dos eventos de calibração e o N₉₀ recalculado continuam pendentes. Gate inalterado.",
    "",
]
handoff = ROOT.parents[3] / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_MEDIDA_T07_A_fonte_livre.md"
with handoff.open("xb") as handle:
    handle.write("\n".join(lines).encode())
print(json.dumps({"result": str(target), "result_sha256": sha(target), "handoff": str(handoff), "handoff_sha256": sha(handoff), "machine_hours": elapsed / 3600}))
