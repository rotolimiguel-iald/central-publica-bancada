"""F0.3.E4: read-only forensic of three historical evidence pins."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json, os
O=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019')
B=Path(r'C:\IALD\PROGRAMA_IALD')
D=O/'F0.3'
OUT=D/'PIN_FORENSICS_E4_20261008.json'
MD=D/'PIN_FORENSICS_E4_20261008.md'
def h(p):return sha256(p.read_bytes()).hexdigest()
def desc(p):
 s=p.stat();return dict(path=str(p),sha256=h(p),bytes=s.st_size,mtime_local=datetime.fromtimestamp(s.st_mtime).astimezone().isoformat())
def write_x(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def old_backup(p,want):
 z=[x for x in p.parent.glob(p.name+'.bak_*') if h(x)==want]
 if len(z)!=1:raise RuntimeError(f'Expected one backup for {p.name}: {len(z)}')
 return z[0]
def record(unit,name,seq,want,attribution,why):
 p=O/unit/name;old=old_backup(p,want);cur=desc(p);prior=desc(old)
 ev=B/'evidencias'/f'{want}{p.suffix}'
 chain=[desc(x) for x in p.parent.glob(p.name+'.bak_*') if x.stat().st_size>=old.stat().st_size and x.stat().st_mtime>=old.stat().st_mtime]
 chain.sort(key=lambda a:(a['bytes'],a['mtime_local']))
 # Count the old pin and each later distinct byte state, then current.
 states=[]
 for x in [prior]+chain+[cur]:
  if x['sha256'] not in [y['sha256'] for y in states]:states.append(x)
 old_bytes=old.read_bytes();cur_bytes=p.read_bytes()
 return dict(unit=unit,name=name,original_board_seq=seq,pin_old=prior,current=cur,official_old_copy=desc(ev) if ev.exists() else None,old_bytes_prefix_of_current=cur_bytes.startswith(old_bytes),intermediate_states=states,author=attribution,reason=why,status='[REAL] hashes/bytes; [DERIVED] person/intent from board and append text')
def main():
 if OUT.exists() or MD.exists():raise FileExistsError('E4 output exists')
 rs=[
 record('F1.1','RESULTADO.json',153,'3aace86312e4ae671d35cc5576bf0c5fa78a6bfecdbd97b18e66b26a79b4f334','codex-gerente-tgl [REAL: eventos 153 e 156]','Evento 153 anexou LightOneParticleByTerm ao recibo original às 20:27; evento 156 restaurou byte a byte o resultado auditado às 20:29, mantendo o complemento em RESULTADO_ADENDO_LIGHT_TERM.json. A troca foi reversão, não adendo.'),
 record('F1.1','INVENTARIO.md',241,'ca769177c2bcbcacdf288399eb24cbd92e4102895966705b58ca24c0e1b96b2c','codex-gerente-tgl [DERIVED: eventos 258, 274, 276, 349/354]','Acréscimos cumulativos: terceira camada R1–R5; errata CR-09; leitura do contorno no plano do boost e precisão do quociente; sexta camada F1.1.E1. O último apêndice é associado à reivindicação 349 e entrega 354.'),
 record('F4.3','PLANO_E_PREREGISTRO.md',254,'10c80b981c22df24a826cc454f746df2f0cb493acacd2358e2ca6b21182dbf46','codex-gerente-tgl [DERIVED: evento 315]','Adendo documental R1–R3 da c1 sobre relógio V1, ramo prógrado/contra-rotante, ordem IMR/FWER e função de veredito; entregue no evento 315 às 09:53. O arquivo mudou às 09:46 por apêndice.')]
 f36=O/'F3.6'/'PRE_REGISTRO_CONDICIONAL.md'
 curr=[desc(O/'F0.3'/'RESULTADO.json'),desc(O/'F1.2'/'RESULTADO.json')]
 assert rs[0]['current']['sha256']=='bb697c8058483809f0eaba06a0b1afd2f12a83e937199a8a803f73e0f390e834'
 assert rs[1]['current']['sha256']=='9f8c891810c2da3160bd88f96fd7514d8666df260c3cdcc997da94073d3fb10e'
 assert rs[2]['current']['sha256']=='f58e42b2e8c500c1315d212e9f3fdfc14d9f44485360fbccd57d78a7edc78612'
 assert curr[0]['sha256']=='6f7d07e7309b30169798ae47f0994fa491af9ab9ac92fe19821e9d588803a7ac'
 assert curr[1]['sha256']=='cbb7866c194ddb5079a41fc59fa0b826240cd3469c09d9a48a74a7046ed3c99b'
 assert rs[1]['old_bytes_prefix_of_current'] and rs[2]['old_bytes_prefix_of_current'] and not rs[0]['old_bytes_prefix_of_current']
 data=dict(unit='F0.3.E4',author='codex-coordenadora',status='[REAL/DERIVED]',records=rs,current_bytes_to_custody=curr,f36_0331_author=dict(name='codex-gerente-tgl',status='[DERIVED]',basis='F3.6 quadro seq 268, 03:45:33, artifacts of the Asimov; FREEZE_PRE_RUN.json pre-run hash and 03:31 append chronology in F0.3 PIN_FORENSICS_E3_20261008. No process-level writer log.',path=str(f36)),no_gate=True)
 write_x(OUT,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 lines=['# F0.3.E4 — forense de três pinos e autoria do apêndice F3.6','', '[REAL] Hashes e bytes medidos no ato. [DERIVED] Atribuição pessoal quando baseada na sequência do quadro, não em log de escrita do processo. Nenhum dos três arquivos pinados foi editado nesta camada.','', 'A escrita de 03:31 no pré-registro F3.6 é atribuída a **codex-gerente-tgl [DERIVED]** pelo evento 268 e o recibo de congelamento. Não há log de processo que prove a mão que gravou aqueles bytes.','']
 for x in rs:
  lines += [f"## {x['unit']}/{x['name']} — seq {x['original_board_seq']}",'',f"Anterior: `{x['pin_old']['sha256']}` ({x['pin_old']['bytes']} B), preservado em `{x['pin_old']['path']}`.",f"Atual: `{x['current']['sha256']}` ({x['current']['bytes']} B; mtime {x['current']['mtime_local']}).",f"Autoria: {x['author']}. {x['reason']}",f"Prefixo antigo preservado: {x['old_bytes_prefix_of_current']}. Estados intermediários: "+', '.join(y['sha256'][:16] for y in x['intermediate_states'])+'.','']
 lines += ['## Custódia solicitada','', 'O avanço F0.3.E4 deve guardar em `evidencias/` os bytes atuais de F0.3/RESULTADO.json e F1.2/RESULTADO.json e os bytes anteriores e atuais dos três pinos acima. Os caminhos e hashes medidos estão no JSON vizinho.','', '[ESTADO] A auditoria da c1 permanece soberana. Sem abertura de dados, recarga, publicação ou mudança de gate.','']
 write_x(MD,('\n'.join(lines)).encode('utf8'))
 print(json.dumps(dict(json=str(OUT),json_sha256=h(OUT),md=str(MD),md_sha256=h(MD),current=curr),ensure_ascii=False))
if __name__=='__main__':main()