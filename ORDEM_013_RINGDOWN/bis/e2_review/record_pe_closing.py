"""Hash current sources and finite-test artifacts; no scientific execution."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json
HERE=Path(__file__).resolve().parent;B=HERE.parents[1]
owned=('pe_runner.py','pseob_source.py','registration_guard.py','run_controlled.py','strain_io.py','blinding.py')
new=('test_temporal_remnant.py','TEMPORAL_REMNANT_SCALAR_TEST.json','test_closing_contracts.py','CLOSING_CONTRACTS.json','PE_CLOSING_ADENDO.md','record_pe_closing.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[B/'bis/e2_code'/s for s in owned]+[B/'bis/e2_code/remnant_conversion.py',B/'bis/E2_REMNANT_BRIDGE_INPUT.json']
for p in sources:
    if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8-sig'))
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'DRAFT_SOURCE_STABLE_FOR_INDEPENDENT_REVIEW_NOT_REGISTRATION',
 'source_sha256':{str(p.relative_to(B)):sha(p) for p in sources},
 'new_files_sha256':{str((HERE/n).relative_to(B)):sha(HERE/n) for n in new},
 'files_modified_this_complement':['bis/e2_code/'+s for s in owned[:3]],
 'files_created_this_complement':['bis/e2_review/'+s for s in new+('PE_CLOSING_RECEIPT.json',)],
 'limits':'No PE, strain or waveform execution. Scalar and mock tests only. Remnant module main-owned, read-only.'}
path=HERE/'PE_CLOSING_RECEIPT.json'
with path.open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'receipt_sha256':sha(path),**receipt},indent=2))
