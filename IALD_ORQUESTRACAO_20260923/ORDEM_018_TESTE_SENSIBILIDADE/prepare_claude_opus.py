"""Prepare and preview the single authorized Opus drafting unit."""

import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from iald_orchestrator.runtime import Runtime
from iald_orchestrator.safe_files import save_json, utc_now

HERE = Path(__file__).resolve().parent


def main():
    campaign_path = HERE / "campaign.json"
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    if campaign["claude_opus"]["status"] != "request_id_reserved":
        raise RuntimeError("Claude unit was already prepared or dispatched.")
    prompt = (HERE / "claude_opus_order_prompt.txt").read_text(encoding="utf-8")
    constraints = {
        "mission_id": "TGL_BANCADA_OFICIAL",
        "branch_id": "ORDEM_018_SENSITIVITY",
        "lemma_id": "claude_opus_final_order_v375",
        "role": "draft", "required_provider": "claude", "max_calls": 1,
        "memory_generation": campaign["canonical_memory"]["generation"],
        "allowed_sources": ["um.py"], "max_projection_chars": 20000,
    }
    record = {"operation": "submit", "prompt": prompt,
              "request_id": campaign["claude_opus"]["request_id"],
              "execution_constraints": constraints}
    path = HERE / "claude_opus_submit.json"
    if path.exists() and json.loads(path.read_text(encoding="utf-8")) != record:
        raise RuntimeError("Existing Claude unit differs; no replacement.")
    if not path.exists():
        save_json(path, record)
    preview = Runtime(recover=False).preview(prompt, constraints)
    if preview.get("selected") != "claude":
        raise RuntimeError("Required Claude executor unavailable.")
    memory = preview["canonical_memory"]
    save_json(HERE / "claude_opus_preview.json", {
        "selected": preview["selected"],
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "request_id": record["request_id"], "preview": preview,
    })
    campaign["claude_opus"].update({
        "status": "prepared_not_submitted", "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_chars": len(prompt), "memory_context_bytes": memory["context_bytes"],
        "prepared_at": utc_now(),
    })
    save_json(campaign_path, campaign)
    print(json.dumps({"selected": "claude", "prompt_chars": len(prompt),
                      "memory_context_bytes": memory["context_bytes"],
                      "source_excerpts": len(memory["sources"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
