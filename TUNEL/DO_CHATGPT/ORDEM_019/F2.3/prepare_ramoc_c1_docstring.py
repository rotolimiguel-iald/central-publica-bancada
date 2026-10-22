"""Add the c1 probe limits to branch C's module docstring, preserving Lean code."""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "LiganteLeiCampoCurvoRamoC.lean"
NEW = HERE / "LiganteLeiCampoCurvoRamoCAuditoriaC1.lean"
SANDBOX = HERE / "kernel/TGLExt/LiganteLeiCampoCurvoRamoCAuditoriaC1.lean"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite {path}")
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=".f23_ramoc_doc_", suffix=".tmp", delete=False
    ) as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.read_bytes() != data:
        raise RuntimeError("Temporary file differs from intended bytes")
    os.rename(temporary, path)
    if path.read_bytes() != data:
        raise RuntimeError("Written file differs from intended bytes")


def main() -> None:
    source = ORIGINAL.read_bytes()
    begin = source.index(b"/-!")
    code = source.index(b"set_option autoImplicit false")
    newline = "\r\n" if b"\r\n" in source else "\n"
    doc = newline.join(
        [
            "/-!",
            "F2.3, branch C of the anti-wall tree. This remains a conditional interface.",
            "The Lorentz wedge orbit, source identification, curved conservation and",
            "H3 at every point and null direction are named inputs. No global metric",
            "or solution is constructed. The finite passage identity is already provable",
            "under its premises, so the bridge hypothesis carries H3 in full.",
            "",
            "c1 audit probes, recorded beside this pinned branch:",
            "* S-A: this exact theorem is a corollary of the audited F2.3 stone. The",
            "  proof rewrites the source by source_matches_maxwell and uses only",
            "  horizon_touch from the supplied wedge. It adds no new implication.",
            "* S-B: 'wedge at x' has no geometric anchor in this type. The region may",
            "  be the whole space and the boost acts around the origin; the same wedge",
            "  can be presented at any other x. The later phrase 'at one chart point'",
            "  names a binder and does not construct a physical Lorentz wedge family.",
            "* S-C: horizon_touch is trivial for the whole-space region.",
            "",
            "Non-vacuity has not been exhibited: neither FockCertificate nor",
            "MaxwellCertificate has a kernel inhabitant for this branch. The flat",
            "Minkowski vacuum witness S7 for the audited stone does not transfer here.",
            "The all-direction wedge family also has no exhibited inhabitant.",
            "-/",
            "",
            "",
        ]
    ).encode("utf-8")
    candidate = source[:begin] + doc + source[code:]
    if candidate[:begin] != source[:begin] or candidate[candidate.index(b"set_option autoImplicit false"):] != source[code:]:
        raise RuntimeError("Imports or Lean declarations differ")
    if NEW.exists() or SANDBOX.exists():
        raise RuntimeError("One of the new source paths already exists")
    write_new(NEW, candidate)
    write_new(SANDBOX, candidate)
    print(f"original_sha256={digest(source)}")
    print(f"new_sha256={digest(candidate)}")
    print(f"imports_and_lean_code_identical=True")
    print(f"new_source={NEW}")
    print(f"sandbox_source={SANDBOX}")


if __name__ == "__main__":
    main()
