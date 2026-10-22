"""Download only the pre-registered public GWOSC frames for T07(b)."""
import concurrent.futures
import hashlib
import json
import os
import threading
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PLAN_PATH = ROOT / "T07_DOWNLOAD_PLAN.json"
PLAN_RAW = PLAN_PATH.read_bytes()
PLAN = json.loads(PLAN_RAW)
assert PLAN["status"] == "PRE_DOWNLOAD_PLAN_CC_BY_4_0_PER_FILE"
assert PLAN["file_count"] == len(PLAN["files"])
assert len({f["relative_path"] for f in PLAN["files"]}) == len(PLAN["files"])
END = datetime.fromisoformat("2026-09-27T10:28:21.3284588+00:00")
LOCK = threading.Lock()
TOTAL = 0


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def reserve(size):
    global TOTAL
    with LOCK:
        TOTAL += size
        if TOTAL > PLAN["download_cap_bytes"]:
            raise RuntimeError("REGISTERED_DOWNLOAD_BYTE_CAP_EXCEEDED")


def get(item):
    if datetime.now(timezone.utc) >= END:
        return {"relative_path": item["relative_path"], "status": "DEADLINE_BEFORE_START"}
    dest = ROOT / item["relative_path"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    receipt = dest.with_name(dest.name + ".receipt.json")
    if receipt.exists():
        old = json.loads(receipt.read_bytes())
        if digest(dest) != old["sha256"] or old["url"] != item["url"]:
            raise ValueError("Existing receipt/file mismatch: " + str(dest))
        return {"relative_path": item["relative_path"], "status": "REUSED_VERIFIED", "sha256": old["sha256"], "bytes": old["bytes"]}
    if dest.exists():
        raise FileExistsError("Unreceipted data: " + str(dest))
    partial = dest.with_name(dest.name + ".part")
    if partial.exists():
        raise FileExistsError("Partial data needs audit: " + str(partial))
    req = urllib.request.Request(item["url"], headers={"User-Agent": "IALD-T07-public-research/1.0"})
    h = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(req, timeout=45) as response, partial.open("xb") as handle:
        expected = response.headers.get("Content-Length")
        while True:
            if datetime.now(timezone.utc) >= END:
                raise TimeoutError("T07_DEADLINE_DURING_DOWNLOAD")
            block = response.read(1 << 20)
            if not block:
                break
            reserve(len(block))
            handle.write(block)
            h.update(block)
            size += len(block)
    if expected is not None and int(expected) != size:
        raise IOError("HTTP_CONTENT_LENGTH_MISMATCH")
    if size == 0 or digest(partial) != h.hexdigest():
        raise IOError("EMPTY_OR_HASH_MISMATCH")
    os.rename(partial, dest)
    record = {
        "status": "PUBLIC_GWOSC_STRAIN_DOWNLOADED",
        "event": item["event"], "role": item["role"],
        "detector": item["detector"], "url": item["url"],
        "relative_path": item["relative_path"],
        "bytes": size, "sha256": h.hexdigest(),
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "plan_sha256": hashlib.sha256(PLAN_RAW).hexdigest(),
        "license_receipt": item["license_receipt"],
        "external_checksum": "not supplied by metadata; local SHA256 verified",
    }
    raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode()
    with receipt.open("xb") as handle:
        handle.write(raw)
    return {"relative_path": item["relative_path"], "status": "DOWNLOADED", "sha256": h.hexdigest(), "bytes": size}


def safe_get(item):
    try:
        out = get(item)
    except Exception as exc:
        out = {"relative_path": item["relative_path"], "status": "FAILED", "error": type(exc).__name__ + ":" + str(exc)[:200]}
    print(json.dumps(out), flush=True)
    return out


def main():
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(safe_get, PLAN["files"]))
    result = {
        "status": "T07_PUBLIC_STRAIN_DOWNLOAD_ATTEMPT",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "plan_sha256": hashlib.sha256(PLAN_RAW).hexdigest(),
        "wall_seconds": time.monotonic() - started,
        "rows": rows,
        "downloaded_bytes_in_this_process": TOTAL,
        "no_gate_change": True,
    }
    target = ROOT / "T07_DOWNLOAD_RESULT.json"
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with target.open("xb") as handle:
        handle.write(raw)
    print(json.dumps({"result_sha256": hashlib.sha256(raw).hexdigest(), "done": sum(r["status"] in ("DOWNLOADED", "REUSED_VERIFIED") for r in rows), "failed": sum(r["status"] == "FAILED" for r in rows), "bytes": TOTAL}), flush=True)


if __name__ == "__main__":
    main()
