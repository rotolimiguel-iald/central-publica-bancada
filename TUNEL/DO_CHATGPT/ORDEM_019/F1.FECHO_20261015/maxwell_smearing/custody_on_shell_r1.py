"""Custody of concrete Maxwell on-shell bivectors and screen intertwiner."""
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
 if re.search(r'\b(sorry|admit|axiom)\b',txt):raise RuntimeError("unproved token "+name)
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
 if j['exit_code']!=0 and n.startswith(('MaxwellOnShellBivector','MaxwellScreenIntertwiner')):
  failed.append({'name':n,'source':pin(Path(j['source']['path'])),'receipt':pin(r),'log':pin(r.parent/'BUILD.log'),'exit_code':j['exit_code']})
obj={'unit':'F1.FECHO_20261015','claim':845,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REAL_KERNEL_TERMS_PENDING_FINAL_FOCAL_REVIEW','modules':mods,'failed_attempts_preserved':failed,'same_objects':'H1, Sector n, F, exponential, a(f), creationVector and Segal already constructed', 'scope':['Actual O16 momentum and circular screen polarizations give a nonzero p-wedge-epsilon bivector, with exact Bianchi, gauge invariance and zero contracted divergence.', 'The physical metric-preserving momentum transport intertwines this bivector with the existing screenCoefficient; the longitudinal remainder vanishes in the wedge.', 'The 01 component equals the positive transverse mass on the regular chart, so non-vacuity is exhibited.'],'not_claimed':['spacetime Fourier restriction to H1','global photon representation from scalar orbital action','Wick stress tensor or charge_link','MaxwellCertificate inhabitant'],'reused_receipts':[pin(BASE/'SURVEY_ON_SHELL_R1.json')]}
p=BASE/'FINAL_MAXWELL_ON_SHELL_RECEIPT_R1.json'
if p.exists():raise RuntimeError('immutable receipt exists')
t=p.with_suffix('.json.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
json.loads(t.read_text(encoding='utf-8'));os.rename(t,p)
print(json.dumps(pin(p),ensure_ascii=False))
