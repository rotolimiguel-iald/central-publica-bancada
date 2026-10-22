"""Prepare one idempotent, provider-locked execution per cockpit v3 brief."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
UNITS = (
    ("kimi_gpu", "BRIEF_V3_GPU_KIMI.md", "kimi", "gpu-architecture", "draft"),
    ("mimo_treatment", "BRIEF_V3_DATA_MIMO.md", "mimo", "data-contract", "skeptic"),
    ("gemini_ui", "BRIEF_V3_UI_GEMINI.md", "gemini", "ui-review", "draft"),
    ("kimi_audit", "BRIEF_V3_KIMI_AUDIT.md", "kimi", "gpu-hdf5-audit", "skeptic"),
    ("mimo_hdf5_review", "BRIEF_V3_MIMO_HDF5_REVIEW.md", "mimo", "hdf5-safety", "skeptic"),
)


def atomic(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".new")
    temp.write_bytes(body)
    if temp.stat().st_size != len(body):
        raise OSError(f"Incomplete file: {temp}")
    temp.replace(path)


def main() -> None:
    for name, brief, provider, lemma, role in UNITS:
        marker = HERE / (name + ".request_id")
        if marker.exists():
            request_id = marker.read_text(encoding="ascii").strip()
            uuid.UUID(request_id)
        else:
            request_id = str(uuid.uuid4())
            atomic(marker, (request_id + "\n").encode("ascii"))
        prompt = (HERE / brief).read_text(encoding="utf-8").strip()
        constraints = {"mission_id": "TGL_BANCADA_OFICIAL", "branch_id": "cockpit-v3",
                       "lemma_id": lemma, "role": role,
                       "required_provider": provider, "max_calls": 1}
        request = {"operation": "submit_execution", "request_id": request_id,
                   "prompt": prompt, "execution_constraints": constraints}
        atomic(HERE / (name + ".submit.json"), json.dumps(request, ensure_ascii=False).encode("utf-8"))
        receipt = BASE / "state" / "session_requests" / (request_id + ".json")
        if not receipt.exists():
            atomic(receipt, json.dumps({"request_id": request_id,
                       "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "origin": str(HERE.parent), "mission": "TGL_BANCADA_OFICIAL",
                       "status": "prepared_not_submitted", "required_provider": provider,
                       "prompt": prompt, "execution_constraints": constraints},
                       ensure_ascii=False, indent=2).encode("utf-8"))
        print(f"{name} {provider} {request_id}")


if __name__ == "__main__":
    main()
