"""Independent static/array audit of the pinned synthetic pilot; never imports author modules."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,sys,subprocess
from audit_provenance import OUT,atomic,metadata
import numpy as np
ROOT=OUT.parent
P=ROOT/'preregistros/conjunto_d/piloto_sintetico'
SOURCES={};checks=[];details={}
def meta(p):
 m,b=metadata(p);SOURCES[str(p)]=m;return m,b
def read(p):return json.loads(meta(p)[1])
def sha(p):return meta(p)[0]['sha256']
def check(name,ok,detail=None):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));return bool(ok)
def ahash(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
cfg=read(P/'CONFIG_SYNTHETIC.json')
contracts=[];results=[]
for suffix,run,launcher in [('', 'RUN_001','launch_qualification.py'),('_V2','RUN_002','launch_qualification_v2.py')]:
 c=read(P/f'CONTRATO_P0_P2{suffix}.json');contracts.append(c)
 r=read(P/run/'RESULT.json');results.append(r)
 rec=read(P/f'EXECUTION_RECEIPT{suffix}.json')
 for rel,pin in c['inputs'].items():
  m,_=meta(P/rel);check(f'{run}: input {rel}',m['sha256']==pin['sha256'] and m['bytes']==pin['bytes'])
 check(run+': supervisor pin',sha(P/launcher)==c['supervisor_sha256'])
 check(run+': contract receipt pins',r['contract_sha256']==rec['contract_sha256']==sha(P/f'CONTRATO_P0_P2{suffix}.json'))
 check(run+': subprocess command and rc',rec['command']==c['launch_command'] and rec['returncode']==0 and rec['status']=='PROCESS_RETURNED')
 for stream in ['stdout','stderr']:check(run+': '+stream+' log pin',sha(P/f'{run}.{stream}.log')==rec['logs'][stream+'_sha256'])
 stdout=(P/f'{run}.stdout.log').read_text().splitlines();summary=json.loads(stdout[-1]);check(run+': stdout summary result',all(r[k]==v for k,v in summary.items()))
 for x in rec['original_source_checks']:
  orig,copy=Path(x['original']),Path(x['copy']);mo,_=meta(orig);mc,_=meta(copy)
  check(run+': original copy '+orig.name,mo['sha256']==mc['sha256']==x['sha256'] and mo['bytes']==mc['bytes']==x['bytes'])
 p1=read(P/run/'P1_CONTROLS.json')
 check(run+': pre-native controls',p1['status']=='PASS' and p1['native_calls']==0 and p1['controls']==r['controls'][:len(p1['controls'])])
 check(run+': all controls',all(x['passed'] for x in r['controls']),{'count':len(r['controls'])})
 check(run+': no PE D or new remote',r['PE_calls']==0 and not any(r[k] for k in ['D_strain_read','D_posterior_read','originals_executed','P3_or_recovery_performed']) and r['new_remote_calls']==0)
 check(run+': no EDOM',r['EDOM_count']==0 and len(meta(P/run/'EDOM_LOG.jsonl')[1])==0)
 check(run+': count and cost',r['native_calls_counted']==len(r['native_trace'])==6 and r['wall_seconds']<c['max_wall_seconds'] and rec['wall_seconds']<650)
 check(run+': native family grid',all(x['family']=='pSEOBNRv4HM_PA' and x['generation_bins']==131073 and x['generation_fmax']==4096 for x in r['native_trace']))
 check(run+': only DTau220',all(x['deformations'][k]==0 for x in r['native_trace'] for k in ['DTau440','DOmega220','DOmega440']))
 seq=[x['deformations']['DTau220'] for x in r['native_trace'][:3]]
 check(run+': GR RB GR',seq[0]==seq[2]==0 and seq[1]<0,seq)
 ctrl={x['name']:x['detail'] for x in r['controls']}
 check(run+': dictionaries and repeat',ctrl['fresh_LAL_dictionary_every_native_generation']=={'dictionaries':6,'native_calls':6,'all_unique':True} and ctrl['native_GR_RB_GR_repeat']=={'relative_error':0.0,'bitwise_equal':True})
 mounted=r['filesystem_audit_mounted_paths'];prefix='/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico'
 check(run+': mounted allowlist observations',all((not x['allowed']) or x['path'].startswith(prefix+'/') for x in mounted) and all(not x['write'] or not x['allowed'] or x['path'].startswith(prefix+'/'+run+'/') for x in mounted))
 check(run+': sentinel denial',r['blocked_operations']==[{'event':'open','path':'/mnt/c/NO_SCIENTIFIC_INPUT_SENTINEL','write':False}])
 for kind in ['source_truth_derivation','stress_truth_derivation']:
  d=r[kind];b=7.2973525693e-3*math.sqrt(math.e);s=d['chi_f'];root=math.sqrt(1-s*s);k=4*math.pi*(1+root)/root;F=1.5251-1.1568*(1-s)**.1292;Q=.7+1.4187*(1-s)**(-.4990);x=b*k*F*Q
  calc={'beta_runtime':b,'k':k,'F':F,'Q':Q,'x':x,'dtau220':-x/(1+x)}
  check(run+': truth algebra '+kind,all(math.isclose(v,d[n],rel_tol=1e-14,abs_tol=0) for n,v in calc.items()),calc)
 m,_=meta(P/run/'SYNTHETIC_ARRAYS.npz');check(run+': NPZ pin',m['sha256']==r['arrays']['sha256'] and m['bytes']==r['arrays']['bytes'])
 with np.load(P/run/'SYNTHETIC_ARRAYS.npz',allow_pickle=False) as z:
  a={k:z[k] for k in z.files}
 f=a['frequencies_Hz'];p=a['PSD_analytic_strain2_per_Hz'];mask=(f>=20)&(f<=1024);T=32
 check(run+': analysis grid',np.array_equal(f,np.fft.rfftfreq(32*4096,1/4096)) and len(f)==65537 and mask.sum()==32129)
 check(run+': PSD array',ahash(p)==ctrl['analytic_PSD_positive_finite_on_band']['sha256'] and np.all(np.isfinite(p[mask])) and np.all(p[mask]>0) and np.all(np.isposinf(p[~mask])))
 want={'frequencies_Hz','PSD_analytic_strain2_per_Hz'}|{f'{x}_{d}_{v}' for x in ['GR_ZERO','GR_GAUSS','RB_GAUSS'] for d in ['H1','L1'] for v in ['noise_fd','signal_fd']}
 check(run+': array key allowlist',set(a)==want,sorted(a))
 rows=[]
 for inj in r['injections']:
  lab=inj['label'];s2=0
  for detector,norm in inj['normalization'].items():
   n=a[f'{lab}_{detector}_noise_fd'];s=a[f'{lab}_{detector}_signal_fd'];check(f'{run}: {lab} {detector} payload hashes',ahash(n)==norm['noise_sha256'] and ahash(s)==norm['signal_sha256'])
   check(f'{run}: {lab} {detector} finite',n.shape==f.shape==s.shape and np.isfinite(n).all() and np.isfinite(s).all())
   q=4/T*float(np.sum(np.abs(n[mask])**2/p[mask]));df=2*int(mask.sum());zz=0. if lab=='GR_ZERO' else (q-df)/math.sqrt(2*df)
   s2+=4/T*float(np.sum(np.abs(s[mask])**2/p[mask]))
   check(f'{run}: {lab} {detector} noise normalization',math.isclose(q,norm['noise_quadratic'],rel_tol=1e-12,abs_tol=1e-12) and math.isclose(zz,norm['z'],rel_tol=1e-12,abs_tol=1e-12) and df==norm['dof'])
   reconstructed=n+s
   matched=ahash(reconstructed)==norm['injected_sha256']
   check(f'{run}: {lab} {detector} reconstructed injected hash',matched,{'sha256':ahash(reconstructed),'pin':norm['injected_sha256']})
   rows.append({'label':lab,'detector':detector,'quadratic':q,'z':zz,'injected_hash_exact':matched})
  check(run+': '+lab+' network full IMR SNR',math.isclose(math.sqrt(s2),20,rel_tol=1e-12),math.sqrt(s2))
 for d in ['H1','L1']:
  check(run+': paired same noise '+d,np.array_equal(a[f'GR_GAUSS_{d}_noise_fd'],a[f'RB_GAUSS_{d}_noise_fd']))
  check(run+': zero noise '+d,np.count_nonzero(a[f'GR_ZERO_{d}_noise_fd'])==0)
 check(run+': detectors not identical noise',not np.array_equal(a['GR_GAUSS_H1_noise_fd'],a['GR_GAUSS_L1_noise_fd']))
 details[run]={'arrays':rows,'controls':len(r['controls']),'native_calls':r['native_calls_counted'],'grid':{'analysis_bins':len(f),'generation_bins':131073,'df_Hz':float(f[1]-f[0]),'active_bins':int(mask.sum())}}
check('V2 lineage',contracts[1]['parent_contract_sha256']==sha(P/'CONTRATO_P0_P2.json') and contracts[1]['first_run_result_sha256']==sha(P/'RUN_001/RESULT.json'))
check('aggregate calls budget',sum(r['native_calls_counted'] for r in results)==12<=contracts[1]['aggregate_unit_native_call_cap']==32 and contracts[1]['native_calls_already_used']==6 and contracts[1]['max_native_calls']==26)
check('runs numeric arrays identical',sha(P/'RUN_001/SYNTHETIC_ARRAYS.npz')==sha(P/'RUN_002/SYNTHETIC_ARRAYS.npz'))
old=read(ROOT/'VERIFICACAO_INDEPENDENTE_RINGDOWN_SHAPE.json')['source'];v1=Path(old['path']);vm,_=meta(v1)
check('V1 byte preservation only',vm['sha256']==old['sha256'] and vm['bytes']==old['bytes'])
# Static inventory: parse source, do not import it or execute any of its calls.
static={}
for rel in ['src/pseob_source.py','src/temporal_contract.py','src/synthetic_adapter.py','src/synthetic_adapter_v2.py','qualify_synthetic.py','qualify_synthetic_v2.py','launch_qualification.py','launch_qualification_v2.py']:
 raw=meta(P/rel)[1];tree=ast.parse(raw.decode('utf-8-sig'));calls=[]
 for node in ast.walk(tree):
  if isinstance(node,ast.Call):calls.append({'line':node.lineno,'function':ast.unparse(node.func)})
 static[rel]=calls
runtime=read(P/'ENVIRONMENT_NATIVE_HASHES.json');check('runtime manifest count and scope',len(runtime['files'])==165 and all(x['path'].startswith('/opt/lal_env/lib/') for x in runtime['files']) and results[1]['runtime_hashes_verified_before_native_calls']==165)
for name in ['DIFF_ADAPTER_V2.patch','CONTRATO_PREFLIGHT.json','CONTRATO_RUNTIME_HASHES.json','environment_preflight.py','runtime_hashes.py']:meta(P/name)
manifest=read(P/'MANIFESTO_PILOTO_SINTETICO.json')
check('manifest file count',manifest['n_files']==len(manifest['files'])==39)
for row in manifest['files']:
 path=(P/row['file']).resolve();check('manifest bounded path '+row['file'],path.is_relative_to(P.resolve()) and path==Path(row['path']).resolve())
 m,_=meta(path);check('manifest pin '+row['file'],m['sha256']==row['sha256'] and m['bytes']==row['bytes'])
errata=read(P/'ERRATA_ALLOWLIST_RUN002.json')
check('F3-01 errata resolves stale prose without rewriting contract',errata['contract_sha256_unchanged']==sha(P/'CONTRATO_P0_P2_V2.json') and errata['code_sha256']==sha(P/'qualify_synthetic_v2.py') and errata['result_sha256']==sha(P/'RUN_002/RESULT.json') and 'RUN_002' in errata['correction'])
record={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Independent hashes, static Python AST and synthetic saved arrays only; no author imports, native waveform regeneration, real D, PE or remote calls.','reviewer_numpy':np.__version__,'checks':checks,'details':details,'static_call_inventory':static,'sources':list(SOURCES.values()),'findings_pending_document_review':[{'id':'F3-01','priority':'P3','text':'V2 contract prose says RUN_001 write allowlist; effective run_id/code/receipt say RUN_002. Preserve pin and correct beside.'}],'all_checks_pass':all(x['passed'] for x in checks),'native_calls_by_reviewer':0,'PE_calls_by_reviewer':0,'D_opened':False}
atomic(OUT/'REVISAO_PILOTO_SINTETICO_F3.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'pass':sum(x['passed'] for x in checks),'failed':[x for x in checks if not x['passed']],'sources':len(SOURCES),'details':details},ensure_ascii=False,indent=2))
