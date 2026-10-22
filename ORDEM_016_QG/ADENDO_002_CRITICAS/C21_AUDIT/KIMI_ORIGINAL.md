# Crítica cética C2.1 — Os cinco probes A1.b contra o contrato v3.1

**Estatuto desta resposta:** `[DECLARADO até confronto da bancada]`. Crítica EXTERNA de forma e alcance, não repetição de compilação mecânica. Não recompilei nada: os recibos `rc=0` são **lidos** do manifest carregado (`A1_delivery_manifest.json`, projeção parcial), não reproduzidos por mim. As fontes chegaram como `PARTIAL_PROJECTION` — **linhas omitidas não foram examinadas**; onde isso muda o veredito, está marcado `[LACUNA de projeção]`. Nenhum habitante H2/H3 físico é fabricado aqui; nenhum nome reservado é criado; o gate não se move. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED ≠ CONFIRMED.

**Régua de classificação usada** (derivada da própria casa): um probe *detecta enfraquecimento do contrato v3.1* só se (i) ataca as **definições reais** do contrato (não um modelo paralelo com o mesmo vocabulário — homônimo ≠ identidade); (ii) não é vacuidade (a estrutura mutante tem habitante, ou a exclusão vale sobre um caso possível); (iii) não é mera falta de premissa (o objeto testado falha numa cláusula que o contrato efetivamente exige); e (iv) tem controle que **pode quebrar**. Um check que não pode falhar não é medida.

---

## 0. Dois achados transversais antes dos probes

**0.1 — O ramo (a) está NÃO PAGO, e isso limita o alvo de todos os probes.** A entrega declara: *"MEDIDA/NÃO PAGO na reprodução integral: duas falhas de memória em 8 GiB; corpo do tipo v3.1 preservado em variante de imports e trechos literais selecionados recompilados. Não se afirma reproduzir seis negativos originais."* (`ENTREGA_016_A1_contrato.md`, linha 7). Consequência: os cinco probes auditam o tipo v3.1 **conforme recompilado na variante `ContratoQG_v31_Minimal.lean`**, não os bytes do corpo original. Nada aqui os invalida — mas toda conclusão da forma "o contrato v3.1 tem a propriedade X" é **condicional à fidelidade da variante**. `[LACUNA nomeada, NÃO encomendada agora, por ordem expressa]` — o menor artefato futuro seria um check de identidade definicional (ou textual) entre as cláusulas consumidas pelos probes e as do corpo original.

**0.2 — A suíte testa enfraquecimentos; ninguém testa a existência.** Os cinco probes atacam cláusulas (comutação, simetria, energia, KMS, suavidade/normalização). Nenhum verifica se o contrato **fortalecido ainda é habitável** — e o acervo já mediu esse modo de falha duas vezes: `ProbeToyContratoH2` (a v2 era habitável por brinquedo) e `W5ParedeEspectral` (a cláusula (S) forçava espectro pontual — a v2 era **vazia no par físico**, boost livre sem autovetores `[KNOWN]`). O próprio veredito do contrato no selo da casa é `...NOT_INHABITED_BY_THE_LEGACY_PAIR__NON_VACUITY_OPEN...`. **Cinco probes fortes podem certificar um tipo vazio.** Menor reparo de suíte: um item de escopo declarado (b0) dizendo "esta suíte é só de falsificação de forma; a não-vacuidade segue [OPEN]", ou um probe de não-vacuidade mínima. κ (calibre; `κ/T = 2π` por tipo; G não predito) e os quatro índices `[INPUT]` ((W₀,R₀), N₀, T₀, m_pos) ficam **fora de escopo por desenho** — correto, mas deve constar para que "passou nos cinco" não seja lido como mais do que é.

---

## 1. b1 — não comutação (`ProbeNoncommutingInternal_v4.lean`)

**O que o arquivo prova (testemunha):** `U(a) = !![1,0,0; 0, phase (a 0), 0; 0,0,1]` (linhas 18–19) e `D(t)` rotação real no plano (linhas 20–21), ambos fixando `e0`, com ações não comutantes. O próprio docblock (linhas 10–13) declara: *"Finite CONTROL, not an AQFT witness... Translations only read a0 and therefore cannot satisfy the actual faithful-translation field of ContratoH2. No identification of D with the genuine modular flow is assumed."*

**Classe: NÃO detecta enfraquecimento do contrato — testa uma tipagem mais fraca, declarada pelo próprio probe.** Três objeções:

1. **A premissa central do contrato falha no modelo, e o modelo o admite.** Para `a = (0, a₁, a₂, a₃) ≠ 0`, `phase (a 0) = 1`, logo `U a = 1` com `a ≠ 0`: a família **não é fiel em ℝ⁴** (nem em ℝ²). O campo do v3.1 é "translações fiéis de energia positiva" (acervo, veredito v3.1). Logo b1 não toca o ContratoH2; mede apenas "existe grupo a um parâmetro com controle unitário não comutante e vácuo comum" — um controle de fumaça da *ideia*, não um probe.
2. **`D(t)` é uma rotação SO(2) qualquer, não Δ^{it}** — homônimo de "fluxo" sem a estrutura modular. O docblock se protege; a crítica registra que a proteção é necessária porque o risco de leitura promocional é real.
3. **Achado estrutural novo (o reparo não é "fortalecer U" — é um teto):** `[DERIVADO nesta análise, a conferir em kernel]` uma ação de ℝⁿ por **matrizes de fase** com `d_f` fases independentes é fiel **somente se `d_f ≥ n+1`**. Prova curta: o kernel é `{a : ∀j, ω_j·a ∈ 2πℤ}`; para `d_f ≤ n` esse sistema tem sempre solução não trivial (se `d_f < n`, já o kernel real do mapa linear é não trivial; se `d_f = n` e det ≠ 0, `a = L⁻¹ m` com `m ∈ ℤⁿ \ {0}` resolve). Suficiência: com `d_f = n+1` e frequências `{1, α₁, …, αₙ}` linearmente independentes sobre ℚ, o mapa `x ↦ (e^{ix₁},…,e^{ixₙ}, e^{i Σ αⱼxⱼ})` é injetivo. Em `V = Fin 3 → ℂ` com `e0` fixo, `d_f = 2` — logo **o máximo realizável é ℝ¹**; o contrato pede ℝ⁴, que exige `d_f ≥ 5`, i.e., `V = Fin 6 → ℂ` no mínimo.

**Menor reparo (PROPOSTA, sem fabricar habitante do contrato):** rebaixar e explicitar o alvo — "ação fiel de ℝ¹ (subgrupo a um parâmetro) + controle não comutante" (possível já em Fin 3: `t ↦ diag(1, e^{it}, e^{it√2})` é fiel, pois `t ∈ 2πℤ ∧ t√2 ∈ 2πℤ ⟺ t=0`); **ou** migrar o probe para `V = Fin 6` com `U(a) = diag(1, e^{ia₀}, e^{ia₁}, e^{ia₂}, e^{ia₃}, e^{i(α₀a₀+…+α₃a₃)})` com `{1, α₀,…,α₃}` ℚ-independentes, provando `fiel ∧ U e0 = e0 ∧ ∃t, U D ≠ D U`, com **controle negativo**: a família velha (só `a₀`) reprova a fidelidade — ela quebra, logo o teste mede. Em ambos os casos, manter tipado que o fragmento testado **não** inclui rede, energia positiva nem implementação modular — senão o reparo recria o homônimo que o docblock evitou. Menor lema faltante: `faithful_Rn_phases_iff_df_ge_succ` (a bicondicional acima) em kernel, pois ela decide o teto de qualquer b1 finito.

---

## 2. b2 — tensor forjado (`ProbeForgedStressContract.lean` + `ProbeForgedStress_v2.lean`)

**O que os arquivos provam (testemunha):** ataque **condicional às definições reais** — `def forgedTensor (T : StressTensorData W) : StressTensorData W` aplicando `forge (T.T ψ x) (nullEnergy T ψ x)` (linhas 21–22). O controle algébrico independente isola o mecanismo: `transverseSkew a` antissimétrico nas direções (2,3) (linhas 20–21) com `nullVector = ![1,1,0,0]` e `nullRead = 0` — a contração nula `n^μn^νT_μν` é **cega à ambiguidade antissimétrica transversa**. Docblocks honestos: *"The attack disproves enforcement of symmetry, not spacelike locality itself"* (linha 11); *"No assertion of locality/nonlocality follows solely from a matrix of expectations"* (`_v2`, linha 13). A definição exata de `forge` está em linhas omitidas `[LACUNA]`.

**Classe: DETECTA enfraquecimento genuíno do tipo — com escopo correto e uma fronteira que a crítica deve cravar.**

1. **Demonstrado:** a simetria `T_μν = T_νμ` **não é forçada** pelas cláusulas que o tipo lê; há habitantes não simétricos com a mesma leitura nula e a mesma resposta. Isto é um diagnóstico real sobre `StressTensorData`, não sobre um modelo paralelo.
2. **Fronteira (objeção externa):** a lei local do v3.1 consome **`T_nn`** (`dθ/dλ = −8πG T_nn`, acervo). Como `T_nn` é invariante sob a parte antissimétrica, **a ambiguidade não contamina a equação local** — o enfraquecimento é de forma do tipo, não da leitura física, *a menos* que outra cláusula consumidora leia componentes fora da nn. Testemunha de que essa distinção ainda não está tipada: nenhuma linha carregada mostra um teorema "as leituras consumidas são invariantes sob forge".
3. **Conservação não mata o forge:** `[DERIVADO nesta análise]` `transverseSkew a` é **constante em x**, logo tem divergência nula — se `StressTensorDataLocal_v2.lean` exige conservação distribucional (linhas 26–34, parcial), o tensor forjado **também passa nela**. A falha é especificamente a simetria. `[LACUNA: verificar nas linhas omitidas se a camada local já exige simetria]`.

**Menor reparo:** (α) cláusula de simetria explícita no tipo do tensor (v3.2: `T_sym : ∀ ψ x, (T ψ x)ᵀ = T ψ x`), tornando `forge` inabitável; **ou**, se a casa preferir o tipo permissivo, (β) o lema `symmetrized_forge_eq_symmetrized` + a prova de que **toda** cláusula consumidora lê apenas a parte simétrica — com controle negativo: sem simetrização, `transverseSkew` altera alguma leitura fora da nn (ex.: `T₂₃`). Sem (α) ou (β), o veredito correto do probe permanece "simetria não forçada — sem consequência demonstrada para a lei local".

---

## 3. b3 — energia positiva (`ProbePositiveEnergy_v2.lean` + `AnalyticBoundaryControl_v2.lean`)

**O que os arquivos provam (testemunha):** `bounded_upper_extension_unique_negative_phase` (linha 13): se `F` é `DiffContOnCl` no semiplano superior, limitada, com borda `F t = exp(-i·t)`, então `F z = exp(-i·z)`; e `negative_phase_has_no_bounded_upper_extension` (linha 42): tal extensão **não existe** (coerente: `e^{-iz}` explode para `Im z > 0`). Estrutura correta: unicidade condicional + inexistência — e a entrega resume corretamente: *"Consumidor analítico de PositiveEnergy exclui modo unitário de frequência negativa"* (linha 10). O docblock do controle compartilhado declara: *"no physical witness is assumed here"* (`AnalyticBoundaryControl_v2.lean`, linha 4).

**Classe: controle analítico genuíno e bem construído — mas o objeto excluído é uma FUNÇÃO de borda, não um MODO do contrato.** Duas objeções:

1. **Falta (visivelmente) o lema-ponte.** A condição de energia positiva do contrato vive sobre representações unitárias; o probe prova fatos sobre funções ℂ→ℂ. A ponte — *espectro de Stone com suporte em `[0,∞)` ⟺ `t ↦ ⟨ψ, U(t)ψ⟩` admite extensão limitada ao semiplano* — **não aparece nas linhas carregadas** `[LACUNA: pode existir nas omitidas; se existir, esta objeção cai e deve ser citada]`. Nota de acervo: a rota já existe na casa (`TGLExt.RetaDeLuzBorchers`, v371 — energia positiva `ax+b`, forma de Borchers com o 2π `[KNOWN, fonte primária conferida na memória: Borchers CMP 143 (1992)]`), de modo que o reparo é **ligação tipada**, não pesquisa nova.
2. **A convenção de sinal é INPUT, não teorema.** "Energia positiva ⟺ extensão limitada a *qual* semiplano" depende da convenção de Fourier; o probe crava uma (coerente: `e^{+iωt}`, ω>0, tem extensão `e^{-ωy}` limitada no semiplano superior; `e^{-iωt}` não tem). Legítimo — mas deve estar tipado como convenção, sob pena de um probe espelhado "provar o oposto" trocando o sinal.

**Menor reparo:** o teorema-ponte no modelo do probe (`PositiveEnergy (campo) ⟹ correladores na classe de Hardy do semiplano superior`, com remissão à pedra v371/[KNOWN]), instanciado no campo real do contrato; controle negativo já pago (o modo `e^{-it}` reprova). Declarar a convenção de sinal no enunciado.

---

## 4. b4 — não-KMS (`ProbeNonKMS_v3.lean`)

**O que o arquivo prova (testemunha):** `horizontal_zero_on_closed_strip` (linhas 13–21): `f` analítica e limitada na faixa `0 < Im z < b`, nula na borda real, é identicamente nula na faixa fechada; a aplicação (linha 32, parcialmente omitida) consome `hkms A hA B hB` obtendo as duas expectativas de borda. Entrega (linha 11): *"KMSAt rejeita fluxo identidade quando as duas expectativas de borda não coincidem."*

**Classe: genuíno como exclusão CONDICIONAL — e a condição precisa ser nomeada, ou o probe é mal lido.** A matemática está correta: com fluxo identidade, KMS força `ω(AB) = ω(BA)` (tracialidade); bordas distintas ⟹ não existe `F` ⟹ `¬KMSAt`. É exatamente a marca de não-tracialidade (coerente com o acervo: `the_dead_weight`/`NoNormalTrace`). Três objeções:

1. **O probe rejeita o PAR (fluxo identidade ∧ estado não tracial), não o fluxo identidade.** Se o contrato admitisse estado tracial, o fluxo trivial seria KMS-legítimo. A força do probe depende de a não-tracialidade do estado estar **tipada no objeto testado** — e a testemunha concreta `(A, B)` com bordas distintas não aparece nas linhas carregadas `[LACUNA]`.
2. **Falta o controle positivo.** Para demonstrar que a condição testada é a não-tracialidade (e não qualquer outra falha do canal), o probe precisa do lado que passa: `tracial_state ∧ fluxo identidade ⊨ KMSAt`. Um check que só reprova não mede.
3. **A altura da faixa `b` é genérica**; a correspondência com a temperatura do contrato (`κ/T = 2π` por tipo) precisa estar instanciada `[LACUNA: verificar na aplicação omitida]`.

**Menor reparo:** teorema final com as três premissas explícitas — (α) fluxo = identidade; (β) testemunhas `A, B` exibidas com bordas distintas; (γ) faixa = a do contrato — mais o controle positivo tracial. Sem isso, b4 é uma exclusão condicional correta com a condição subnomeada.

---

## 5. b5 — suavidade/normalização (`ProbeFieldMutations_v2.lean`)

**O que o arquivo mostra (testemunha):** as estruturas mutantes `H2WithoutSmooth` (linha 10; mantém `kappa`, `kappa_pos`, `Δit`, `flow_implemented`, …) e `H3WithoutUnit` (linha 47; **contém o campo `H2 : ContratoH2 W R N`**, linha 50). A entrega **não exibe linha de resumo para b5** (projeção, linhas 12–26 vazias), e nenhuma linha carregada mostra teorema habitando as mutações nem provando estritude. `[LACUNA de projeção — esta auditoria é estrutural, não de conteúdo]`.

**Classe: NÃO AUDITÁVEL na forma carregada — com o risco duplo já medido no acervo.**

1. **Vacuidade:** se a estrutura mutante não tem habitante, o probe testa o nada.
2. **Brinquedo:** se é habitada por um trivial que também falha o campo removido, mede apenas "sem o campo, o campo falta" — tautologia. Os dois modos já aconteceram nesta casa (v2: habitada por brinquedo; cláusula (S): vazia no par físico).
3. **Herança condicional:** `H3WithoutUnit` exige um `ContratoH2` habitado — a dívida central, não fabricada. Se a mutação é habitada **sob a hipótese de um H2**, é CONDICIONAL e deve ser rotulada como tal; se não é habitada de todo, recai em (1).
4. **Nota de classe:** mesmo bem-sucedido, b5 decide **independência de campos** (metateste), não enfraquecimento físico — é o menos decisivo dos cinco: sua ausência não cega o contrato; sua presença não o fortalece fisicamente (um campo redundante não é um dano; um campo independente num tipo vazio não é um ativo).

**Menor reparo (por mutação):** o par — (α) teorema de habitabilidade `∃ dados satisfazendo (todas as cláusulas − este campo) ∧ ¬ este campo`, com as **demais cláusulas verificadas no habitante** (isolamento); e (β) controle: o mesmo objeto **não** habita a estrutura plena, porque o campo removido falha. Resultado possível legítimo e útil: descobrir que um campo é **consequência** das outras cláusulas (aí a mutação é desnecessária e o probe deve provar essa implicação em vez disso).

---

## 6. Tabela-síntese `[DECLARADO]`

| probe | ataca as defs reais? | habitado/não-vazio? | classe | menor reparo |
|---|---|---|---|---|
| **b1** não comutação | **não** (declarado, l.10–13) | sim, mas num fragmento mais fraco | tipagem mais fraca + **teto novo**: fiel ℝ⁴ impossível em Fin 3 (`d_f ≥ n+1`) | ação fiel de ℝ¹ declarada, ou Fin 6 + ℚ-independência + controle negativo; lema do teto em kernel |
| **b2** tensor forjado | **sim** (`StressTensorData`) | condicional (H3 e fonte como hipóteses) | **detecta**: simetria não forçada; sem consequência demonstrada para `T_nn` | cláusula de simetria (v3.2) ou lema de invariança das leituras consumidas; conservação **não** mata o forge |
| **b3** energia positiva | indireta (análise ℂ) | sim (exclusão provada) | controle analítico genuíno; falta a ponte campo↔Hardy | teorema-ponte Stone/Hardy ligado a `RetaDeLuzBorchers` [KNOWN] + convenção de sinal tipada |
| **b4** não-KMS | sim (KMSAt) | condicional | exclusão condicional correta; condição subnomeada | premissas (α)(β)(γ) explícitas + controle positivo tracial |
| **b5** suavidade/normalização | estruturas mutantes | **desconhecido** `[LACUNA]` | não auditável; risco vacuidade/brinquedo | par habitabilidade+isolamento por campo; rotular herança condicional de H2 |

## 7. Veredito e pendências (não encomendadas)

1. **A entrega é honesta nos docblocks** — b1 ("not an AQFT witness"), b2 ("disproves enforcement of symmetry, not locality"), b3/b4 ("no physical witness is assumed"). A crítica externa **confirma as declarações** e acrescenta: o risco não está nos arquivos, está na **leitura posterior** que promova os probes além do declarado. Reparo institucional mínimo: registrar no manifest/índice a **classe** de cada probe (controle de forma / ataque condicional / consumidor analítico / metateste de independência).
2. **Conclusão por probe:** b2 é o único que ataca as definições reais com diagnóstico fechado (e mesmo assim sem consequência demonstrada para a lei local `T_nn`); b3 e b4 são analiticamente corretos e condicionais; b1 é tipagem mais fraca com um **teto estrutural** que nenhum reparo em Fin 3 remove (`d_f ≥ n+1` — lema candidato); b5 permanece não auditável.
3. **Pendências nomeadas, não encomendadas agora** (por ordem expressa): fidelidade da variante Minimal ao corpo v3.1 (ramo a); item de escopo de não-vacuidade da suíte; verificação nas linhas omitidas de (i) simetria em `StressTensorDataLocal`, (ii) eventual ponte já existente em b3, (iii) testemunhas `A,B` e faixa em b4, (iv) teoremas de b5.
4. **O caminho crítico não se move:** H2 segue sendo o pagamento; H3 no mesmo horizonte; κ na face curva; setor interagente; a não-vacuidade do contrato no par físico segue `[OPEN]`. Nada aqui é confirmação física; nada aqui move o gate.