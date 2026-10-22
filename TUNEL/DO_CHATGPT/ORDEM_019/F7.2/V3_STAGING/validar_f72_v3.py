# -*- coding: utf-8 -*-
"""Read-only validation of the staged, relocatable F7.2 V3 package."""

import codecs
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
MODULE = HERE / "bancada" / "neutrino_canal_v3.py"
MANIFEST = HERE / "bancada" / "neutrino_fontes_f72_v3.json"
RECEIPT = HERE / "STAGING_RECEIPT_V3.json"
OUT = HERE / "VALIDACAO_V3_CENTRAL.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data):
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(f".{path.name}.tmp_{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if tmp.stat().st_size != len(data):
            raise OSError("temporary size differs")
        os.rename(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


receipt_raw = RECEIPT.read_bytes()
receipt = json.loads(receipt_raw.decode("utf-8"))
assert receipt["status"] == "STAGED_NOT_INSTALLED"
assert receipt["source_counts"] == {
    "scripts": 6, "primary_pdfs": 10, "documents": 8,
    "context_docs": 1, "context_pdfs": 1,
}
for relative, pin in receipt["files"].items():
    path = HERE / relative
    assert path.resolve().is_relative_to(HERE.resolve()), relative
    blob = path.read_bytes()
    assert sha(blob) == pin["sha256"] and len(blob) == pin["bytes"], relative
assert len(receipt["files"]) == 29
assert sha(MANIFEST.read_bytes()) == receipt["manifest_sha256_locked"]

spec = importlib.util.spec_from_file_location("neutrino_canal_f72_v3_staging", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.MANIFEST_SHA256 == receipt["manifest_sha256_locked"]
assert module.SOURCE_ROOT.resolve() == (HERE / "fontes_externas" / "F7.2").resolve()
codecs.lookup("utf-8-sig")  # avoid first-use stdlib codec import during the audited call
original_read_bytes = Path.read_bytes
active = False
audit_events = {"read_opens": 0, "blocked": 0}


def guard(event, args):
    if not active:
        return
    if event == "open":
        flags = args[2]
        if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            audit_events["blocked"] += 1
            raise RuntimeError("channel attempted write")
        audit_events["read_opens"] += 1
    if event == "exec" or event.startswith("socket.") or event.startswith("subprocess.") or event == "os.system":
        audit_events["blocked"] += 1
        raise RuntimeError(f"channel attempted {event}")


sys.addaudithook(guard)
active = True
try:
    output = module.canal()
finally:
    active = False
assert output["ok"] is True and output["gate_effect"] == "NONE"
assert len(output["rows"]) == 13
assert len(output["local_sources"]) == 6
assert len(output["primary_pdfs"]) == 10
assert len(output["local_documents"]) == 8
assert output["overall_verdict"] == "SEM_LIMITE_TGL"
assert output["clock_v369_context"]["statute"] == "[DERIVED]"
assert all(r["tau_star_limit_s"] is None and r["verdict"] == "SEM_LIMITE_TGL" for r in output["rows"])
assert all(r["statute"] == "[KNOWN]" for r in output["rows"] if r["published_model_limit"] is not None or r["published_observation"] is not None)
assert output["not_falsified_is_not_confirmed"] is True


def tamper_manifest(self):
    data = original_read_bytes(self)
    return data + b" " if self.resolve() == MANIFEST.resolve() else data


active = True
try:
    with patch.object(Path, "read_bytes", tamper_manifest):
        try:
            module.canal()
        except module.FonteRecusada as exc:
            assert "manifest hash differs" in str(exc)
        else:
            raise AssertionError("altered manifest was accepted")
finally:
    active = False

first_script = module.SOURCE_ROOT / "scripts" / "tgl_neutrino_decoherence.py"


def tamper_script(self):
    data = original_read_bytes(self)
    return data + b" " if self.resolve() == first_script.resolve() else data


active = True
try:
    with patch.object(Path, "read_bytes", tamper_script):
        try:
            module.canal()
        except module.FonteRecusada as exc:
            assert "source hash differs" in str(exc)
        else:
            raise AssertionError("altered June script was accepted")
finally:
    active = False

assert audit_events["blocked"] == 0
result = {
    "schema": "iald.f7_2.v3_staging_validation.v1",
    "status": "PASS",
    "receipt_sha256": sha(receipt_raw),
    "manifest_sha256": sha(MANIFEST.read_bytes()),
    "module_sha256": sha(MODULE.read_bytes()),
    "source_files_verified": 26,
    "inventory_entries_verified": len(receipt["files"]),
    "rows": len(output["rows"]),
    "read_opens_under_audit_hook": audit_events["read_opens"],
    "blocked_operations": audit_events["blocked"],
    "tampered_manifest_rejected": True,
    "tampered_script_rejected": True,
    "all_tau_star_null": True,
    "gate_effect": "NONE",
    "production_installation": False,
}
blob = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
write_new(OUT, blob)
print(json.dumps({"validation": str(OUT), "sha256": sha(blob), "status": "PASS"}, ensure_ascii=False))
