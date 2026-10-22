"""Metadata-only long-path inventory of four expressly named historical caches."""
from pathlib import Path
from datetime import datetime,timezone
import os,json,stat
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');D=B/'bis/015/t13'
names=['guard_7h3lo515','native_package_tamper_20260922_080445_470834','delivery_fresh_20260922_025830_447404','delivery_v2_fresh_20260922_032436_194092']
rows=[]
for name in names:
    root=B/'cache'/name;errors=[];sizes=[];links=[];files=0
    for parent,dirs,leaves in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
        for leaf in leaves:
            p=Path(parent)/leaf
            try:
                s=p.lstat();sizes.append(s.st_size);files+=1
                if stat.S_ISLNK(s.st_mode):links.append(str(p))
            except OSError as e:errors.append(str(e))
    rows.append(dict(name=name,files=files,bytes=sum(sizes),errors=errors,links_not_followed=links,deleted=False,role_statute='INFERRED_FROM_HISTORICAL_PATH_NAME',deletable='NOT_AUTHORIZED_WITHOUT_REFERENCE_AUDIT'))
out=D/'CACHE_INVENTORY_WSL.json';raw=(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),rows=rows,content_read=False),indent=2)+'\n').encode()
with out.open('xb') as f:f.write(raw)
print(json.dumps([dict(name=r['name'],files=r['files'],bytes=r['bytes'],errors=len(r['errors'])) for r in rows]))
