"""Create an additive Temperature candidate without unused observer boost fields."""

from __future__ import annotations

from pathlib import Path
import os


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "LiganteLeiCampoCurvoTemperaturaStandalone.lean"
NAME = "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean"
TARGETS = (ROOT / NAME, ROOT / "kernel" / "TGLExt" / NAME)


def replace_once(data: bytes, old: bytes, new: bytes) -> bytes:
    if data.count(old) != 1:
        raise RuntimeError(f"Expected one exact occurrence, found {data.count(old)}: {old[:70]!r}")
    return data.replace(old, new, 1)


def exclusive_bytes(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


if __name__ == "__main__":
    if any(path.exists() for path in TARGETS):
        raise FileExistsError(TARGETS)
    data = SOURCE.read_bytes()
    data = replace_once(
        data,
        b"attached to the *same supplied light wedge* through observer_boost_eq.\n",
        b"defined relative to the *supplied* wedge, without an unused observer boost field.\n",
    )
    data = replace_once(
        data,
        b"/-- A named reading on the same wedge, with observer time t mapped to\n    boost rapidity rate*t. Faithfulness concerns the angular reading\n    Circle.exp(rate*t), not a global Lorentz action or KMS state. -/",
        b"/-- A named reading on a supplied wedge. The positive rate remains freely\n    chosen; faithfulness concerns Circle.exp(rate*t), not a global Lorentz\n    action or a KMS state. The H3 bridge remains a named input. -/",
    )
    data = replace_once(
        data,
        b"  observer_boost : \u211d \u2192 Matrix (Fin 4) (Fin 4) \u211d\n  observer_boost_eq : \u2200 t, observer_boost t = wedge.boost (rate * t)\n".decode("unicode_escape").encode("utf-8"),
        b"",
    )
    for path in TARGETS:
        exclusive_bytes(path, data)
        if path.read_bytes() != data:
            raise RuntimeError(f"Bytes differ after exclusive write: {path}")
    print("created", *TARGETS, sep="\n")
