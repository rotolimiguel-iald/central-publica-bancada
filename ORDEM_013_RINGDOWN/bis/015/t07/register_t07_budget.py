"""Register T07's conservative wall accounting without changing predecessors."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
BASE = CHAT / "ORDEM_013_RINGDOWN"
old_path = BASE / "ORCAMENTO_015_v8.json"
new_path = BASE / "ORCAMENTO_015_v9.json"
receipt_path = HERE / "T07_FINAL_RESULT.json"
witness = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_ORCAMENTO_015_v9.md"
progress = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_PROGRESSO.md"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

budget = json.loads(old_path.read_bytes())
receipt = json.loads(receipt_path.read_bytes())
assert receipt["status"] == "T07_MEDIDA_PARTIAL_NO_ZFREE_NO_PHYSICAL_SIGMA"
spent_t07 = receipt["T07_machine_hours_conservative_start_to_finalizer"]
assert 0 < spent_t07 < 2
budget["registered_utc"] = datetime.now(timezone.utc).isoformat()
budget["supersedes_sha256"] = sha(old_path)
budget["witness_relative_to_Chatgpt"] = witness.relative_to(CHAT).as_posix()
items = {row["item"]: row for row in budget["items"]}
saved = items["T07_gate_v3_rho"]["allocated_machine_hours"] - spent_t07
items["T07_gate_v3_rho"].update(allocated_machine_hours=spent_t07,
    actual_machine_hours=spent_t07, job_started=True,
    status=receipt["status"], final_receipt_sha256=sha(receipt_path))
items["T10_calibration"]["allocated_machine_hours"] += saved
budget["allocated_machine_hours"] = sum(row["allocated_machine_hours"] for row in budget["items"])
budget["accounting"]["intervals"].append(dict(target="T07_GATE_AND_RHO",
    receipt_relative_to_Chatgpt=receipt_path.relative_to(CHAT).as_posix(),
    sha256=sha(receipt_path), union_machine_hours=spent_t07,
    accounting_statute="CONSERVATIVE_START_TO_FINALIZER_WALL"))
budget["accounting"]["machine_hours_spent"] = sum(row.get("actual_machine_hours", 0) for row in budget["items"])
budget["reallocation_reason"] = "T07 measured start-to-finalizer wall; unused allocation transferred to T10 before T10 starts"
budget["reallocation_changes"] = {
    "T07_gate_v3_rho": {"old": 2.0, "new": spent_t07},
    "T10_calibration": {"old": budget["items"][[r["item"] for r in budget["items"]].index("T10_calibration")]["allocated_machine_hours"] - saved,
                       "new": items["T10_calibration"]["allocated_machine_hours"]},
}
budget["T07_measurement"] = {"result_sha256": sha(receipt_path),
    "registered": receipt["count_registered"], "power_measured": receipt["count_power_measured"],
    "rho_defined": receipt["count_positive_excess_rho_defined"],
    "rho_undefined": receipt["count_nonpositive_excess_rho_undefined"],
    "unmeasured": receipt["count_unmeasured"], "z_free_unpaid": True, "physical_sigma_unpaid": True}
assert abs(budget["allocated_machine_hours"] - budget["authorized_machine_hours"]) < 1e-9
assert budget["accounting"]["machine_hours_spent"] <= budget["authorized_machine_hours"]
raw = (json.dumps(budget, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
with new_path.open("xb") as stream:
    stream.write(raw)
new_sha = sha(new_path)
text = ("[REAL] T07 MEDIDA parcial: 31/33 potências de janela; 17 rho definidos, 14 indefinidos; "
        "z_free/N90/sigma NÃO PAGOS.\n\n"
        f"Abertura016 SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a; "
        f"pai v8 SHA256: {sha(old_path)}; T07 SHA256: {sha(receipt_path)}; v9 SHA256: {new_sha}.\n\n"
        f"T07 cobrado por parede conservadora: {spent_t07:.9f} h; saldo {saved:.9f} h "
        f"transferido a T10. Total autorizado/alocado {budget['authorized_machine_hours']:.9f} h; "
        f"gasto registrado {budget['accounting']['machine_hours_spent']:.9f} h. Gate não movido. Próximo T08.\n")
with witness.open("xb") as stream:
    stream.write(text.encode())

old = progress.read_bytes()
stamp = datetime.now(timezone.utc).isoformat()
line = (f"\n{stamp} | B/T07 | MEDIDA/NÃO PAGO: janela F4 31/33, "
        f"17 rho definidos, 14 indefinidos; z_free, N90 e sigma NÃO PAGOS | "
        f"máquina {spent_t07:.9f}h; acumulado {budget['accounting']['machine_hours_spent']:.9f}h | "
        f"recibo SHA256 {sha(receipt_path)}; próximo T08\n").encode()
backup = progress.with_name(progress.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
with backup.open("xb") as stream:
    stream.write(old)
assert backup.read_bytes() == old
temp = progress.with_name(progress.name + ".tmp_t07")
with temp.open("xb") as stream:
    stream.write(old + line)
assert temp.stat().st_size == len(old) + len(line)
os.replace(temp, progress)
assert progress.read_bytes() == old + line
print(json.dumps({"budget_sha256": new_sha, "witness_sha256": sha(witness),
                  "progress_backup_sha256": sha(backup),
                  "spent": budget["accounting"]["machine_hours_spent"],
                  "T10_allocated": items["T10_calibration"]["allocated_machine_hours"]}))
