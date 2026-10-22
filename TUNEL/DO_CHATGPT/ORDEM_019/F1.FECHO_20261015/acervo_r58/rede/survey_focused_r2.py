"""Bounded primary-file search excluding historical copies of canonical kernel modules."""
from survey_rede import *
roots=[r'C:\IALD\Artigo',r'C:\IALD\papers_latex',r'C:\IALD\Central de Patentes\Chatgpt',r'C:\IALD\Bancada_Um\investigacao']
exclusions=['**/.lake/**','**/.git/**','**/*backup*/**','**/*BACKUP*/**','**/the_boundary*/**','**/*selo*/**','**/*SELO*/**','**/attempts/**','**/dependency_cache/**','**/F1.FECHO_20261015/**','**/node_modules/**','**/venv/**','**/.venv/**','**/vault/**','**/originals_copy/**','**/boundary_sources/**','**/dev_build/**','**/build/**']
args=['rg','--files',*roots,'-g','*.lean','-g','*.tex','-g','*.md']
for ex in exclusions:args+=['-g','!'+ex]
cp=subprocess.run(args,capture_output=True,text=True,encoding='utf8');assert cp.returncode==0,cp.stderr
names=cp.stdout.splitlines();print('enumerated',len(names),flush=True)
canonical={p.name for p in KERNEL.glob('*.lean')}
metadata=[];skipped=[];hits=[];seen={};errors=[]
rx=re.compile(r'quasi.free|quasifree|quase.livre|two.point|dois pontos|duas pontas|squeez(?:ed|ing)|Bogoliubov|refinamento|refinement|inductive limit|limite indutivo|continuum limit|limite cont[ií]nuo',re.I)
for name in names:
 p=Path(name);s=name.lower()
 if any(x in s for x in ['iald_stack','iald_psion','.env','credencia','password','senha','.bak']):continue
 if 'central de patentes' in s and p.suffix=='.lean' and p.name in canonical:
  skipped.append({'path':name,'reason':'canonical_module_basename_copy_not_rehashed'});continue
 if p.suffix=='.md' and not re.search(r'gns|fock|rede|net|torre|tower|continu|graviton|modular|q6|two.point|squeez|relatorio|report|entrega|delivery|resposta|sintese|inventory|inventario|index|indice',p.name,re.I):
  skipped.append({'path':name,'reason':'navigation_filename_outside_focus'});continue
 try:
  if p.stat().st_size>2_000_000:
   skipped.append({'path':name,'reason':'large_source_not_read_by_bulk_search_primary_read_separate'});continue
  b=p.read_bytes()
 except OSError as e:errors.append({'path':name,'error':str(e)});continue
 digest=hashlib.sha256(b).hexdigest()
 if digest in seen:seen[digest].append(name);continue
 seen[digest]=[name]
 text=b.decode('utf16') if b.startswith((b'\xff\xfe',b'\xfe\xff')) else b.decode('utf8',errors='replace')
 record={'path':name,'bytes':len(b),'sha256':digest};metadata.append(record)
 matches=[{'line':i,'text':line[:1000]} for i,line in enumerate(text.splitlines(),1) if rx.search(line)]
 if matches:hits.append({**record,'matches':matches})
e={'roots':roots,'glob_exclusions':exclusions,'pattern':rx.pattern,'enumerated':len(names),'unique_read':len(metadata),'bytes_read_unique':sum(x['bytes'] for x in metadata),'exact_duplicates':sum(len(x)-1 for x in seen.values()),'source_pins':metadata,'aliases':[x for x in seen.values() if len(x)>1],'skipped':skipped,'hits':hits,'errors':errors,'prior_scan':'FOCUSED R1 was manually interrupted after extended traversal of historical replicas; no completed evidence or negative conclusion from that attempt. This bounded pass records every omission.'}
print(json.dumps({'result':save('FOCUSED_SEARCH_R2.json',e),'unique_read':len(metadata),'hits':len(hits),'skipped':len(skipped),'quasi':[{'path':x['path'],'matches':[m for m in x['matches'] if re.search(r'quasi.free|quasifree|quase.livre|Bogoliubov',m['text'],re.I)][:4]} for x in hits if any(re.search(r'quasi.free|quasifree|quase.livre|Bogoliubov',m['text'],re.I) for m in x['matches'])][:20]},ensure_ascii=False))
