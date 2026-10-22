"""Append F0.3.E6 forensic note to four memories under named claim."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json,os,subprocess,sys
R=Path(r'C:\IALD\Central de Patentes');O=R/'Chatgpt'/'TUNEL'/'DO_CHATGPT'/'ORDEM_019';B=Path(r'C:\IALD\PROGRAMA_IALD');D=O/'F0.3'
TARGETS=[R/'memory'/'TGL_ATLAS.md',R/'memory'/'TGL_INDICE_VIVO.md',R/'memory'/'TGL_CORE_MEMORY.md',O/'AVISO_GERENCIA.md']
F=D/'PIN_FORENSICS_E6_20261008.json';OUT=D/'MEMORY_F03_E6_20261008.json';MARK=b'<!-- f03_e6_missing_pins_08out -->'
def h(b):return sha256(b).hexdigest()
def wx(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
 if OUT.exists():raise FileExistsError(OUT)
 s=json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(B/'iald.py'),'ver','F0.3.E6'],text=True));cl=s.get('reivindicacao') or {};note=cl.get('nota','')
 if s.get('status')!='EM_CURSO' or cl.get('quem')!='codex-coordenadora' or not all(p.name in note for p in TARGETS):raise RuntimeError('F0.3.E6 named memory claim required')
 fb=F.read_bytes();d=json.loads(fb)
 if h((O/'AVISO_GERENCIA.md').read_bytes())!=d['aviso_gerencia']['pre_e6']['sha256']:raise RuntimeError('AVISO changed after forensic snapshot')
 block=('\n\n### 08/10/2026 — F0.3.E6: pinos históricos remanescentes [codex-coordenadora]\n'
        '<!-- f03_e6_missing_pins_08out -->\n\n'
        '[ERRATA AO LADO, em nome de codex-coordenadora] A nota .md da F0.3.E5 omitiu o estado anterior `da2513df` do ADENDO_TEMPERATURA_DIAGNOSTICO.md, pinado nos mapas 817/829 e preservado no backup `.bak_20261008_114746`. A ordem medida é da2513df → 673780c0 → cb0a73cb, com prefixo preservado. Uma sonda preliminar inverteu os dois primeiros, falhou antes de escrever e foi corrigida.\n\n'
        '[REAL — custódia] `F1.1/INVENTARIO.md` pino 73 (04a42d03, 5314 B) e `AVISO_GERENCIA.md` mapas 821/822 (ba432582, 31561 B) sobrevivem em backups byte a byte, prefixos dos estados posteriores. O pino `.pyc` F3.6 do mapa 816 (111fea0c, 19958 B) foi removido na higiene E5; seu hash está no plano, mas os bytes não estão em `evidencias/` nem no caminho. Esse pino histórico NÃO se reproduz dos arquivos atuais. Recibo PIN_FORENSICS_E6_20261008.json, SHA-256 '+h(fb)+'.\n\n'
        '[ESTADO] F0.3.E5 permanece FECHADA pela c1. Esta E6 espera reauditoria. Nada foi aberto, recarregado ou promovido no gate.\n').encode('utf8')
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
 rec=dict(unit='F0.3.E6',claim=cl,forensic_sha256=h(fb),append_sha256=h(block),append_bytes=len(block),targets=rows,no_gate=True)
 wx(OUT,(json.dumps(rec,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 print(json.dumps(dict(receipt=str(OUT),sha256=h(OUT.read_bytes()),targets=len(rows)),ensure_ascii=False))
if __name__=='__main__':main()