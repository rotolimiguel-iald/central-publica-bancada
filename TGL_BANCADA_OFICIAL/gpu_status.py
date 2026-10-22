"""Read-only telemetry; never changes GPU allocation or other processes."""
from __future__ import annotations

import re
import subprocess


def status() -> dict:
    try:
        completed = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3, check=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        rows = []
        for line in completed.stdout.splitlines():
            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 4 or not all(re.fullmatch(r"\d+", x) for x in parts[1:]):
                raise ValueError("Unexpected GPU telemetry")
            rows.append({"name": parts[0], "total_mib": int(parts[1]),
                         "free_mib": int(parts[2]), "utilization_percent": int(parts[3])})
        if not rows:
            raise ValueError("No GPU telemetry")
        return {"status": "NVIDIA_TELEMETRY_READ_ONLY", "devices": rows,
                "policy": "Rendering uses a small browser WebGL2 buffer; no compute job or VRAM reservation."}
    except (OSError, subprocess.SubprocessError, ValueError):
        return {"status": "GPU_TELEMETRY_UNAVAILABLE", "devices": [],
                "policy": "Do not infer available VRAM or hardware rendering from an absent reading."}
