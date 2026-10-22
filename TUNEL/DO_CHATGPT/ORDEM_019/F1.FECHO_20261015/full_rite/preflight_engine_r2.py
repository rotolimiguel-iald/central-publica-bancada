"""Run the actual existing E1--E8 engine under the retry's exact IO guard."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import time

HERE = Path(__file__).resolve().parent
OLD = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015")
ROOT = OLD / "r2"
PYTHON = Path(r"C:\Python314\python.exe")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    temp = path.with_name(path.name + ".tmp")
    if path.exists():
        raise FileExistsError(path)
    with temp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert temp.stat().st_size == len(raw)
    temp.rename(path)

pre = json.loads((ROOT / "ENVIRONMENT_PREFLIGHT_R3.json").read_text(encoding="utf-8"))
env = os.environ.copy()
for key in pre["unset"]:
    env.pop(key, None)
env.update(pre["overrides"])
env.update(PYTHONPATH=str(ROOT / "environment" / "guard"),
           TGL_RITE_SANDBOX=str(ROOT), TGL_RITE_GUARD_PHASE="preflight")
work = ROOT / "engine_preflight"
work.mkdir()
sources = []
for name in ["pilar_quantico_worker.py", "pilar_quantico_spec.json"]:
    original = OLD / "quantum_pillar" / name
    target = work / name
    raw = original.read_bytes()
    with target.open("xb") as f:
        f.write(raw)
    assert sha(original) == sha(target)
    sources.append({"path": str(target), "source": str(original), "sha256": sha(target)})
spec = json.loads((work / "pilar_quantico_spec.json").read_text(encoding="utf-8"))
assert spec["worker_sha256"] == sha(work / "pilar_quantico_worker.py")
command = [str(PYTHON), "-u", "-B", "-X", "utf8", str(work / "pilar_quantico_worker.py"),
           "--mode", "engine", "--spec", str(work / "pilar_quantico_spec.json"),
           "--out", str(work / "outputs")]
t0 = time.perf_counter()
start = dt.datetime.now(dt.timezone.utc).isoformat()
with (work / "ENGINE_STDOUT_STDERR.log").open("xb") as log:
    process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    print(json.dumps({"phase": "engine_preflight_started", "pid": process.pid, "start_utc": start}), flush=True)
    rc = process.wait(timeout=600)
end = dt.datetime.now(dt.timezone.utc).isoformat()
result_path = work / "outputs" / "result.json"
result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}
receipt = {
    "command": command, "cwd": str(ROOT), "pid": process.pid,
    "start_utc": start, "end_utc": end, "seconds": time.perf_counter() - t0,
    "exit_code": rc, "sources": sources,
    "guard_source_sha256": sha(HERE / "sitecustomize_rite_r2.py"),
    "result": {"path": str(result_path), "sha256": sha(result_path) if result_path.exists() else None},
    "verdict": result.get("verdict"), "engine_selftest": result.get("engine_selftest"),
    "passed": rc == 0 and result.get("verdict") == "ENGINE_SELFTEST_PASSED"
              and result.get("engine_selftest", {}).get("all_ok") is True,
    "scope": "Actual existing engine E1-E8 only; not the full quantum pillar recomputation nor full um.py rite",
    "environment_overrides": pre["overrides"], "environment_unset": pre["unset"],
}
save(ROOT / "ENGINE_PREFLIGHT_RECEIPT.json", receipt)
print(json.dumps({"phase": "engine_preflight_finished", "passed": receipt["passed"],
                  "exit_code": rc, "seconds": receipt["seconds"], "verdict": receipt["verdict"]}), flush=True)
raise SystemExit(0 if receipt["passed"] else 1)
