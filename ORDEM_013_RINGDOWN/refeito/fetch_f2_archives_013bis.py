"""Fetch only the two registered, public, non-blind robustness archives."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
import tarfile

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'cache/public/21454847'
meta_path=FOLDER/'record.json'
meta=json.loads(meta_path.read_bytes())
results=[]
for key in ('QNMRF.tar.gz','RD.tar.gz'):
    entry=next(x for x in meta['files'] if x['key']==key)
    path=FOLDER/key
    row=dict(key=key,url=entry['links']['self'],expected_bytes=entry['size'],
             expected_checksum=entry['checksum'],license=meta['metadata']['license'],
             license_source_sha256=hashlib.sha256(meta_path.read_bytes()).hexdigest(),
             non_blind=True,scope='Published before registration; robustness/calibration only')
    try:
        if not path.exists():
            partial=FOLDER/(key+'.013bis.partial')
            offset=partial.stat().st_size if partial.exists() else 0
            request=urllib.request.Request(row['url'],headers={'Range':f'bytes={offset}-'} if offset else {})
            with urllib.request.urlopen(request,timeout=45) as response:
                if offset and (response.status!=206 or not response.headers.get('Content-Range','').startswith(f'bytes {offset}-')):
                    raise RuntimeError('Resume not honored; partial preserved')
                with partial.open('ab' if offset else 'xb') as f:
                    while block:=response.read(4*1024*1024): f.write(block)
            candidate=partial
        else: candidate=path
        md5,sha=hashlib.md5(),hashlib.sha256()
        with candidate.open('rb') as f:
            while block:=f.read(4*1024*1024): md5.update(block);sha.update(block)
        if candidate.stat().st_size!=entry['size'] or 'md5:'+md5.hexdigest()!=entry['checksum']:
            raise RuntimeError('Size or MD5 mismatch; preserve suspect file')
        if candidate!=path: candidate.replace(path)
        listing=[]
        with tarfile.open(path,'r:gz') as tar:
            for member in tar:
                listing.append(dict(name=member.name,bytes=member.size,type=member.type.decode('ascii','replace')))
        row.update(status='DOWNLOADED_VERIFIED_LISTED',sha256=sha.hexdigest(),md5=md5.hexdigest(),
                   bytes=path.stat().st_size,path=str(path),members=listing)
    except Exception as exc:
        row.update(status='DOWNLOAD_OR_VALIDATION_FAILED',error=repr(exc))
    row['utc']=datetime.now(timezone.utc).isoformat()
    results.append(row)
    print(json.dumps({k:v for k,v in row.items() if k!='members'},ensure_ascii=False),flush=True)
out=ROOT/'bis/F2_ARCHIVE_DOWNLOADS.json'
with out.open('x',encoding='utf-8') as f: json.dump(results,f,ensure_ascii=False,indent=2);f.write('\n')
print('receipt_sha256',hashlib.sha256(out.read_bytes()).hexdigest(),flush=True)
