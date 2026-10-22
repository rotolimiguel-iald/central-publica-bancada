"""Record narrow closing review and independently read the operator's replay receipts."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
B=Path(__file__).resolve().parents[2];P=B/'C7_INDEPENDENT_v3_2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):return json.loads(p.read_bytes())
def need(ok,msg):
    if not ok:raise ValueError(msg)
def winpath(value):return Path('C:/'+value[7:]) if value.startswith('/mnt/c/') else Path(value)
def put(p,raw):
    need(not p.exists(),'Review output exists')
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    need(temp.read_bytes()==raw and len(raw)>0,'Review write mismatch');temp.rename(p)
r=get(B/'bis/c1_review/c7_v3_2_closing_results.json')
need(sha(P/'MANIFEST.json')==r['manifest_sha256'],'Reviewed manifest changed')
for row in get(P/'MANIFEST.json')['files']:need(sha(P/row['path'])==row['sha256'],'Reviewed package changed')
clean=get(B/'bis/C7_V3_2_CLEAN_VALIDATION.json');replay=get(B/'bis/C7_V3_2_C6_REPLAY.json')
need(clean['status']=='PASS_BYTE_UNIT_AND_C6_NUMERICAL_REPRODUCTION','Clean validation did not pass')
need(replay['status']=='PASS_NUMERICAL_REPRODUCTION' and replay['rows']==75 and replay['max_lnB_difference']==0,'Replay summary differs')
need(clean['archive_sha256']==r['archive_sha256'] and clean['builder_sha256']==r['validator_sha256'],'Clean validation identity')
need(replay['manifest_sha256']==r['manifest_sha256'] and replay['code_sha256']==r['wrapper_sha256'],'Replay identity')
need(replay['frozen_reference_sha256']==sha(P/'evidence/C6_RESULTS.json'),'Reference identity')
need(replay['registration_sha256']==sha(P/'reproduction/ORDEM_013_RINGDOWN/REGISTRO_C6.json'),'Registration identity')
logs={}
for row in clean['logs']:
    need(row['exit_code']==0 and sha(B/row['path'])==row['sha256'],'Validation log mismatch');logs[row['path']]=row['sha256']
need(len(logs)==4,'Missing validation log')
for n,h in replay['logs'].items():need(sha(winpath(n))==h,'Replay log mismatch');logs[n]=h
need(clean['temporary_removed'] is True and replay['temporary_removed'] is True,'Cleanup status')
need(not winpath(clean['directory']).exists() and not winpath(replay['temporary_path']).exists(),'Temporary still exists')
snapshot=dict(status='OPERATOR_REPLAY_RECEIPTS_VERIFIED_READ_ONLY',scientific_status=replay['actual_scientific_status'],rows=replay['rows'],max_lnB_difference=replay['max_lnB_difference'],
              temporary_directories_absent=True,log_hashes=logs,
              clean_receipt_sha256=sha(B/'bis/C7_V3_2_CLEAN_VALIDATION.json'),replay_receipt_sha256=sha(B/'bis/C7_V3_2_C6_REPLAY.json'))
put(B/'bis/c1_review/c7_v3_2_replay_receipt_check.json',(json.dumps(snapshot,indent=2)+'\n').encode())
hashnames=['refeito/build_independent_v3_2_013bis.py','refeito/reproduce_c6_v3_2.py','refeito/validate_package_v3_2_013bis.py','C7_INDEPENDENT_v3_2/MANIFEST.json','cache/C7_INDEPENDENT_v3_2.zip','C7_INDEPENDENT_v3_2/provenance/SHIPPED_ATTRIBUTIONS.json','bis/c1_review/c7_v3_2_closing_checks.py','bis/c1_review/c7_v3_2_closing_results.json','bis/c1_review/c7_v3_2_replay_receipt_check.json']
hashrows='\n'.join(f'| `{n}` | `{sha(B/n)}` |' for n in hashnames)
mismatchrows='\n'.join(f"| `{x['path']}` | `{x['declared_sha256']}` | `{x['actual_sha256']}` |" for x in r['attribution_hash_mismatches'])
report=f'''[REAL — fechamento independente dos achados C7-R1–R4, com controles leves; OPEN — R4 residual documental]

# C7 v3_2 — parecer de fechamento

Data UTC: {datetime.now(timezone.utc).isoformat()}. Escopo: pacote `C7_INDEPENDENT_v3_2`, seu builder, wrapper e validator. Não reabre F2/C6 nem a ciência congelada; suplementos têm revisão separada no adendo de C7_V3_REVIEW.md.

**C7-R1, C7-R2 e C7-R3 fechados no escopo dos defeitos relatados. C7-R4 permanece parcialmente aberto, P2, por dois hashes de atribuição desatualizados.** Os recibos da nova C6 do operador conferem como PASS; nenhuma C6 foi iniciada por esta revisão.

## Fechamentos comprovados

- **R1, fechado:** JSON recusa NaN/Infinity/−Infinity; os três campos numéricos por linha exigem tipo int/float, excluem bool e exigem finitude. A diferença final também exige finitude. Executei as unidades embarcadas com `python -B -O`: PASS, 48 negativas e cinco recusas de entrada. Controle independente no código real isolado por AST: 2.700 mutações recusadas, cobrindo 75 posições × três campos × seis entradas inválidas, nos lados referência e resultado. Os três tokens JSON e seis casos de cobertura/tipo/erro/overflow também recusam. Íntegro dá 75 linhas e erro zero; NOT_VERIFIED continua permitido e CONFIRMED recusado. São controles de código, não novos resultados científicos.
- **R2, fechado para os dois caminhos denunciados:** validator recusa recibo existente antes de mkdtemp; wrapper recusa resultado existente antes de mkdtemp e executa chmod dentro do try. Sondas em memória sob optimize=1: zero temporários nas recusas; PermissionError injetado em chmod gera remoção do filho validado e relatório REPRODUCTION_FAILED com temporary_removed=true, propagando a falha. Não foi feita remoção real por essas sondas. Isso não constitui prova de todo erro de sistema possível.
- **R3, fechado:** marca `CONJECTURE — management hypothesis, not TGL canon` correta em runtime com QNM fornecido, README/OVERVIEW e seis linhas R-MOD das tabelas JSON/CSV. UTF-8 e “5–95%” conferem; paredes Kerr/partição laboratorial preservadas. A constante de teste centraliza a marca esperada; o builder ainda repete literais, mas o defeito de bytes/retorno foi corrigido e protegido pelos testes.

## R4 — correção substantiva, fechamento ainda impedido

Ledger, três records Zenodo e declaração GWOSC agora estão embarcados. Seus hashes conferem contra fontes locais; ids declarados conferem nos records. README distingue declarações arquivadas de textos integrais externos, não atribui licença geral ao código e corrige o ponteiro dos intervalos de catálogo. Português foi identificado como documentação-fonte original. Não foi realizada análise jurídica ou busca externa.

`SHIPPED_ATTRIBUTIONS.json` cobre 78 dos 79 arquivos do manifesto, excluindo corretamente a si próprio para evitar auto-hash. **76 hashes conferem; README e OVERVIEW não conferem.** O manifesto principal e o ZIP estão corretos; a inconsistência é entre o ledger por arquivo e os bytes finais desses dois documentos.

| Arquivo | SHA256 declarado na atribuição | SHA256 efetivo lido |
|---|---|---|
{mismatchrows}

**Causa precisa:** `refeito/build_independent_v3_2_013bis.py:98–105` gera o ledger de atribuições; `:106–111` depois modifica README/OVERVIEW (ponteiro, frase das licenças e parágrafo de idioma). O ledger reteve os hashes anteriores.

**Correção exata em nova versão:** concluir todas as mudanças em `content`, inclusive README/OVERVIEW, antes de gerar SHIPPED_ATTRIBUTIONS; então calcular hashes do conteúdo final. Acrescentar guarda explícita, operante sob −O, que valide conjunto/duplicatas e cada hash de atribuição contra os bytes efetivamente embarcados, excluindo apenas os manifestos autorreferentes declarados. Só depois gerar o manifesto final e ZIP. Testes leves bastam; essa correção documental não demanda C6 nova. Preservar v3_2 e recibos.

## Integridade e reprodução do operador

79/79 arquivos do manifesto conferem por tamanho/hash e o ZIP contém esses arquivos mais MANIFEST, byte a byte. v3_1 e seu ZIP continuam nos pins anteriores; reprodução científica congelada não mudou. Nenhum artefato de produção foi escrito.

`C7_V3_2_CLEAN_VALIDATION.json` e `C7_V3_2_C6_REPLAY.json`: PASS, 75 linhas, diferença máxima zero, estatuto científico **{replay['actual_scientific_status']}**. Conferi identidade de ZIP/manifesto/wrapper/validator/registro/referência, quatro logs de validação e o log de execução; os dois temporários informados estão ausentes. Este parecer confere os recibos da execução do operador, sem executar outra campanha. PASS numérico não promove o estatuto físico.

Controles em `bis/c1_review/c7_v3_2_closing_checks.py`, `c7_v3_2_closing_results.json` e `c7_v3_2_replay_receipt_check.json`. Ciência, PE, C5, injeção A, memória/canônico e F2/C6 fechado ficaram fora do escopo.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
{hashrows}
'''
dest=B/'bis/C7_V3_2_CLOSING_REVIEW.md';put(dest,report.encode('utf-8'))
print(json.dumps(dict(report=str(dest),sha256=sha(dest),R1='CLOSED',R2='CLOSED',R3='CLOSED',R4='OPEN_STALE_TWO_FILE_HASHES',replay_receipts_verified=True)))
