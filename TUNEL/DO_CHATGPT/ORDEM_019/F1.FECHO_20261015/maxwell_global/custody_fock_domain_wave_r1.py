"""Custody of actual regular photon domain, moment transport, and differentiated Maxwell waves."""
from pathlib import Path
import datetime,hashlib,json,re,os,sys
BASE=Path(__file__).resolve().parent
OUT=BASE.parent
NAMES=sys.argv[1:]
if not NAMES: raise SystemExit("explicit final module names required")
def pin(p):
 b=p.read_bytes();return {"path":str(p),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
mods=[]
for name in NAMES:
 src=BASE/(name+'.lean');b=src.read_bytes();txt=b.decode('utf-8')
 code=re.sub(r'/\-.*?\-/','',txt,flags=re.S); code=re.sub(r'--[^\n]*','',code)
 if re.search(r'\b(sorry|admit|axiom)\b',code):raise RuntimeError("unproved token "+name)
 hits=[]
 for r in (OUT/'kms_strip'/'attempts').glob('*/RECEIPT.json'):
  j=json.loads(r.read_text(encoding='utf-8'))
  if Path(j['source']['path']).stem==name and j['exit_code']==0 and j['source']['sha256']==hashlib.sha256(b).hexdigest():hits.append((r,j))
 if len(hits)!=1:raise RuntimeError((name,len(hits)))
 r,j=hits[0];a=r.parent;ax=(a/'AXIOMS.txt').read_text(encoding='utf-8')
 if 'sorryAx' in ax:raise RuntimeError('sorryAx')
 decl=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",ax)
 if not decl:raise RuntimeError('missing axioms')
 for n,axs in decl:
  if set(v.strip() for v in axs.split(',') if v.strip())-{'propext','Classical.choice','Quot.sound'}:raise RuntimeError(n)
 if not j['readonly_dependencies_unchanged']:raise RuntimeError('dependencies changed')
 mods.append({'name':name,'source':pin(src),'attempt':str(a),'seconds':j['seconds'],'exit_code':0,'printed_declarations':[n for n,_ in decl],'axioms':'subset of propext, Classical.choice, Quot.sound','files':[pin(a/(name+'.olean')),pin(a/'BUILD.log'),pin(a/'AXIOMS.txt'),pin(r)]})
failed=[]
for r in (OUT/'kms_strip'/'attempts').glob('*/RECEIPT.json'):
 j=json.loads(r.read_text(encoding='utf-8'));n=Path(j['source']['path']).stem
 if j['exit_code']!=0 and (BASE/(n+'.lean')).is_file():
  failed.append({'name':n,'source':pin(Path(j['source']['path'])),'receipt':pin(r),'log':pin(r.parent/'BUILD.log'),'exit_code':j['exit_code']})
obj={'unit':'F1.FECHO_20261015','claim':845,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REAL_KERNEL_TERMS_PENDING_ROOT_FOCAL_REVIEW','modules':mods,'failed_attempts_preserved':failed,
'same_objects':'TGLExt.ImportedSQ.H1 with original orbitalMeasure 0; original real O16 screen, Cartesian representative equal to p-wedge-screen on the regular chart; original F1Rede.BosonicFock.F and exponential core',
'scope':['The original coherent vectors are proved linearly independent; synthesis on labels with actual polynomial L1/L2 moments is injective and supplies unique finite coefficients in the SAME canonical Fock.', 'The concrete finite coherent domain contains the vacuum and is invariant, in both directions, under the existing translations and wedge boost. Density of this narrower domain is not asserted in this batch.', 'Every regular H1 profile has an integrable on-shell point wave; the physical Schwartz smearing is identified with it, and translation covariance is proved for the existing U1 without changing Fourier convention.', 'The actual Schwartz spacetime wave satisfies the pointwise source-free divergence by the previously constructed derivative and on-shell symbol.', 'Maxwell stress-jet conservation is a proved algebraic identity from antisymmetry, Bianchi and divergence of the first jet, with diagonal signature squared equal to one. Those conditions still need the complete wave consumer.'],
'not_claimed':['No coincident-point Wick stress on the Fock domain, tensor boost covariance, null-plane charge identity, MaxwellCertificate inhabitant, or global physical field localization is claimed.'],
'reused_receipts':[pin(OUT/'maxwell_smearing'/'FINAL_MAXWELL_ON_SHELL_RECEIPT_R1.json'),pin(OUT/'maxwell_smearing'/'FINAL_MAXWELL_SMEARING_RECEIPT_R1.json'),pin(OUT/'segal_selfadjoint'/'FINAL_SEGAL_ESSENTIAL_RECEIPT_R1.json')],
'reviewer':'root only; no duplicate semantic review requested'}
p=BASE/'FINAL_MAXWELL_FOCK_DOMAIN_WAVE_RECEIPT_R1.json'
if p.exists():raise RuntimeError('immutable receipt exists')
t=p.with_suffix('.json.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
json.loads(t.read_text(encoding='utf-8'));os.rename(t,p)
print(json.dumps(pin(p),ensure_ascii=False))
