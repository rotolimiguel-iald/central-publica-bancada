from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parent/'probes'
receipts=[]
for name in ['ProbePositiveEnergy','ProbeNonKMS']:
    old=root/(name+'.lean')
    new=root/(name+'_v2.lean')
    raw=old.read_bytes()
    text=raw.decode()
    assert text.count('by ext <;> simp')==1
    content=text.replace('by ext <;> simp','by apply Complex.ext <;> simp').encode()
    assert not new.exists()
    tmp=new.with_suffix('.lean.tmp')
    with tmp.open('xb') as f:f.write(content)
    assert tmp.read_bytes()==content
    tmp.rename(new)
    receipts.append({'source':str(old),'source_sha256':hashlib.sha256(raw).hexdigest(),
                     'variant':str(new),'variant_sha256':hashlib.sha256(content).hexdigest(),
                     'change':'Name Complex.ext explicitly; preserve all mathematical statements'})
out=root/'complex_ext_revisions.json'
assert not out.exists()
content=(json.dumps(receipts,indent=2)+'\n').encode()
tmp=out.with_suffix('.json.tmp')
with tmp.open('xb') as f:f.write(content)
assert tmp.read_bytes()==content
tmp.rename(out)
print(json.dumps(receipts))
