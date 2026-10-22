"""Archive primary public pages; retrieval is not a claim of full-text reading."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent
SOURCES={
 'gw250114_article.html':'https://arxiv.org/html/2509.08099v1',
 'gw250114_source.tar':'https://arxiv.org/e-print/2509.08099v1',
 'almost_periodic_article.html':'https://arxiv.org/html/2406.00874v1',
 'simon_jaksch_abstract.html':'https://arxiv.org/abs/quant-ph/0406007',
 'kay_wald_author_abstract.html':'https://pure.york.ac.uk/portal/en/publications/theorems-on-the-uniqueness-and-thermal-properties-of-stationary-n/',
 'milburn_publisher_abstract.html':'https://journals.aps.org/pra/abstract/10.1103/PhysRevA.44.5401',
 'gwtc5_tgr_abstract.html':'https://arxiv.org/abs/2607.19293',
}

def main():
    folder=ROOT/'cache/literature';folder.mkdir(parents=True,exist_ok=True)
    records=[]
    for name,url in SOURCES.items():
        path=folder/name
        try:
            if path.exists():raw=path.read_bytes();mime='existing_cached_content'
            else:
                with urllib.request.urlopen(url,timeout=30) as response:
                    raw=response.read();mime=response.headers.get('Content-Type')
                if not raw:raise ValueError('Empty source')
                temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(raw)
                assert temp.stat().st_size==len(raw);temp.replace(path)
            row=dict(name=name,url=url,path=str(path),bytes=len(raw),content_type=mime,
                     sha256=hashlib.sha256(raw).hexdigest(),status='RETRIEVED',
                     note='Reading scope recorded separately; never infer full reading from download')
        except Exception as error:
            row=dict(name=name,url=url,status='RETRIEVAL_FAILED',error=str(error))
        records.append(row);print(json.dumps(row),flush=True)
    atomic_json(ROOT/'LITERATURE_MANIFEST.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=records))

if __name__=='__main__':main()
