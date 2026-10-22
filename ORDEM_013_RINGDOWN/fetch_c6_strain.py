"""Fetch registered public strain only after verifying the delivered C6 hash."""
from pathlib import Path
from datetime import datetime,timezone
import json
import urllib.request
from urllib.parse import urlparse
from c6_engine import checked_registration
from fetch_public import atomic_json,digests

ROOT=Path(__file__).resolve().parent

def main():
    reg,digest=checked_registration()
    folder=ROOT/'cache/gwosc/on_source';folder.mkdir(exist_ok=True)
    rows=[]
    for item in reg['target_downloads']:
        url=item['hdf5_url'];parsed=urlparse(url)
        if parsed.scheme!='https' or parsed.netloc!='gwosc.org':raise ValueError('Non-GWOSC registered source')
        path=folder/Path(parsed.path).name;receipt=path.with_name(path.name+'.receipt.json')
        if not path.exists():
            partial=path.with_name(path.name+'.partial')
            if partial.exists():raise FileExistsError('Preserve incomplete download before retry')
            with urllib.request.urlopen(url,timeout=60) as response:
                expected=int(response.headers['Content-Length']) if response.headers.get('Content-Length') else None
                with partial.open('xb') as stream:
                    while block:=response.read(8*1024*1024):stream.write(block)
            if expected is not None and partial.stat().st_size!=expected:raise ValueError('Truncated download')
            partial.replace(path)
        sha=digests(path)[1]
        if receipt.exists() and json.loads(receipt.read_bytes())['sha256']!=sha:raise ValueError('Existing strain changed')
        row=dict(path=str(path),detector=item['detector'],url=url,sha256=sha,bytes=path.stat().st_size,
            registration_sha256=digest,downloaded_utc=datetime.now(timezone.utc).isoformat(),
            external_checksum='Not supplied by GWOSC metadata; local SHA256 recorded',samples_analyzed=False)
        atomic_json(receipt,row);rows.append(row);print(json.dumps(row),flush=True)
    if {r['detector'] for r in rows}!={'H1','L1'}:raise ValueError('Missing detector')
    atomic_json(ROOT/'C6_DOWNLOADS.json',dict(status='REGISTERED_TARGET_FILES_DOWNLOADED',registration_sha256=digest,files=rows))

if __name__=='__main__':main()
