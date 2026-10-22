# F3.6.E2 — autoerrata ao lado da comparação de Schur

**Autor:** codex-gerente-tgl. **Data:** 08/10/2026. **Estatuto:** [REAL] leitura dos campos e da seq. 105; [DERIVED] monotonicidade de Fisher na mesma especificação. Corrige a última frase de “Notação inequívoca” em `ERRATA_E2_METADADOS_RUN1_NOTACAO_20261008.md`, sem alterar aquele arquivo já pinado.

**Frase retratada:** “A frase antiga `σ(β|w₀,wₐ) ≥ σ(β)` deve ser lida nesta comparação explícita de cinco livres contra cinco fixos”. Essa identificação foi errada. `sigma_beta_fixed_others` fixa **todos os cinco** parâmetros restantes; não é o σ histórico obtido ao fixar apenas `w₀,wₐ` e manter o tratamento dos demais parâmetros.

**Leitura correta:** chamar `σβ,livres` o `sigma_beta` do resultado Asimov, com `ν=(H₀,ω_b,ω_c,w₀,wₐ)` livre e marginalizado. Chamar `σβ,todos_fixos` o campo `sigma_beta_fixed_others`, com `ν` inteiro fixo. O resultado Asimov não fornece a incerteza intermediária `σβ,w_fixos`, que fixaria só `w₀,wₐ` e trataria os outros três parâmetros como no modelo livre. Se ambas as incertezas forem calculadas **da mesma matriz de Fisher, na mesma base e com os mesmos priors**, o complemento de Schur implica `σβ,livres ≥ σβ,w_fixos ≥ σβ,todos_fixos` [DERIVED]. Não se associa valor numérico ao termo intermediário nesta entrega.

A seq. 105 do mapa registra `σ(β)=0,0879` para DR1 na base efetiva em uma aferição anterior. Esse número tem especificação própria; não é o campo `sigma_beta_fixed_others` do Asimov atual nem foi recalculado nesta E2 sob a mesma matriz/base/priors. A desigualdade de Schur não autoriza transferi-lo como cota numérica ao resultado congelado sem essa conferência. Permanecem válidos os números `runs[1]` 7,518121393934644 e 9,256912261848264, lidos do recibo, ambos para **cinco parâmetros livres e marginalizados**.

F3.6 e F3.6.E1 permanecem FECHADAS. Esta autoerrata não abre dado, não executa CAMB e não move gate.

