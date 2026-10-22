"""Prepared F7.2 V2 disk deployment. Never reloads MCP or changes a gate.

Default invocation is read-only. A c1-reviewed invocation with --apply may add
the versioned channel beside V1. Any drift from the audited MCP baseline fails.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile


STAGE = Path(__file__).resolve().parent
UNIT = STAGE.parent
BANCADA = Path(r"C:\IALD\Bancada_Um")
SOURCES = {
    "module": (STAGE / "bancada" / "neutrino_canal_v2.py",
               "252de897ee9e43944cffc9adebe38da14aba6c2736e4cbb56e472f000ad159e5"),
    "manifest": (STAGE / "bancada" / "neutrino_fontes_f72_v2.json",
                 "b7beff016f070ba8bb4aa40866d512c885e9d2197703954cfad05137bfb29131"),
    "mcp_v2": (STAGE / "mcp_um_v2.py",
               "5da9a9fbd777cb7114e4f7cf84d735310044af46ac0c3d1817f73ab096a40a4d"),
    "juno_pdf": (STAGE / "fontes_primarias" / "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf",
                 "9212cd391d88846ee8065ac3ebf8ccb17be297417a86a22482fca858ed3be107"),
    "table_v2": (STAGE / "TABELA_DE_PODER_POR_CANAL_V2.md",
                 "f2376aea770e877dd43dead67d186a2da326e4ae7076b2f66574a0d00bccd5fd"),
    "juno_custody": (STAGE / "JUNO_SOURCE_CUSTODY.json",
                     "e612ed7ada21723cd2701a4923fde300c88513f15be3336d00c8f39113777bad"),
    "mcp_v1": (UNIT / "STAGING" / "mcp_um.py",
               "efe6673e7e07519b51ababff4e0cd1f8430d78edad8d9014ef3a697a697e3e32"),
}
TARGETS = {
    "module": BANCADA / "bancada" / "neutrino_canal_v2.py",
    "manifest": BANCADA / "bancada" / "neutrino_fontes_f72_v2.json",
    "mcp_v2": BANCADA / "mcp_um.py",
}


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def checked_sources() -> dict[str, bytes]:
    result = {}
    for label, (path, expected) in SOURCES.items():
        blob = path.read_bytes()
        if digest(blob) != expected:
            raise ValueError(f"staging source drift: {label}")
        result[label] = blob
    manifest = json.loads(result["manifest"].decode("utf-8"))
    if (manifest.get("schema") != "iald.f7_2.channel_sources.v3"
            or len(manifest.get("primary_pdfs", [])) != 10
            or manifest.get("raw_experimental_data_custodied") is not False):
        raise ValueError("V2 manifest scope/count mismatch")
    module = result["module"].decode("utf-8")
    if (SOURCES["manifest"][1] not in module
            or SOURCES["juno_pdf"][1] not in module
            or "tau_star_limit_s\": None" not in module):
        raise ValueError("V2 module pins or null bound missing")
    original = ast.parse(result["mcp_v1"].decode("utf-8"))
    proposed = ast.parse(result["mcp_v2"].decode("utf-8"))
    before = {node.name: ast.dump(node) for node in original.body
              if isinstance(node, ast.FunctionDef)}
    after = {node.name: ast.dump(node) for node in proposed.body
             if isinstance(node, ast.FunctionDef)}
    if (not set(before).issubset(after)
            or any(after[name] != shape for name, shape in before.items())
            or set(after) - set(before) != {"neutrino_canal_f72_v2"}):
        raise ValueError("MCP proposal is not additive to V1")
    return result


def current_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def preflight(blobs: dict[str, bytes]) -> tuple[dict, dict[str, bytes | None]]:
    states = {}
    snapshots = {}
    for label in ("module", "manifest"):
        path = TARGETS[label]
        current = current_bytes(path)
        snapshots[label] = current
        if current is not None and current != blobs[label]:
            raise ValueError(f"unexpected existing V2 target: {path}")
        states[label] = "already_present" if current is not None else "to_create"
    mcp = TARGETS["mcp_v2"]
    current = current_bytes(mcp)
    snapshots["mcp_v2"] = current
    if current == blobs["mcp_v2"]:
        states["mcp_v2"] = "already_present"
    elif current == blobs["mcp_v1"]:
        states["mcp_v2"] = "to_add"
    else:
        raise ValueError("live MCP differs from audited V1 or V2; c1 must rebase")
    return states, snapshots


def atomic_replace(path: Path, blob: bytes, expected_prior: bytes | None) -> str | None:
    prior = current_bytes(path)
    if prior != expected_prior:
        raise ValueError(f"concurrent target drift before backup: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if prior is not None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
        backup_path = path.with_name(path.name + ".bak_" + stamp)
        with backup_path.open("xb") as stream:
            stream.write(prior)
            stream.flush()
            os.fsync(stream.fileno())
        if backup_path.read_bytes() != prior:
            raise OSError(f"byte backup mismatch: {path}")
        backup = str(backup_path)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".",
                                     suffix=".tmp", delete=False) as stream:
        stream.write(blob)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.stat().st_size != len(blob):
        temporary.unlink(missing_ok=True)
        raise OSError(f"temporary size mismatch: {path}")
    # User-space byte CAS immediately before the atomic replacement.
    if current_bytes(path) != expected_prior:
        temporary.unlink(missing_ok=True)
        raise ValueError(f"concurrent target drift before replace: {path}")
    os.replace(temporary, path)
    if path.read_bytes() != blob:
        raise OSError(f"installed bytes mismatch: {path}")
    return backup


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Only c1 should use this after reviewing staging and the live baseline")
    args = parser.parse_args()
    blobs = checked_sources()
    states, snapshots = preflight(blobs)
    result = {"unit": "F7.2", "stage": "V2", "preflight": states,
              "mcp_process_reloaded": False, "gate_effect": "NONE"}
    if not args.apply:
        result["status"] = "PLAN_ONLY_NO_WRITES"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    backups = {}
    for label in ("module", "manifest", "mcp_v2"):
        if states[label] in ("to_create", "to_add"):
            backups[label] = atomic_replace(TARGETS[label], blobs[label], snapshots[label])
    for label in ("module", "manifest", "mcp_v2"):
        if current_bytes(TARGETS[label]) != blobs[label]:
            raise ValueError(f"post-install target drift: {label}")
    result.update(status="INSTALLED_ON_DISK_PROCESS_NOT_RELOADED", backups=backups,
                  cas_byte_checked=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
