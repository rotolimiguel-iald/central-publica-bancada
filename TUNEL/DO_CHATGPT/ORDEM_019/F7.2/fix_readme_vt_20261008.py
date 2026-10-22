"""Repair the sole VT byte in the F7.2 deployment README, with byte backup."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import os
import tempfile

path = Path(__file__).parent / "STAGING" / "README_DEPLOY.md"
old = path.read_bytes()
needle = b"project_fisica\x0b369_um_absoluto.json"
assert old.count(needle) == 1, "expected one original VT sequence"
assert old.count(b"\x0b") == 1, "unexpected VT elsewhere"
new = old.replace(needle, b"project_fisica\\v369_um_absoluto.json")
stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
backup = path.with_name(path.name + ".bak_" + stamp)
with backup.open("xb") as stream:
    stream.write(old)
    stream.flush()
    os.fsync(stream.fileno())
assert backup.read_bytes() == old
with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
    stream.write(new)
    stream.flush()
    os.fsync(stream.fileno())
    temporary = Path(stream.name)
assert temporary.stat().st_size == len(new)
assert path.read_bytes() == old, "source drifted before replace"
os.replace(temporary, path)
assert path.read_bytes() == new
print({"file": str(path), "old_sha256": sha256(old).hexdigest(), "new_sha256": sha256(new).hexdigest(), "backup": str(backup), "backup_sha256": sha256(backup.read_bytes()).hexdigest(), "old_bytes": len(old), "new_bytes": len(new)})
