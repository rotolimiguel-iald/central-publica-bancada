# Auditoria ORDEM 013-bis — Parte A (F0–F8) — conferência da gerência, 23/09/2026

Ferramentas: verify_hashes.py (128/128 sha256 citados em M1–M6/MA/ERRATA conferem em disco); v1_intact.py (34/34 sha16 do ESTADO_AUDITADO.json intactos); cadeias supersedes 11/11 conferidas; RD.tar.gz sha256 9810e0e45cd35824... lido.
Replay próprio do bundle v3_1 em C:\tmp\aud013bis_v31: verify_delivery PASS 231; unit_checks PASS (3.95e-16 / 3.48e-16); reproduce_c6.py --run (WSL /opt/lal_env, cache só leitura): 75 linhas, max_lnB_difference 0.0, 73.18 s, temporário removido (C:\tmp\aud013bis_out\C6_v3_aud.json).
Extração do zip no scratchpad profundo FALHOU (FileNotFoundError) — o aviso MAX_PATH do README é real.

F0: C5_ANEXO_PROCESSOS.json NÃO EXISTE. Substitutos: bis/F0_SNAPSHOT_*Z.json (17:03, 17:35, 18:14, 18:46Z), F0_PRESTOP_20260922T215825Z.json (processos: []), F0_CLOSED_20260922T215825Z.json (signals [], files com sha256, scientific_use ANNEX_ONLY).
Trajetória medida: continuous_source_curves/IMRPhenomXPHM 22384/22384 concluído 18:36:56Z; SEOBNRv4HM curvas 5088/8520 último PROGRESS 19:59:43Z; phase_real_refined/IMRPhenomXPHM 19856/22384 último PROGRESS 20:00:30Z. Dois grupos pararam INCOMPLETOS no mesmo minuto, sem causa registrada; checkpoint 20:15:57Z ainda dizia "F0_old_jobs: May still run"; RAM usada 108 GB (17:03Z) -> ~1,5 GB (21:58Z). [CONJECTURE] reinício/desligamento da VM WSL não registrado.
Primeiro job pesado da Parte B (Kerr controller) terminou 22:06:43Z com 394 s de parede -> começou ~22:00Z, depois do PRESTOP 21:58Z. Tempo dos jobs antigos fora das 40 h (Part B start 19:06:33Z).

F7 medido: 0 arquivos > 25.000.000 B fora de cache\ de 1º nível; 57 removidos (2.809.549.015 B) em 4 DUPLICATAS_REMOVIDAS.json (17+2+2+36); 4 mkdtemp ausentes; MANIFESTO_DOWNLOADS_013BIS_v2.json 1064 entradas todas com licença (cc-by-4.0 752+19+9+1; MIT 24; próprios NOT_ASSIGNED 259); REGISTRO_C4_EMENDA NONBLIND ESS>=100; ERRATA_contrato cobre C6a, C4c, 6×C5 + C4a.
