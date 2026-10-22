"""Measure which source lines ORDEM_018 wave one actually transported."""

import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from iald_orchestrator.safe_files import save_json, utc_now

HERE = Path(__file__).resolve().parent
SOURCE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")


def main():
    source_bytes = SOURCE.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    total_lines = source_bytes.count(b"\n") + (not source_bytes.endswith(b"\n"))
    campaign = json.loads((HERE / "campaign.json").read_text(encoding="utf-8"))
    if source_hash != campaign["um_py"]["sha256"]:
        raise RuntimeError("The canonical source changed after wave one was prepared.")
    previews = json.loads((HERE / "wave1/previews.json").read_text(encoding="utf-8"))
    union = set()
    by_provider = {}
    for provider, entry in previews.items():
        memory = entry["preview"]["canonical_memory"]
        if memory["generation"] != campaign["canonical_memory"]["generation"]:
            raise RuntimeError("Memory generation changed between previews.")
        intervals = {(s["first_line"], s["last_line"])
                     for s in memory["sources"] if s["file"] == "um.py"}
        lines = set()
        for first, last in intervals:
            lines.update(range(first, last + 1))
        union.update(lines)
        by_provider[provider] = {
            "context_bytes": memory["context_bytes"],
            "listed_excerpts": len(memory["sources"]),
            "unique_excerpts": len(intervals),
            "unique_source_lines": len(lines),
            "source_line_coverage_fraction": len(lines) / total_lines,
            "coverage_label": memory["coverage"],
        }
    receipt = {
        "at": utc_now(), "source": str(SOURCE), "source_sha256": source_hash,
        "source_bytes": len(source_bytes), "source_lines": total_lines,
        "by_provider": by_provider, "union_unique_source_lines": len(union),
        "union_line_coverage_fraction": len(union) / total_lines,
        "not_transported_source_lines": total_lines - len(union),
        "interpretation": "Source-line coverage of the returned memory packet only; model comprehension and other documents are not established.",
    }
    save_json(HERE / "wave1/coverage_audit.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
