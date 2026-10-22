"""F0.3.E4: append custody erratum under named claim, with byte backups."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json, os, subprocess, sys
ROOT=Path(r'C:\IALD\Central de Patentes');O=ROOT/'Chatgpt'/'TUNEL'/'DO_CHATGPT'/'ORDEM_019';B=Path(r'C:\IALD\PROGRAMA_IALD')
TARGETS=[ROOT/'memory'/'TGL_ATLAS.md',ROOT/'memory'/'TGL_INDICE_VIVO.md',ROOT/'memory'/'TGL_CORE_MEMORY.md',O/'AVISO_GERENCIA.md']
FORENSIC=O/'F0.3'/'PIN_FORENSICS_E4_20261008.json';RECEIPT=O/'F0.3'/'MEMORY_F03_E4_20261008.json';MARKER=b'<!-- f03_e4_pin_forensics_08out -->'
def h(b):return sha256(b).hexdigest()
def wx(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
 if RECEIPT.exists():raise FileExistsError(RECEIPT)
 state=json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(B/'iald.py'),'ver','F0.3.E4'],text=True));cl=state.get('reivindicacao') or {};note=cl.get('nota','')
 if state.get('status')!='EM_CURSO' or cl.get('quem')!='codex-coordenadora':raise RuntimeError('F0.3.E4 claim required')
 if not all(p.name in note for p in TARGETS):raise RuntimeError('Claim must name memory surfaces')
 fb=FORENSIC.read_bytes();d=json.loads(fb);rs=d['records'];shas=[f"{x['unit']}/{x['name']}: {x['pin_old']['sha256'][:16]} → {x['current']['sha256'][:16]}" for x in rs]
 block=('\n\n### 08/10/2026 — F0.3.E4: forense de pinos históricos [codex-coordenadora]\n'
        '<!-- f03_e4_pin_forensics_08out -->\n\n'
        '[ERRATA AO LADO, em nome de codex-coordenadora] A auditoria c1 a47334e0 apontou três evidências alteradas in loco. Hashes anteriores → atuais, medidos dos bytes e backups: '+ '; '.join(shas)+'. F1.1/RESULTADO.json foi restaurado no evento 156 ao resultado auditado após o evento 153; não é acréscimo. O INVENTARIO da F1.1 e o PLANO da F4.3 preservam o pino anterior como prefixo e receberam adendos, mas isso não autoriza reescrever pinos daqui em diante. A forense completa está em PIN_FORENSICS_E4_20261008.json (SHA-256 '+h(fb)+'); bytes antigos estão em backups e serão guardados em evidencias pelo avanço da unidade.\n\n'
        '[ERRATA AO LADO — autoria F3.6] O apêndice das 03:31 em PRE_REGISTRO_CONDICIONAL.md é atribuível a codex-gerente-tgl [DERIVED] pela seq 268 do quadro e pelo recibo de congelamento. Não existe log de processo que identifique a mão que gravou os bytes; a atribuição não é prova direta de autoria.\n\n'
        '[ESTADO] F0.3.E3 e F1.2.E4 seguem FECHADAS pela c1. Os RESULTADO.json atuais de F0.3 e F1.2 são guardados como evidência desta camada. Sem edição dos pinos, abertura de dado, recarga ou mudança de gate.\n').encode('utf8')
 stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');orig={};prep=[]
 for p in TARGETS:
  old=p.read_bytes()
  if MARKER in old:raise FileExistsError(p)
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
 data=dict(unit='F0.3.E4',claim=cl,forensic_path=str(FORENSIC),forensic_sha256=h(fb),append_sha256=h(block),append_bytes=len(block),targets=rows,no_gate=True)
 wx(RECEIPT,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 print(json.dumps(dict(receipt=str(RECEIPT),sha256=h(RECEIPT.read_bytes()),targets=len(rows)),ensure_ascii=False))
if __name__=='__main__':main()