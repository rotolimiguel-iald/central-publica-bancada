[REAL — análise computacional condicional, NÃO-CEGA; não move o gate]

# Ordem 013 — catálogo, pyRing, relógio e trajetórias

Controle pyRing: 84701 amostras; ramo B ln B=0.141139410 (pSEOB primário: 0.029026162). Mesmo evento, sem multiplicação das evidências. As três amostras de spin negativo foram mantidas e verificadas por qnm e Leaver. A versão 2.7.0 é do ambiente de figuras; procedência integral do binário/mesclagem é ressalva explícita.

Catálogo já calculado foi consolidado: 33 produtos, seleção literal primária de 31. Conteúdo HPD da RG na combinação primária: 0.983710937; RG fora de 95%, portanto o critério registrado conserva INCONCLUSIVE_SYSTEMATICS. Nem esse conteúdo HPD nem ln B são sigma de descoberta.

Relógio livre integrado com os dois priors previamente registrados, sem tratá-lo como Bayes de ponto. Limites condicionais de 95% (segundos na fonte): uniform: 0.00029209333, log_uniform: 3.34417752e-06. A coordenada de prior permanece quase uniforme; a grande diferença não é evidência de medição precisa. Quadratura independente aprovada em C4_FREE_CLOCK_ORACLE.json.

Trajetórias: 1100 ajustes em 22 células, 50 por célula, 0 falhas de otimizador, 0 contatos com limites. Incluem Wiener, Cauchy e Poisson coerente N=4/64/256. Ruído OU sintético, sem alegação de C5 empírico; o ajuste de uma trajetória não é igual ao ajuste da média de ensemble.

Manifesto de downloads: 70 arquivos com hash recalculado, falhas de obtenção preservadas. Nenhum strain da janela foi lido. Memórias canônicas e um.py não alterados.

**Pendências integrais**

- C0: três downloads de literatura falharam (403/406), registrados; não equiparar resumo/abstract a leitura integral.
- C2/C3: escolhas de desenrolamento continuam hipóteses físicas; portar/explicitar interfaces de Cauchy e soma de Poisson no pacote. O teste atual usa ruído sintético, não off-source.
- C4: hipóteses conjuntas 220+440 e tratamento dos demais modos; comparação de início tardio com pyRing; conferência do GWTC-3 sem duplicar eventos; sensibilidade restante de priors e remanescente.
- C4: procedência da fusão do weighted_posterior e binário original pyRing não reconstruída; 2.7.0 está fixado no ambiente publicado de figuras. Controle secundário fica condicionado a isso.
- C5: PSD fora da fonte, injeções com duas famílias IMR e N>=50 por célula; viés/cobertura sob ruído empírico; completar distribuições de evidência calibradas, além de Fisher.
- C6: entregar registro com hash antes de ler strain na janela; executar rota escolhida validada, incluindo cinco tempos de início e controles.
- C7: pacote independente em inglês, comandos e teste de reprodução integral; só declarar completo após auditoria do objetivo inteiro.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| C1, tabela e unidades | PAGO no escopo condicional | C1_TABLES.json e C1_LEITURAS_E_RELOGIOS.md |
| C2, distribuição de estimadores sem/com ruído colorido | PAGO como simulação explícita | C2_TRAJECTORY_RECOVERY.json; não substitui ruído empírico |
| C3, consumidor Bilby | PAGO para fonte 220 | C3_BILBY_CONSUMER.json; regressão preservada |
| C4, priors, grade e catálogo sem duplicação | PAGO para comparação condicional 220 | C4_CATALOG_220.json + C4_CATALOG_COMBINATION.json |
| C4, controle pyRing | PARCIAL | C4_PYRING.json; versão da inferência e fusão das amostras não auditadas |
| C4, relógio livre | PAGO para GW250114/220 | C4_FREE_CLOCK.json + oráculo independente |
| C4, todos os modos e todas as sensibilidades | NÃO PAGO | lista de pendências acima |
| C5, ruído empírico e duas famílias IMR | NÃO PAGO | Fisher anterior e simulação OU não bastam |
| C6, strain registrado | NÃO PAGO | janela ainda não lida |
| C7, pacote e reprodução integral | NÃO PAGO | objetivo permanece ativo |

## Reprodução

Executar no WSL, com `/opt/lal_env/bin/python -B` e diretório absoluto `/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN`:

1. `pyring_readout.py` (usa os arquivos públicos e fontes já fixados no cache).
2. `free_clock_posterior.py`, depois `verify_free_clock_oracle.py`.
3. `trajectory_recovery.py`.
4. `verify_prediction_catalog_compatibility.py`.

Não reinstalar nada em `/opt`; vendor próprio fica em cache/vendor. O manifesto de downloads registra as fontes e seus direitos. Os scripts de análise preservam resultados anteriores em backup. O registrador desta entrega não é um teste científico a ser repetido.

## Custódia lida dos artefatos

| Arquivo na Ordem 013 | SHA-256 |
|---|---|
| C1_LEITURAS_E_RELOGIOS.md | `c86b35a8ee08874c2782131a04ff5f13e0b8ea9df78b3f36a38502ab39e29997` |
| C1_TABLES.json | `bf5ac0d2dad2322a5b0cb1ac3b861870447e6f2ff41c1ab251e443b61a56d79a` |
| C3_BILBY_CONSUMER.json | `bc49da2a45a5652f4b1e2ce1c5f129c1075ea827f42e5dadb84fd81255e60c1a` |
| QNM_GRID.json | `4f34367a0906023836fcf8013ada3ccef48877a17f59f697b9dabc25a2494b24` |
| C4_CATALOG_220.json | `93bdc413130d294acde91ec03f8392b8d9c5ec5b33fdc97274371656503d8e17` |
| C4_CATALOG_COMBINATION.json | `f3d8c1959ded3efd15045923ce0cbafe7356ec888ced1934d8d0c183046d0d01` |
| C4_CATALOG_PRIOR_AUDIT.json | `d5a8ca83e7f4895961d15186c3b81fd91732e8f720ffe5a9bb80383e4083aaf1` |
| C4_PYRING.json | `76af853137f3e7d3396f001eb44cfc3a6366d2e92b9d9ed7b8454ec8b0f35b0a` |
| pyring_readout.py | `ffbfe7bd90b9ba8305a50e5241177adf8d818a8d15bea800daf71e126a981547` |
| C4_FREE_CLOCK.json | `cbf63327719372780ec3b3c89376360e78828c45198ee5cfd5bf04cd5ea328b1` |
| free_clock_posterior.py | `acb13e9a0fc90130f1f68440b663bb9090a1cf0daba092380e70a010ad0e28f1` |
| C4_FREE_CLOCK_ORACLE.json | `b75283ddc1b2001fcb6cb2458077a0c99f914f3493b497fa0e2902d7e2390b38` |
| verify_free_clock_oracle.py | `40b5bef87ea08034e7a81a08500bcc7d37b387a0663b2a33a296641aeca09cff` |
| C2_TRAJECTORY_RECOVERY.json | `339be42bec67a48e1e3341d678ac9bc0804c6e1db035e6b4b57df62673eafd38` |
| trajectory_recovery.py | `a5648ee2303159fb8cd083d9f490ff6d1ec0d1231f2a9fb6e8163ea93de01b33` |
| tgl_ringdown_prediction.py | `458940f77a49430521e06b369adaaa43157c69f635f64a733e7a4bf07d5d7f80` |
| C3_PREDICTION_COMPATIBILITY.json | `83bb5ed07bf3783b05c20f99666536ab37f5d0aae1379b90e99fae0267382f2b` |
| cache/MANIFESTO_DOWNLOADS.json | `6aef8f1dd8d811a07ab15b2bc30c69f9a3097009ffe6130271c036afdab2a047` |

## Ficha de aproveitamento

Reutilizados: módulos de predição/KDE/constantes/forma de onda, registro C4, grade QNM, solver Leaver, posteriores verificados e regras de exclusão. Novos: adaptador restrito aos dois ajustes aritméticos pyRing, marginalização do relógio e oráculo, matriz de trajetórias, consolidação de memória e downloads. Nenhum programa ou kernel canônico editado; nenhuma confirmação física ou escolha de partição. Axiomas: N/A — sem Lean.

Falhas preservadas: limiar arbitrário de arredondamento do spin; grade positiva que recusou três amostras negativas; portadora comum inicial; quadratura ainda insuficiente nas primeiras grades. As correções e os controles numéricos estão no diário e nos JSONs.
