# E45A — reprodução histórica relativa P4 / P5 sombra

[REAL — reprodução numérica local] Concluídas 12 grades: a primeira P4/TGL n25 foi reutilizada; 11 unidades novas, sequenciais, uma thread e limites 600 s/512 MiB. Nenhum fit, MCMC, F9 ou grade acumulada. Os números abaixo reproduzem o contrato histórico; não são veredito científico.

## Integrais reduzidas

| Família | Modelo | lnZ n25 | lnZ n35 | Δ35−25 | Δ25−arquivo |
|---|---|---:|---:|---:|---:|
| P4_d1b | lcdm | -28.990590108119 | -28.990590180435 | -7.23155757e-08 | 3.12094173e-09 |
| P4_d1b | tgl | -20.970218677401 | -20.970218732214 | -5.48125634e-08 | -1.59995466e-08 |
| P4_d1b | livre | -23.216178625710 | -23.213361755213 | 0.0028168705 | -1.15940821e-08 |
| P5_sombra | lcdm | -761.687199099196 | -761.687198853603 | 2.45593696e-07 | 1.63488608e-07 |
| P5_sombra | tgl | -747.850257507562 | -747.850257776942 | -2.6938028e-07 | 2.45118372e-07 |
| P5_sombra | livre | -750.714648383404 | -750.710774874889 | 0.00387350852 | 2.40202098e-07 |

## Razões na mesma família

| Família | Razão | lnB n25 | lnB n35 | Δ25−arquivo |
|---|---|---:|---:|---:|
| P4_d1b | tgl_vs_lcdm | 8.020371430718 | 8.020371448221 | -1.91204883e-08 |
| P4_d1b | livre_vs_lcdm | 5.774411482410 | 5.777228425222 | -1.47150239e-08 |
| P4_d1b | tgl_vs_livre | 2.245959948308 | 2.243143022999 | -4.40546444e-09 |
| P5_sombra | tgl_vs_lcdm | 13.836941591634 | 13.836941076660 | 8.16297643e-08 |
| P5_sombra | livre_vs_lcdm | 10.972550715792 | 10.976423978714 | 7.67134907e-08 |
| P5_sombra | tgl_vs_livre | 2.864390875842 | 2.860517097947 | 4.91627361e-09 |

## Savage–Dickey e discretização

| Família | Razão | SD n25 | SD n35 | SD25−grade25 | SD35−grade35 |
|---|---|---:|---:|---:|---:|
| P4_d1b | tgl_vs_livre | 2.102377717933 | 2.288498971902 | -0.14358223 | 0.0453559489 |
| P4_d1b | lcdm_vs_livre | -5.774411668511 | -5.777228565417 | -1.86101516e-07 | -1.4019441e-07 |
| P5_sombra | tgl_vs_livre | 2.696249921630 | 2.831447823556 | -0.168140954 | -0.0290692744 |
| P5_sombra | lcdm_vs_livre | -10.972550812719 | -10.976424941280 | -9.69267866e-08 | -9.62565997e-07 |

[REAL] As diferenças SD são preservadas. A interpolação pontual de uma marginal grosseira não tem a mesma precisão da sua integral; os quantis de CDF de nós também dependem da malha. O JSON conserva as densidades e quantis 25/35. Igualdade exata Savage–Dickey exige suporte/prior condicional comum: as caixas numéricas centradas em fits de cada modelo são adicionais ao prior amplo.

- P4_d1b: maior |ΔlnZ35−25|=0.00281687049698; arquivo=0.00281687058063; diferença=-8.36450909e-11.
- P5_sombra: maior |ΔlnZ35−25|=0.00387350851531; arquivo=0.00387350906362; diferença=-5.48311618e-10.

[OPEN — caudas não medidas] O desenho histórico integra caixas ±6σ nos três parâmetros de fundo e todo o prior em β. A comparação 25/35 não limita a massa de probabilidade omitida fora dessas caixas. O suporte CAMB menor também foi preservado. Nenhuma ampliação ou correção de cauda foi introduzida.

## Alcance estatístico

[INPUT] P4 inclui Planck+DR2+SH0ES gaussiano. P5 sombra inclui Planck+DR2+Pantheon+SH0ES, 77 calibradores e 1580 SN não-calibradoras; não duplica o escalar SH0ES. Matrizes completas dentro dos blocos; covariância cruzada ausente e fatorização histórica explícita. CC está fora de ambas. Não são famílias sem escada e não devem ser multiplicadas como dados independentes.

[DERIVED] lnZ é reduzido pelas constantes gaussianas omitidas; em P5 M é perfilado. As constantes comuns cancelam nas razões da mesma família sob a mesma medida de M/limite de prior amplo compatível. Não se reivindica evidência absoluta normalizada. O diagnóstico diagonal-Laplace usa produto das variâncias marginais, não determinante da covariância completa; permanece separado no JSON.

[CORREÇÃO AO LADO — proveniência histórica] A abertura da ORDEM018 associa os diagnósticos de escada 5,26σ/−0,38σ de P5 aos lnB 8,02037 e 2,24596 de P4. São famílias distintas: a tabela acima mantém essa identidade. √Δχ² é estatística conjunta, e zβ é diagnóstico do ajuste β livre; nenhum é resíduo de previsão de fundo sem escada. Esses diagnósticos não foram recalculados aqui.

[REAL/DECLARADO] Foram reutilizados os centros e sigmas P45 independentes. O arquivo histórico reduzido não armazenou todos os centros/sigmas dos refits internos da evidência; a concordância é numérica no contrato, sem alegar geometria byte a byte idêntica.

## Custo e rastreio

Wall somado das 11 novas unidades: 904.881 s; projeção anterior 896.386 s, margem 2× 1799.958 s.
Das 12 grades, wall=908.978 s, CPU=893.391 s; pico máximo=165.594 MiB. Tempos somados de processamento não incluem esperas de coordenação.
Nós processados totais: 4016500. Checks: {"all_units_complete": true, "all_source_pins_intact": true, "all_result_hashes_match": true, "all_limits_pass": true, "all_n25_lnZ_reproduced": true, "all_n25_lnB_reproduced": true, "all_n25_SD_reproduced": true, "n25_n35_diagnostic_below_threshold": true, "max_grid_difference_reproduced": true}.

A falha NameError do controlador v1 ocorreu antes de qualquer subprocesso científico. Ficou preservada com backup/recibo; controlador v2 corrigiu apenas pathlib.Path e arquivos de continuação/estado. Pré-checagem pura e autorização posterior antecederam a retomada (mapas 430/431). Nenhuma grade científica foi repetida.

Fontes, hashes de cada grade, entradas, estado de campanha, ambiente e recibos individuais estão no manifesto e JSON consolidados. Kernel, originais e gate preservados.
