"""Register T08 partial measured cost; preserve older budget and progress."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
BASE = CHAT / "ORDEM_013_RINGDOWN"
OLD = BASE / "ORCAMENTO_015_v9.json"
NEW = BASE / "ORCAMENTO_015_v10.json"
RECEIPT = HERE / "T08_FINAL_RESULT.json"
WITNESS = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_ORCAMENTO_015_v10.md"
PROGRESS = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_PROGRESSO.md"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

budget = json.loads(OLD.read_bytes())
result = json.loads(RECEIPT.read_bytes())
assert result["status"].startswith("T08_MEDIDA_PARTIAL")
spent = result["machine_hours_conservative_start_to_finalizer"]
assert 0 < spent < 2
items = {r["item"]: r for r in budget["items"]}
old_t10 = items["T10_calibration"]["allocated_machine_hours"]
saved = items["T08_selection"]["allocated_machine_hours"] - spent
items["T08_selection"].update(allocated_machine_hours=spent,
    actual_machine_hours=spent, job_started=True,
    status=result["status"], final_receipt_sha256=sha(RECEIPT))
items["T10_calibration"]["allocated_machine_hours"] += saved
budget["registered_utc"] = datetime.now(timezone.utc).isoformat()
budget["supersedes_sha256"] = sha(OLD)
budget["witness_relative_to_Chatgpt"] = WITNESS.relative_to(CHAT).as_posix()
budget["allocated_machine_hours"] = sum(r["allocated_machine_hours"] for r in budget["items"])
budget["accounting"]["intervals"].append({
    "target": "T08_SELECTION_PARTIAL",
    "receipt_relative_to_Chatgpt": RECEIPT.relative_to(CHAT).as_posix(),
    "sha256": sha(RECEIPT), "union_machine_hours": spent,
    "accounting_statute": "CONSERVATIVE_START_TO_FINALIZER_WALL"})
budget["accounting"]["machine_hours_spent"] = sum(r.get("actual_machine_hours", 0) for r in budget["items"])
budget["reallocation_reason"] = "T08 public PE catalog requires approximately 40.77 GB; one-file rate extrapolation 7.53h transfer-only exceeds 2h T08 budget; unused T08 allocation transferred to T10"
budget["reallocation_changes"] = {"T08_selection": {"old": 2.0, "new": spent},
    "T10_calibration": {"old": old_t10, "new": items["T10_calibration"]["allocated_machine_hours"]}}
budget["T08_measurement"] = {"result_sha256": sha(RECEIPT),
    "public_PE_coverage": result["counts"],
    "pilot_only": True, "epsilon_alpha_unpaid": True,
    "transfer_forecast_hours_not_spent": result["sequential_all_files_forecast_hours_at_one_file_rate"]}
assert abs(budget["allocated_machine_hours"] - budget["authorized_machine_hours"]) < 1e-9
assert budget["accounting"]["machine_hours_spent"] < budget["authorized_machine_hours"]
with NEW.open("xb") as stream:
    stream.write((json.dumps(budget, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
text = ("[REAL] T08 MEDIDA parcial: 70/74 arquivos PE encontrados em metadados; 1 piloto GR de SNR dividido; seleção 74, ε(θ) e α(Λ) NÃO PAGOS.\n\n"
        f"Abertura016 SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a; "
        f"pai v9 SHA256: {sha(OLD)}; T08 SHA256: {sha(RECEIPT)}; v10 SHA256: {sha(NEW)}.\n\n"
        f"T08 cobrado por parede conservadora {spent:.9f}h; saldo {saved:.9f}h movido a T10. "
        f"Total autorizado/alocado {budget['authorized_machine_hours']:.9f}h; "
        f"gasto registrado {budget['accounting']['machine_hours_spent']:.9f}h. "
        f"Projeção apenas de transferência dos 70 arquivos {result['sequential_all_files_forecast_hours_at_one_file_rate']:.3f}h; fora do teto T08. Sem gate.\n")
with WITNESS.open("xb") as stream:
    stream.write(text.encode())
old = PROGRESS.read_bytes()
backup = PROGRESS.with_name(PROGRESS.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
with backup.open("xb") as stream:
    stream.write(old)
assert backup.read_bytes() == old
line = (f"\n{datetime.now(timezone.utc).isoformat()} | B/T08 | MEDIDA/NÃO PAGO: 70/74 arquivos PE públicos indexados; "
        f"1 piloto GR, seleção 74/ε/α NÃO PAGOS; corte ≥8 interno ≠ >6 LVK | "
        f"máquina {spent:.9f}h; acumulado {budget['accounting']['machine_hours_spent']:.9f}h | "
        f"recibo SHA256 {sha(RECEIPT)}; próximo T09\n").encode()
temp = PROGRESS.with_name(PROGRESS.name + ".tmp_t08")
with temp.open("xb") as stream:
    stream.write(old + line)
assert temp.stat().st_size == len(old) + len(line)
os.replace(temp, PROGRESS)
assert PROGRESS.read_bytes() == old + line
print(json.dumps({"budget_sha256": sha(NEW), "witness_sha256": sha(WITNESS),
                  "machine_hours_spent": budget["accounting"]["machine_hours_spent"],
                  "T10_allocated_hours": items["T10_calibration"]["allocated_machine_hours"]}))
