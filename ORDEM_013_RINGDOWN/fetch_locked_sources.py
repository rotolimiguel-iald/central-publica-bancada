"""Retrieve a public source distribution pinned by the LVK release lockfile.

Never installs or executes the distribution. Package names are CLI inputs;
URLs and hashes come only from the locally verified release artifact.
"""
from pathlib import Path
import argparse
import hashlib
import json
import tomllib
import urllib.request
from fetch_public import atomic_json
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('package',nargs='+');args=p.parse_args()
    receipt=json.loads((ROOT/'cache/public/17018009/extraction_receipt.json').read_bytes())
    row=next(r for r in receipt['files'] if r['member'].endswith('/uv.lock'))
    # Receipt was produced on Windows; the short selected basename is portable.
    name=row['path'].replace('\\','/').split('/')[-1]
    path=ROOT/'cache/public/17018009/selected'/name;raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Lockfile changed')
    lock=tomllib.loads(raw.decode());folder=ROOT/'cache/source_distributions';folder.mkdir(exist_ok=True)
    rows=[]
    for name in args.package:
        package=next(v for v in lock['package'] if v['name']==name);source=package['sdist']
        if not source['url'].startswith('https://files.pythonhosted.org/'):raise ValueError('Nonpublic source host')
        target=folder/Path(source['url']).name
        if target.exists():data=target.read_bytes()
        else:
            with urllib.request.urlopen(source['url'],timeout=40) as response:data=response.read()
        sha=hashlib.sha256(data).hexdigest()
        if len(data)!=source['size'] or 'sha256:'+sha!=source['hash']:raise ValueError('Source hash/size mismatch')
        if not target.exists():
            temp=target.with_suffix(target.suffix+'.tmp');temp.write_bytes(data);temp.replace(target)
        result=dict(package=name,version=package['version'],path=str(target),url=source['url'],
                   sha256=sha,bytes=len(data),lockfile_sha256=row['sha256'],installed=False)
        rows.append(result);print(json.dumps(result),flush=True)
    manifest=folder/'manifest.json';old=json.loads(manifest.read_bytes()) if manifest.exists() else {'packages':[]}
    combined={r['package']:r for r in old['packages']};combined.update({r['package']:r for r in rows})
    atomic_json(manifest,dict(packages=list(combined.values())))

if __name__=='__main__':main()
