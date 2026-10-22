"""Serialized, bounded Windows-to-WSL bridge for the byte-pinned V3 background.

This module never imports the resident GW runtime. A timeout or lost reply is
uncertain: the same request is not silently dispatched again in this process.
"""

from __future__ import annotations

import atexit
import hashlib
import json
import math
import os
from pathlib import Path
import queue
import subprocess
import threading
import time
import uuid


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "scientific_models" / "tgl_camb_worker_v3.py"
WORKER = BASE / "workers" / "cosmology_v3_worker.py"
SOURCE_SHA256 = "72032b3abe1c537762291ac6086d8d2e6076c007373f87ae7363f942eb830ce3"
WSL_PYTHON = "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/t14_pyseobnr_venv/bin/python"
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
TIMEOUT_SECONDS = 45.0
MODEL_IDS = {"fixed": "TGL_V3_TOTAL_FIXED_BETA", "zero": "V3_TOTAL_BETA_ZERO"}
_LIMITS = {"H0": (40.0, 100.0), "omega_m": (0.1, 0.5),
           "rd_mpc": (120.0, 170.0), "redshift": (0.001, 3.0)}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_LOADED_SOURCE_SHA256 = _sha(SOURCE)
_LOADED_WORKER_SHA256 = _sha(WORKER)
_LOADED_BRIDGE_SHA256 = _sha(Path(__file__))
if _LOADED_SOURCE_SHA256 != SOURCE_SHA256:
    raise RuntimeError("pinned scientific source SHA-256 mismatch at bridge import")


def _wsl_path(path: Path) -> str:
    full = str(path.resolve())
    if len(full) < 3 or full[1:3] != ":\\":
        raise RuntimeError("WSL bridge requires an absolute Windows drive path")
    return "/mnt/" + full[0].lower() + full[2:].replace("\\", "/")


def _number(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be a finite number")
    return out


def _validate(parameters, beta_mode, redshifts):
    if beta_mode not in MODEL_IDS:
        raise ValueError("beta_mode must be 'fixed' or 'zero'")
    if not isinstance(parameters, dict):
        raise ValueError("parameters must be an object")
    required = (*_LIMITS, "w0", "wa")
    missing = [name for name in required if name not in parameters]
    if missing:
        raise ValueError("missing parameters: " + ", ".join(missing))
    p = {name: _number(parameters[name], name) for name in required}
    for name, (low, high) in _LIMITS.items():
        if not low <= p[name] <= high:
            raise ValueError(f"{name} outside [{low}, {high}]")
    if p["w0"] != -1.0 or p["wa"] != 0.0:
        raise ValueError("pinned V3 requires w0=-1 and wa=0")
    if redshifts is None:
        redshifts = []
    if not isinstance(redshifts, (list, tuple)) or len(redshifts) > 128:
        raise ValueError("redshifts must be a list of at most 128 values")
    zs = [_number(z, f"redshifts[{i}]") for i, z in enumerate(redshifts)]
    if any(z < 0.0 or z > 3.0 for z in zs):
        raise ValueError("redshifts must lie in [0, 3]")
    return p, zs


class _Session:
    def __init__(self):
        self.lock = threading.Lock()
        self.process = None
        self.replies = None
        self.uncertain = set()

    def _stop(self):
        process = self.process
        self.process = None
        self.replies = None
        if process is not None:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=1)
            except (OSError, subprocess.TimeoutExpired):
                pass

    def _start(self):
        if self.process is not None and self.process.poll() is None:
            return
        self._stop()
        if _sha(SOURCE) != _LOADED_SOURCE_SHA256:
            raise RuntimeError("scientific source changed after bridge import")
        if _sha(WORKER) != _LOADED_WORKER_SHA256:
            raise RuntimeError("V3 adapter worker changed after bridge import")
        if _sha(Path(__file__)) != _LOADED_BRIDGE_SHA256:
            raise RuntimeError("V3 bridge changed after import; reload required")
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        process = subprocess.Popen(
            ["wsl.exe", "--exec", WSL_PYTHON, "-u", _wsl_path(WORKER)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
            creationflags=flags,
        )
        replies = queue.Queue()
        def read_lines():
            try:
                for line in process.stdout:
                    replies.put(line)
            finally:
                replies.put(None)
        threading.Thread(target=read_lines, daemon=True, name="cosmology-v3-stdio").start()
        self.process, self.replies = process, replies

    def exchange(self, request):
        key = hashlib.sha256(json.dumps(request, sort_keys=True,
            separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
        with self.lock:
            if key in self.uncertain:
                raise RuntimeError("previous delivery of this request is uncertain; no automatic retry")
            self._start()
            request_id = str(uuid.uuid4())
            wire = dict(request, request_id=request_id)
            try:
                self.process.stdin.write(json.dumps(wire, allow_nan=False,
                    separators=(",", ":")) + "\n")
                self.process.stdin.flush()
                line = self.replies.get(timeout=TIMEOUT_SECONDS)
                if line is None:
                    raise RuntimeError("V3 worker exited before responding")
                try:
                    reply = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise RuntimeError("V3 worker produced non-JSON output; check WSL execution access") from exc
                if reply.get("request_id") != request_id:
                    raise RuntimeError("V3 worker reply identity mismatch")
                return reply
            except (OSError, ValueError, queue.Empty, RuntimeError) as exc:
                self.uncertain.add(key)
                self._stop()
                if isinstance(exc, queue.Empty):
                    raise TimeoutError("V3 worker timed out; delivery uncertain") from exc
                raise


_SESSION = _Session()
atexit.register(_SESSION._stop)


def evaluate_background(parameters, beta_mode, redshifts=None) -> dict:
    """Return exact requested z distances and the 121-point visual curve.

    No interpolation of the visual series is used for requested observations.
    Errors are explicit JSON-shaped results; uncertain requests are never retried.
    """
    start = time.perf_counter()
    model_id = MODEL_IDS.get(beta_mode) if isinstance(beta_mode, str) else None
    try:
        p, zs = _validate(parameters, beta_mode, redshifts)
        beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e) if beta_mode == "fixed" else 0.0
        request = {"parameters": p, "beta_mode": beta_mode,
                   "beta": beta, "model_id": model_id, "redshifts": zs}
        result = _SESSION.exchange(request)
        result.pop("request_id", None)
        if result.get("status") != "ok":
            result.setdefault("error", {"code": "WORKER_ERROR", "message": "V3 worker failed"})
        else:
            result["source_hashes"]["scientific_model_sha256"] = _LOADED_SOURCE_SHA256
            result["source_hashes"]["adapter_worker_sha256"] = _LOADED_WORKER_SHA256
            result["source_hashes"]["bridge_sha256"] = _LOADED_BRIDGE_SHA256
        result["elapsed_ms"] = (time.perf_counter() - start) * 1000.0
        return result
    except Exception as exc:
        return {"status": "error", "model_id": model_id,
                "error": {"code": type(exc).__name__, "message": str(exc)},
                "elapsed_ms": (time.perf_counter() - start) * 1000.0}
