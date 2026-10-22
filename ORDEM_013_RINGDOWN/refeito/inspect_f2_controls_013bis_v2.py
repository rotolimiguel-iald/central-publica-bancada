"""Read public control schemas without executing archived code or pickle."""
from pathlib import Path
import json, hashlib
import h5py
ROOT=Path(__file__).resolve().parents[1]
receipt=json.loads((ROOT/'bis/F2_CONTROL_EXTRACTION.json').read_bytes())
out=[]
for archive in receipt['archives']:
    chosen=[]
    for row in archive['files']:
        if archive['kind']=='LVK_INJECTION' or (row['path'].endswith('.nc') and len(chosen)<6):
            chosen.append(row)
    for row in chosen:
        p=ROOT/row['path'].replace('\\','/')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError(p)
        item=dict(path=row['path'],sha256=row['sha256'])
        if p.suffix in ('.h5','.nc'):
            datasets=[]
            with h5py.File(p,'r') as f:
                def visit(name,obj):
                    if isinstance(obj,h5py.Dataset):
                        d=dict(name=name,shape=obj.shape,dtype=str(obj.dtype))
                        if 'config' in name.lower() and obj.size<10:
                            d['text']=str(obj[()])[:12000]
                        datasets.append(d)
                f.visititems(visit)
                item['root_attributes']={str(k):str(v) for k,v in f.attrs.items()}
            item['datasets']=datasets
        else:item['first_lines']=p.read_text().splitlines()[:4]
        out.append(item)
p=ROOT/'bis/F2_CONTROL_SCHEMAS.json'
raw=(json.dumps(out,indent=2,ensure_ascii=False)+'\n').encode()
with p.open('xb') as f:f.write(raw)
for item in out:
    print(item['path'])
    for d in item.get('datasets',[]):
        if d['name'].startswith('posterior/') or 'posterior_samples' in d['name']:print(d)
    print(item.get('first_lines',[]))
