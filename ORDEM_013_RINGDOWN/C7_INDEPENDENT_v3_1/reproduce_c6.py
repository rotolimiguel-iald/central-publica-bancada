"""Reproduce the frozen C6-pre diagnostic in a temporary, verified workspace.

The new output is outside the shipped package. No physical gate is upgraded.
Temporary data are removed in finally, including on a failed run.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk)
    return h.hexdigest()
def permit_status(status):
    return isinstance(status,str) and (status.startswith('INCONCLUSIVE_') or status in {'AWAITING_DATA','NOT_VERIFIED','INPUT_INTEGRITY_FAILED'})
def new(p,doc):
    if p.exists():raise FileExistsError(p)
    p.parent.mkdir(parents=True,exist_ok=True);raw=(json.dumps(doc,indent=2,allow_nan=False)+'\n').encode();tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Short write')
    tmp.replace(p)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true');parser.add_argument('--source-cache',type=Path)
    parser.add_argument('--work-root',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
    for r in manifest['files']:
        p=ROOT/r['path']
        if not p.resolve().is_relative_to(ROOT.resolve()) or p.is_symlink():raise ValueError('Unsafe manifest path')
        if p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:raise ValueError('Shipped file changed: '+r['path'])
    if not args.run:
        print(json.dumps(dict(status='PACKAGE_HASHES_VERIFIED',files=len(manifest['files']),experiment_run=False)));return
    if not args.source_cache or not args.work_root or not args.output:parser.error('--run requires --source-cache, --work-root and --output')
    workroot=args.work_root.resolve();workroot.mkdir(parents=True,exist_ok=True)
    output=args.output.resolve()
    if output.is_relative_to(ROOT.resolve()):raise ValueError('Output must be outside shipped package')
    if output.exists():raise FileExistsError(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    started=datetime.now(timezone.utc);parent=Path(tempfile.mkdtemp(prefix='c6pre_v3_',dir=workroot)).resolve()
    if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe temporary path')
    os.chmod(parent,0o755);run=parent/'ORDEM_013_RINGDOWN';logs={};report=dict(status='REPRODUCTION_INTERRUPTED')
    try:
        assets=ROOT/'reproduction'
        for p in assets.rglob('*'):
            if p.is_symlink():raise ValueError('No symlinks in package')
        shutil.copytree(assets,parent,dirs_exist_ok=True)
        if list(run.glob('C6_STRAIN_*_GRID_*.json')) or (run/'C6_RESULTS.json').exists():raise ValueError('Saved outputs present in clean run')
        receipts=json.loads((run/'C6_DOWNLOADS.json').read_bytes())
        folder=run/'cache/gwosc/on_source';folder.mkdir(parents=True,exist_ok=True)
        for r in receipts['files']:
            name=r['path'].replace('\\','/').rsplit('/',1)[-1];src=args.source_cache/name;dst=folder/name
            if src.stat().st_size!=r['bytes'] or sha(src)!=r['sha256']:raise ValueError('Input strain hash mismatch')
            shutil.copyfile(src,dst)
            if sha(dst)!=r['sha256']:raise ValueError('Copy mismatch')
        env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
        log=parent/'run.log'
        with log.open('xb') as stream:
            completed=subprocess.run([sys.executable,'-B',str(run/'run_c6_grid.py')],cwd=run,env=env,stdout=stream,stderr=subprocess.STDOUT)
        logs['run.log']=log.read_bytes()
        if completed.returncode:raise RuntimeError('Frozen diagnostic failed; see preserved output log')
        reference=json.loads((ROOT/'evidence/C6_RESULTS.json').read_bytes());actual=json.loads((run/'C6_RESULTS.json').read_bytes())
        key=lambda r:(r['start_tM'],r['reading'],r['amplitude_prior_sd_strain'])
        wanted={key(r):r for r in reference['results']};found={key(r):r for r in actual['results']}
        if len(wanted)!=len(reference['results']) or len(found)!=len(actual['results']) or found.keys()!=wanted.keys():raise ValueError('Result coverage/duplicates differ')
        error=max(abs(found[k]['lnB_vs_GR']-wanted[k]['lnB_vs_GR']) for k in wanted)
        if error>1e-5:raise ValueError('Numeric reproduction differs')
        if not permit_status(actual['status']):raise ValueError('Physical status promotion or unknown status')
        report=dict(status='PASS_NUMERICAL_REPRODUCTION',actual_scientific_status=actual['status'],rows=len(found),max_lnB_difference=error,
          all_windows_recomputed_from_strain=True,preexisting_window_results=[],registration_sha256=actual['registration_sha256'],
          frozen_reference_sha256=sha(ROOT/'evidence/C6_RESULTS.json'),manifest_sha256=sha(ROOT/'MANIFEST.json'),code_sha256=sha(Path(__file__)))
    except Exception as error:
        report=dict(status='REPRODUCTION_FAILED',error_type=type(error).__name__,error=str(error))
        if (parent/'run.log').exists():logs['run.log']=(parent/'run.log').read_bytes()
        raise
    finally:
        # The checked target is a newly created child of the explicit work root.
        if not parent.is_relative_to(workroot) or parent==workroot:raise ValueError('Unsafe cleanup target')
        shutil.rmtree(parent)
        if parent.exists():raise RuntimeError('Temporary cleanup failed')
        end=datetime.now(timezone.utc)
        report.update(started_utc=started.isoformat(),finished_utc=end.isoformat(),elapsed_seconds=(end-started).total_seconds(),temporary_removed=True,temporary_path=str(parent))
        report['logs']={}
        for name,raw in logs.items():
            dest=output.with_name(output.stem+'_'+name)
            with dest.open('xb') as f:f.write(raw)
            report['logs'][str(dest)]=sha(dest)
        new(output,report)
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
