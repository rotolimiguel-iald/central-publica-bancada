"""Existing reader controls and explicit canonical-name audit corrections."""
from pathlib import Path
import json
from prepare_part_d import write,save,sha,R
S=R/'FECHAMENTO_PARCIAL';L=S/'lean';rows=[]
p=L/'ContractGroupH_v3.lean';q=L/'ContractGroupH_v3_Integration_v2.lean'
text=p.read_text('utf-8').replace('TGLExt.ContratoQGv31.ContratoH3.response_covariant\n','TGLExt.ContratoQGv31.ContratoH3.response_covariant_v31\n')
assert text!=p.read_text('utf-8')
write(q,('// predecessor SHA256 '+sha(p)+'\n'+text).encode())
rows.append(dict(module=q.stem,item='C1',source=str(q),sha256=sha(q),expected_rc=0,supersedes='ContractGroupH_v3',
    reason='Canonical v371 renamed response_covariant to response_covariant_v31; no new proof'))
q=L/'CanonicalResponseCovarianceAudit.lean'
write(q,b'import TGLExt.ContratoQG_v31_Teoremas\n#print axioms TGLExt.ContratoQGv31.ContratoH3.response_covariant_v31\n')
rows.append(dict(module=q.stem,item='A1',source=str(q),sha256=sha(q),expected_rc=0,
    reason='Restores the 21st original WindowLemmas axiom query under its canonical renamed symbol'))
for name in ['ReaderRejectEmpty_v2','ReaderRejectToy_v2','ReaderRejectIndex_v2','RejectConditionalAsInhabitant']:
    p=R/'A8'/(name+'.lean');q=L/(name+'.lean');write(q,p.read_bytes())
    rows.append(dict(module=name,item='A8',source=str(q),sha256=sha(q),expected_rc=1,
        original=str(p),original_sha256=sha(p),
        expected_diagnostic='EXACT_TYPE_MISMATCH' if name.startswith('ReaderReject') else 'type mismatch'))
save(S/'SUPPLEMENTAL_PLAN.json',rows)
print(json.dumps(dict(supplemental=len(rows))))
