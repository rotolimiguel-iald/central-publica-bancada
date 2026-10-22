# Cosmos — fundo V3, comparação e caderno local

28/09/2026 · Entrega de software e reprodução de um fundo condicional. Nenhum gate alterado.

A bancada reutiliza `FundoV3` de uma cópia byte a byte do worker embutido no programa. As âncoras e os hashes medidos estão em `COSMOLOGY_CANONICAL_ROUTE_AUDIT.md`. Não é uma nova derivação de Friedmann, nem o solver completo de perturbações da TGL.

## Usar

Abra TGL na área de trabalho e entre em Cosmologia, ou acesse http://127.0.0.1:18766/cosmos.

1. Escolha V3 β zero e clique **Fixar atual como A**.
2. Escolha **TGL V3 · β fixo**. A continua tracejada e B é contínua; os dados aparecem uma única vez.
3. Em **Diferença B − A**, selecione DM, DH ou DV e percorra z. A curva representa diferença de modelos; o χ² usa os 13 valores nos redshifts exatos e a covariância completa.
4. Ajuste H₀, Ωm total ou r_d pelos controles ou valores exatos. w₀ = −1 e wₐ = 0 ficam fixos no V3; CPL permite variar ambos como referência exploratória.
5. Dê um nome e salve B. **Usar como A** recupera o resultado histórico se dados e geração do motor coincidirem. **Carregar como B** reaplica os parâmetros ao motor atual. O original é preservado. JSON exporta o cenário completo; Exportar A + B recalcula e guarda a comparação. Os arquivos são gravados em `state/exports/` no computador, com link de leitura na própria interface; não dependem de download por URL temporária do navegador.

Os cenários ficam em `state/cosmology_scenarios.sqlite3` na instalação. A gravação é transacional, append-only, validada por hash; o servidor recalcula antes de salvar. O hash detecta corrupção, não constitui assinatura contra quem pode substituir dados e digest. Nenhum estado inferido do navegador é aceito como resultado científico.

## Hipóteses do V3

- Fluido total: radiação + matéria + Λ; Φ = 1 + β(ρ+p)/ρ no ramo de entalpia não negativa.
- E² = ρ + βJ, J(a) = ∫_a^∞ 3(ρ+p)²/(ρã) dã; C = 0 e P(∞) = ρΛ.
- ΩΛ resolvido por H(0) = H₀. Ωm representa a matéria total. TCMB = 2,7255 K e N_eff = 3,046 são entradas do worker histórico.
- β fixo calculado por ALPHA_FINE_CODATA_2018 × √e; β zero é o controle correspondente, também com radiação.
- A divisão `ombh2=0, omch2=Ωm h², mnu=0` é representante computacional da soma que entra em E/DM, não afirmação de ausência física de bárions/neutrinos. Nenhum horizonte acústico é calculado dessa divisão.
- r_d é entrada independente. O painel não chama CAMB, `derivados` ou `rs_integral`. Não transporta priors, χ² nem sigmas históricos para os 13 pontos DR2.
- A face recíproca mencionada na v367 não substitui informalmente o ramo V3. Sua escolha e o fechamento perturbativo global seguem explícitos no contrato D10.

## Precisão, desempenho e limites

A fonte mantém sua grade de 400001 pontos, raiz do fecho e quadratura de distância. O adaptador verifica E(0), positividade, resíduo da segunda equação em z≤3, refinamento local de E e refinamento do cursor. O teste β zero usa integração independente. Os resultados medidos são registrados em `state/validation_cosmology_v3_*.json`; limiares não são promessas de precisão universal. r_d/CMB e calibração estatística global não estão resolvidos por estes controles.

O processo WSL separado conserva o último fundo/curva; mudar somente r_d ou cursor reaproveita esse fundo. A CPU calcula e a GPU WebGL2 desenha. Erros ficam visíveis, sem substituição silenciosa por CPL. A memória GW pertence a outro processo e não é reiniciada por esta atualização.

A navegação de z/animação ainda é navegação do fator de escala, não relógio físico TGL. A grade 3D é esquemática. A/B e Δχ² são diagnósticos manuais, sem ajuste dos parâmetros, significância ou confirmação física; a busca D10 global continua regida pelo protocolo próprio.
