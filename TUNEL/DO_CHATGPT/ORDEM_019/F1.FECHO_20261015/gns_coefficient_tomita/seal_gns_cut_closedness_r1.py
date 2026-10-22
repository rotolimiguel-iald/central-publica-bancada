"""Custody for actual full-weight GNS cuts and closedness plus generic right-action helpers."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
NAMES=['GenericCountableCutsR1','GenericFiniteStarRightR1','GenericPolarRightCommutationR2','CanonicalFockGNSCutsR2','CanonicalFockGNSClosednessR5']
ALLOWED={'propext','Classical.choice','Quot.sound'}
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==b
assert not (BASE/'GNS_CUT_CLOSEDNESS_RECEIPT_R1.json').exists()
records=[];deps={};decl={};printed={};failures=[]
for name in NAMES:
 src=BASE/(name+'.lean');sp=pin(src)
 assert not re.search(r'\b(sorry|admit)\b',src.read_text(encoding='utf8'))
 matches=[]
 for rp in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
  r=json.loads(rp.read_bytes())
  if Path(r['source']['path']).stem!=name:continue
  if type(r['exit_code']) is not int or r['exit_code']!=0:failures.append(pin(rp));continue
  if r['source']['sha256']==sp['sha256']:matches.append((rp,r))
 assert matches,name
 rp,r=matches[-1];assert r['readonly_dependencies_unchanged']
 assert pin(r['source']['path'])==r['source']
 for d in r['dependencies']:
  if d['path'] not in deps:assert pin(d['path'])==d;deps[d['path']]=d
  else:assert deps[d['path']]==d
 log=(rp.parent/'AXIOMS.txt').read_text(encoding='utf8')
 assert 'sorryAx' not in log and 'error:' not in log
 for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",log,re.S):
  ax=[x.strip() for x in a.split(',') if x.strip()];assert set(ax)<=ALLOWED;printed[n]=ax
 for line in log.splitlines():
  if line.startswith('LOCAL_DECL\t'):
   _,n,a=line.split('\t',2);ax=[x.strip() for x in a.split(',') if x.strip()];assert set(ax)<=ALLOWED
   assert n not in decl;decl[n]=ax
 for d in r['artifacts']:assert pin(d['path'])==d
 records.append(dict(source=sp,receipt=pin(rp),build=pin(rp.parent/'BUILD.log'),axioms=pin(rp.parent/'AXIOMS.txt'),olean=pin(rp.parent/(name+'.olean')),start_utc=r['start_utc'],end_utc=r['end_utc'],seconds=r['seconds'],exit_code=0))
assert len(printed)==14
# Earlier failed revisions are retained, too, rather than hidden by final names.
for rp in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
 r=json.loads(rp.read_bytes())
 if r['exit_code']!=0 and any(Path(r['source']['path']).stem.startswith(prefix) for prefix in ('GenericCountableCuts','GenericFiniteStarRight','GenericPolarRightCommutation','CanonicalFockGNSCuts','CanonicalFockGNSClosedness')) and pin(rp) not in failures:failures.append(pin(rp))
result=dict(unit='F1.FECHO_20261015',claim=845,actor='codex-gerente-tgl/root',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING',records=records,checked_dependencies=list(deps.values()),printed_declarations=printed,all_local_declarations=decl,all_local_decl_count=len(decl),axioms_only_trio=True,source_has_no_sorry=True,failed_attempts_preserved=failures,conclusions=[
 'Countably many finite-interval cuts identify the full dual-weight GNS vector.',
 'Finite scalar square weight is equivalent to L2 integrability of its existing dual orbit.',
 'The actual GNS inscription is closed under simultaneous bounded strong operator convergence and GNS norm convergence.',
 'A genuine finite-star right product remains in the finite-star domain, with its adjoint identified.',
 'Given a dense GNS map and its actual left action, a proved polar right identity commutes with the left representation.'
],scope_limits=[
 'Baseline is v393; historic V350/V351 modules are reused from that baseline.',
 'The convergence theorem requires both stated convergences; strong operator convergence alone is insufficient.',
 'The generic polar-right commutation lemma retains J, dense range and left-action premises until a concrete consumer.',
 'No trace, additivity of the inverse supremum, traciality or semifinitude is asserted.',
 'The printed declarations are checked here. This receipt is not an environment-wide declaration audit or independent rebuild.',
 'No production modification, whole main execution or gate change is claimed.'
],builders=[pin(BASE/'build_coefficient_stream_r4.py')],provenance=[pin(BASE/'GENERAL_CUTOFF_FORMS_REUSE_R1.json'),pin(BASE.parent/'PROVENIENCIA_V393_REUSO_V351_R1.json')],sealer=pin(__file__),production_modified=False,gate_modified=False)
save(BASE/'GNS_CUT_CLOSEDNESS_RECEIPT_R1.json',result)
print(json.dumps(dict(receipt=pin(BASE/'GNS_CUT_CLOSEDNESS_RECEIPT_R1.json'),modules=len(records),local_declarations=len(decl),printed=len(printed),dependencies=len(deps))))
