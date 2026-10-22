from pathlib import Path
import hashlib,json,datetime
b=Path(__file__).resolve().parent
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
d=json.loads((b/'WEDGE_CYCLIC_SURVEY_R1.json').read_bytes())
d['predecessor']=pin(b/'WEDGE_CYCLIC_SURVEY_R1.json')
d['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=b.parent/'wedge_exponential/RealSubspaceTotalityR5.lean';lines=p.read_text(encoding='utf8').splitlines()
d['sources'][0]=dict(**pin(p),anchors=[dict(needle=n,lines=[i+1 for i,s in enumerate(lines) if n in s]) for n in ['standard_exponential_total','standard_complex_span_dense']])
d['accepted_totality_receipt']=pin(b.parent/'wedge_exponential/FINAL_WEDGE_EXPONENTIAL_RECEIPT_R1.json')
d['correction']='Source R4 was interrupted before a result; accepted route is R5 consuming generic StandardComplexSpanR1. Proof statement preserved.'
with (b/'WEDGE_CYCLIC_SURVEY_R2.json').open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2)
s=(b/'custody_cyclic.py').read_text(encoding='utf8').replace('WEDGE_CYCLIC_SURVEY_R1.json','WEDGE_CYCLIC_SURVEY_R2.json')
with (b/'custody_cyclic_r2.py').open('x',encoding='utf8',newline='\n') as f:f.write(s)
print(pin(b/'WEDGE_CYCLIC_SURVEY_R2.json'))
