"""One-off HDF5 external-storage refusal probe in the existing WSL runtime."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hdf5_bridge


def main() -> None:
    fixture = Path(__file__).resolve().parent.parent / "scratch_external.h5"
    code = (
        "import h5py; p=" + repr(hdf5_bridge.wsl_path(fixture)) + "; "
        "f=h5py.File(p,'w'); "
        "f.create_dataset('outside',(10,),dtype='f8',external=[('outside.bin',0,80)]); "
        "f.close()"
    )
    subprocess.run(["wsl.exe", "-e", hdf5_bridge.ENV_PYTHON, "-c", code],
                   check=True, timeout=15)
    try:
        hdf5_bridge.call(fixture, "describe")
    except ValueError as exc:
        if "External-storage HDF5 dataset refused" not in str(exc):
            raise
        print("EXTERNAL_STORAGE_REFUSED")
    else:
        raise AssertionError("External-storage HDF5 was accepted")


if __name__ == "__main__":
    main()
