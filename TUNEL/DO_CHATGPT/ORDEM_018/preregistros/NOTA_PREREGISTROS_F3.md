# ORDEM 018 — nota de preparação dos pré-registros F3

[REAL — auditoria local] Os 23 arquivos do manifesto de insumos, os cinco hashes internos do V1 do ramo B e o hash canônico de `spec` conferem. Treze dependências selecionadas do V1 também conferem em disco. A reprodução e as medidas estão em `AUDITORIA_PREREGISTROS_F3.json`, gerado por `auditar_preregistros_f3.py`. Esta é uma auditoria da preparação; não constitui entrega integral F3 nem veredito de natureza.

[REAL] Consultado antes: mapa `ringdown.ramo_b_preregistro_v386`, seq 365, e `primordial.fase8_era_da_radiacao`, seq 371. Os recibos integrais estão nesta pasta. Foi lido o `PROTOCOLO_ANTI_PAREDE.md` da ORDEM 015. Originais, kernel, gate, fila e provedores não foram alterados. Nenhum strain nem posterior do conjunto D foi aberto. Nenhuma PE, gerador legado ou `um.py` foi executado. As contagens/listas abaixo vêm da cópia congelada: não certificam o estado atual de cada evento em fonte externa.

## 1. Ramo B: o que está autorizado e o que ainda precisa estar pronto

[INPUT] A decisão de 05/10 às 17:11:36 UTC reabre a investigação. O próprio V1 registra a delegação às 18:29:37 UTC dos itens 7–13: outra lei/canal F2b, `k=2π/κ̂(χ_f)`, `M_X=M_f`, fonte, amortecimento da envoltória primário, conjunto D como único teste e PE só-220 na casa para a etapa v387. A autorização da ORDEM018 incorporada pelo operador cobre esse trabalho. A decisão não autoriza trocar para propagação, escolher outro k após olhar o sinal ou promover A/B/C a teste novo.

O V1 define PE de IMR completo pSEOB com deformação do 220; `ringdown-only` é diagnóstico. A implementação nominal indicada é WSL `/opt/lal_env`, `pSEOBNRv4HM_PA` só-220, bilby+dynesty. São requisitos de instrumento a conferir localmente, não prova de execução atual. O 221 de GW250114 é diagnóstico; não entra na contagem de evidência. A/B/C são calibração `NOT_BLIND_TO_DATA_STATED`.

[REAL — lido] O V1 congela o CRITÉRIO, não a lista final por evento:14 elegíveis,10 sem hold,4 com hold,8 sem metadadosGR. Todos os 14 GPS da tabela de previsão são `null`. A massa/spin/SNR são metadados declarados no registro; a folha precisa ser reconciliada com fontes primárias/manifesto residente antes da PE. Não completar GPS de memória nem supor hold resolvido.

Sequência operacional exigida:

1. Reconciliar os eventos pelo critério: SNR ≥ 12; mediana M_f,det≥40M☉;0≤χ_f<0,98; fonte GWOSC/GR IMR; ausente do censo publicado congelado e dos catálogos excluídos. Preservar holds até resolução documental.
2. Congelar lista, fonte/hash de metadados, hashes de strain/PSD e política de seleção, sem abrir deformações. O manifesto do V1 aponta14 strains residentes, mas isso ainda não foi revalidado nesta auditoria.
3. Selar código/estimador, priors, orçamento, sementes, C1–C9 e separação entre saída cega e posterior privado. `PODER_RAMO_B_ANTES_DE_ABRIR.json` deve conterσ_i,spins,κ̂,N,previsões, covariância e poder antes dos centros. O modo de obterσ_i por PE sem revelarδτ precisa ser explicitamente implementado; “rodou PE” sozinho não certifica cegueira.
4. InjeçõesGR e ramo B, viés≤0,2|δ_pred| e cobertura; variações de início pareadas; família de onda; efeito de priors; identificação após nuisance; um bloco H1/L1 por evento; jackknife; gaussianidade; mínimo 10. Só então a abertura D usa a mesma função selada.

[REAL — inspeção estática] Os três geradores fornecidos contêm funções para gerar documentos/tabelas e poder. A AST não mostra uma função dedicada de veredito executável entre suas funções de topo. Isso não prova que tal função inexista em toda a casa. O V1 cita `bancada/gw_stack.py` como função de referência da Fase6; antes da PE é necessário localizar a implementação exata do contrato F2b e fixar seu hash, sem executar novamente o gerador documental que pode escrever fora desta pasta.

## 2. A identificação após nuisance precisa ser resolvida antes do gasto de PE

[DERIVED — álgebra gaussiana condicional] Escreva o contraste previsto entre as hipóteses como Δ e o modelo `y=μ_h+Xη+ε`, com `X=[1,σ]`, `η=(c0,kc)` e covariânciaC. Se η é livre sob ambas as hipóteses, o contraste identificável é

`Δ_perp = [I − X(XᵀC⁻¹X)⁻¹XᵀC⁻¹] Δ`,

`Z_shape² = Δ_perpᵀC⁻¹Δ_perp`.

Para matriz singular usa-se o subespaço de posto aferido/pseudoinversa. Um deslocamento constante está no espaço deX e é absorvido por c0. Se o próprio residual sob GR é usado para ajustar livremente c0, a equação normal impõe `1ᵀC⁻¹(y−Xη_hat)=0`. Portanto uma média ajustada desse mesmo residual não é, por si, uma estatística independente capaz de testar o deslocamento médio. O V1 pede nuisance perfilado e simultaneamente apresenta poder da média sem essa projeção; falta operacionalizar a relação entre ambos, ou a informação auxiliar que limita nuisance. Não é lícito fixar c0=0 para recuperar o poder: o V1 proíbe isso.

[REAL — calculado aqui, SEM valores observados] Usei somente os 31σ e spins já publicados na tabela congeladaA31. ReproduziBCW220,κ̂,k e δ_pred de todos os 31 eventos: diferença máxima de previsão exatamente0 em ponto flutuante. A31 permanece calibração conhecida, nunca teste D. Sob Gaussianas independentes, sem informação auxiliar sobre nuisance:

| σ_sys diagonal (cenário) | poder ingênuo da média | norma após c0 livre | norma após c0 + kc σ livres |
|---|---:|---:|---:|
| 0 | 11.382606 | 0.763928 | 0.741696 |
| 0.029 | 10.916587 | 0.754923 | 0.734777 |
| 0.038 | 10.659286 | 0.748914 | 0.729966 |

A primeira linha retém0,423% da norma quadrática do contraste bruto. As outras duas são cenários de sistemática diagonal, não um modelo demonstrado de correlação de família. Os resíduos projetados satisfazem as duas equações normais em precisão numérica. Isto mede uma lacuna de identificação da estatística, não exclui a lei, não faz forecastD e não emenda V1. Covariância compartilhada, calibração externa, limites físicos de nuisance ou uma verossimilhança completa podem mudar o resultado; precisam estar declarados e aferidos antes de D.

Árvore de alternativas para a coordenação, antes da próxima medida:

- A: operacionalizar o perfil livre já escrito e aferir o contraste ortogonal/injeções sem centrosD. Se o contraste efetivo for pequeno, registrá-lo e continuar nos demais canais úteis; nenhuma parede é declarada aqui.
- B: localizar informação auxiliar independente para nuisance (injeções/controles com covariância própria) e incorporá-la à verossimilhança conjunta das DUAS hipóteses. Não reutilizar números013-bis como prior nem ajustar a calibração para produzir o efeito. Qualquer mudança de contrato V1 exige interpretação/ratificação da gerência e, se alterar o contrato, nova versão; nunca sobrescreverV1.
- C: se a implementação falhar, reutilizar a árvore/receita já aferida ORDEM015 em um processo de controle isolado, registrando comando,rc,hash e custo. Um diagnóstico 220+440/221 não substitui o teste IMR só 220 autorizado.

## 3. Fase8: radiação, N_eff e BBN

[INPUT/DERIVED] A lei δK=β|1+w| é entrada do modelo; a álgebra do mapa ρ+p é condicionada a ela. A crítica fornecida localiza `entropyFactor` como definição/entrada e `hubble_form` como identidade. Esta auditoria não recompilou o kernel. Para radiação,δρ_r/ρ_r=4β/3. Com `F=(7/8)(4/11)^(4/3)` eN_SM=3,044, `ΔN_eff=(4β/3)(1/F+N_SM)`. O script calcula β=α_CODATA2018√e em runtime a partir do α registrado no insumo hash-verificado; β não é literal nem ajuste.

[REAL — reprodução] ΔN_eff=0,11946607525373276; S=√(1+4β/3)=1,007988955231027. Antes da aniquilação e±, a equivalência BBN é `(4β/3)·43/7≈0,09854`; depois é0,119466. Uma fração constante de ρ_r não equivale a um ΔN constante ao longo de toda BBN. As tabelas PRIMAT/PArthENoPE podem produzir um BRACKET declarado; o cálculo exato pede S(T) na história térmica. Não aplicar0,0985 ao deutério tardio nem0,1195 indiscriminadamente ao congelamento n/p.

Poder significa separação das hipóteses/σ, sem centro observado. Com σ0,17:0,702742; com σ0,12:0,995551; com σ0,03:3,982203. A condição 5σ éσ≤0,0238932. O número6,45 do rascunho usa a hipótese de o centro futuro permanecer2,97: é uma tensão nesse cenário, não poder de separaçãoTGL−SM. Valores/épocas SO e S4 continuam[DECLARADO] até fonte primária, especialmente a previsão de calendário. Nenhum calendário 2030/2032 foi certificado. Não somar Planck+ACT/Planck+SPT como experimentos independentes.

O rascunho FASE8 ainda é`AWAITING_RATIFICATION`. Sua numeraçãoD1–D9 não coincide com a lista consolidadaD1–D11 da crítica; identificar a lista ao colher respostas. Pendências científicas concretas:

- Mapas: radiação4β/3 é o ramo registrado na crítica; “só matéria” não é alternativa canônica já ratificada. Não escolher por melhor concordância. TGL-S/free-streaming é hipótese do fechamento perturbativo; TGL-L não herda o mesmo poder N_eff e sua rodada antiga não convergiu.
- Uma entrada de β por instrumento: fundo já vestido por Φ_total conserva N_eff padrão; CAMB usa a representação nnu/ω_c,eff sem adicionar Φ_total outra vez. A ordem é Bancada antes de um.py. Implementar controlesβ=0 e a equivalência do fundo antes de dados.
- BBN: jamais derivar o baseline do D/H observado ou usar ω_b inferido do próprioD/H como preditor independente dele. Obterω_b CMB com covariância/referência compatível; declarar as alterações sobTGL-S e o prior BBN (S=1) da análise Nível 2.
- Fontes: Y_p2015 versus2021, respostaD/H0,57 versus1,57/1,618/1,9 e incerteza nuclear requerem fonte primária/hash. As duas convençõesΔN e S(T) devem ficar distintas. A crítica aponta tabelas CAMB residentes apesar de não achar código BBN standalone.
- Regras: D/H com sistemática nuclear1,6% frente a efeito0,46–1,55% viola a razão0,3 no próprio rascunho; essa checagem precede o degrau de poder. Portanto não resumir todos os canais simplesmente comoUNDERPOWERED. O estado atual é preparação, sem ratificação nem veredito novo.

Árvore para os insumosBBN: A localizar e hashear tabelas CAMB já existentes e fazer somente bracket/controlado, se o escopo ratificado admitir; B preparar o código BBN com S(T), fontes e calibração para a decisão de instalação/execução. Em ambos, usar primeiroσs/fontes e controles, não centros para escolher mapa. Alternativa para documentação faltante: A fonte primária pública; B catálogo/release oficial citado, mantendoAWAITING_SOURCE se a grandeza não estiver documentada. Isso permite avançar a instrumentação e as outras rotas enquanto se resolve a fonte.

## 4. Artefatos operacionais a reutilizar e custos

O JSON de auditoria inventaria as 13 dependências hash-verificadas: PODERcegoV1/V2 e scripts, reconciliaçãoD e script, decisão, RINGDOWN_5SIGMA_V1, E0_ROUTE_IV_POWER_v2, E0_CORE, SYSTEMATICS_ADENDO, F4_POWER_GATE_REVIEW eT01. Não se executou nenhum desses arquivos. O censo e as listas de fontes completas estão noV1. A leitura debytes para hash do registro 5SIGMA não extraiu centrosD.

As estimativas 63–78 e 58–390 CPUh do V1 são[DECLARADO], não custo medido nesta rodada. O arquivo hoje localizado `bis/015/t09/T09_PREREQUISITE_RESULT.json` registra PE_started=false, T09_NAO_PAGO_OPERATOR_BOX_B_LINE_ABSENT e estimativa 2,6–3,3h/teto 8 h para outro objetivo (440/220); não comprova o orçamentoPE/D citado. Medir custo por injeção/piloto seguro e conferir proveniência da estimativa antes do lote. Os contratos/priors antigos não ganham autorização nova por terem sido encontrados.

A busca de nomes com rg encontrouAccessDenied nos diretórios E2_PRIVATE; não houve leitura de conteúdo nem escalonamento. É proteção respeitada, não prova de ausência de dados nem falha do instrumento. Os arquivos de preparação foram gravados por bytes→temporário verificado→substituição; qualquer edição recebe backup de bytes. Nenhum provedor externo foi chamado; logo não hárequest_id de executor nesta subtarefa.

Reprodução: `C:\Python314\python.exe -X utf8 auditar_preregistros_f3.py` dentro desta pasta. A primeira execução científica local durou 0,409 s de walltime de processo segundo exec_command; não se trata de CPUh de PE. O script gera apenas esta auditoria; abre somente insumos e dependências documentais nomeadas.
