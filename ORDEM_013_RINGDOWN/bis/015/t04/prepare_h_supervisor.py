"""Copy the qualified C supervisor to one witnessed H supervisor, unchanged otherwise."""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "supervise_t04_c.py"
DESTINATION = HERE / "supervise_t04_h.py"
REPLACEMENTS = (
    ("choices=['branch_c']", "choices=['branch_h']"),
    ("GW250114_PILOT_V2_S220_C1", "GW250114_PILOT_V2_S220_H1"),
    ("item='T04_branch_C'", "item='T04_branch_H'"),
    ("Branch C already reserved; inspect instead of retry", "Branch H already reserved; inspect instead of retry"),
    ("Budgeted T04 branch-C supervisor", "Budgeted T04 branch-H supervisor"),
)


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    text = source_bytes.decode("utf-8")
    for before, after in REPLACEMENTS:
        if text.count(before) != 1:
            raise ValueError(f"Replacement not unique: {before}")
        text = text.replace(before, after)
    if "branch_c" in text or "T04_branch_C" in text or "PILOT_V2_S220_C1" in text:
        raise ValueError("C branch identifier remains")
    ast.parse(text, filename=str(DESTINATION))
    data = text.encode("utf-8")
    with DESTINATION.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert DESTINATION.read_bytes() == data
    print(dict(status="H_SUPERVISOR_COPIED_NOT_EXECUTED",
               source_sha256=hashlib.sha256(source_bytes).hexdigest(),
               h_sha256=hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
