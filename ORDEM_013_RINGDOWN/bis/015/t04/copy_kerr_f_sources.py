"""Make an immutable-byte starting copy of the reviewed Kerr V2 instrument."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

RING = Path(__file__).resolve().parents[3]
SOURCE = RING / "bis" / "e3_kerr_continuation"
DEST = RING / "bis" / "e3_kerr_dtau_f_015"
FILES = ("conditioning.py", "controller.py", "custody.py", "kerr_model.py",
         "runner.py", "CONFIG.json", "MANIFEST.json")


def main() -> None:
    DEST.mkdir(exist_ok=False)
    for name in FILES:
        raw = (SOURCE / name).read_bytes()
        with (DEST / name).open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        assert (DEST / name).read_bytes() == raw
        print(name, hashlib.sha256(raw).hexdigest())
    print("COPIED_BASE_NOT_EXECUTED", DEST)


if __name__ == "__main__":
    main()
