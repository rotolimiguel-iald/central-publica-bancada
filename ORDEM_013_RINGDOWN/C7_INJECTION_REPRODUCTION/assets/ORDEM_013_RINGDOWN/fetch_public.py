"""Download public Zenodo releases into this task's cache with hash verification.

No archive is extracted by this script. No strain samples are read.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent

def atomic_json(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    if path.exists():
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        path.with_name(path.name+'.bak_'+stamp).write_bytes(path.read_bytes())
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw)
    temporary.replace(path)

def digests(path):
    md5, sha = hashlib.md5(), hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(8*1024*1024):
            md5.update(block); sha.update(block)
    return md5.hexdigest(), sha.hexdigest()

def fetch(record, key=None):
    folder = ROOT/'cache'/'public'/str(record)
    folder.mkdir(parents=True, exist_ok=True)
    url = f'https://zenodo.org/api/records/{record}'
    with urllib.request.urlopen(url, timeout=60) as response:
        meta = json.load(response)
    atomic_json(folder/'record.json', meta)
    print(json.dumps({'record':record,'title':meta['metadata']['title'],
                      'files':[{k:f[k] for k in ('key','size','checksum')} for f in meta['files']]}), flush=True)
    if key is None:
        return
    item = next(f for f in meta['files'] if f['key']==key)
    if Path(key).name != key:
        raise ValueError('Expected an archive filename, not a path')
    target, partial = folder/key, folder/(key+'.partial')
    source = item['links']['self']
    if not target.exists():
        offset = partial.stat().st_size if partial.exists() else 0
        headers = {'Range':f'bytes={offset}-'} if offset else {}
        with urllib.request.urlopen(urllib.request.Request(source, headers=headers),timeout=60) as response:
            if offset and (response.status != 206 or not response.headers.get('Content-Range','').startswith(f'bytes {offset}-')):
                raise RuntimeError('Server did not honor resume; preserve partial and investigate')
            with partial.open('ab' if offset else 'xb') as stream:
                last = offset
                while block := response.read(4*1024*1024):
                    stream.write(block); offset += len(block)
                    if offset-last >= 100*1024*1024:
                        print(json.dumps({'record':record,'downloaded_bytes':offset,'total_bytes':item['size']}),flush=True)
                        last=offset
        if partial.stat().st_size != item['size']:
            raise RuntimeError('Incomplete download, left .partial intact')
        md5, sha = digests(partial)
        if item['checksum'] != 'md5:'+md5:
            raise RuntimeError('Release MD5 mismatch; partial preserved')
        partial.replace(target)
    else:
        md5, sha = digests(target)
        if target.stat().st_size != item['size'] or item['checksum'] != 'md5:'+md5:
            raise RuntimeError('Existing artifact differs from release')
    receipt = dict(record=record,doi=meta['doi'],url=source,path=str(target),bytes=target.stat().st_size,
                   md5=md5,sha256=sha,retrieved_utc=datetime.now(timezone.utc).isoformat(),
                   release_checksum_verified=True,extracted=False)
    atomic_json(folder/(key+'.receipt.json'),receipt)
    print(json.dumps(receipt),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('record',type=int)
    parser.add_argument('--key')
    args=parser.parse_args()
    fetch(args.record,args.key)
