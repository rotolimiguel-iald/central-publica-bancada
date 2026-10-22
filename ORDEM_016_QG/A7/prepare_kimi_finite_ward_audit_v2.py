from pathlib import Path
import hashlib, json
H=Path(__file__).resolve().parent
p=H/'audit_kimi_finite_ward.py'
q=H/'audit_kimi_finite_ward_v2.py'
text=p.read_text(encoding='utf-8')
old='4*(n-1)*residue(n+1,tuple(int(j==i) for j in range(4)),(1,1,1,1)))'
new='s.cancel(4*(n-1)*rnext*Q[i]/q2))'
assert text.count(old)==1
text=text.replace(old,new).replace("D = H/'kimi_finite_ward_audit'",
 "D = H/'kimi_finite_ward_audit_v2'\nD.mkdir(exist_ok=True)\nSOURCE = H/'kimi_finite_ward_audit'")
text=text.replace("D/'ANSWER.md',D/'provided_check.py'","SOURCE/'ANSWER.md',SOURCE/'provided_check.py'")
assert not q.exists()
q.write_bytes(text.encode())
print(json.dumps(dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
 corrected_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),
 correction='Expected derivative commutator uses q_i times scalar residue/q2, not x_i residue')))
