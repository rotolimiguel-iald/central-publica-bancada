"""Create additive retry scripts; never edit the failed attempt or candidate."""
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
OLD = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015")
NEW = OLD / "r2"

def emit(name, text):
    ast.parse(text)
    with (HERE / name).open("x", encoding="utf-8", newline="\n") as f:
        f.write(text)

guard = (HERE / "sitecustomize_rite.py").read_text(encoding="utf-8")
guard = guard.replace("import re\n", "import re\nimport shutil\n")
old = '        if name not in _TRUSTED:\n            _refuse(event, args[:3], "executable not on the explicit allowlist")'
new = '''        # Exact readonly probes from Python platform and Triton AMD discovery.
        # rocm-sdk is absent: permit the OS's natural FileNotFoundError, which
        # Triton explicitly catches. An installed executable needs new review.
        cmd_ver = (name == os.path.normcase(r"C:\\Windows\\System32\\cmd.exe")
                   and isinstance(argv, str)
                   and argv.lower() in {
                       'c:\\\\windows\\\\system32\\\\cmd.exe /c "ver"',
                       '"c:\\\\windows\\\\system32\\\\cmd.exe" /c "ver"'})
        rocm_probe = (str(resolved_exe).lower() == "rocm-sdk"
                      and (argv == "rocm-sdk path --root"
                           or argv == ["rocm-sdk", "path", "--root"])
                      and shutil.which("rocm-sdk") is None)
        if name not in _TRUSTED and not cmd_ver and not rocm_probe:
            _refuse(event, args[:3], "executable not on the explicit allowlist")'''
assert old in guard
guard = guard.replace(old, new)
emit("sitecustomize_rite_r2.py", guard)

env = (HERE / "prepare_environment_r2.py").read_text(encoding="utf-8")
env = env.replace(str(OLD), str(NEW)).replace("ENVIRONMENT_PREFLIGHT_R2.json", "ENVIRONMENT_PREFLIGHT_R3.json")
env = env.replace('"torch", "cuda",', '"torch", "cuda", "triton", "torchinductor",')
env = env.replace('"TORCH_HOME": str(envroot / "torch"),',
                  '"TRITON_CACHE_DIR": str(envroot / "triton"), "TORCHINDUCTOR_CACHE_DIR": str(envroot / "torchinductor"),\n        "TORCH_HOME": str(envroot / "torch"),')
emit("prepare_environment_r3.py", env)

launcher = (HERE / "launch_full_rite.py").read_text(encoding="utf-8")
launcher = launcher.replace(str(OLD), str(NEW))
launcher = launcher.replace("PREPARATION_RECEIPT_R3.json", "PREPARATION_RECEIPT_R4.json")
launcher = launcher.replace("ENVIRONMENT_PREFLIGHT_R2.json", "ENVIRONMENT_PREFLIGHT_R3.json")
launcher = launcher.replace('HERE / "sitecustomize_rite.py"', 'HERE / "sitecustomize_rite_r2.py"')
launcher = launcher.replace('command = [str(PYTHON), "-B",', 'command = [str(PYTHON), "-u", "-B",')
launcher = launcher.replace('    env["TGL_RITE_GUARD_PHASE"] = "actual"', '''    engine_preflight = json.loads((ROOT / "ENGINE_PREFLIGHT_RECEIPT.json").read_text(encoding="utf-8"))
    assert engine_preflight["passed"] and engine_preflight["exit_code"] == 0
    assert engine_preflight["guard_source_sha256"] == sha(guard_src)
    env["TGL_RITE_GUARD_PHASE"] = "actual"''')
emit("launch_full_rite_r2.py", launcher)

receipt = json.loads((OLD / "RITE_RECEIPT.json").read_text(encoding="utf-8"))
report = {
    "status": "INTERRUPTED_ENVIRONMENT_GUARD_MISMATCH_NOT_SCIENTIFIC_FAILURE",
    "start_utc": receipt["start_utc"], "end_utc": receipt["end_utc"],
    "exit_code": receipt["exit_code"], "seconds": receipt["seconds"],
    "cause": "Python audit guard refused readonly platform cmd/ver and optional missing rocm-sdk/path/--root probe; Triton catches FileNotFoundError but not the guard's PermissionError. Engine selftest failed, full GPU fallback was refused, then only our Python/Lean tree was terminated.",
    "interrupted_pid": receipt["pid"], "canonical_mutation": False,
    "scope": "Unchanged R3 candidate; retry only environment guard, exact reviewed probes; no scientific result or main replacement.",
    "prior_receipt": {"path": str(OLD / "RITE_RECEIPT.json"), "sha256": hashlib.sha256((OLD / "RITE_RECEIPT.json").read_bytes()).hexdigest()},
    "retry_root": str(NEW), "no_full_rite_success_claimed": True,
}
with (HERE / "FIRST_ATTEMPT_INTERRUPTION.json").open("x", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(json.dumps({"created": 4, "retry_root": str(NEW)}))
