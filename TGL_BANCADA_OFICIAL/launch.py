"""Open the canonical local TGL bench, starting it only when necessary."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from contextlib import contextmanager
import ctypes
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = "http://127.0.0.1:18765"
COSMOS_URL = "http://127.0.0.1:18766"
PYTHONW = Path(r"C:\Python314\pythonw.exe")


@contextmanager
def launch_lock():
    """Serialize simultaneous desktop clicks without affecting running workers."""
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateMutexW.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p)
    kernel.CreateMutexW.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
    kernel.ReleaseMutex.argtypes = (ctypes.c_void_p,)
    kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
    suffix = hashlib.sha256(str(HERE).lower().encode()).hexdigest()[:16]
    handle = kernel.CreateMutexW(None, False, "Local\\TGL-Bench-" + suffix)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    acquired = False
    try:
        acquired = kernel.WaitForSingleObject(handle, 30000) in (0, 0x80)
        if not acquired:
            raise RuntimeError("Outra abertura da bancada ainda está em andamento.")
        yield
    finally:
        if acquired:
            kernel.ReleaseMutex(handle)
        kernel.CloseHandle(handle)


def is_our_bench(cosmology: bool = False) -> bool:
    try:
        endpoint = COSMOS_URL + "/api/cosmology/health" if cosmology else URL + "/api/overview"
        with urllib.request.urlopen(endpoint, timeout=1.5) as response:
            data = json.load(response)
        return isinstance(data, dict) and (
            data.get("service") == "tgl-cosmology-resident-v1" if cosmology else
            data.get("name") == "Bancada Oficial TGL — protótipo local")
    except (OSError, ValueError, urllib.error.URLError):
        return False


def start(cosmology: bool = False) -> None:
    if not PYTHONW.is_file():
        raise FileNotFoundError(f"Python indisponível: {PYTHONW}")
    app = HERE / ("cosmology_server.py" if cosmology else "app.py")
    if not app.is_file():
        raise FileNotFoundError(f"Bancada indisponível: {app}")
    log_path = HERE / "state" / ("cosmology_server.log" if cosmology else "server.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab") as log:
        subprocess.Popen(
            [str(PYTHONW), str(app)],
            cwd=str(HERE),
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True,
        )
    for _ in range(40):
        if is_our_bench(cosmology):
            return
        time.sleep(0.25)
    raise RuntimeError(f"A bancada não iniciou. Consulte {log_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Atalho local da Bancada TGL")
    parser.add_argument("--check", action="store_true", help="Verificar sem abrir navegador")
    args = parser.parse_args()
    if args.check:
        print(json.dumps({"running": is_our_bench(), "url": URL,
                          "cosmology_running": is_our_bench(True), "cosmology_url": COSMOS_URL + "/explore",
                          "app": str(HERE / "app.py")}, ensure_ascii=False))
        return 0
    try:
        cosmos_error = None
        with launch_lock():
            if not is_our_bench():
                start()
            try:
                if not is_our_bench(True):
                    start(True)
            except Exception as exc:
                cosmos_error = exc
        destination = COSMOS_URL + "/explore" if cosmos_error is None else URL + "/universe"
        webbrowser.open(destination, new=2)
        if cosmos_error is not None:
            raise RuntimeError(f"A bancada foi aberta, mas o domínio cosmológico está indisponível: {cosmos_error}")
        return 0
    except Exception as exc:
        try:
            from tkinter import messagebox
            messagebox.showerror("TGL — bancada", str(exc))
        except Exception:
            print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
