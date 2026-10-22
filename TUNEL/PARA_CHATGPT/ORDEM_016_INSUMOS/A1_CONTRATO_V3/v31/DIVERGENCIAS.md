# DIVERGENCIAS — Contrato v3 → v3.1 (rodada 2, 23/09/2026)

> Rascunho de gerência, frente `contrato_v3`, scratchpad. Nenhum nome reservado foi cunhado e nada move o gate.
> Cada ataque dos dois céticos da rodada 1 recebe um veredito: **ACEITO**, **PARCIAL** ou **RECUSADO**. Recusar
> exige fonte. Os sha16 e rc estão em `MANIFESTO_V31.json`, lidos dos arquivos por script.
> Estatutos: `[REAL]` = compilado aqui; `[KNOWN]` = literatura; `[DERIVED à mão]` = argumento não formalizado;
> `[OPEN]` = em aberto.

## 0. Reprodução dos céticos (antes de corrigir)

Os oito arquivos dos céticos foram copiados sem alteração para `rodada2_ceticos_v3/src/` e recompilados contra
os oleans da v3, abertos só para leitura. Os sha16 conferem com os declarados: 44b92cdc31abc773, 56020eb8c8beb6a9,
957f5ac79142a327, 333a662a8fde1b51, e986f2bac15c978a, 6b1374b5b9b3ed0f, 39e2508fdde98aef e 948fb8c29d3661e4.
**Os oito deram rc=0** `[REAL]`, e `find -newer` contou 0 arquivos novos em `v3/` e 0 no kernel. Os ataques
eram reais contra a v3.

## 1. Cético 1 (lente brinquedo)

| # | Ataque | Veredito | O que mudou / evidência |
|---|---|---|---|
| 1.1 | **BLOQUEANTE:** `ContratoH3`/`ContratoImportH3` v3 habitados por brinquedo dado um H2 (`toyH3`, `H3_toy_for_every_G`, `H3_toy_on_geoFrame`, `toyImport`) | **ACEITO** (a parte «para todo G» é **RECUSADA como defeito**, ver 2.1b) | (i) A matéria deixou de ser do habitante: virou o **índice** `T : StressTensorData W`, nulo no vácuo e covariante por translação. (ii) A resposta deixou de ser escolhida por estado: é `𝔉(T(ψ))`, com o **propagador** `𝔉` fixo antes de todo ψ, nulo na fonte nula e covariante (`propagator_zero`, `propagator_covariant`). Daí `same_source_same_geometry` e `response_covariant` saem como teoremas. (iii) A lei deixou de ser um escalar por estado. Virou **local em todo ponto x**, ao longo do gerador nulo: `raychaudhuri_einstein`, dθ/dλ = −8πG·T_nn. (iv) BH/Clausius/8πG passaram a teoremas de janela, por integração exata (`first_law_window`, `bekenstein_hawking_window`, `einstein_coefficient_window`). O porte do brinquedo (`ProbeAjustadorV31`) **reprova exatamente** em {`propagator_covariant`, `raychaudhuri_einstein`}. O porte da matéria por estado reprova em {`T_covariant`}. O import pelo brinquedo só compila herdando `sorryAx`. As refutações estão em kernel: `slope_response_excluded`, `exp_response_excluded`, `slope_propagator_excluded`, `exp_propagator_excluded`, `expansion_not_constant`, `response_not_identically_zero`. |
| 1.2 | **IMPORTANTE:** κ livre no tipo (`rekappa`, `kappa_is_free`, `unruhTemperature_is_free`, `rekappa3`) | **ACEITO** | O observador fiducial virou o **índice externo** `N : KillingNormalization` `[INPUT]`. Dado N, κ é fixo (`kappa_fixed`, `kappa_eq_inv_radius`, `no_rekappa`). O porte de `rekappa` (`ProbeRekappaV31`) reprova em {`observer_unit`}. Fica dito, como teorema, que **o par (W, R) não fixa κ**: `kappa_is_input` e `reindex`. O que o tipo fixa é a relação β_Killing·κ = 2π (`kms_product_is_two_pi`, teorema do cético). A frase «κ amarrado três vezes» foi retirada, e também «R-MOD [DERIVED no contrato]» e «colapsa a caixa de prior de τ★» (ver §4). |
| 1.3 | NOTA: transpor T1–T4 e riscar `V_continuous` da lista «sem consumidor» | **ACEITO** | Transpostos para `ContratoQG_v31_Teoremas.lean` com crédito: `transverse_U_excluded`, `trivial_boost_excluded`, `tower_excluded`, `boost_moves_null_eigen`, `null_eigen_orth`, `null_point_spectrum_excluded`, `discrete_null_momentum_excluded`. `V_continuous` passa a ter consumidor. Nas paredes, `toy_not_v31_by_null_momentum` aplica T4 ao brinquedo. |
| 1.4 | NOTA: `W.m` é decorativo | **ACEITO** | `m` é rótulo. A v3.1 **não** exige gap de massa, e a frase «m > 0 já é campo de W» deixa de ser usada como apoio. |
| 1.5 | NOTA: a exclusão da rede por bandeiras é condicional | **ACEITO** | Continua condicional, agora à hipótese fiel `KMSUniqueGroup` (ver 2.5). O estatuto está dito no cabeçalho de `FlagNetV31.lean`. |
| 1.6 | Correção proposta: covariância da matéria também por V(s)/Λ_s | **PARCIAL** | Covariância por translações: sim. Covariância de Lorentz de T: **não** tipada. Não é necessária às paredes; fica refinamento `[OPEN]`, dito no docstring de `StressTensorData`. |
| 1.7 | Correção proposta: a carga de boost como teorema, B = ∫ ξ^a T_ab n^b | **PARCIAL** | É **campo** (`modular_charge`: energia modular = 2π × carga nula de T), não teorema. Um teorema exigiria o tensor como distribuição operatorial e a quantização no plano nulo, que não estão na mathlib da casa. `[KNOWN como exigência: Casini–Teste–Torroba 2017 (J. Phys. A 50, 364001); Faulkner–Leigh–Parrikar–Wang 2016 (JHEP 09 (2016) 038)]`. |

## 2. Cético 2 (lente vacuidade/fidelidade)

| # | Ataque | Veredito | O que mudou / evidência |
|---|---|---|---|
| 2.1a | **IMPORTANTE:** H3 e o import pagáveis por AJUSTADOR (`adjustH3`, `H3_of_H2`, `H3_of_H2_geo`, `genericImport`, `import_is_adjustment`) | **ACEITO** | Mesma correção de 1.1. O `geoFrame` **paga** a planura do fundo (`geoFrame_screen_flat`, provado no probe), então a reprovação do ajustador **não** vem do fundo: vem dos dentes novos. |
| 2.1b | …e «G é livre como um todo» (`G_is_free`) | **RECUSADO como defeito** | Na rota de Jacobson, G **é entrada**: a constante η (entropia por área) é postulada, e G = 1/(4ħη) `[KNOWN: T. Jacobson, «Thermodynamics of spacetime: the Einstein equation of state», PRL 75, 1260 (1995)]`. Nenhum tipo honesto de H3 pode predizer G sem física UV (o item `interacting_…_UV_scope` do gate). A v3.1 não esconde isso: prova `G_not_predicted`/`rescaleG`, que diz que de todo habitante sai outro com G' arbitrário. **O que se aceita**: a frase da v3 «G não se ajusta por perturbação» induzia a ler «G fixado». Foi reescrita como «G fixo por habitante, não predito». |
| 2.2 | **IMPORTANTE:** κ é calibre (`regauge`, `kappa_is_gauge`, `kappa_set_is_all_positive`) | **ACEITO** | Mesma correção de 1.2. «Pagar H2 no par plano NÃO fixa κ» está dito com todas as letras em §4 e em `kappa_is_input`. |
| 2.3 | **IMPORTANTE:** o δS de H3 era a energia modular BILATERAL, sem termo de 1ª ordem, e o rótulo «primeira lei, 1ª ordem» era falso | **ACEITO** | O teorema do cético foi transposto (`bilateral_no_first_order`). O δS de H3 v3.1 é a carga **unilateral** do corte nulo, `windowEntropy = 2π∫_c^d (λ − c)T_nn`, lida de T. A energia bilateral ficou só no elo `modular_charge`. A identidade δQ = T_U·δS é **definicional** e foi rotulada assim (`clausius_window`, «Clausius como leitura»). Identidade `[KNOWN, não formalizada]`: ⟨−log Δ⟩_ψ = S(ψ‖Ω)_M − S(ψ‖Ω)_{M′} (Ceyhan–Faulkner 2018, arXiv:1812.04683; CTT 2017). **Correção do alvo B6**: estados coerentes W(f)Ω têm δS_EE = 0 exato. O teste de 1ª ordem tem de usar perturbações Ω + εφ com φ de dois corpos, em que a carga unilateral tem termo linear. |
| 2.4 | NOTA: as 37 guardas são tautológicas; relatar a mordida | **ACEITO** | `GuardasV3` foi abandonado. A v3.1 mede a matriz de mutação (`mutacao/mutar.py`, 37 campos mais BASE), separando mordida em probe negativo de quebra de teorema derivado. A Ponte v3↔v3.1 não conta como consumidor, porque é transporte campo a campo e tautológica por construção. Os números estão em `mutacao/matriz_mutacao.json` e no relatório. |
| 2.4' | …acrescentar probes negativos (KMS falso, BW de sinal trocado, `positive_energy` refutada, rede não covariante, observador fora da cunha, frame não arrastado num par que pague o resto) | **PARCIAL** | Feitos: BW de sinal trocado → teorema `ContratoH2.bw_sign_matters`. Observador fora da cunha → impossível de escrever, porque `KillingNormalization.point_in_wedge` faz parte do índice (a mutação mede o campo). Frame não arrastado → `curvedFrame_not_dragged` e `frame_ne_curvedFrame_by_drag`. **Não feitos**: fluxo não-KMS e refutação de `positive_energy`. Ambos pedem princípio de reflexão de Schwarz ou Phragmén–Lindelöf no semiplano/faixa para `DiffContOnCl`, fora do alcance desta rodada. Além disso, **nenhum par paga o resto** (é o ponto do contrato), então probes negativos «de um campo só» não têm onde morar. Ficam `[OPEN]`, ditos. |
| 2.5 | NOTA: `KMSUnique` quantifica sobre funções e proíbe Z₂ | **ACEITO** | `FlagNetV31` usa `KMSUniqueGroup` (a forma de Takesaki). O teorema do cético foi transposto (`kmsUniqueFun_forbids_Z2`). A parede `flag_net_excludes_v31` usa a hipótese fiel. |
| 2.6 | NOTA: coerência de sinal só à mão; `positive_energy` sem consumidor; frase sobre massa; traço de Takesaki em B5 | **ACEITO / PARCIAL** | Transpostos com crédito: `halfsided_inclusion`, `contract_borchers_form`, `positiveEnergy_orientation`, `translate_null_subset`. Frase corrigida: a ergodicidade nula vale para o campo livre massivo **e** sem massa em 3+1; só falha no caso quiral/2D. B5: aviso registrado no relatório. O `canonicalTrace` do kernel pede tracialidade para todo x, y, e o traço de M ⋊_σ ℝ estendido por ⊤ a viola `[argumento à mão do cético, não medido aqui]`. `positive_energy` **continua sem consumidor em teorema** (dito). |
| 2.7 | Veredito do cético: «não há v3 vazia no par físico» | registrado | A v3.1 acrescenta cláusulas. A não-vacuidade para o campo livre é argumentada à mão em §3 e **não é teorema**. |

## 3. Não-vacuidade da v3.1 para o par físico (campo escalar livre em 3+1) — `[DERIVED à mão / KNOWN]`, NÃO formalizado

* **H2**: não muda em relação à v3, exceto o índice N. A `PonteV3V31` prova H2 v3 habitado ⟺ ∃ N, H2 v3.1 habitado. Logo vale a análise do cético 2 na rodada 1: BW `[KNOWN: Bisognano–Wichmann 1975/76]`, KMS `[Takesaki]` e Borchers são coerentes, e `null_ergodic` vale porque P⁰ − P¹ > 0 em cada partícula.
* **T₀**: ⟨ψ, :T_ab(x): ψ⟩, nulo no vácuo e covariante.
* **`modular_charge`**: −log Δ = 2π∫λ T_nn no plano nulo para estados suaves `[KNOWN: CTT 2017; Wall 2012]`. A classe A são os vetores unitários suaves com λT_nn integrável, que é fechada por translação.
* **𝔉₀**: o propagador nulo teleológico, h = diag(0, 0, −a, −a) com a(x) = −8πG∫_0^∞ μ T_nn(x + μn) dμ e θ(x) = 8πG∫_0^∞ T_nn(x + μn) dμ. Cumpre a lei local, o gauge h·n = 0 e a covariância. O `propagator_zero` e a covariância valem para **toda** fonte, inclusive a não integrável, porque o lixo de Bochner é invariante por translação.
* **Fundo**: o frame de Rindler ortonormal (e o `geoFrame`, provado) tem tela −1₂ na cunha.
* ⚠ Isto é argumento, **não teorema**. `ProbeResidualH3v31.H3_iff_null_solution` prova só a redução: dado (H2, T, A, elo), H3 v3.1 ⟺ ∃ solução nn covariante como lei fixa da fonte.

## 4. O que a v3.1 NÃO diz (as frases da rodada 1 que se retiram)

1. **«κ amarrado três vezes»**: retirada. O tipo fixa β_Killing·κ = 2π (relação de Unruh). O **valor** de κ é o índice N `[INPUT]`, que no espaço plano é a aceleração do detector.
2. **«R-MOD τ★ = 2π/κ_H vira [DERIVED no contrato]»** e **«colapsa a caixa de prior de τ★»**: retiradas. Pagar H2 no par plano **não** fixa κ_H. κ_H exige a face curva com normalização assintótica do Killing (ξ → ∂_t no infinito; Schwarzschild: κ_H = 1/(4GM)), que está **fora** deste tipo `[OPEN]`. Em Kerr há a obstrução de Kay–Wald: não existe estado Hadamard invariante pelo fluxo de Killing regular no horizonte bifurcado `[KNOWN: B. S. Kay, R. M. Wald, Phys. Rep. 207, 49 (1991)]`, e os eventos do LIGO são Kerr. A leitura do ringdown por τ★ = 2π/κ_H fica `[CONJECTURE]` em Schwarzschild e `[OPEN/obstruída]` em Kerr.
3. **«Clausius deixou de ser campo»** (v3): era troca de nome, como apontado. Na v3.1 a identidade é definicional e está dita. O conteúdo de H3 v3.1 é outro: o elo `modular_charge` mais a lei local nn.
4. **«H3 v3.1 é Einstein»**: **não**. É a componente **nn** linearizada, ao longo de **uma** direção nula n, com a geometria dada por um propagador fixo. As demais componentes pedem a família de Lorentz de cunhas (W não tem rotações) `[OPEN]`. Ler a geometria do **estado modular** (cociclo de Connes, o «Lema 3» da TGL) em vez de um propagador dado é `[OPEN]` e é **o** conteúdo físico que falta.

## 5. A matriz de mutação da v3.1 (medida; `mutacao/matriz_mutacao.json`, lida por script)

Cada um dos **37** campos `Prop` foi afrouxado a `True`, um de cada vez. Em cada vez recompilaram-se o tipo, os
teoremas, os seis probes negativos, o probe positivo e, quando os teoremas compilavam, as paredes, a FlagNet e
a Ponte. Resultado: 0 falhas de memória, `find -newer` = 0 arquivos novos no kernel em todas as rodadas, e rc do
tipo = 0 nas 37 mutações.

* **Mordidos por probe negativo: 8/37.** São `translations_faithful`, `positive_energy`, `null_ergodic`,
  `observer_unit`, `T_covariant`, `admissible_nontrivial`, `propagator_covariant` e `raychaudhuri_einstein`. Em
  todos, o dente sai do conjunto de erros do probe quando o campo vira `True`.
* **Consumidos genuinamente por teorema derivado: 34/37.** O critério exclui os sítios de construção do próprio
  campo mutado (`decl.campo := …`, artefato de tipo) e a propagação de `sorryAx`. Sete dos oito mordidos também
  são consumidos. Alguns consumidores são leituras de uma linha, como `response_null_null_zero`; estão listados
  por nome na matriz para que o leitor julgue.
* **Só mordido, sem consumidor: `positive_energy`.** Está dito. Um consumidor exigiria reflexão de Schwarz ou
  Phragmén–Lindelöf no semiplano.
* **Nem mordida nem consumo: 2/37, `ContratoH2.smooth_on` e `ContratoH3.admissible_unit`.** São convenções: a
  suavidade do frame, que nenhuma derivação usa, e a normalização dos estados. Estão ditas, não escondidas.
* A mutação de um campo consumido nos teoremas BLOQUEIA o estágio 2 (paredes, FlagNet, Ponte), porque os
  teoremas deixam de compilar. Nesses campos, o consumo nas paredes não foi medido separadamente. A Ponte v3↔v3.1
  é transporte campo a campo e **não** é contada como consumidora.

## 6. Buracos que a v3.1 deixa ABERTOS e diz

1. **T₀ é índice e pode ser forjado.** O tipo não prova que T é o tensor LOCAL da rede: localidade, conservação
   ∂^a T_ab = 0, simetria e a forma de Wightman/sesquilinear não estão tipadas. Um T covariante forjado pode ser
   construído por escolha, sobre as órbitas de translação, para satisfazer o elo `modular_charge` `[DERIVED à
   mão]`. Por isso T₀ tem de ser **ratificado** junto com (W₀, R₀), como a partição. `[OPEN/INPUT]`
2. **O propagador não é único.** Dado (H2, T₀, A, elo), H3 v3.1 ⟺ existe solução nn covariante como lei fixa da
   fonte (`H3_iff_null_solution`). A liberdade restante são as soluções homogêneas a + bλ ao longo dos
   geradores, isto é, a condição de contorno (teleológica, retardada). Ela seria fixada por linearidade de 𝔉
   num domínio de fontes com decaimento. Não foi tipado, porque a linearidade global briga com o lixo de
   Bochner fora de L¹. `[OPEN]`
3. **A geometria não é lida do estado modular.** Na v3.1 a resposta é 𝔉(⟨T⟩), a leitura semiclássica. Lê-la dos
   dados modulares do estado ψ (fluxo modular relativo, cociclo de Connes (Dψ : DΩ)_t) é o «Lema 3» da TGL, e é o
   que faria de H3 uma DERIVAÇÃO em vez de um postulado nn. `[OPEN]`
4. **Só a componente nn, numa direção nula.** As demais componentes de Einstein exigem a família de Lorentz de
   cunhas, e o W do kernel só tem translações e uma família de boosts. `[OPEN]`
5. **G não é predito** (§2.1b). `[KNOWN: Jacobson 1995]`. Fixá-lo é o item UV do gate.
