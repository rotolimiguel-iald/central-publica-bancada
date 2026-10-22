"""Prepare one idempotent ORDEM016 Kimi review without calling a provider."""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORCH = HERE.parent / "orchestration"
PROMPT = (
    "ORDEM016 / ORDEM015 T04-H: revisão cética independente, uma pergunta. "
    "C terminou controladamente com status PARTIAL_MAXCALL_NOT_ACCEPTED, não aborto nativo; "
    "limpeza confirmada. ncall=5.739.196 em 23.066,605932876 s; "
    "delta_logz=176,98412180837477 (limiar 0,1), ESS=1,0005999249182786 "
    "(mínimo 100), uma amostra posterior, aceitação falsa. "
    "A ORDEM015 distingue D por status literal PARTIAL_LOW_ESS ou "
    "PARTIAL_TOO_FEW_POSTERIOR_SAMPLES, E por aborto nativo e H por outro estado; "
    "H autoriza uma repetição com novo ID/semente, nlive1024, maxcall pela fórmula C, "
    "teto de 8 h. Registramos H1, seed15260404, nlive1024, "
    "maxcall=floor(0,9×28800×(5739196/23066,605932876))=6449148. "
    "Preflight guard passou; fonte, dados, priors e grade preservados. "
    "C consumiu 6,410089644876389 h; o orçamento v4 reserva 8 h a H "
    "reduzindo T10 a 5,640245016630272 h; soma 35,01724298083333 h. "
    "Pergunta única: há uma violação verificável da árvore ou do orçamento que "
    "impeça lançar H1, ou a classificação residual e a reserva são defensáveis? "
    "Distingua previsão de duração de previsão de convergência. "
    "Não invente chance de sucesso, posterior, sigma nem mudança de gate. "
    "Fontes auditáveis: ORDEM015 SHA256 c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3; "
    "RESULT C SHA256 9663242560623d92e933bdab82ca176022f6b3606ee285aceea6c8a9eecaea36; "
    "orçamento v4 SHA256 56da0bdff06d25db6ad7dfcd5fe5cf37b8af3155af8f6f6fc3a248d26912ccca."
)


def write_new(path: Path, obj: dict) -> None:
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.stat().st_size == len(data)


def main() -> None:
    ORCH.mkdir(exist_ok=True)
    key = "t04h_kimi"
    candidates = list(ORCH.glob(f"{key}_*.json"))
    if candidates:
        print(json.dumps(dict(status="EXISTING_REQUEST_MUST_BE_RECOVERED", files=[p.name for p in candidates])))
        return
    request_id = str(uuid.uuid4())
    constraints = dict(mission_id="ORDEM_016", branch_id="B_T04_H",
                       lemma_id="post_C_route_and_budget", role="skeptic",
                       required_provider="kimi", max_calls=1)
    payload = dict(operation="preview_execution", prompt=PROMPT,
                   execution_constraints=constraints)
    submit = dict(payload, operation="submit", request_id=request_id)
    receipt = dict(request_id=request_id, job_id=None,
                   created_utc=datetime.now(timezone.utc).isoformat(),
                   home="C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/015/t04",
                   mission="ORDEM_016", branch="B_T04_H",
                   state="PREPARED_NOT_SUBMITTED",
                   prompt_sha256=hashlib.sha256(PROMPT.encode("utf-8")).hexdigest())
    write_new(ORCH / f"{key}_receipt.json", receipt)
    write_new(ORCH / f"{key}_preview.json", payload)
    write_new(ORCH / f"{key}_submit.json", submit)
    print(json.dumps(dict(status="PREPARED_NOT_SUBMITTED", request_id=request_id,
                          prompt_sha256=receipt["prompt_sha256"], prompt_chars=len(PROMPT))))


if __name__ == "__main__":
    main()
