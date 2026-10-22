"""Custodied local compatibility patch for pygsl_lite 0.1.8 source distribution."""
import hashlib
import json
import os
import tarfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
ROOT = RING / "cache" / "t14_local_deps" / "src"
EXPECTED = "3213755c71da61e9629551e088530130d28e27048cd5f3ba48deb8165e6df6de"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    api = "https://pypi.org/pypi/pygsl-lite/0.1.8/json"
    with urllib.request.urlopen(api, timeout=30) as response:
        metadata = json.load(response)
    items = [x for x in metadata["urls"] if x["filename"] == "pygsl_lite-0.1.8.tar.gz"]
    assert len(items) == 1 and items[0]["digests"]["sha256"] == EXPECTED
    with urllib.request.urlopen(items[0]["url"], timeout=60) as response:
        raw = response.read()
    assert digest(raw) == EXPECTED
    tarball = ROOT / items[0]["filename"]
    with tarball.open("xb") as f:
        f.write(raw)
    with tarfile.open(tarball, "r:gz") as archive:
        names = archive.getmembers()
        assert all(not x.issym() and not x.islnk() and not x.name.startswith("/")
                   and ".." not in Path(x.name).parts for x in names)
        archive.extractall(ROOT, filter="data")
    src = ROOT / "pygsl_lite-0.1.8" / "gsl_dist" / "swig_extension.py"
    before = src.read_bytes()
    needle = b"spawn(cmd, 1, 1)"
    assert before.count(needle) == 1
    after = before.replace(needle, b"spawn(cmd)")
    with src.open("wb") as f:
        f.write(after)
        f.flush()
        os.fsync(f.fileno())
    receipt = dict(status="LOCAL_THIRD_PARTY_COMPATIBILITY_PATCH",
                   created_utc=datetime.now(timezone.utc).isoformat(),
                   PyPI_api=api, source_sha256=EXPECTED,
                   source_url=items[0]["url"],
                   source_bytes=len(raw), patched_file="gsl_dist/swig_extension.py",
                   original_file_sha256=digest(before), patched_file_sha256=digest(after),
                   old_call="spawn(cmd, 1, 1)", new_call="spawn(cmd)",
                   scope="Python 3.12/setuptools signature compatibility, not a physics modification",
                   official_package_unchanged=False, gate_changed=False)
    target = HERE / "T14_B_PATCH_RECEIPT.json"
    with target.open("xb") as f:
        f.write((json.dumps(receipt, indent=2) + "\n").encode())
    print(json.dumps({"status": receipt["status"], "source_sha256": EXPECTED,
                      "patched_file_sha256": receipt["patched_file_sha256"]}))


if __name__ == "__main__":
    main()
