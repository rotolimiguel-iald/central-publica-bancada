# Sintetizador vivo TGL — arquitetura operacional (27/09/2026)

## Objetivo e limite

O programa deve permitir formular uma pergunta, localizar dados pertinentes, ler produtos tratados, executar uma rota quantitativa já existente, confrontar controles e ver o resultado na mesma tela. A forma canônica da TGL e os teoremas do kernel são referências versionadas; nenhum gráfico os recompila ou confirma por si. Todos os originais científicos ficam em leitura somente.

## Fluxo único, com tipos distintos

`fonte original → inventário → esquema → tratamento específico da sonda → produto multirresolução → GPU → previsão existente → resíduo/controle → inferência com protocolo → recibo`

Cada seta produz um recibo ligado à fonte anterior. O programa recusa saltar de `DATA_PREVIEW_NOT_MODEL_FIT` para σ. O leitor não escolhe unidades, horizonte, calibração ou likelihood por nome de arquivo; estes campos vêm da documentação da sonda ou permanecem `UNKNOWN`.

O contrato `TGL_TREATMENT_V1` já implementa o primeiro nível: identidade local opaca, formato, tamanho, mtime, impressão parcial de bordas explicitamente distinta de SHA integral, colunas e unidades declaradas, qualidade, estado do adaptador e estado estatístico. O par DESI BAO é exceção tipada: média e covariância têm hashes integrais separados e o vetor de 13 pontos é correlacionado. A impressão parcial só agrupa candidatos a cópia; não prova igualdade de bytes nem independência entre estudos.

## Hardware e renderização

Medição local: RTX 5090, 32607 MiB; aproximadamente 4,1 GiB livres no momento da implantação, com `llama-server` em uso. O navegador foi observado usando WebGL2 via ANGLE/NVIDIA/D3D11. A primeira camada desenha pontos em um buffer pequeno da GPU; eixos e barras usam Canvas2D e o fallback assume tudo quando WebGL2 falta ou perde contexto. Essa camada não reserva VRAM e não acelera cálculo de física.

Para milhões de amostras, o servidor não envia o arquivo inteiro: calcula vistas por escala, janela, filtro e variável. Cada tile derivado guarda chave `(hash integral quando disponível, mtime, tamanho, adaptador, versão, seleção, intervalo, resolução, unidade)`. O navegador mantém só os tiles visíveis e libera buffers antigos. O orçamento deve consultar RAM/VRAM livres e encolher sob pressão, sem interromper o modelo local. Latência, FPS e memória serão medidas antes de anunciar metas de desempenho.

## Adaptadores e cobertura observada

O catálogo atual contém 1.350 caminhos/71,97 GiB, incluindo caches que podem repetir observações. Distribuição por extensão, medida pela API: 955 NPY, 180 HDF5, 57 H5, 86 NPZ, 35 FITS, 24 DAT, 9 TXT e 4 CSV. Isso é inventário de caminhos, não número de conjuntos independentes.

| Rota | Estado atual | Tratamento necessário antes de comparar com TGL |
|---|---|---|
| DESI BAO média + covariância | par 13×13 legível e validado em dimensões/simetria/diagonal | conferir origem, seleção, unidades, positividade da covariância, modelo D9/likelihood e calibração estatística |
| NPY 1D/2D numérico | cabeçalho e amostra por stride | semântica do array, escala e unidade por produto |
| FITS tabela binária | colunas numéricas escalares e amostra por seek | máscaras, coordenadas, cosmologia/seleção e pesos |
| CSV/DAT/TXT tabular | colunas e reservatório limitado | esquema, nulos, unidade, erros e proveniência |
| HDF5/H5 numérico 1D/2D | h5py existente em WSL; hiperslab até 1200 posições; links externos não seguidos | escolher dataset, unidade, frame de tempo, calibração, máscara, PSD/posteriores, correlações |
| NPZ e FITS imagem/HEALPix | inventariados, sem leitor interativo nesta versão | adaptador próprio com orçamento de descompressão/fatias e semântica do pixel |

Leitor genérico é infraestrutura. Tratamento científico exige perfil por sonda: por exemplo, GWOSC strain requer GPS, taxa de amostragem, máscara de qualidade, detector e PSD; BAO requer z, DV/DM/DH sobre r_s, covariância e seleção; weak lensing requer calibração de shear, pesos, redshift fotométrico e máscaras. Esses perfis devem versionar suas hipóteses e falhar visivelmente quando metadados obrigatórios faltarem.

## Painel que sintetiza sem confundir

Uma investigação seleciona `dados tratados`, `previsão TGL já implementada`, `previsão rival`, `resíduo/covariância`, `controle nulo` e `protocolo de inferência`. O painel mostra a cadeia de custódia e os estatutos em cada camada. O D9 histórico pode ser lido, mas a reexecução deve chamar o executor existente em ambiente isolado, registrar inputs e hash da rodada, e só então desenhar curva/resíduo. Nunca recalcular β ou um likelihood em JavaScript só para completar um gráfico.

## Próximos passos críticos

1. Criar índice incremental de tratamento por arquivo, com estado `VALIDATED`, `SCHEMA_REJECTED`, `ADAPTER_PENDING` ou `STALE`; distinguir disponibilidade do leitor de validação efetiva da fonte.
2. Criar perfis semânticos de DESI BAO, GWOSC strain/posteriores e KiDS; impor campos obrigatórios e grupos de correlação antes de análises conjuntas.
3. Introduzir tiles multirresolução e benchmark de navegação em milhões de pontos; medir FPS e VRAM enquanto `llama-server` está ativo.
4. Ligar D9 existente por execução reprodutível em ambiente isolado. A inferência σ exige protocolo pré-definido e calibração adequada; `sqrt(abs(Δχ²))` isolado não basta.
5. Adicionar NPZ/FITS imagem com limites de descompressão e semântica de produto. Ampliar as raízes do catálogo somente com regra explícita de inclusão e proteção de acervos privados.

Estado desta arquitetura: implementação parcial verificável; síntese quantitativa multi-sonda e tratamento de todos os arquivos ainda abertos. Nenhum gate matemático ou físico é alterado pelo painel.

## Adendo de revisão — 27/09/2026

O mapa `/api/lab/coverage` contou 1.263 rotas com leitor disponível e 87 pendentes em 1.350 caminhos, mas **não abriu e validou os esquemas de todos os arquivos**. FITS imagem pode aparecer entre os 35 FITS com adaptador de tabelas disponível e ainda ser recusado ao abrir. Candidatos a duplicata usam tamanho e impressão parcial de bordas, sem estabelecer igualdade ou independência.

Kimi e MiMo fizeram críticas independentes registradas em `stack/STACK_V3_REVIEW.md`. A verificação local levou a uma correção concreta: datasets HDF5 com armazenamento externo agora são recusados, além dos links externos já ignorados. O preview declara pares não finitos omitidos, índice sintético e que stride não autoriza inferência espectral. Continua faltando perfil físico GWOSC com tempo GPS, detector, calibração, qualidade e máscara; a amostra visual não é análise de onda gravitacional.
