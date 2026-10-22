[REAL — ficha C2; readouts condicionais]

Existia: trajectory_recovery.py::fit/main, tgl_ringdown_unravelings.py::poisson_support, tgl_ringdown_prediction.py::prediction, prepare_empirical_noise.py::polynomial_whitener, C2_MAPEAMENTO_ANALITICO.md e C5_RECOLORED_NOISE.json.

Reusado: estimador de três inícios, fórmulas de predição, soma de Poisson, grade QNM e ruído arquivado; nenhuma reimplementação do kernel. Novo: mil trajetórias por célula, janela explicitada, agrupamento por intervalo de ruído no EP e diagnóstico de perda de SNR. Motivo: F1 pede distinguir uma realização do ensemble e medir a distribuição ajustada.

Resultados SHA256 9d734d976146188ae83a9557ae947f1021c7cfef26c49e998f39b1c1a128d691; adendo SHA256 5f6cc6bee61233c1476c1008054fb15aba20082484d72144de183e852ad35812; abertura SHA256 0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0. Reprodução e lacunas no adendo; axiomas N/A — sem Lean.
