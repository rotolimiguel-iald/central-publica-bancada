"""Invoke the existing scientific WSL environment without installing packages."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_PYTHON = ("/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/"
              "cache/t14_pyseobnr_venv/bin/python")


def wsl_path(path: Path) -> str:
    resolved = path.resolve()
    if not resolved.drive or resolved.drive.lower() != "c:":
        raise ValueError("HDF5 source must be on the local C: drive")
    return "/mnt/c/" + str(resolved)[3:].replace("\\", "/")


def call(path: Path, operation: str, x: str = "", y: str = "", limit: int = 800) -> dict:
    if operation not in {"describe", "preview"} or not 1 <= limit <= 1200:
        raise ValueError("Invalid HDF5 operation")
    request = {"path": wsl_path(path), "operation": operation,
               "x": x, "y": y, "limit": limit}
    script = wsl_path(HERE / "adapters" / "hdf5_reader.py")
    try:
        result = subprocess.run(["wsl.exe", "-e", ENV_PYTHON, script],
                                input=json.dumps(request), text=True, capture_output=True,
                                timeout=30, check=False,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"HDF5 adapter unavailable: {type(exc).__name__}") from exc
    if len(result.stdout) > 1_000_000:
        raise ValueError("HDF5 adapter response exceeds bounded size")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("HDF5 adapter returned no valid JSON") from exc
    if result.returncode != 0 or "error" in payload:
        raise ValueError("HDF5 adapter refused source: " + str(payload.get("error", "unknown"))[:300])
    return payload
