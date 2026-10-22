# E1 — resultado e alcance para integração

[REAL — leitura/hash/contagem das saídas; NÃO-CEGO] Resultado numérico existente, sem rerun. Esta nota é transcrição estruturada e delimitação pelo autor do código, **não aprovação numérica independente**. A revisão do agente principal e a revisão de escopo/seleção por B continuam pendentes nesta emissão. Axiomas N/A; teoremas 0.

Execução registrada: 2026-09-22T19:53:26.012287+00:00; wall 41.584702 s; CPU 24.338970 s. Um processo, caps de threads=1 por ambiente; threads efetivas não verificadas. Hash resultado `4fec657346f96153488b872190484e3c4bee3800111f16193d844ce20decae00`; recibo `7b63a6faa19eb8fc4fd5f9879b90c9408c662fb8e6a73fdad9ede4ffd16ef5a5`. Ambos lidos e cruzados com código/manifesto/autorização.

33 eventos, 608681 draws registrados; 324 células: **288 condicionais e 36 NÃO PAGO**. Há 891 controles KDE e 32 comparações. As contagens foram reobtidas do JSON, sem abrir HDF.

- `GWTC5_31/sigma_lt_0.15`: n=3, 18 células NÃO PAGO por regra n<5; não são ajustes bem-sucedidos.
- `GWTC5_33/sigma_lt_0.15`: n=3, 18 células NÃO PAGO por regra n<5; não são ajustes bem-sucedidos.

## Comparadores nominais c(σ), banda 1

± corresponde a SE de curvatura local. d=c0/SE é somente distância descritiva. GR aqui é δtau=0 com df livre/marginalizado.

| Leitura | 31: c0 ± SE | 31: k ± SE | d31 | 33: c0 ± SE | d33 |
|---|---:|---:|---:|---:|---:|
| GR | -0.052272 ± 0.049250 | 0.639412 ± 0.304960 | -1.061 | -0.046095 ± 0.052800 | -0.873 |
| R-A | -0.052272 ± 0.049250 | 0.639412 ± 0.304960 | -1.061 | -0.046095 ± 0.052800 | -0.873 |
| R-B | -0.032749 ± 0.049576 | 0.645565 ± 0.307758 | -0.661 | -0.026566 ± 0.052491 | -0.506 |
| R-MOD | -0.013637 ± 0.051270 | 0.621849 ± 0.304961 | -0.266 | -0.007931 ± 0.054938 | -0.144 |
| R-RAIZ-0 | -0.015573 ± 0.049572 | 0.646139 ± 0.307941 | -0.314 | -0.009385 ± 0.052426 | -0.179 |
| R-RAIZ-EP4 | -0.052272 ± 0.049250 | 0.639412 ± 0.304960 | -1.061 | -0.046095 ± 0.052800 | -0.873 |
| R-RAIZ-REST | -0.052272 ± 0.049250 | 0.639412 ± 0.304960 | -1.061 | -0.046095 ± 0.052800 | -0.873 |
| R-LIN | 0.018583 ± 0.049584 | 0.649754 ± 0.309067 | 0.375 | 0.024782 ± 0.052069 | 0.476 |
| R-GLOBAL | -0.052272 ± 0.049250 | 0.639412 ± 0.304960 | -1.061 | -0.046095 ± 0.052800 | -0.873 |

R-RAIZ-COHERENT e R-PROP permanecem OPEN, com motivos no resultado. R-A/EP4/REST são numericamente irresolvidas nesta subtração em ponto flutuante; igualdade numérica a GR não prova efeito físico exatamente nulo. R-GLOBAL mantém sua hipótese de relógio comum. Nenhuma leitura é escolhida.

## Variante SNR e sensibilidade à banda

c(ρ)=c∞+kρ·40/ρ: SNR network do join congelado; não os cortes inspiral/pós-inspiral. Intercepto é extrapolação. Resultados nominais completos, covariâncias e todas as leituras estão em RESULT_SCOPE.json.

| População | GR: c∞ ± SE | GR: kρ ± SE | d_GR | d_R-B |
|---|---:|---:|---:|---:|
| GWTC5_31 | -0.057302 ± 0.045707 | 0.079277 ± 0.036083 | -1.254 | -0.835 |
| GWTC5_33 | -0.044243 ± 0.065173 | 0.062957 ± 0.044586 | -0.679 | -0.394 |

| Banda em 31/c(σ) | d_GR | d_R-B |
|---|---:|---:|
| 0.7 | -1.881311 | -1.260128 |
| 1 | -1.061369 | -0.660587 |
| 1.4 | -0.915345 | -0.552149 |

A dependência da banda é material para curvatura/distância local: não apresentar somente a banda mais favorável. Todos os intervalos locais nominais de c0 nas populações completas contêm zero: True. Isso não equivale a cobertura calibrada, teste de GR ou confirmação de qualquer leitura.

## Ponte para a convenção da gerência

| Método em GR/31 | c0 ± SE | k ± SE |
|---|---:|---:|
| median_q90_1.6449 | -0.061048529 ± 0.068315127 | 0.791656052 ± 0.369307648 |
| median_std_ddof1 | -0.057309310 ± 0.067897308 | 0.764013921 ± 0.363221373 |
| mean_std_ddof1 | -0.064374975 ± 0.067897308 | 0.880428183 ± 0.363221373 |
| Momento gaussiano u, fullsample | -0.064374975 ± 0.067897308 | 0.880428183 ± 0.363221373 |
| KDE fullsample nominal | -0.052272076 ± 0.049249685 | 0.639412448 ± 0.304960259 |

O controle mediana/q90 usa exatamente 1,6449 e cov absoluta; maior diferença absoluta arquivada entre os quatro números WLS e a gerência, nas duas populações: 3.33e-16. As mudanças de largura, média/mediana e forma marginal explicam estimadores distintos. O controle de medianas não substitui o resultado fullsample.

## Controles e paredes

Registrado nos outputs: máximo |Δlog KDE| em quantis 0.000161766; nos ótimos 4.21027e-05; erro máximo de massa 8.88178e-16; distância Newton máxima 0.00206971; menor distância ao suporte em h 7.22872; maior dispersão multistart 0.00984977. São resumos das verificações do construtor, não recomputação independente. A revisão principal GR/R-B poderá conferir sua validade.

**Não LR/Bayes factor; z calibrado permanece null.** df marginalizado não impõe df=0; prior conjunto e eficiência de seleção continuam OPEN; σ é endógeno; ESS desconhecida; covariância local não é posterior calibrado. Interseção de suporte é guarda conservadora mais restrita que a união induzida. Modelos compartilham eventos: não tratar diferenças entre c0 como independentes. Offset fixo: **PROIBIDA_COMO_TESTE**.

Para NUISANCE_V1: importar resultado/hash e esta matriz condicional; anexar revisão numérica do agente principal e nota de seleção/escopo de B. E1.2 não está pago por estes números; E1.3 não ganha curva SNR a partir do ponto LVK; E1.4 ainda requer distinção C2/C5; E1.5 só oferece distâncias locais. Nenhum NUISANCE_V1 formal foi escrito aqui.

Correção documental ao lado: o formulário anterior previa runs/authorized_002; a execução efetiva registrada usou **runs/authorized_001**. A primeira leitura pelo caminho previsto falhou com FileNotFoundError; após listar somente o diretório runs, o arquivo correto foi localizado e pinado. Não houve rerun nem alteração de originais.

UTC desta nota: 2026-09-22T19:58:20.047700+00:00

Fontes (raiz Chatgpt):

- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json` — `4fec657346f96153488b872190484e3c4bee3800111f16193d844ce20decae00`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json` — `7b63a6faa19eb8fc4fd5f9879b90c9408c662fb8e6a73fdad9ede4ffd16ef5a5`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/prepare_e1.py` — `cce4cf36a0c5d8fb3a07a13f54c4e2d867aa495b0f76e739613df84d59b63e4f`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/DESIGN_MANIFEST.json` — `375ee6824bae3ab65dcf802904a3a025e7a43ac0f009d3a59a3fc09225925a83`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/AUTHORIZATION.json` — `29e80e5cc30ea83d1c0daff1adf4195b7bf4074e263a05249d24b7bd81c83892`
- `ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/PLAN.md` — `81409ab298b8d7f7a81fd67d8d0dd7f2c0c977ea5b66b8e115fdb059190eb634`

Localizadores: resultado `/fits`, `/events`, `/management_WLS_controls`, `/descriptive_comparisons`, `/kde_controls`; RESULT_SCOPE.json conserva ponteiro exato `/fits/<índice>` de cada célula nominal. Código `prepare_e1.py:139`, `:158`, `:219`, `:297`, `:331`, `:476` ancora prior, densidade, ajuste, WLS, pares e comparação.
