# Pré-registro Fase 9 — V2 proposta por gerador novo (R7)

**Estado:** `RASCUNHO_NAO_CONGELADO`. **Spec SHA-256:** `5a2318bb5cfeb4671392b91263f01551e713766b6cb99a46f349bbb742bad503`.

[REAL documental] Gerado do V1 pinado. Não admite fonte, não abre dado, não roda composto e não move gate. F3.4 e NAT-22 precisam da palavra do operador antes de congelar; D-H precede a abertura e D-J dá o nome final ao token.

## Lei e leitores

`mu_do_rito: q→0 (Thomson; Teorema da Escala)`. β₀=α(0)√e em runtime = `0.012031300400803142`; K recalculado=`1.0838071748529643`; K V1=`1.0838071748529643`; diferença=`0.000e+00`.

L4 decisório usa os **cinco** masers sem NGC 4258: `73,6 +3,1/−3,0` (Pesce+2020, Tabela 2, PDF pinado). Os seis são diagnóstico separado e nunca somados. L1b só substitui L1 na réplica R25; L6 é diagnóstico de sirenes. L2 é TRGB sozinho, com 24 SN Ia; L3 não depende de Cefeidas ou SN Ia como calibração; L5 partilha a restrição de Ωm do Pantheon+.

**Mapa TGL do observável:** a conversão dos H0 publicados de todos os leitores locais precisa de exame de verossimilhança sob TGL antes da admissão. A Eq. 1 de Pesce usa ΛCDM plano, Ωm=0,315; a fonte diz que Ωm∈[0;0,5] muda a distância em ≲1%. Isso não valida automaticamente o mapa TGL. Veja `observable_TGL_H0_map` no JSON.

## Covariância e poder (só σ)

Componentes: NGC 4258 `0,024⊕0,022` mag; TRGB na âncora `0,025` mag; sistemático CCHP `1,33`; SBF `0,032/0,033` mag [DECLARADO web]; SH0ES capado em σ_L1. SN L1–L2, Pantheon+ L1–L5 e âncoras HST secundárias seguem [OPEN]. A grade fixa λ_N, λ_T∈{0;0,05;…;1}, retém matrizes positivas e desempata pela primeira ocorrência. Sem correlação central.

| Família | σ mínimo | Poder BG1/BG2/BG3 no mínimo | σ máximo | Poder BG1/BG2/BG3 no máximo | λ_N,λ_T no máximo |
|---|---:|---|---:|---|---|
| Cinco decisório | 0.8035 | 6.623/5.679/5.554 | 0.9493 | 5.722/5.062/4.989 | 0.95,0.05 |
| Seis diagnóstico | 0.8025 | 6.630/5.684/5.558 | 0.9989 | 5.466/4.876/4.816 | 0.95,0.05 |
| Sem Cefeidas diagnóstico | 1.2654 | 4.395/4.049/4.035 | 1.4215 | 3.938/3.672/3.672 | 1.00,1.00 |

Cota GLS: σ_comb≤min σᵢ=`1.04`; poder BG1≥`5.269`. UNDERPOWERED por covariância não ocorre no primário × BG1 sob este contrato; pode ocorrer em BG2/BG3 ou sem Cefeidas. A ponta adversa de discriminação é o máximo na grade, possivelmente interior, não o canto. Pesos GLS, negativos e autovalor mínimo de ambas as pontas estão no JSON. Falsificação e tensão usam σ mínimo; dispersão falha em qualquer ponta.

## D5, executor e veredito

As σ de CCHP, SBF, TDCOSMO e L4 cinco são compressões locais gaussianas simétricas: não recuperam a verossimilhança original nem provam independência (**achado D5 da seq 696**). Preservar lados publicados +3,1/−3,0 e +3,9/−3,3 no vínculo. Sensibilidades c1: TDCOSMO lado 3,9 → 5,439 em diagnóstico de seis; SBF sem decomposição web → 5,718.

NAT-22 pendente. Executor observado: fundo marginalizado; z_δ por perfil −2lnL com log-det; lnB com n≥100 e conferência 100/200; z_disc por forma quadrática (histórico 4,2837; log-det diagnóstico 4,2818); σ_β média dos lados. Errata V1 ao lado: lnB(TGL/β-livre) convergido 1,97, não 2,24 com n=25.

`n_alvos_declarados` conta leitores sem **ambos** gate verificado e admissão do operador em registro pinado; vínculo documental sozinho não reduz a contagem (**achado D6 da seq 696**). Gatilho de leitor único σ≤1,0 inativo no primário (mínimo 1,04). Sufixo da sistemática da escada exige poder sem Cefeidas≥5 e hoje permanece fail-closed. D-J nomeia o token final. Citar **achados D1 a D6 da seq 696**.

Nenhum `ALVOS_FASE9_LIDOS.json` é produzido. Nada é congelado nem aberto. `NOT_FALSIFIED` nunca é creditação.
