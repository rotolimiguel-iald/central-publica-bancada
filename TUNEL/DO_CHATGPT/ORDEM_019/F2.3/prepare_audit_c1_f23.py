"""Create a new F2.3 source with only the c1 audit scope clarified."""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "LiganteLeiCampoCurvo.lean"
TARGET = HERE / "LiganteLeiCampoCurvoAuditoriaC1.lean"

OLD = b"""/-!\nF2.3 \xe2\x80\x94 conditional wiring of the finite passage to the curved field law.\n\nThe named H3 below is precisely the all-points, all-null-directions area/Clausius\ncondition required by AreaChart. It is NOT derived from the finite passage.\nThe arrow from the passage identity to H3 is an explicit input across different\ntypes. Chart records, conservation, topology and smooth transitions are also\nexplicit inputs. The theorem asserts an implication, not a global solution.\n-/"""

NEW = """/-!
F2.3 — conditional wiring of the curved field law; c1 audit scope.

The named H3 is an all-points, all-null-directions area/Clausius premise for the
supplied AreaChart records. The c1 sandbox probe S5 identifies its null projection
with Ric(k,k) = 8πG · T(k,k) when eta = (4G)⁻¹. H3 therefore carries physical
content. The finite-passage identity is invoked through hH3, but it is already
provable under its premises: c1 probes S2–S4 show that its occurrence is logically
idle. This theorem yields a unique Einstein coefficient on the supplied connected
smooth atlas; it does not construct that atlas.

What this theorem does not prove:
* H3 is not derived from the state, Fundacao, or the light contract.
* The identification of NamedAtlasH3 with Jacobson's H3 is [KNOWN], not a
  theorem here; the Lean name is a label.
* No Lorentz wedge family is constructed. Its all-direction requirement is
  subsumed in the named H3 premise.
* The recorded stress source is not linked to StressTensorData or
  MaxwellCertificate. Covariant conservation is an explicit record premise.
* No metric or solution, local or global, is constructed.
-/""".encode("utf-8")


def create_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite {path}")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".f23_c1_", suffix=".tmp", delete=False) as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.read_bytes() != payload:
        raise RuntimeError("Temporary source differs from intended bytes")
    os.rename(temporary, path)
    if path.read_bytes() != payload:
        raise RuntimeError("Created source differs from intended bytes")


def main() -> None:
    raw = SOURCE.read_bytes()
    if raw.count(OLD) != 1:
        raise RuntimeError("Original c1 header is not unique or differs")
    revised = raw.replace(OLD, NEW)
    create_new(TARGET, revised)
    print(f"{TARGET}\nbytes={len(revised)}\nsha256={hashlib.sha256(revised).hexdigest()}")


if __name__ == "__main__":
    main()
