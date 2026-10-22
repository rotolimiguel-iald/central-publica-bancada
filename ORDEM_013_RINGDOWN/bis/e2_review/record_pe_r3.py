"""Document source pins only; no execution of science modules."""
from pathlib import Path
import hashlib,json,ast
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;CODE=HERE.parent/'e2_code'
names=('pe_runner.py','registration_guard.py','pseob_source.py','run_controlled.py','strain_io.py','blinding.py','temporal_contract.py')
written=('test_likelihood_counter.py','LIKELIHOOD_COUNTER_FINITE.json','test_shared_temporal.py','SHARED_TEMPORAL_REPLAY.json','PE_R3_ADENDO.md','record_pe_r3.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in names:ast.parse((CODE/name).read_text(encoding='utf-8-sig'))
out=dict(created_utc=datetime.now(timezone.utc).isoformat(),status='READY_FOR_B_INDEPENDENT_REVIEW_NOT_REGISTRATION',
  source_sha256={name:sha(CODE/name) for name in names},
  files_written={name:sha(HERE/name) for name in written},
  receipt_itself='PE_R3_RECEIPT.json',modified_sources=list(names[:3]),
  untouched_main_helper='temporal_contract.py')
with (HERE/'PE_R3_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
