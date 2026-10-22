"""Run an archival numerical replay only in a temporary package copy.

No run occurs without --run. ORDEM013BIS does not reopen the C5 campaign.
"""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import argparse,hashlib,json,shutil,tempfile,subprocess,os,sys
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',action='store_true');p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--work-root',type=Path);p.add_argument('--output-root',type=Path);args=p.parse_args()
    manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
    for r in manifest['files']:
        rel=PurePosixPath(r['path']);source=(ROOT/rel).resolve()
        if rel.is_absolute() or '..' in rel.parts or '\\' in r['path'] or not source.is_relative_to(ROOT):raise ValueError('Unsafe path')
        if source.is_symlink() or sha(source)!=r['sha256']:raise ValueError('Package changed')
    if not args.run and not args.prepare_only:
        print(json.dumps(dict(status='HASHES_VERIFIED_NO_COMPUTATION',files=len(manifest['files']))));return
    if args.run and args.prepare_only:p.error('Choose run or preparation only')
    if not args.work_root or not args.output_root:p.error('Work/output roots required')
    work=args.work_root.resolve();out=args.output_root.resolve()
    if work.is_relative_to(ROOT) or out.is_relative_to(ROOT):raise ValueError('Roots must be outside package')
    work.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
    destination=out/(ROOT.name+'_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    destination.mkdir();report=dict(status='INTERRUPTED',scientific_calibration=False)
    temporary=Path(tempfile.mkdtemp(prefix='legacy_replay_',dir=work)).resolve()
    try:
        if not temporary.is_relative_to(work) or temporary==work:raise ValueError('Unsafe temporary')
        for r in manifest['files']:
            target=temporary/r['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/r['path'],target)
        shutil.copyfile(ROOT/'MANIFEST.json',temporary/'MANIFEST.json')
        if args.prepare_only:report['status']='PREPARATION_VERIFIED_NO_COMPUTATION'
        else:
            env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
            with (destination/'run.log').open('xb') as stream:
                process=subprocess.run([sys.executable,'-B',str(temporary/'reproduce_legacy.py')],cwd=temporary,env=env,stdout=stream,stderr=subprocess.STDOUT)
            report['exit_code']=process.returncode;report['status']='LEGACY_REPLAY_EXIT_ZERO' if process.returncode==0 else 'LEGACY_REPLAY_FAILED'
            for source in temporary.rglob('RESULT.json'):
                target=destination/'results'/source.relative_to(temporary);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
            if process.returncode:raise RuntimeError('Legacy replay failed; external log preserved')
    except Exception as error:
        report['error']=str(error);raise
    finally:
        if not temporary.is_relative_to(work) or temporary==work:raise ValueError('Unsafe cleanup')
        shutil.rmtree(temporary)
        report.update(temporary_removed=not temporary.exists(),temporary=str(temporary),utc=datetime.now(timezone.utc).isoformat(),manifest_sha256=sha(ROOT/'MANIFEST.json'))
        with (destination/'RECEIPT.json').open('xb') as f:f.write((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(report))
if __name__=='__main__':main()
