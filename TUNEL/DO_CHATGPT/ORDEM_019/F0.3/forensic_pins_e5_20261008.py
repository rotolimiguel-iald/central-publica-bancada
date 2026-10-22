"""Read-only forensic of four additional in-place changed pins."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime
import json,os,difflib
O=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019');B=Path(r'C:\IALD\PROGRAMA_IALD');MAP=Path(r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl');D=O/'F0.3'
OUT=D/'PIN_FORENSICS_E5_20261008.json';MD=D/'PIN_FORENSICS_E5_20261008.md'
SPECS=[
 ('F9.5/RESULTADO.json',[(80,'5263445ac24c7fb163667f5ad9ee2da62f14730c1a1e6f4a5a6ee425d5b683dd'),(82,'bcd6b2506637c4bed902624ae7727f84f94ef866a4b50736152e418056edce52')],'7e3e11b7d17dad3ccef3fa6e7012354a6b6085265a16f0390edea2c38ee133d0','Recibo refeito após arquivar 130 backups do transporte; evento 136, mapa 720. Não é append: campos e pins foram regenerados.','codex-gerente-tgl [REAL: eventos 80, 82, 136]'),
 ('F2.3/ADENDO_TEMPERATURA_DIAGNOSTICO.md',[(355,'673780c016334c72a2463453ac5bbc8179a301c19fb2ce66814fe323def099f9')],'cb0a73cb40f68652aa0e8945a53355fefa62b429016c94c381bd8a26ed53a728','Acréscimo de 651 bytes da errata de nomenclatura F2.3.E2 às 14:15, entregue no evento 428; a própria F2.3 já possuía forense desse desvio.','codex-gerente-tgl [DERIVED: evento 428 e marcador F23_E2]'),
 ('F7.2/STAGING/README_DEPLOY.md',[(822,'0d380faae32dcc166166221d4c452cca9738c98f8f98b82b249ff9e9ea7ba802')],'3791c6e582dcdd1d5707cd4fff5da9c9e2e6e3a49128bd61e3f65d7501df1562','Correção do byte 0x0b no caminho project_fisica para os caracteres literais barra invertida + v, entregue no evento 300; não é append.','codex-gerente-tgl [DERIVED: evento 300, mapa 835]'),
 ('F7.2/V2_STAGING/README_V2_STAGING.md',[(822,'6b7442471a77c37c4703fc2567ff3c81669686196406b2776fde042e924e7e72'),(841,'6b7442471a77c37c4703fc2567ff3c81669686196406b2776fde042e924e7e72')],'cb4a2f6e3c091689ce19103b5fdedd2886a512819f8c88d99ce527baf635be3e','Acréscimo de 1175 bytes com errata de estado de implantação e Eq.6, entregue no evento 336. A frase histórica sobre ratificação pendente foi depois corrigida ao lado; não a adotar como estado atual.','codex-gerente-tgl [DERIVED: evento 336, mapa 857]')]
def h(p):return sha256(p.read_bytes()).hexdigest()
def desc(p):
 s=p.stat();return dict(path=str(p),sha256=h(p),bytes=s.st_size,mtime_local=datetime.fromtimestamp(s.st_mtime).astimezone().isoformat())
def wx(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
 if OUT.exists() or MD.exists():raise FileExistsError('E5 forensic outputs exist')
 board=[json.loads(l) for l in (B/'eventos.jsonl').open(encoding='utf8')]
 maps=[json.loads(l) for l in MAP.open(encoding='utf8')]
 rows=[]
 for rel,pins,want,reason,author in SPECS:
  p=O/Path(rel);cur=desc(p)
  if cur['sha256']!=want:raise RuntimeError('current pin changed '+rel)
  old=[]
  for seq,sha in pins:
   hits=[x for x in p.parent.glob(p.name+'.bak_*') if h(x)==sha]
   if len(hits)!=1:raise RuntimeError(f'old backup {rel} {sha[:16]} hits={len(hits)}')
   old.append(dict(seq=seq,backup=desc(hits[0]),original_in_evidencias=desc(B/'evidencias'/f'{sha}{p.suffix}') if (B/'evidencias'/f'{sha}{p.suffix}').exists() else None))
  board_pins=[]
  for e in board:
   for a in e.get('dados',{}).get('evidencia',[]) if isinstance(e.get('dados',{}).get('evidencia'),list) else []:
    if a.get('caminho')==str(p):board_pins.append(dict(seq=e['seq'],when=e['quando'],who=e['quem'],sha256=a['sha256']))
  map_pins=[]
  for e in maps:
   for a in e.get('artefatos',[]):
    if isinstance(a,dict) and a.get('caminho')==str(p):map_pins.append(dict(seq=e['seq'],when=e.get('quando'),who=e.get('quem'),sha256=a['sha256']))
  latest=old[-1]['backup']['path'];prefix=p.read_bytes().startswith(Path(latest).read_bytes())
  rows.append(dict(relative=rel,current=cur,old=old,old_prefix_of_current=prefix,board_pins=board_pins,map_pins=map_pins,change_reason=reason,author=author,attribution_status='[REAL] hashes/bytes; [DERIVED] editing hand where no writer log'))
 data=dict(unit='F0.3.E5',author='codex-coordenadora',correction='A afirmação geral «nenhum outro pino mudou» é falsa. Estes quatro arquivos também mudaram in loco e depois foram repinados. F0.3.E3/E4 só cobriam seus alvos declarados.',source_audit=r'C:\IALD\PROGRAMA_IALD\auditorias\F0.3.E4\AUDITORIA_F0_3_E4_C1_a9f3787c.md',records=rows,precise_repin_note='README_DEPLOY atual no mapa 835/841; README_V2_STAGING atual no mapa 857/860/863, não no 835.',no_pinned_source_edited=True,no_gate=True)
 wx(OUT,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 lines=['# F0.3.E5 — errata e forense curta de quatro pinos','', '[ERRATA AO LADO, em nome de codex-coordenadora] Retiro a afirmação geral «nenhum outro pino mudou». Ela é falsa: além dos casos registrados na F0.3.E3/E4, a auditoria c1 a9f3787c encontrou quatro caminhos adicionais. Os hashes abaixo foram lidos dos bytes atuais e backups. Os originais não foram editados nesta unidade.','']
 for r in rows:
  lines += [f"## {r['relative']}",'',f"Antes: "+', '.join(f"seq {o['seq']} `{o['backup']['sha256']}` ({o['backup']['bytes']} B)" for o in r['old'])+'.',f"Atual: `{r['current']['sha256']}` ({r['current']['bytes']} B; mtime {r['current']['mtime_local']}).",f"Prefixo anterior preservado: {r['old_prefix_of_current']}. {r['change_reason']}",f"Autoria: {r['author']}.",f"Repins no mapa: "+', '.join(f"{x['seq']}:{x['sha256'][:16]}" for x in r['map_pins'] if x['sha256']==r['current']['sha256'])+'.','']
 lines += ['[REAL — precisão de sequência] `README_DEPLOY.md` atual aparece no mapa 835/841. `README_V2_STAGING.md` atual aparece nas seq 857/860/863; a seq 835 não o repina. O número corrige a descrição agrupada da auditoria.','', '[ESTADO] As alterações históricas foram repinadas depois; a existência do repin não legitima editar um pino no lugar. Novas camadas seguem em novos arquivos. Sem dado aberto, publicação ou mudança de gate.','']
 wx(MD,('\n'.join(lines)).encode('utf8'))
 print(json.dumps(dict(json=str(OUT),json_sha256=h(OUT),md=str(MD),md_sha256=h(MD),records=len(rows)),ensure_ascii=False))
if __name__=='__main__':main()