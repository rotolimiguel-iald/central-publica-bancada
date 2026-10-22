# Cético C-05 (PE reduzida = Kerr V2 + dtau) — 23/09/2026
Fontes lidas: bis/e3_kerr_continuation/{kerr_model.py,CONFIG.json,MANIFEST.json}; cache/E3_KERR220_CALIBRATION_V2/{COST.json,public_psd/COMPARISON.json,CONVERGENCE.json};
cache/E3_KERR220_CALIBRATION_V1/welch/FAILURE.json; C5_IMR_CONTROLS.json; bis/E3_CALIBRATION_NOISE_METADATA_V1.json; bis/e3_blind_prepare/READINESS.md;
PORTAO_DA_AMPLIACAO_V1.json (sha256 710028a7…); ENTREGA_013BIS_B3 (tabela N); ORDEM_013BIS l.194–196; cache/gwosc (só GW250114 O4b).
REAL: Kerr V2 8 params (sem dtau), 638,3 s parede/1 thread, nlive 512, PSD PÚBLICA NRSur (não off-source), GW250114 (SNR~77); Welch/off-source FALHOU condicionamento (2,55 s).
REAL: nproc=48; 125 GB. Ordem fala 22–28 workers [INPUT].
REAL: contagens 170/620/2140 = sigma_inj 0,058 (INPUT ilustrativo GW250114-like). Cegos: SNR 12,1–16,8, sigma_med 0,29–0,39 (fit E0).
Recontagem @48×638 s: sigma_inj 0,30 → R-LIN 4.410 (16,3 h); R-MOD 16.440 (60,7 h); R-B 57.110 (210,9 h). sigma 0,24 → 10,4 / 38,8 / 134,9 h.
REAL: strain dos cegos NÃO baixado (downloads=0); cegos são O4a, ruído em cache é O4b. C5_IMR_CONTROLS = 1 onda por família, fonte única (39+33, 403 Mpc).
