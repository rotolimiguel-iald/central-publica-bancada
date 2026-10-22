"""Prepare one Kimi skeptical review of the concrete copied T04-F instrument."""
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
F = RING / "bis" / "e3_kerr_dtau_f_015"


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
    assert not list(ORCH.glob("t04f_kimi_*.json"))
    manifest = json.loads((F / "MANIFEST.json").read_bytes())
    assert manifest["code_sha256"]["kerr_model.py"] == sha(F / "kerr_model.py")
    assert manifest["code_sha256"]["runner.py"] == sha(F / "runner.py")
    assert manifest["source_and_config_pins"]["ORDEM_013_RINGDOWN/bis/e3_kerr_dtau_f_015/CONFIG.json"] == sha(F / "CONFIG.json")
    prompt = (
        "ORDEM016 Parte B T04-F: revisão cética de UM artefato concreto, sem executar código. "
        "O instrumento Kerr V2 foi COPIADO (originais intactos) para bis/e3_kerr_dtau_f_015. "
        f"Hashes: modelo {sha(F/'kerr_model.py')}; runner {sha(F/'runner.py')}; "
        f"config {sha(F/'CONFIG.json')}; manifesto {sha(F/'MANIFEST.json')}. "
        "Diff científico exato: PARAMETERS originais 8 agora acrescidos de 'dtau220' no fim; "
        "polarizations chama frequency_tau(Mf,af,coeff,mass_time) inalterado e depois "
        "if not dtau220>-1: ValueError; tau *= 1+dtau220; h original usa exp(-t/tau) "
        "nas duas ramas ±220. f, harmonias, fases, geometria H1/L1, covariância e likelihood não mudam. "
        "Runner mantém posterior pareado dinâmico por PARAMETERS, muda label para Kerr220DtauF "
        "e grava dtau_identifiability=SINGLE_220_FREE_MF_AF_NOT_IDENTIFIABLE, sigma_eligible=false. "
        "Config: prior dtau220 Uniform[-0.8,2.0] copiado do pSEOB C; os oito priors antigos "
        "são os mesmos; seed novo 15260405; dados e PSD mesmos do Kerr V2; saída única; "
        "7200s envelope/6800s public_psd; deadline do relógio Part015 2026-10-03; "
        "orçamento v5 SHA 63d3436d... reserva 7,958360255746666h para F. "
        "Teste local no WSL pinado: dtau=0 coincide bitwise (erro 0); dtau=.5 muda amortecimento "
        "com erro máximo na razão 4,44e-15; -1,-1.1,NaN recusados; posterior não rodado. "
        "A custódia copiada ainda exigirá autorização NOVA, assinada após revisão, e validação de "
        "pins/tempo antes de lançar; autorização antiga expirada não será reutilizada. "
        "Pergunta única: encontre qualquer falha verificável nessa extensão ou na separação "
        "diagnóstico sem sigma versus medição, e indique os controles mínimos faltantes antes "
        "do primeiro job F. Marque o que depende dos arquivos integrais que você não recebeu. "
        "Não trate o hash como prova de conteúdo, não invente convergência nem mova gate."
    )
    request_id = str(uuid.uuid4())
    constraints = dict(mission_id="ORDEM_016", branch_id="B_T04_F",
                       lemma_id="concrete_kerr_dtau_f_skeptic", role="skeptic",
                       required_provider="kimi", max_calls=1)
    preview = dict(operation="preview_execution", prompt=prompt, execution_constraints=constraints)
    submit = dict(preview, operation="submit", request_id=request_id)
    receipt = dict(request_id=request_id, job_id=None, state="PREPARED_NOT_SUBMITTED",
                   created_utc=datetime.now(timezone.utc).isoformat(),
                   home=str(HERE), mission="ORDEM_016", branch="B_T04_F",
                   prompt_sha256=hashlib.sha256(prompt.encode("utf-8")).hexdigest())
    ORCH.mkdir(exist_ok=True)
    new(ORCH / "t04f_kimi_receipt.json", receipt)
    new(ORCH / "t04f_kimi_preview.json", preview)
    new(ORCH / "t04f_kimi_submit.json", submit)
    print(json.dumps(dict(status="PREPARED_NOT_SUBMITTED", request_id=request_id,
                          prompt_chars=len(prompt),prompt_sha256=receipt["prompt_sha256"])))


if __name__ == "__main__":
    main()
