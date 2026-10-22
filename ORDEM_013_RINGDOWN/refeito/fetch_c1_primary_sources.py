"""Archive primary-source retrieval attempts, without claiming unperformed reading."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,urllib.request

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'cache/literature/013bis'
folder.mkdir(exist_ok=True)
urls={
 'bisognano_wichmann_1975.pdf':'https://denebola.if.usp.br/~jbarata/leituras-recomendadas/BisognanoWichmann-01-DualityConditionHermitianScalarField_985_1_online.pdf',
 'bisognano_wichmann_1976.pdf':'https://denebola.if.usp.br/~jbarata/leituras-recomendadas/BisognanoWichmann-02-DualityConditionQuantumFields_303_1_online.pdf',
 'kay_wald_1991_publisher.html':'https://www.sciencedirect.com/science/article/abs/pii/037015739190015E',
 'kay_wald_1991_author.html':'https://pure.york.ac.uk/portal/en/publications/theorems-on-the-uniqueness-and-thermal-properties-of-stationary-n/',
 'sewell_1982_publisher.html':'https://doi.org/10.1016/0003-4916(82)90285-8',
}
rows=[]
for name,url in urls.items():
    row=dict(name=name,url=url,license='NOT_VERIFIED__NO_REDISTRIBUTION',
             reading_scope='RETRIEVAL_ONLY__READING_RECORDED_SEPARATELY')
    p=folder/name
    try:
        if p.exists():
            raw=p.read_bytes()
        else:
            with urllib.request.urlopen(url,timeout=35) as r:
                raw=r.read();row.update(content_type=r.headers.get('Content-Type'),resolved_url=r.url)
            if name.endswith('.pdf') and not raw.startswith(b'%PDF'):
                raise ValueError('Expected PDF, received non-PDF bytes')
            with p.open('xb') as f: f.write(raw)
        row.update(status='RETRIEVED',path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    except Exception as exc: row.update(status='RETRIEVAL_FAILED',error=repr(exc))
    row['utc']=datetime.now(timezone.utc).isoformat()
    rows.append(row); print(json.dumps(row,ensure_ascii=False),flush=True)
target=ROOT/'bis/C1_PRIMARY_RETRIEVALS.json'
with target.open('x',encoding='utf-8') as f: json.dump(rows,f,ensure_ascii=False,indent=2);f.write('\n')
