# F1b — reprodução histórica independente T/F4 D1b

[REAL — reprodução numérica local] Os três ajustes históricos da família T_dr2_cc, núcleo D1b, foram reproduzidos dentro das tolerâncias congeladas. Nenhum veredito científico foi emitido.

## Resultado

| Modelo | χ² arquivado | χ² independente | diferença | H0 independente |
|---|---:|---:|---:|---:|
| lcdm | 29.01667860403752 | 29.01667862716304 | +2.313e-08 | 68.53169343668 |
| tgl | 39.40979766861820 | 39.40979769971895 | +3.110e-08 | 68.43852438280 |
| livre | 28.94597631703161 | 28.94597634072850 | +2.370e-08 | 68.52501235062 |

| Estatística arquivada reproduzida | Independente | Diferença |
|---|---:|---:|
| beta_livre | 0.00094705573050955 | -3.822e-12 |
| sigma_beta_JtJ | 0.00355116574135674 | +1.396e-14 |
| delta | -0.0110842446702936 | -3.822e-12 |
| z_delta | -3.12129747739084 | -1.064e-09 |
| z_perfil_beta_tgl | 3.23478304666487 | +1.144e-09 |
| z_ganho_da_lei | -3.22383608028633 | -1.237e-09 |
| custo_por_nat_medido | 0.000905517406672752 | -3.661e-12 |

Os valores acima preservam a definição histórica dos estimadores. Reproduzir o cálculo não acrescenta nova incidência física nem reabre o ramo como teste. β_TGL foi calculado em runtime como α_CODATA2018√e; o ramo β livre é apenas o diagnóstico arquivado.

## Entradas, suporte e independência

A likelihood soma Planck comprimido (Chen2019,3×3), DESI DR2 (13×13 completa) e 32 cronômetros. **Não há SH0ES, calibradores, Pantheon ou outro bloco de escada nesta família.** Os cronômetros usam diag(σ²), como a Fase4; a covariância sistemática completa não integra esse alvo histórico. Não foi substituída pela Fase7. A independência entre os três blocos é a fatorização histórica [INPUT], não foi inferida deste acordo numérico.

O código novo T4_reproduzir.py usa NumPy/SciPy. Não importou ou executou um.py, os motores originais, seus backups ou seus auxiliares de ajuste. A tabela CAMB congelada foi reutilizada como dado de entrada com hash, portanto a independência é da implementação das previsões/integrais/likelihood/ajuste, não uma geração independente do CAMB. As origens e hashes de cada cópia estão no protocolo.

Preservados: β apenas na lei, c=0, z* da lei=1089.95, E(z) e aproximações históricas, covariâncias, limites declarados e suporte efetivo CAMB. Priors declarados: H0[50,90], ωb[.015,.030], ωc[.08,.18], β[−.05,.05]; suporte CAMB: H0[60,76], ωb[.02025,.02475], ωc[.102,.138]. Não houve evidência nem renormalização de prior nesta unidade. A tabela continua recusando extrapolação.

Diferença numérica explícita: DM foi integrado por Gauss–Legendre64, com confronto GL128, em vez do Simpson cumulativo/interpolação cúbica original. O interpolador CAMB independente preserva Lagrange separável de seis nós (grau5). TRF, coordenadas escaladas, passo central .001 e covariância JᵀJ seguem o contrato histórico. A soma retangular25/35 de evidência não foi executada nem trocada por outro método.

## Verificação e recursos

400/400 pontos congelados de teste CAMB dentro do suporte. Erro relativo máximo entre as cinco grandezas: 6.544e-06, contra tolerância prévia1e−5. O erro da própria tabela em relação a CAMB é distinto da diferença de reprodução do fit.
Nos parâmetros arquivados TGL/livre, a maior diferença por bloco foi 3.049e-08. Esses confrontos precederam os ajustes. GL64/128 diferiram nos resíduos em no máximo 8.885e-14; nos mínimos, |Δχ²| GL128−GL64≤5.329e-14.
Convergência dos três ajustes registrada: lcdm: nfev=12, njev=5, status=3, sucesso=True, tgl: nfev=4, njev=4, status=2, sucesso=True, livre: nfev=4, njev=4, status=2, sucesso=True. Limite200 avaliações por modelo; sem GPU.
Tempo do programa, incluindo imports científicos: wall=1.503660s; CPU=0.796875s. Pico do processo Windows=79323136bytes (75.65MiB), incluindo bibliotecas; orçamento wall300s, uma thread, três modelos. O limite de projeto<64MiB refere-se aos arrays, não ao processo inteiro. O lançamento pela ferramenta levou2.0583s; distingue-se do cronômetro interno.
Ambiente: 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]; Windows-11-10.0.26200-SP0; NumPy 2.4.3; SciPy 1.18.0; executável C:\Python314\python.exe. Variáveis BLAS/OMP/NumExpr fixadas em1.

## Pré-registro, proveniência e limite

Protocolo/hash congelados em 2026-10-06T01:24:12.835118+00:00; execução iniciada em 2026-10-06T01:24:46Z. Protocolo SHA-256: ee8760baee2d32ad6fd5de4036599d3d08ed143b46ade54b83afb3bdda3b1518. Código SHA-256: 08552c24d56f23cf04342bd8e41db61e5a9ce688af84ea3205ee53b3beb1c340. Ambos continuaram idênticos após o run.

A tentativa adicional de registrar o protocolo no MCP antes do run foi recusada por enumeração inválida de status EM_EXAME. O recibo original está em T4_RECUSA_REGISTRO_PREEXEC.json. O congelamento local ocorreu antes do cálculo, mas **não houve registro MCP prévio bem-sucedido dessa unidade**. A presente nota e o registro de conclusão não retrodatam o evento. Isso foi falha de escrituração, não divergência numérica; não se repetiu o fit para encobri-la.

Os resultados originais F4 não contêm hash completo do motor histórico, como já registrado no plano. O acordo dos números e dos blocos fornece verificação independente do contrato executável reconstruído, mas não inventa identidade binária do processo antigo. O θ_LCDM completo não consta do bloco-alvo arquivado: para esse caso foram confrontados χ², decomposição, H0 e K; θ_TGL e θ_livre completos foram confrontados.

Esta entrega cobre somente T/F4 D1b determinístico. D1a, posteriors, evidências e famílias P/Q/R/S permanecem fora desta execução; V_SH0ES não foi repetido. Não houve ajuste da teoria para aproximar os alvos, novos catálogos, acesso remoto, atualização do livro de multiplicidade ou movimento de gate. A confirmação física continua fora deste relatório.

Artefatos: T4_PROTOCOLO.json, T4_PREEXEC_HASHES.json, T4_reproduzir.py, T4_RESULTADO.json, T4_ALVO_HISTORICO.json e T4_MANIFESTO.json. Código/resultados completos, covariâncias e fontes por hash permitem revisão da coordenação.
