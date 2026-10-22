[NÃO-CEGO — B1 entregue: portão e nuisance condicionais PAGOS; calibração física e eficiência de seleção NÃO PAGAS]

# B1 — portão da ampliação e nuisance

Abertura vinculante: `ENTREGA_013BIS_ABERTURA_operador.md`, SHA256 `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`. Ficha `REAPROVEITAMENTO_AMPLIACAO_B1.md`, SHA256 `6f69d57d77a1da413c85e1e230ea4f4db3bbde8ad86e9ffd23e945021d78c081`.

E0 conserva dez leituras, cinco conjuntos e os resultados C4 herdados. O alvo é informação esperada, condicionado à mistura de sinais/precisões, não uma seleção por largura posterior. N90/N50=1,578315602824 no cenário gaussiano de média; rotaIV calculada separadamente por MC.

O critério [INPUT] usa SNR GWOSC≥12, mediana GR Mf,det≥40 M☉ e 0≤χf<0,98, com prioridade SNR≥30. Na cobertura atual O4b, 27 passam entre 45 com SNR≥12; um aguarda Mf/χf. A ausência de metadados não é reprovação física; o censo de teste e preenchimento de metadados serão fixados em E2 antes de PE.

| Alvo | Estatuto e prova |
|---|---|
| E0.1–E0.5 | PAGO: combinações, alvos, SNR, tendência e falsificador espúrio. Offset zero PROIBIDA_COMO_TESTE. |
| E0.6 | PAGO como parede: controles C5 recalculados; σ(c) pSEOB livre NÃO PAGO. Gate de admissão falso. |
| E0.7–E0.8 | PAGO como cenários com fontes/datas e C4 herdada; nenhuma promessa de calendário. |
| E1.1 | PAGO no escopo condicional: 33 eventos, 608.681 amostras pareadas; 288 ajustes e 36 recortes não identificáveis preservados. |
| E1.2 | Regra pSEOB inspiral E pós-inspiral≥8 documentada em seções primárias; eficiência α(Λ) e leitura integral dos artigos NÃO PAGAS. |
| E1.3 | Uma injeção LVK com duas recuperações; curva por SNR NÃO PAGA. RD não mede 220 livre. |
| E1.4 | Dois estimadores C2/C5 com N/erro, sem juntá-los numa curva física. |
| E1.5 | Distâncias locais descritivas PAGAS; significância/separação física NÃO PAGA. |

No ajuste principal c(σ), referência δτ=0 com δf marginalizado: c0=-0.052272 ±0.049250, k=0.639412 ±0.304960. Erros de curvatura local, não intervalos calibrados. O controle mediana/q90 reproduz −0,061048529 ±0,068315127 e k=0,791656052 ±0,369307648; a diferença é de estimador, não ganho físico demonstrado.

R-B residual no mesmo recorte: −0,032749 ±0,049576. As leituras são ajustadas sobre os mesmos dados e compartilham o nuisance: não somar essas variâncias como independentes. Todas as bandas e recortes ficam no JSON. Nenhuma leitura escolhida.

A verificação independente por KDE exata conferiu oito ajustes GR/R-B, sem importar o produtor; maior distância entre parâmetros =0,001506 na métrica local. Outra revisão conferiu escopo, priors, 297 identidades de momentos e cadeia de custódia. Para as demais leituras, a verificação combina controles diretos do produtor e revisão documental; não se afirma refit independente integral.

As declarações Uniform não fecham a normalização global do modelo restrito. Portanto os escores E1 não são lnB nem likelihood hierárquica calibrada. NUISANCE_V1 transporta a matriz nominal apenas como INPUT para nulos sintéticos de E2; σ(c) físico permanece null.

Custo do ajuste: 41.584702 s de parede e 24.338970 s CPU. Revisão direta: 13.677910 s. Tempo contínuo consumido na Parte B ao fechar esta nota: 0.9632 h de 40; deadline `2026-09-24T11:06:33.802143+00:00`. Simultaneidade não é somada em dobro.

Tentativas preservadas: v1 parou antes da leitura HDF por ausência de threadpoolctl; v2 retirou só essa dependência e executou. Contagem de threads foi solicitada por ambiente, não medida. Dois candidatos MC da mistura33 falharam o limite inferior de poder e subiram na grade já fixada; os negativos permanecem. Guardas MC corrigidas ao lado, com custódia posterior explicitada.

Reprodução: planos/manifestos, scripts e comandos nos recibos vinculados abaixo. Os produtores recusam saída existente: repetir em cópia isolada e destino novo. Não executar o canônico. N/A — sem Lean; zero teoremas.

**Próximo passo obrigatório:** E2 com código completo, nulos sintéticos e testemunha no túnel antes de qualquer dado/PE de teste; depois E5/E4 e piloto. B1 não encerra a ordem.

## Arquivos e hashes

- `NUISANCE_V1.json` — `83f860bbfa904c0048005c8b0f1b367814032052f352e780af7d77ed1f257b85`.
- `PORTAO_DA_AMPLIACAO_V1.json` — `710028a7d2af7b649511afe369d88462d2add95c5fecbb1fb03c517fc91fe8a0` (903525 B).
- `PORTAO_DA_AMPLIACAO_V1.md` — `4fd8568d643525e415ab6d890a33220ce1eeb1447cad77f474d8cfce7e4c2dac` (6876 B).
- `bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json` — `4fec657346f96153488b872190484e3c4bee3800111f16193d844ce20decae00` (1302027 B).
- `bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json` — `7b63a6faa19eb8fc4fd5f9879b90c9408c662fb8e6a73fdad9ede4ffd16ef5a5` (1316 B).
- `bis/e1_nuisance_v2/DESIGN_MANIFEST.json` — `375ee6824bae3ab65dcf802904a3a025e7a43ac0f009d3a59a3fc09225925a83` (4998 B).
- `bis/e1_nuisance_v2/AUTHORIZATION.json` — `29e80e5cc30ea83d1c0daff1adf4195b7bf4074e263a05249d24b7bd81c83892` (882 B).
- `bis/e1_nuisance_v2/prepare_e1.py` — `cce4cf36a0c5d8fb3a07a13f54c4e2d867aa495b0f76e739613df84d59b63e4f` (30718 B).
- `bis/e1_nuisance_v2/PLAN.md` — `81409ab298b8d7f7a81fd67d8d0dd7f2c0c977ea5b66b8e115fdb059190eb634` (11204 B).
- `bis/e1_nuisance_v2/FAILURE_001.json` — `84e8b1bf594b38239a9c8c65c5d5bed36f39935eaa923fd5fbf62baba7bf0032` (1657 B).
- `bis/e1_nuisance_v2/RESULT_SCOPE_NOTE.md` — `bac427ca677023955cd092ea8471e970810a366c5270299714f33ee933d275e4` (7230 B).
- `bis/E1_DIRECT_KDE_REVIEW.json` — `230dd8f9424a3d8603d52131eb8fd92996cba84ff70527bf0ee31d00c65b6c31` (12117 B).
- `bis/E1_INDEPENDENT_SCOPE_REVIEW.md` — `13032341286f5ab61130fdcdcbcae3944d954112f96019dde0641852601ce7f4` (7479 B).
- `bis/e1_selection/SELECTION_AND_CONTROLS.json` — `6f8235bc13494818a8ca6c9fc1f76762ac52e119aae3a696bc2c286a41a18312` (45906 B).
- `bis/e1_selection/SELECTION_AND_CONTROLS.md` — `28244faeb8c76e0a8611965df8dba70f3f7ce02221fed9545abca579ce973a80` (6899 B).
- `bis/e1_selection/SOURCE_PASSAGES.json` — `5e61af849ac129aa42ec6a44143c46c1ef247bb41dc09c25043f78ee310aa1b0` (15483 B).
- `bis/e1_selection/RECEIPT.json` — `cd3fab331e8e324c30d38c8c8c26c69e1383efbb0b9557c23eb4796d0e991826` (912 B).
- `bis/e1_selection/NUISANCE_SCOPE_CONTROLS.json` — `978b059df98d67f88ee210f21cf272038316c36cd5f852394c9b3e22f2c1f49f` (6405 B).
- `bis/PART_B_BUDGET_START.json` — `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f` (1536 B).
