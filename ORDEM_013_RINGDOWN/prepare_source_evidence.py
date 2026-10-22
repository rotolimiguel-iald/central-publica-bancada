"""Freeze nonlinear evidence inputs without modifying previous experiments."""
from pathlib import Path
import hashlib
import json
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "cache/source_evidence"


def main():
    if DEST.exists():
        raise FileExistsError("Preserve registered work; do not reinitialize")
    DEST.mkdir()
    source = ROOT / "cache/nonlinear_intrinsic_peak"
    names = ["coherent_imr_model.py", "coherent_imr_likelihood.py", "tgl_ringdown_prediction.py",
             "tgl_ringdown_likelihood.py", "QNM_GRID.json", "REGISTRO_C6.json"]
    provenance = []
    for name in names:
        src = source / name
        shutil.copyfile(src, DEST / name)
        provenance.append(dict(source=str(src), destination=name,
                               sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
    (DEST / "cache/recolored_noise").mkdir(parents=True)
    for psd in ("O4", "O5"):
        src = ROOT / f"cache/recolored_noise/{psd}_noise.npz"
        dst = DEST / f"cache/recolored_noise/{psd}_noise.npz"
        shutil.copyfile(src, dst)
        provenance.append(dict(source=str(src), destination=dst.relative_to(DEST).as_posix(),
                               sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
    data = dict(date_utc=datetime.now(timezone.utc).isoformat(), inputs=provenance,
                scope="Byte copies of the verified intrinsic-22 peak model and previously frozen noise")
    raw = (json.dumps(data, indent=2)+"\n").encode()
    tmp = DEST / "PROVENANCE.json.tmp"
    tmp.write_bytes(raw)
    assert tmp.stat().st_size == len(raw)
    tmp.replace(DEST / "PROVENANCE.json")
    print(json.dumps(dict(destination=str(DEST), files=len(provenance))))


if __name__ == "__main__":
    main()
