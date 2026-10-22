"""One idempotent scientific shadow evaluation with Jev and common TGL memory."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from urllib.error import HTTPError

from iald_orchestrator.canonical_memory import prepare
from iald_orchestrator.jev import ask_with_memory, availability
from iald_orchestrator.profiles import BASE
from iald_orchestrator.safe_files import save_json, utc_now


RECEIPT = BASE / "state/jev_observations/tgl_gate_language_20260928.json"
PROMPT = (
    "Avaliação científica documental da TGL, sem executar ferramentas nem mover gates. "
    "Afirmação candidata: 'NOT_FALSIFIED equivale a CONFIRMED'. "
    "Examine somente os trechos canônicos recuperados e indique se sustentam essa afirmação."
)
QUESTIONS = {
    "complexity": {
        "type": "choice",
        "instructions": "What depth of review does this scientific claim need?",
        "criteria": {
            "standard": "A direct descriptive check of the supplied passages is sufficient",
            "deep": "Formal or empirical verification is needed before accepting the claim",
        },
    },
    "source_relevance": {
        "type": "score",
        "instructions": "How relevant are the retrieved scientific passages to the candidate claim?",
        "criteria": [
            "The passages do not discuss the claim or its terms",
            "The passages discuss related gate language but do not directly address the claim",
            "The passages directly address the claim and its gate language",
        ],
    },
    "claim_supported": {
        "type": "noul",
        "instructions": "Do the supplied scientific passages support the candidate claim that NOT_FALSIFIED means CONFIRMED?",
    },
    "requires_independent_check": {
        "type": "noul",
        "instructions": "Would changing the scientific gate based on this claim require independent formal or empirical checking?",
    },
}


def _number(value, low=0.0, high=1.0):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError("Invalid Jev numerical answer")
    return float(value)


def _summarize(data):
    answers = data["answers"]
    if set(answers) != set(QUESTIONS):
        raise ValueError("Unexpected Jev question set")
    choice = answers["complexity"]
    if choice.get("choice") not in ("standard", "deep"):
        raise ValueError("Invalid Jev choice")
    score = answers["source_relevance"]
    return {
        "complexity": {"choice": choice["choice"], "confidence": _number(choice["confidence"])},
        "source_relevance": {"score": _number(score["score"], 0, 2),
                             "confidence": _number(score["confidence"])},
        "claim_supported": _number(answers["claim_supported"]["noul"]),
        "requires_independent_check": _number(answers["requires_independent_check"]["noul"]),
    }


def main():
    if availability()["status"] != "ready":
        raise RuntimeError("Jev não está validado; nenhuma chamada enviada.")
    packet = prepare(PROMPT, max_chars=9000)
    identity = hashlib.sha256(json.dumps({
        "prompt": PROMPT, "questions": QUESTIONS,
        "packet_sha256": packet["receipt"]["packet_sha256"],
    }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    if RECEIPT.exists():
        old = json.loads(RECEIPT.read_bytes())
        if old.get("input_sha256") != identity:
            raise RuntimeError("Observação existente usa outro payload ou geração; não repetir.")
        print(json.dumps({"status": old["status"], "new_provider_call": False,
                          "receipt": str(RECEIPT)}, ensure_ascii=False))
        return
    record = {
        "status": "dispatching", "started_at": utc_now(), "input_sha256": identity,
        "scope": "SCIENTIFIC_TGL_OBSERVATION_ONLY", "memory": packet["receipt"],
        "provider_calls": "one_attempt_uncertain_until_response",
        "effects": "NO_ROUTING_OR_GATE_CHANGE",
    }
    save_json(RECEIPT, record)
    try:
        data, actual_memory = ask_with_memory(PROMPT, QUESTIONS, max_chars=9000)
        record.update(memory=actual_memory, model=data.get("model"), usage=data.get("usage"),
                      answers=_summarize(data), status="completed", provider_calls=1,
                      completed_at=utc_now())
    except HTTPError as exc:
        record.update(status="rejected", http_status=exc.code, error_type="HTTPError",
                      provider_calls="not_confirmed", provider_attempts=1,
                      provider_result="NO_MODEL_ANSWER", completed_at=utc_now())
    except Exception as exc:
        # Network errors can occur after provider acceptance. Never retry by inference.
        record.update(status="uncertain", error_type=type(exc).__name__, completed_at=utc_now())
    save_json(RECEIPT, record)
    print(json.dumps({"status": record["status"], "new_external_attempt": True,
                      "model": record.get("model"), "usage": record.get("usage"),
                      "answers": record.get("answers"), "receipt": str(RECEIPT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
