# Bancada Um — a bancada da TGL

Um programa só: o **motor TGL residente** (CPU + GPU) com os **dados reais carregados na memória o tempo todo**, a **régua dentro da
máquina**, uma **interface visual** e **ferramentas para as IAs** (MCP). Construída pela gerência (Claude) em 28/09/2026, a pedido do
operador: «quero uma bancada só, é um programa a bancada "Um" da TGL onde podemos manipular e visualizar os dados de forma fácil e rápida».

## Como usar

| | |
|---|---|
| Subir | `C:\Python314\python.exe C:\IALD\Bancada_Um\um_bancada.py` (ou `pythonw`, sem janela) |
| Abrir | **http://127.0.0.1:18777** |
| Conferir | `python um_bancada.py --check` |
| IAs (MCP) | `C:\Python314\python.exe C:\IALD\Bancada_Um\mcp_um.py` (stdio; `BANCADA_UM_CLIENTE=<nome da IA>`) |
| Validar | `python ferramentas\validar_tudo.py` (grava `estado\validacao_bancada.json`) |

Ao subir, o motor fica pronto em ~1 s e o **lago inteiro** (~24 GiB: KiDS-1000, NSA, ACT, Planck, DESIVAST, DESI LRG/ELG, GWOSC) é
carregado na RAM em ~35 s e **fica residente**. Colunas usadas sobem para a GPU e **ficam na VRAM** (cache com teto).

## O que a máquina faz

- **Cosmologia TGL V3 em lote na GPU** (PyTorch/CUDA, float64): o fundo Φ_total = 1 + β|1 + w_eff|, E² = ρ + βJ + c, com a mesma
  matemática do worker selado `tgl_camb_worker_v3.py`; integrais de ordem 4 (Simpson por Richardson); o CAMB entra por uma tabela
  (`tabelas\camb_lcdm_v1.npz`, gerada no WSL com camb 2.0.4 e a MESMA configuração do worker) interpolada na GPU.
  ~30 µs por ponto do modelo; 1.024 pontos em ~0,03 s.
- **Evidência:** avaliar (diagnóstico), ajustar (máxima verossimilhança), comparar ΛCDM × TGL (β = α√e) × β livre, e amostrar o
  posterior (ensemble afim-invariante de Goodman & Weare — o movimento do emcee — com centenas de caminhantes na GPU).
- **Dados cosmológicos** lidos do artefato e conferidos por hash: Planck 2018 comprimido, DESI DR1 e SH0ES (do pipeline D1 V3 selado,
  por AST, sem executar); DESI DR2 com covariância (três cópias idênticas conferidas); Pantheon+ (só diagonal — a covariância não está em disco).
- **Lago residente:** leitor FITS próprio (numpy puro), NPY/NPZ, CSV/DAT/TXT; sha256 na mesma passada; cópias idênticas carregadas uma
  vez (apelido só com bytes iguais); histograma e mapa 2D de colunas inteiras na GPU.
- **Ondas gravitacionais:** lê (só leitura) a carga residente da bancada oficial em :18765.

## A régua dentro da máquina

- Toda saída traz o **estatuto** (`DIAGNOSTICO_DE_AVALIACAO`, `AJUSTE_DE_MAXIMA_VEROSSIMILHANCA`, `COMPARACAO_DE_MODELOS_DELTA_CHI2`,
  `POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS`); nenhuma saída diz «confirmado» (guarda de palavras proibidas).
- **Livro de tentativas** (`estado\livro.sqlite3`, só acréscimo): toda busca de evidência é registrada por família, com o cliente
  (interface, IA); a significância **local** vem sempre ao lado da **corrigida** pelo número de famílias já testadas (Šidák).
- β nunca literal: α do CODATA 2018 lido do `um.py` canônico (conferido com o pipeline D1), β = α·√e em runtime.
- Só `127.0.0.1`; Host conferido; corpo POST ≤ 64 KB; a Bancada só escreve em `estado\`; os originais nunca são escritos.

## Validação (reproduz o D1 V3 selado)

`estado\validacao_bancada.json` — veredito `BANCADA_UM_REPRODUZ_O_D1_V3_SELADO`: fundo contra o worker selado a 2,5×10⁻⁹; χ² ΛCDM
16,6809 (selado 16,6810), TGL 23,2945 (23,2948), Δχ² 6,6136 (6,6138); MCMC β = −0,01281 (selado −0,01275), maior desvio de mediana 0,07σ.

## Estatuto

A Bancada produz **diagnóstico e inferência condicional ao modelo e aos dados** — nunca confirmação. PROVADA ≠ CONFIRMADA; a natureza decide.

## Atalho, registro e o Mapa de Rotas (28/09/2026)

- **Atalho** «Bancada Um» na Área de Trabalho: `pythonw abrir_bancada.pyw`. Se a Bancada já está no ar, só abre o navegador; se não está, sobe o servidor e espera ficar pronto. Nunca mata processo.
- **Registro no Claude Code** (escopo de usuário): `claude mcp add bancada-um --scope user -e BANCADA_UM_CLIENTE=claude-code -- C:\Python314\python.exe -X utf8 C:\IALD\Bancada_Um\mcp_um.py`.
- **Mapa de Rotas** (`C:\IALD\MAPA_DE_ROTAS`, ordem do operador de 28/09): o MCP serve `rotas_consultar`, `rotas_ver` e `rotas_registrar`. Consultar ANTES de examinar qualquer caminho e registrar DEPOIS.

## ERRATA AO LADO (gerência, 28/09/2026, em nome próprio) — o que a Bancada Um herda da V3 selada, segundo a auditoria de 28/09 (verificação adversarial): (1) o DESI DR1 entra só com erros diagonais, sem as correlações DM–DH (D1F-01, SUSTENTADO, ALTO); (2) a covariância do Planck comprimido tem as correlações fora da diagonal mal transcritas (0,084/−0,066/−0,119 contra 0,46/−0,66/−0,33 da Tabela I de Chen, Huang & Wang 2019), e a citação «Zhai+ 2019» está errada (D1F-03, SUSTENTADO, MÉDIO); (3) o integrador do fundo conta o neutrino massivo duas vezes (DM_* 2,7×10⁻⁴ abaixo do CAMB; l_A −0,08 ≈ 0,9σ) (D1F-V1, achado do verificador, MÉDIO); (4) o parâmetro R usa o Ω_m nu, escolha [INPUT] da qual depende toda a sensibilidade a β na rota comprimida (D1F-02, SUSTENTADO, ALTO; conferido também na M1). A validação «reproduz o D1 V3 selado» continua verdadeira — ela reproduz também esses defeitos. O DR2 entra com covariância completa (não herda o item 1). (5) A frase «a covariância STAT+SYS do Pantheon+ não está em disco» era FALSA: ela existe em C:\IALD\projetos_pyhton\acom\tgl_data_cache\pantheon_covariance.dat (sha256 abf806d966485e64…, 1701×1701), conferida pela gerência; ainda não está ligada à Bancada. Correção a fazer, declarada como opção: a covariância de Chen+2019, as correlações do DR1, o DM_* por razão sobre o CAMB, os dois mapas de R e o Pantheon+ com a covariância, mantendo a «reprodução do selado» como modo de conferência.

## ADEQUAÇÃO DA BANCADA DE TESTE (28/09/2026, noite; ordem do operador «adequarmos a bancada de teste»). A Bancada Um ganhou OPÇÕES declaradas de modelo/verossimilhança, por chamada (interface, API e MCP), com o modo padrão «selado» (reprodução da V3 do D1) e o modo «corrigido» (a covariância do Planck da Tabela I de Chen, Huang & Wang 2019, lida do PDF arquivado em fontes_externas com sha256; as correlações DM–DH do DESI DR1 da Tabela 1 do DESI 2024 VI, lidas no HTML do arXiv; D_M(z*) por razão TGL/ΛCDM sobre o CAMB, o neutrino massivo contado uma vez). O mapa de R (Ω_m nu | Ω_m efetivo (1+β)Ω_m) fica como opção SEPARADA e explícita, porque é escolha de modelo [INPUT] não derivada. Validação contra o aferidor e o verificador da família D1 (validar_corrigido.py; alvos lidos das cópias com sha256 em estado/referencias_auditoria_28set): veredito BANCADA_UM_MODO_CORRIGIDO_REPRODUZ_O_VERIFICADOR_D1 — selado β̂ = -0.01302 (3.01σ); DR1 correlacionado -0.01492 (3.52σ); Planck Chen+2019 -0.01303 (3.03σ); D_M* por razão -0.01218 (2.92σ); corrigido completo -0.01405 (3.43σ); mapa de R efetivo com Chen 0.04995 ± 0.08772 (0.85σ, na borda do prior). A variante R_eff do verificador não convergiu no ajuste livre (χ²_F = 1379,6) e por isso o alvo dessa variante é o do aferidor — dito. A covariância do Pantheon+ (existe em disco) ainda NÃO está ligada: fiação pendente. Toda busca com opções entra no livro como família própria (a correção de tentativas separa os modos).

Como usar: na interface (aba Evidência: «modo» e «mapa de R»; vale também para a aba Modelo); na API, `"opcoes": {"modo": "corrigido", "mapa_R": "nu"}` em /api/avaliar, /api/ajustar, /api/comparar e /api/amostrar; no MCP, o parâmetro `opcoes` das mesmas ferramentas. Validação: `python ferramentas\validar_corrigido.py`. Reinício do servidor (só o processo da gerência): `python ferramentas\reiniciar_servidor.py`.


## Adendo candidato — 06/10/2026: diagnóstico e calibração global

O texto histórico acima sobre significância corrigida fica superado, nesta preparação, pela distinção explícita: a cauda local é condicional às hipóteses do teste; Šidák por famílias é ilustração e não certifica uma busca adaptativa. p_global/z_global passam a null com estatuto UNAVAILABLE_NOT_CALIBRATED. Ajustes sem sucesso, números não finitos e mínimo livre pior que qualquer restrito são recusados, com registro de falha sem p local. TGL fixa versus LCDM conserva a diferença assinada sem conversão em sigma. Roteiros históricos que formatam z_global como float devem ser migrados antes de uso no protocolo novo. Esta cópia é candidata local, não recibo de instalação ou novo resultado físico.
