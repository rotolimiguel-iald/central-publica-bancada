"""Probe a repeated short CCHP anchor against the pinned R3 documentary gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile

import f9_reader_gate_v1x_r3 as gate
import test_f9_r3_independent_adversarial_20261008 as helpers


def main() -> None:
    binding = json.loads(helpers.BINDING.read_text(encoding="utf-8"))
    draft = json.loads(Path(binding["draft_v2"]["path"]).read_text(encoding="utf-8"))
    row = next(item for item in binding["readers"] if item["reader_id"] == "L2_cchp")
    source_path = Path(row["source"]["path"])
    source_raw = source_path.read_bytes()
    source_sha = hashlib.sha256(source_raw).hexdigest()
    assert source_sha == row["source"]["sha256"]
    source = source_raw.decode("utf-8")
    index = source.index("1.33")
    short_context = source[index - 6:index + 11]
    repetitions = source.count(short_context)
    assert len(short_context) == 17 and repetitions == 3
    row["numeric_windows"]["sigma_components"][1]["literal"] = short_context
    with tempfile.TemporaryDirectory(prefix="f9_r3_repeated_anchor_") as directory:
        path, spec_sha = helpers.save_variant(Path(directory), binding, draft)
        try:
            helpers.checked(path, spec_sha)
        except gate.ReaderGateError as exc:
            refusal = str(exc)
        else:
            raise AssertionError("R3 gate accepted threefold ambiguous CCHP anchor")
    assert refusal == "CCHP 1.33 source window lacks sys/TRGB context"
    print(json.dumps({
        "probe": "G2_REPEATED_CCHP_CONTEXT",
        "source_path": str(source_path), "source_sha256": source_sha,
        "literal": short_context, "literal_characters": len(short_context),
        "source_occurrences": repetitions,
        "result": "REFUSED", "reason": refusal,
        "binding_and_draft_mutated_only_in_temporary_directory": True,
        "observed_data_opened": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
