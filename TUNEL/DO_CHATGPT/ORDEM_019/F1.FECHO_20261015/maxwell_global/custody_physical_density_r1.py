"""Custody of the constructive physical smearing density and regular Fock domain."""
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
'same_objects':'Original TGLExt.ImportedSQ.H1 and F1Rede.BosonicFock.F; regular coherent domain already constructed in RegularMaxwellFockDomainR5.',
 'scope':['Smooth compact profiles are dense for the actual orbital measure; they satisfy every L1 and L2 energy moment. The unchanged regular coherent domain is dense in the unchanged canonical Fock space.', 'A smooth cutoff outside the kernel of a linear map converges in L2 when that kernel is a measured-null set. The measured-null transverse axis specializes this to an explicit dense chart class.', 'An explicit tensor inverse uses the 01 and 23 screen components. Smoothness across the axis is proved from actual vanishing near that axis.', 'The smooth compact tensor is extended to four-dimensional momentum by a time cutoff equal to one on the compact shell-energy image. The existing physical Fourier surjectivity produces actual spacetime Schwartz tests.', 'Every axis-avoiding compact smooth profile lies in the range of physicalSmearCLM, hence this same map has dense range.'],
'not_claimed':['The auxiliary fixed-axis chart class is not claimed invariant under every Lorentz transformation.', 'Dense range alone does not prove wedge localization, causal commutation, stress covariance, or a null-plane charge identity.', 'The extension is a momentum-space compact tensor; its inverse Fourier test is Schwartz and is not asserted compactly supported in spacetime.', 'No MaxwellCertificate is fabricated from density.'],
'reused_receipts':[pin(BASE/'FINAL_REAL_MAXWELL_STRESS_RECEIPT_R1.json')],
'reviewer':'root only; no duplicate semantic review requested','production_modified':False,'gate_modified':False,'provider_calls':False}
p=BASE/'FINAL_MAXWELL_PHYSICAL_DENSITY_RECEIPT_R1.json'
if p.exists():raise RuntimeError('immutable receipt exists')
t=p.with_suffix('.json.tmp')
with t.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
json.loads(t.read_text(encoding='utf-8'));os.rename(t,p)
print(json.dumps(pin(p),ensure_ascii=False))
