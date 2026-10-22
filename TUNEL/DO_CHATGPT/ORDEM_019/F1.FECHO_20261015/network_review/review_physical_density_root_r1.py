"""Independent source and custody review of the actual weak stress consumer."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'maxwell_global/FINAL_MAXWELL_PHYSICAL_DENSITY_RECEIPT_R1.json'
TARGET=BASE/'MAXWELL_PHYSICAL_DENSITY_ROOT_REVIEW_R1.json'
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
assert len(printed)==20
out=dict(unit='F1.FECHO_20261015',claim=845,reviewer='/root',
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 verdict='PASS_WITH_STATED_SCOPE',mode='independent_semantic_source_and_custody_review_no_rebuild',
 source_receipt=pin(SOURCE),checked_files=list(pins.values()),checked_file_count=len(pins),
 printed_count=len(printed),material_findings=[],conclusions=[
 'Compact smooth momentum profiles are dense for the actual locally finite orbital measure; their energy moments imply strong regularity. Continuity and totality of exponential vectors transfer this to the unchanged coherent Fock domain.',
 'Smooth transverse cutoffs converge in L2 by dominated convergence. The exceptional gauge axis is proved null for the existing measure, rather than silently deleted.',
 'The explicit antisymmetric inverse tensor uses components 01 and 23 of the actual p-wedge-screen coefficient and is smooth when the profile vanishes near the gauge axis.',
 'A compact smooth four-dimensional extension is constructed with a time bump equal to one on the compact shell-energy image. Smoothness of the shell energy at the cone vertex is not assumed.',
 'Surjectivity of the physical Fourier transform and the explicit tensor inverse put each axis-avoiding compact smooth profile in the actual physical smearing range, which proves dense range.'
 ],scope_limits=[
 'The auxiliary gauge-chart class is not asserted invariant under every Lorentz transformation.',
 'DenseRange is global on complex Schwartz tests. Wedge density, real localization, locality and the integrated charge identity require their own consumers.',
 'No independent recompilation, production change or gate change.'
 ],review_script=pin(__file__))
b=(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf8')
with TARGET.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
assert TARGET.read_bytes()==b
print(json.dumps(dict(receipt=pin(TARGET),files=len(pins),prints=len(printed))))
