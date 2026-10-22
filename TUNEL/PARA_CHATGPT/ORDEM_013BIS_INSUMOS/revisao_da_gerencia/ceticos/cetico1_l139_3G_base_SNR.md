# CÉTICO 1 — achado estatistica_poder sobre a l.139 (§4.0 (i), 3G) — 22/09/2026

refutado = false · gravidade mantida = IMPORTANTE

## Refeito por script (Python, 22/09)
- rendimento_e_5sigma.py:57-61: sig40 = min(G) = 0,0580 (GW250114), posta em SNR_RD = 40 («pos-fusao ~40»); N_at(s) = 25/(dmed/(0,058*40/s))². RENDIMENTO_E_5SIGMA.json R-B: N_SNR50 = 131,17; N_SNR100 = 32,79; R-MOD 43,2/10,8; R-RAIZ-0 38,2/9,5; R-LIN 10,3/2,6. Tudo Σz² = 25 → poder 50 %.
- Com 0,058 ≙ SNR_RD = 2/0,058 = 34,48 (equivalência que a própria ordem usa na l.125 / SINTESE §3.1): N_SNR50 = 97,6; N_SNR100 = 24,4 (34,28 → 96,5/24,1; a diferença é arredondamento). ✓ achado (i).
- Fator N90/N50 = (5+1,2816)²/25 = 1,578: 131,4→207,3; 32,8→51,8; R-MOD 43,2→68,2; R-RAIZ-0 38,2→60,3; R-LIN 10,3→16,2. A l.125 declara «Convenção de poder desta ordem: 90 %»; a l.139 é N50 sem dizer. ✓ achado (iii).
- C5_FISHER.json same_source_R_B: parameters 68,1 M☉, χ 0,68, source_status ILLUSTRATIVE_INPUT, banda 20–2048 Hz, scope «individual reference PSD; no detector network»; z_local ET 3,856 / CE 7,028 em snr_if_O4_were_40 = 381,9 / 698,2 — isto é, a fonte ESCALADA para SNR40 em O4. aud_4.txt:74 e :144: as células SNR40 são 4,2–4,4× (O4) / 2,5–2,6× (O5) a fonte de referência a 403 Mpc na janela de 10 t_M, que o auditor lê como o GW250114 (:23, :133). ✓ achado (ii): «um só evento» é um evento ~4× o GW250114 nessa janela.
- Reforço não citado pelo revisor: SINTESE l.112 (frente A) dá N GW250114-like em ET = 2,3 (⇒ z ≈ 3,3 por evento), o que só é compatível com z = 3,86 se a base de SNR do Fisher (fonte fixa, 20–2048 Hz, 1 PSD) NÃO for a janela de 10 t_M das injeções. É exatamente a base que a errata 4 (l.48) manda declarar e a l.139 não declara.
- Berti et al. (berti_bhspec.txt:14905-14908): «a non-negligible fraction of ∼10² events/yr will have SNR_RD ≳ 50, and O(10) events/yr ... ≳ 100», citando [1184] (Fisher, população sintética); a definição temporal do SNR_RD (início da janela) não está no trecho — base não dita. ✓.
- «~1,3 ano / ~3,3 anos» contradiz a l.135 («esta ordem fixa N_alvo e o critério de qualidade, nunca anos»).

## Por que não BLOQUEANTE
Os números são cenário 3G, sem veredito; não movem gate nem decidem partição. Mas a inconsistência interna (l.125: 0,058 ≙ 34; l.139: 0,058 @ 40), a convenção de poder trocada dentro da mesma seção e o «um só evento» sem escala dariam à bancada um N 1,6–2,1× menor que o da própria ordem. IMPORTANTE.

## Correção final (texto a substituir na l.139, do «R-B com um só evento» até «R-LIN ~10;»)
R-B com a fonte de referência da C5 (68,1 M☉, χ 0,68, ILLUSTRATIVE_INPUT; um detector, 20–2048 Hz; fonte fixa; escalada a SNR40 em O4, o que na janela de 10 t_M vale 4,2–4,4× o GW250114 — aud_4), z = 3,86 (ET) / 7,03 (CE) `[DERIVED, teto de fonte fixa; não é «um evento GW250114-like»: a frente A dá 2,3 GW250114-like em ET]`; população 3G com a âncora σ(δτ̂) = 0,058 do GW250114 posta em SNR_RD = 40 (B; com SNR_RD ≈ 34 pela equivalência 2/ρ da l.125: ≈ 97 / 24): **~130 eventos com SNR_RD ≥ 50 ou ~33 com SNR_RD ≥ 100 a poder 50 % (≈ 207 / 52 a 90 %, convenção desta ordem)** — a bancada declara a base do SNR_RD de Berti/Bhagwat (início da janela, rede) e converte para a escala do GW250114 (F4); R-MOD/R-RAIZ-0 ~43/~38 a 50 % (~68/~60 a 90 %); R-LIN ~10 (~16); taxas ~10²/ano (SNR_RD ≳ 50) e O(10)/ano (≳ 100) são [KNOWN] de ordem de grandeza (Berti et al. §7.1, Fig. 76); **nenhum «ano» nesta linha — N_alvo, nunca prazo (l.135); prazo só como cenário com banda, se a bancada o registrar.**
