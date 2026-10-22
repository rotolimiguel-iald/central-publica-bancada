"""Custody checks after root source review; no independent recompilation."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
OUT=BASE.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
ALLOWED={'propext','Classical.choice','Quot.sound'}
JOBS=[
 ('takesaki_fock/GENERAL_FINITE_APPROXIMATION_POLAR_RECEIPT_R1.json','GENERAL_FINITE_APPROXIMATION_POLAR_ROOT_REVIEW_R1.json',[
 'The involutive antiunitary transport is generic; its specialization must match the concrete module instances.',
 'The cutoff square roots commute with regular translations and their interval averages by CFC and Bochner integration.',
 'Strong Fatou controls the same inverse supremum on squares; no traciality is inferred from lower semicontinuity.',
 'The finite star core reduction uses the explicit vacuum-fixed premise and proves two inequalities via sandwich approximation.',
 'Positive finite minorants are constructed only under the tracial square law and the actual finite-contraction approximate identity. The domain bound produces that approximate identity.',
 'The closed Tomita flip follows from its dense closed involution. The antiunitary flip additionally consumes the actual polar factorization and dense square-root range.'
 ],['Concrete finite-core traciality and domain-bound consumers remain outstanding. No trace additivity or full Takesaki identification is claimed.']),
 ('orbital_rotation/FINAL_MAXWELL_BOOST_UNIQUENESS_RECEIPT_R1.json','MAXWELL_BOOST_UNIQUENESS_ROOT_REVIEW_R1.json',[
 'The inverse Lorentz pullback and covariant test-tensor indices are used consistently; volume invariance supplies the physical Fourier covariance.',
 'The on-shell contraction is intertwined by the physical longitudinal boost almost everywhere on the same H1.',
 'The real localized wedge subspace is preserved by this boost, using the transformed physical test support.',
 'Gaussian regularizers prove equality with KWR only after complex density is supplied. This batch retains that premise explicitly.',
 'The generic real-subspace uniqueness argument uses closedness, bounded antilinear regularizers and dense complex span; it does not manufacture density.'
 ],['Longitudinal boost covariance is proved here. Full causal locality, all Lorentz directions, and complex localized density are separate obligations.'])]
for rel,target,conclusions,limits in JOBS:
 src=OUT/rel;dest=BASE/target;assert not dest.exists()
 d=json.loads(src.read_bytes());pins={}
 def walk(v):
  if isinstance(v,dict):
   if 'path' in v and 'sha256' in v:
    a=pin(v['path']);assert a['sha256']==v['sha256'],v['path']
    if 'bytes' in v:assert a['bytes']==v['bytes']
    if a['path'] in pins:assert pins[a['path']]==a
    pins[a['path']]=a
   for w in v.values():walk(w)
  elif isinstance(v,list):
   for w in v:walk(w)
 walk(d)
 printed={};local={};records=d.get('records',d.get('accepted',[]))
 for r in records:
  rr=json.loads(Path(r['receipt']['path']).read_bytes());assert rr['exit_code']==0
  assert rr['readonly_dependencies_unchanged'];walk(rr)
  text=Path(r['source']['path']).read_text(encoding='utf8')
  assert not re.search(r'\b(sorry|admit)\b',text)
  log=(Path(r['receipt']['path']).parent/'AXIOMS.txt').read_text(encoding='utf8')
  assert 'sorryAx' not in log and 'error:' not in log
  for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",log,re.S):
   aa=[x.strip() for x in a.split(',') if x.strip()];assert set(aa)<=ALLOWED;printed[n]=aa
  for line in log.splitlines():
   if line.startswith('LOCAL_DECL\t'):
    _,n,a=line.split('\t',2);aa=[x.strip() for x in a.split(',') if x.strip()]
    assert set(aa)<=ALLOWED;local[n]=aa
 if 'printed_declarations' in d:
  expected_printed=d['printed_declarations']
  assert (len(printed)==expected_printed if isinstance(expected_printed,int) else printed==expected_printed)
 if 'all_local_declarations' in d:
  expected=d['all_local_declarations']
  if isinstance(expected,list):expected={x['name']:x['axioms'] for x in expected}
  assert local==expected
 result=dict(unit='F1.FECHO_20261015',claim=845,reviewer='/root',
  created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  verdict='PASS_WITH_STATED_SCOPE',mode='independent_semantic_source_and_custody_review_no_rebuild',
  source_receipt=pin(src),checked_files=list(pins.values()),checked_file_count=len(pins),
  printed_count=len(printed),local_decl_count=len(local),material_findings=[],
  conclusions=conclusions,scope_limits=limits+['No independent recompilation, production change, or gate change.'],
  review_script=pin(__file__))
 b=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 with dest.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert dest.read_bytes()==b
 print(json.dumps(dict(receipt=pin(dest),files=len(pins),prints=len(printed),locals=len(local))))
