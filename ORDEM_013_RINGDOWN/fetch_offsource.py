"""Download only complete GWOSC files proven wholly before the target event."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
from urllib.parse import urlparse
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    discovery=json.loads((ROOT/'OFFSOURCE_DISCOVERY.json').read_bytes())
    gps=discovery['event_GPS'];outputs=[]
    folder=ROOT/'cache/gwosc/offsource';folder.mkdir(exist_ok=True)
    for rec in discovery['rows']:
        if 'error' in rec:raise ValueError('Missing off-source discovery')
        for item in rec['data']['strain']:
            if item['format']!='hdf5' or item['sampling_rate']!=4096:continue
            end=item['GPSstart']+item['duration']
            if end>=gps-2:raise ValueError('Source file overlaps forbidden event region')
            parsed=urlparse(item['url'])
            if parsed.scheme!='https' or parsed.netloc!='gwosc.org':raise ValueError('Unexpected source host')
            path=folder/Path(parsed.path).name
            receipt=path.with_name(path.name+'.receipt.json')
            if not path.exists():
                partial=path.with_name(path.name+'.partial')
                if partial.exists():raise ValueError('Partial download preserved; inspect before resuming')
                with urllib.request.urlopen(item['url'],timeout=60) as response:
                    expected=int(response.headers['Content-Length']) if response.headers.get('Content-Length') else None
                    with partial.open('xb') as stream:
                        while block:=response.read(8*1024*1024):stream.write(block)
                if expected is not None and partial.stat().st_size!=expected:raise ValueError('Incomplete download')
                partial.replace(path)
            digest=hashlib.sha256()
            with path.open('rb') as stream:
                while block:=stream.read(8*1024*1024):digest.update(block)
            if receipt.exists() and json.loads(receipt.read_bytes())['sha256']!=digest.hexdigest():
                raise ValueError('Existing off-source file changed')
            row=dict(path=str(path),url=item['url'],detector=item['detector'],
                GPSstart=item['GPSstart'],duration=item['duration'],sample_rate=item['sampling_rate'],
                end_before_event_seconds=gps-end,sha256=digest.hexdigest(),bytes=path.stat().st_size,
                at=datetime.now(timezone.utc).isoformat(),external_checksum='Not supplied by discovery; local SHA256 recorded',
                authorization_scope='Entire file strictly earlier than event GPS-2; no target-event strain bytes downloaded')
            atomic_json(receipt,row);outputs.append(row);print(json.dumps(row),flush=True)
    if {r['detector'] for r in outputs}!={'H1','L1'}:raise ValueError('Missing detector')
    atomic_json(ROOT/'OFFSOURCE_DOWNLOADS.json',dict(status='WHOLLY_OFFSOURCE_FILES_DOWNLOADED',
        target_GPS=gps,files=outputs,on_source_strain_read=False))

if __name__=='__main__':main()
