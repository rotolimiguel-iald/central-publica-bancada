# F7.2 — errata ao lado do bloco J.4b de junho

[REAL documental, 08/10/2026] O original `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` permanece intacto (SHA-256 lido: `29c92b66b2fd6b4d589adbef4de86a67f979e03964b3f7ae892732a40ab395cd`; 1.216.423 bytes). Na linha 18393 há literalmente `'tau_star_bound_neutrino_s': 7.8e-10`. A linha 18392 ainda chama `8e-27 GeV` de projeção JUNO/DUNE. Esse valor de τ★ é uma entrada literal histórica do bloco J.4b, **não** uma cota calculada a partir dos limites publicados e **não** uma medida da TGL.

[KNOWN] Beccaria–Ternes, arXiv:2606.13362v1, publica depois dos scripts de junho o limite `Γ₂₁ = Γ₃₁ < 4,1 × 10⁻²⁷ GeV` para `n = −2`, `E₀ = 1 GeV`, 90% CL, sob o cenário do artigo. O PDF foi custodiado na V2 da F7.2; esse número é limite do modelo do artigo, não cota de τ★ da TGL.

[OPEN] A tradução do operador físico da TGL para o dissipador em matéria e para a verossimilhança do experimento. A linha literal não deve ser usada como `tau_star_limit_s` no canal: o canal V2 devolve `null` e `SEM_LIMITE_TGL`. Os originais científicos de junho não foram editados; esta correção fica ao lado no mapa.
