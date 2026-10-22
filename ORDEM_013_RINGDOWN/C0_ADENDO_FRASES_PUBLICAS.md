[REAL/DERIVED condicional; lacunas de leitura explícitas] Adendo datado 2026-09-22T17:24:28.794715+00:00

# C0 — frases públicas corrigidas

Supersedes: C0_AUDITORIA.json, SHA256 f0009e1194282434ac599a35df68573db08967951a320218184670e15e1559cd. A v1 permanece intacta. Abertura do operador: 0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0.

## T02

[REAL] _verb_L constrói um salto hermitiano num proxy positivo 4×4, seed 11, FINITE_DIM_SANITY_NOT_III1_PROOF. Há uma família finita de transições Davies no Artigo A (56 saltos para espectro simples de dimensão 8); ela não é equivalente ao salto-raiz: um transfere populações, o outro as conserva. Família física de horizonte não construída; a expressão “família inexistente” só vale para _verb_L. README TGL_v2 25/05 → nota 31/05 é cronologia DECLARADA, README primário não localizado; nota finita → fig02 → teorema/implementações foram lidos. A identidade da fonte efetivamente usada pelo texto externo permanece OPEN.

## T10

[REAL] O catálogo selecionado tem 24/31 medianas de δτ positivas; o V2 registra +0,176647±0,108894 e +0,031294±0,175529, estratos distintos, não somados. Amortecimento aditivo Γ≥0 prevê δτ=−Γτ/(1+Γτ)≤0. Viés de seleção, forma de onda, estimador e física nova permanecem hipóteses distintas; não se declara RG aprovada em todos os testes.

## T11

[REAL, aritmética sobre resultados] Em GW, β não foi medido independentemente: a razão efeito/erro do V2 é 0,177851σ, não uma probabilidade de poder. Fora de GW, D1 V3 dá β livre em tensão com α√e: D1_BETA_TENSION, 3.0124975σ pela convenção simétrica da fonte. Cadeia não refeita; N/50=40 e autocorrelação até 41,60, com 2/4 parâmetros aquém de 50τ. O produto βτ★ permanece degenerado na lei quadrática sem relógio externo.

## T19

[DERIVED condicional] Γ=β/t_M dá δτ=-0.1285451469 com QNM exato arquivado; o controle BCW dá -0.127656099238. A supressão canônica Γ=(β/2)τ★ω², τ★=t_P [PRINCIPLED IDENTIFICATION], já existe. A lei-raiz no IR recupera o coeficiente apenas para kbar=1/4 [INPUT]. Nas fontes e elos conferidos não há derivação da identificação física de τ★ ou da partição; não é prova de inexistência em todo o acervo. Nenhuma falsificação global decorre do 10^76 dimensionalmente errado.

## T20

[KNOWN/REAL] No posterior pSEOBNR IMR de GW250114 a frequência 220 tem limite em escala de 2% e δτ é −0,01(+0,10/−0,09), a 90%. Ringdown isolado é menos restritivo. R-B de ensemble: mediana -0.0198452854234 frente a σ amostral 0.0577943800453, correção/σ 0.343377425. Não é precisão de poucos por cento em todos os testes.

## T21

[REAL/DERIVED condicional] Consistência do GW250114 com Kerr depende do modelo e não confirma a TGL. R-B de ensemble tem correção/σ 0.343377425; isso não é Bayes factor nem teste calibrado. Catálogos e GW250114 já consultados são calibração NÃO-CEGA.

## (d) — gerador unilateral, gerador bilateral e domínio

[REAL — enunciados lidos, sem nova compilação] ModularFirstLaw.lean:45–58 é finito e diagonal; não assume Σp=1. Sua derivada usa −log p, mas não prova sua positividade. Com normalização de estado, −logρ≥0 é unilateral. ContinuousModularZero.lean:62–93 é outro objeto, L_h−R_h, com pares ±k; o nome contínuo não elimina Fintype. Não há ponte entre homônimos por mera nomenclatura.

[KNOWN — Connes 1973, pp.133–134, fonte primária consultada pelo revisor] Um fator III₁ não admite traço normal fiel semifinito. Isso impede a representação tracial intrínseca τ(ρ·) nessa álgebra, não estados normais ou representações vetoriais. Δ positivo injetivo admite logΔ autoadjunto, possivelmente ilimitado, com domínio denso; não se deduz H_eff=0 da ausência de traço. Sorce, introdução eqs.(1)–(6), fornece o quadro modular; a prova integral não foi lida. URLs e alcance no relatório independente.

[DERIVED/REAL em matriz] Γij=(β/2)(√f(ki)−√f(kj))²: f=|K| dá Γ(+3,−3)=0; f=K₊ dá Γ(+3,−3)=3β/2. Em (0,1), ambas dão β/2=0.00601565020040157. Unidades do parâmetro modular, não s⁻¹ sem relógio. A escolha f e os domínios ilimitados não são fixados por Tomita. A ausência de dephasing ±k vale só para esse canal.

A alegada redundância universal de −i[K,ρ] tem contraexemplo; o Artigo A já a restringe a KMS/estado estacionário. Comutar fluxos não faz um deles identidade.

## Evidência, custódia e limites

As 64 fontes do recibo independente foram reconferidas pelo script desta correção. A cópia LVK está arquivada; o antigo ARCHIVING_PENDING foi removido do estado corrente. O template histórico citado por ef1b4d69 não coincide com o atual nem com o backup irmão; a busca exaustiva é DECLARADA pela auditoria da gerência. Os C2_TEMPLATE_CHECKS históricos não são reprodução byte a byte com a versão atual.

- C0_AUDITORIA_v2.json: 37f4e792584550c7c2ded07b50a7b07befa67a0351a21667ed7c2669903aaef7
- Revisão independente JSON: 21644dea544c1019c148d585b41997ba6a137b870c5f87a9fb4fb367b865d2e0
- Revisão independente MD: a4ee68c4831dd032ee651ec2aff051a515d5e32e256e913e0009238c78369910
- Fonte LVK local: 9efcdea95f47b1fb3352b4e95053edde160be7d9337c36e0d50a96c0ae727afa

Comando: `python -B -X utf8 refeito/record_c0_013bis.py`; escrita única, recusa sobrescrever. Contas independentes: `bis/c0_review/review_numbers.py`. A revisão original discrimina fontes não lidas e falhas de acesso; não houve nova PE ou cadeia cosmológica. Axiomas: N/A — sem Lean executado. Nenhum gate alterado, nenhuma leitura física escolhida.
