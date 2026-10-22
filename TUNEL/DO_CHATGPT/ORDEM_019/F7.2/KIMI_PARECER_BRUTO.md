# Revisão cética — F7.2 (ORDEM 019, ADENDO 004): decoerência de neutrinos (n = −2) e interferometria de matéria

**Papel exercido:** crítico de proveniência e poder. Nenhum código executado, nenhum dado experimental aberto, nenhum original editado, gate intocado. β permanece `ALPHA_FINE_CODATA_2018 × √e` em runtime (usei β = 0,0120313004008 [KNOWN, forma canônica]).

**Limitação declarada:** não li os artigos integrais nesta chamada. Os fatos bibliográficos abaixo vêm (i) das descrições fornecidas no próprio pedido (URLs, tabelas e números citados) e (ii) da memória canônica carregada. Tudo o que é **conta minha** está marcado [DERIVED] e é reproduzível à mão; o que depende de leitura integral está marcado [OPEN]. Nenhum resultado de modelo aqui é prova, confirmação ou autorização.

---

## (1) A cota τ★ ≤ 7,8×10⁻¹⁰ s segue da fonte e da lei?

**Veredito: SEGUE aritmeticamente dos inputs declarados; a primeira passagem NÃO auditada é a proveniência do γ de entrada, não a matemática.**

Verificação (conta minha, [DERIVED]), com a lei declarada Γ_ω = ½·β·τ★·ω², ω = Δm²/(2E):

- Inputs declarados pela rota local: γ ≲ 10⁻¹⁷ eV em E₀ = 1 MeV (`tgl_dephasing_falsifier.py:32`, escala solar/KamLAND n = −2); canal solar/KamLAND ⟹ Δm²₂₁ [KNOWN que este canal sonda Δm²₂₁]; adoto Δm²₂₁ = 7,5×10⁻⁵ eV² [KNOWN externo, NuFIT — não lido dos artefatos nesta chamada].
- ω = 7,5×10⁻⁵ eV² / (2 × 10⁶ eV) = 3,75×10⁻¹¹ eV; ω² = 1,40625×10⁻²¹ eV².
- βω² = 0,0120313004 × 1,40625×10⁻²¹ = 1,6919×10⁻²³ eV².
- τ★ = 2Γ/(βω²) = 2×10⁻¹⁷ eV / 1,6919×10⁻²³ eV² = 1,1821×10⁶ eV⁻¹.
- Conversão ℏ = 6,582119569×10⁻¹⁶ eV·s [KNOWN]: τ★ = 1,1821×10⁶ × 6,5821×10⁻¹⁶ s = **7,78×10⁻¹⁰ s**. ✓ coincide com a cota declarada.

**Sensibilidade (o que precisa estar explícito para a cota ser auditável):**
- τ★ ∝ Γ·E²/(β·Δm⁴). Se E₀ = 10 MeV em vez de 1 MeV, a cota sobe 100×. Se se usasse Δm²₃₁ ≈ 2,5×10⁻³ eV² (canal errado para solar/KamLAND), a cota cairia por ~(33,3)² ≈ 1,1×10³, para ~7×10⁻¹³ s. **A identificação Δm²₂₁ + E₀ = 1 MeV é a escolha que carrega o número** — está correta para o canal declarado, mas precisa constar em cabeçalho, com a CL.
- Com Δm²₂₁ = 7,42×10⁻⁵ eV² (NuFIT), a cota vira ~7,95×10⁻¹⁰ s — mesma ordem; declarar o valor adotado.

**Primeira passagem problemática (não “inválida”, não auditada):** a origem de **γ ≲ 10⁻¹⁷ eV @ 1 MeV** (`tgl_dephasing_falsifier.py:32`). O pedido mesmo registra que “a origem e conversão exatas requerem verificação”. Sem artigo/página/tabela/CL, a cota τ★ fica no estatuto **[DECLARADA, não inscrita]** — aritmeticamente consistente, proveniência pendente. Nota de sanidade: a ORCA tab. 4 (item 2 abaixo) reporta, para o caso KamLAND n = −2, Γ₂₁ = Γ₃₂ < 7,9×10⁻²⁷ GeV = 7,9×10⁻¹⁸ eV a 90% CL [KNOWN via contexto] — mesma ordem do 10⁻¹⁷ eV local, mas **não idêntico** (outra hipótese de canal: Γ₂₁ = Γ₃₂; E₀ da análise-fonte desconhecido aqui). A identificação entre os dois é [OPEN].

**Contexto de poder [KNOWN da memória canônica]:** a v369 (CLOCK_TEST_V1) já fixou τ★ ≤ 4,8×10¹² t_P ≈ 2,6×10⁻³¹ s (95% CL, relógios, partição P1). A cota de neutrinos é ~21–22 ordens mais fraca. **O valor deste canal não é a magnitude de τ★ — é a FORMA espectral** (n = −2 ⟺ Γ ∝ ω² ∝ E⁻², pois ω = Δm²/2E ∝ E⁻¹ [DERIVED da lei declarada]).

---

## (2) O que pode ser comparado sem trocar hipótese, ordenamento ou confiança

**Regras de comparabilidade (minhas, de auditoria):** só se comparam limites com (a) mesmo canal Γᵢⱼ, (b) mesmo ordenamento (NO/IO), (c) mesma CL, (d) E₀ declarado, (e) mesma forma funcional (n). Violada qualquer uma, a comparação vira [OPEN].

**A conversão auditável (única, completa):** ORCA6 tab. 3, n = −2, 90% CL, Γ₂₁ < 4,6×10⁻²¹ GeV, E₀ = 1 GeV (eq. 15) [KNOWN via contexto]:

- Unidade: 4,6×10⁻²¹ GeV × 10⁹ eV/GeV = **4,6×10⁻¹² eV**.
- ω = Δm²₂₁/(2E₀) = 7,5×10⁻⁵/(2×10⁹) = 3,75×10⁻¹⁴ eV; ω² = 1,40625×10⁻²⁷ eV².
- τ★ < 2 × 4,6×10⁻¹² / (0,0120313 × 1,40625×10⁻²⁷) = 5,4377×10¹⁷ eV⁻¹ × 6,5821×10⁻¹⁶ s/eV⁻¹ ≈ **3,6×10² s** [DERIVED, condicional à lei TGL e à escolha Δm²₂₁].

Leitura: a cota ORCA em τ★ é ~4,6×10¹¹ vezes mais fraca que a solar/KamLAND — esperado sob a lei (Γ_bound 4,6×10⁵ maior; ω² 10⁶ menor). **Não há tensão entre as fontes; há regimes distintos.**

**O que NÃO pode ser comparado nesta chamada:** Γ₃₁ (outro Δm², outro canal TGL — [OPEN]: o contexto não dá Δm²₃₁ nem o mapeamento); De Romeri 2023 (sem números no contexto — [OPEN]: valores, CL, E₀, ordenamento); Fogli 2007 (sem página/tabela/CL para o 10⁻¹⁷ eV — [OPEN]); IceCube n = 0 → n = −2 (promoção proibida — ver item 3).

---

## (3) Errata bibliográfica mínima IceCube e alcance real para n = −2

**Errata mínima [P0 documental]:** em `tgl_dephasing_falsifier.py:34`, a citação de “Γ₀ ≤ 1,17×10⁻¹⁵ eV” a **arXiv:2503.13061 está errada** — esse identificador é Nandi et al., artigo **teórico** com escala **E⁻⁴** (incompatível com a forma n = −2; não serve de suporte a este canal). O documento correto é **arXiv:2308.00105** (IceCube), que reporta Γ₀ ≤ 1,17×10⁻¹⁵ eV **em modelo n = 0** e um **caso separado n = +2** [KNOWN via contexto]. Corrigir também a etiqueta **“10.7 yr”**, que carece de fonte correspondente auditável [OPEN].

**Alcance real para n = −2:** **nulo como limite.** O artigo não apresenta análise n = −2 no material recuperado; qualquer cota n = −2 a partir dele seria extrapolação não auditada [OPEN]. Conforme a instrução: **não promover o limite n = 0 para n = −2.**

---

## (4) Interferometria de matéria (Pedalino et al. 2026): observável TGL existe?

**Não, no estado atual [OPEN].** O experimento demonstra interferência de nanopartículas de sódio [KNOWN via contexto; Nature s41586-025-09917-9] — **isso não é automaticamente um limite TGL** (instrução do próprio pedido, endossada). Para virar teste da lei Γ_ω = ½βτ★ω² faltam três peças, todas ausentes nesta chamada:

1. **Mapa TGL → ω efetivo.** Na rota local, ω é definido para oscilação de neutrinos (Δm²/2E) e, na v369, para frequências de relógio. Para uma nanopartícula não há Δm² análogo declarado; identificar ω com separação de energia dos braços ou frequência interna é **hipótese nova, não derivada**.
2. **Mapa TGL → visibilidade/ruído.** O observável experimental é contraste de franjas vs massa/tempo; sem a cadeia Γ_ω → perda de visibilidade → separação do fundo de decoerência ambiental, nenhum número de τ★ pode ser extraído.
3. **Separação de modelos.** Transpor cotas de modelos de colapso macroscópico (CSL/DP) para a lei TGL sem demonstração está **proibido** pelo pedido — e seria, de fato, troca de hipótese física.

---

## Tabela por canal (fatos dos artigos × minhas inferências separados)

| Canal / fonte (localização) | Estatuto | Parâmetro; E₀; unidades | CL | Hipótese sabor/ordenamento | Limite vs projeção | Poder demonstrado | Lacuna |
|---|---|---|---|---|---|---|---|
| Solar/KamLAND — Fogli et al. 2007 (arXiv:0704.2568), via `tgl_dephasing_falsifier.py:32` | [INPUT não auditado nesta chamada; OPEN leitura integral] | γ ≲ 10⁻¹⁷ eV; E₀ = 1 MeV (declarado no script); n = −2 | [OPEN] | ν_e, Δm²₂₁ [KNOWN]; ordenamento insensível (Δm²₂₁ solar) | Limite (não projeção) | Sustenta τ★ ≤ 7,78×10⁻¹⁰ s [DERIVED desta revisão, condicionado aos inputs]; zero poder de detecção | Página/tabela/CL do valor; relação com ORCA tab. 4 (7,9×10⁻¹⁸ eV) — mesma ordem, identificação [OPEN] |
| De Romeri et al. 2023 (arXiv:2306.14699, JHEP 09 097) | [KNOWN existência/escopo via contexto; OPEN valores] | Cenários Γᵢⱼ vários | [OPEN] | [OPEN] | [OPEN] | Nenhum auditável nesta chamada | Valores, CL, E₀, ordenamento |
| KM3NeT/ORCA6, JCAP 03 (2025) 039 — tab. 3 (arXiv:2410.01388v2) | [KNOWN via contexto] | Γ₂₁ < 4,6×10⁻²¹ GeV = 4,6×10⁻¹² eV; Γ₃₁ < 8,4×10⁻²¹ GeV; E₀ = 1 GeV (eq. 15); n = −2 | 90% (conservador) | Canais Γ₂₁/Γ₃₁ separados; tabelas distinguem NO/IO — qual coluna para estes valores: [OPEN] | Limite | Limite direto n = −2 em GeV; sob a lei: τ★ ≲ 3,6×10² s [DERIVED, conta em §2] | Valor nominal vs conservador; ordenamento por linha |
| ORCA tab. 4 (compilação, caso KamLAND) | [KNOWN via contexto] | Γ₂₁ = Γ₃₂ < 7,9×10⁻²⁷ GeV = 7,9×10⁻¹⁸ eV; n = −2 | 90% | **Γ₂₁ = Γ₃₂** (≠ Γ₂₁ isolado) | Limite reportado | Sanidade da ordem de grandeza do 10⁻¹⁷ eV local | Fonte primária, E₀, e identificação com o valor do script [OPEN] |
| IceCube (arXiv:2308.00105) | [KNOWN via contexto] | Γ₀ ≤ 1,17×10⁻¹⁵ eV; modelo n = 0; caso n = +2 | [OPEN no resumo fornecido] | n = 0 / n = +2 — **sem n = −2** | Limite | **Nenhum para n = −2** | Análise n = −2 inexistente no material recuperado |
| Nandi et al. (arXiv:2503.13061) | [KNOWN via contexto] | Teórico; escala E⁻⁴ | — | — | Não é limite | **Não usar como fonte** neste canal | Citação indevida na linha 34 |
| Pedalino et al. 2026 (Nature s41586-025-09917-9) | [KNOWN via contexto] | Interferência de nanopartículas de sódio | — | — | Demonstração (não limite TGL) | **Nenhum observável TGL** | Mapa ω efetivo → visibilidade/ruído [OPEN] |

**Auditoria dos enunciados da rota local:** NO DETECTION (consistente: só limites superiores) ✓; n UNMEASURED (consistente: γ₀→0 ajusta todos os limites) ✓; n = −2 ALLOWED (consistente: Δχ²(n = −2) = 0,00 contra limites [KNOWN, memória canônica]; ORCA limita sem excluir) ✓; τ★ ≤ 7,8×10⁻¹⁰ s (aritmeticamente consistente; proveniência do γ pendente) ⚠.

---

## Erros

**P0 (proveniência bloqueante):**
1. Citação IceCube incorreta em `tgl_dephasing_falsifier.py:34` (arXiv:2503.13061 não contém o número; correto: arXiv:2308.00105; remover ou fontar “10.7 yr”).
2. Proveniência não fixada de γ ≲ 10⁻¹⁷ eV @ 1 MeV (linha 32), que sustenta a única cota τ★ do canal: sem artigo/tabela/CL, a cota é DECLARADA, não inscrita.

**P1 (risco de leitura):**
3. Risco estrutural de promoção de limites n = 0 → n = −2 em textos futuros (prevenir com nota explícita junto à tabela IceCube).
4. Hipótese Γ₂₁ = Γ₃₂ (ORCA tab. 4) ≠ Γ₂₁ isolado (script): declarar a diferença antes de qualquer identificação numérica.
5. CL do limite solar/KamLAND ausente do material local.

**P2 (higiene):**
6. Δm²₂₁ = 7,5×10⁻⁵ eV² usado nesta revisão é [KNOWN externo, NuFIT], não lido dos artefatos nesta chamada; fixar valor e fonte no cabeçalho.
7. E₀ = 1 MeV e CL devem constar no cabeçalho dos scripts (a cota é sensível a E²).
8. Ordenamento NO/IO das linhas da ORCA tab. 3 não fixado no contexto.

**Menor próximo passo verificável (pendência — não executo aqui):** leitura pontual de Fogli et al. 2007 (arXiv:0704.2568) e da referência citada pela ORCA tab. 4 para o “caso KamLAND”, extraindo (valor, E₀, CL, canal Γᵢⱼ, ordenamento); em seguida corrigir a linha 34 (arXiv:2308.00105) e inscrever a proveniência na linha 32 com E₀ e CL. É tarefa de leitura/edição, fora do meu escopo executivo nesta revisão — fica identificada como pendência.

**Régua final:** NOT_FALSIFIED ≠ CONFIRMED. Nada nesta revisão move gate, autoriza execução ou confirma a teoria; a cota auditada é condicional à lei declarada e aos inputs nomeados.
