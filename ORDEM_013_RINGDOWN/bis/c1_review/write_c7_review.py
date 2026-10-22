"""Finalize the lateral package review; consume user replay receipts read-only."""
import json,hashlib,math
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=R/'C7_INDEPENDENT_v3_1'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def get(p):return json.loads(p.read_bytes())
def need(ok,msg):
    if not ok:raise ValueError(msg)
def put(p,raw):
    need(not p.exists(),'Output exists');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    need(t.read_bytes()==raw and len(raw)>0,'Write differs');need(not p.exists(),'Output appeared');t.rename(p)
def from_wsl(value):
    if value.startswith('/mnt/c/'):return Path('C:/'+value[len('/mnt/c/'):])
    return Path(value)
p=R/'bis/C7_V3_REVIEW.md';receipt=R/'bis/c1_review/c7_replay_receipt_check.json';need(not p.exists() and not receipt.exists(),'Output exists')
r=get(R/'bis/c1_review/c7_v3_results.json')
for n,h in r['input_hashes'].items():need(sha(R/n)==h,'Audited input changed: '+n)
for name,m in r['manifests'].items():
    need(sha(R/name/'MANIFEST.json')==m['manifest_sha256'],'Manifest changed')
    for row in get(R/name/'MANIFEST.json')['files']:need(sha(R/name/row['path'])==row['sha256'],'Package file changed')
clean=get(R/'bis/C7_V3_1_CLEAN_VALIDATION.json');replay=get(R/'bis/C7_V3_1_C6_REPLAY.json')
need(clean['archive_sha256']==r['manifests']['C7_INDEPENDENT_v3_1']['archive_sha256'],'Replay archive mismatch')
need(clean['builder_sha256']==sha(R/'refeito/validate_package_v3_013bis.py'),'Replay validator mismatch')
logs={}
for row in clean['logs']:
    path=R/row['path'];need(sha(path)==row['sha256'],'Validation log hash mismatch');need(row['exit_code']==0,'Validation failed');logs[row['path']]=sha(path)
for name,h in replay['logs'].items():need(sha(from_wsl(name))==h,'Replay log hash mismatch');logs[name]=h
need(replay['manifest_sha256']==sha(P/'MANIFEST.json') and replay['code_sha256']==sha(P/'reproduce_c6.py'),'Replay package identity')
need(replay['frozen_reference_sha256']==sha(P/'evidence/C6_RESULTS.json'),'Replay frozen reference')
need(replay['registration_sha256']==sha(P/'reproduction/ORDEM_013_RINGDOWN/REGISTRO_C6.json'),'Replay registration')
need(replay['rows']==75 and replay['max_lnB_difference']==0 and math.isfinite(replay['max_lnB_difference']),'Replay summary differs')
need(not from_wsl(clean['directory']).exists() and not from_wsl(replay['temporary_path']).exists(),'Reported temporary remains')
filelist=get(P/'MANIFEST.json')['files'];license_mentions=[];large=[]
for row in filelist:
    if row['bytes']>25_000_000:large.append(row['path'])
    if Path(row['path']).suffix in ('.md','.json','.txt'):
        text=(P/row['path']).read_text(encoding='utf-8').lower()
        if any(term in text for term in ('license','licence','licença')):license_mentions.append(row['path'])
snap=dict(utc=datetime.now(timezone.utc).isoformat(),status='USER_REPLAY_RECEIPTS_VERIFIED_READ_ONLY',replay_status=replay['status'],scientific_status=replay['actual_scientific_status'],rows=75,max_lnB_difference=0.0,
          cleanup_directories_absent=True,log_hashes=logs,clean_receipt_sha256=sha(R/'bis/C7_V3_1_CLEAN_VALIDATION.json'),replay_receipt_sha256=sha(R/'bis/C7_V3_1_C6_REPLAY.json'),
          license_mentions_in_manifest_text_files=license_mentions,package_files_over_25MB=large,script_sha256=sha(Path(__file__)))
put(receipt,(json.dumps(snap,ensure_ascii=False,indent=2)+'\n').encode())
paths=['refeito/build_independent_v3_1_013bis.py','refeito/reproduce_c6_v3.py','refeito/validate_package_v3_013bis.py','C7_INDEPENDENT_v3_1/MANIFEST.json','cache/C7_INDEPENDENT_v3_1.zip','C7_INDEPENDENT_v3/MANIFEST.json','cache/C7_INDEPENDENT_v3.zip','bis/C7_V3_1_C6_REPLAY.json','bis/C7_V3_1_CLEAN_VALIDATION.json','bis/c1_review/c7_v3_checks.py','bis/c1_review/c7_v3_results.json','bis/c1_review/c7_replay_receipt_check.json']
hashes='\n'.join(f'| `{n}` | `{sha(R/n)}` |' for n in paths)
text=f'''[REAL — revisão lateral F6/F7; replay do operador conferido por recibos; OPEN — guardas, limpeza e documentação]

# Revisão C7 v3_1

Data UTC: {snap['utc']}. Raiz: `C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN`. O pacote efetivo está em `C7_INDEPENDENT_v3_1/`; B é a variável de raiz nos construtores, não uma subpasta existente.

**Parecer: reprodução ordinária registrada como PASS, mas pacote ainda não aprovado sem ressalvas.** A comparação numérica aceita silenciosamente NaN em uma posição não inicial; há uma falha de limpeza antes do try; a marca Unicode exata de R-MOD continua corrompida. O README também promete rastreabilidade de licenças que não está embarcada no manifesto. Os achados F2/C6 encerrados não foram reabertos.

## O que confere

- 73/73 arquivos de cada manifesto v3 e v3_1 conferem por tamanho/hash. Os dois ZIPs contêm exatamente os 73 arquivos mais MANIFEST, com bytes idênticos às pastas. A v3 anterior está preservada. Da v3 para v3_1 mudaram apenas README, OVERVIEW, reading_scope.json/csv e o módulo público de predição; a árvore congelada reproduction permanece idêntica.
- A tabela possui dez leituras × seis conjuntos, 60 chaves únicas. Números, estatutos, nulls, vereditos condicionais, contexto de sigma/z e marcas analíticas conferem com F2 fechado. Os campos novos C1_scope, EXCLUDED_IF_UNIVERSAL e C6_pre_lnB conferem com as fontes hasheadas. CSV conserva a projeção de todos os campos, sem promover zeros analíticos a medições.
- Fixture é exatamente per_series[2] do arquivo declarado, com hash correto. Executei apenas `python -B -O unit_checks.py` do pacote com o Python bundled: PASS, cinco recusas de entrada; regressões A/B com erros relativos 3,951998679763808e−16 e 3,4760409478204096e−16. Conversão exata da taxa, a=0/a=1 e onset passam. Não houve replay C6 por esta revisão.
- O wrapper recusa output dentro do pacote e resultado preexistente, usa temporário filho do work-root resolvido, verifica hashes do strain antes/depois da cópia e recusa grids/resultados C6 previamente presentes na área de execução. O finally normal confere o alvo como descendente próprio antes de removê-lo; não houve exclusão real na sonda adversarial.
- Downgrade não é token fixo: a sonda aceita NOT_VERIFIED e os estados inconclusivos previstos e recusa CONFIRMED, EXCLUDED_IN_READING, PASS e string vazia. Falta/duplicata de linha e erro finito 0,1 são recusados. A aprovação numérica permanece distinta do estatuto físico.
- README/OVERVIEW têm escopo 220/440, ensemble versus realização OPEN, paredes Kerr/laboratório, contraste entre gerador positivo-raiz e postulado modular, tensão R-RAIZ-0, BCW/exato, perfis de constantes, delta_tau_linear legado, onset/fase/overtones, Occam e aviso MAX_PATH. São correções substantivas presentes; os defeitos editoriais abaixo não apagam isso.

**Execução iniciada pelo operador (session49378):** ao fim desta revisão existiam C7_V3_1_CLEAN_VALIDATION.json e C7_V3_1_C6_REPLAY.json, com PASS_BYTE_UNIT_AND_C6_NUMERICAL_REPRODUCTION e PASS_NUMERICAL_REPRODUCTION, 75 linhas, diferença máxima 0, estatuto científico INCONCLUSIVE_SYSTEMATICS. Conferi hashes do ZIP, manifesto, wrapper, registro, referência congelada e cinco logs; os dois diretórios temporários informados já não existem. É conferência independente dos recibos dessa execução, não uma segunda execução minha. O defeito de NaN é demonstrado por mutação, não detectado nesse replay ordinário.

## Achados e correções exatas

**C7-R1 — P1, falso aceite de não finito.** Em `refeito/reproduce_c6_v3.py:67`, max(abs(actual−reference)) seguido de `error > 1e-5` não recusa NaN. Isolei o bloco real por AST sob optimize=1 e alterei apenas lnB_vs_GR da segunda linha para NaN: a guarda aceitou com max_error=0,0. O relatório resumido pode ser serializado com allow_nan=False porque o NaN ficou apenas na entrada, não no resumo; essa opção de escrita não corrige a falha.

Correção: leitura JSON estrita com rejeição de NaN/Infinity e validação explícita de finitude/tipo de todos os números comparados (incluindo chaves numéricas) antes de diferenças/max. Manter cobertura e unicidade e validar também finitude do erro final. Usar ValueError explícito, operante sob −O. Aceitação: NaN/±Infinity em qualquer posição devem recusar; amostra íntegra e downgrade legítimo devem continuar passando. Não exige nova ciência para testar a guarda.

**C7-R2 — P2, limpeza não cobre toda criação.** `validate_package_v3_013bis.py:9` cria o temporário; `:12` pode lançar FileExistsError por recibo já existente; o try/finally só começa em `:15`. Simulei esse caminho com objetos em memória: um diretório criado, zero remoções. É falha reproduzível ao tentar validar novamente com recibo existente. No wrapper há a mesma janela estrutural: chmod em `reproduce_c6_v3.py:43` fica depois da criação e antes do try.

Correção: verificar saídas já existentes antes de mkdtemp e colocar todo o ciclo após a criação (incluindo chmod/preparação/hash suscetível a erro) sob finally, preservando a validação do alvo descendente resolvido. Não resolver com remoção ampla do work-root. Testar falhas logo após criação e nas precondições sem tocar diretórios reais da campanha. A remoção no caminho ordinário do replay atual confere; a promessa “incluindo falhas” ainda não vale para esses caminhos.

**C7-R3 — P2 editorial, string exata de R-MOD.** A atribuição a scope existe agora em `tgl_ringdown_prediction.py:119` e contém as palavras e duas paredes requeridas. Contudo, o separador é a sequência Unicode U+00E2/U+20AC/U+201D, não o travessão U+2014. O teste literal `CONJECTURE — management hypothesis, not TGL canon` falha no scope, README, OVERVIEW e nas seis linhas R-MOD. Há também corrupção em “5–95%”. Isso foi conferido por codepoints, não pela aparência do terminal.

Correção em novo builder/pacote: gerar texto UTF-8 correto (pode usar escape Python `\\u2014` para a constante), centralizar a marca e testá-la integralmente nas quatro superfícies; manter as paredes completas no scope/README. Testar o valor retornado para R-MOD com QNM fornecido, além da recusa sem QNM. Não editar os arquivos/manifests deste pacote selado para corrigir a codificação.

**C7-R4 — P2 documental, licença afirmada sem recibo embarcado.** README:49 afirma que cada licença upstream foi preservada separadamente e que recibos identificam os releases. No universo de 73 arquivos do manifesto, somente README e OVERVIEW contêm menção a licença; não há manifesto/recibo de licenças por arquivo nem textos de licença embarcados. A lista narrativa de quatro releases não é o vínculo de proveniência exigido em F7.

Correção: incluir na próxima versão o recorte verificável do manifesto de downloads/atribuições aplicável ao bundle, vinculando caminhos/hashes embarcados à origem e à licença documentada, sem inferir licença para o código de pesquisa. Preservar textos upstream aplicáveis ou declarar precisamente o que é somente referência externa. Até lá, reformular a frase para não afirmar preservação dentro do pacote. Não foi feita análise jurídica nem nova consulta aos provedores nesta revisão; o achado é a ausência da evidência documental prometida.

**Ajustes menores do README:** os intervalos por evento do catálogo estão em `evidence/C4_CATALOG_220.json`, não no agregado de `current_evidence/F2_ALL_READING_TABLES_v2.json`; corrigir o ponteiro da linha 11. A entrada é inglesa, mas current_evidence ainda contém quatro adendos Markdown em português: se o critério “bundle em inglês” for literal para toda documentação corrente, falta versão inglesa ao lado; preservar os originais como fontes históricas. Nenhuma leitura deve virar preferida nessa edição.

## Limites, reprodução e integridade

O foco foi o pacote e os três construtores pedidos. Não auditei novamente ciência F2/C6, calibração C5, nem a limpeza de todas as outras pastas C7 da casa. Não há arquivo >25 MB entre os 73 membros examinados; isso não quita sozinho o critério global F7. A aceitação em extração limpa tem o recibo lido acima; pasta profunda não foi testada, estando pago apenas o aviso MAX_PATH permitido pela ordem.

Controle próprio: `bis/c1_review/c7_v3_checks.py`, executado com Python bundled `-B -O`; hashes/ZIP/tabela/fixture, unidades leves e sondas AST/mock sem subprocesso C6. Resultado em c7_v3_results.json. Conferência dos recibos da execução do operador: c7_replay_receipt_check.json. Nenhum pacote, manifesto ou produção foi escrito; nenhuma C6 concorrente foi criada, interrompida ou aguardada por ferramenta. Axiomas: N/A — sem Lean. Repetir controles em cópia isolada, pois as saídas recusam sobrescrita.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
{hashes}
'''
put(p,text.encode('utf-8'))
print(json.dumps(dict(report=str(p),sha256=sha(p),user_replay_receipts_verified=True,bytes=p.stat().st_size)))
