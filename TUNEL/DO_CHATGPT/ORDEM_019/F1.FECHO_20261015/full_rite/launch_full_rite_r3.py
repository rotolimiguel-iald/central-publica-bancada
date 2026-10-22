"""Run the unmodified candidate's REAL main, retaining all tests and outputs.

No baseline core injection, no monkeypatch of scientific functions, no skipped
formal selftest, no production installation. Native tooling is not OS-isolated
by the Python hook; its explicit environment and paths are recorded separately.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
ROOT = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r3")
PYTHON = Path(r"C:\Python314\python.exe")


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def save(path, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    tmp = path.with_name(path.name + ".tmp")
    if path.exists() or tmp.exists():
        raise FileExistsError(path)
    with tmp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.stat().st_size == len(raw)
    tmp.rename(path)


def copy_new(source, target):
    raw = source.read_bytes()
    with target.open("xb") as f:
        f.write(raw)
    assert sha(target) == hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="Launch after reviewed preflight")
    args = ap.parse_args()
    prep = json.loads((ROOT / "PREPARATION_RECEIPT_R5.json").read_text(encoding="utf-8"))
    pre = json.loads((ROOT / "ENVIRONMENT_PREFLIGHT_R4.json").read_text(encoding="utf-8"))
    integration_path = UNIT / "INTEGRATION_QUADRATIC_R3.json"
    integration = json.loads(integration_path.read_text(encoding="utf-8"))
    candidate = Path(integration["candidate"]["path"])
    assert prep["passed"] and prep["destination_link_count"] == 0
    assert pre["all_probes_exit_zero"]
    assert sha(candidate) == sha(ROOT / "um.py") == integration["candidate"]["sha256"]
    if sha(Path(prep["manifest"])) != prep["manifest_sha256"]:
        raise RuntimeError("Preparation manifest changed")
    env = os.environ.copy()
    for key in pre["unset"]:
        env.pop(key, None)
    env.update(pre["overrides"])
    guard_dir = ROOT / "environment" / "guard"
    guard_dir.mkdir(exist_ok=True)
    guard = guard_dir / "sitecustomize.py"
    guard_src = HERE / "sitecustomize_rite_r3.py"
    if not guard.exists():
        copy_new(guard_src, guard)
    if sha(guard) != sha(guard_src):
        raise RuntimeError("Guard changed after preparation")
    env.update({"PYTHONPATH": str(guard_dir), "TGL_RITE_SANDBOX": str(ROOT),
                "TGL_RITE_GUARD_PHASE": "preflight"})
    guard_receipt = ROOT / "GUARD_PREFLIGHT.json"
    if not guard_receipt.exists():
        code = """import json,os,socket,subprocess
from pathlib import Path
root=Path(os.environ['TGL_RITE_SANDBOX'])
checks=[]
try:
    with open(root.parent/'rite_guard_outside_probe.tmp','x') as f:f.write('guard failed')
    checks.append(False)
except PermissionError:checks.append(True)
try:
    socket.create_connection(('127.0.0.1',9),timeout=.1)
    checks.append(False)
except PermissionError:checks.append(True)
try:
    subprocess.run(['cmd.exe','/c','echo','guard failed'],capture_output=True)
    checks.append(False)
except PermissionError:checks.append(True)
with open(root/'environment'/'inside_guard_probe.txt','x') as f:f.write('inside sandbox')
print(json.dumps({'checks':checks,'passed':len(checks)==3 and all(checks)}))
"""
        cmd = [str(PYTHON), "-B", "-X", "utf8", "-c", code]
        started, t0 = now(), time.perf_counter()
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        try:
            verdict = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            verdict = {"passed": False}
        save(guard_receipt, {"start_utc": started, "end_utc": now(),
                            "seconds": time.perf_counter() - t0, "command": cmd,
                            "exit_code": r.returncode, "stdout": r.stdout,
                            "stderr": r.stderr, "result": verdict,
                            "guard_source_sha256": sha(guard_src)})
    gr = json.loads(guard_receipt.read_text(encoding="utf-8"))
    assert gr["exit_code"] == 0 and gr["result"]["passed"]
    assert gr["guard_source_sha256"] == sha(guard_src)
    if not args.run:
        print(json.dumps({"ready": True, "rite_started": False,
                          "candidate_sha256": sha(candidate)}))
        return
    forbidden_outputs = ["um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_pt.pdf",
                         "um_absoluto_en.pdf", "RITE_STARTED.json", "RITE_RECEIPT.json"]
    if any((ROOT / name).exists() for name in forbidden_outputs):
        raise RuntimeError("Scientific output folder is not fresh; refusing overwrite")
    # Authoritative independent component review remains external evidence.
    review_path = UNIT / "quadratic_review" / "INTEGRATION_REVIEW_R2.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    assert review["status"] == "PASSA_COMPONENTE_INTEGRADO_AGUARDA_RITO_INTEGRAL"
    assert review["candidate"]["sha256"] == sha(candidate)
    assert review["integration"]["sha256"] == sha(integration_path)
    assert review["ladder"]["all_verified"] and review["ladder"]["clean"] == 7171
    engine_preflight = json.loads((ROOT / "ENGINE_PREFLIGHT_RECEIPT.json").read_text(encoding="utf-8"))
    assert engine_preflight["passed"] and engine_preflight["exit_code"] == 0
    assert engine_preflight["guard_source_sha256"] == sha(guard_src)
    env["TGL_RITE_GUARD_PHASE"] = "actual"
    command = [str(PYTHON), "-u", "-B", "-X", "utf8", str(ROOT / "um.py")]
    t0, started = time.perf_counter(), now()
    log_path = ROOT / "RITE_STDOUT_STDERR.log"
    with log_path.open("xb") as log:
        proc = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.PIPE,
                                stdout=log, stderr=subprocess.STDOUT)
        start_rec = {"start_utc": started, "command": command, "stdin": "1\\n",
                     "cwd": str(ROOT), "pid": proc.pid,
                     "candidate": {"path": str(candidate), "sha256": sha(candidate)},
                     "execution_copy_sha256": sha(ROOT / "um.py"),
                     "environment_overrides": pre["overrides"], "environment_unset": pre["unset"],
                     "pythonpath_guard": str(guard), "guard_sha256": sha(guard),
                     "review": {"path": str(review_path), "sha256": sha(review_path)},
                     "preparation_receipt_sha256": sha(ROOT / "PREPARATION_RECEIPT_R5.json"),
                     "full_main_unmodified": True, "baseline_core_injected": False,
                     "whole_rite_requested": True, "native_OS_containment_claimed": False,
                     "data_scope": "Replay historical admitted inputs; no new opening. Fase9 reexecutes only the frozen verdict on the historical input; v376 Coma re-reads the previously revealed 19-Aug reference; void/KiDS repeat the previous admitted calculations.",
                     "script_sha256": sha(Path(__file__))}
        save(ROOT / "RITE_STARTED.json", start_rec)
        print(json.dumps({"phase": "actual_rite_started", "pid": proc.pid,
                          "start_utc": started, "log": str(log_path)}), flush=True)
        proc.communicate(input=b"1\n")
        rc = proc.returncode
    ended = now()
    reads, refusals, processes = {}, [], []
    for path in sorted((ROOT / "environment" / "guard_logs" / "actual").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            if record["kind"] == "EXTERNAL_READ_BEFORE":
                key = os.path.normcase(record["path"])
                reads.setdefault(key, record)
            elif record["kind"] == "REFUSAL":
                refusals.append(record)
            elif record["kind"] == "PROCESS":
                processes.append(record)
    changes = []
    for record in reads.values():
        p = Path(record["path"])
        record["sha256_after"] = sha(p) if p.is_file() else None
        record["unchanged"] = record["sha256_after"] == record["sha256"]
        if not record["unchanged"]:
            changes.append(record)
    save(ROOT / "EXTERNAL_INPUTS_BEFORE_AFTER.json", list(reads.values()))
    save(ROOT / "ACTUAL_GUARD_REFUSALS.json", refusals)
    save(ROOT / "ACTUAL_CHILD_PROCESSES.json", processes)
    outputs = []
    for name in ["um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_pt.tex",
                 "um_absoluto_en.tex", "um_absoluto_pt.pdf", "um_absoluto_en.pdf"]:
        p = ROOT / name
        outputs.append({"path": str(p), "exists": p.exists(),
                        "sha256": sha(p) if p.is_file() else None,
                        "bytes": p.stat().st_size if p.is_file() else None})
    receipt = {**start_rec, "end_utc": ended, "seconds": time.perf_counter() - t0,
               "exit_code": rc, "log_sha256": sha(log_path),
               "external_input_count": len(reads), "external_inputs_unchanged": not changes,
               "guard_refusal_count": len(refusals), "child_process_count": len(processes),
               "candidate_original_unchanged": sha(candidate) == start_rec["candidate"]["sha256"],
               "execution_copy_unchanged": sha(ROOT / "um.py") == start_rec["execution_copy_sha256"],
               "outputs": outputs,
               "scientific_review_required": True,
               "process_completed_zero": rc == 0,
               "gate_installation_or_publication": False}
    save(ROOT / "RITE_RECEIPT.json", receipt)
    print(json.dumps({"phase": "actual_rite_finished", "exit_code": rc,
                      "seconds": receipt["seconds"], "guard_refusals": len(refusals),
                      "external_inputs_changed": len(changes),
                      "receipt": str(ROOT / "RITE_RECEIPT.json")}), flush=True)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
