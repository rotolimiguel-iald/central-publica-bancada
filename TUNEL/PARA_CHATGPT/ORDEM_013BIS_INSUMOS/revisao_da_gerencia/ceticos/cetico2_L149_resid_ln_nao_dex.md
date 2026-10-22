# CÉTICO 2 — achado L149 (E0.3): «resíduo 0,24 dex» — NÃO REFUTADO

Fonte: medir/B_catalogos/rendimento_e_5sigma.py:29,33,35 — ajuste por np.polyfit(np.log(S), np.log(G)); resid = np.log(G) − (lnA + p·log S); 'log_resid_sd' = resid.std(). np.log é logaritmo NATURAL ⟹ a dispersão está em ln (nepers), não em dex.
RENDIMENTO_E_5SIGMA.json sigma_vs_snr_fit_31: A 3,02665; p −0,85992; log_resid_sd 0,24446; 31 eventos.
Refeito por script (dos 31 pares do JSON, σ arredondado a 4 casas): A 3,0249; p −0,8597; sd_ln 0,2444; sd_ln/ln10 = 0,1062; ajuste direto em log10: sd_dex 0,1062 (idêntico). Limiares da ordem conferem: σ≤0,06 → SNR≥95,6; σ≤0,10 → SNR≥52,8.
«dex» aparece no scratchpad só na L149 da ordem — não em SINTESE/CRITICO/FRENTE_B_RESULTADO: a unidade nasceu na redação, não na medição.
Gravidade: IMPORTANTE (mantida) — número com unidade errada em ordem imutável que manda a bancada refazer.
Correção final: ver StructuredOutput.
