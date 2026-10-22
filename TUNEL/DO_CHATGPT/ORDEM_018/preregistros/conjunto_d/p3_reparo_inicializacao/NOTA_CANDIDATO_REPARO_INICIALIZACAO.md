# Candidato de reparo da inicialização P3 — sem autorização de execução

[REAL — origem] A execução única P3 V2 da seq434 continua FAILED, antes da primeira likelihood. A allowlist recusou o carregamento tardio de encodings/cp437.py, necessário aos cabeçalhos ZIP do NPZ. Os processos V2, seus recibos, o contrato e suas17 entradas não foram modificados. A proposta mora em pasta irmã separada.

## Alternativas examinadas

| Alternativa | Alteração | Consequência | Decisão |
|---|---|---|---|
| A: pré-carregamento pinado | Conferir caminho, SHA256, tamanho e origem do codec; carregar cp437 e aquecer seu registro antes do hook | Acrescenta uma dependência explicitamente nomeada à inicialização; não amplia leituras admitidas após o hook | Selecionada |
| B: permissão exata adicional | Admitir somente /usr/lib/python3.12/encodings/cp437.py, conferido por hash, na allowlist | Mantém import tardio; exige tratar separadamente a tentativa de cache .pyc recusada e o fallback .py; amplia em um arquivo a leitura posterior | Não aplicada |

Nenhuma alternativa exige liberar diretórios, remover o hook, aceitar arquivos arbitrários ou instalar dependências. A alternativa A é a menor alteração comportamental justificada pelo erro observado: o driver candidato acrescenta apenas import/chamada do helper de pré-carregamento antes de instalar o hook. O helper valida o arquivo exato e o roundtrip dos256 valores de byte, preservando a fronteira de leitura posterior.

[REAL — artefatos] DELTA_CODEC_PRELOAD.patch compara a fonte V2 executada com driver_p3_candidate.py. O helper é preload_npz_codec.py e o codec é pinado em CODEC_CP437_PIN.json. CONTRATO_CANDIDATO_SEM_EXECUCAO.json registra as alternativas, os pins e a cópia explícita das hipóteses, priors, grade, seeds/ruído, sampler, limites e critérios de convergência preservados. São fonte e proposta para revisão, não um pacote de lançamento: não foram criados novo job, CLAIM, launcher, contrato executável ou autorização.

## Controle isolado de leitura

[REAL] O primeiro controle preservado em CONTROLE_NPZ_LEITURA.json confirmou a identidade e o roundtrip do codec, mas falhou ao tentar importar zipfile depois do hook. Isso decorre da inicialização reduzida desse controle, que não importa Bilby/Dynesty. A falha ficou registrada; não foi um relançamento P3.

O controle V2 carrega antes do hook somente os parsers padrão nomeados zipfile e ast, conferidos por hashes próprios, além de NumPy e do mesmo helper de codec proposto. Sua política posterior é ainda estrita: leitura do arquivo NPZ exato, escrita apenas do recibo e seu temporário. Essa preparação é exclusiva do controle isolado; não acrescenta permissões ao driver candidato nem à execução V2.

CONTROLE_NPZ_LEITURA_V2.json: PASS_SYNTHETIC_NPZ_READ_ONLY. Foram conferidos os14 nomes, shapes de65537 elementos, tipos numéricos sem objetos, finitude pertinente, estrutura da PSD e grade j/32 Hz. allow_pickle=False foi mantido; hashes dos arrays estão no recibo. Depois do hook, somente o NPZ pinado foi lido, sem qualquer bloqueio ou leitura tardia de codec. Não foram importados Bilby, Dynesty, LAL ou as fontes waveform nesse controle.

| Controle | Parede | CPU do processo | Estatuto |
|---|---:|---:|---|
| Inicial, parser ausente | 0,632482 s | 0,241071 s | Falha preservada do controle |
| V2, parsers nomeados | 0,732913 s | 0,291640 s | Leitura/estrutura aprovada |

Esses custos pertencem aos controles de inicialização; não são benchmark de likelihood, PE ou campanha. Zero waveform, likelihood, sampler ou acesso a D. Os dois jobs científicos de P3 não foram relançados.

[OPEN — próximo passo] Revisão independente do delta e do controle de leitura. O sucesso do NPZ não certifica toda a montagem científica restante. Qualquer nova implantação ou repetição científica permanece dependente de autorização específica da coordenação e de novo contrato compatível; esta entrega não a concede. Holds, V1, P0–P2, limites, Atlas e fila permanecem preservados.
