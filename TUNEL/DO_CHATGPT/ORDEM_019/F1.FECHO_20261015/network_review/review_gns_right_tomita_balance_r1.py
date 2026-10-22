"""Independent source/receipt review; no compilation or production mutation."""
from pathlib import Path
import datetime, hashlib, json, os, re
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'gns_coefficient_tomita'/'GNS_RIGHT_TOMITA_REPRESENTED_BALANCE_RECEIPT_R1.json'
TARGET=BASE/'GNS_RIGHT_TOMITA_REPRESENTED_BALANCE_SEMANTIC_REVIEW_R1.json'
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
assert not TARGET.exists()
data=json.loads(SOURCE.read_bytes());pins={}
def walk(v):
 if isinstance(v,dict):
  if 'path' in v and 'sha256' in v:
   actual=pin(v['path']);assert actual['sha256']==v['sha256']
   if 'bytes' in v:assert actual['bytes']==v['bytes']
   if actual['path'] in pins:assert pins[actual['path']]==actual
   pins[actual['path']]=actual
  for w in v.values():walk(w)
 elif isinstance(v,list):
  for w in v:walk(w)
walk(data)
printed={};local={};allowed={'propext','Classical.choice','Quot.sound'}
for r in data['records']:
 receipt=json.loads(Path(r['receipt']['path']).read_bytes())
 assert type(receipt['exit_code']) is int and receipt['exit_code']==0
 assert receipt['readonly_dependencies_unchanged'] is True
 walk(receipt)
 text=Path(r['source']['path']).read_text(encoding='utf8')
 assert not re.search(r'\b(sorry|admit)\b',text)
 log=Path(r['axioms']['path']).read_text(encoding='utf8')
 assert 'sorryAx' not in log and 'error:' not in log
 for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",log,re.S):
  ax=[s.strip() for s in a.split(',') if s.strip()];assert set(ax)<=allowed;printed[n]=ax
 for line in log.splitlines():
  if line.startswith('LOCAL_DECL\t'):
   _,n,a=line.split('\t',2);ax=[s.strip() for s in a.split(',') if s.strip()]
   assert n not in local and set(ax)<=allowed;local[n]=ax
assert printed==data['printed_declarations'] and local==data['all_local_declarations']
out=dict(unit='F1.FECHO_20261015',claim=845,reviewer='/root/tempo_math_review',
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 verdict='PASS_WITH_STATED_SCOPE',mode='independent_semantic_source_and_custody_review_no_rebuild',
 source_receipt=pin(SOURCE),checked_files=list(pins.values()),checked_file_count=len(pins),
 printed_count=len(printed),local_decl_count=len(local),material_findings=[],
 conclusions=[
 'The actual regular right product stays in the full finite-star core, and its star is left multiplication by the adjoint regular unitary. Continuity transfers this identity to the same closed Tomita graph.',
 'The generic GNS representation inherits positivity from the concrete dual-orbit representation. Uniformly bounded strong convergence is transported on the actual invariant GNS subspace, with no normality axiom added.',
 'The concrete Fock order consumer instantiates the existing weightContext; it does not change the algebra, vector or Hilbert completion.',
 'The represented regular resolvent derives the damped phase identity by CFC functoriality, and derives commutation from the sine-window approximants plus explicitly required bounded-strong continuity.',
 'The polar modular balance is a conditional generic lemma: polar resolvent flip, left/right phase identities and actual modular implementation remain explicit premises. Antiunitarity changes the phase sign, and the conclusion is a bounded operator balance, not a trace.',
 'The final norm-order lemma compares squared norms of adjoint images from B B* <= C C* by the Hilbert quadratic form.'
 ],scope_limits=[
 'No trace additivity, traciality, semifiniteness or completion of the actual polar identification is asserted by this batch.',
 'Generic premises in represented_resolvent_commutes and balance remain obligations of their concrete consumers.',
 'The review independently checked six source files, recorded logs and hashes, without a new Lean build, whole rite, production or gate action.'
 ],review_script=pin(__file__))
b=(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf8')
with TARGET.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
assert TARGET.read_bytes()==b
print(json.dumps(dict(receipt=pin(TARGET),verdict=out['verdict'],files=len(pins),prints=len(printed),local=len(local))))
