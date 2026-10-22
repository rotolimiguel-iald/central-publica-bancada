# CÉTICO 2 — achado l.46 (§2 item 2 / F2, «Relógio livre τ★») — VERIFICADO, NÃO REFUTADO

Data: 22/09/2026. Lente: refutação do achado «atribuição errada da extensão do prior».

## Medido
- ORDEM 013-bis l.46: «a bancada mediu por conta própria que o dado só começa a cortar em τ★ ≳ 5–10 GM_f/c³: ln B(5 t_M) = −1,10; (8 t_M) = −2,67; (10 t_M) = −5,11».
- auditoria/aud_6.txt l.91: «Estendendo por conta própria: ln B(τ★ = 5·t_M) = −1,10; 8·t_M: −2,67; 10·t_M: −5,11» (bloco [NOTA] C4_FREE_CLOCK.json; «Defeito da ordem, não da bancada»).
- auditoria/aud_6.txt l.127: «Meu corte pela verossimilhança: ln B = −1,1 em 5·t_M, −2,7 em 8·t_M, −5,1 em 10·t_M. | [REAL] (reproduzido); a extensão acima de t_M é conta do auditor, NÃO-CEGA».
- Bancada (só leitura) `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_FREE_CLOCK.json` (64.009 bytes): regex `-1\.1\d|-2\.6[6-8]|-5\.1[01]` → False; `physical_clock_bounds.upper = "tM_source for each nuisance sample"`; grade `prior_coordinate` u ∈ [0,1] ⇒ τ★ ≤ t_M. `C4_FREE_CLOCK_ORACLE.json`: idem, False. `free_clock_posterior.py` l.42/61: τ = t_P + u·(t_M − t_P), sem teto acima de t_M. Nenhum arquivo da pasta contém os três valores (grep sobre *.json/*.md/*.txt/*.py, excluído cache/vendor).
- bis/medir (SINTESE, CRITICO, CRITICO_completude) e RELATORIO_AUDITORIA_AO_OPERADOR_22SET.md: zero ocorrências de 1,10 / 2,67 / 5,11 / «5–10» — a única fonte é aud_6.
- Reprodução por script: IMPOSSÍVEL a partir dos artefatos da bancada — o JSON só carrega a verossimilhança marginal até u = 1 (τ★ = t_M); a curva de predição acima de t_M não está serializada. Os três números ficam [DECLARADO — aud_6, NÃO-CEGO] até a bancada refazer.

## Veredito
refutado = false. A ordem atribui à bancada uma conta que é do auditor 6 da gerência, e apaga o estatuto NÃO-CEGO. Se publicada assim, a bancada terá de «citar» uma medição que não existe nos seus artefatos (indução de fabricação de fonte) — IMPORTANTE, mantida.

## Correção FINAL (l.46, substituir do «Corrige-se» ao fim)
Corrige-se na Parte A (F2): reportar os dois priors pré-declarados E, ao lado, o corte que o dado impõe sem teto. O auditor 6 da gerência mediu, **NÃO-CEGO e fora do registro**, que o dado só começa a cortar um relógio escalado pela fonte em τ★ ≳ 5–10 GM_f/c³ (ln B(5 t_M) = −1,10; (8 t_M) = −2,67; (10 t_M) = −5,11) `[DECLARADO — aud_6; não reproduzível a partir de C4_FREE_CLOCK.json, cujo teto é t_M]`. A bancada **refaz** essa conta com o teto do prior estendido a várias t_M, pré-declarado como [INPUT] em emenda datada, marca o resultado NÃO-CEGO e reporta os dois priors originais ao lado; nenhum número do auditor entra na entrega sem ser recalculado pela bancada.

## Consequente (l.75, F2) — acrescentar
«…o corte sem teto, [INPUT] dito» → «…o corte sem teto, [INPUT] dito, **refeito pela bancada e marcado NÃO-CEGO** (os valores de aud_6 são referência, não fonte)».
