"""Prepare one exact-diff Kimi source review; no provider is called here."""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

here = Path(__file__).resolve().parent
ring = here.parents[2]
old = ring / "bis" / "e3_kerr_continuation"
new = ring / "bis" / "e3_kerr_dtau_f_015"
outdir = here.parent / "orchestration"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path: Path, obj: object) -> None:
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    assert path.read_bytes() == raw


def main() -> None:
    assert not (outdir / "t04f_source_review_receipt.json").exists()
    chunks = []
    for name in ("kerr_model.py", "runner.py", "CONFIG.json"):
        a, b = old / name, new / name
        delta = "".join(difflib.unified_diff(a.read_text(encoding="utf-8").splitlines(True),
                                               b.read_text(encoding="utf-8").splitlines(True),
                                               fromfile="old/"+name, tofile="new/"+name, n=5))
        chunks.append(f"{name}: old_sha={sha(a)} new_sha={sha(b)}\n{delta}")
    manifest = new / "MANIFEST_v2.json"
    evidence = ring / "C5_FISHER_v3.json"
    allocation = ring / "bis" / "015" / "E2_PE_JOBS_ALLOCATION_015_V4.json"
    prompt = (
        "ORDEM016 Parte B T04-F, source-level skeptic review. Abaixo estão os diffs completos "
        "dos três arquivos alterados; conditioning/controller/custody são cópias bytewise. "
        "Qual defeito verificável nestes diffs impediria uma execução F diagnóstica única, "
        "sem σ ou gate? Aponte linha/expressão e controle mínimo; se nenhum, diga isso, "
        "sem prometer convergência. F é último ramo de T04 após C maxcall parcial; F usa "
        "um modo 220 com Mf e af livres e é não identificável para dtau. Testes locais: "
        "dtau=0 waveform idêntico, dtau=.5 razão analítica nas ramas + e -, invalid -1/NaN recusados. "
        "Não viu arquivos completos de runtime nem executou código; não alegue isso. "
        f"Manifesto v2 sha={sha(manifest)}; prior pSEOB C allocation sha={sha(allocation)}; "
        f"C5 Fisher status NON_IDENTIFIABLE_SINGLE_220 sha={sha(evidence)}.\n\n"
        + "\n".join(chunks)
    )
    assert len(prompt) <= 20000, len(prompt)
    request_id = str(uuid.uuid4())
    constraints = dict(mission_id="ORDEM_016", branch_id="B_T04_F",
                       lemma_id="kerr_dtau_f_exact_source_delta", role="skeptic",
                       required_provider="kimi", max_calls=1)
    preview = dict(operation="preview_execution", prompt=prompt, execution_constraints=constraints)
    submit = dict(preview, operation="submit", request_id=request_id)
    outdir.mkdir(exist_ok=True)
    create(outdir / "t04f_source_review_preview.json", preview)
    create(outdir / "t04f_source_review_submit.json", submit)
    create(outdir / "t04f_source_review_receipt.json",
           dict(request_id=request_id, job_id=None, state="PREPARED_NOT_SUBMITTED",
                at=datetime.now(timezone.utc).isoformat(), prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    print(json.dumps(dict(status="PREPARED", request_id=request_id, prompt_chars=len(prompt),
                          prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest())))


if __name__ == "__main__":
    main()
