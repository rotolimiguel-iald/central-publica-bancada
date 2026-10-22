# CÉTICO 1 — achado «convenção de poder declarada, não aplicada» (ORDEM 013-bis, §4.0, l.125/131/137/139)

Veredito: refutado = false. Gravidade: IMPORTANTE (mantida).

Refeito por script (22/09/2026):
- z_0,90 = 1,28155; (5 + 1,28155)²/25 = 1,57832 — igual a REFEITOS_REVISAO.json `fator_N90_N50_filtro_casado`.
- l.131 «~2.100 / 669 / 618 / 166»: A2_tabela_5sigma.csv `N_5sigma_same_mix_matched_O4` = 2108/669/618/166 = E[z]=5 = poder 50 %. Sem rótulo. Idem «112/81/78/44» (contra a leitura), que também são E[z]=5.
- l.137 «17.578 — inviável»: d2_resultado.json cases[4] = {σ_meas 0,0803, σ_jit 0,019, N_LRT_power50 17578, N_LRT_power90 null}. Vem logo depois de «N₉₀ = 59 / 38 / 21» (que SÃO power90: cases[1] 59, cases[2] 21) — o leitor lê 17.578 como N₉₀; é N₅₀ e o N₉₀ não foi simulado.
- l.139 «~130 / ~33 / ~40 / ~10»: RENDIMENTO_E_5SIGMA.json N_5sigma_SNR_RD_50 = 131,2 / 38,2 / 43,2 / 10,3 (poder 50 %); REFEITOS `3G_N5_RB_ancora_SNR40.0.N90_SNR50` = 207,3. «5–9»: d2 cases[7] = N50 5 / N90 9 — par sem rótulo.
- N90 GW250114-like (REFEITOS `GW250114.N90_like`): R-B 336,5 · R-MOD 97,6 · R-RAIZ-0 96,5 · R-LIN 25,9. N90 mistura (`catalogo31_gauss.N90_mistura31`): 3.254 · 1.036 · 954 · 257.

Por que IMPORTANTE e não BLOQUEANTE: E0 (l.148) e E2 (l.170) já fixam «N_alvo a 90 %» para o registro; a ambiguidade está no §4.0, onde a bancada pode ancorar a leitura de N em números de 50 % (l.131, l.137, l.139). Não induz erro de física, mas induz registro de N_alvo errado por fator 1,58.

Correção FINAL (ver StructuredOutput).
