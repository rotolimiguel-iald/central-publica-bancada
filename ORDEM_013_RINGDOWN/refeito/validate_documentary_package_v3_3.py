"""Validate attribution-only correction and prove execution bytes unchanged."""
from pathlib import Path,PurePosixPath
import json,hashlib,tempfile,zipfile,shutil,subprocess,sys
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=B/'C7_INDEPENDENT_v3_2';new=B/'C7_INDEPENDENT_v3_3';out=B/'bis/C7_V3_3_DOCUMENTARY_VALIDATION.json'
    if out.exists():raise FileExistsError(out)
    m0=json.loads((old/'MANIFEST.json').read_bytes());m1=json.loads((new/'MANIFEST.json').read_bytes())
    lookup={r['path']:r for r in m0['files']};changed=[];execution=[]
    for r in m1['files']:
        n=r['path']
        if n not in lookup or lookup[n]['sha256']!=r['sha256']:changed.append(n)
        if n.startswith('reproduction/') or n.endswith('.py'):
            if n not in lookup or sha(old/n)!=sha(new/n):raise ValueError('Execution bytes changed '+n)
            execution.append(n)
    allowed={'README.md','OVERVIEW.md','provenance/SHIPPED_ATTRIBUTIONS.json'}
    if set(changed)-allowed:raise ValueError('Beyond documentary correction: '+str(changed))
    attrs=json.loads((new/'provenance/SHIPPED_ATTRIBUTIONS.json').read_bytes())['files']
    if len({r['path'] for r in attrs})!=len(attrs) or {r['path'] for r in attrs}!={r['path'] for r in m1['files']}-{'provenance/SHIPPED_ATTRIBUTIONS.json'}:raise ValueError('Attribution coverage')
    for r in attrs:
        if r['sha256']!=sha(new/r['path']):raise ValueError('Attribution mismatch')
    cache=(B/'cache').resolve();report=dict(status='INCOMPLETE',changed_files=changed,execution_files_identical=execution,attribution_hashes_verified=len(attrs),replayed_science=False,prior_replay='bis/C7_V3_2_C6_REPLAY.json',prior_replay_sha256=sha(B/'bis/C7_V3_2_C6_REPLAY.json'))
    temp=Path(tempfile.mkdtemp(prefix='docv3_',dir=cache)).resolve()
    try:
        if not temp.is_relative_to(cache) or temp==cache:raise ValueError('Unsafe temp')
        with zipfile.ZipFile(B/'cache/C7_INDEPENDENT_v3_3.zip') as z:
            for n in z.namelist():
                rel=PurePosixPath(n)
                if rel.is_absolute() or '..' in rel.parts or '\\' in n:raise ValueError('Unsafe zip')
                p=temp/rel;p.parent.mkdir(parents=True,exist_ok=True)
                with p.open('xb') as f:f.write(z.read(n))
        root=temp/new.name;reports=[]
        for args in [['verify_delivery.py'],['-O','unit_checks.py'],['reproduce_c6.py']]:
            run=subprocess.run([sys.executable,'-B',*args],cwd=root,capture_output=True)
            if run.returncode:raise RuntimeError(run.stderr.decode(errors='replace'))
            reports.append(dict(args=args,result=json.loads(run.stdout)))
        report.update(status='PASS_DOCUMENTARY_CORRECTION_SAME_EXECUTION_BYTES',checks=reports,archive_sha256=sha(B/'cache/C7_INDEPENDENT_v3_3.zip'))
    finally:
        if not temp.is_relative_to(cache) or temp==cache:raise ValueError('Unsafe cleanup')
        shutil.rmtree(temp);report['temporary_removed']=not temp.exists()
        with out.open('xb') as f:f.write((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k!='execution_files_identical'}))
if __name__=='__main__':main()
