"""Recover already-used historical inputs omitted from the copied rite assets.

No scientific execution, network, new observation or original modification.
Claim F1.FECHO_20261015 /845, short sandbox scope849. Exclusive output.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import shutil

HERE = Path(__file__).resolve().parent
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
DEST = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r3")
BASELINE = NOS / "um_absoluto.json"
REPORT = HERE / "HISTORICAL_ASSETS_RECOVERED_R1.json"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def walk_json(value):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk_json(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_json(v)

def main():
    if REPORT.exists() or REPORT.with_suffix(".tmp").exists():
        raise FileExistsError(REPORT)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    baseline_sha = sha(BASELINE)
    baseline = json.loads(BASELINE.read_bytes())
    manifest = list(walk_json(baseline))
    sources = [
        (NOS / "STOKES_A_Prova_do_Contorno.md", DEST / "STOKES_A_Prova_do_Contorno.md"),
        (NOS / "nivel2_mcmc" / "12_nivel2_frozen.json", DEST / "nivel2_mcmc" / "12_nivel2_frozen.json"),
        (NOS / "nivel2_mcmc" / "13_nivel2_resultado.json", DEST / "nivel2_mcmc" / "13_nivel2_resultado.json"),
    ]
    for hemi in ("NGC", "SGC"):
        name = f"DESIVAST_BGS_VOLLIM_V2_REVOLVER_{hemi}.fits"
        sources.append((NOS.parent / "TGL_CODE_ONE_REAL_FALSIFIER" / "release_clean" / "data" / "voids" / "desivast" / name,
                        DEST / "cache" / "voids" / "desivast" / name))
    records = []
    for source, target in sources:
        if source.is_symlink() or source.is_junction():
            raise RuntimeError(f"Linked source refused: {source}")
        if not target.resolve().is_relative_to(DEST.resolve()):
            raise RuntimeError(f"Outside destination: {target}")
        if target.exists():
            raise FileExistsError(target)
        digest = sha(source)
        matches = [d for d in manifest if d.get("file") == source.name and d.get("sha256") == digest]
        if "REVOLVER" in source.name and not matches:
            raise RuntimeError(f"Historical manifest pin mismatch: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        with source.open("rb") as src, target.open("xb") as dst:
            shutil.copyfileobj(src, dst, 4 * 1024 * 1024)
            dst.flush()
            os.fsync(dst.fileno())
        if sha(target) != digest or sha(source) != digest:
            raise RuntimeError(f"Copy/source hash mismatch: {source}")
        records.append({"source": str(source), "destination": str(target), "bytes": source.stat().st_size,
                        "sha256": digest, "historical_manifest_exact_matches": len(matches),
                        "original_unchanged": True, "copy_equal": True})
    if sha(BASELINE) != baseline_sha:
        raise RuntimeError("Historical baseline changed during recovery")
    result = {"unit": "F1.FECHO_20261015", "claim": 845, "scope_event": 849,
              "started_utc": started, "ended_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "status": "COPIED_AND_PINNED_HISTORICAL_INPUTS_ONLY", "baseline": str(BASELINE),
              "baseline_sha256": baseline_sha, "records": records,
              "desy3_metadata": "No historical DES-Y3 catalog identified; network remains disabled.",
              "not_a_scientific_run": True}
    data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    temporary = REPORT.with_suffix(".tmp")
    with temporary.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if temporary.stat().st_size != len(data):
        raise RuntimeError("Short report write")
    temporary.rename(REPORT)
    print(json.dumps({"report": str(REPORT), "sha256": sha(REPORT), "files": len(records),
                      "bytes": sum(r["bytes"] for r in records)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
