"""Custody for exact coefficient modular calculus, without a GNS equality claim."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
NAMES=['FibreModularCalculusR2','CoefficientConjugationR2','CoefficientBoostR1','CoefficientTwistedConjugationR1','CoefficientTomitaSquareR2','FibreRootGraphR3','CoefficientFockConjugationR2','ResolventRootIdentificationR2','FibreRootPointwiseR1','RealLpGraphCoreR3','LpClosedSubspaceCoreR3','CoefficientFockPointwiseR1','CoefficientPointwiseR1','CoefficientTomitaAuditR1']
ALLOWED={'propext','Classical.choice','Quot.sound'}
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==b
assert not (BASE/'COEFFICIENT_TOMITA_RECEIPT_R1.json').exists()
records=[];deps={};decl={};printed={};failures=[]
for name in NAMES:
 src=BASE/(name+'.lean');sp=pin(src)
 assert not re.search(r'\b(sorry|admit)\b',src.read_text(encoding='utf8'))
 matches=[]
 for rp in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
  r=json.loads(rp.read_bytes())
  if Path(r['source']['path']).stem!=name:continue
  if r['exit_code']!=0:failures.append(pin(rp));continue
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
assert decl and printed
# Earlier failed revisions are retained, too, rather than hidden by final names.
for rp in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
 r=json.loads(rp.read_bytes())
 if r['exit_code']!=0 and pin(rp) not in failures:failures.append(pin(rp))
result=dict(unit='F1.FECHO_20261015',claim=845,actor='codex-gerente-tgl/root',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING',records=records,checked_dependencies=list(deps.values()),printed_declarations=printed,all_local_declarations=decl,all_local_decl_count=len(decl),axioms_only_trio=True,source_has_no_sorry=True,failed_attempts_preserved=failures,conclusions=[
 'The fibre representation intertwines continuous functional calculus, resolvent square roots and imaginary powers, including exact operator domains.',
 'The coefficient antiunitary is reflection followed by the actual Fock J and the coefficient boost. Its involution and the square graph identity are proved.',
 'A positive selfadjoint operator equals the resolvent square root of its square resolvent by graph core and maximal adjoint arguments.',
 'The actual Fock coefficient Tomita graph has an exact AE characterization: (f(-a),B_-a g(a)) belongs to the existing actual Weyl/vacuum Tomita graph almost everywhere.',
 'Real Hilbert L2 interval totality and closed-subspace graph core helpers are proved without an extra ambient separability assumption.'
],scope_limits=[
 'The coefficient operator is not yet identified with the GNS Tomita of the same regular-core weight by this receipt.',
 'The concrete transport of interval graph generators, reverse GNS inclusion, scaled trace and PF are subsequent obligations.',
 'No whole program execution, production write or gate change is claimed.'
],builders=[pin(BASE/'build_coefficient_r2.py'),pin(BASE/'build_coefficient_stream_r3.py')],sealer=pin(__file__),production_modified=False,gate_modified=False)
save(BASE/'COEFFICIENT_TOMITA_RECEIPT_R1.json',result)
print(json.dumps(dict(receipt=pin(BASE/'COEFFICIENT_TOMITA_RECEIPT_R1.json'),modules=len(records)-1,local_declarations=len(decl),printed=len(printed),dependencies=len(deps))))
