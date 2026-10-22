"""Preserve the failed known-event pilot without accepting partial products."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

B = Path(__file__).resolve().parents[1]
P = B / "cache/E3_PSEOB_PILOT_V1"
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    controller = json.loads((P/"CONTROLLER.json").read_bytes())
    context = json.loads((P/"LAUNCH_CONTEXT.json").read_bytes())
    if controller["blind"] is not False or controller["job"] != "GW250114_PILOT":
        raise ValueError("Known calibration pilot only")
    if controller["returncode"] != -11 or controller["cleanup"]["group_absent"] is not True:
        raise ValueError("Unexpected failure or incomplete cleanup")
    log = (P/"PRIVATE.log").read_text(encoding="utf-8")
    value = {
        "status": "NATIVE_SIGSEGV_BEFORE_ACCEPTED_POSTERIOR__DIAGNOSIS_OPEN",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "controller": controller,
        "context_sha256": sha(P/"LAUNCH_CONTEXT.json"),
        "controller_sha256": sha(P/"CONTROLLER.json"),
        "known_calibration_log_sha256": sha(P/"PRIVATE.log"),
        "original_pilot_absolute_stop_utc": context["stop_utc"],
        "log_signature_counts": {
            marker: log.count(marker) for marker in (
                "Ringdown frequency > Nyquist frequency!",
                "Likelihood will be set to -inf.",
                "Generating initial points from the prior"
            )
        },
        "expected_product_presence": {
            name: (P/name).exists() for name in (
                "PRIVATE_CONVERGENCE.json", "ANALYST_OUTPUT.json",
                "ANALYST_STATUS.json", "FAILURE.json"
            )
        },
        "likelihood_calls": None,
        "source_calls": None,
        "cost_per_converged_event": None,
        "interpretation": "Negative return code -11 records native SIGSEGV. Nyquist warnings were observed before exit but causal connection is not yet demonstrated. Missing final counters are unknown, not zero. No accepted posterior is available.",
        "next_scope": "Bounded isolated diagnostics and independent review; any executable repair must be versioned and witnessed before another pilot or blind run. Original prior/data/family and failed bytes remain preserved.",
        "script_sha256": sha(Path(__file__)),
    }
    path = B/"bis/E3_PILOT_FAILURE_AUDIT_V1.json"
    raw = (json.dumps(value, indent=2, allow_nan=False)+"\n").encode()
    tmp = path.with_name(path.name+".pending")
    with tmp.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    if tmp.stat().st_size != len(raw): raise IOError("Incomplete receipt")
    os.link(tmp, path); tmp.unlink()
    print(json.dumps({"path":str(path),"sha256":sha(path),"status":value["status"],"observed_log_signatures":value["log_signature_counts"]}))

if __name__ == "__main__": main()
