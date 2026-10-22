from pathlib import Path
import hashlib
import json

folder=Path(__file__).resolve().parent/'probes'
old=folder/'AnalyticBoundaryControl.lean'
new=folder/'AnalyticBoundaryControl_v2.lean'
raw=old.read_bytes()
text=raw.decode()
replacements=[
 ('(fun w hw => hM w (by simpa [hw] using hb.le) (by simpa [hw]))',
  '(fun w hw => hM w (by change w.re = b at hw; linarith) (by change w.re = b at hw; exact hw.le))'),
 ('zero_rpow (ne_of_gt he)', 'Real.zero_rpow (ne_of_gt he)'),
 ('simpa [mul_im] using hw','simpa [verticalStrip, mul_im] using hw')]
for a,b in replacements:
    assert text.count(a)==1,a
    text=text.replace(a,b)
assert not new.exists()
content=text.encode()
tmp=new.with_suffix('.lean.tmp')
with tmp.open('xb') as f:f.write(content)
assert tmp.read_bytes()==content
tmp.rename(new)
print(json.dumps({'supersedes':str(old),'old_sha256':hashlib.sha256(raw).hexdigest(),
                  'new':str(new),'new_sha256':hashlib.sha256(content).hexdigest()}))
