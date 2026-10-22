from pathlib import Path
import hashlib,json,re,datetime
b=Path(__file__).resolve().parent
accepted=b/'attempts/002'
r=json.loads((accepted/'RECEIPT.json').read_text(encoding='utf-8'))
assert r['exit_code']==0
src=b/'OpticalPopulationBridgeR2.lean';raw=src.read_bytes();text=raw.decode('utf-8-sig')
assert hashlib.sha256(raw).hexdigest()==r['source_sha256']
assert not re.search(r'\bsorry\b',text)
log=(accepted/'BUILD.log').read_text(encoding='utf-8')
axioms={}
for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log):
 vals=[a.strip() for a in body.split(',') if a.strip()]
 assert set(vals)<= {'propext','Classical.choice','Quot.sound'}
 axioms[name]=vals
assert len(axioms)==15
files=[]
for p in sorted(b.rglob('*')):
 if p.is_file(): files.append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out={'unit':'F1.ATRATOR','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'accepted_source':str(src),'accepted_attempt':str(accepted),'build':r,'axioms':axioms,'theorems_checked':len(axioms),'sorry_tokens':0,'result':'PASSA','scope':'Exact finite population algebra and no-fixed-point affine control; scalar beta symbolic. Does not identify angular rotation with dissipation, or assert an empirical result.','failure_preserved':'attempts/001 failed for missing noncomputable on two real-division definitions; proofs already reported the trio; full old source/log/receipt retained.','artifacts':files}
with (b/'FINAL_OPTICAL_RECEIPT_R1.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'source':str(src),'source_sha256':r['source_sha256'],'receipt_sha256':hashlib.sha256((b/'FINAL_OPTICAL_RECEIPT_R1.json').read_bytes()).hexdigest(),'exit':r['exit_code'],'theorems':len(axioms)},ensure_ascii=False))
