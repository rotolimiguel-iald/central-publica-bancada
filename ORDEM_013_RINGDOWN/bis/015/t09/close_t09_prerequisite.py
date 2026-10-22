"""Close T09 without running an unauthorized 440 prior box."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
BASE = CHAT / "ORDEM_013_RINGDOWN"
OPEN = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_ABERTURA_operador.md"
ORDER = CHAT / "TUNEL" / "PARA_CHATGPT" / "ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md"
T04 = BASE / "bis" / "015" / "t04" / "branch_f" / "RESULT.json"
PROGRESS = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_PROGRESSO.md"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

opening = OPEN.read_text(encoding="utf-8")
assert "Sem decisões adicionais de partição, caixa 440" in opening
t04 = json.loads(T04.read_bytes())
assert not t04["sigma_eligible"]
result = {
    "status": "T09_NAO_PAGO_OPERATOR_BOX_B_LINE_ABSENT",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "opening_sha256": sha(OPEN), "order_sha256": sha(ORDER),
    "T04_F_diagnostic_sha256": sha(T04),
    "operator_box_b_authorization_in_opening": False,
    "prior_box_b_started": False,
    "prior_box_b_minus_started": False,
    "PE_started": False,
    "machine_hours": 0.0,
    "estimated_cost_if_authorized_hours": [2.6, 3.3],
    "estimated_ceiling_hours": 8.0,
    "lnBayes_440_220": None,
    "gate_changed": False,
    "next_branch": "T10",
}
target = HERE / "T09_PREREQUISITE_RESULT.json"
with target.open("xb") as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode())
handoff = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_MEDIDA_T09_sem_caixa_b.md"
body = ("[REAL — pré-condição não satisfeita; OPEN — efeito físico do 440 livre]\n\n"
        "# ORDEM 015 / T09 — caixa (b) não iniciada\n\n"
        f"Abertura do operador SHA256 `{sha(OPEN)}` declara expressamente que não houve decisão adicional sobre a caixa 440. "
        f"A ORDEM015 SHA256 `{sha(ORDER)}` exige linha do operador para a caixa (b). "
        f"O T04/F SHA256 `{sha(T04)}` é diagnóstico não identificável e inelegível para sigma. "
        "Nenhuma PE 440 foi iniciada; lnB segue indefinido. Custo estimado da rodada: 2,6–3,3 h, teto 8 h, não consumido. "
        f"Recibo `{sha(target)}`. Próximo T10.\n")
with handoff.open("xb") as stream:
    stream.write(body.encode())
old = PROGRESS.read_bytes()
backup = PROGRESS.with_name(PROGRESS.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
with backup.open("xb") as stream:
    stream.write(old)
assert backup.read_bytes() == old
line = (f"\n{datetime.now(timezone.utc).isoformat()} | B/T09 | NÃO PAGO: caixa (b) sem linha do operador; "
        f"0h consumidas, custo estimado 2,6–3,3h, teto 8h | recibo SHA256 {sha(target)}; próximo T10\n").encode()
temp = PROGRESS.with_name(PROGRESS.name + ".tmp_t09")
with temp.open("xb") as stream:
    stream.write(old + line)
os.replace(temp, PROGRESS)
assert PROGRESS.read_bytes() == old + line
print(json.dumps({"result_sha256": sha(target), "handoff_sha256": sha(handoff),
                  "progress_sha256": sha(PROGRESS)}))
