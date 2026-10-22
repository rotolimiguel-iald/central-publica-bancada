"""Read the real guards once; no job, seed, posterior or runtime materialization."""
from pathlib import Path
import importlib.util,json,sys,hashlib
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1]
out={}
for label,code in [('historical_V1',B/'bis/e2_code'),('V1_1_latest',B/'bis/e2_code_v1_1')]:
    path=code/'registration_guard.py';spec=importlib.util.spec_from_file_location('guard_'+label,path)
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    try:
        reg,digest=guard.checked_registration();out[label]=dict(status='ACCEPTED',registration_sha256=digest)
    except Exception as exc:
        out[label]=dict(status='REFUSED',exception=type(exc).__name__,message=str(exc))
    out[label]['guard_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
print(json.dumps(out))
assert out['historical_V1']['exception']=='TimeoutError'
assert out['V1_1_latest']['exception']=='ValueError'
assert out['V1_1_latest']['message']=='V1.1 activation does not match latest registration/witness'
