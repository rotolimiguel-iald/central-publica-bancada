"""Read-only source probe for the F1.3 dependency graph."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
INVENTORY = Path(r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.md")
SOURCES = {
    "inventory": (INVENTORY, [(20, 72), (1213, 1224), (1673, 1684), (2041, 2052), (2711, 2723), (2764, 2776), (2809, 2825), (2844, 2856)]),
    "toolchain": (ROOT / "lean-toolchain", [(1, 3)]),
    "manifest": (ROOT / "lake-manifest.json", []),
    "LightOneParticleByTerm": (ROOT / "TGLExt/LightOneParticleByTerm.lean", [(1, 30), (250, 300)]),
    "QGSolutionComplete": (ROOT / "TGLExt/QGSolutionComplete.lean", [(50, 74), (120, 140)]),
    "TheImportedSecondQuantization": (ROOT / "TGLExt/TheImportedSecondQuantization.lean", [(75, 140), (185, 235), (365, 386)]),
    "ClosedAntilinearStandardSubspace": (ROOT / "TGLExt/ClosedAntilinearStandardSubspace.lean", [(195, 228)]),
    "GenericAntilinearAdjoint": (ROOT / "TGLExt/GenericAntilinearAdjoint.lean", [(60, 84)]),
    "ContinuousModularReconstruction": (ROOT / "TGLExt/ContinuousModularReconstruction.lean", [(78, 103), (118, 153)]),
    "V351FourierTranslation": (ROOT / "TGLExt/V351FourierTranslation.lean", [(42, 64)]),
    "FourierStandardTransport_v3": (ROOT / "TGLExt/O16/FourierStandardTransport_v3.lean", [(20, 48)]),
    "OrbitalRapidityMeasure_v4": (ROOT / "TGLExt/O16/OrbitalRapidityMeasure_v4.lean", [(12, 26)]),
    "OrbitalL2Equivalence_v2": (ROOT / "TGLExt/O16/OrbitalL2Equivalence_v2.lean", [(23, 62)]),
    "OrbitalRapidityTransport_v3": (ROOT / "TGLExt/O16/OrbitalRapidityTransport_v3.lean", [(12, 20), (70, 82)]),
    "OrbitalBoostTransport": (ROOT / "TGLExt/O16/OrbitalBoostTransport.lean", [(37, 65)]),
    "OrbitalBoostUnitary_v2": (ROOT / "TGLExt/O16/OrbitalBoostUnitary_v2.lean", [(11, 29)]),
    "LightRayGaussianDensity_v2": (ROOT / "TGLExt/O16/LightRayGaussianDensity_v2.lean", [(35, 60)]),
    "FourierLightRayBridge": (ROOT / "TGLExt/O16/FourierLightRayBridge.lean", [(60, 83)]),
    "RetaDeLuzBorchers": (ROOT / "TGLExt/RetaDeLuzBorchers.lean", [(182, 205)]),
    "KMSStripConditional": (ROOT / "TGLExt/O16/KMSStripConditional.lean", [(40, 82)]),
    "FiniteCrossedProduct": (ROOT / "TGLExt/FiniteCrossedProduct.lean", [(1, 40)]),
}


def main() -> None:
    result = {}
    for name, (path, ranges) in SOURCES.items():
        raw = path.read_bytes()
        lines = raw.decode("utf-8-sig").splitlines()
        result[name] = {
            "path": str(path),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "excerpts": [
                {"start": start, "end": end, "lines": [f"{n}: {lines[n - 1]}" for n in range(start, min(end, len(lines)) + 1)]}
                for start, end in ranges
            ],
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
