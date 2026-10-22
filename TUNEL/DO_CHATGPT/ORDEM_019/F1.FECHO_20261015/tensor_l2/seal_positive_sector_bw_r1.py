"""Seal exact accepted tensor-coordinate modules, never replacing prior evidence."""
from pathlib import Path
import hashlib,json,re,datetime
BASE=Path(__file__).resolve().parent
MODULES=['TensorResolventScalarsR4','CanonicalTensorResolventR2']
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
rows=[]
for m in MODULES:
    source=BASE/(m+'.lean')
    matches=[]
    for r in (BASE/'attempts').glob('*/RECEIPT.json'):
        d=json.loads(r.read_bytes())
        snap=r.parent/source.name
        if d['exit_code']==0 and snap.exists() and snap.read_bytes()==source.read_bytes():matches.append(r)
    if not matches:raise RuntimeError(('no accepted build',m))
    receipt=sorted(matches)[-1];data=json.loads(receipt.read_bytes());out=receipt.parent
    text=(out/'AXIOMS.txt').read_text(encoding='utf-8')
    declarations=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)
    assert declarations and all(set(x.strip() for x in a.split(','))<= {'propext','Classical.choice','Quot.sound'} for _,a in declarations)
    assert not re.search(r'\b(sorry|admit|axiom)\b',source.read_text(encoding='utf-8'))
    assert data['readonly_dependencies_unchanged']
    rows.append({'source':pin(source),'receipt':pin(receipt),'build':pin(out/'BUILD.log'),'axioms':pin(out/'AXIOMS.txt'),'olean':pin(out/(m+'.olean')),'seconds':data['seconds'],'exit_code':0,'declarations':[n for n,a in declarations],'axioms_only_trio':True})
failures=[]
for r in (BASE/'attempts').glob('*/RECEIPT.json'):
    d=json.loads(r.read_bytes())
    name=Path(d['source']['path']).stem
    if d['exit_code']!=0 and name.startswith(('TensorResolventScalars','CanonicalTensorResolvent')):failures.append(pin(r))
result={'unit':'F1.FECHO_20261015','claim':845,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REAL_COMPILED_SANDBOX_REVIEW_PENDING','scope':'Concrete equality of the actual Fock resolvent with the summed-rapidity sigmoid multiplier in every positive-particle sector, followed by equality of the actual modular imaginary-power flow and Gamma(B0(-2*pi*t)) in these same sectors. The vacuum component is a separate root-agent construction; no KMS statement is included here.','modules':rows,'failed_attempts':failures,'survey':pin(BASE/'TENSOR_SPECTRAL_SURVEY_R1.json'),'builder':pin(BASE/'build_tensor.py'),'sealer':pin(Path(__file__)),'production_modified':False}
p=BASE/'FINAL_POSITIVE_SECTOR_BW_RECEIPT_R1.json'
with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(pin(p)))
