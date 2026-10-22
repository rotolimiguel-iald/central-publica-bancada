"""Environment metadata only. No waveform, injection, likelihood or PE."""
from pathlib import Path
import json,hashlib,sys,inspect,os,time
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
contract=json.loads((ROOT/"CONTRATO_PREFLIGHT.json").read_text())
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert digest(__file__)==contract["probe_sha256"]
assert contract["waveform_calls_authorized"]==0
import lal,lalsimulation as ls,bilby,numpy as np
from importlib.metadata import version
modules=[lal,ls,bilby,np]
doc={"status":"ENVIRONMENT_METADATA_ONLY","at":datetime.now(timezone.utc).isoformat(),
     "python":sys.version,"executable":sys.executable,"prefix":sys.prefix,
     "versions":{n:version(n) for n in ("bilby","numpy","scipy","lalsuite")},
     "modules":[{"name":m.__name__,"path":m.__file__,"sha256":digest(m.__file__)} for m in modules],
     "required_symbols":{n:hasattr(ls,n) for n in ("pSEOBNRv4HM_PA","SimNoisePSDaLIGOZeroDetHighPower","SimIMREOBFinalMassSpin","SEOBNRv4")},
     "signatures":{n:str(inspect.signature(getattr(bilby.gw.detector.Interferometer,n))) for n in ("set_strain_data_from_frequency_domain_strain","get_detector_response","optimal_snr_squared")},
     "waveform_generator_signature":str(inspect.signature(bilby.gw.WaveformGenerator)),
     "waveforms":0,"injections":0,"PE":0,"data_files_opened":False}
path=ROOT/"ENVIRONMENT_PREFLIGHT.json";assert not path.exists()
raw=(json.dumps(doc,ensure_ascii=False,indent=2)+"\n").encode();tmp=path.with_suffix(".tmp")
tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,path)
print(json.dumps(doc,ensure_ascii=False))
