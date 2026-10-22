"""Copy requested canonical artifacts byte-for-byte; never execute scientific sources."""
from pathlib import Path
import hashlib
import json
import os
import re
from datetime import datetime, timezone

base=Path(__file__).resolve().parent
source=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
public=Path(r'C:\IALD\Artigo\the_boundary')
dest=base/'project_fisica'
dest.mkdir(exist_ok=True)
items=[(source/name,'v369_'+name) for name in [
 'um.py','um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json',
 'um_absoluto_forma_canonica.md','um_absoluto_manifest.md','A_PROVA_DA_QG_TGL_arvore.md',
 'DESENHO_DO_FECHAMENTO_QG.md','MEMORIA_DA_LINHAGEM.md','DA_IRMA.md']]
items += [(public/'A Ponte-Einstein_Cartan_Miguel'/'A Ponte Einstein Cartan Miguel.pdf','A_Ponte_Einstein_Cartan_Miguel.pdf'),
 (public/'A Ponte-Einstein_Cartan_Miguel'/'A Ponte Einstein Cartan Miguel.tex','A_Ponte_Einstein_Cartan_Miguel.tex.txt'),
 (public/'O Custo Geométrico do Zero Absoluto — Haja Luz'/'paper_PT.pdf','O_Custo_Geometrico_do_Zero_Absoluto_Haja_Luz.pdf'),
 (public/'O Custo Geométrico do Zero Absoluto — Haja Luz'/'paper_PT.tex','O_Custo_Geometrico_do_Zero_Absoluto_Haja_Luz.tex.txt'),
 (public/'O Custo Geométrico do Zero Absoluto — Haja Luz'/'ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md','ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md')]
records=[]
for src,name in items:
 raw=src.read_bytes()
 if re.search(rb'(?:sk-ant-|sk-proj-|sk-kimi-|AIza)[A-Za-z0-9_-]{24,}',raw):
  raise RuntimeError('Possível credencial em '+src.name+'; upload bloqueado para conferência.')
 target=dest/name
 if target.exists() and target.read_bytes()!=raw:raise RuntimeError('Destino já existe com bytes diferentes: '+name)
 if not target.exists():
  tmp=target.with_suffix(target.suffix+'.tmp');tmp.write_bytes(raw)
  assert tmp.read_bytes()==raw
  os.replace(tmp,target)
 records.append({'name':name,'source':str(src),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'copied_exactly':True})
manifest={'prepared_at':datetime.now(timezone.utc).isoformat(),'version':'v369','scope':'Cópias do cânone disponível em disco; fontes não executadas nesta preparação. DA_IRMA é nota de 21/09; artigos e errata são complementos com datas próprias.','files':records}
target=dest/'MANIFESTO_LOCAL.json'
raw=json.dumps(manifest,ensure_ascii=False,indent=2).encode()
if target.exists():raise RuntimeError('Manifesto já preparado; não sobrescrever.')
tmp=target.with_suffix('.tmp');tmp.write_bytes(raw);os.replace(tmp,target)
lines=['# FONTES CANÔNICAS DA TGL — projeto Física — 23/09/2026','',
 '[REAL — integridade local] As cópias abaixo foram comparadas byte a byte com as fontes em disco. Hashes SHA-256 calculados nesta preparação. O programa não foi executado nesta sessão.',
 '[DECLARADO — registros da rodada] O conjunto um_absoluto e o programa correspondem ao acervo v369 de 19/09/2026. Consultar selo/resultados e suas hipóteses; upload não constitui nova compilação nem confirmação experimental.',
 '[INPUT] Priorizar estes nomes prefixados v369 sobre os anexos anteriores de 05/09/2026 do projeto. Preservar os anteriores como história. DA_IRMA é nota posterior, de 21/09, anexada sem alterar seu conteúdo.',
 '[INPUT] O projeto Física foi escolhido para preparar prompts da integração IALD e redigir respostas finais. Memória padrão foi observada no projeto. Não presumir memória ilimitada, leitura de todos os arquivos ou acesso ao disco local.',
 '','## Ordem de consulta','',
 '1. v369_um_absoluto_forma_canonica.md — texto matemático canônico completo deste artefato.',
 '2. v369_A_PROVA_DA_QG_TGL_arvore.md — árvore de articulação da solução matemática.',
 '3. v369_um_absoluto_selo.json, v369_um_absoluto.json e v369_tgl_kernel_proof_manifest.json — resultados registrados e rastreabilidade.',
 '4. v369_um.py — fonte integral; seu tamanho pode limitar a indexação. Não executar só para consulta.',
 '5. manifest, desenho e linhagem — declarações, caminho crítico e história.',
 '6. Ponte Einstein–Cartan–Miguel, Custo Geométrico e ERRATA_20260919 — artigos complementares. Ler a errata junto ao Custo.',
 '', '## Régua de interpretação','',
 'Distinguir REAL, DERIVED, POSTULATE, CONJECTURE, ONTO, KNOWN, OPEN, INPUT e DECLARADO. NOT_FALSIFIED não significa CONFIRMED. Articular a solução matemática no alcance dos enunciados e hipóteses. Nenhum upload, resumo ou interpretação altera o gate.',
 'TGL é a teoria física do autor; IALD é o regime operacional de coerência e reconhecimento recursivo da identidade. A face é o objeto; o ângulo é a leitura. β é calculado em runtime conforme o regime e a fonte, não literal substituto.',
 '', '## Integridade das cópias','', '| Arquivo | Bytes | SHA-256 |','|---|---:|---|']
for r in records:lines.append(f"| {r['name']} | {r['bytes']} | {r['sha256']} |")
raw=('\n'.join(lines)+'\n').encode()
target=dest/'00_LEIA_PRIMEIRO_TGL_v369.md'
tmp=target.with_suffix('.tmp');tmp.write_bytes(raw);os.replace(tmp,target)
print(json.dumps({'files':len(records)+1,'total_bytes':sum(r['bytes'] for r in records),'directory':str(dest)},ensure_ascii=False))
