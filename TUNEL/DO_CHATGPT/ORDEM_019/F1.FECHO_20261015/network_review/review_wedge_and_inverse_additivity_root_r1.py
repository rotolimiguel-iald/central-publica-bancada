"""Custody checks after root source review; no independent recompilation."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
OUT=BASE.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
ALLOWED={'propext','Classical.choice','Quot.sound'}
JOBS=[('orbital_rotation/FINAL_PHYSICAL_WEDGE_EQUALITY_RECEIPT_R1.json', 'PHYSICAL_WEDGE_EQUALITY_ROOT_REVIEW_R1.json', ['Boundary uniqueness derives differentiability of the zero extension from within derivatives; actual positive-energy coefficients supply this regularity using finite energy moments.', 'The closed COMPLEX span, not the real localized space, becomes invariant under both null groups. Their sum gives spatial shifts; bounded supports are moved into the right wedge and pulled back in that complex span.', 'Real compact cutoffs converge in the full Schwartz topology with an explicit seminorm estimate, preserve reality and retain the original support as a subset.', 'Global density is supplied by the independently reviewed PhysicalSmearDensityR6. The Gaussian uniqueness criterion then yields equality of the physical real wedge with canonical KWR, without a density premise in the final theorem.', 'The adapter supplies actual isotony, translation covariance, longitudinal boost covariance and wedge_glue. The existing nonzero KWR vector supplies nonvacuum localization.'], ['No K_local theorem for arbitrary SpacelikeSep regions and no complete LightNetData inhabitant is asserted. No joint closure of both supports, hidden margin, or all-direction Lorentz covariance is inferred.']), ('takesaki_fock/GENERAL_INVERSE_ADDITIVITY_RECEIPT_R1.json', 'GENERAL_INVERSE_ADDITIVITY_ROOT_REVIEW_R1.json', ['Comparison on the finite-square ideal passes to every square by the existing regular averages and explicit vacuum-fixing and commutation premises.', 'Positive square-root membership in the same core then extends the comparison to every positive operator.', 'Additivity of the supremum consumes antitonicity of the cut weights and a common regulator min(e,d); it is not inferred from an arbitrary supremum.', 'Normality for internal directed positive suprema follows from the previously proved monotone operator limit and the von Neumann inclusion theorem.'], ['The concrete Fock antitonicity and finite-domain estimate remain consumers. No square traciality, semifiniteness or total cyclic ENNReal extension is inferred.'])]
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
