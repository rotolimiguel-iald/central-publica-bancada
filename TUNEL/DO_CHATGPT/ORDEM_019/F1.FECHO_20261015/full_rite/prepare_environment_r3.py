"""Prepare and inspect the real rite environment; does not import or run um.py."""
from __future__ import annotations
import argparse
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
PYTHON = Path(r"C:\Python314\python.exe")
LEAN_BIN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin")
MIKTEX_ROOT = Path(r"C:\Users\rotol\AppData\Local\Programs\MiKTeX")
MIKTEX_BIN = MIKTEX_ROOT / "miktex" / "bin" / "x64"


def sha(p):
    with Path(p).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def save(p, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    tmp = p.with_name(p.name + ".tmp")
    if p.exists() or tmp.exists():
        raise FileExistsError(p)
    with tmp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.stat().st_size == len(raw)
    tmp.rename(p)


def copy_new(src, dest):
    before = sha(src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("xb") as out, src.open("rb") as inp:
        shutil.copyfileobj(inp, out, 4 * 1024 * 1024)
    assert sha(dest) == before == sha(src)
    return {"source": str(src), "path": str(dest), "sha256": before,
            "bytes": dest.stat().st_size}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sandbox", type=Path)
    args = ap.parse_args()
    root = args.sandbox.resolve(strict=True)
    if root != Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r2").resolve():
        raise RuntimeError("Sandbox escaped unit")
    integration = UNIT / "INTEGRATION_QUADRATIC_R3.json"
    data = json.loads(integration.read_text(encoding="utf-8"))
    candidate = Path(data["candidate"]["path"])
    assert sha(candidate) == data["candidate"]["sha256"]
    candidate_copy = copy_new(candidate, root / "um.py")
    envroot = root / "environment"
    for name in ["tmp", "matplotlib", "torch", "cuda", "triton", "torchinductor", "miktex_logs", "guard_logs"]:
        (envroot / name).mkdir(parents=True, exist_ok=True)
    config = root / "miktex_config" / "miktex" / "config" / "miktex.ini"
    config.parent.mkdir(parents=True, exist_ok=True)
    if config.exists():
        raise RuntimeError("Unexpected copied MiKTeX config; review before append")
    config.write_text("[MPM]\nAutoInstall = f\n\n[Core]\nShellCommandMode = Forbidden\n"
                      f"UserLogDirectory = {envroot / 'miktex_logs'}\n"
                      f"TempDir = {envroot / 'tmp'}\n", encoding="utf-8")
    bench = root / "bench_documents"
    original_bench = Path(r"C:\IALD\Central de Patentes\Chatgpt")
    tree = ast.parse(candidate.read_text(encoding="utf-8"))
    bench_records = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(x, ast.Name) and x.id in
            {"_V365_BENCH_TEXTS", "_V370_BENCH_TEXTS"} for x in node.targets):
            for rel in ast.literal_eval(node.value):
                src = original_bench / rel
                if src.is_file():
                    bench_records.append(copy_new(src, bench / rel))
                else:
                    bench_records.append({"source": str(src), "missing_in_origin": True})
    overrides = {
        "TGL_CACHE_DIR": str(root / "cache"), "TGL_BENCH_ROOT": str(bench),
        "TGL_LAKE": str(LEAN_BIN / "lake.exe"), "TGL_FORMAL_MODE": "strict",
        "TGL_NO_NETWORK": "1", "TGL_VOID_NO_NETWORK": "1",
        "TGL_COMA_MODE": "report", "TGL_COMA_REVEAL": "0",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1",
        "TEMP": str(envroot / "tmp"), "TMP": str(envroot / "tmp"),
        "TMPDIR": str(envroot / "tmp"), "MPLCONFIGDIR": str(envroot / "matplotlib"),
        "TRITON_CACHE_DIR": str(envroot / "triton"), "TORCHINDUCTOR_CACHE_DIR": str(envroot / "torchinductor"),
        "TORCH_HOME": str(envroot / "torch"), "CUDA_CACHE_PATH": str(envroot / "cuda"),
        "MIKTEX_USERCONFIG": str(root / "miktex_config"),
        "MIKTEX_USERDATA": str(root / "miktex_data"),
        "MIKTEX_USERINSTALL": str(MIKTEX_ROOT),
        "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "protocol.allow",
        "GIT_CONFIG_VALUE_0": "never", "GIT_TERMINAL_PROMPT": "0",
        "CUBLAS_WORKSPACE_CONFIG": ":4096:8",
    }
    unset = ["TGL_RITE_CHECKPOINT", "TGL_SKIP_SELFTEST", "TGL_KERNEL_PREBUILT",
             "LEAN_PATH", "LAKE_HOME", "PYTHONPATH"]
    env = os.environ.copy()
    for k in unset:
        env.pop(k, None)
    env.update(overrides)
    probes = []
    commands = [
        [str(PYTHON), "-B", "-X", "utf8", "-c",
         "import json,platform,torch,numpy,scipy;ok=torch.cuda.is_available();print(json.dumps({'torch':torch.__version__,'cuda':torch.version.cuda,'numpy':numpy.__version__,'scipy':scipy.__version__,'python':platform.python_version(),'gpu':torch.cuda.get_device_name(0) if ok else None}))"],
        [r"C:\WINDOWS\system32\nvidia-smi.EXE", "--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu", "--format=csv,noheader,nounits"],
        [str(LEAN_BIN / "lake.exe"), "--version"],
        [str(LEAN_BIN / "lean.exe"), "--version"],
        [str(MIKTEX_BIN / "initexmf.exe"), "--disable-installer", "--report"],
        [str(MIKTEX_BIN / "initexmf.exe"), "--disable-installer", "--show-config-value=[MPM]AutoInstall"],
        [str(MIKTEX_BIN / "pdflatex.exe"), "--disable-installer", "--version"],
    ]
    for i, cmd in enumerate(commands):
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        t0 = time.perf_counter()
        r = subprocess.run(cmd, cwd=root, env=env, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=300)
        rec = {"command": cmd, "start_utc": started,
               "end_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "seconds": time.perf_counter() - t0, "exit_code": r.returncode,
               "stdout": r.stdout, "stderr": r.stderr}
        save(envroot / f"PROBE_{i:02d}.json", rec)
        probes.append({"file": str(envroot / f"PROBE_{i:02d}.json"),
                       "sha256": sha(envroot / f"PROBE_{i:02d}.json"),
                       "exit_code": r.returncode})
        print(json.dumps({"probe": i, "exit_code": r.returncode,
                          "stdout_summary": r.stdout[:1500]}), flush=True)
    save(root / "ENVIRONMENT_PREFLIGHT_R3.json", {
        "scope": "dependency_preflight_no_rite_no_um_import", "candidate": candidate_copy,
        "integration": {"path": str(integration), "sha256": sha(integration)},
        "overrides": overrides, "unset": unset, "probes": probes,
        "all_probes_exit_zero": all(x["exit_code"] == 0 for x in probes),
        "bench_documents": bench_records,
        "miktex_local_configuration": {"path": str(config), "sha256": sha(config)},
        "guard_not_yet_installed": True,
        "full_rite_not_started": True,
    })


if __name__ == "__main__":
    main()
