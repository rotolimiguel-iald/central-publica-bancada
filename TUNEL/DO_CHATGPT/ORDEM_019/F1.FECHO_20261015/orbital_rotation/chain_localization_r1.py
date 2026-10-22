"""Wait for exact in-flight dependency sources, then build two new consumers once.
No retries, source edits, state promotion or production writes are performed.
Every compiler attempt retains the existing builder's immutable receipts.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
DEPENDENCIES = ["PhysicalWedgeNullGeometryR3", "RegularSemigroupClosureR3"]
CONSUMERS = ["PhysicalWedgeGroupInvariantR3", "PhysicalWedgeSchwartzClosureR2"]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def exact_receipts(mod):
    wanted = digest(BASE / (mod + ".lean"))
    result = []
    for rp in sorted((BASE / "attempts").glob("*/RECEIPT.json")):
        r = json.loads(rp.read_bytes())
        if Path(r["source"]["path"]).stem == mod and r["source"]["sha256"] == wanted:
            result.append((rp, r))
    return result

for mod in CONSUMERS:
    if exact_receipts(mod):
        raise RuntimeError("Existing consumer attempt refused: " + mod)

print("Waiting for exact dependency receipts; no duplicate compiler launched.", flush=True)
pending = set(DEPENDENCIES)
deadline = time.monotonic() + 7200
while pending:
    if time.monotonic() > deadline:
        raise TimeoutError("Dependency wait expired without starting consumers")
    for mod in list(pending):
        rs = exact_receipts(mod)
        if not rs:
            continue
        rp, r = rs[-1]
        if r["exit_code"] or not r["readonly_dependencies_unchanged"]:
            raise RuntimeError("Dependency failed; consumers not started: " + str(rp))
        print("Dependency accepted: " + mod + " " + str(rp), flush=True)
        pending.remove(mod)
    if pending:
        time.sleep(5)

for mod in CONSUMERS:
    if exact_receipts(mod):
        raise RuntimeError("Concurrent consumer attempt refused: " + mod)
    print("BUILDING " + mod, flush=True)
    r = subprocess.run([sys.executable, "-B", "-X", "utf8",
                        str(BASE / "build_orbital_r3.py"), mod + ".lean"],
                       cwd=BASE, check=False)
    if r.returncode:
        raise SystemExit(r.returncode)
print("Both localized consumers compiled; inspect their receipts before claiming scope.", flush=True)
