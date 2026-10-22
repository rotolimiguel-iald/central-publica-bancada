"""Custody for constructed Gaussian regularizers of the resolvent modular group."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
NAMES=['ResolventPhaseIntegralR2', 'ResolventScaledPhaseIntegralR1', 'GaussianLogScalarR4', 'GaussianProbabilityKernelR4', 'GaussianResolventSymbolR2', 'StrongUnitaryAverageR1', 'GroupAverageApproximationR2', 'GaussianResolventRegularizerR4', 'GaussianResolventAverageR5', 'GaussianRegularizationAuditR1']
ALLOWED={'propext','Classical.choice','Quot.sound'}
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==b
assert not (BASE/'GAUSSIAN_REGULARIZATION_RECEIPT_R1.json').exists()
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
 if r['exit_code']!=0 and any(Path(r['source']['path']).stem.startswith(prefix) for prefix in ('Gaussian','ResolventPhase','ResolventScaled','StrongUnitary','GroupAverage')) and pin(rp) not in failures:failures.append(pin(rp))
result=dict(unit='F1.FECHO_20261015',claim=845,actor='codex-gerente-tgl/root',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING',records=records,checked_dependencies=list(deps.values()),printed_declarations=printed,all_local_declarations=decl,all_local_decl_count=len(decl),axioms_only_trio=True,source_has_no_sorry=True,failed_attempts_preserved=failures,conclusions=[
 'The weighted phase integral commutes with continuous functional calculus on the actual positive contraction resolvent.',
 'A normalized real Gaussian kernel has integral one and Fourier multiplier exp(-s^2/4).',
 'The Gaussian logarithmic multiplier extends continuously to both spectral endpoints and factors through the resolvent.',
 'The real strong unitary Gaussian average equals this spectral multiplier on all H, proved first on the dense damped range.',
 'The averages at scale 1/(n+1) converge strongly to identity and have range in the exact resolvent square-root graph domain.',
 'Real group averages preserve invariant closed real graphs.'
],scope_limits=[
 'These operator theorems do not alone identify the actual weight GNS graph with the coefficient graph.',
 'The GNS consumer must independently supply graph inclusion, group invariance, and the concrete resolvent identification.',
 'No whole program execution, production write or gate change is claimed.'
],builders=[pin(BASE/'build_coefficient_stream_r4.py')],sealer=pin(__file__),production_modified=False,gate_modified=False)
save(BASE/'GAUSSIAN_REGULARIZATION_RECEIPT_R1.json',result)
print(json.dumps(dict(receipt=pin(BASE/'GAUSSIAN_REGULARIZATION_RECEIPT_R1.json'),modules=len(records)-1,local_declarations=len(decl),printed=len(printed),dependencies=len(deps))))
