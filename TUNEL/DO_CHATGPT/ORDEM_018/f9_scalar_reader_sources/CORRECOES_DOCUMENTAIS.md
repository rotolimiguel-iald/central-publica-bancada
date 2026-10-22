# Fase 9 escalar — fontes dos cinco leitores e correções ao lado

[REAL documental] Os cinco valores centrais e as incertezas usados no V1 escalar têm correspondência nos resumos primários arquivados por SHA-256. Três arquivos foram reutilizados e dois coletados agora. Não houve reexecução do composto nem admissão automática.

| Leitor | Valor publicado (km/s/Mpc) | Transformação local de sigma |
|---|---|---|
| SH0ES R22 v3 | 73,04 ±1,04, com sistemáticos | identidade |
| CCHP v3 | 70,39 ±1,22(stat) ±1,33(sys) ±0,70(sigma_SN) | quadratura =1,935794410571536 |
| SBF v2 | 73,8 ±0,7(stat) ±2,3(sys) | quadratura =2,4041630560342613 |
| Masers v2 | 73,9 ±3,0 | identidade |
| TDCOSMO v4 | 71,6 +3,9/−3,3 | média dos lados =3,6 |

[KNOWN] Resultados publicados pelos autores. [REAL] Transcrição, aritmética elementar dos erros e integridade conferidas aqui. Não reproduz medições ou verossimilhanças dos artigos.

## Correções e limites

**D1_CCHP_METHOD_LABEL** — L2 tipo diz TRGB+JAGB+Cef, mas70.39 é TRGB sozinho na fontev3. cefeida=false já existe no congelado; erro do rótulo não implica mudança automática da classificação numérica.

**D2_SBF_DEPENDENCY_FLAGS** — L3 tem grupo_SN=true e grupo_4258=false. A fonte descreve rota independente de SN Ia, calibrada via NGC4258. Revisar interpretação dos grupos e regra de covariância antes de novo composto; não apenas inverter flags.

**D3_MASER_SHARED_OBJECT** — L4 tem grupo_4258=false, mas NGC4258 integra as seis galáxias publicadas. Objeto compartilhado não determina sozinho covariância; requer rastrear medições reutilizadas e pesos.

**D4_TDCOSMO_EXTERNAL_CONSTRAINT** — L5 tem grupo_SN=false, embora Pantheon+ forneça restrição Omega_m. Isso não equivale à calibração SN da escada nem fixa covariância cruzada; a dependência deve constar explicitamente.

**D5_ERROR_COMPRESSION** — Quadraturas CCHP/SBF e média dos lados TDCOSMO reproduzem erros do V1. São compressões locais documentadas, não recuperação da verossimilhança original nem prova de independência dos componentes.

**D6_MEMBERSHIP_IS_NOT_HASH_VERIFICATION** — Runner linhas65,175,177 carrega ALV e usa presença da chave para REAL por hash/contagem de declarados. Nesse ponto não verifica bytes das fontes nem revisão da covariância. Não criar ALVOS_FASE9_LIDOS.json a partir deste vínculo como admissão.

A presença de NGC4258 em métodos distintos e o uso de Pantheon+ não permitem inventar covariâncias. O próprio V1 qualifica a covariância cruzada como estimativa de desenho. Os resumos não a promovem a covariância publicada. A simetrização TDCOSMO preserva o resumo escolhido, não a verossimilhança.

O resultado oficial continua INCONCLUSIVE_SYSTEMATICS. ALVOS_FASE9_LIDOS.json não foi criado; V1 e runner intactos; z_disc/evidência não recalculados. d72/P3 e a comparação conjunta ROOT permanecem separados.

## Fontes primárias

- [L1_sh0es_r22](https://arxiv.org/abs/2112.04510v3): arquivo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\sh0es_2022.html, SHA-256 df9136da862ef625ce692d6a6813b069ccdc9d7ce93537256fedcc9457c2d7d0, linhas 32,43,132.
- [L2_cchp](https://arxiv.org/abs/2408.06153v3): arquivo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\cchp_2025_v3.html, SHA-256 eb1b6689f13dbceaaa9e919ad68682bc75cf8f8cd4bf78ced3180a39b8207fa6, linhas 30,41,129.
- [L3_sbf](https://arxiv.org/abs/2502.15935v2): arquivo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_scalar_reader_sources\sbf_2502.15935v2.html, SHA-256 b61012efc5238c0e701baf9a442bb697deaec041fb3f1016b91365bb164d4946, linhas 30,41,129.
- [L4_masers](https://arxiv.org/abs/2001.09213v2): arquivo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_scalar_reader_sources\masers_2001.09213v2.html, SHA-256 041b7bd9bf8a4a31eec2d81f08f28a0734c72c9aec6c80821c408dfe712fddc7, linhas 30,41,128.
- [L5_tdcosmo](https://arxiv.org/abs/2506.03023v4): arquivo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\tdcosmo_2025_v4.html, SHA-256 b04dfc911acb4ad357224a3f2b432b407a109254277993f90a68a0e56137bf02, linhas 30,41,129.

O JSON registra bytes, hashes, metadados congelados, procedência textual dos erros e limites. Revisão independente entregue separadamente.
