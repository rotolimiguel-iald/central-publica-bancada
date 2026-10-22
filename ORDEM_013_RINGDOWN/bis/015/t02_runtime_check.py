"""Read-only verification of the pinned runtime for T02; no model/data execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,sys,time
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
ROOT=B.parent;D=B/'bis/015/t02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    start=time.perf_counter()
    reg=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    p=ROOT/reg['runtime_manifest_relative_to_Chatgpt'];assert sha(p)==reg['runtime_manifest_sha256']
    manifest=json.loads(p.read_bytes());errors=[]
    if Path(sys.prefix).resolve()!=Path('/opt/lal_env'):errors.append('Wrong prefix '+sys.prefix)
    exe=Path(manifest['python_executable'])
    if Path(sys.executable).resolve()!=exe.resolve():errors.append('Wrong executable')
    if sha(exe)!=manifest['python_executable_sha256']:errors.append('Executable hash mismatch')
    for name,v in manifest['files'].items():
        f=Path(name)
        if not f.resolve().is_relative_to('/opt/lal_env') or sha(f)!=v['sha256']:errors.append(name)
    result={'at':datetime.now(timezone.utc).isoformat(),'status':'RUNTIME_PINS_MATCH' if not errors else 'RUNTIME_PIN_FAILURE',
      'runtime_manifest_sha256':sha(p),'files_checked':len(manifest['files']),'errors':errors,'wall_seconds':time.perf_counter()-start}
    raw=(json.dumps(result,indent=2)+'\n').encode();out=D/'RUNTIME_CHECK.json'
    with out.open('xb') as f:f.write(raw)
    print(json.dumps(result));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
