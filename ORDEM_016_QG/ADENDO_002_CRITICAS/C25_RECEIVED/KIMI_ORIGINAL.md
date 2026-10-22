# C2.5 — Plano de integração em partes para as DOZE fontes da ficha T20

**Estatuto desta resposta: `[DECLARADO]`** — plano auditável, sem execução, sem compilação, sem leitura integral dos arquivos (trabalhei sobre as projeções parciais fornecidas, `[PROJEÇÃO PARCIAL]`), sem confirmação física, sem criação de nomes reservados, sem mover gate algum. A Parte C3 executará após A8; o juiz de cada passo é a compilação isolada (rc0) e o `#print axioms` no trio `{propext, Classical.choice, Quot.sound}`, zero `sorry`, zero axioma `TGL.*` novo. Onde algo é proposta e não fato lido, está marcado `[PROPOSTA]`; onde falta insumo, está marcado `[LACUNA]`.

---

## 1. Diagnóstico demonstrado (lido das projeções)

As doze fontes, seus imports locais e seus namespaces, conforme as projeções:

| # | arquivo | imports locais (lidos) | namespace |
|---|---|---|---|
| 1 | `TheEquationOfTruth_T20_v3.lean` (749 l.) | `Mathlib`, `TGLExt.TheNameIsTheInstrument` | `TGLExt.EquationOfTruth` |
| 2 | `InscriptionBridge.lean` (69 l.) | `TheEquationOfTruth_T20`, `TGLExt.NameIsTheContent` | `TGLExt.EquationOfTruth` |
| 3 | `PenaltyThreeLocksBridge_v2.lean` (25 l.) | `TheEquationOfTruth_T20`, `TGL.FiniteThreeLocks` | `TGLExt.EquationOfTruth` |
| 4 | `OperatorContourBridge_v2.lean` (48 l.) | `InscriptionBridge`, `TGLExt.TheContourOfTruth` | `TGLExt.EquationOfTruth` |
| 5 | `QubitScalarEntropy.lean` (127 l.) | (só Mathlib seletivo) | `...EquationOfTruth.QubitScalar` |
| 6 | `QubitEntropyDerivative_v3.lean` (60 l.) | `QubitScalarEntropy`, Mathlib seletivo | `...QubitScalar` (reabre) |
| 7 | `IdempotentDephasing_v2.lean` (48 l.) | (só Mathlib seletivo) | `...IdempotentDephasing` |
| 8 | `FiniteGapRate_v2.lean` (78 l.) | `TheEquationOfTruth_T20_v3` | `TGLExt.EquationOfTruth` |
| 9 | `InfiniteLimitUniformControl_v2.lean` (54 l.) | (só Mathlib seletivo) | `...InfiniteLimitControl` |
| 10 | `ModularGeneratorControl.lean` (67 l.) | `TGLExt.ContinuousModularZero`, Mathlib seletivo | `...ModularGeneratorControl` |
| 11 | `TheEquationOfTruth_T20_controles_v3.lean` (202 l.) | `OperatorContourBridge_v2`, Mathlib seletivo | `...NegativeControls` |
| 12 | `NegativeControlsCompleteness_v2.lean` (32 l.) | `TheEquationOfTruth_T20_controles_v3` | `...NegativeControls` (reabre) |

**D1 — A divergência estrutural do grafo (demonstrada pelas linhas de import).** Os arquivos 2 e 3 importam `TheEquationOfTruth_T20` (sem sufixo); o arquivo 8 importa `TheEquationOfTruth_T20_v3`. Entre as doze fontes só existe o `_v3`. **A fonte `TheEquationOfTruth_T20.lean` (sem sufixo) não está no conjunto.** Isto é um ponto de falha real, não cosmético: se `penalty` (referenciado em `PenaltyThreeLocksBridge_v2:10-11`) vive no `T20` sem sufixo e não no `_v3`, as pontes quebram contra o núcleo novo. Não posso decidir isto sem leitura integral — fica como pendência P0 (§8).

**D2 — O núcleo puxa `import Mathlib` monolítico** (fonte 1, linha 9), enquanto as fontes 5–7 e 9 já usam imports seletivos. Combinado com `maxHeartbeats` de 800000–1400000 (fontes 6, 8, 11 e outras) e com alvo de elaboração único, esta é a hipótese estrutural mais plausível para o pico de memória medido registrado na ficha (`MEASURED_PACKAGING_GAP`). **[DIAGNÓSTICO PLAUSÍVEL — não medido por mim; o valor do pico não consta nas projeções [LACUNA].]**

**D3 — A cobertura de cinco nós do parecer 12e2b4f2.** O grafo resolvido pelo parecer anterior é a cadeia 1→2→4→11→12. Ficaram fora os nós 3, 5, 6, 7, 8, 9, 10 — sete dos doze. Este plano ataca exatamente essa insuficiência: o DAG completo abaixo cobre os doze, incluindo as três folhas independentes (5/7/9) e os dois módulos ligados ao kernel maior (10 via `ContinuousModularZero`, 3 via `TGL.FiniteThreeLocks`).

**D4 — Namespaces já são compatíveis com pacote em partes.** Todas as fontes vivem sob `TGLExt.EquationOfTruth.*`, com subnamespaces disjuntos (`QubitScalar`, `IdempotentDephasing`, `InfiniteLimitControl`, `ModularGeneratorControl`, `NegativeControls`). Reabertura de namespace entre arquivos (5→6, 11→12) é legal em Lean 4. Nenhuma fusão de namespace é necessária — logo nenhuma duplicação de nomes precisa ser criada.

---

## 2. Separação das trilhas (pedido explícito do operador)

**Trilha R — manter o prefixo V3 intacto como artefato de referência.** Congelar os 12 arquivos, byte a byte, em pasta de referência **fora do build**, com manifesto sha256 próprio (a abertura `216a1a7d…` da ficha ancora o conjunto; o manifesto registra arquivo a arquivo). Custo: zero. Serve como fonte de verdade para o diff de corpos (V-BODY, §6) e como fallback. **Não cumpre a ficha sozinha** (o destino `TGLExt/TheEquationOfTruth.lean` não passa a existir), mas é a Fase 0 obrigatória de qualquer das outras trilhas.

**Trilha M — monólito (avaliada, rejeitada como caminho principal).** Concatenar os 12 corpos (~1559 linhas) num único `TGLExt/TheEquationOfTruth.lean`. Rejeitada por quatro razões auditáveis: (i) um único alvo de elaboração com `import Mathlib` inteiro e três arquivos de heartbeats ≥ 800k reproduz, no mesmo processo, exatamente a configuração candidata ao pico medido — a direção errada; (ii) a fusão força convivência de todas as declarações no mesmo escopo de elaboração, maximizando o risco de colisão de nomes e de instâncias anônimas (lição da casa, v324: módulos que compilam sozinhos podem não coexistir); (iii) perde o build incremental e a paralelização por módulo; (iv) diffs ilegíveis. **Não prometo que o monólito cabe nem que não cabe; só o descarto como primeira rota por análise estrutural, não por medição.**

**Trilha P — pacote em partes (RECOMENDADA `[PROPOSTA]`).** Doze módulos estáveis + um arquivo-índice, na ordem topológica do §3, com imports seletivos, corpos preservados byte a byte e o V3 congelado como referência. É a única trilha que atende simultaneamente: cobertura dos doze, preservação dos corpos, não-duplicação de nomes e redução do alvo de elaboração por processo.

---

## 3. Trilha P — ordem topológica (DAG completo, 12 nós)

Nomes de módulo propostos **sem sufixos de versão** (a versão vive no manifesto e na pasta de referência; a casa já usa nomes estáveis, cf. `TGLExt.TheNameIsTheInstrument`). `[PROPOSTA — ratificação da gerência]`

**Nível 0 — folhas (zero dependências locais):**
- `TGLExt.EquationOfTruthQubitScalar` ← fonte 5
- `TGLExt.EquationOfTruthIdempotentDephasing` ← fonte 7
- `TGLExt.EquationOfTruthInfiniteLimit` ← fonte 9

**Nível 1 — núcleo e independentes de primeiro andar:**
- `TGLExt.EquationOfTruthCore` ← fonte 1 (dep. externa: `TGLExt.TheNameIsTheInstrument`)
- `TGLExt.EquationOfTruthQubitDerivative` ← fonte 6 (dep: QubitScalar)
- `TGLExt.EquationOfTruthModularGenerator` ← fonte 10 (dep. externa: `TGLExt.ContinuousModularZero`)

**Nível 2 — pontes sobre o Core:**
- `TGLExt.EquationOfTruthInscription` ← fonte 2 (dep: Core; externa: `TGLExt.NameIsTheContent`)
- `TGLExt.EquationOfTruthPenaltyThreeLocks` ← fonte 3 (dep: Core; externa: `TGL.FiniteThreeLocks`)
- `TGLExt.EquationOfTruthFiniteGapRate` ← fonte 8 (dep: Core)

**Nível 3:**
- `TGLExt.EquationOfTruthOperatorContour` ← fonte 4 (dep: Inscription; externa: `TGLExt.TheContourOfTruth`)

**Nível 4:**
- `TGLExt.EquationOfTruthNegativeControls` ← fonte 11 (dep: OperatorContour)

**Nível 5:**
- `TGLExt.EquationOfTruthNegativeControlsCompleteness` ← fonte 12 (dep: NegativeControls)

**Índice (arquivo da ficha):** `TGLExt/TheEquationOfTruth.lean` — apenas imports dos módulos + docstring de escopo. Linha em `TGLExt.lean`: `import TGLExt.TheEquationOfTruth` (conforme ficha, linha 7).

**Ausência de ciclos:** verificável por inspeção do DAG acima (toda aresta desce um nível). **Paralelização:** níveis 0 e 1 têm 6 módulos independentes; nível 2 tem 3 — o build elabora até 6 alvos em paralelo, cada job com seu próprio heap, o que ataca o pico por divisão de alvo, não por promessa.

**Decisão pendente (a ratificar):** o índice público reexporta os 10 positivos (níveis 0–3). Os 2 módulos de controles (níveis 4–5) **compilam** (não são negativos-de-recusa no sentido da casa; são teoremas sobre controles) — proposta: entram no build como módulos auditados, mas **fora do índice de reexportação**, preservando a separação positivo/controle que a casa pratica. `[PROPOSTA]`

---

## 4. Tabela arquivo → imports removidos / adicionados

| módulo novo | REMOVER | ADICIONAR | notas |
|---|---|---|---|
| `EquationOfTruthCore` (fonte 1) | `import Mathlib` (monólito) | **lista mínima a derivar por redução incremental** (candidatos iniciais, não afirmados: `Mathlib.Analysis.InnerProductSpace.*`, `Mathlib.Topology.*`, `Mathlib.Tactic`, conforme o corpo exigir) — verificação V-IMPORTS (§6) | mantém `import TGLExt.TheNameIsTheInstrument` |
| `EquationOfTruthQubitScalar` (5) | — | — | já seletivo; modelo para os demais |
| `EquationOfTruthIdempotentDephasing` (7) | — | — | já seletivo |
| `EquationOfTruthInfiniteLimit` (9) | — | — | já seletivo |
| `EquationOfTruthQubitDerivative` (6) | `import QubitScalarEntropy` | `import TGLExt.EquationOfTruthQubitScalar` | `Mathlib.Analysis.SpecialFunctions.Sqrt` redundante com o pai (que importa `Real.Sqrt`) — remoção **opcional**, a ratificar |
| `EquationOfTruthModularGenerator` (10) | — | — | mantém `TGLExt.ContinuousModularZero` |
| `EquationOfTruthInscription` (2) | `import TheEquationOfTruth_T20` | `import TGLExt.EquationOfTruthCore` | **correção obrigatória (D1)**; mantém `TGLExt.NameIsTheContent` |
| `EquationOfTruthPenaltyThreeLocks` (3) | `import TheEquationOfTruth_T20` | `import TGLExt.EquationOfTruthCore` | **correção obrigatória (D1)**; condicionada à P0 (`penalty` existe no Core?) |
| `EquationOfTruthFiniteGapRate` (8) | `import TheEquationOfTruth_T20_v3` | `import TGLExt.EquationOfTruthCore` | unifica a divergência T20/T20_v3 |
| `EquationOfTruthOperatorContour` (4) | `import InscriptionBridge` | `import TGLExt.EquationOfTruthInscription` | mantém `TGLExt.TheContourOfTruth` |
| `EquationOfTruthNegativeControls` (11) | `import OperatorContourBridge_v2` | `import TGLExt.EquationOfTruthOperatorContour` | mantém `Mathlib...MatrixExponential` |
| `EquationOfTruthNegativeControlsCompleteness` (12) | `import TheEquationOfTruth_T20_controles_v3` | `import TGLExt.EquationOfTruthNegativeControls` | — |
| `TheEquationOfTruth` (índice, NOVO) | — | os 10 módulos positivos | ~15 linhas; sem código |

**Total de edições de código:** 9 linhas de import renomeadas + 1 import monolítico substituído + 1 arquivo-índice novo. **Nenhuma declaração é tocada** — é essa a forma precisa de "preservar os corpos".

---

## 5. Declarações afetadas e controle de duplicação de nomes

**Afetadas:** nenhuma declaração muda de corpo; apenas a *visibilidade por módulo* muda. As declarações-chave a inventariar (grep, V-NAMES) contra o kernel inteiro (1018+ fontes) e entre si: `truthValue`, `truthValue_table`, `penalty` (?), `penalty_eq_kernel_H3L`, `equation_of_truth_is_not_static`, `diagonal_norm_bound`, `radius`, `hasDerivAt_radius`, `spectralLimit`, `diagonalFlow`, `diagonalFlow_eq`, `constant_reader_always_conserved`, `invalidDensity`, e a def/teorema de compatibilidade de `InscriptionBridge` (linhas 12–13 da projeção, conteúdo não integralmente projetado `[LACUNA]`).

**Riscos nomeados:** (i) homônimo entre `spectralLimit` (`InfiniteLimitControl`) e qualquer def no Core — subnamespaces disjuntos tornam colisão improvável, mas o grep decide; (ii) `radius` em `QubitScalar`; (iii) instâncias anônimas — o build do ROOT inteiro é o juiz (lição v324); (iv) `penalty` — ver P0 (§8).

---

## 6. Verificações (elaboração / instâncias / axiomas / memória) — checklist executável da Parte C3

- **V-BODY (preservação):** para cada módulo, a região a partir da primeira declaração é byte a byte idêntica à do V3 congelado; hash da região publicado no manifesto. O bloco de cabeçalho (imports, `set_option`) é a única região mutável, e toda mutação é registrada.
- **V-IMPORTS:** a lista mínima do Core é derivada por redução incremental com rc0 como juiz; nunca por chute. Registro da lista final no manifesto.
- **V-ELAB:** cada módulo compila isolado (rc0); depois o ROOT inteiro (`lake build TGLExt`) — só o ROOT decide a coexistência (instâncias anônimas, colisões).
- **V-NAMES:** grep dos nomes de declaração novos contra o kernel e contra o pacote; zero colisões admitidas. `grep -R "TheEquationOfTruth_T20"` no pacote novo deve retornar zero (o nome legado vive só na pasta de referência).
- **V-AXIOMS:** `#print axioms` de cada declaração pública nova; exigido ⊆ `{propext, Classical.choice, Quot.sound}`; zero `sorry`; zero axioma `TGL.*`. Incluir as linhas no `TGL/Audit.lean` — **regra paga da casa (errata v253→v254): nome reservado sem inscrição no Audit é bandeira cega.**
- **V-HEARTBEATS:** após imports seletivos, tentar reduzir os `maxHeartbeats` (800k/1.2M/1.4M); registrar valores finais. Se `EquationOfTruthFiniteGapRate` (1.4M) falhar, a causa é do teorema, não do pacote — isolar e reportar, não inflar o teto global.
- **V-MEM (memória, o gate honesto):** medir pico por módulo e do ROOT com `time -v` (WSL) ou equivalente; publicar a tabela de picos no manifesto. **Não prometo 8 GiB nem coisa alguma antes desta medição.** O cabimento é conclusão da V-MEM, nunca premissa.
- **V-CONTR:** confirmar que os módulos de controles compilam e que seus teoremas de controle (ex.: `constant_reader_always_conserved`, `invalidDensity`) permanecem fora do índice público (decisão a ratificar, §3).
- **Fora de escopo desta entrega:** a cirurgia no `um.py` (os 5 edits padrão: import/dicionário/esqueleto/artigo/selo) e qualquer selo — etapa posterior, da gerência, com ratificação do operador.

---

## 7. B1d forte geral — permanece hipótese

Nenhum passo deste plano descarrega, renomeia como pago ou cria nome que simule **B1d forte geral**: ele segue `[OPEN — hipótese]`. O manifesto do pacote deve carregar a nota `B1d_STRONG_GENERAL_REMAINS_OPEN_HYPOTHESIS` como texto, não como bandeira. `[LACUNA]: o enunciado exato de B1d não consta das projeções recebidas; a Parte C3 deve lê-lo no ADENDO016002 antes de redigir qualquer nota de escopo — não o parafraseio aqui para não inventar conteúdo.`

---

## 8. Menor lema/artefato faltante (nomeados, em ordem de prioridade)

1. **P0 — a decisão T20 vs T20_v3:** a fonte `TheEquationOfTruth_T20.lean` (sem sufixo) não está nas doze. Menor artefato: **diff entre os dois núcleos** (ou confirmação por grep de que `penalty` e as declarações usadas pelas fontes 2–3 existem no `_v3`). Se existirem: 2 linhas de import corrigidas bastam. Se não existirem: ou a 13ª fonte entra na ficha, ou as pontes 2–3 ficam fora desta integração, declarado.
2. **Manifesto sha256 dos 12 congelados** (~1 arquivo, gerável por script; ancora V-BODY).
3. **O arquivo-índice** `TGLExt/TheEquationOfTruth.lean` (~15 linhas).
4. **A lista mínima de imports do Core** (derivável só por redução incremental; não determinável sem leitura integral `[LACUNA]`).
5. **A tabela de picos de memória da V-MEM** — sem ela, nenhuma frase sobre cabimento é permitida.

---

## 9. Lacunas declaradas

Leitura **não integral** de todas as projeções (linhas omitidas não examinadas); conteúdo de `TheEquationOfTruth_T20` (sem sufixo) desconhecido; corpo completo do `_v3` (749 linhas; ~40 projetadas) desconhecido — a lista de declarações do §5 é parcial; valor do pico de memória medido não projetado; `lakefile` não projetado (pressuponho que submódulos por nome plano funcionam — verificação V0 da Parte C3); ADENDO016002 §2/§3 e o texto de B1d não projetados; o parecer `12e2b4f2` não foi projetado — caracterizei sua cobertura a partir da descrição do operador, não do documento.

## 10. O que esta resposta NÃO é

Não é teorema, não é compilação, não é medição, não é promessa de cabimento em 8 GiB, não escolhe partição física, não constrói Fock, não cria nomes reservados, não move o gate, não paga B1d. Concordância de modelos não foi usada como prova de coisa alguma. É o plano auditável — e só ele — que a Parte C3 executará após A8, com rc0, o trio de axiomas e a V-MEM como juízes.