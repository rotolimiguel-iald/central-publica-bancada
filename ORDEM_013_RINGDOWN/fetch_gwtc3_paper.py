"""Archive primary GWTC-3 HTML to recover its published event selection."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent


def main():
    url='https://arxiv.org/html/2112.06861v3'
    path=ROOT/'cache/literature/gwtc3_article_v3.html'
    receipt=ROOT/'C4_GWTC3_PAPER_RECEIPT.json'
    if path.exists() or receipt.exists():
        raise FileExistsError('Preserve prior download and inspect it')
    try:
        with urllib.request.urlopen(url,timeout=60) as response:
            raw=response.read()
        if b'GW191109_010717' not in raw or b'pSEOBNRv4HM' not in raw:
            raise ValueError('Unexpected scientific HTML')
        temporary=path.with_suffix('.html.partial')
        temporary.write_bytes(raw)
        if temporary.stat().st_size != len(raw):
            raise ValueError('Short write')
        temporary.replace(path)
        record=dict(status='RETRIEVED_NOT_FULLY_READ',url=url,path=path.relative_to(ROOT).as_posix(),
            bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),date_utc=datetime.now(timezone.utc).isoformat())
    except Exception as exc:
        record=dict(status='FAILED',url=url,error=str(exc),date_utc=datetime.now(timezone.utc).isoformat())
        atomic_json(receipt,record)
        raise
    atomic_json(receipt,record)
    print(json.dumps(record))


if __name__=='__main__':
    main()
