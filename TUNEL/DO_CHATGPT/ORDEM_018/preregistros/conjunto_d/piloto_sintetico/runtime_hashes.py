"""Read-only provenance of imported runtime code and native libraries, no model calls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,inspect,json,os,sys
ROOT=Path(__file__).resolve().parent
contract=json.loads((ROOT/"CONTRATO_RUNTIME_HASHES.json").read_text())
assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==contract["script_sha256"]
import lal,lalsimulation,bilby,numpy
paths={Path(m.__file__).resolve() for m in (lal,lalsimulation,bilby,numpy)}
paths.update(Path(inspect.getsourcefile(fn)).resolve() for fn in (bilby.gw.source.lal_binary_black_hole,
  bilby.gw.WaveformGenerator,bilby.gw.detector.Interferometer,bilby.gw.detector.PowerSpectralDensity))
for line in Path("/proc/self/maps").read_text().splitlines():
    fields=line.split()
    if fields and fields[-1].startswith("/opt/lal_env/") and ".so" in fields[-1]:paths.add(Path(fields[-1]).resolve())
rows=[{"path":str(p),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
doc={"status":"RUNTIME_CODE_AND_NATIVE_LIBRARIES_PINNED_NO_WAVEFORMS","created_utc":datetime.now(timezone.utc).isoformat(),
     "files":rows,"PE_calls":0,"waveforms":0,"D_read":False,"source_scope":"Imported modules, inspected Bilby implementation files and /opt/lal_env libraries mapped in this process"}
p=ROOT/"ENVIRONMENT_NATIVE_HASHES.json";assert not p.exists()
raw=(json.dumps(doc,ensure_ascii=False,indent=2)+"\n").encode();t=p.with_suffix(".tmp");t.write_bytes(raw);assert t.read_bytes()==raw;os.replace(t,p)
print(json.dumps({"files":len(rows),"sha256":hashlib.sha256(raw).hexdigest(),"paths":[x["path"] for x in rows if "lal" in Path(x["path"]).name]}))
