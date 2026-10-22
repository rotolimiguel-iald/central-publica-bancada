"""Recompile frozen candidate sources independently; inputs readonly, outputs sandbox."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review'/'lean_independent'
OUT.mkdir(exist_ok=False)
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
search=[K/'.lake/build/lib/lean']+sorted((K/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=dict(os.environ,LEAN_PATH=';'.join(str(p) for p in search))
assert all(p.is_relative_to(K/'.lake') and p.is_dir() for p in search)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_new(p,b):
 with Path(p).open('xb') as f:f.write(b)
def write_json(p,o):write_new(p,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
assert '4.31.0' in version
entries=[('main',ROOT/'lean_candidate'/'TheSingularityReadsTheAttractor.lean',ROOT/'lean_candidate'/'FINAL_LEAN_RECEIPT_R1.json'),('optical',ROOT/'lean_optical_bridge'/'OpticalPopulationBridgeR2.lean',ROOT/'lean_optical_bridge'/'FINAL_OPTICAL_RECEIPT_R1.json')]
results=[]
for role,src,final in entries:
 final_data=json.loads(final.read_text(encoding='utf-8'));data=src.read_bytes();before=sha(src)
 pinned=[]
 def visit(o):
  if isinstance(o,dict):
   if o.get('path')==str(src) and 'sha256' in o:pinned.append(o['sha256'])
   for v in o.values():visit(v)
  elif isinstance(o,list):
   for v in o:visit(v)
 visit(final_data)
 assert before in pinned, (role,'source not final-pinned')
 local=OUT/src.name;write_new(local,data)
 assert re.search(r'\bsorry\b|\baxiom\s',data.decode()) is None
 olean=local.with_suffix('.olean')
 cmd=[str(LEAN),'-o',str(olean),str(local)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
 cp=subprocess.run(cmd,cwd=OUT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 elapsed=time.perf_counter()-t;end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 output=cp.stdout+cp.stderr
 log=('COMMAND: '+repr(cmd)+'\nTOOLCHAIN: '+version+'\nLEAN_PATH: '+env['LEAN_PATH']+'\nSTART: '+start+'\nEND: '+end+'\nSECONDS: '+str(elapsed)+'\nEXIT: '+str(cp.returncode)+'\nOUTPUT:\n').encode()+output
 logpath=OUT/(role+'_BUILD.log');write_new(logpath,log)
 declarations=[]
 for name,ax in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",output.decode('utf-8','replace')):
  axioms=[x.strip() for x in ax.split(',') if x.strip()];assert set(axioms)<= {'propext','Classical.choice','Quot.sound'}
  declarations.append({'name':name,'axioms':axioms})
 assert sha(src)==before,'source changed during independent build'
 result={'role':role,'source':str(src),'source_sha256':before,'copied_source':str(local),'copied_source_sha256':sha(local),'source_final_receipt':str(final),'source_final_receipt_sha256':sha(final),'command':cmd,'cwd':str(OUT),'toolchain':version,'LEAN_PATH':env['LEAN_PATH'],'start_utc':start,'end_utc':end,'seconds':elapsed,'exit_code':cp.returncode,'printed_axioms':declarations,'print_count':len(declarations),'sorry_source':False,'sorryAx_log':b'sorryAx' in output,'log':str(logpath),'log_sha256':sha(logpath),'olean':str(olean),'olean_sha256':sha(olean) if olean.exists() else None}
 # Olean equality is measured, not presumed.
 original_artifacts=[]
 def arts(o):
  if isinstance(o,dict):
   if str(o.get('path','')).endswith('.olean') and 'sha256' in o:original_artifacts.append(o)
   for v in o.values():arts(v)
  elif isinstance(o,list):
   for v in o:arts(v)
 arts(final_data)
 result['matching_original_olean_paths']=[i['path'] for i in original_artifacts if i['sha256']==result['olean_sha256']]
 write_json(OUT/(role+'_RECEIPT.json'),result);results.append(result)
 print(json.dumps({'role':role,'exit':cp.returncode,'seconds':elapsed,'axioms_printed':len(declarations),'olean_same_as_original':bool(result['matching_original_olean_paths'])}),flush=True)
 assert cp.returncode==0 and not result['sorryAx_log']
 assert len(declarations)==(14 if role=='main' else 15)
write_json(OUT/'INDEPENDENT_BUILD_RESULT.json',{'status':'PASSA','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':sha(__file__),'builds':results})
