# CÉTICO 1 — achado da lente fidelidade_auditorias sobre a ORDEM 013-bis, linha 46 (§2 item 2 / F2, relógio livre τ★)

**Veredito: NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE.**

## O que medi
1. **Ordem, l.46** (única ocorrência; l.75 e l.87 tratam do relógio livre sem atribuição): «a bancada mediu por conta própria que o dado só começa a cortar em τ★ ≳ 5–10 GM_f/c³: ln B(5 t_M) = −1,10; (8 t_M) = −2,67; (10 t_M) = −5,11».
2. **Bancada (só-leitura), `ORDEM_013_RINGDOWN\C4_FREE_CLOCK.json`** (64.009 bytes, lido por script): `physical_clock_bounds.upper = "tM_source for each nuisance sample"`; dois priors (`uniform`, `log_uniform`), coordenada de prior u ∈ [0,1]; `log_likelihood_ratio_range = [0, 0,0376]`. **Zero** ocorrências de −1,1 / −2,67 / −5,11 / «t_M» / «extend». As cópias em `C7_INDEPENDENT\evidence\` e `C7_POSTERIOR_REPRODUCTION\cache\run_free_clock_*` são o mesmo produto (teto = t_M). `grep -rn` por −1,10 / −2,67 / −5,1 em .md/.txt/.log da pasta da bancada: nenhuma linha. **A bancada não tem esse artefato.**
3. **aud_6.txt l.91** («Estendendo por conta própria: ln B(τ★ = 5·t_M) = −1,10; 8·t_M: −2,67; 10·t_M: −5,11») e **l.127** («Meu corte pela verossimilhança … a extensão acima de t_M é conta do auditor, NÃO-CEGA»). O script existe: `auditoria\c4\free_clock_check.py` (20 linhas; loop `for u in [1,2,3,5,8,10]`).
4. **Reproduzi o número rodando o script do auditor** (`python free_clock_check.py`, posterior `post_GW250114_17018009__pSEOBNRv5PHM.npz`, KDE 2D em (δf̂, δτ̂), deslocamento s = −u·x_B/(1+u·x_B), β = α·√e em runtime): u=1 → +0,0290; u=2 → −0,147; u=3 → −0,421; **u=5 → −1,0963; u=8 → −2,6706; u=10 → −5,1055**. Os três números da ordem estão CERTOS (arredondados a 2 casas) — **a autoria é que está errada**: são do auditor 6 da gerência, não da bancada, e a conta é declarada NÃO-CEGA (o posterior já era conhecido).

## Por que não refuto
- Não é questão de gosto: a frase atribui à bancada uma medição que só existe no scratchpad da gerência. Publicada imutável, a bancada terá de «reportar ao lado» algo que nunca mediu — ou cita a própria medição inexistente (fabricação de fonte, régua nº 1/2), ou refaz e descobre que a ordem lhe imputou um artefato.
- O estatuto NÃO-CEGO (aud_6 l.127) some da ordem; a l.75 diz «[INPUT] dito» para o prior estendido, mas não diz NÃO-CEGO para o corte.
- Não é BLOQUEANTE: os números são corretos e reproduzidos; a física da errata (limite dominado pelo prior) está certa; a correção é de proveniência e estatuto, não de conteúdo.

## Correção FINAL (substituir na l.46 o trecho entre parênteses e o fecho)
Substituir «(a bancada mediu por conta própria que o dado só começa a cortar em τ★ ≳ 5–10 GM_f/c³: ln B(5 t_M) = −1,10; (8 t_M) = −2,67; (10 t_M) = −5,11), declarando o prior estendido como [INPUT].» por:

«(o auditor 6 da gerência mediu, NÃO-CEGO e fora do registro — `auditoria\c4\free_clock_check.py`, mesmo posterior e mesmo KDE, deslocamento s = −u·x_B/(1+u·x_B) com u = τ★/t_M —, que o dado só começa a cortar em τ★ ≳ 5–10 GM_f/c³: ln B(5 t_M) = −1,10; (8 t_M) = −2,67; (10 t_M) = −5,11; o `C4_FREE_CLOCK.json` da bancada tem teto em t_M e não contém essa extensão). A bancada REFAZ essa conta com o teto do prior pré-declarado em múltiplos de t_M (u ∈ {1, 2, 3, 5, 8, 10}) [INPUT], marca-a NÃO-CEGA, reporta a diferença contra os três números da gerência, e mantém os dois priors originais ao lado.»

Ajuste coerente na l.75 (F2): «**Relógio livre τ★ (errata 2 da §2):** os dois priors pré-declarados E o corte sem teto refeito pela bancada (u ∈ {1,2,3,5,8,10}), [INPUT] e NÃO-CEGO ditos, com a diferença contra a conta do auditor 6.»
