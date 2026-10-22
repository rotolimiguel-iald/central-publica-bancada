"""Freeze all R2 numerical code and execution wrapper before the one run."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parent
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,obj):
    with Path(p).open('xb') as f:f.write((json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
p=json.loads((ROOT/'PRE_REGISTRO_R69.json').read_text(encoding='utf8'))
p.update({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'version':'R2_ADDITIVE_NUMERICAL_GUARDS','previous_preregistration':pin(ROOT/'PRE_REGISTRO_R69.json'),'previous_result':pin(ROOT/'RESULT_R69.json'),'adversarial_evidence':pin(ROOT.parent/'AUDIT_NUMERICAL_RANGE_R69.json'),'additional_controls':['finite gains overflow product: refuse','finite gains underflow product: refuse','finite ratio overflow/underflow and subnormal denominator: refuse','C=1e200I retains residual one','transport/decoder/difference overflow: refuse','large finite residual computed safely'],'expected_check_count':50})
p['source_pins'].append(pin(ROOT.parent/'AUDIT_NUMERICAL_RANGE_R69.json'))
new(ROOT/'PRE_REGISTRO_R69_R2.json',p)
names=('PRE_REGISTRO_R69_R2.json','bridge_r69_r2.py','test_r69_r2.py','execute_r69_r2.py','prepare_r2.py','freeze_r69_r2.py','ERRATA_NUMERICA_R69_R2.md')
new(ROOT/'FREEZE_R69_R2.json',{'status':'FROZEN_BEFORE_SYNTHETIC_EXECUTION','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[pin(ROOT/n) for n in names]})
print(json.dumps(pin(ROOT/'FREEZE_R69_R2.json')))
