"""Copy existing rite inputs to a new sandbox, verifying bytes; never run um.py.

Claim: F1.FECHO_20261015 / event 845. No junctions/hardlinks are created.
The candidate is selected later, after independent review. This is preparation,
not a scientific result, full rite, new observation, or canonical installation.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import time

HERE = Path(__file__).resolve().parent
SHORT = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r3")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CACHE = NOS.parent / "cache"
KERNEL = NOS / "tgl_kernel"
PACKAGE_LINK = KERNEL / ".lake" / "packages"
PACKAGE_SOURCE = PACKAGE_LINK.resolve(strict=True)
MIKTEX_CONFIG = Path(r"C:\Users\rotol\AppData\Roaming\MiKTeX")
MIKTEX_DATA = Path(r"C:\Users\rotol\AppData\Local\MiKTeX")


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def exclusive_json(path, obj):
    payload = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    tmp = path.with_name(path.name + ".tmp")
    if path.exists() or tmp.exists():
        raise FileExistsError(path)
    with tmp.open("xb") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    if tmp.stat().st_size != len(payload):
        raise RuntimeError("Short write")
    tmp.rename(path)


def is_link(path):
    return path.is_symlink() or path.is_junction()


def walk(source, excludes):
    if is_link(source):
        raise RuntimeError(f"Unresolved source reparse point: {source}")
    for base, dirs, files in os.walk(source, followlinks=False):
        base = Path(base)
        rel = base.relative_to(source)
        kept = []
        for name in sorted(dirs):
            child = base / name
            child_rel = (rel / name).as_posix()
            if child_rel in excludes:
                continue
            if is_link(child):
                raise RuntimeError(f"Unexpected source reparse point: {child}")
            kept.append(name)
        dirs[:] = kept
        for name in sorted(files):
            child = base / name
            if is_link(child):
                raise RuntimeError(f"Unexpected linked source file: {child}")
            yield child, rel / name


def copy_one(item):
    group, source, target = item
    before = source.stat()
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.resolve().is_relative_to(SHORT):
        raise RuntimeError(f"Target escaped sandbox: {target}")
    if target.exists():
        digest = sha(source)
        if target.stat().st_size != before.st_size or sha(target) != digest:
            raise RuntimeError(f"Existing partial copy differs; no overwrite: {target}")
        return {"group": group, "source": str(source), "target": str(target),
                "bytes": before.st_size, "source_mtime_ns": before.st_mtime_ns,
                "sha256": digest, "destination_sha256": digest,
                "copy": "previous_partial_copy_verified_bytes"}
    tmp = target.with_name(target.name + ".copying_r6")
    h = hashlib.sha256()
    with source.open("rb") as reader, tmp.open("xb") as writer:
        for block in iter(lambda: reader.read(4 * 1024 * 1024), b""):
            h.update(block)
            writer.write(block)
    after = source.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"Source changed during copy: {source}")
    digest = h.hexdigest()
    if tmp.stat().st_size != before.st_size or sha(tmp) != digest:
        raise RuntimeError(f"Copy mismatch: {target}")
    shutil.copystat(source, tmp)
    tmp.rename(target)
    return {"group": group, "source": str(source), "target": str(target),
            "bytes": before.st_size, "source_mtime_ns": before.st_mtime_ns,
            "sha256": digest, "destination_sha256": digest,
            "copy": "ordinary_bytes_no_link"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--resume", type=Path)
    args = ap.parse_args()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    run = args.resume.resolve(strict=True) if args.resume else SHORT
    if not run.resolve() == SHORT.resolve():
        raise RuntimeError("Resume path outside this unit")
    if not args.resume:
        run.mkdir(parents=True, exist_ok=False)
    started = now()
    t0 = time.perf_counter()
    groups = [
        ("existing_observed_cache", CACHE, run / "cache", set()),
        ("kernel_sources_and_local_artifacts", KERNEL, run / "tgl_kernel", {".lake"}),
        ("kernel_build_cache", KERNEL / ".lake", run / "tgl_kernel" / ".lake", {"packages"}),
        ("resolved_lean_packages", PACKAGE_SOURCE, run / "tgl_kernel" / ".lake" / "packages", set()),
        ("miktex_user_configuration", MIKTEX_CONFIG, run / "miktex_config", set()),
        ("miktex_user_data", MIKTEX_DATA, run / "miktex_data", set()),
    ]
    plan = {"scope": "prepare_only_no_rite_execution", "unit": "F1.FECHO_20261015",
            "claim_event": 845, "short_path_scope_event": 849, "start_utc": started, "sandbox": str(run),
            "script_sha256": sha(Path(__file__)),
            "packages_source_link": str(PACKAGE_LINK),
            "packages_source_resolved": str(PACKAGE_SOURCE),
            "groups": [{"name": g, "source": str(s), "target": str(d),
                        "excluded_subtrees": sorted(e)} for g, s, d, e in groups],
            "no_new_observed_data": True, "no_network": True,
            "candidate_not_yet_selected": True,
            "no_junctions_or_hardlinks_created": True}
    exclusive_json(run / "PREPARATION_PLAN_R6.json", plan)
    print(json.dumps({"sandbox": str(run), "phase": "inventory"}), flush=True)
    items = []
    totals = {}
    for group, source, target, excludes in groups:
        totals[group] = {"files": 0, "bytes": 0}
        for p, rel in walk(source, excludes):
            items.append((group, p, target / rel))
            totals[group]["files"] += 1
            totals[group]["bytes"] += p.stat().st_size
    total_bytes = sum(v["bytes"] for v in totals.values())
    if shutil.disk_usage(HERE).free < total_bytes * 1.2:
        raise RuntimeError("Insufficient free disk for copies and generated output")
    exclusive_json(run / "ASSET_INVENTORY_R6.json", {"groups": totals,
                   "files": len(items), "bytes": total_bytes})
    print(json.dumps({"phase": "copy", "files": len(items), "bytes": total_bytes}), flush=True)
    copied = 0
    last = time.perf_counter()
    manifest = run / "COPY_MANIFEST_R6.jsonl"
    with manifest.open("x", encoding="utf-8", newline="\n") as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for record in pool.map(copy_one, items, buffersize=args.workers * 4):
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                copied += 1
                if time.perf_counter() - last > 45:
                    f.flush()
                    print(json.dumps({"copied_files": copied, "total_files": len(items),
                                     "seconds": time.perf_counter() - t0}), flush=True)
                    last = time.perf_counter()
    bad_links = []
    for base, dirs, files in os.walk(run, followlinks=False):
        for name in dirs + files:
            p = Path(base) / name
            if is_link(p):
                bad_links.append(str(p))
    if bad_links:
        raise RuntimeError(f"Unexpected links in prepared sandbox: {bad_links}")
    receipt = {**plan, "end_utc": now(), "seconds": time.perf_counter() - t0,
               "files_copied": copied, "bytes_copied": total_bytes,
               "manifest": str(manifest), "manifest_sha256": sha(manifest),
               "verified_all_destination_bytes": True, "destination_link_count": 0,
               "passed": True}
    exclusive_json(run / "PREPARATION_RECEIPT_R6.json", receipt)
    print(json.dumps({"passed": True, "sandbox": str(run),
                      "receipt": str(run / "PREPARATION_RECEIPT_R6.json")}), flush=True)


if __name__ == "__main__":
    main()
