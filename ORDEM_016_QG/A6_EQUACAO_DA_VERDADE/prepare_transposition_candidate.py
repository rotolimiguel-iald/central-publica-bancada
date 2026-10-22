"""Mechanical consolidation proposal. Does not modify originals or claim prefix compliance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re
HERE=Path(__file__).resolve().parent
DEST=HERE/'E_ficha/candidate'
DEST.mkdir(parents=True,exist_ok=True)
sources=[
 'B_fechamentos/TheEquationOfTruth_T20_v3.lean',
 'B_fechamentos/InscriptionBridge.lean',
 'B_fechamentos/PenaltyThreeLocksBridge_v2.lean',
 'B_fechamentos/OperatorContourBridge_v2.lean',
 'B_fechamentos/QubitScalarEntropy.lean',
 'B_fechamentos/QubitEntropyDerivative_v3.lean',
 'B_fechamentos/IdempotentDephasing_v2.lean',
 'B_fechamentos/FiniteGapRate_v2.lean',
 'B_fechamentos/InfiniteLimitUniformControl_v2.lean',
 'B_fechamentos/ModularGeneratorControl.lean',
 'C_controles/TheEquationOfTruth_T20_controles_v3.lean',
 'C_controles/NegativeControlsCompleteness_v2.lean']
local_modules={Path(s).stem for s in sources}|{'TheEquationOfTruth_T20'}
def sha(b): return hashlib.sha256(b).hexdigest()
imports=[];blocks=[];records=[]
for relative in sources:
    path=HERE/relative;raw=path.read_bytes();text=raw.decode('utf-8')
    header=[];body=[]
    for line in text.splitlines(keepends=True):
        match=re.fullmatch(r'import ([\w.]+)\s*',line)
        if match:
            name=match.group(1);header.append(name)
            if name not in local_modules and name not in imports: imports.append(name)
        else: body.append(line)
    body=''.join(body).encode('utf-8')
    records.append(dict(path=str(path),source_sha256=sha(raw),removed_imports=header,
                        retained_body_sha256=sha(body),retained_body_bytes=len(body)))
    blocks.append(b'\n/- Source body: '+relative.encode()+b'; imports relocated only. -/\n'+body)
raw=('\n'.join('import '+n for n in imports)+'\n').encode()+b''.join(blocks)
path=DEST/'TheEquationOfTruth_IntegrationCandidate.lean'
assert not path.exists()
path.write_bytes(raw)
original=(HERE/'A_reproducao/TheEquationOfTruth.lean').read_bytes()
assert not raw.startswith(original)
manifest=dict(status='PROPOSAL_NOT_YET_COMPILED',at=datetime.now(timezone.utc).isoformat(),
 sources=records,external_imports=imports,candidate=str(path),candidate_sha256=sha(raw),
 source_bodies_preserved_except_import_relocation=True,original_prefix_preserved=False,
 original_reference_sha256=sha(original),original_reference_bytes=len(original),
 required_decision='Management must accept relocated imports for this separate monolithic proposal; strict B prefix acceptance remains MEDIDA.',
 canonical_written=False,gate_changed=False)
p=DEST/'construction_manifest.json';assert not p.exists();p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(candidate=str(path),bytes=len(raw),source_count=len(records),imports=imports)))
