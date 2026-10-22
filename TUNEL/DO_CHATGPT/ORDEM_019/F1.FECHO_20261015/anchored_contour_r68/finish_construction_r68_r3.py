"""Custody only; no administrative acceptance or canonical changes."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
def pin(p):
 p=Path(p);raw=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
attempts=sorted((B/'attempts').glob('*/RECEIPT.json'))
assert attempts, 'No build receipt'
receipts=[json.loads(p.read_text(encoding='utf-8')) for p in attempts]
good=[(p,r) for p,r in zip(attempts,receipts) if r['passed']]
assert good, 'No passed build'
p,r=good[-1]
assert len(r['axioms'])==22, 'R3 requires 22 checked declarations'
assert 'TGLExt.AnchoredNameContourR68.exact_correspondence_iff' in r['axioms']
for s in json.loads((B/'SOURCE_PINS_R68.json').read_text(encoding='utf-8')):
 assert pin(s['path'])['sha256']==s['sha256'],s['path']
for key in ('source','compiled_source','olean','stdout','stderr','build_log'):
 assert pin(r[key]['path'])['sha256']==r[key]['sha256'],key
result={'status':'CANDIDATE_COMPILED_NOT_APPROVED','previous_construction':pin(B/'CONSTRUCTION_R68.json'),'unit':'F1.FECHO_20261015','requirement':'R12_CONTORNO','claim':960,
 'constructor':'r68_anchor_construction','source':r['source'],'receipt':pin(p),'olean':r['olean'],
 'axiom_prints':r['axioms'],'declaration_count':len(r['axioms']),'all_attempts':[pin(p) for p in attempts],
 'source_pins':pin(B/'SOURCE_PINS_R68.json'),'operator_source':pin(B/'ORIGEM_R68.txt'),'build_runner':pin(B/'build_r68.py'),
 'limits':['Vector flow, not a CPTP density-matrix channel.','Limit is P x, not universal a.',
 'Exact vector equality is phase-sensitive; a and -a have the same projector and quadratic reading.',
 'No historical or theological uniqueness theorem; no empirical beta discriminator.',
 'Generator block identities do not by themselves assert a full-spectrum theorem.',
 'R3 checks zero complementary residual on the input before dissipation; projection alone may hide a nonzero kernel component.',
 'Reference-to-projection uniqueness already exists in Verdade.the_projection_is_forced_by_its_truth (913-915), not reconstructed here.',
 'Independent review and administrative acceptance are separate and not performed by this script.']}
with (B/'CONSTRUCTION_R68_R3.json').open('xb') as f:f.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'receipt':pin(B/'CONSTRUCTION_R68_R3.json'),'declarations':len(r['axioms']),'attempts':len(attempts)},ensure_ascii=False))
