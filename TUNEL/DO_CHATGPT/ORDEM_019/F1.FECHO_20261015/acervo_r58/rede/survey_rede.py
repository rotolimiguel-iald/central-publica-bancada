"""Read-only scoped archival search; writes derived evidence only beside this script."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
REFERENCE = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,obj):
    p=ROOT/name
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f: f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    os.rename(tmp,p)
    return pin(p)
def project(label):
    payload={'operation':'project','reference':str(REFERENCE),'max_chars':400000}
    cp=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(payload),capture_output=True,text=True,encoding='utf8')
    result=json.loads(cp.stdout)
    ev=save(label+'.json',{'request':payload,'exit_code':cp.returncode,'response':result})
    assert cp.returncode==0 and result.get('ok'), ev
    v=result['result'];print(json.dumps({'receipt':ev,'revision':v['receipt']['revision'],'R5':[t for t in v['projection']['active'] if t['id']=='R5']},ensure_ascii=False))
def safe(p):
    s=str(p).replace('/','\\').lower()
    allowed=tuple(x+'\\' for x in (r'c:\iald\artigo',r'c:\iald\bancada_um\investigacao',r'c:\iald\central de patentes\chatgpt'))
    forbidden=('iald_stack_v7','iald_psion_state','.env','credencia','password','senha','token','\\the_boundary','\\.lake\\','\\.git\\','\\backup','\\backups','_backups','\\dependency_cache\\','\\attempts\\','\\f1.fecho_20261015\\')
    return s.startswith(allowed) and not any(x in s for x in forbidden) and '.bak' not in s
def corpus():
    idx=Path(r'C:\IALD\INDICE_DO_ACERVO\corpus_index.json')
    data=json.loads(idx.read_text(encoding='utf8')); items=data['itens']
    pats={
      'two_point':r'dois pontos|duas pontas|two.point|two.mode|squeez|correla.{0,35}(psion|psi[oô]n|campo)|Wightman',
      'refinement':r'refinamento|refinement|limite indutivo|inductive limit|continuum limit|limite cont[ií]nuo|sistema direcionado',
      'transport':r'entrela.{0,30}(dispositivo|din[aâ]mica)|intertwin.{0,35}(cell|microscopic)|Poincar[eé]|MQC|Psi.NET',
    }
    rx={k:re.compile(v,re.I) for k,v in pats.items()};seen=set();hits=[];errors=[];scanned=0;chars=0
    for it in items:
      if it.get('status')!='OK' or not safe(it.get('path','')):continue
      cp=Path(it['corpus'])
      try: b=cp.read_bytes()
      except OSError as e: errors.append({'path':str(cp),'error':str(e)});continue
      digest=hashlib.sha256(b).hexdigest()
      if digest in seen:continue
      seen.add(digest);s=b.decode('utf8',errors='replace');scanned+=1;chars+=len(s)
      counts={};samples={}
      for k,r in rx.items():
        matches=list(r.finditer(s));counts[k]=len(matches)
        samples[k]=[{'corpus_line':s.count('\n',0,m.start())+1,'text':s[max(0,m.start()-180):m.end()+240]} for m in matches[:6]]
      if any(counts.values()):hits.append({'source':it['path'],'corpus':str(cp),'corpus_sha256':digest,'counts':counts,'samples':samples})
    evidence={'scope':'Scientific paths in historical corpus index; excluded replicas/cache/backups/confidentials/F1.FECHO; exact-byte corpus deduplication. Navigation only; primary sources required.','index':pin(idx),'patterns':pats,'scanned_unique_corpora':scanned,'scanned_chars':chars,'hits':hits,'errors':errors}
    print(json.dumps({'output':save('CORPUS_SEARCH_R1.json',evidence),'scanned':scanned,'hits':len(hits),'top':[{'source':x['source'],'counts':x['counts']} for x in sorted(hits,key=lambda x:x['counts']['refinement']+x['counts']['two_point'],reverse=True)[:35]]},ensure_ascii=False))
def focused():
    roots=[r'C:\IALD\Artigo',r'C:\IALD\papers_latex',r'C:\IALD\Central de Patentes\Chatgpt',r'C:\IALD\Bancada_Um\investigacao']
    exclusions=['**/.lake/**','**/.git/**','**/*backup*/**','**/*BACKUP*/**','**/the_boundary*/**','**/*selo*/**','**/*SELO*/**','**/attempts/**','**/dependency_cache/**','**/F1.FECHO_20261015/**','**/node_modules/**','**/venv/**','**/.venv/**']
    args=['rg','--files',*roots,'-g','*.lean','-g','*.tex','-g','*.md','-g','*.txt']
    for ex in exclusions:args+=['-g','!'+ex]
    cp=subprocess.run(args,capture_output=True,text=True,encoding='utf8');assert cp.returncode==0,cp.stderr
    regex=re.compile(r'quasi.free|quasifree|quase.livre|two.point|dois pontos|duas pontas|squeez|Bogoliubov|refinamento|refinement|inductive limit|limite indutivo|continuum limit|limite cont[ií]nuo',re.I)
    seen={};hits=[];files=[];errors=[]
    for name in cp.stdout.splitlines():
      p=Path(name);s=name.lower()
      if any(x in s for x in ['iald_stack','iald_psion','.env','credential','credencia','password','senha','.bak','stdout','stderr','axioms','build.log','_log.','capture.txt']):continue
      try:b=p.read_bytes()
      except OSError as e:errors.append({'path':name,'error':str(e)});continue
      digest=hashlib.sha256(b).hexdigest()
      if digest in seen:seen[digest].append(name);continue
      seen[digest]=[name]
      if b.startswith((b'\xff\xfe',b'\xfe\xff')):text=b.decode('utf16')
      else:text=b.decode('utf8',errors='replace')
      files.append({'path':name,'sha256':digest,'bytes':len(b)})
      lines=[{'line':i,'text':line[:1200]} for i,line in enumerate(text.splitlines(),1) if regex.search(line)]
      if lines:hits.append({'path':name,'sha256':digest,'bytes':len(b),'matches':lines})
    ev={'roots':roots,'exclusions':exclusions,'regex':regex.pattern,'files_unique':len(files),'duplicates':sum(len(x)-1 for x in seen.values()),'files':files,'alias_groups':[v for v in seen.values() if len(v)>1],'hits':hits,'errors':errors}
    print(json.dumps({'output':save('FOCUSED_SEARCH_R1.json',ev),'files_unique':len(files),'hits':len(hits),'errors':errors,'quasifree':[{'path':h['path'],'lines':[x for x in h['matches'] if re.search('quasi.free|quasifree|quase.livre|Bogoliubov',x['text'],re.I)][:4]} for h in hits if any(re.search('quasi.free|quasifree|quase.livre|Bogoliubov',x['text'],re.I) for x in h['matches'])][:30]},ensure_ascii=False))
if __name__=='__main__':
    if sys.argv[1]=='project':project(sys.argv[2])
    elif sys.argv[1]=='corpus':corpus()
    elif sys.argv[1]=='focused':focused()
