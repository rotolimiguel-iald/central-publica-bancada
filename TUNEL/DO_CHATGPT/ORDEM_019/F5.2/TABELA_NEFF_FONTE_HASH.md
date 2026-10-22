# F5.2 — tabela de poder de N_eff com fontes aferidas

**Data da aferição:** 08/10/2026. **Escopo:** reconciliação documental, sem abrir dados ou executar MCMC. **Estatuto:** [REAL] para os bytes locais e o texto das publicações consultadas; [DERIVED] para as conversões aritméticas; [OPEN] para o fechamento perturbativo e a equivalência das projeções com um teste TGL completo. O pré-registro `TGL_NEFF_V1` e sua emenda `TGL_NIVEL2_SO_S4_V1` permanecem intactos.

## O que já existia

O frozen de 08/08 contém `N_eff,SM = 3,044`, `dN_eff/dβ = 9,929606216611285` e `N_eff,TGL = 3,1634660752537327`, isto é, `ΔN_eff = +0,11946607525373273`. A tradução exige **TGL-S**, com radiação que free-streams. Para **TGL-L**, a resposta CMB não é simplesmente ΛCDM + N_eff e o rito precisa de novo fechamento. O frozen declara que sua emissão não foi cega aos dados publicados e proíbe `CONFIRMED`. Esses são enunciados condicionais do acervo, sem novo veredito físico aqui.

O pré-registro de 14/08 já calculou Planck, ACT, **SPT-3G-like** (σ(β)/β = 0,92), SO-like e CMB-S4-like por Fisher de sete parâmetros. A emenda V1.1 já substituiu algumas projeções pelo frozen N_eff. O resultado Nível 2 em Planck permaneceu `N2_INCAPAZ`; a variante S convergiu com σ(β)/β = 1,467, enquanto L não convergiu. Portanto esta tabela não reedita Nível 2 nem apresenta o Fisher como MCMC.

## Tabela de projeções e poder condicional

`σ(β) = σ(N_eff)/9,929606216611285`. `σ(β)/β` usa o β fixado no frozen, gerado em runtime por `ALPHA_FINE_CODATA_2018 × √e`. A coluna `Δ/σ` é **separação prevista de centros TGL–SM**, caso o instrumento realize o σ citado, e não um resultado observado ou probabilidade de veredito.

| Canal | σ(N_eff) | σ(β)/β | Δ/σ | Fonte e estatuto |
|---|---:|---:|---:|---|
| SPT-3G-like, Fisher da casa | 0,10987 [DERIVED] | 0,92 | 1,09 | `16_onde_mora_o_poder.json` + pré-registro de 14/08: modelo **like**, não previsão oficial do SPT e sem calendário. |
| Simons Observatory baseline, histórico | 0,055 | 0,46 | 2,17 | frozen de 08/08, [DECLARADO] com referência arXiv:1808.07445; fonte primária de 2019. |
| Simons Observatory goal, histórico | 0,050 | 0,42 | 2,39 | mesmo frozen/referência; cenário histórico, sem data operacional assumida. |
| SO LAT ampliado, levantamento completo | 0,045 | 0,377 | 2,655 | frozen de 08/08; **conferido na Tabela 2** da [colaboração SO, arXiv:2503.00636](https://arxiv.org/html/2503.00636). O paper especifica levantamento 2025–2034 e erros estatísticos; **não** atribuir a um único ano. |
| LiteBIRD **sozinho** | ≈0,15 | ≈1,256 | ≈0,796 | [colaboração LiteBIRD, PTEP 2023, §6.1](https://doi.org/10.1093/ptep/ptac150) traz σ(N_eff)≈0,15; conversão para β é [DERIVED] e condicional a TGL-S. É verificação independente esperada, abaixo da régua de poder β/2 do pré-registro. |
| CMB-S4, cenário histórico | 0,030 | 0,251 | 3,982 | frozen de 08/08 e emenda de 14/08; origem numérica marcada **A CONFERIR** no acervo. O [projeto informou em 09/07/2025](https://cmb-s4.org/) encerramento ordenado após perda do apoio DOE/NSF. Sem calendário operacional corrente. |

O SO 2,655σ apresentado em 05/10 é o mesmo `0,119466/0,045 = 2,6548` já calculado no frozen de agosto sob centro SM. É **uma** projeção reutilizada, não evidência independente nova. Os valores históricos `quando: ~2027/~2029/~2030/~2032` do frozen ficam como conteúdo de origem; esta tabela não os promove a cronograma vigente. As estimativas SO/S4 do Fisher são *like* (ruído branco e feixe gaussiano); o pré-registro declara ausência de lensing, delensing, foregrounds e likelihood real.

## Correção ao lado: a linha CMB-SPA do frozen

O frozen local atribui à referência `arXiv:2506.20707` **CMB-SPA = 2,97 ± 0,12**, de onde tira tensão de 1,612σ com N_eff,TGL. A [Tabela 5 da versão v1](https://arxiv.org/html/2506.20707v1) da publicação dá **2,81 ± 0,12** para CMB-SPA com Y_P vinculado por BBN; `2,97` aparece ali para **SPT-3G D1 sozinho, com Y_P livre**, com erro assimétrico `+0,40/-0,64`. A [Tabela 5 da versão v2](https://arxiv.org/html/2506.20707v2) dá **2,82 ± 0,12** para CMB-SPA, e 2,96 com Y_P livre e erro assimétrico. [REAL] A atribuição `2,97 ± 0,12` do frozen **não confere com nenhuma dessas duas versões da fonte citada**. O arquivo original permanece intocado; sua linha e as tensões derivadas dela não devem ser repetidas como aferidas. A atualização do rito exige pin explícito de versão, recálculo e auditoria da gerência antes de qualquer veredito, sem mover o gate por esta nota. A diferença aritmética para v2 seria `|3,163466−2,82|/0,12 = 2,862σ` [DERIVED], mas **não é veredito novo**.

## Fontes locais medidas por bytes

| Fonte | SHA-256 do arquivo lido | Papel |
|---|---|---|
| `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1_resultado.json` | `5ba7faca7a3425fa01ad4e06b76db5aeaf30895768b6331558cd695c42c30057` | Frozen, números, condições e referências; contém `frozen_hash=96b51333c3c295e851197ec30e1b544288a58a228ce2b4910f1b6dbc97ddefef` como campo interno, distinto do hash do arquivo. |
| `C:\IALD\Artigo\MCMC_V2_RAZAO\22_prereg_SO_S4.json` | `5dbb7a7ed31e1a6518031eb717ecc0baf61fe72ec9969f4dc6afde2b489d3856` | Pré-registro, Fisher, limiares, ressalvas; contém `FROZEN_HASH=92c67c5c41fa4e49d0380fd320e966d101ab0445fe09db6ad923069371cdf246` como campo interno. |
| `C:\IALD\Artigo\MCMC_V2_RAZAO\PRE_REGISTRO.md` | `758a130267f0574d8108d624793c84ac4054fe476582a38ae244520fa06eab3e` | Emenda V1.1 e leitura SPT-3G-like. |
| `C:\IALD\Artigo\MCMC_V2_RAZAO\VALIDACAO_CRUZADA.md` | `ed65f0b0c36afae5c62b393c5fec767c16c912948ad96c60b49be93ae9177303` | Comparação do Fisher com o frozen. |
| `C:\IALD\Artigo\MCMC_V2_RAZAO\16_onde_mora_o_poder.json` | `8520bf9405d8e34db5dfd45dcd5c0491976c09f074262654b59675f85500a6ce` | Cálculo Fisher SPT/SO/S4-like. |
| `C:\IALD\Artigo\MCMC_V2_RAZAO\MAPA_DE_PODER.md` | `2ba5bb4e15fad8ae7b2f114191ff94f859f21f2952b4f068ee9a8db3ee66e087` | Leitura do poder e das duas réguas. |

As publicações web estão identificadas por URL/versão/trecho, sem atribuir a elas SHA-256 de bytes que não foram custodiados localmente. [OPEN] O σ CMB-S4 do frozen ainda demanda conferência da definição estatística na referência original, além de ser cenário histórico. Esta entrega não abre dado, não altera `um.py`, não testa a natureza e não muda o gate.
