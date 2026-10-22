"""Isolated NPZ read control only. Never imports a waveform source, Bilby or Dynesty."""
import sys,os,json,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
sys.pycache_prefix=str(ROOT/"UNUSED_BYTECODE_CACHE")
from preload_npz_codec import preload_npz_codec
started=time.perf_counter();cpu0=time.process_time()
cp=ROOT/"CONTRATO_CONTROLE_LEITURA.json"
contract=json.loads(cp.read_text());contract_sha=hashlib.sha256(cp.read_bytes()).hexdigest()
if contract["purpose"]!="SYNTHETIC_NPZ_STRUCTURE_ONLY_NO_PE":
    raise ValueError("Read-control-only contract required")
for rel,pin in contract["inputs"].items():
    p=ROOT/rel;raw=p.read_bytes()
    if len(raw)!=pin["bytes"] or hashlib.sha256(raw).hexdigest()!=pin["sha256"]:
        raise ValueError("Control input pin mismatch: "+rel)
import numpy as np
codec=preload_npz_codec(json.loads((ROOT/"CODEC_CP437_PIN.json").read_text()))
npz=(ROOT/contract["npz"]).resolve()
result=ROOT/"CONTROLE_NPZ_LEITURA.json";temp=ROOT/"CONTROLE_NPZ_LEITURA.json.tmp"
if result.exists() or temp.exists():raise FileExistsError("No overwrite/repeat of control receipt")
read_paths=[];blocked=[];checks=[]
def check(name,ok):
    checks.append({"name":name,"passed":bool(ok)})
    if not ok:raise AssertionError(name)
def audit(event,args):
    if event in ("socket.connect","socket.bind","subprocess.Popen","os.system","os.fork","os.forkpty","os.posix_spawn"):
        blocked.append({"event":event});raise PermissionError("No remote/child operations")
    if event=="open" and not isinstance(args[0],int):
        p=Path(os.fsdecode(args[0])).resolve();mode=args[1];flags=args[2] or 0
        write=bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)) or (isinstance(mode,str) and any(x in mode for x in "wax+"))
        if write:
            if p not in (temp,result):
                blocked.append({"path":str(p),"mode":"write"});raise PermissionError("Exact receipt paths only")
        elif p not in (npz,temp):
            blocked.append({"path":str(p),"mode":"read"});raise PermissionError("Exact synthetic NPZ only after codec preload")
        else:read_paths.append(str(p))
sys.addaudithook(audit)
status="FAILED";error=None;arrays=[]
try:
    expected={"frequencies_Hz","PSD_analytic_strain2_per_Hz"}
    for label in ("GR_ZERO","GR_GAUSS","RB_GAUSS"):
        for det in ("H1","L1"):
            expected|={label+"_"+det+"_noise_fd",label+"_"+det+"_signal_fd"}
    with np.load(npz,allow_pickle=False) as archive:
        check("14_exact_array_names",set(archive.files)==expected and len(archive.files)==14)
        for name in sorted(expected):
            a=archive[name]
            check("shape:"+name,a.shape==(65537,))
            check("numeric_not_object:"+name,a.dtype.kind in ("f","c") and not a.dtype.hasobject)
            if name=="PSD_analytic_strain2_per_Hz":
                f=archive["frequencies_Hz"];mask=(f>=20)&(f<=1024)
                check("PSD_structure",np.isfinite(a[mask]).all() and (a[mask]>0).all() and np.isinf(a[~mask]).all())
            else:check("finite:"+name,np.isfinite(a).all())
            arrays.append({"name":name,"shape":list(a.shape),"dtype":str(a.dtype),"bytes":a.nbytes,
                           "sha256":hashlib.sha256(a.tobytes(order="C")).hexdigest()})
        check("frequency_grid",np.array_equal(archive["frequencies_Hz"],np.fft.rfftfreq(131072,1/4096)))
    check("no_codec_read_after_hook",not any("cp437" in p for p in read_paths))
    check("only_pinned_npz_read",set(read_paths)=={str(npz)})
    check("no_blocked_operations",not blocked)
    check("no_scientific_PE_modules",not any(m in sys.modules for m in ("bilby","lal","lalsimulation","dynesty","pseob_source","synthetic_adapter_v2")))
    status="PASS_SYNTHETIC_NPZ_READ_ONLY"
except Exception as exc:
    error={"type":type(exc).__module__+"."+type(exc).__qualname__,"message":str(exc)}
out={"status":status,"finished_utc":datetime.now(timezone.utc).isoformat(),"contract_sha256":contract_sha,
     "codec":codec,"checks":checks,"array_structure":arrays,"error":error,
     "read_paths_after_hook":read_paths,"blocked_operations":blocked,
     "wall_s":time.perf_counter()-started,"CPU_s":time.process_time()-cpu0,
     "NumPy_version":np.__version__,"PE_jobs":0,"likelihood_calls":0,"waveform_calls":0,
     "D_read":False,"scope":"Preload and exact synthetic NPZ structure/hash read only; no waveform, likelihood or sampler; not P3 retry."}
raw=(json.dumps(out,indent=2)+"\n").encode()
with temp.open("xb") as fh:fh.write(raw)
if temp.read_bytes()!=raw:raise OSError("Atomic verification")
os.replace(temp,result)
print(json.dumps({k:out[k] for k in ("status","wall_s","CPU_s","PE_jobs","likelihood_calls","waveform_calls","error")}))
sys.exit(0 if status.startswith("PASS") else 2)
