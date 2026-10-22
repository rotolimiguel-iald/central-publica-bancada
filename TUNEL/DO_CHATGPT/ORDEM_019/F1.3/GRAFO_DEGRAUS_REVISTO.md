# F1.3 — grafo revisto após a crítica MiMo

[REAL — escopo] Este é um plano de dependências, não uma nova prova física. A conciliação F1.1 × v376 e o parecer MiMo ficam preservados como entradas históricas. O core regular de `V351RegularCoreTraceConstruction.lean` e o core físico da cunha são objetos distintos. O primeiro tem fornecedores Lean para tracialidade e escala dual; o segundo ainda exige um habitante do par físico e a ponte entre os tipos. Nenhum estatuto do core regular é transferido pelo nome.

## Tipos e três elos do canto

- `P_kerK` e `ρ*_IALD`: igualdade por termo no objeto da luz, no escopo registrado pela v376 `[REAL — termo]`.
- `P_F^fin`: canto da face finita dos Three Locks. `three_locks_corner_weight` e `three_locks_name_is_one` falam da dimensão do núcleo de `H3L`, sob as hipóteses de testemunha e não trivialidade `[KERNEL — face finita]`.
- `P_F^core`: campo `FockCertificate.PF` destinado ao core da cunha física `[VINCULADO — contrato sem habitante físico]`. A relação `ρ*_IALD ↔ P_F^core` permanece `[KNOWN/OPEN — citação e identificação tipada ainda não demonstrada]`. Não compor os dois primeiros elos para concluir `P_kerK = P_F^core`; `P_F^fin` também não o substitui.

## Dependências e modo de quitação

| Nó | Pré-requisito → entrega mínima | Situação nesta entrega |
|---|---|---|
| F1.3.D0 — fornecedores existentes | `LightOneParticleByTerm.lean` entrega `U1_continuous` e `null_no_eigen`; `QGSolutionComplete.lean:60–69` já os coloca em `LightNetData.toLightOneParticle`. `TGLExt.Commutant` é tijolo algébrico de comutante. | `[REAL — fonte]` A ligação dos dois campos já aparece por termo; o comutante algébrico não constrói a álgebra da cunha. |
| F1.3.D0.5 — primeiro controle factível | Compilar em cópia o consumidor e conferir axiomas, pin e dependências da fiação D0. | `[OPEN — auditoria reprodutiva]` Não descarrega nó físico. Serve para detectar quebra de integração, sem promover os outros campos. |
| F1.3.D1 — primeiro nó construtivo | Instanciar uma rede padrão física Wigner/BGL de helicidade ±1 na cunha, com subespaços padrão, isotonia, localidade, covariância e boost; fornecer um habitante tipado de `LightNetData`, começando por uma cunha e estendendo com hipóteses explícitas. | `[OPEN — construção]` A literatura é `[KNOWN]`; a rede física desta casa ainda não tem habitante. |
| F1.3.D2 — segunda quantização | Sobre a mesma rede D1, construir Γ/Fock/Weyl, energia positiva e álgebra de von Neumann. | `[OPEN]` Um campo nomeado em `FockCertificate` não é a instância física. |
| F1.3.D3 — vetor padrão | Provar ciclicidade e separação de Reeh–Schlieder para o vácuo e a **mesma** álgebra da cunha de D2. | `[OPEN]` Sem esse par, Tomita físico não tem entrada. |
| F1.3.D4 — comutante e Tomita | Construir o operador antilinear `S` inicialmente denso, provar fechabilidade, obter `S=JΔ^{1/2}` com `Δ` positivo auto-adjunto não limitado e provar `J A J=A′` no mesmo par. Reaproveitar o comutante algébrico finito como lema local, com transporte explicitado. | `[OPEN — analítico e tipado]` `StandardSubspace.lean` no pin local ainda nomeia Tomita/KMS como TODO; isso não impede teorema próprio da casa. |
| F1.3.D5 — BW/KMS | Identificar o fluxo modular de D4 com o boost físico e provar KMS analítico regional na mesma cunha. | `[KNOWN — literatura]`, `[OPEN — realização da casa]`. A órbita angular periódica da torre não é o boost hiperbólico. |
| F1.3.D6 — core físico | Construir **ou** importar com hipóteses e citação a tipagem do core contínuo físico, ação dual, traço normal semifinito fiel e tipo III₁/fluxo de pesos pertinente. Provar um morfismo que transporte os fornecedores do regular v351 antes de aplicá-los. | `[OPEN]` `scalarInverseLimitTraceData` prova tracialidade e escala no core regular v351; `FockCertificate.trace_tracial` da luz continua sem consumidor downstream. Importação e construção têm modos de quitação distintos. |
| F1.3.D7 — projeção e cisão | Construir `P_F^core` finito não nulo, suas metades ortogonais de mesmo traço e a identificação tipada com `ρ*_IALD` se esta for a afirmação pretendida. | `[OPEN]` A normalização `P_F^fin` não paga essa obrigação. Maxwell/carga modular e janela de Jacobson são consumidores posteriores, sob seus próprios contratos. |

**Primeiro trabalho concretamente verificável:** D0.5, auditoria da fiação já escrita; o primeiro nó que acrescentaria uma construção física é D1. Os demais campos tipados permanecem **sem habitante do par físico**, sem bandeira de promoção e sem uso como prova por consumidores posteriores. `VINCULADO` e `SABIDO` descrevem eixos diferentes: existência de campo formal, existência de termo no escopo e realização física devem ser registrados separadamente.

**Custo:** a ORDEM 016 §1 registra ≥400 h como **piso estimado** para o caminho físico completo, com risco muito alto. As escalas por nó são estimativas de gestão, não medições de CPU nem limites superiores; a soma pode ultrapassar o piso. A ressalva histórica 8/12 GiB consta do inventário da bancada e não é critério de fechamento de D1–D7.

## Fontes primárias para os resultados importados

- Rede modular Wigner/BGL: Brunetti, Guido e Longo, *Reviews in Mathematical Physics* **14** (2002), 759–785, [texto dos autores](https://www.mat.uniroma2.it/~guido/research/papers/BGLo3.pdf) `[KNOWN]`.
- Ciclicidade local: Reeh e Schlieder, *Il Nuovo Cimento* **22** (1961), 1051–1068, [DOI 10.1007/BF02787889](https://link.springer.com/article/10.1007/BF02787889) `[KNOWN]`.
- Teoria modular: Takesaki, *Lecture Notes in Mathematics* **128** (1970), [DOI 10.1007/BFb0065832](https://link.springer.com/book/10.1007/BFb0065832) `[KNOWN]`.
- Relação modular e boosts: Bisognano e Wichmann, *Journal of Mathematical Physics* **16** (1975), 985–1007, [DOI 10.1063/1.522605](https://doi.org/10.1063/1.522605); **17** (1976), 303–321, [DOI 10.1063/1.522898](https://doi.org/10.1063/1.522898) `[KNOWN]`.
- Tipo III e fluxo de pesos: Connes, *Annales scientifiques de l'É.N.S.* **6** (1973), 133–252, [fonte editorial](https://numdam.org/articles/10.24033/asens.1247/); Connes e Takesaki, *Tohoku Mathematical Journal* **29** (1977), 473–575, [fonte editorial](https://www.jstage.jst.go.jp/article/tmj1949/29/4/29_4_473/_article) `[KNOWN]`.

Esses trabalhos sustentam resultados gerais com suas hipóteses próprias; nenhuma citação fornece por si o habitante do certificado físico desta casa.
