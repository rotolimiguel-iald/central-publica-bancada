import sys,inspect,json,hashlib,pathlib,datetime
import bilby,dynesty,lal,lalsimulation,numpy,scipy
from dynesty import utils
base=pathlib.Path("/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico")
old=json.loads((base/"ENVIRONMENT_NATIVE_HASHES.json").read_text())

files=set()
for row in old["files"]:
 p=pathlib.Path(row["path"]);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==row["sha256"] and len(raw)==row["bytes"]
 files.add(p)
for mod in list(sys.modules.values()):
 f=getattr(mod,"__file__",None)
 if f and f.startswith("/opt/lal_env/"):
  p=pathlib.Path(f)
  if p.suffix==".pyc" and p.with_suffix(".py").exists():p=p.with_suffix(".py")
  if p.is_file():files.add(p)
for line in pathlib.Path("/proc/self/maps").read_text().splitlines():
 p=line.split()[-1]
 if p.startswith("/opt/lal_env/") and pathlib.Path(p).is_file():files.add(pathlib.Path(p))
# Fixed scientific package files include lazy imports and detector definitions; no private data.
for package in (bilby,dynesty):
 top=pathlib.Path(package.__file__).parent
 files.update(p for p in top.rglob("*") if p.is_file() and p.suffix in (".py",".interferometer"))
out={"status":"READ_ONLY_RUNTIME_PREPARATION","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "versions":{m.__name__:getattr(m,"__version__",None) for m in (bilby,dynesty,numpy,scipy,lal,lalsimulation)},
 "baseline_165_verified":len(old["files"]),"files":[{"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size} for p in sorted(files)],
 "signatures":{name:str(inspect.signature(obj)) for name,obj in {
 "NestedSampler":dynesty.NestedSampler,"sample":dynesty.NestedSampler.sample,"add_live_points":dynesty.NestedSampler.add_live_points,"compute_integrals":utils.compute_integrals,
 "likelihood":bilby.gw.likelihood.GravitationalWaveTransient,"log_likelihood_ratio":bilby.gw.likelihood.GravitationalWaveTransient.log_likelihood_ratio}.items()},
 "source excerpts":{"sample":inspect.getsource(dynesty.NestedSampler.sample),"compute_integrals":inspect.getsource(utils.compute_integrals)},
 "native_waveforms":0,"PE_jobs":0,"D_read":False,"scope":"Imports and static source/file hashing only; no sampler or likelihood instantiated; not an execution attestation of P3."}
import os
dst=base.parent/"p3_preparacao"/"RUNTIME_P3_READONLY.json"
assert not dst.exists()
raw=(json.dumps(out,indent=2)+"\n").encode()
tmp=dst.with_name(dst.name+".tmp");tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,dst)
print(json.dumps({"path":str(dst),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"runtime_files":len(files),"versions":out["versions"],"signatures":out["signatures"]}))