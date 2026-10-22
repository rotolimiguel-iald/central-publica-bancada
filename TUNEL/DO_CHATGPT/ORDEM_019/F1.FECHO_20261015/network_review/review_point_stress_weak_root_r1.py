"""Independent source and custody review of the actual weak stress consumer."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'maxwell_global/FINAL_POINT_STRESS_WEAK_RECEIPT_R1.json'
TARGET=BASE/'POINT_STRESS_WEAK_ROOT_REVIEW_R1.json'
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
assert not TARGET.exists()
data=json.loads(SOURCE.read_bytes());pins={}
def walk(v):
 if isinstance(v,dict):
  if 'path' in v and 'sha256' in v:
   actual=pin(v['path']);assert actual['sha256']==v['sha256']
   if 'bytes' in v:assert actual['bytes']==v['bytes']
   pins[actual['path']]=actual
  for w in v.values():walk(w)
 elif isinstance(v,list):
  for w in v:walk(w)
walk(data)
printed={};allowed={'propext','Classical.choice','Quot.sound'}
for r in data['modules']:
 attempt=Path(r['attempt']);receipt=json.loads((attempt/'RECEIPT.json').read_bytes())
 assert receipt['exit_code']==0 and receipt['readonly_dependencies_unchanged'];walk(receipt)
 s=Path(r['source']['path']).read_text(encoding='utf8')
 assert not re.search(r'\b(sorry|admit)\b',s)
 log=(attempt/'AXIOMS.txt').read_text(encoding='utf8')
 assert 'sorryAx' not in log and 'error:' not in log
 for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",log,re.S):
  ax=[x.strip() for x in a.split(',') if x.strip()];assert set(ax)<=allowed;printed[n]=ax
assert len(printed)==10
out=dict(unit='F1.FECHO_20261015',claim=845,reviewer='/root',
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 verdict='PASS_WITH_STATED_SCOPE',mode='independent_semantic_source_and_custody_review_no_rebuild',
 source_receipt=pin(SOURCE),checked_files=list(pins.values()),checked_file_count=len(pins),
 printed_count=len(printed),material_findings=[],conclusions=[
 'The physical smearing-wave pairing is an inner-product identity on the same H1, retaining the tensor factor 1/2 and the chosen angular Fourier convention.',
 'Fock translation covariance uses the existing unitary and unique finite coherent coefficients; it does not infer Lorentz covariance.',
 'The energy moments supply an integrable majorant for coordinate derivatives. Continuity and differentiated finite coherent sums are proved on the regular domain.',
 'Weak conservation follows from the actual pointwise conservation and integration by parts against compact smooth tests on four-dimensional Lebesgue spacetime.'
 ],scope_limits=[
 'This is a sesquilinear form on the specified coherent domain. No closed stress operator or self-adjoint realization is established by this batch.',
 'The integral charge identity, full Lorentz tensor covariance and extension to larger domains remain separate obligations.',
 'No independent recompilation, production change or gate change.'
 ],review_script=pin(__file__))
b=(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf8')
with TARGET.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
assert TARGET.read_bytes()==b
print(json.dumps(dict(receipt=pin(TARGET),files=len(pins),prints=len(printed))))
