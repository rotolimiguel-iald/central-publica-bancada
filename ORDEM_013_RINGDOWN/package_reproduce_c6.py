"""Recompute the frozen actual-strain experiment from verified public inputs.

Default action verifies the registration only. --run requires --download or
--source-cache to populate the two public strain files and then recomputes
all five registered windows, without copying their saved outputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'reproduction/ORDEM_013_RINGDOWN'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while part:=stream.read(1024*1024):h.update(part)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',action='store_true')
    p.add_argument('--download',action='store_true');p.add_argument('--source-cache',type=Path)
    args=p.parse_args()
    if args.download and args.source_cache:p.error('Use one data source')
    sys.path.insert(0,str(RUN));from c6_engine import checked_registration
    reg,regsha=checked_registration()
    print(json.dumps(dict(registration='PASS',sha256=regsha)),flush=True)
    if not args.run:return
    receipts=json.loads((RUN/'C6_DOWNLOADS.json').read_bytes())
    folder=RUN/'cache/gwosc/on_source';folder.mkdir(parents=True,exist_ok=True)
    for item in receipts['files']:
        name=item['path'].replace('\\','/').rsplit('/',1)[-1];target=folder/name
        if not target.exists():
            partial=target.with_suffix('.partial')
            if partial.exists():raise FileExistsError('Preserve and inspect previous incomplete download')
            if args.source_cache:
                source=args.source_cache/name
                if digest(source)!=item['sha256']:raise ValueError('Source cache checksum mismatch')
                shutil.copyfile(source,partial)
            elif args.download:
                with urllib.request.urlopen(item['url'],timeout=60) as response,partial.open('xb') as output:
                    shutil.copyfileobj(response,output)
            else:raise ValueError('Use --download or --source-cache to supply raw public strain')
            if partial.stat().st_size!=item['bytes'] or digest(partial)!=item['sha256']:
                raise ValueError('Public strain differs from archived measurement; partial preserved')
            partial.replace(target)
        if digest(target)!=item['sha256']:raise ValueError('Cached public strain changed')
    # Initial delivered package has no result files in RUN. Later repeats visibly
    # reuse same-registration outputs according to the original orchestrator.
    preexisting=[p.name for p in RUN.glob('C6_STRAIN_*_GRID_*.json')]
    result=subprocess.run([sys.executable,'-B',str(RUN/'run_c6_grid.py')],check=False)
    if result.returncode:raise RuntimeError('Frozen experiment failed')
    expected=json.loads((ROOT/'evidence/C6_RESULTS.json').read_bytes())
    actual=json.loads((RUN/'C6_RESULTS.json').read_bytes())
    key=lambda r:(r['start_tM'],r['reading'],r['amplitude_prior_sd_strain'])
    reference={key(r):r for r in expected['results']};current={key(r):r for r in actual['results']}
    if reference.keys()!=current.keys():raise ValueError('Result coverage differs')
    difference=max(abs(current[k]['lnB_vs_GR']-reference[k]['lnB_vs_GR']) for k in reference)
    if difference>1e-5:raise ValueError(f'Independent-directory reproduction differs: {difference}')
    if actual['status']!='INCONCLUSIVE_SYSTEMATICS':raise ValueError('Scientific status was promoted')
    out=dict(status='PASS',registration_sha256=regsha,rows=len(current),
        max_lnB_difference=difference,preexisting_window_results=preexisting,
        all_windows_recomputed_from_strain=not preexisting)
    target=ROOT/'C6_REPRODUCTION_RESULT.json';temp=target.with_suffix('.tmp')
    if target.exists():raise FileExistsError('Keep previous reproduction result; use a fresh package directory')
    temp.write_bytes(json.dumps(out,indent=2).encode());temp.replace(target)
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
