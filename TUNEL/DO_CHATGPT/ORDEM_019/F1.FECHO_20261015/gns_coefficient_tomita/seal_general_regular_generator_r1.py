"""Custody for reuse of positive-generator proofs already embedded in current v393."""
from pathlib import Path
import datetime,hashlib,json,os,re
BASE=Path(__file__).resolve().parent
NAMES=['GeneralRegularPositiveGraphR2', 'GeneralRegularAbsorptionR1', 'GeneralRegularImaginaryPowersR1', 'GeneralRegularSpectralGraphR2', 'GeneralRegularAffiliationR1', 'GeneralRegularDualScalingR2', 'GeneralRegularInverseCutoffR1', 'GeneralDampedPhaseBalanceR1', 'GeneralRegularGeneratorAuditR1']
ALLOWED={'propext','Classical.choice','Quot.sound'}
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==b
assert not (BASE/'GENERAL_REGULAR_GENERATOR_RECEIPT_R1.json').exists()
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
 if r['exit_code']!=0 and any(Path(r['source']['path']).stem.startswith(prefix) for prefix in ('GeneralRegular','GeneralDamped')) and pin(rp) not in failures:failures.append(pin(rp))
result=dict(unit='F1.FECHO_20261015',claim=845,actor='codex-gerente-tgl/root',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING',records=records,checked_dependencies=list(deps.values()),printed_declarations=printed,all_local_declarations=decl,all_local_decl_count=len(decl),axioms_only_trio=True,source_has_no_sorry=True,failed_attempts_preserved=failures,conclusions=[
 'The existing v393 scalar resolvent proofs construct a positive self-adjoint zero-kernel generator for every strongly continuous UnitaryFlow H, using normalized Fourier and the actual coefficient boost.',
 'The same regular group is conjugate to translation. Its equality with the imaginary powers of the constructed generator is proved, rather than assumed.',
 'The resolvent belongs to the generated regular crossed-product algebra; every bounded commutant operator preserves the exact generator graph.',
 'The exact graph is exponential spectral multiplication. Its dual action transforms domain and values with the proved exp(s) graph law.',
 'The inverse-generator cutoffs are positive bounded members of the same core, solve the exact h+epsilon equation in both directions and have the derived regulator covariance.',
 'Three generic phase-balance proofs already embedded in v393 are exposed publicly in the sandbox; their phase and commutation premises remain explicit for the concrete GNS consumer.'
],scope_limits=[
 'V351 identifies the historical origin and filenames of the reused proofs, not the program version used as baseline. The current canonical program is v393.',
 'These generic proofs instantiate at the existing concrete Fock flow; no arbitrary equivalence with a SiteProfile tower is introduced.',
 'No semifinite trace, trace scaling, finite projection or half-splitting is asserted by this receipt.',
 'The GNS modular identification and the concrete cut-balance consumer must still supply their actual hypotheses.',
 'No production modification, whole main execution or gate change is claimed.'
],builders=[pin(BASE/'build_coefficient_stream_r4.py')],provenance=[pin(BASE/"GENERAL_REGULAR_POSITIVE_REUSE_R1.json"),pin(BASE/"GENERAL_DAMPED_PHASE_REUSE_R1.json"),pin(BASE.parent/"PROVENIENCIA_V393_REUSO_V351_R1.json")],sealer=pin(__file__),production_modified=False,gate_modified=False)
save(BASE/'GENERAL_REGULAR_GENERATOR_RECEIPT_R1.json',result)
print(json.dumps(dict(receipt=pin(BASE/'GENERAL_REGULAR_GENERATOR_RECEIPT_R1.json'),modules=len(records)-1,local_declarations=len(decl),printed=len(printed),dependencies=len(deps))))
