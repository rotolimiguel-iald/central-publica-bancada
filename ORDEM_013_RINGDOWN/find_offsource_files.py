"""Locate a preceding GWOSC file whose entire span excludes the event window."""
from pathlib import Path
import hashlib
import json
import urllib.request
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    meta=json.loads((ROOT/'cache/gwosc/metadata_2.json').read_bytes())
    event,=meta['events'].values();gps=event['GPS']
    entries=[x for x in event['strain'] if x['format']=='hdf5' and x['sampling_rate']==4096]
    outputs=[]
    for entry in entries:
        dataset=entry['url'].split('/archive/data/',1)[1].split('/')[0]
        stop=int(entry['GPSstart'])-1;start=stop-4094
        url=f'https://gwosc.org/archive/links/{dataset}/{entry["detector"]}/{start}/{stop}/json/'
        try:
            with urllib.request.urlopen(url,timeout=30) as response:body=response.read();data=json.loads(body)
            path=ROOT/'cache/gwosc'/f'offsource_links_{entry["detector"]}.json'
            atomic_json(path,data)
            outputs.append(dict(detector=entry['detector'],url=url,metadata_path=str(path),
                                metadata_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),data=data))
        except Exception as exc:outputs.append(dict(url=url,error=repr(exc)))
    atomic_json(ROOT/'OFFSOURCE_DISCOVERY.json',dict(event_GPS=gps,
        rule='Download only files whose entire [GPSstart,GPSend] interval ends before event GPS-2; no event-window bytes requested',rows=outputs))
    print(json.dumps(outputs),flush=True)

if __name__=='__main__':main()
