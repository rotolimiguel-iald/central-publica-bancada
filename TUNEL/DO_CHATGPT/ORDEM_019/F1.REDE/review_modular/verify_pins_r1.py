"""Verify declared file hashes transitively, without changing originals."""
from pathlib import Path
import json, hashlib
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
queue=[ROOT/'modular_wedge/RESULTADO_MODULAR_R1.json',ROOT/'fubini/DELIVERY_R1.json',ROOT/'fiber_conjugation/DELIVERY_FIBER_R1.json']
seen=set(); pins={}; errors=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def walk(x):
    if isinstance(x,dict):
        if 'path' in x and 'sha256' in x:
            p=Path(x['path']); want=x['sha256']
            try:
                got=sha(p); n=p.stat().st_size
                ok=got==want and ('bytes' not in x or n==x['bytes'])
                row={'path':str(p),'expected_sha256':want,'actual_sha256':got,'bytes':n,'match':ok}
                pins[(str(p),want)]=row
                if not ok: errors.append(row)
                if p.suffix.lower()=='.json': queue.append(p)
            except Exception as e: errors.append({'path':str(p),'error':str(e)})
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
while queue:
    p=queue.pop()
    if str(p) in seen: continue
    seen.add(str(p)); walk(json.loads(p.read_text(encoding='utf-8-sig')))
result={'root_manifest_sha256':sha(ROOT/'modular_wedge/RESULTADO_MODULAR_R1.json'),'checked_pin_count':len(pins),'checked_json_count':len(seen),'errors':errors,'pins':list(pins.values())}
out=BASE/'PIN_VERIFICATION_R1.json'
with out.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'pins':len(pins),'errors':len(errors),'sha256':sha(out)}))
if errors: raise SystemExit(1)
