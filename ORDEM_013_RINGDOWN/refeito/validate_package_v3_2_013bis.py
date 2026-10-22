"""Clean extraction, byte/unit controls, then the required C6 numerical replay."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import json,hashlib,zipfile,subprocess,sys,os,shutil,tempfile
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    archive=B/'cache/C7_INDEPENDENT_v3_2.zip';cache=(B/'cache').resolve()
    out=B/'bis/C7_V3_2_CLEAN_VALIDATION.json'
    if out.exists():raise FileExistsError(out)
    env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    receipt=dict(started_utc=datetime.now(timezone.utc).isoformat(),archive_sha256=sha(archive),status='INCOMPLETE',logs=[],directory=None)
    parent=Path(tempfile.mkdtemp(prefix='v3clean_',dir=cache)).resolve()
    try:
        if not parent.is_relative_to(cache) or parent==cache:raise ValueError('Unsafe temporary')
        receipt['directory']=str(parent)
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                rel=PurePosixPath(info.filename)
                if rel.is_absolute() or '..' in rel.parts or '\\' in info.filename:raise ValueError('Unsafe archive')
                path=parent/rel;path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('xb') as f:f.write(z.read(info))
        root=parent/'C7_INDEPENDENT_v3_2'
        commands=[['verify_delivery.py'],['-O','unit_checks.py'],['reproduce_c6.py'],
          ['reproduce_c6.py','--run','--source-cache',str(B/'cache/gwosc/on_source'),'--work-root',str(cache),'--output',str(B/'bis/C7_V3_2_C6_REPLAY.json')]]
        for i,command in enumerate(commands):
            log=B/f'bis/C7_V3_2_CLEAN_{i}.log'
            with log.open('xb') as f:
                p=subprocess.run([sys.executable,'-B',*command],cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
            receipt['logs'].append(dict(command=command,exit_code=p.returncode,path=str(log.relative_to(B)),sha256=sha(log)))
            print(json.dumps(receipt['logs'][-1]),flush=True)
            if p.returncode:raise RuntimeError('Validation failed; log preserved')
        receipt['status']='PASS_BYTE_UNIT_AND_C6_NUMERICAL_REPRODUCTION'
    except Exception as e:
        receipt['status']='FAILED';receipt['error']=str(e);raise
    finally:
        if not parent.is_relative_to(cache) or parent==cache:raise ValueError('Unsafe cleanup')
        shutil.rmtree(parent);receipt['temporary_removed']=not parent.exists()
        receipt['finished_utc']=datetime.now(timezone.utc).isoformat();receipt['builder_sha256']=sha(Path(__file__))
        with out.open('xb') as f:f.write((json.dumps(receipt,indent=2)+'\n').encode())
if __name__=='__main__':main()
