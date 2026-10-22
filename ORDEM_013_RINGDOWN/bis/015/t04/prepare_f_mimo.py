"""Prepare one bounded MiMo draft for the next written T04-F instrument."""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
ORCH = HERE.parent / "orchestration"
MODEL = RING / "bis" / "e3_kerr_continuation" / "kerr_model.py"
RUNNER = RING / "bis" / "e3_kerr_continuation" / "runner.py"
CONFIG = RING / "bis" / "e3_kerr_continuation" / "CONFIG.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new(path: Path, obj: dict) -> None:
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.stat().st_size == len(data)


def main() -> None:
    assert sha(MODEL) == "d1ecfb420a61bf998b86b818f4b98350947e0d41961a411d50260401df47ac38"
    assert sha(RUNNER) == "d4f1975c4c0671e305507b41dbeaf5c9432c6c28f90cc25947e43bcdf27ead50"
    assert sha(CONFIG) == "f0028baf5ffaceb9b68e4672e8acae45ecce6325a4b523d068815e5cca63b18d"
    assert not list(ORCH.glob("t04f_mimo_*.json"))
    prompt = (
        "ORDEM016 Parte B / ORDEM015 T04-F: uma tarefa de rascunho técnico, sem executar. "
        "O ramo C terminou sem posterior aceito (delta_logz 176,984, ESS 1,0006, 1 amostra). "
        "A árvore manda F: segundo instrumento Kerr V2 estendido por dtau220, com aviso "
        "de não identificabilidade de um único modo quando Mf e af são livres. "
        "Trabalhar em CÓPIAS na bancada, sem alterar fonte custodiada. "
        "Código base Kerr V2 (kerr_model.py SHA256 d1ecfb42...): "
        "PARAMETERS=('psi','Mf','af','cosiota','A2220_1','A2220_2','phi2220_1','phi2220_2'); "
        "frequency_tau(mass,spin,coefficients,mass_time_s) retorna f e tau>0; "
        "polarizations calcula h=reference_amplitude*exp(-t/tau)*"
        "(yp*A1*exp(i phi1)*exp(+2pi i f t)+ym*A2*exp(i phi2)*exp(-2pi i f t)); "
        "likelihood usa H1/L1, mesma geometria e covariância. "
        "Runner SHA256 d4f1975c... monta priors por cfg['priors'], verifica PARAMETERS "
        "e escreve posterior pareado; CONFIG SHA256 f0028baf... define 8 priors. "
        "Pergunta única: qual é o diff MÍNIMO e quais testes adversariais verificáveis para "
        "introduzir o 9º parâmetro dtau220 com tau'=tau_Kerr*(1+dtau220), suporte "
        "dtau220>-1, preservando f, fases, harmonias, H1/L1, likelihood e custódia, "
        "e impedindo que um posterior de um modo com (Mf,af) livres seja vendido como "
        "medição identificável ou sigma? Distinga o que é definição, INPUT de prior, "
        "e o que precisará ser medido no GW250114. Não proponha nova camada geral, "
        "não invente dados nem mude a leitura física/gate. Até 1200 palavras."
    )
    request_id = str(uuid.uuid4())
    constraints = dict(mission_id="ORDEM_016", branch_id="B_T04_F",
                       lemma_id="kerr_dtau220_extension", role="draft",
                       required_provider="mimo", max_calls=1,
                       max_cost_usd=None, max_output_tokens=131072)
    preview = dict(operation="preview_execution", prompt=prompt, execution_constraints=constraints)
    submit = dict(preview, operation="submit", request_id=request_id)
    receipt = dict(request_id=request_id, job_id=None, state="PREPARED_NOT_SUBMITTED",
                   created_utc=datetime.now(timezone.utc).isoformat(),
                   home=str(HERE), mission="ORDEM_016", branch="B_T04_F",
                   prompt_sha256=hashlib.sha256(prompt.encode("utf-8")).hexdigest())
    ORCH.mkdir(exist_ok=True)
    new(ORCH / "t04f_mimo_receipt.json", receipt)
    new(ORCH / "t04f_mimo_preview.json", preview)
    new(ORCH / "t04f_mimo_submit.json", submit)
    print(json.dumps(dict(status="PREPARED_NOT_SUBMITTED", request_id=request_id,
                          prompt_chars=len(prompt), prompt_sha256=receipt["prompt_sha256"])))


if __name__ == "__main__":
    main()
