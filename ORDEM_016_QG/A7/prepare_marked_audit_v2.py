"""Preserve the 0**0 library error; correct only zero-power monomial assembly."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
source=HERE/'marked_polynomial_audit.py';target=HERE/'marked_polynomial_audit_v2.py'
raw=source.read_text('utf-8')
old='for i in range(4):term*=comb(alpha[i],even[i])*(-shift[i])**(alpha[i]-even[i])'
new='''for i in range(4):
            exponent=alpha[i]-even[i]
            term*=comb(alpha[i],even[i])
            if exponent:term*=(-shift[i])**exponent'''
assert raw.count(old)==1
raw=raw.replace(old,new).replace("DEST=HERE/'marked_polynomial_audit'","DEST=HERE/'marked_polynomial_audit_v2'")
assert not target.exists()
encoded=raw.encode();tmp=target.with_name(target.name+'.tmp')
with tmp.open('xb') as f:f.write(encoded)
assert tmp.read_bytes()==encoded;tmp.replace(target)
print(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),
    predecessor_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    target_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
    diagnostic='Sparse ring rejects 0**0; skip factors with exponent zero (polynomial unit)',
    mathematical_rules_changed=False)))
