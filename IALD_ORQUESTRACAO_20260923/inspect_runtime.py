"""Read only deployment readiness: health, active slots and reservation metadata."""
import json
from pathlib import Path
import sqlite3
import urllib.request

root=Path(r'C:\IALD\projetos_pyhton\IALD')
for path in sorted(root.glob('*.reservas.sqlite3')):
    with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) as db:
        counts=db.execute('SELECT status,count(*) FROM calls GROUP BY status').fetchall()
        print(json.dumps({'database':path.name,'counts_by_status':counts},ensure_ascii=False))
for port,endpoint in [(8082,'health'),(8081,'slots')]:
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/{endpoint}',timeout=5) as response:
        value=json.loads(response.read())
    if endpoint=='slots':
        value=[{k:row.get(k) for k in ('id','is_processing')} for row in value]
    else:
        value={'http_status':response.status}
    print(json.dumps({'port':port,'endpoint':endpoint,'value':value}))
