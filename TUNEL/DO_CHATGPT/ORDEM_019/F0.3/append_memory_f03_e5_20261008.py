"""Append F0.3.E5 correction to four memory surfaces, with byte backups."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json,os,subprocess,sys
R=Path(r'C:\IALD\Central de Patentes');O=R/'Chatgpt'/'TUNEL'/'DO_CHATGPT'/'ORDEM_019';B=Path(r'C:\IALD\PROGRAMA_IALD');D=O/'F0.3'
TARGETS=[R/'memory'/'TGL_ATLAS.md',R/'memory'/'TGL_INDICE_VIVO.md',R/'memory'/'TGL_CORE_MEMORY.md',O/'AVISO_GERENCIA.md']
F=D/'PIN_FORENSICS_E5_20261008.json';C=D/'CACHE_HYGIENE_E5_RESULT_20261008.json';OUT=D/'MEMORY_F03_E5_20261008.json';MARK=b'<!-- f03_e5_quatro_pinos_cache_08out -->'
def h(x):return sha256(x).hexdigest()
def wx(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
 if OUT.exists():raise FileExistsError(OUT)
 s=json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(B/'iald.py'),'ver','F0.3.E5'],text=True));c=s.get('reivindicacao') or {};note=c.get('nota','')
 if s.get('status')!='EM_CURSO' or c.get('quem')!='codex-coordenadora' or not all(p.name in note for p in TARGETS):raise RuntimeError('F0.3.E5 named memory claim required')
 fb=F.read_bytes();d=json.loads(fb);cb=C.read_bytes();cache=json.loads(cb);assert cache['all_targets_absent']
 pins='; '.join(f"{x['relative']}: {x['old'][-1]['backup']['sha256'][:16]} → {x['current']['sha256'][:16]}" for x in d['records'])
 block=('\n\n### 08/10/2026 — F0.3.E5: quatro pinos adicionais [codex-coordenadora]\n'
        '<!-- f03_e5_quatro_pinos_cache_08out -->\n\n'
        '[ERRATA AO LADO, em nome de codex-coordenadora] Retiro a frase geral «nenhum outro pino mudou». A auditoria c1 a9f3787c achou mais quatro alterações in loco, e a forense local mediu os bytes anteriores → atuais: '+pins+'. A F0.3.E3/E4 cobria somente os alvos nela enumerados. Os estados atuais foram repinados depois, mas o repin não legitima editar pinos no lugar. Recibo PIN_FORENSICS_E5_20261008.json, SHA-256 '+h(fb)+'. O README_DEPLOY atual está no mapa 835/841; o README_V2_STAGING atual nas seq 857/860/863, precisão que corrige a referência agrupada à seq 835.\n\n'
        '[REAL — higiene] Sob a reivindicação F0.3.E5, foram removidos 9 diretórios __pycache__ e 43 arquivos .pyc (528829 bytes) apenas em ADENDO003_COORD, F2.3, F3.6, F5.2, F7.2 e F9.9. Os hashes e caminhos antes da remoção estão em CACHE_HYGIENE_E5_PLAN_20261008.json e o recibo final em CACHE_HYGIENE_E5_RESULT_20261008.json, SHA-256 '+h(cb)+'.\n\n'
        '[ESTADO] F0.3.E4 segue FECHADA pela c1; esta E5 aguarda auditoria. Originais pinados, Bancada, dados, MCP e gate intactos nesta camada.\n').encode('utf8')
 stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');orig={};prep=[]
 for p in TARGETS:
  old=p.read_bytes()
  if MARK in old:raise FileExistsError(p)
  bak=p.with_name(p.name+'.bak_'+stamp);tmp=p.with_name(p.name+'.tmp_'+stamp)
  wx(bak,old);wx(tmp,old+block)
  if bak.read_bytes()!=old or tmp.read_bytes()!=old+block:raise RuntimeError('preflight mismatch')
  orig[p]=old;prep.append((p,bak,tmp))
 rows=[]
 try:
  for p,bak,tmp in prep:
   os.replace(tmp,p);new=p.read_bytes()
   if new!=orig[p]+block:raise RuntimeError('append mismatch')
   rows.append(dict(path=str(p),before_sha256=h(orig[p]),after_sha256=h(new),backup=str(bak),backup_sha256=h(bak.read_bytes()),before_bytes=len(orig[p]),after_bytes=len(new)))
 except Exception:
  for p,bak,tmp in prep:
   if p.exists() and p.read_bytes()!=orig[p]:
    rest=p.with_name(p.name+'.restore_'+stamp);wx(rest,orig[p]);os.replace(rest,p)
  raise
 result=dict(unit='F0.3.E5',claim=c,forensics_sha256=h(fb),cache_result_sha256=h(cb),append_sha256=h(block),append_bytes=len(block),targets=rows,no_gate=True)
 wx(OUT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 print(json.dumps(dict(receipt=str(OUT),sha256=h(OUT.read_bytes()),targets=len(rows)),ensure_ascii=False))
if __name__=='__main__':main()