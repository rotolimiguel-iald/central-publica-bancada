"""Finalize the claimed NU2/B1 artifacts and internal memory without deployment."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
B=Path(__file__).resolve().parent
N=B.parent/'F8.2.NU2'
MEM=Path(r'C:\IALD\Central de Patentes\memory')
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def new(p,b):
 if p.exists():raise FileExistsError(p)
 t=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 if t.read_bytes()!=b:raise RuntimeError('temporary mismatch')
 os.rename(t,p)
 if p.read_bytes()!=b:raise RuntimeError('final mismatch')
def js(p,d):new(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
mode=sys.argv[1]
if mode=='memory':
 dest=B/'MEMORY_RECEIPT_B1_NU2_R1.json'
 if dest.exists():raise FileExistsError(dest)
 paths=[B/'RELATORIO_COMPATIBILIDADE_R1.md',B/'VERSION_IDENTITY_R1.json',B/'RUNTIME_COMPARISON_R1.json',N/'RELATORIO_NEUTRINOS_R1.md',N/'CALCULOS_ESPECTRAIS_R1.json',N/'review/REPORT_REVIEW_ADDENDUM_R2.md']
 refs=[pin(p) for p in paths]
 marker='<!-- F03B1_F82NU2_20261009_codex -->'
 note='\n\n### 09/10/2026 — Neutrinos e compatibilidade da Bancada [codex-gerente-tgl]\n'+marker+'\n\n'
 note+='[INPUT] Ordens diretas do operador nesta conversa: prosseguir o estudo e verificar a Bancada contra o um.py recente. Ciencia F8.2.NU2 reivindicacao618; memoria NU2 F0.3.NU2 reivindicacao619; auditoria e memoria Bancada F0.3.B1 reivindicacao621, com estas tres superficies nomeadas. Consulta previa NosF7.2/F8.2/F0.3; unidades novas ausentes do grafo, dito; mapa982/983.\n\n'
 note+='[REAL documental; DERIVED condicional] A lei vigente de desfasamento usa beta0 fixo. A expressao beta(E) discutida na conversa e contrafactual, nao previsao instalada; v388 distingue fronteira/bulk. Densidade diagonal na base de massa permanece exatamente inalterada pelo desfasamento nessa base. Para estado coerente, tau_star=tP, Kfac=1 e geometria ideal52,5km/2-8MeV: max|deltaP|=1,7880671599537207e-39; nao e medida nem poder real do JUNO. Reproducao independente Decimal95 digitos. Textura de taxas gap^2 difere da textura do limite JUNO publicado. A ponte emissao/Ye/EOS/luminosidade e a amplitude fisica permanecem OPEN. Nenhum sigma observado calculado.\n\n'
 note+='[REAL — estado vivo e bytes] um.py atual e selo v391 conferem. A Bancada no ar desde01/10 registra como origem de alpha o hash do v379 custodiado; alpha e beta numericos sao iguais aos atuais. Isto nao identifica a versao de todo codigo em RAM. Compatibilidade e PARCIAL: modo selado e historico; modo tgl/eff existe; curvas do modo artigo desconsideram opcoes (sonda AST sintetica); Neff ainda le fonte congelada com linha errada; F7.2v2 confere fontes mas nao calcula likelihood; GW e ECOhistorico; Fase9instalada e V1, candidato E1 synthetic_only segue no tunel. TabelaCAMB tem suporte finito e nao pode ser tomada como prior fisico silencioso. Ler matriz antes de novo teste.\n\n'
 note+='Nenhuma escrita/reinicio na Bancada, nenhum ajuste observado, abertura de dado selado, mensagem a Claude ou provedor. Esta entrega nao aprova instalacao; regra evento c1 nomeado e ato X17 preservados. Nenhuma versao selada ou caminho critico alterado; sem escrita no Nos/linhagem. Gate intacto.\n\n'
 note+='Fontes desta camada (hash lido dos bytes):\n'+''.join('- '+r['path']+' — '+r['sha256']+'\n' for r in refs)
 rows=[]
 for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md']:
  p=MEM/name;old=p.read_bytes()
  if marker.encode() in old:raise RuntimeError('duplicate marker')
  stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f_UTC');bak=p.with_name(p.name+'.bak_'+stamp)
  new(bak,old)
  eol='\r\n' if b'\r\n' in old else '\n';add=note.replace('\n',eol).encode();expect=old+add
  tmp=p.with_name(p.name+'.tmp_'+stamp);new(tmp,expect)
  if p.read_bytes()!=old:raise RuntimeError('concurrent change')
  os.replace(tmp,p)
  if p.read_bytes()!=expect:raise RuntimeError('memory mismatch; backup preserved')
  rows.append(dict(before_sha256=sha(old),before_bytes=len(old),backup=pin(bak),after=pin(p),added_bytes=len(add),prefix_preserved=True))
 js(dest,dict(units=['F0.3.NU2','F0.3.B1'],claims=[619,621],author='codex-gerente-tgl',utc=datetime.now(timezone.utc).isoformat(),surfaces=rows,refs=refs))
 print(json.dumps(pin(dest)))
elif mode=='package':
 mr=pin(B/'MEMORY_RECEIPT_B1_NU2_R1.json')
 for root,unit,claim,report,verdict,route,domain in [(N,'F8.2.NU2',618,'RELATORIO_NEUTRINOS_R1.md','CONDITIONAL_OPERATOR_CHECKED_PHYSICAL_MAPPING_OPEN','sn.neutrinos.v388_operador_e_identificabilidade','SUPERNOVA_IA'),(B,'F0.3.B1',621,'RELATORIO_COMPATIBILIDADE_R1.md','PARTIAL_COMPATIBILITY_NOT_READY_FOR_NEW_NEUTRINO_STELLAR_TEST','infra.bancada_um.compatibilidade_v391_09out','INFRAESTRUTURA')]:
  dest=root/'RESULTADO_R1.json'
  if dest.exists() or (root/'MAPA_FINAL_R1.json').exists():raise FileExistsError(dest)
  files=[pin(p) for p in sorted(root.rglob('*')) if p.is_file() and '.tmp_' not in p.name and p.name not in ['RESULTADO_R1.json','MAPA_FINAL_R1.json']]
  js(dest,dict(unit=unit,claim=claim,author='codex-gerente-tgl',utc=datetime.now(timezone.utc).isoformat(),status='ENTREGUE_PARA_AUDITORIA_E_DISCUSSAO',verdict=verdict,report=pin(root/report),memory_receipt=mr,observed_sigma=None,observed_fit=False,bench_writes=False,bench_restart=False,provider_call=False,gate_effect='NONE',files=files))
  js(root/'MAPA_FINAL_R1.json',dict(tipo='RESULTADO',rota_id=route,dominio=domain,titulo=unit+' — '+verdict,status='EXAMINADA',estatuto='REAL documental/computacional; DERIVED condicional; OPEN matching fisico',veredito=verdict,olhou_dados=False,artefatos=[str(dest),str(root/report),mr['path']],nota='Leitura de literatura/documentos nao cega; nenhum ajuste observado. Estatutos e limites no relatorio. Candidatos nao instalados; nenhuma mensagem a Claude/provedor.'))
  print(json.dumps(pin(dest)))
else:raise ValueError(mode)
