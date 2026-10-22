# CÉTICO 2 — achado «anos como promessa» (ORDEM 013-bis l.135 §4.0(g) e l.139 §4.0(i))

Veredito: NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE.

## Refeito por script (fonte: medir/B_catalogos/RENDIMENTO_E_5SIGMA.json; f90 = (5+1,28)²/25 = 1,5775)
taxa pSEOBNR O4ab = 14,483/ano; O5: g_lo=1,5625 → g³=3,815 → 55,2/ano; g_hi=1,7857 → g³=5,694 → 82,5/ano.
R-LIN N_O5 (50 %): 51,1–66,7; (90 %): 80,5–105,2.
R-LIN anos O5 coerentes (N e taxa com o MESMO g): 50 % → 0,62–1,21; 90 % → 0,98–1,90.
  JSON «anos_O5_a_taxa_x4.6..5.7» = [0,924; 1,207] divide os dois limites por g_lo³ apenas (rendimento_e_5sigma.py:61; CRITICO I6).
3G R-B: N(SNR_RD≥50) = 131,2 (50 %) → 206,9 (90 %); N(SNR_RD≥100) = 32,8 → 51,7.
  anos: 1,31 / 3,28 (50 %) → 2,07 / 5,17 (90 %), a 10²/ano e 10/ano [KNOWN, ordem de grandeza, Berti 2026 §7.1 ← Bhagwat 2023].
Âncora dos N de 3G: σ=0,058 do GW250114 em «SNR_RD~40 pós-fusão»; aud_4.txt:74 mede ~17,7 na janela de 10 t_M → âncora [DERIVED] otimista, não dita na l.139.

## Por que o achado se sustenta
1. l.125 fixa «Convenção de poder desta ordem: 90 %»; l.135 dá para o R-B as duas convenções («N₅₀; 79–137 a 90 %»), mas o «~1 ano» do R-LIN é a 50 % e sem banda; l.139 dá 130/33 a 50 % sem o dizer. Inconsistência interna com a própria convenção.
2. l.216 proíbe «5σ alcançável em N anos» como promessa e só admite «cenário [DERIVED] com a banda»; l.135 termina «esta ordem fixa N_alvo e o critério de qualidade, nunca anos» — e a mesma frase contém «R-LIN fecha em ~1 ano». «~1» não cobre 0,62–1,90.
3. A ordem será imutável; «fecha em ~1 ano» é verbo de promessa que a bancada herda como fato.

## Tentativas de refutação e por que falham
- «O parágrafo já está sob [DERIVED, cenário]»: o rótulo cobre o parágrafo, mas a l.216 exige banda, e o R-B a tem no mesmo parágrafo — o R-LIN não. Assimetria dentro da mesma linha.
- «10²/ano já é a banda»: é ordem de grandeza [KNOWN]; o defeito principal da l.139 não é a taxa, é o poder (50 % contra a convenção 90 % da l.125), que muda 1,3→2,1 e 3,3→5,2.
- Não é BLOQUEANTE: nenhum número fabricado, nada da partição do operador, executável. É IMPORTANTE: inconsistência interna explorável.

## Correção FINAL (texto exato)
l.135, substituir: «R-LIN fecha em ~1 ano de O5 estatisticamente, mas é EXCLUDED_IF_UNIVERSAL na C1 e a mais penalizada no catálogo (ln B −8,22).»
por: «R-LIN atinge N₉₀ = 81–105 de mistura (51–67 a 50 %) — a 55–83 pSEOBNR/ano isso é 1,0–1,9 ano de O5 a 90 % (0,6–1,2 a 50 %), cenário [DERIVED] com a banda de taxa, nunca promessa —, mas é EXCLUDED_IF_UNIVERSAL na C1 e a mais penalizada no catálogo (ln B −8,22).»
l.139, substituir: «**~130 eventos com SNR_RD ≥ 50 (~1,3 ano a 10²/ano) ou ~33 com SNR_RD ≥ 100 (~3,3 anos)**; R-MOD/R-RAIZ-0 ~40; R-LIN ~10;»
por: «**N₉₀ ≈ 207 eventos com SNR_RD ≥ 50 ou ≈ 52 com SNR_RD ≥ 100 (131 / 33 a 50 %)**; com as taxas [KNOWN] de ordem de grandeza (10²/ano e 10/ano) isso é ~2 / ~5 anos de ET+CE a 90 % (~1,3 / ~3,3 a 50 %) — cenário [DERIVED], não promessa; âncora σ = 0,058 do GW250114 posta em SNR_RD ≈ 40 [DERIVED, otimista: ~17,7 na janela de 10 t_M, aud. 4]; R-MOD/R-RAIZ-0 ≈ 60–70 a 90 % (~40 a 50 %); R-LIN ≈ 16 (~10);»
