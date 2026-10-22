"""List a verified release, then extract only explicitly selected regular files.

No extractall, links, paths outside the task cache, or on-source strain access.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import tarfile
from fetch_public import atomic_json, digests

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--member',action='append',default=[])
    parser.add_argument('--record',type=int,default=17018009)
    parser.add_argument('--archive',default='TGR_companion_S250114ax_results.tar.gz')
    parser.add_argument('--flat',action='store_true',help='Short hashed paths; original member retained in receipt')
    args=parser.parse_args()
    if Path(args.archive).name!=args.archive:raise ValueError('Archive must be a basename')
    folder=ROOT/'cache/public'/str(args.record)
    archive=folder/args.archive
    receipt=json.loads((folder/(archive.name+'.receipt.json')).read_bytes())
    sha=digests(archive)[1]
    if sha!=receipt['sha256']:raise ValueError('Archive hash differs from verified download')
    index_path=folder/'archive_index.json'
    if not index_path.exists():
        with tarfile.open(archive,'r:gz') as tar:
            index=[dict(name=m.name,size=m.size,regular=m.isfile(),link=m.issym() or m.islnk()) for m in tar]
        atomic_json(index_path,dict(archive_sha256=sha,members=index))
    else:
        index_doc=json.loads(index_path.read_bytes())
        if index_doc['archive_sha256']!=sha:raise ValueError('Stale archive index')
        index=index_doc['members']
    relevant=[m for m in index if (args.record!=17018009 or 'gw250114_pseobnr' in m['name'] or
             ('TEOB' in m['name'] and any(s in m['name'] for s in ['config','prior','.ini']))) and m['regular']]
    if not args.member:
        print(json.dumps(dict(member_count=len(index),candidates=relevant[:120])),flush=True)
    else:
        print(json.dumps(dict(member_count=len(index),requested=args.member)),flush=True)
    if not args.member:return
    allowed={m['name']:m for m in index if m['regular'] and not m['link']}
    for name in args.member:
        p=PurePosixPath(name)
        if name not in allowed or p.is_absolute() or '..' in p.parts:
            raise ValueError('Nonregular or unsafe requested member')
        known_documentation={
            'TGR_companion_S250114ax_results/README.md',
            'TGR_companion_S250114ax_results/pyproject.toml',
            'TGR_companion_S250114ax_results/uv.lock',
            'TGR_companion_S250114ax_results/scripts/utils_gw250114.py',
            'TGR_companion_S250114ax_results/scripts/ringdown_directories.py'}
        if not ('pseob' in name.lower() or 'pyring' in name.lower() or name in known_documentation):
            raise ValueError('Only parameter-estimation products allowed in this pass')
        if any(k in name.lower() for k in ['strain','timeseries','time_series']):
            raise ValueError('Strain access requires separate C6 registration')
    found=[]
    with tarfile.open(archive,'r:gz') as tar:
        for member in tar:
            if member.name not in args.member:continue
            rel=PurePosixPath(member.name)
            out=folder/'extracted'/Path(*rel.parts)
            if args.flat:
                out=folder/'selected'/(hashlib.sha256(member.name.encode()).hexdigest()[:16]+rel.suffix)
            out.parent.mkdir(parents=True,exist_ok=True)
            data=tar.extractfile(member).read()
            if len(data)!=member.size:raise ValueError('Truncated archive member')
            if out.exists() and out.read_bytes()!=data:raise ValueError('Changed extracted member')
            if not out.exists():
                temp=out.with_suffix(out.suffix+'.tmp');temp.write_bytes(data)
                assert temp.stat().st_size==len(data);temp.replace(out)
            found.append(dict(member=member.name,size=len(data),sha256=hashlib.sha256(data).hexdigest(),path=str(out)))
            if len(found)==len(args.member):break
    if len(found)!=len(args.member):raise ValueError('Requested member missing')
    receipt_path=folder/'extraction_receipt.json'
    previous=json.loads(receipt_path.read_bytes()) if receipt_path.exists() else {'files':[]}
    merged={row['member']:row for row in previous['files']}
    merged.update({row['member']:row for row in found})
    atomic_json(receipt_path,dict(archive_sha256=sha,files=list(merged.values())))
    print(json.dumps(dict(extracted=found)),flush=True)

if __name__=='__main__':main()
