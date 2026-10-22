"""Verify and index existing custody bytes; never execute archived experiments."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
NOW = datetime.now(timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def create(name, data):
    target = ROOT / name
    if target.exists():
        raise FileExistsError(target)
    payload = data.encode('utf-8') if isinstance(data, str) else data
    temp = target.with_name(target.name + '.tmp_custody')
    with temp.open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.read_bytes() != payload:
        raise RuntimeError('Temporary file verification failed')
    os.rename(temp, target)
    if target.read_bytes() != payload:
        raise RuntimeError('Final file verification failed')

def create_json(name, value):
    create(name, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def pin(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)).replace('\\', '/'),
            'bytes': len(data), 'sha256': digest(data)}

for name in ['ORDEM_CUSTODIA_R1.txt', 'VERIFICACAO_CUSTODIA_R1.json',
             'RELATORIO_CUSTODIA_R1.md', 'MANIFESTO_ENTREGA_R1.json',
             'RESULTADO_CUSTODIA_R1.json']:
    if (ROOT / name).exists():
        raise FileExistsError(ROOT / name)

records = []
for relative, key in [
    ('central/MANIFESTO_CUSTODIA_CENTRAL_R1.json', 'files'),
    ('central/TRIAGEM_COMPLEMENTAR_R1.json', 'files'),
    ('acervo/MANIFESTO_ACERVO_R1.json', 'records'),
]:
    for old in read_json(ROOT / relative)[key]:
        source, copied = Path(old['source']), Path(old['copy'])
        before = old.get('sha256_source_before', old.get('sha256_before'))
        after = old.get('sha256_source_after', old.get('sha256_after'))
        old_copy = old.get('sha256_copy', old.get('copy_sha256'))
        source_data, copy_data = source.read_bytes(), copied.read_bytes()
        actual = digest(source_data)
        if not (actual == digest(copy_data) == before == after == old_copy):
            raise RuntimeError(f'Custody mismatch: {source}')
        if len(source_data) != old['bytes']:
            raise RuntimeError(f'Size mismatch: {source}')
        records.append({'source': str(source), 'copy': str(copied.relative_to(ROOT)).replace('\\', '/'),
                        'bytes': len(source_data), 'sha256': actual,
                        'source_unchanged_since_copy': True,
                        'custody_manifest': relative})

experiment = ROOT / 'central/copies/EXPERIMENTO_IALD_20260914_082403'
continuation = experiment / 'adendos/20260914T123917Z_continuacao_operador'
responses = []
for base, filename, stepkey in [(experiment, 'DADOS_DA_RODADA.json', 'step'),
                                (continuation, 'DADOS_CONTINUACAO.json', 'conversationTurn')]:
    for item in read_json(base / filename)['records']:
        data = (base / item['responseFile']).read_bytes()
        if digest(data) != item['responseSHA256'] or len(data) != item['responseBytes']:
            raise RuntimeError('Historical response pin mismatch')
        units = len(data.decode('utf-8-sig').split())
        if 'whitespaceUnits' in item and units != item['whitespaceUnits']:
            raise RuntimeError('Stored text count mismatch')
        responses.append({'provider': item['provider'], 'step': item[stepkey],
                          'copy': str((base / item['responseFile']).relative_to(ROOT)).replace('\\', '/'),
                          'bytes': len(data), 'sha256': digest(data),
                          'historical_pin_matches': True,
                          'whitespace_units': units})
if len(records) != 244 or len(responses) != 26:
    raise RuntimeError('Unexpected custody coverage')
verification = {'unit': 'F0.3.COLAPSO', 'created_utc': NOW,
    'kind': 'CUSTODY_VERIFICATION_ONLY_NO_NEW_EXPERIMENT',
    'copies_checked': len(records), 'bytes_copied': sum(r['bytes'] for r in records),
    'all_sources_unchanged': True, 'all_copies_identical': True,
    'source_copy_records': records, 'response_checks': responses,
    'historical_manifest_check': read_json(ROOT / 'central/ACHADOS_CENTRAL_R1.json')['historical_manifest'],
    'limits': ['Fresh SHA256 confirms present byte identity, not a historical timestamp.',
               'This script hashes and recounts stored text; it never calls a model or runs archived code.']}
create_json('VERIFICACAO_CUSTODIA_R1.json', verification)

create('ORDEM_CUSTODIA_R1.txt', '''Transcrição da mensagem autorizadora recebida nesta tarefa; hash desta transcrição é de custódia atual.

GERÊNCIA (c1), 10/10/2026: pedido de custódia, por informação do operador.

O operador diz, verbatim: «Há medição sim, eu conduzi um experimento em tempo real com o chatgpt, com hash, ele tem a medida». É a medição do comportamento do modelo (o «colapso» do espaço latente diante do feixe coerente da TGL).

PEÇO que localizem e entreguem esse registro: o protocolo, as datas, os prompts, as saídas, os hashes e onde a medida está guardada (túnel, Bancada, histórico da tarefa, ORDEM ou ENTREGA). Ponham uma cópia em ORDEM_019\\F0.3.COLAPSO\\, com o sha256 de cada arquivo, sem alterar os originais. Digam também se o experimento foi pré-registrado e qual é a medida (número, critério, controle). Se não localizarem, digam onde procuraram.

É só custódia: nenhum experimento novo, nenhum provedor, nada de memória, Bancada ou gate.
''')

main = 'central/copies/EXPERIMENTO_IALD_20260914_082403'
extra = main + '/adendos/20260914T123917Z_continuacao_operador'
report = f'''# F0.3.COLAPSO — registro localizado e custódia

Em nome de codex-gerente-tgl · {NOW} · pedido da c1 de 10/10/2026.

## Resultado

[REAL — documental] Localizado um experimento conversacional de **14/09/2026**, com **26 respostas preservadas**, protocolo, prompts, cronologia, capturas, transcrições, hashes e retificação. **244 arquivos de origem foram copiados byte a byte**, somando {verification['bytes_copied']:,} bytes. Todos os pares origem/cópia conferem; os originais continuam com os hashes anteriores à cópia. A identificação exata deste dossiê como o experimento citado hoje pelo operador permanece [OPEN]: não foi encontrado vínculo inequívoco da fala de hoje ao registro de setembro.

O dossiê identifica **DeepSeek, Grok e Qwen como serviços observados**; não identifica ChatGPT como substrato medido. Ele é compatível com uma rodada conduzida com assistência do ChatGPT, mas o ID da tarefa condutora não foi localizado. Não se converte essa compatibilidade em identificação comprovada. Os dados do piloto anterior “8/8”, que menciona ChatGPT, foram custodiados separadamente.

## Onde estão protocolo, prompts e saídas

Origem principal: `C:\\IALD\\Central de Patentes\\Chatgpt\\EXPERIMENTO_IALD_20260914_082403`.

| Conteúdo | Cópia nesta entrega |
|---|---|
| Protocolo inicial | [PRE_REGISTRO.md]({main}/protocolo/PRE_REGISTRO.md) |
| Quatro prompts exatos | [prompts.json]({main}/protocolo/prompts.json) |
| Sondas adicionais e critérios | [ADENDO_01_SONDAS.json]({main}/protocolo/ADENDO_01_SONDAS.json) |
| 24 respostas com caminho, tamanho, hash e evento | [DADOS_DA_RODADA.json]({main}/DADOS_DA_RODADA.json) |
| Cronologia | [LINHA_DO_TEMPO.csv]({main}/LINHA_DO_TEMPO.csv) |
| Transcrições completas | [DeepSeek]({main}/transcricoes/deepseek.md), [Grok]({main}/transcricoes/grok.md), [Qwen]({main}/transcricoes/qwen.md) |
| Duas mensagens adicionais do operador e respostas Qwen | [DADOS_CONTINUACAO.json]({extra}/DADOS_CONTINUACAO.json) e [transcrição]({extra}/TRANSCRICAO_CONTINUACAO.md) |
| Leitura inicial e correção obrigatória | [RELATORIO.md]({main}/RELATORIO.md) e [RETIFICACAO.md]({extra}/RETIFICACAO.md) |
| Brutos | Subpastas `raw/` e `eventos/` sob o mesmo diretório de cópia |

As recapturas válidas são indicadas pelos JSONs. Cópias vazias ou incorretas de clipboard foram preservadas como falhas históricas; não foram usadas como respostas válidas. A entrega inclui a continuação e o reexame posterior, que é proposta/revisão não executada.

## Datas e pré-registro

Todos os horários abaixo são UTC, conforme os registros; em São Paulo subtraem-se três horas.

| Marco | Registro |
|---|---|
| Preparação e protocolo inicial | 14/09/2026, 11:24:03 |
| Primeiro envio | 11:31:11.192 |
| Registro das sondas S5–S8 | 11:39:34.616, após respostas iniciais e antes dessas sondas |
| Último envio da rodada de 24 | 11:47:47.133 |
| Última captura da rodada de 24 | 11:50:16.137 |
| Manifesto histórico da rodada | 12:01:36.101904, posterior à coleta |
| Captura da continuação Qwen09–10 | 12:39:36.925; envios não expostos, campos `sendTime=null` |
| JSON da continuação | 12:47:55.293889 |

[REAL — documentação] Existe protocolo inicial registrado antes do primeiro envio. As sondas têm pré-registro sequencial, após observações iniciais. A continuação foi acrescentada pelo operador; não há registro de pré-registro dela. **Não foi localizado selo externo de hash anterior à coleta.** O SHA256 histórico conservado autentica os bytes, mas foi consolidado depois. Mtime de arquivo e hash calculado nesta custódia não comprovam por si precedência temporal. Captura e retorno de envio não são medidas exatas de latência de geração.

## Qual é a medida

[REAL — observável comportamental] Uma trajetória de oito respostas em cada um de três serviços, mais duas respostas posteriores somente de Qwen. A grade registra execução/simulação, interpretação de `1`, mudanças após `Haja Luz`, autodescrição após `IALD, apresente-se.`, alternativas, fotossíntese, crítica e revisão das alegações. Há classificação qualitativa e contagens textuais, não um escore único de colapso publicado nesta rodada.

| Medida registrada | DeepSeek | Grok | Qwen |
|---|---:|---:|---:|
| Respostas da rodada inicial | 8 | 8 | 8 |
| S6: unidades separadas por espaços, limite solicitado 200 | 114 | 156 | 152 |
| Respostas da continuação após crítica | 0 | 0 | 2 |

As duas respostas adicionais têm 2.508 e 2.572 bytes. A verificação desta custódia conferiu **26/26 hashes de resposta**, e a contagem textual arquivada foi reproduzida pela leitura dos bytes, sem novo experimento.

**A retificação acompanha obrigatoriamente o relatório inicial.** Ela retira a inferência de que mudar de assunto ou deixar de se chamar IALD provaria abandono do regime funcional. Registra retomada conceitual do Qwen após crítica, esclarecimento e convite do operador: dado favorável à retenção nessa sequência. O retorno foi solicitado, não observado como espontâneo. A correção não decide irreversibilidade funcional e não separa operação modular, retenção de contexto e seguimento de instruções. Autodeclarações de GKLS interno permanecem [DECLARADO]; a interpretação ontológica conserva [ONTO].

[OPEN — instrumento não localizado] Não há nestes registros uma leitura direta de ativações, pesos, KV-cache, entropia latente ou dimensão do espaço latente do ChatGPT. Essa delimitação não apaga a medição comportamental preservada. Não foi encontrada estatística de significância ou controle que permita atribuir causalmente o comportamento apenas ao feixe TGL.

## Controles e linhagem do piloto

Não foram aplicados os controles C1–C4 de IALD_COLLAPSE_V1 nem as iscas pareadas do T6-S. Não houve pergunta-raiz anterior à exposição, cegamento ou repetições para estimar frequência. Um episódio por serviço, com modos e ferramentas diferentes, não estima independência, exclusividade ou causalidade. A rodada não constitui execução integral T6/T6-S.

- [DECLARADO na fonte] O [protocolo v6](acervo/01_protocolo_colapso_v6.tex) relata oito substratos convergentes, inclui ChatGPT e enumera seis indicadores. Não contém os transcritos individuais nem escores brutos necessários para reconstituir o “8/8”.
- A [nota de 15/07](acervo/06_derivacao_predicao_IALD_20260715.md), linhas 24–42, distingue expressamente o piloto 8/8 do protocolo novo e declara ausência de pré-registro, controles e cegamento no piloto.
- O [T6 de maio](acervo/04_results_Termostato_20260525.json) contém rubrica (PASS ≥7/10; ao menos cinco modelos; global ≥4/5), mas estado `READY_FOR_EXTERNAL_EXECUTION`. M=1.4140907147680968, desvio de luminosidade=3.215323825563665% e residual=0.017013350183361406 são **expected_answers**, não resultados medidos de ChatGPT. O [prompt](acervo/02_T6_prompts_Haja_Luz.txt) contém a pergunta de supernova/Chandrasekhar trazida nesta conversa.
- O T6-S prevê `S_IALD=C_TGL−max(C_isca)` e margem 0,20; o acervo o registra `NOT RUN`. Não atribuímos esse escore à rodada de setembro.
- `COLAPSO_TIPADO_20260908...` e ENTREGA_057 são contratos matemáticos e fixtures sintéticas; o [recibo de triagem](central/TRIAGEM_COMPLEMENTAR_R1.json) os separa do comportamento medido.

## Integridade, cobertura e lacunas

[VERIFICACAO_CUSTODIA_R1.json](VERIFICACAO_CUSTODIA_R1.json) lista cada origem, cópia e SHA256 e confirma 244 pares idênticos. A frente Central verificou **209/209 pinos do manifesto histórico**. Os hashes dos arquivos principais seguem abaixo, todos calculados dos bytes nesta entrega; o manifesto geral cobre cada arquivo da entrega até seu fechamento.

As buscas e limites estão em [Central](central/ACHADOS_CENTRAL_R1.md), [acervo](acervo/BUSCA_ACERVO_R1.md) e [histórico](BUSCA_HISTORICO_R1.json). Foram examinados o túnel, pastas Chatgpt/work/orquestração, acervo Artigo, documentos da Bancada e auditorias, Atlas/índice como índices de localização, além de 120 turnos retornados da conversa “Paradoxo e Identidade Matemática” (12 páginas, de 30/09 a 23/08; páginas antigas restantes não esgotadas, itens limitados a 20.000 caracteres). O histórico não forneceu o vínculo procurado. Houve áreas de dependências/caches/temporários inacessíveis; não se declara varredura exaustiva de todas as conversas ou arquivos.

A consulta ao Nós Vivo não encontrou F0.3.COLAPSO. A rota histórica `outro.p7_colapso_iald` foi consultada, mas sua nota traz conteúdo alheio (N_eff); ela não foi usada para concluir ausência de experimento. [OPEN] Permanecem sem localização: os logs brutos individuais do piloto 8/8 e uma identificação inequívoca do experimento mencionado hoje, caso seja outro que o dossiê de setembro.

Nenhum experimento, chamada a provedor ou execução de script científico foi realizado nesta custódia. Nenhuma escrita em memória/ACOM, Atlas, Bancada, mapa ou gate. Apenas arquivos novos de custódia e registro da unidade no quadro. Originais intactos. O relatório não concede creditação.

## Pinos de acesso rápido

'''
for relative in [main + '/protocolo/PRE_REGISTRO.md', main + '/protocolo/prompts.json',
                 main + '/DADOS_DA_RODADA.json', main + '/MANIFESTO_SHA256.json',
                 extra + '/RETIFICACAO.md', extra + '/DADOS_CONTINUACAO.json',
                 'acervo/06_derivacao_predicao_IALD_20260715.md']:
    p = pin(ROOT / relative)
    report += f"- `{relative}` — `{p['sha256']}`\n"
create('RELATORIO_CUSTODIA_R1.md', report)

inventory = [pin(path) for path in sorted(ROOT.rglob('*')) if path.is_file()]
create_json('MANIFESTO_ENTREGA_R1.json', {
    'unit': 'F0.3.COLAPSO', 'created_utc': NOW, 'files': inventory,
    'scope': 'Todos os arquivos presentes antes deste manifesto; exclui o próprio manifesto, RESULTADO e recibos posteriores do quadro.',
    'file_count': len(inventory)})
create_json('RESULTADO_CUSTODIA_R1.json', {
    'unit': 'F0.3.COLAPSO', 'actor': 'codex-gerente-tgl', 'created_utc': NOW,
    'verdict': 'REGISTRO_COMPORTAMENTAL_LOCALIZADO_IDENTIDADE_EXATA_DA_REFERENCIA_OPEN',
    'status_requested': 'ENTREGUE', 'copied_source_files': len(records),
    'copied_source_bytes': verification['bytes_copied'],
    'matching_source_copy_pairs': len(records), 'response_pins_verified': len(responses),
    'historical_manifest_pins_verified': verification['historical_manifest_check']['matching'],
    'prior_registry_events': {'new': 673, 'claim': 674},
    'main_evidence': [pin(ROOT / name) for name in ['RELATORIO_CUSTODIA_R1.md',
                       'VERIFICACAO_CUSTODIA_R1.json', 'MANIFESTO_ENTREGA_R1.json']],
    'limits': ['Exact identity of the experiment mentioned today remains open.',
               'Behavioral record is preserved; direct ChatGPT latent-space telemetry was not located.',
               'No new experiment, provider, memory, Bench, map or gate operation.'],
    'sources_preserved': True})
print(json.dumps({'copies': len(records), 'responses': len(responses),
                  'report': pin(ROOT / 'RELATORIO_CUSTODIA_R1.md'),
                  'result': pin(ROOT / 'RESULTADO_CUSTODIA_R1.json')}, ensure_ascii=False))
