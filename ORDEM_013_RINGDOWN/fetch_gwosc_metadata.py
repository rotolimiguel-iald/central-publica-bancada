"""Discover GW250114 public file URLs and parameters; never download/read strain."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    folder=ROOT/'cache/gwosc';folder.mkdir(exist_ok=True)
    endpoints=[
      'https://gwosc.org/api/v2/events/GW250114_082203',
      'https://gwosc.org/api/v2/events/GW250114_082203/strain-files',
      'https://gwosc.org/eventapi/json/O4_Discovery_Papers/GW250114_082203/v1/']
    records=[]
    for index,url in enumerate(endpoints):
        try:
            with urllib.request.urlopen(url,timeout=30) as response:
                body=response.read();value=json.loads(body)
                mime=response.headers.get('Content-Type');effective=response.url
            path=folder/f'metadata_{index}.json'
            if path.exists() and path.read_bytes()!=body:
                path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S')).write_bytes(path.read_bytes())
            temp=path.with_suffix('.tmp');temp.write_bytes(body);assert temp.stat().st_size==len(body);temp.replace(path)
            row=dict(url=url,effective_url=effective,path=str(path),sha256=hashlib.sha256(body).hexdigest(),
                     content_type=mime,status='METADATA_ONLY',keys=list(value) if isinstance(value,dict) else None)
            print(json.dumps(dict(record=row,content=value)),flush=True)
        except Exception as exc:
            row=dict(url=url,status='FAILED',error=repr(exc));print(json.dumps(row),flush=True)
        records.append(row)
    atomic_json(ROOT/'GWOSC_METADATA.json',dict(at=datetime.now(timezone.utc).isoformat(),
        records=records,strain_downloaded=False,on_source_strain_read=False))

if __name__=='__main__':main()
