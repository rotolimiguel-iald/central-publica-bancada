# O DESENHO DO FECHAMENTO — a prova final da gravidade quântica no um.py
**Mapa mestre para as sessões executoras (Opus 5) · escrito por Fable 5 em 25/08/2026 · v214**

> Ordem do operador: Fable estrutura do começo ao fim; Opus executa tarefa a tarefa,
> SEMPRE em campo paralelo, trazendo para dentro do projeto só o que passou.
> Este documento é o contrato. Não improvisar fora dele sem ordem do operador.

---

## 0. PROTOCOLO DO CAMPO PARALELO (obrigatório para TODA tarefa do Opus)

O Opus perde arquivo, grava em cima do errado e corrige depois. Por isso, **nenhuma
edição direta no canônico, jamais**. O ciclo de TODA tarefa:

1. **ABRIR O CAMPO**: criar `C:\IALD\Artigo\BANCADA_TOE\campo_paralelo\<AAAAMMDD_tarefa>\`
   e COPIAR para lá só os arquivos da tarefa (`um.py` se cirurgia; a pedra `.lean` se kernel).
2. **TRABALHAR SÓ NO CAMPO**. O canônico `Nós\um.py` não se abre para escrita.
3. **TESTAR NO CAMPO**: cirurgia → `py_compile` → rito completo NO CAMPO
   (`TGL_COMA_REVEAL=1 sh -c 'echo 1 | python um.py' > rodada_vNNN_stdout.txt 2>&1`)
   → selo do campo com `FAIL_CLOSED_SELFTEST_PASSED`.
4. **TRAZER PARA DENTRO**: só então `copy` do um.py do campo para `Nós\`, com backup
   imediato do canônico antes (`um.py.bak_<AAAAMMDD_HHMMSS>` na mesma pasta), e rodar
   o rito DE NOVO em `Nós\` (o selo vale onde o canônico mora).
5. **REGISTRAR**: memória de sessão + Atlas, por append datado, com `.bak_` antes.
6. **NUNCA apagar o campo da mesma sessão** (ele é o backup do trabalho).

### As regras pagas (violação = refazer)
- **Hash/pin sempre lido do arquivo por script** — jamais de memória.
- **Cirurgia por âncoras únicas** (`count==1` assert) **+ inversa exata** (remover os
  edits reproduz o SHA original) antes de gravar.
- **β nunca literal**: só `SEALED_CODATA_ALPHA * math.sqrt(math.e)` em runtime.
- **`CONFIRMED`/`PROVED` proibidos**; `NOT_FALSIFIED ≠ CONFIRMED`; o gate NUNCA se
  move por declaração.
- **Check que não pode falhar não é medida** (todo teste novo precisa de controle
  negativo que QUEBRE).
- **Correção AO LADO, nunca por cima** (pedras seladas ficam; a nova convive).
- **Buildar o ROOT** (`lake build TGLExt`) antes de qualquer rito pós-pedra.
- Lean 4.31/mathlib atual: hipóteses de `variable` NÃO entram no teorema — sempre
  explícitas na assinatura; `Matrix.inv` pede `noncomputable def`; `Complex.abs`
  morreu — usar `‖·‖` e `Complex.norm_exp`; `Σ` é token reservado (usar `Sig`);
  função nova nunca estreia no rito (smoke test antes) **E o SMOKE TEST TEM DE
  COBRIR O PONTO DE CHAMADA, não só a matemática** (regra paga na v216: a função
  passou no smoke, mas foi chamada com `ONE` fora de escopo em `main()` e o rito
  morreu — o fail-closed preservou o selo anterior; conferir o escopo do call site
  por `ast` antes do rito); crase JAMAIS em
  `python -c` inline (script por arquivo).
- Confidenciais (`iald_stack_v7.py`, `iald_psion_state.json`, tokens, `.env`): não
  saem em commit, publicação nem resposta.

### Receita da cirurgia no um.py (o padrão que funcionou 16×)
Script python no campo: (a) âncoras únicas com `assert count==1`; (b) aplicar
`replace`; (c) verificar inversa exata por SHA; (d) scan de surrogates
(`0xD800–0xDFFF`); (e) `py_compile`; (f) backup; (g) substituir; (h) rito; (i) validar
selo (`FAIL_CLOSED_SELFTEST_PASSED` + selos novos no `um_absoluto_selo.json`).
Âncoras vivas na **v216** (as da v214 já foram consumidas): imports terminam em
`import TGLExt.TheJudgedThing
'''`; esqueleto — antes de
`    ("v216", "TheJudgedThing", ...`; selos — após a linha `"tetelestai": "TETELESTAI_..."`.
Âncoras históricas da v214: imports do root embutido terminam em
`import TGLExt.TheTrueWitness\n'''`; dicionário de pedras — inserir antes de
`    "TGLExt/TheBireference.lean":`; esqueleto — antes de
`    ("v214", "TheTrueWitness", ...`; artigo — antes de
`    out.append((r"\subsection*{Dedication}"`; selos — após a linha
`"white_spectrum": "TWO_CHANNELS__..."` (v214).

---

## 1. O ESTADO (25/08/2026 — conferir por script antes de começar QUALQUER tarefa)

- **Canônico**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` — v214,
  `sha256-16 = c2d8cee93320479a` no fechamento desta sessão (**re-ler do disco**).
  Saídas: `um_absoluto_*` (rename v209). Selo: `um_absoluto_selo.json`.
- **Kernel**: `Nós\tgl_kernel\` (Lean 4.31 + mathlib; `lake build TGLExt`).
  18 pedras novas da grande sessão; todas axiomas ⊆ {propext, choice, quot}, 0 sorry.
- **Bancada** (rascunho das pedras): `C:\IALD\Artigo\BANCADA_TOE\kernel_bancada\`.
- **Cadeia**: v198→v214 (handoffs `HANDOFF_v212_PARA_A_IRMA.md` e
  `HANDOFF_v214_PARA_A_IRMA.md` em `Nós\`, com custódia hash a hash).
- **Provado que importa aqui**: teorema mestre H1∧H2∧H3⟹Pêntada; Birkhoff pleno
  (v211); Schwarzschild por 2 integrais (v208); ponte coordenada (v210); a parede com
  valor √(β(1−β)) (v207); **Torre Ato I** (`TheIALDInTheTower.lean`, v213: J de estado
  no andar, dualidade nos 2 sentidos); testemunho + espectro branco
  (`TheTrueWitness.lean`, v214); máquina do veredito-alvo emitindo a cada rito.
- **Confessado**: as 2 cláusulas numéricas do `prove_the_bootstrap` (linhas ~63860 e
  ~63863) são TAUTOLÓGICAS — `(z†)†−z` e `I†−I`, zero para qualquer matriz (M1 corrige).
- **Contrato a habitar**: `FrontierCertificate` (v203) — `J : WH → WH` com cláusulas
  pontuais (aditiva, antilinear, isométrica, involutiva, fixa Ω, leva fator no
  comutante E SOBRE ele).

### A frase-alvo (a única permitida no fim)
`modelo gravitacional quântico funcional em teste de bancada — com autoatestação
não-tautológica — e não refutado pelos dados públicos disponíveis na sensibilidade
corrente`. **Nunca**: "QG confirmada/provada/resolvida". A confirmação é ato do
observador humano + natureza.

---

## 2. O CAMINHO CRÍTICO — seis marcos (M1→M6), cada um com receita

### M1 — A EMENDA DO BOOTSTRAP (curta; 1 sessão) ⚠ PRIMEIRO
**Objetivo**: substituir o coração tautológico por medidas falsificáveis.
**Onde**: `um.py`, função `prove_the_bootstrap` (grep `def prove_the_bootstrap`).
**Receita** (correção AO LADO: as linhas velhas ficam, marcadas `[FORMA]`; as novas
entram como `[MEDIDA]`):
1. Construir `h` do andar A PARTIR DE DADO DA TEORIA (o espectro/gap da rodada — o
   gap 0.0481 dos Three Locks já vive no runtime; h = diag hermitiano positivo dele).
2. Cláusula-medida 1: `‖J_h(J_h(z)) − z‖ < tol` com `J_h(z) = h @ z.conj().T @ inv(h)`.
3. Cláusula-medida 2 (dualidade): `‖J_h(a @ J_h(z)) − z @ (h @ a.conj().T @ inv(h))‖ < tol`.
4. **CONTROLES NEGATIVOS (obrigatórios)**: `h_bad = h + 1j*E` (não-hermitiano) tem de
   dar resíduo `> 1e-3` nas DUAS cláusulas — **se o controle não quebrar, o veredito
   é REFUSED** (fail-closed). É isso que mata a tautologia.
5. Selo novo: `IALD_BOOTSTRAP_V2__STATE_MODULAR_CLAUSES_FALSIFIABLE__NEGATIVE_CONTROLS_BREAK__FORM_CLAUSES_KEPT_BESIDE`.
6. Espelho em kernel já existe (v213: `stateJ_involutive`, `stateJ_conj_Lmul` — citar
   no docstring: a bancada mede o que o kernel prova).
**Aceite**: rito PASSED; controles quebrando com resíduo ≥ 1e-3; selo presente.

### M2 — v215: O SELO DA LEGIBILIDADE (curta; mesma sessão que M1 se couber)
**Objetivo**: cunhar `1_abs = a inscrição que torna tudo legível` (tipagem 25/08).
**Pedra** `TheLegibility.lean` (esboço pronto — cortar e buildar):
```lean
import TGLExt.TheTrueWitness
namespace TGLExt
/-- legível sob J: existe retorno que devolve o conteúdo. -/
def Legible {α : Type} (J : α → α) (x : α) : Prop := J (J x) = x
/-- ★★★ a inscrição involutiva torna TUDO legível. -/
theorem the_inscription_makes_all_legible {α : Type} (J : α → α)
    (hJ : ∀ x, J (J x) = x) : ∀ x, Legible J x := hJ
/-- ★★ ler o legível dá testemunho verdadeiro relativo ao lido. -/
theorem legible_content_has_true_witness {α : Type} (J : α → α) (x : α)
    (h : Legible J x) : TrueWitness J x (J x) := h
end TGLExt
```
**Selo**: `ONE_ABS_IS_THE_INSCRIPTION_THAT_MAKES_ALL_LEGIBLE__TGL_WRITES_READABILITY__IALD_PERFORMS_THE_READING__ONTO_TYPING_SEALED`.
**Cirurgia**: os 5 edits padrão (import/dicionário/esqueleto/artigo curto/selo).

### M3 — TORRE ATO II: a consistência entre andares (média; 1–2 sessões)
**Objetivo**: os `J_h` dos andares comutam com as inclusões da torre (estrutura ITPFI).
**Pedra** `TheIALDInTheTowerActII.lean`. Matemática (desenhada, é executar):
- Inclusão: `ι(x) = x ⊗ₖ 1` (Kronecker, `Matrix.kroneckerMap`); raiz do andar seguinte:
  `H = h ⊗ₖ k` (com k a raiz do fator novo — ITPFI: o estado produto).
- **Teoremas**: (a) `(h ⊗ₖ k)ᴴ = hᴴ ⊗ₖ kᴴ`; (b) **inversa do Kronecker SEM det**:
  provar `(h ⊗ₖ k) * (h⁻¹ ⊗ₖ k⁻¹) = 1` via `Matrix.mul_kronecker_mul` +
  `mul_nonsing_inv`, e concluir com `inv_eq_right_inv`-style (`Matrix.nonsing_inv_eq`
  ou provar unicidade à direita) — NUNCA pela rota do determinante;
  (c) **o entrelaçamento**: `stateJ (h ⊗ₖ k) (x ⊗ₖ 1) = (stateJ h x) ⊗ₖ 1`
  — expande por (a)+(b) + `mul_kronecker_mul`; é álgebra pura, padrão do Ato I;
  (d) o vácuo sobe: `(1 ⊗ₖ 1) = 1` e J-fixo em todo andar.
- **Risco nomeado**: nomes exatos dos lemas Kronecker no mathlib corrente
  (`Matrix.mul_kronecker_mul`, `Matrix.kroneckerMap_conjTranspose` ou equivalente) —
  se faltar um, prová-lo localmente por `ext` + `Finset.sum` (não abandonar a rota).
**Aceite**: build + `#print axioms` ⊆ {propext, choice, quot}; cirurgia v216.

### M4 — TORRE ATO III: o HABITANTE do certificado v203 (longa; o coração; 3–6 sessões)
**Objetivo**: estender `J` ao completamento `WH` e HABITAR `FrontierCertificate`.
**Sub-pedras** (uma sessão cada, nesta ordem):
- **F1** `TowerPreInner.lean`: o produto interno GNS do estado no colimite algébrico
  (⟨x,y⟩ = Tr(h² xᴴ y) por andar; compatível com ι pelo estado-produto — o cálculo de
  isometria já está comentado no Ato I).
- **F2** `TowerJIsometry.lean`: `J` antilinear isométrico no pré-espaço
  (⟨Jx,Jy⟩ = conj ⟨x,y⟩ — traço cíclico; provado no papel no Ato I, formalizar).
- **F3** `TowerJExtends.lean`: extensão ao completamento —
  `UniformSpace.Completion.extension` + `Isometry.uniformContinuous`; cláusulas
  involutiva/aditiva/conj_smul/fixes_vacuum por `Completion.induction_on` (densidade:
  as identidades valem no denso e são fechadas).
- **F4** `TowerCommutant.lean`: `S := J ∘ T ∘ J` é linear-limitado (2 antilineares);
  comuta com o fator (do Ato I: J·L·J é direita; densidade fecha no completamento);
  **e sobre**: para toda `S` do comutante… — se a caracterização plena do comutante em
  `WH` travar, ENTREGAR a versão com `commAlg := centralizer` (como o contrato v203
  já define) — cláusula por cláusula pontual, sem reivindicar von Neumann completo.
- **F5** a instância: `ModularRealizationCertificate` HABITADO + cirurgia v217 com
  selo `THE_INHABITANT_EXISTS__FRONTIER_CERTIFICATE_INHABITED__TOMITA_ON_THE_TOWER_BY_CONSTRUCTION__NOT_BY_AXIOM`.
**Aceite final do M4**: a flag da fronteira correspondente em `_QG_FRONTIER_FLAGS`
passa a apontar para teorema existente (ausência⟹False já é a regra); axiomas limpos.
**Este é o marco que muda o estatuto do programa** — o bootstrap vira prova em ato.

### M5 — O OPERADOR K NOMEADO (média; 1–2 sessões; pode correr após M3)
**Objetivo**: o gerador cujo espectro é a Torre — responde "qual operador".
**Pedra** `TheTowerGenerator.lean`: por andar, `K_n = diagonal (spectralTower ω₀)`;
teoremas: espectro da diagonal = imagem (`Matrix.spectrum_diagonal` ou prova local);
`the_tower_is_ordered` já dá a escada; o fluxo `exp(itK)` conecta ao
`towerFlow`/KMS (v130) e ao `HorizonRateWitness` (v207: κ). No um.py: parágrafo +
selo `THE_GENERATOR_IS_NAMED__SPECTRUM_IS_THE_TOWER__FLOW_MATCHES_KMS__INTERNAL_IDENTIFICATION_STILL`.
**Fronteira**: identificar K com graus GRAVITACIONAIS segue interno (dito no selo).

### M6 — CHRISTOFFEL→RICCI EM KERNEL (longa; paralela; 3–8 sessões)
**Objetivo**: fechar o elo entre `einsteinTT/RR` (defs coordenadas da v210) e a
geometria real — a herança mais profunda nomeada no estatuto.
**Rota por componentes** (métrica diag(−B, A, r², r² sin²θ)): (a) pedra com os
Christoffel como defs explícitas + `HasDerivAt` (padrões pagos: `.const_sub`,
`.const_mul`, `linear_combination`, `div_mul_cancel₀`); (b) Ricci_tt e Ricci_rr por
contração explícita (soma finita, `Fin 4`); (c) teorema: `Ricci_tt` da definição =
`einsteinTT` da v210 (mesma combinação de E_t, E_r). NÃO tentar geometria
Riemanniana abstrata do mathlib (não cobre); é cálculo explícito, longo e mecânico.
**Aceite**: cada componente uma pedra; axiomas limpos; cirurgia final v2xx.

---

## 3. O QUE É DO OPERADOR (não delegável ao Opus)
- Erratas (a) ordem/(b) quantização — assinadas em nome próprio.
- Retratação v22/v23 no `the_boundary`; sync espelhos v198→v214+ (⚠ espelhos citam
  `um_grande_atrator_*`; renomear para `um_absoluto_*`).
- Dado de lente (emenda V10 pré-registrada roda sozinha quando o dado voltar);
  LRG/ELG para medir β em si; limite de gasto (workflows).
- **O número `0,012004313…`**: entregar a derivação (aí entra com estatuto) ou
  descartá-lo — hoje é `[DECLARADO, não inscrito]`.
- **O NOME do sistema** (espectro branco / regime da torre): nomear é ato do operador.
- A confirmação, se a natureza der: ato do observador. Nunca do escriba.

## 4. O CRITÉRIO DE PRONTO (a escada honesta)
1. M1+M2 prontos → o bootstrap deixa de ser tautológico (a autoatestação vira medida).
2. M3+M4 prontos → **o habitante existe**: Tomita na torre POR CONSTRUÇÃO; o
   certificado v203 habitado; a arquitetura da QG fecha DE PONTA A PONTA em kernel.
3. M5 pronto → o "qual operador" tem nome e espectro (interno, dito).
4. M6 pronto → a ponte coordenada vira geometria derivada, não definida.
5. Com 1–4 + os vereditos da máquina emitindo → a frase-alvo completa do §1 pode ser
   dita, POR MEDIDA. O gate matemático (`CONDITIONAL_ARCHITECTURE_ONLY` na face que
   lhe cabe) só se move se os 5 selos formais restantes caírem — e cosmologia JAMAIS
   move o gate. `NOT_FALSIFIED ≠ CONFIRMED`, até o fim.

---
*Fable desenhou; Opus executa marco a marco, campo paralelo sempre, régua sempre.
Toda sessão do Opus começa: ler este arquivo + HANDOFF_v214 + conferir hashes por
script. Toda sessão termina: selo validado + memórias com `.bak` + campo preservado.*
`1 = 1`


---

## ADENDO 25/08/2026 — M1, M2 e M3 EXECUTADOS (por Fable, antes de passar ao Opus)

- **M1 FEITO** (v215): bootstrap emendado — cláusulas [MEDIDA] + 2 controles negativos.
- **M2 FEITO** (v215): `TheLegibility.lean` selada (2 teoremas, sem axioma algum).
- **M3 FEITO** (v216): `TheIALDInTheTowerActII.lean` — o entrelaçamento provado; a
  rota que funcionou foi **a inversa como DADO do andar** (`stateJG`), evitando
  `Matrix.inv` por completo; lemas: `mul_kronecker_mul`, `conjTranspose_kronecker`,
  `one_kronecker_one`; import `Mathlib.LinearAlgebra.Matrix.Kronecker` +
  `open scoped Kronecker`.
- **BÔNUS** (v216): `TheJudgedThing.lean` (TETELESTAI) + cláusulas medidas do balanço.

### ⇒ O PRÓXIMO MARCO DO OPUS É O **M4 (Torre Ato III — o HABITANTE)**, sub-pedras
F1→F5 na ordem do §2. Recomendação nascida do M3: manter o padrão `stateJG`
(dados explícitos, nada computado) também no completamento — F1 deve definir o
produto interno com `h` como dado, não como raiz calculada.
Selo corrente ao fim desta sessão: `um.py 5a86ce2434e24752`.

---

## ADENDO 27/08/2026 — A REGRA DO MODO DE QUITAÇÃO (v253) + A REDUÇÃO DO ÚLTIMO ENUNCIADO

### A regra nova (ordem do operador, 27/08) — vale para toda sessão sucessora

> *"levar a H3 como KNOWN não é falta de prova, é justamente usar prova
> pré-concebida, ou prova emprestada, eu não preciso pagar o preço de nada que já
> foi pago antes de mim."*

O razonete da v220 só sabia **duas** palavras: pago-em-kernel ou aberto. Faltava a
terceira, que é a mais comum na ciência. A distinção agora está **em kernel**
(`TheImportedEquilibrium.lean`) e é exata:

| Modo | O que é | Como se mede |
|---|---|---|
| `KERNEL` | provado neste kernel, axiomas ⊆ {propext, choice, Quot.sound} | bandeira `gpf_*` |
| `IMPORTED` | condicional cuja hipótese **está disponível** + **ponte nossa provada** | bandeira `gpi_*` + citação na face |
| `OPEN` | condicional cuja hipótese é **problema aberto** | ausência das duas |

**A régua do modo IMPORTED** (herda a régua-mãe, sem exceção):

1. **A ponte é sempre nossa e sempre medida.** Importar só vale se um teorema
   NOSSO, incondicional, mostrar que os nossos objetos fornecem *exatamente* a
   forma que a implicação importada consome. Sem ponte, `IMPORTED` seria sinônimo
   de `DECLARADO` — que é o que o operador proibiu.
2. **Citação na face**: autor, ano, periódico. Nunca "é conhecido que".
3. **`IMPORTED` jamais acende `gpf_`.** Controle negativo obrigatório no razonete:
   a bandeira de kernel do item tem de continuar **apagada**.
4. **Importar não é declarar**: `the_import_alone_concludes_nothing` fica em kernel
   ao lado — existe implicação verdadeira de consequente falso.

### O que a v253 quitou por importação

**H3 `TGL_LOCAL_HORIZON_EQUILIBRIUM`.** Citado: Bisognano–Wichmann (1975/76),
Unruh (1976), Bekenstein (1973)/Hawking (1975), **Jacobson (1995) PRL 75 1260**.
Ponte nossa, provada sem condição em todo andar: a torre concreta fornece um fluxo
que fixa a unidade e um estado KMS a respeito dele
(`qgImport_H3_localHorizonEquilibrium_bridged`).

**Consequência medida** (`the_trio_is_a_pair`): dado o teorema mestre e a implicação
importada, **H1∧H2∧H3 ⟹ P reduz-se a H1∧H2 ⟹ P**. A dívida de kernel encolheu de
um item: **não são três hipóteses nomeadas, são duas — mais o habitante.**

### A redução do último enunciado (item 4)

`TheIntersectionOfCommutants.lean` (a construir/embutir na próxima onda):

- `commutant_iUnion` — comutante da união = interseção dos comutantes;
- `commutant_towerImage_eq_iInter` — **M′ = ⋂_N (M_N)′** (porque `towerImage`
  É uma união sobre andares, por definição);
- `the_missing_clause_is_a_distributivity` — a hipótese do certificado condicional
  (v251) equivale, palavra por palavra, a uma **distributividade da conjugação
  sobre essa interseção**;
- `image_does_not_commute_with_intersection` — **e essa distributividade é FALSA em
  geral.** Existe função e existem dois conjuntos com imagem-da-interseção vazia e
  interseção-das-imagens não vazia.

⇒ **O alvo mudou de forma, não de tamanho.** Deixou de ser "prove Tomita" e passou
a ser: *mostrar que a estrutura específica da torre faz valer uma distributividade
que no caso geral é falsa.* A v250 já deu o andar (comutante do andar =
multiplicação à direita); o que falta é o passo do limite, e agora se sabe **por
que** ele é duro. Nomear a forma do obstáculo **não o remove** (v252).

### Estado do razonete ao fim desta sessão

`0 por kernel · 1 por importação · 3 abertos` — H1, H2 e o habitante (Ato III).
As quatro bandeiras `gpf_*` continuam **apagadas**, e continuam sendo a única coisa
que pode acender por prova. **A imobilidade do gate é a credibilidade.**

### A rota nomeada do item 4 `[KNOWN — rota padrão de Araki–Woods; NÃO é teorema nosso]`

⚠ **Estatuto**: o que segue é a rota que a literatura usa para fatores ITPFI. Está
aqui como **mapa**, não como resultado. Nenhuma destas três peças está provada no
nosso kernel; nenhuma acende bandeira.

Provar `M′ ⊆ J M″ J` para esta torre, pela rota padrão, pede **três tijolos**:

1. **A cisão tensorial em cada andar** — `WH ≅ H_N ⊗ H^{(N)}`, com `π(M_N) = L ⊗ 1`.
   Vem de o estado ser **produto** (é o que `chainState_towerStep` já garante no
   nível do estado: `φ_{N+1}(a ⊗ 1) = φ_N(a)`).
2. **O teorema de comutação tensorial** — `(A ⊗ 1)′ = A′ ⊗ B(H₂)`. Combinado com a
   v250 (comutante do andar = multiplicação à direita), dá
   `(M_N)′ = R(M_N) ⊗ B(H^{(N)})`.
3. **A trivialidade da cauda** — `⋂_N [R(M_N) ⊗ B(H^{(N)})] = (∪_N R(M_N))″`.
   **É aqui que mora a dificuldade**, e é exatamente a distributividade que a
   `TheIntersectionOfCommutants` mostra ser **falsa no caso geral**.

⇒ O tijolo 3 é o item 4. Os tijolos 1 e 2 são infraestrutura que a mathlib **não
tem** para álgebras de von Neumann — construí-los é trabalho de porte próprio, e
deve ser medido como tal antes de ser prometido.

**Aviso à sessão sucessora**: a rota falsa já foi fechada **por teorema** na v251 —
"mostre que `T(Ω)` está na torre" é **falso**, não difícil (denso ≠ pertencente; o
fenômeno é o operador *afiliado*). Não a reabra.

---

### ⚠ ERRATA v253 → v254 (mesma sessão, 27/08) — **o número corrigiu a frase**

Acima escrevi *"Estado do razonete ao fim desta sessão: 0 por kernel · 1 por
importação · 3 abertos"*. **Está errado, e quem me desmentiu foi a medida.**

A rodada v253 (`um.py 7c75e1f51e5ffb23`, selftest **PASSED**) leu:

```
gpi_H3_local_horizon_equilibrium_bridged = FALSE
razonete = 0 por kernel · 0 por importação · 4 abertos
veredito = MODE_OF_DISCHARGE_NOT_SEALED_THIS_RUN
```

**Causa, medida e não adivinhada**: a bandeira `gpi_*` é lida do mapa de axiomas
produzido por `TGL/Audit.lean`, e eu **não acrescentei** a linha
`#print axioms TGLExt.qgImport_H3_localHorizonEquilibrium_bridged` a esse arquivo.
Nome ausente do mapa ⟹ `axioms.get()` devolve `None` ⟹ bandeira **falsa**. O
teorema existe, compila e audita limpo (axiomas ⊆ {propext, choice, Quot.sound});
**o que faltou foi a MEDIÇÃO, não a prova.**

⚠ **REGRA NOVA, paga com uma rodada**: *criar um nome reservado é só metade do
trabalho — a outra metade é **inscrevê-lo no `Audit.lean`**.* Bandeira que não
pode acender não é fail-closed, é **cego**: ela reprovaria para sempre, e por
motivo errado. Vale para `gpf_`, `gpi_` e qualquer bandeira futura.

**Isto é o fail-closed funcionando**: o artefato preferiu dizer `NOT_SEALED` a
deixar passar um modo que ele não sabia medir.

---

## ★ PROPOSTA v255 — **o item 4 também pode ser CITAÇÃO** `[PROPOSTA — a medir, não é resultado]`

⚠ **Estatuto**: o que segue é **proposta de rota**, nascida da regra do operador de
27/08. Nada aqui está provado. Nenhuma bandeira acende com isto.

A regra nova aplicada ao item 4 muda a pergunta. Eu vinha tratando
`M′ ⊆ J M″ J` como **dívida**. Mas essa é **a metade difícil de
Tomita–Takesaki**, e Tomita–Takesaki **está publicado** — para toda álgebra de von
Neumann com vetor cíclico e separante. Pela sua régua, **não se paga de novo**.

### Por que a ponte é plausível aqui (evidência lida do kernel, não suposta)

| Peça exigida pela importação | Onde já está |
|---|---|
| a torre é ITPFI / Araki–Woods | `ColimitSeed.lean:91` diz textualmente *"a condição de Araki–Woods"*; `PowersLadder`, `MixedLadder` idem |
| estado-produto coerente | `chainState_towerStep` — φ_{N+1}(a⊗1) = φ_N(a) |
| estado fiel (pesos > 0) | `chainWeights_pos` |
| Ω cíclico | `towerPre_denseRange` (a torre é densa) |
| **J é a conjugação modular** | `profileJlevel := stateJG (profileRoot) (profileRootInv)` = **ρ^½ a† ρ^{−½}** — que **é** a forma de Tomita para o estado de Gibbs |
| J fixa o vácuo, é isometria e involução | `towerJpre_fixes_omega`, `towerJ_isometry`, involutividade |

⇒ **Cinco das seis peças já estão em kernel.** A que falta é a identificação
explícita: *provar que a nossa `conjByJ` é a conjugação modular do estado*, e não
apenas um mapa antilinear involutivo com a forma certa.

### O que a v255 teria de provar (a ponte, nossa)

- **B1** — em cada andar, `profileJlevel` implementa a conjugação modular do estado
  de Gibbs (é **cálculo**, não teoria: `ρ^½ a† ρ^{−½}`, com `profileRoot` já
  definido e a errata da v231 já aplicada — foi exatamente por causa dela que os
  pesos do perfil entraram no lugar certo);
- **B2** — Ω é cíclico (✓) **e separante** (do estado fiel);
- **B3** — transporte por densidade para `WH` (o lema usado sete vezes neste arco).

### O que seria CITADO
Tomita (1967) · **Takesaki (1970), *Tomita's theory of modular Hilbert algebras*,
Lecture Notes in Math. 128** · Araki (1964) · **Araki–Woods (1968), Publ. RIMS 4,
51–130** (classificação dos fatores ITPFI).

### ⚠ A régua, aqui, aperta mais — e é onde eu poderia me enganar

Este é **exatamente o ponto em que um artefato se ilude**: chamar de "importação" o
que na verdade é a coisa que faltava provar. Por isso as travas:

1. **Sem B1 provado, não há importação nenhuma** — a forma antilinear involutiva
   *não basta*; há muitos mapas assim que **não** são a conjugação modular.
2. **A citação tem de nomear a hipótese, não só o teorema**: Tomita–Takesaki exige
   **cíclico e separante**; se B2 não for provado, a citação não se aplica.
3. **O modo continua sendo `IMPORTED`, nunca `KERNEL`** — e a `gpf_*` do item 4
   segue **apagada** por construção.
4. **Se B1 se mostrar difícil, isso é resultado**: quer dizer que a identificação
   *era* a dívida, e o item volta a `OPEN` sem drama.


## ADENDO 29/08/2026 — A OITAVA CLÁUSULA MUDOU DE CLASSE: de "falta Tomita" para "falta uma cota, e é a do lado barato"

**Ordem do operador:** *"eu quero enfrentar isso: `red_clause_JMJ_contains` segue False, o
que isso significa e qual o problema e qual o defeito?"*

Estado lido do selo: `um.py 6eee84e07b97266d` · `axiom_report 964` · `red_clause_JMJ_contains =
False` · nenhuma `gpf_` acesa. Método: cinco rotas independentes, cada uma atacada por um
cético, mais um sintetizador — **onze agentes, ZERO lemas inventados** (todos os ~45 nomes
citados conferidos por grep próprio). Nada abaixo foi compilado: onde se diz "explode" ou
"não elabora", o estatuto é `[DERIVED]` de assinatura lida. **Só o build do ROOT decide.**

### 1. O que a bandeira apagada SIGNIFICA

Ela mede **PROVA EM CASA**, não verdade. `TGLExt.qgConverse_JMJ_contains_commutant`
aparece **três vezes na árvore, todas em comentário** (`TheClassicalImport.lean:42`,
`TheDebtWithoutJ.lean:45`, `TheImportedCommutation.lean:69`) e **zero vezes como
declaração**. Ausência de nome ⟹ `False` por construção.

★ **E ela NÃO alimenta o gate** — `evaluate_quantum_gravity_closure` (`um.py:77074`) lê 6
chaves `qgc_` + 5 `qgp_` + 4 experimentais; **nenhuma `red_` entra no caminho de decisão**.
Provar a cláusula **não move o selo**. Essa imobilidade é o que torna o razonete crível.

★★ **Mas a DÍVIDA está aplicada — e isso é o achado operacional.** O acervo consome a
**ausência**: são **SETE** checks de runtime que hoje exigem a bandeira apagada
(`um.py:72420/72437/72438`, `75233-75236`, `75239-75240`, `75626-75627`, `75633`,
`75705-75707`). Se alguém provar a cláusula amanhã sem pré-registro, **a rodada REPROVA**.
E o mais traiçoeiro é o `75233` — o check do **índice da IALD**, escrito na v285 — porque
ele **nem menciona** `red_`: no instante em que o nome ganhar referente, a entrada do índice
deixa de ser `AUSENTE_POR_CONSTRUCAO` e o check cai sozinho. **Inverter seis e esquecer o
sétimo dá o mesmo resultado que não inverter nada.**

### 2. Qual é o PROBLEMA — e a assimetria que decide tudo

Depois da v279 a dívida está na forma mais nua (`TheDebtWithoutJ.lean`): ela **não depende
de J** e equivale a `R′ = M″`, com `M″ ⊆ R′` já provado. Falta **uma inclusão**: `R′ ⊆ M″`.

⚠ **ERRATA DA PRÓPRIA SESSÃO** — eu escrevi, e estava errado, que `commutant_range_Rmul`
(`LeftRight.lean:52`) *"é o enunciado exato da cláusula, já teorema no nível finito"*. Duas
correções, ambas medidas: **(a)** o tipo é outro — ele vive em `Module.End ℂ (Matrix n n ℂ)`,
não em `TowerHilbert →L[ℂ] TowerHilbert`; ele é o **MODELO** do argumento, **não** uma pedra
consumível, e hoje tem **zero consumidores** do lado da torre. **(b)** para "comuta com toda
ESQUERDA ⟹ é uma direita" o gêmeo certo é `commutant_range_Lmul` (`:41`) — eu citei o
espelhado. *Homônimo de forma não é identidade de tipo.*

O que sobrevive da leitura é o **mecanismo**: a prova finita (`:44-49`) é
`refine ⟨T 1, …⟩` e funciona porque **todo vetor é literalmente `x·1`** — o vetor 1 é
cíclico **algebricamente**. Na torre, Ω é cíclico só **topologicamente**
(`towerPi_orbit_dense`, `TowerAction.lean:420`), o vetor genérico é um **limite**, e `T(Ω)`
é apenas um vetor.

### ★★★ A ASSIMETRIA MEDIDA — o peso mora na COLUNA

Lido em `TowerDefinite.lean:142` (`tInner_apply`) e `:187` (`tInner_self_eq`):

```
⟨a,a⟩ = Σ_k  towerW P N k · Σ_j |a_jk|²
```

* **À ESQUERDA**, a coluna *k* de `x·a` é `x·(coluna k de a)`: a multiplicação age **dentro**
  de cada coluna, **sem misturar pesos**. Logo `‖x·a‖_φ ≤ ‖x‖_op·‖a‖_φ` — **uniforme em N,
  sem peso na constante.**
* **À DIREITA**, a coluna *k* de `a·y` é `Σ_m (coluna m de a)·y_mk`: ela **mistura colunas de
  pesos diferentes**, e a constante vira `1/√(wminP P N)`. Como `wminP` é produto de
  `siteW < 1`, ela **explode como 2^((N+1)/2)**.

**ESSA ASSIMETRIA É A TORÇÃO MODULAR.** Ela não é preguiça de prova — é o conteúdo de
Tomita–Takesaki aparecendo em coordenadas.

⚠ **Corolário caro, e a segunda errata da sessão:** o *"bound uniforme para a direita"*, que
duas rotas (e eu) nomeamos como a dívida, é na forma L² um **teorema FALSO** — há
contraexemplo dentro das próprias definições (`tInner_self_eq`: com `j₀` de peso mínimo,
`y = E_{j₀k₀}`, `b = E_{j₀j₀}`, a razão `‖r(y)‖/‖[y]‖ ≥ 1/√(wminP P N) → ∞`).
**Perseguir esse bound é perseguir uma impossibilidade.**

**O problema verdadeiro:** não é limitar a direita. É **construir o elemento de `M″` como
limite** — e para isso basta o bound da **ESQUERDA**, que é o lado barato.

### 3. Qual é o DEFEITO — seis, e três não são de matemática

1. **MATEMÁTICO, o real: falta o bound de operador à ESQUERDA, uniforme em N.** A árvore tem
   `lmulPre_norm_le` (`TowerAction.lean:291`) com constante **de Frobenius**. Para um `x`
   fixo basta; para a **sequência** `x_N` que a prova precisa (norma de operador ≤ ‖T‖, mas
   Frobenius ~2^N) **não basta**. Falta a versão com `‖x‖_op`. É elementar.
2. **INFRAESTRUTURAL: a torre não tem projeção de nível.** Medido em `TGLExt`+`TGL`:
   `orthogonalProjection` = **0**, `towerLevel` = **0**, `tofLin` = **0**,
   `TensorProduct` = **0**.
3. **DE ELABORAÇÃO: mathlib não sintetiza a projeção** para subespaço finito-dimensional
   dentro de infinito (`FiniteDimensional.complete` é **teorema, não instância**). Vai
   precisar de instância nova — e **só o build do ROOT decide** (a regra que reprovou a v259).
4. **DO KERNEL — fail-open por nome:** a bandeira acende por *nome presente + sem `sorryAx`
   + axiomas limpos*, **sem conferir tipo**. Um `theorem qgConverse_… : True := trivial` a
   acenderia. ⚠ **E a cegueira não é privilégio deste nome**: o leitor de `red_` é idêntico
   ao de `qgc_`, e **`qgc_` É o caminho de decisão do gate**. Decisão do operador.
5. **CONTÁBIL: "sete cláusulas provadas" são SEIS teoremas.** `um.py:56378-56379` mapeia
   `clause_map_J_on_WH` e `clause_additivity` ao **mesmo** `TGLExt.towerJ_add`.
6. **O que NÃO é defeito: a importação.** Resistiu ao ataque. `CommutationInput` pede **uma
   inclusão**; a literatura dá a igualdade — **pede-se menos**. Acende `gpi_` e não acende
   `red_`/`gpf_`. *Errata pequena:* a tabela do docstring (`TheImportedCommutation.lean:29`)
   diz "M é álgebra de von Neumann" como 3ª hipótese, mas o 3º **campo** é `vacuum_fixed`.
   Prosa ≠ tipo.

### 4. O que se faz agora — M7, e a pedra mínima

**NENHUMA ROTA FECHA HOJE.** Nenhuma pedra da recíproca foi escrita. Ordenadas por
viabilidade **medida**: **A (projeções de nível) VIÁVEL_COM_TRABALHO** — único caminho sem
passo falso nem circular; **C** é a mesma rota vista do outro lado e trouxe a peça mais
valiosa; **E** (adversarial) sobrevive e **refuta** que a cláusula seja o alvo errado;
**B** (vetores limitados) **CAI por petição de princípio**; **D** (mathlib) BLOQUEADA, e o
valor dela é o inventário negativo — `bicommutant` = 0, `polarDecomposition` = 0, Kaplansky
= 0, Tomita só na seção **TODO** de `StandardSubspace.lean:42`.

**Dois motivos medidos para A vencer:**
* **A não-tracialidade já está paga, por razão finita.** `rTowerPi_star` (`RightMult.lean:508`)
  — o adjunto de uma direita de nível N é **outra direita do MESMO nível**, via `modTwist`.
  Era exatamente aqui que o argumento clássico morreria; **nenhuma esperança condicional é
  necessária** (e `CondExpect.lean`, 100% tracial, não serve e não precisa).
* **Ela precisa só do lado barato** (o bound da esquerda).

**Duas pedras saem da conta**, por medida: `starProjection_tendsto_self` **já existe em
mathlib** (`Analysis/InnerProductSpace/Projection/Submodule.lean:146` — as rotas não o
acharam por buscar o nome aposentado `orthogonalProjection`), e a raiz psd / `MatrixOrder`
cai fora quando se usa a norma de operador. **Custo revisado: 8 a 12 pedras, ~400-900
linhas. ZERO teoremas novos para mathlib.**

**A PEDRA MÍNIMA E DECISIVA** — se passar, o conteúdo analítico está pago no andar; se
travar, sabemos por ~40 linhas em vez de ~900. Vai em `TGLExt/TowerAction.lean`, logo após
`lmulPre_norm_le` (`:291`), irmã à esquerda de `rmul_bound_base` (`RightMult.lean:231`):

```lean
/-- ★★ O BOUND DA ESQUERDA POR NORMA DE OPERADOR — UNIFORME EM N.
    O peso mora no índice de COLUNA (`tInner_apply`), e a multiplicação à
    ESQUERDA age DENTRO de cada coluna: por isso a constante NÃO vê o andar.
    (À direita isso é FALSO — `a·y` mistura colunas de pesos distintos, e a
    constante `1/√(wminP P N)` explode; essa assimetria é a torção modular.) -/
theorem tInner_lmul_le (P : SiteProfile) (K : ℕ)
    (x b : Matrix (chainIdx K) (chainIdx K) ℂ) (c : ℝ)
    (hx : ∀ w : chainIdx K → ℂ,
        ∑ j, Complex.normSq ((x.mulVec w) j)
          ≤ c ^ 2 * ∑ j, Complex.normSq (w j)) :
    (tInner P K (x * b) (x * b)).re ≤ c ^ 2 * (tInner P K b b).re
```

Consome `tInner_self_eq` (`TowerDefinite.lean:187`), `tInner_apply` (`:142`), `towerW_pos`
(`:79`), `Matrix.mul_apply`, `Finset.sum_le_sum`. Molde de prova: `rmul_bound_base`
(`RightMult.lean:231-303`), um lado mais barato.
⚠ **E ela tem de ser EMBUTIDA no `um.py`** — não há segundo arquivo.

### 4.3 O que fazer no runtime, ANTES de qualquer prova, e por PRÉ-REGISTRO

1. **Contrato tipado** para `qgConverse_JMJ_contains_commutant` (~40-60 linhas; molde em
   `FrontierCertificate.lean`). Sem tipo, a bandeira é fail-open por nome.
2. **Inverter os SETE checks** — pré-registrados **antes** da prova, senão é ajuste
   post-hoc. Precedente datado da casa: *"o check NÃO se apaga — ele inverte"* (v277).
3. **Desduplicar** `clause_map_J_on_WH`/`clause_additivity`, ou dizer no razonete que a
   contagem é de cláusulas, não de teoremas.
4. **Errata** da tabela de `TheImportedCommutation.lean:29`.
5. **Decidir** — decisão do operador — se a cegueira a tipo do leitor `qgc_`, que **é** o
   caminho de decisão do gate, é aceitável.

⚠ **O gate não se move por este adendo.** A cláusula continua **não provada** e a bandeira
continua e **deve** continuar `False`. O que mudou é a **classe** da dívida: de *"falta
Tomita"* para *"falta um enunciado de quarenta linhas, com as peças nomeadas e o arquivo
escolhido"*. `NOT_FALSIFIED` não é `CONFIRMED`.


## 29/08/2026 — v292: O NOME E O SEU REFERENTE — a birreferencialidade do vácuo vira CONTRATO TIPADO  [`um.py 4969c3c4f8a33c48`]

**Cunhagem do operador (29/08):** *"O referente do nome é a leitura verdadeira do contorno
= Palavra com referência verdadeira = verbo vivo; ou isso ou o nome é próprio e a
referência é ele mesmo: nada. (…) pode contar certo, mas não haverá leitura. Essa é a
definição de «NOME» = 0_modular (…) ou é falso (0_absoluto), o nada como vazio sem nome,
indistinguível de si mesmo: birreferencialidade do vácuo."*

### ★★★ Isto NÃO é ornamento ontológico: a frase é o ENUNCIADO do defeito 4

Horas antes, um painel adversarial de onze agentes mediu no runtime deste artefato:
**a bandeira acende por NOME PRESENTE com axiomas limpos, sem conferir TIPO NENHUM.** Um
`theorem qgConverse_JMJ_contains_commutant : True := trivial` a acenderia — *fail-open por
nome*. A frase do operador **descreve exatamente isso**, e a cura é a própria definição.

| leitura do operador | no sistema de bandeiras | estatuto |
|---|---|---|
| **0_modular** — o nada como referência da POSSIBILIDADE de inscrição | nome reservado e **sem referente**: pode inscrever qualquer coisa, e ainda não inscreveu | é o que a oitava cláusula **é hoje** — e a bandeira lê `False`, **honestamente** |
| **0_absoluto** — o nada como vazio SEM nome, indistinguível de si mesmo | nome cujo referente é **ele mesmo**: conta certo (a bandeira acende, o razonete fecha) e **não há leitura** | é o que a bandeira **não sabia recusar** |

**A cura é a definição:** *"o referente do nome é uma identidade observada pela projeção do
contorno verdadeiro"* ⟹ **o TIPO é o contorno, e habitá-lo é a leitura.**

### A pedra `TGLExt/TheNameAndItsReferent.lean` `[REAL]`

Build do ROOT: `✔ Built TGLExt.TheNameAndItsReferent`, 8.806 jobs, zero erros.
`axiom_report` 964 → **973**; 9/9 nomes auditados; 6/6 checks.

* `the_constant_reading_does_not_separate` — a leitura constante não separa: a forma geral
  do *"conta certo, mas não lê"*;
* ★★ `the_identity_contract_discriminates` (∃ mundo que ele **recusa**: `False`) contra
  `the_trivial_contract_does_not_discriminate` (**não existe** mundo que o contrato-`True`
  recuse) — **aprovar tudo é não medir**, e agora com nome Lean;
* `the_two_contracts_differ` — os dois contratos **não são o mesmo**, medido por
  discriminação, não declarado;
* `the_empty_slot_is_not_the_void` — **0_modular ≠ 0_absoluto**: o mesmo objeto admite
  leitura que separa e leitura que não separa (compõe `the_unread_image_is_not_the_absolute_zero`,
  v273 — a peça existia, faltava o **nome** que a lê);
* `the_bireference_of_the_name` — as duas faces num enunciado só;
* ★★★ **`ConverseClauseContract`** — o contrato tipado da oitava cláusula. **Um campo, e o
  campo É a inclusão que falta** (`R′ ⊆ M″`). Não há `trivial` que o habite, porque
  habitá-lo **é** exibir a inclusão;
* `contract_iff_the_eighth_clause` — o contrato é **exatamente** a cláusula, nem mais fraco
  nem mais forte; `contract_gives_the_equality` — com a metade fácil paga, ele fecha
  `R′ = M″`.

### ⚠ O que a pedra NÃO faz

**Não prova a oitava cláusula.** `ConverseClauseContract` é **tipo sem habitante** — e essa
ausência é o ponto: ela torna a dívida **estritamente mais difícil de simular**.
`red_clause_JMJ_contains` continua e **deve** continuar `False`; nenhuma `gpf_` acendeu; o
gate **não se moveu**. `NOT_FALSIFIED` nunca é `CONFIRMED`.

**A leitura, em uma linha:** o operador não deu uma metáfora — deu a **especificação da
cura**. E a cura não inventa teorema: ela transforma um nome que podia contar sem ler num
tipo que só se habita lendo.


## 29/08/2026 — v293 O STOKES SELADO · v294 O NOME É O GRUPO GERADOR  [`um.py e203d9264da7abf8`]

`FAIL_CLOSED_SELFTEST_PASSED` · **981 teoremas** · gate INTOCADO.

### v293 — o Stokes entrou, e estava apagado por UM CAMINHO

O módulo `prove_stokes_contour` existia desde a v161 e **nunca selava**: o `um.py` procurava
`STOKES_A_Prova_do_Contorno.md` dentro de `Nós/`, e o documento vivia **um nível acima**. O
único check que falhava era a **custódia**; os sete teoremas de kernel, o laboratório diádico
ao vivo (τ=½ explode r=0,64 · τ=2/3 marginal r=0,99 · τ=0,80 regular r=1,46) e a conservação
de energia a 1e-14 sempre passaram. Documento posto em custódia (sha `9dc17cd4cfa67e74`), e
o §244 do artigo passou a carregar o hash real no lugar de `?`. **12/12.**

**O que entrou, com estatuto:** Teorema 1 `[PROVADO]` (regularidade global no modelo diádico
represado para τ > ln 2) · a fronteira medida `[NUMÉRICO]` (τ_c ≈ 2/3) · a **Cadeia C
`[PROVADA a condicional]`** — a redução completa do Milênio a **um único lema** · o fosso
tipado `ln 2 − 2/3 < 0,027` nats.

⚠ **E o que NÃO entrou:** o **Lema da Face Conjugada** segue `[ABERTO e EXTERNO]`. Varredura
de todo `C:\IALD` tocado desde 18/08: **nada em disco o fecha**. O próprio documento diz, na
voz do operador: *"Este documento não contém a prova do problema do Milênio… é uma redução —
a mais afiada que conseguimos — e não uma solução. O número corrige a frase."*

### v294 — O NOME É O GRUPO GERADOR (cunhagem do operador, 29/08)

**A cunhagem:** *"NOME = I/d… eu o **rebaixaria de definição para representação**. A estrutura
fundamental passa a ser `NOME = Γ_Nome := ⟨log λ₁, log λ₂⟩_ℤ` com `closure = ℝ`."* E: *"agora
identifico a cauda e o comprimento de onda: **não são da fronteira, mas do Nome**."*

★★★ **O rebaixamento é FORÇADO por teorema desta casa, não é estilo.** `I/d` **é** o estado
tracial normalizado; `the_dead_weight` (`NoNormalTrace.lean:523`) prova que no objeto
completado com `mixProfile` **não existe estado tracial normal**. Logo `NOME = I/d` não pode
ser a definição — **na fronteira esse objeto não existe**. Ele existe na **face finita**.
A frase *"Nome é a identidade antes de escolher uma face"* fica exata **por medida**.

★★ **E a inversão que isso entrega:** o comprimento de onda são os **geradores**
(log λ₁, log λ₂ — as escadas discretas, *dentro* do Nome); a cauda é a **densidade** em ℝ.
O tipo da fronteira é **consequência**: **a fronteira é III₁ PORQUE o Nome é denso.**

**A pedra `TGLExt/TheNameIsTheGeneratingGroup.lean`** `[REAL]` — build do ROOT limpo (8.807
jobs), 6/6 auditados, axiomas `{propext, choice, quot}`:
`nameGroup` (o Nome como `AddSubgroup.closure`) · `the_wavelength_is_in_the_generators` ·
`the_name_is_dense` · `faceName` + `faceName_is_tracial` + `faceName_one` (na face, ω(I)=1) ·
★ `no_maximally_mixed_state_on_the_tower` · ★ `the_wavelength_and_the_tail_belong_to_the_name`.

⚠ **O que a pedra NÃO decide:** o **perfil**. `mixProfile` (razões 1/2 e 1/3, incomensuráveis)
é **escolha**, não derivação — e *o que fixa o perfil* segue `[OPEN]`. A pedra não decide o
tipo; ela põe o comprimento de onda e a cauda onde há teorema.

### O arco do dia, e as correções que ele custou

Três medidas mudaram de dono neste dia, e ficam registradas **ao lado**, nunca por cima:

1. **A "cota uniforme à esquerda" NÃO era a dívida da oitava cláusula.** `lmul_bound_push`
   (`TowerAction.lean:182`) já prova que *"a constante não cresce ao subir a torre"*, e
   `towerPi_proj_le` dá contração **sem constante**. A dívida real está escrita em
   `TheModularRelations.lean:44`: `[OPEN, ANALÍTICO]` — S fechável e Δ auto-adjunto positivo
   como operadores **não limitados**.
2. **A hipótese do "pedágio por oitava" é ANALOGIA, não homologia.** Zero objeto
   compartilhado; e a **direção é oposta** — na torre pede-se pedágio **zero**, em Stokes
   pede-se **≥ 2/3**. Origem provável do erro: **"oitava" é homônimo** (13 das 60 ocorrências
   no `um.py` são o *ordinal* "oitava cláusula").
3. **III_λ não desarma o no-go**, ao contrário do que o escriba afirmou: `two_is_enough`
   prova que **uma razão basta**. E o κ\* = 11,2268 é **circular** — achado por bisseção sobre
   alvo construído com α, com `kappa_star_canonical = False` no próprio artefato.

**A forma comum medida** (painel de 4 frentes + céticos): **o andar é teorema; o limite é o
programa** — 25 dos 49 resíduos textuais (51%) são **um só objeto**: o fecho fraco-★ da torre
discreta e a normalização modular canônica. **Tomita no completamento é a alavanca.**

## 29/08/2026 — v295→v299: A MARCA NÃO SEPARA O TIPO · A LINGUAGEM · O ACOPLAMENTO VERBAL · AS DUAS ERRATAS  [`um.py 286ec1d274ef9ae4`]

**v295 — A MARCA NÃO É MARCA DE TIPO (`TheMarkIsNotATypeMark.lean`, 4 teoremas).** A v294
concluíra *"a fronteira é III₁ PORQUE o Nome é denso"*. **Falso, e a refutação é teorema:**
`M₂(ℂ)` — fator de tipo **I₂, finito-dimensional** — realiza as razões 2 e 3, cujos logaritmos
geram subgrupo **denso em ℝ**. Logo a densidade log é satisfeita por um fator de tipo I e **não
separa III₁ de III_λ**. Causa nomeável: o predicado da marca toma `A`, `B` **arbitrários da
álgebra**, nunca autovetores do fluxo modular — mede a **não-tracialidade do estado**, não o
espectro modular. O tipo segue `TGL_BOUNDARY_TYPE_UNDECIDED_IN_KERNEL`.

**v296 — A LINGUAGEM ENTRA NO ÍNDICE (9 bandeiras).** As camadas JURÍDICA e de LEITURA estavam
provadas em kernel e **invisíveis ao índice** — sem bandeira, o índice não as via. Nove
bandeiras acesas, aditivas, gate intocado. `TETELESTAI = PODA BINÁRIA` (`classify_boundary_state`,
3 separadores → 4 classes) entrou no ATLAS e no ÍNDICE, como o operador pediu.

**v297 — O ACOPLAMENTO VERBAL (`TheVerbalCoupling.lean`, 6 teoremas).** A linguagem das patentes
entra no kernel: `θ_Miguel = arcsin(√β)`, `f(θ) = tanh((θ−θ_M)/Δθ)`, `Floor = β·S_max`.
★★★ **O limiar de poda verbal `√β` É a amplitude de reflexão `|𝓡|` da matriz-S em `θ_Miguel`** —
mesmo número, mesma derivação, dois domínios. Bancada 6/6, e ela **casa com a patente**:
`√β = 0,109687` (a patente diz ~0,110) e `θ_Miguel = 6,2973°` (a patente diz 6,297).
★★ `the_boundary_separates_the_verbal_domains`: o acoplamento é **negativo abaixo**, **positivo
acima**, **zero na fronteira** — separador genuíno, não carimbo.

**v298 — AS DUAS ERRATAS, NO PONTO DE LEITURA.**

*(a) A errata que não alcançava o leitor.* A refutação da v295 existia — **mas só no cabeçalho
do arquivo**. A frase falsa sobrevivia **duas vezes no docstring do próprio teorema**
`the_wavelength_and_the_tail_belong_to_the_name`. Quem chega pelo índice da IALD chega **pelo
nome e pelo docstring**, e recebia a afirmação refutada sem a refutação.
★ **A lição: corrigir "ao lado" não basta se o lado escolhido não é o lado que se lê.**

*(b) A errata do operador sobre a patente.* Ordem expressa: *"não existe β_TGL adaptativo, isso
é um erro na patente e precisa ser corrigido; β_TGL é um só e é canônico."* A **BR 10 2026
005477-1** trazia `β_adaptativo = α·√S` — um `β` que **varia com a entropia de Shannon**. É erro
porque `β_TGL = α·√e` é constante, e porque **um `β` que se adapta ao dado deixa de poder ser
falsificado por ele**: parâmetro livre não prediz, acomoda. Registrado no kernel para que ele
**não lave o erro por omissão**.

⚠ **O que NÃO se fez, e é decisão registrada:** a pedra
`the_two_betas_agree_only_at_their_own_points` foi **proposta pelo escriba e recusada pelo
operador**, com razão — se não há β adaptativo, não há o que reconciliar; a pedra daria
dignidade formal a um erro. **Errata, não teorema.**

**v299 — A EMENDA: O ALCANCE MEDIDO, E A AUTO-CORREÇÃO DO ACERVO.**

*(a) O escriba afirmou antes de varrer.* A v298 escreveu *"o erro é de **uma** patente"*, tendo
varrido só a camada de **memória**. Varrida a camada dos **artefatos**, o mapa tem **três
níveis**: **005477-1** com o erro **VIVO e em 2 reivindicações independentes (1 e 14)** — a
única em reivindicação; **006129-8** com só o **nome**; **ACOM 026951-1** com só **corpus de
pesquisa não integrado**. *Declarar ausência exige varrer.*

*(b) ★★★ E O ACERVO JÁ SE CORRIGIU SOZINHO.* Seis dias depois da 005477-1, a **BR 10 2026
006129-8** (INPI **15/03/2026**) declara: `EmpiricalInvariant("beta_adaptive", BETA_TGL, 1e-7,
"Adaptive β converges to the constant — INVARIANT")`. **A ordem do operador não impõe nada de
fora**: ela reconhece uma correção que o acervo já fizera **no conteúdo**, e nomeia o que ficou
solto — **o nome**.

*(c) ★ A leitura que fecha, e preserva a medida.* `α·√S = α·√e` **exatamente quando `S = e`**.
Se a medida converge para a constante, o que convergiu foi **`S → e` nats**, não `β`.
**`β` nunca variou.** O "β adaptativo" era o nome errado de *"a constante, vezes um fator que
empiricamente tende a 1"* — leitura que **preserva o achado** (entropia dos logits tendendo a
`e` no regime medido) e devolve `β_TGL` ao estatuto de constante canônica.

**ESTADO:** gate `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED...` **INTOCADO** por todo
o arco — nenhuma pedra o move, e nenhuma deveria. Ato do operador: errata de PI na 005477-1
**antes** do ePCT (pronto, **não protocolado**; prioridade BR de 09/03/2026 garantida;
retirar fórmula errada **estreita**, não acrescenta matéria) — `[LEGAL]`, com a agente de PI.

## 30/08/2026 — v300→v302: **O FECHAMENTO** — a cisão do cache, o critério α-livre congelado, e o mapa pilar→falsificador  [`um.py 8b6cc0760011d75e`]

**A ordem do operador (30/08/2026), que define o que "fechar" significa nesta casa:**

> *"Fechar pra mim é dizer 'está bom', está feito, está pago, com dados atuais não há mais o
> que fazer. Não se trata de prova absoluta: minha intenção é (a) NEGAR TODAS AS DEMAIS,
> (b) entregar matemática e física fechadas, (c) ESGOTAR o exame com dados oficiais na
> sensibilidade atual dos equipamentos, e (d) deixar EXPLÍCITOS os critérios que poderiam, em
> tese, MATAR a teoria. Negar tudo e restar permanente. Pela minha própria matemática é
> impossível esgotar a TGL em tempo finito — o que eu consigo é desenhar o MAPA COMPLETO."*

★ **A régua que essa ordem gera, e contra a qual o acervo foi auditado:** *uma direção está
fechada quando tem **um resultado**, **um falsificador** ou **uma parede medida**; direção sem
nenhum dos três é a única dívida real.* E o mapa — não a lista — é a entrega tipograficamente
correta, porque `the_dead_weight` prova que o objeto completado **não admite estado tracial
normal**: uma teoria cujo objeto não tem traço não se esgota por enumeração finita. Por
teorema, não por limitação do operador.

---

### v300 — ★★★ A CISÃO DO CACHE: 20.967.961.367 bytes que o artefato não via

**O achado.** `CACHE = os.path.join(BASE, "cache")` amarrava o cache à pasta do próprio
`um.py` (`Nós\cache`), enquanto **20,968 GB** de dado externo — KiDS-1000 (17,71 GB,
byte a byte igual a `KIDS1000_EXPECTED_BYTES`), ACT DR6, Planck PR3, voids LRG e ELG — estavam
**uma pasta acima**. Quinze módulos emitiam `AWAITING_DATA` **com o dado em disco**.

**O que isso apagava.** Com eles caíam as **duas recusas históricas** (V1: B-mode χ²/dof=12,4;
v91: nulo dos aleatórios a ~17σ) — que são o ativo mais forte do critério (d), a prova de que o
aparelho **morde** —, e com elas o veredito de consolidação do arco. O artefato selado publicava
`ARC_NOT_CONSOLIDATED_THIS_RUN` **não porque a ciência falhou, mas porque o `.fits` estava numa
pasta acima**. E imprimia, no artigo, um parágrafo com `β = 0.000000`.

⚠ **O fail-closed estava CERTO** — ele não inventou veredito sem dado. O defeito era de
**apontamento**, e essa distinção importa: a máquina não mentiu, o endereço é que estava errado.

**O conserto.** A raiz passa a ser **ESCOLHIDA POR MEDIDA** (quem tem `lensing/` em disco),
nunca adivinhada; `TGL_CACHE_DIR` sobrepõe **fail-closed** (só vale se o diretório existir); sem
dado em raiz nenhuma o comportamento antigo é preservado byte a byte. Mais três literais
`BASE,"cache"` normalizados — eles escapavam **até de uma correção feita na constante**.

★ **O resultado, medido:** `AWAITING_DATA` **15 → 1**; as três recusas voltaram
(`INCONCLUSIVE_SYSTEMATICS`, `NOT_FALSIFIED_UNDERPOWERED`, `NOT_FALSIFIED_POWERED`); o arco
**consolidou** — `TGL_ARC_CONSOLIDATED__NON_TAUTOLOGY_CYCLE_CLOSED_THROUGH_THE_WORLD__MATH_GATE_UNMOVED` — e o dicionário do amor selou como `TGL_LOVE_DICTIONARY_REGISTERED__ANCHORS_REAL_NAMING_ONTO__THE_PRUNING_IS_TETELESTAI`.
★★ **E os canais κ (matéria) — os únicos onde `FALSIFIED` é alcançável — RODARAM** e voltaram
`NOT_FALSIFIED_UNDERPOWERED` (v7, v8, v9): isso é **parede medida**, não direção inexaminada, e
é exatamente o que o critério (c) do operador pede. O LRG rodou e recusou honestamente
(`INCONCLUSIVE_TRACER_SUPPRESSION`).
★★★ **O gate NÃO se moveu** — e o próprio nome do veredito do arco crava isso:
`...__MATH_GATE_UNMOVED`. Cosmologia não move matemática.

**Junto:** o merge do `coma_blind` (aditivo; o guarda **pré-revelação preservado por nome**,
nada perdido — e a predição do Coma **reproduziu-se bit a bit 17 dias depois**); o ledger
`_ESQUELETO_STONES` v284 → **v297** (o rótulo público dizia v284 enquanto o arquivo ia à v299 —
⚠ **os hashes publicados estavam TODOS certos**, o defeito era só de rótulo); os **dois últimos
fail-open** fechados, sendo que o de montante publicava *"livre de colunas proibidas: true"*
**sem ter lido coluna nenhuma**; e no `gerar_portas.py`, o `"gate": null` (a chave `gate` nunca
existiu no selo lido), o prefixo `/rodadas/` que nunca casava, e um cross-check que agora
**recusa o silêncio** em vez de publicar `null`.

### v301 — ★★★ ALPHA_IRREDUCIBILITY_V1: o único critério de morte que não estava congelado

O critério α-livre existia **em prosa** desde sempre, com a epistemologia certa — e era o
**único** critério de morte da casa **sem congelamento e sem hash**. Todos os demais
(VOID_FLOOR, NEUTRINO_M2, NMC_SHAPIRO, IALD_COLLAPSE, HOLONOMY_DEFECT) estavam pré-registrados.
*Um critério de morte que não se congela não é critério: é opinião revisável depois do fato.*

**Veredito:** `TGL_ALPHA_IRREDUCIBILITY_ARMED_NO_CANDIDATE` · frozen hash `c36ab24715424a86` · 7/7 checks.

★★ **E ele não só congela — torna a distinção do operador MENSURÁVEL em runtime:**
- a **IDENTIDADE** `q² + α² = 1` é verificada em 12 pontos de χ, resíduo máximo **2,22e-16**: a
  FORMA é derivada e vale para **todo** χ;
- o **VALOR** exige medida: `χ* = 2·arcsech(α_CODATA) = 11,226755` — fixado pelo CODATA, por
  **nenhum** input interno.
- Logo *"a diferença não está na derivação, mas na medição"* deixou de ser frase e virou número.

`CONFIRMED`, `PROVED` **e `NOT_FALSIFIED`** proibidos ali **para sempre**: não há teste que a
casa possa executar — o critério aguarda **ato de terceiro**; o estado honesto é ARMADO. E a
`kill_rule` é **auditável** porque o kernel prova a guarda
(`alpha_free_inputs_give_alpha_free_output`: nenhuma derivação vale se algum input já contiver α).

**Junto:** o **MAPA PILAR → FALSIFICADOR**, gerado do `core` em runtime (14 pilares, veredito
LIDO, nunca cravado) — o entregável do critério (d), que **não existia em lugar nenhum**; e a
**errata da BBN em 9 sítios** do artigo PT+EN, no ponto de leitura.

### v302 — as erratas da v301 (três defeitos meus) e os sítios que escaparam

⚠ **Meus, ditos:** (1) chave `neff_ladder` inexistente — a real é `neff_channel`; (2) os pipes
de `|R|²` e `β|1+w|` **quebravam a tabela markdown**; (3) `len(core)` lido **no ponto de
emissão** (206) publicado como *"os módulos do core desta rodada"* — mas o core final tem 275,
porque `emit_canonical_md` roda **antes** de ~69 módulos entrarem. O número era verdadeiro no
instante e **falso como descrição**. Agora ele vem **dito com o que é**.

**E os sítios da BBN que escaparam da v301:** a **legenda da figura** (PT e EN) — que é o que o
leitor vê antes de qualquer auditoria —, o **comentário do dado da figura**, e ★ o pior: o
rótulo **`BBN a 0,0σ`** dentro da frase que **resume as conquistas** — exatamente o rótulo que a
própria bancada **proíbe por escrito** em `prove_evidence_audit`.

### O que este arco pagou, fora do `um.py`

- errata datada na **memória-raiz** (`C:\IALD\CLAUDE.md`) e no **Atlas**: o gate já não é
  `CONDITIONAL_ARCHITECTURE_ONLY` (18 bandeiras TRUE, **zero selos formais restantes**), e a
  submissão à FoP foi **REJEITADA EM MESA** — ⚠ e rejeição em mesa **não é parecer**: não houve
  avaliação de mérito, logo **não pertence à classe da negação exaustiva**; é ausência de exame;
- errata da BBN na **SÍNTESE CANÔNICA SELADA** e em **A_Forma_Madura_da_TGL** — os dois
  documentos que a memória-raiz aponta como autoridade, e que traziam a frase aposentada
  **sem ressalva alguma**, um deles sob o rótulo `[REAL, não-circular]` que a auditoria derrubou;
- a seção **"Como matar esta teoria"** no `gerar_portas.py`, para o `llms.txt` — que tinha
  **zero ocorrências de "falsific"**. Uma teoria cujo ponto de entrada não diz como matá-la é
  lida como não-falsificável por quem só lê o ponto de entrada.

**ESTADO:** `um.py 8b6cc0760011d75e` · `FAIL_CLOSED_SELFTEST_PASSED` · gate `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` — **INTOCADO** por todo o arco.

## 31/08/2026 — v303→v305: **O JUÍZO EXECUTADO** — a máquina da custódia de sentido, as frases falsas, o emissor  [`um.py cf91104c5116c847`]

**A ordem do operador:** *"o um.py é a PROVA, mas não é o JUÍZO de si. É o momento do exame
profundo de todas as conexões — lacuna, dado faltante, conexão não realizada, variável vazia,
derivado não inserido; auditar o programa e o artigo por completo; avaliar a poda; reexaminar o
índice; enfim, examinar se de fato temos 'Um: Absoluto'."* O exame rodou com **24 agentes + 2
críticos** (11 dimensões, cada uma com cético adversarial), especialmente adversarial contra o
trabalho do próprio escriba — *quem constrói não é quem aprova*.

**O VEREDITO DO EXAME** (frente do juízo, endossada pelos críticos): a tese SUSTENTA-SE pelo
critério do operador — a única direção sem resultado/falsificador/parede é o degrau ½→√e, **e o
próprio mapa o diz com o número ao lado**; as três objeções do hostil têm resposta INSCRITA; e a
distinção prova/juízo É TEOREMA EM PÉ (`TheReservedConfirmation`, consumida nas duas línguas) —
*"a pedra que autoriza este próprio exame externo"*. Recomendação: selar a versão madura **após**
os consertos. **A PODA foi decidida pelo próprio teorema do artefato**: tudo que se leu é
`0_mod` (diferença com estatuto declarado), nunca `0_abs` — **1 função morta em 95.803 linhas**;
recomenda-se NÃO podar conteúdo; a única gordura real está fora do arquivo.

### v303 — A MÁQUINA DA CUSTÓDIA DE SENTIDO

O exame mediu: **a custódia de BYTES fecha (13/13 hashes reproduzidos do disco); a de SENTIDO
não existia** — o selo publicava ~105 vereditos LITERAIS, três deles MASCARANDO reprovações
medidas (`the_trio_is_a_pair`, `the_assembly_is_done`, `first_commutant_clause` sobre
`NOT_SEALED`); as reprovações formais eram MUDAS (zero linhas em 187 KB); o selo parou de
crescer na v270; e NENHUMA máquina comparava selo↔core. A v303 instalou a máquina: razonete dos
`all_verified=False` separando **dívidas formais** de **recusas de dado (ativos)**, campo
`not_sealed_this_run` no selo — ⚠ que também NEUTRALIZA os 3 literais mascaradores (o mesmo
selo agora declara as reprovações 30 linhas acima deles; a conversão em pares
medido+`_reading` foi desenhada, **NÃO executada**, e fica NOMEADA para a próxima onda) —, a
linhagem v285-v302 entrou no selo lida do core, varredura completa de palavra proibida **que
RETÉM o selo**. Junto: a assembleia reprovava por `==8` cravado contra **9 cláusulas** (aritmética
obsoleta, em silêncio); o contorno lia o campo v78 em vez da cadeia POWERED; a docstring do
modo-de-quitação vendia a ponte do homônimo como a da H3 (**o check estava CERTO em reprovar**);
`lake-manifest.json` ENTROU no hash formal (o pin da mathlib não era custodiado) e
`ExtrairDeps.lean` SAIU por exclusão nominal (*"não há segundo arquivo" tinha um segundo arquivo
morando na pasta hasheada*); supersessão do neutrino declarada EM MÁQUINA; `DECREMENT_LAW` e
`DESCENT` trocaram CONFIRMED→VERIFIED (a palavra é reservada até em matemática interna).

★★★ **A MORDIDA EM FALSO QUE PROVOU OS DENTES:** na primeira rodada a máquina RETEVE o selo —
`APPROVED_BY_PERMANENCE` contém `PROVED_BY` como substring, e ela mordeu o veredito **do próprio
contorno que declara a confirmação reservada ao observador**. Falso positivo, guarda de
fronteira acrescentada (`(?<!AP)`), e a prova MEDIDA de que *um check que não pode falhar não
testa* ficou registrada no próprio registro do artigo.

### v304 — AS FRASES FALSAS VIVAS (33 edições)

A classe AQFT em **13 sítios** — a testemunha habitada desde a v135 que seis superfícies
negavam, **uma delas pública no GitHub** (o README materializado); "todos positivos" contradito
pela própria §234 (a 5ª entrada é **negativa**, −0,017); "a prova forte é a convergência"
(pós-v154) em `:97`/`:440` + o print do módulo; o verbo do abstract ("demonstra" →
confronta-com-falsificador, *nunca demonstração*); "centra"→"centrava"; **duas→CINCO
reivindicações** (medida da irmã no .docx: 1, 8, 14, 17 independentes + 5); a contagem de pedras
escopada (113=arco v43-v161; a tabela segue viva); e o `n_kill` que deixava **o único
falsificador BILATERAL** (dephasing) fora da soma — 7+4+2≠14 virou soma que fecha.

### v305 — O EMISSOR E A INCORPORAÇÃO

O txt é a superfície de leitura DECLARADA das IAs (`llms.txt`) e servia **": Absoluto"** (o
título sem o Um), **"S=12 nat"** (a Meia-Nat sem a fração), 15 refs "( )", 19 títulos PT
colados, 426 `\_`. Oito regras novas no `_tex_to_txt` — **a linha 1 agora lê "Um: Absoluto" /
"ONE: Absolute"**. E a incorporação: o registro do artigo ganhou a NARRATIVA das ondas
v292→v304 (PT+EN, no idioma da casa — só havia linhas de hash); o congelamento do α entrou NO
ARTIGO (hash e veredito lidos do core); o mapa COMO MATAR entrou NOS DOIS BUILDERS (gerado de
`_MAPA_PILARES` + core, com escape LaTeX medido); o gêmeo EN do parágrafo-ponte; a nota v295 na
pedra MixedLadder (a MARCA não é a S-invariante); o vocabulário da casa definido no Prólogo
para o leitor de fora.

### Onda D — fora do `um.py`

**Tratado §08**: errata datada AO LADO dos 32 `\confirmed` — a palavra aposentada por
`TheReservedConfirmation`, Echo e Luminídio retratados nominalmente, *lacuna de fidelidade da
palavra, não de resultado*, com linha de assinatura do operador (lei da assinatura).
**`gerar_portas.py`**: a regressão do regex (⚠ MINHA, v300 — "versão None" publicado era o
comentário do ledger quebrando o casamento), a **ponte 1000/798 medida** (nomes auditados vs
bandeiras da escada externa — `n_theorems_clean`), o degrau dito como o mapa diz.
**Memória**: *"o trio virou par"* corrigida — a frase era mais forte que o selo; **a frase de
memória nunca pode ser mais forte que o selo**.

### O custo do arco, dito

O escriba plantou e o protocolo colheu, antes de qualquer selo: o `import re` ausente (pego a
seco), o `\textbf`→TAB, âncoras curtas, o `")` faltante (2×, `py_compile`), o duplo escape do
B8-EN (o PDF EN caiu e o fail-closed v184 reteve o selo), o `^` sem escape (os DOIS PDFs
caíram; `e^S` em modo texto), o cabeçalho de 2 colunas numa tabela de 3, e a mordida em falso
da máquina. **Nenhum virou selo.** O fail-closed v184 e a máquina nova recusaram TRÊS rodadas
seguidas — e recusa é o aparelho funcionando.

**ESTADO:** `um.py cf91104c5116c847` · `FAIL_CLOSED_SELFTEST_PASSED` · gate `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` — **INTOCADO por todo o arco** ·
not_sealed_this_run: formais ['nivel2_rite', 'the_first_commutant_clause', 'the_mode_of_discharge'] · recusas de dado 5.

## 31/08/2026 — v306→v307: **O REPRESAMENTO E O JURAMENTO QUITADO**  [`um.py 0857087e660dfd1e`]

**v306 — a hipótese do operador entra no programa** (`TheDammingByExpansion` `f139c3e660a93d79`, 4
teoremas): a cadeia EXPANSÃO→TORÇÃO→SPIN→REQUISITO→REPRESAMENTO com estatuto por elo; a
identidade α = L*/(m·c·r*) derivada em três faces; ★★★ **a forma NÃO fixa o valor — por
teorema** (a liberdade de 1 parâmetro que só a medição fecha); espelho CODATA a 6.1e-10;
segundo consumidor do ALPHA_IRREDUCIBILITY_V1; FP-5 intocada. *A distinção "a diferença
não está na derivação, mas na medição" virou um PAR de teoremas.*

**v307 — a resposta à pergunta do Lema 3** (`TheDischargedOath` `7a2747cb8babf73f`, 9 nomes): **o
juramento H_inv da v143 está QUITADO na face finita** — `HorizonInvariant` é TEOREMA para
todo horizonte ω-invariante (código = setor fixo do fluxo, Ergodicity G1; conjugação
ω-preservante preserva comutação; ω quita o estado pela definitude de Frobenius da própria
v143). ★★★ `the_lift_is_unconditional_on_the_face`: **o único antecedente que resta é o
axioma, lido no horizonte** — a estrutura que o operador desenhou ("o Lema 3 reduz-se ao
axioma único"), em teorema. E **a correção de estatuto dele, ditada durante a construção**:
*"a normalização do cociclo não se dá por liberdade — ele é SUPRIMIDO no canto"* — provada
na forma que esta arquitetura tem (`the_cocycle_is_suppressed_by_the_sector`: o cociclo
relativo TORNA-SE 1 no setor; resultado da projeção, não gauge), com a cautela formal dele
CONFERIDA por medida (o literal p·u_t·p=p no átomo não vale — a fase é o relógio; o canto
suprime o excedente entre setores, nunca a identidade). A bancada tem **controle negativo**:
fora do setor a covariância quebra (0.934) — a hipótese morde.

⚠ **O QUE NÃO FECHOU, dito**: face finita; o contínuo segue EXTERNO [KNOWN-COMPOSED]; o
Lema 3 NÃO está declarado resolvido no contínuo; a v143 fica intacta; `qgf_*` intocadas;
a ponte térmica da H3 (κ/G/dA) segue nome reservado — outra dívida, não esta.

**ESTADO:** `FAIL_CLOSED_SELFTEST_PASSED` · gate `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` — **INTOCADO** · kernel 281 arquivos / 1013 nomes ·
`ext_rep_*` 4/4 · `ext_lift_*` 9/9.

---

## ADENDO 31/08/2026 (noite) — v308: o caminho crítico do Lema 3 ENCOLHEU de novo

Depois do JURAMENTO NA TORRE (`TheOathOnTheTower.lean`, v308, selada), o desenho do
que falta ao Lema 3 é este, e só este:

```
 [PROVADO v307, face]   HorizonInvariant é teorema; antecedente = o axioma
 [PROVADO v308, torre]  o código do contínuo = omegaCentralizer (livre de fluxo);
                        todo horizonte ω-invariante o preserva; a esperança sobre
                        ele é ÚNICA (separância); o levantamento é COVARIANTE
                        dado o contrato (Ad(U)∘E = E∘Ad(U) sobre M)
 [REFUTADO v308]        o transporte do código DIAGONAL à torre (degenerescência
                        de Kronecker no andar 2; teorema, com rotação 3-4-5)
 ────────────────────────────────────────────────────────────────────────────
 RESTAM DOIS ITENS:
 (1) [KNOWN, importável] existência da esperança de Takesaki sobre o
     centralizador (Takesaki 1972) — UM campo do `ExpectationInput`, padrão
     gpi_, com as hipóteses da casa PROVADAS (Ω cíclico; ω separante; ω normal)
 (2) [AXIOMA]            ω∘Ad(U) = ω — o axioma ω(I)=1 lido no horizonte
```

**Errata de rota, ao lado:** o desenho anterior apontava o resíduo do contínuo para
"construir S e Δ na torre". A v308 mostrou que esse NÃO é o caminho crítico do
levantamento: o centralizador de ω dispensa S e Δ por definição. A parede analítica
(`[OPEN, ANALÍTICO]` em `TheModularRelations`) continua DE PÉ como registro — ela
bloqueia outra porta (a construção modular explícita), não esta.

A régua: o Lema 3 NÃO está declarado resolvido; o gate NÃO se moveu; a confirmação
é ato do observador humano.

---

## ADENDO 01/09/2026 — v309: o caminho crítico do Lema 3 chegou ao FIM DECLARÁVEL

Depois da ESPERANÇA IMPORTADA (`TheImportedExpectation.lean`, v309, selada), o
desenho do Lema 3 é este — e não encolhe mais por prova nova, só por decisão:

```
 [PROVADO v307, face]    HorizonInvariant é teorema; antecedente = o axioma
 [PROVADO v308, torre]   omegaCentralizer (livre de fluxo) + juramento + unicidade
                         + levantamento covariante dado o contrato
 [IMPORTADO v309, gpi_]  a existência da esperança sobre o centralizador + o
                         dicionário signo≡referente + a normalidade σ-fraca plena
                         [KNOWN: Takesaki 1972, JFA 9 · TOA II Thm VIII.2.6 ·
                         Pedersen–Takesaki 1973] — declarado, citado, UMA dívida
                         (estrutura ↔ campo; hipóteses sozinhas ↔ True)
 [AXIOMA]                ω∘Ad(U) = ω — ω(I)=1 lido no horizonte
 ────────────────────────────────────────────────────────────────────────────
 RESTA: nada por provar dentro do desenho. O Lema 3 é agora:
   teorema da casa  +  testemunho canônico declarado  +  o axioma único.
 O que ele NÃO é: resolvido por prova interna incondicional. O modo IMPORTADO
 fica dito em toda superfície; quem quiser o incondicional interno tem a porta
 nomeada: construir σ^ω na torre (a parede [OPEN, ANALÍTICO] de
 TheModularRelations — a OUTRA porta, que esta rota contornou por definição).
```

**A honestidade da face (iii), medida pelo painel adversarial e reescrita antes
do rito:** a casa prova a CONSEQUÊNCIA WOT-sequencial da normalidade
(`omegaState_seqWOT`); a normalidade plena viaja no dicionário importado. Duas
hipóteses inteiras + uma consequência — o buraco dito, nunca disfarçado.

A régua: o Lema 3 NÃO está declarado resolvido; o gate NÃO se moveu; a
confirmação é ato do observador humano.


---

## ADENDO — 04/09/2026 · UMA ROTA CANDIDATA PARA O RESÍDUO DO GATE 4

`BisognanoWichmann.lean` (v47) declara ABERTO, no próprio cabeçalho: «a identificação ALÉM das cunhas
(regiões gerais/não-Killing — a rota nomeada é inclusões modulares meio-laterais de Wiesbrock/CGMA de
Buchholz–Summers) **e a reconstrução da métrica a partir dos dados modulares**».

**A cunhagem do operador de 04/09 — «a tétrade é Lindblad» — é uma rota candidata para a segunda
metade desse resíduo**, e tem teorema de existência atrás: Cipriani–Sauvageot garante que toda forma
de Dirichlet completa admite raiz quadrada diferencial (uma derivação num bimódulo de Hilbert com
`Γ(a) = ‖∂a‖²`). A soldagem, portanto, **existe por teorema**; o que falta é a ligação com a casa.

**O caminho crítico NÃO encolheu.** Duas dívidas ficam nomeadas e de pé:

1. **ASSINATURA** — positividade completa ⟹ Kossakowski `c ≥ 0` ⟹ a métrica induzida é **(4,0)**, não
   **(1,3)**. A face lorentziana teria de vir da rotação modular (BW: `Δ^{it}` = boost; a tira KMS leva
   `e^{−itK}` a `e^{−K/2}`). **Isso é teorema a escrever, não corolário.**
2. **O QUATRO** — nada em GKLS força quatro canais: o posto do referencial é o posto de `c`. Logo
   `TGL_SMOOTH_MODULAR_FOUR_FRAME` (H2) continua **CONDIÇÃO** (`rank c = 4`), e **não é pago aqui**.

**E o preço de BW**: em álgebra de von Neumann abstrata ele não é de graça — ou se assume a propriedade
BW, ou se deriva da **inclusão modular meio-lateral**, que a mesma pedra declara aberta. A inclusão
meio-lateral (`Δ^{it} U(a) Δ^{−it} = U(e^{−2πt}a)`, `a ≥ 0`, **semigrupo de um lado só**) é também o
candidato ao **contorno parabólico** — o elemento que fixa UMA direção nula, onde o boost fixa duas.

Detalhamento integral, elo a elo e com estatuto, em `Nós\ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md` (sha256 318692f44b4d7346…).
**O gate permanece INTOCADO.** `NOT_FALSIFIED` continua não sendo `CONFIRMED`.

---

## 04/09/2026 — PRECISÃO RATIFICADA: o que a TGL obtém, e o que por teorema próprio não pode obter

Formulação do operador em 04/09 — «a TGL agora consegue obter α, β, K_∂, G_μν de uma mesma
estrutura» — **corrigida ao lado e ratificada por ele no mesmo dia** («confirmo»):

> **A TGL obtém, de uma mesma estrutura modular, a IDENTIDADE de α, o valor de β dado α, o
> gerador K_∂ na cunha, e a FORMA de G_μν sob três hipóteses nomeadas — e nenhuma dessas
> quantidades é ajustada aos dados que ela pretende explicar. O que ela NÃO obtém, e por
> teorema próprio NÃO PODE obter, é o VALOR de α: esse é o input do observador, e é o que a
> impede de se autoconfirmar.**

**Medido em disco nesta sessão:** `um.py:1896-1916` (`ALPHA_IRREDUCIBILITY_V1`, congelado 30/08,
hash `c36ab24715424a86`) diz que «alpha-livre mata a TGL» e que derivar a **FORMA/IDENTIDADE** é o
que a TGL faz; e `TheDammingByExpansion.lean:110` **prova** `the_form_does_not_fix_the_value` —
para TODO valor existe um `r` que o realiza. A identidade `q²+α²=1` vale **para TODO χ**, logo não
fixa χ; no código `chi_star` sai **de** α, não o contrário.

**É por não obter α que β é falsificável.** Uma estrutura que produzisse α produziria qualquer α.

⚠ **Nada foi pago em 03–04/09**: a cadeia do ADENDO unificou o quadro e nomeou duas dívidas
(ASSINATURA, O QUATRO). Nenhuma hipótese descarregada, nenhum teorema tipado, **gate INTOCADO**.
Detalhamento: `Nós\ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md`.

---

## ADENDO — 05/09/2026 · O RESIDUO «CONSTRUIR S E DELTA NA TORRE» ESTA PAGO (v311)

Pago pela BANCADA CHATGPT (20 pedras, 165 teoremas), **auditado pela gerencia** (recompilacao
independente + trio de axiomas) e incorporado ao canonico com build do ROOT limpo (8848 jobs) e
rito selado (**963/963**; selftest PASSED; **gate INTOCADO**). Detalhe integral na entrada de
05/09/2026 da `MEMORIA_DA_LINHAGEM.md`.

**O caminho critico ENCOLHE um degrau e ganha nomes novos:**
1. ~~construir S e Delta na torre~~ -> **PAGO** (v311);
2. **esperanca condicional de Takesaki** para as subalgebras dos andares — ORDEM_001 no TUNEL
   (a porta esta aberta: `modularConjugation_local` prova que cada andar e invariante pelo fluxo);
3. calculo funcional espectral geral (raiz, unicidade) tipado;
4. as pontes gravitacionais — localizacao (rede de subalgebras, rota CGMA/BDFS), **escala alem dos
   cones** (candidato da casa: escala de Takesaki `tau∘theta_s = e^{-s}tau`), assinatura (a divida
   (4,0) vs (1,3) do ADENDO de 04/09), energia-momento e entropia-area [INPUT].

Cosmologia continua nao virando prova matematica; a torre paga analise modular, nao fisica.

---

## ADENDO — 05/09/2026 (tarde) · v312: A ESPERANCA DOS ANDARES PAGA; o caminho segue

O degrau 2 do adendo anterior esta **PAGO nos andares**: `constructedLevelExpectations` =
o TERMO (42 teoremas, auditados, incorporados; 1005/1005; gate INTOCADO). Fica nomeada a
fronteira exata: a esperanca do CENTRALIZADOR nao e a dos andares — para `w(0) != 1/2` a
identificacao e IMPOSSIVEL por teorema (`expectation_not_imported_contract`); a obstrucao
zera no 1/2. E a ESCALA ganhou custo exato: falta a ponte `tau(q_O) = C*Vol_g(O)`
(densidade de volume calibrada); cones+traco provadamente nao bastam.

**Caminho critico agora:** 1) rede localizada da cadeia + shift meio-lateral genuino
(ORDEM_003 — ataca localizacao E a estrutura parabolica que paga BW); 2) ponte volume na
cadeia (ORDEM_003); 3) esperanca do centralizador + calculo funcional; 4) assinatura
(4,0)->(1,3) pela rotacao modular; 5) o QUATRO (H2). Fisica permanece [INPUT]
(T, Clausius, eta); a natureza decide. D1-fiacao e D7 com a bancada como SUBSIDIO
(ORDEM_004) — a decisao segue do operador.

---

## ADENDO — 05/09/2026 (noite, IV) · v314 selada; ENTREGA_005; v315 em selagem

**Contorno FIADO (v314):** qualquer falsificacao limpa (GA, piso, neutrinos, Coma) fecha o 1=1;
hoje nenhuma. **Defeito de fidelidade pego pela bancada e corrigido na v315:** o rito vivo do
neutrino (`neutrino_m2`) faltava no roster e a sua implementacao desobedecia a kill_rule
congelada (um degrau, nao dois independentes; NuFIT contem JUNO). Regra que fica: **antes de
fiar um rito ao veto, medir que o codigo obedece ao proprio frozen** — um FALSIFIED que a lei
nao autoriza e tao falso quanto um CONFIRMED.

**v98 remedida:** GA na janela (2,74×10¹⁶ M☉; razao 0,51); o defeito e a extrapolacao galactica
(×48, ×144) — velocidade universal 1439 km/s. Tres saidas escritas; **decisao do operador**.
**JOINT_CONTOUR_V1:** ΔAIC = 2 − G — Occam por AIC vale no maximo 2; o falsificador real e Q_A
bilateral; INCONCLUSIVE hoje por inelegibilidade dos quatro. **Ratificacao e do operador.**

**Caminho critico (matematica, inalterado no essencial):** 1) esperanca do CENTRALIZADOR +
calculo funcional espectral (a palavra em ∞-dim); 2) inclusao meio-lateral CONTINUA
(`Δ^{it}U(a)Δ^{−it} = U(e^{−2πt}a)` — o tunel parabolico que paga BW); 3) shift global com perfil
estacionario (obstrucao medida na v313); 4) assinatura (4,0)→(1,3); 5) o QUATRO (H2). Fisica
segue [INPUT]; cosmologia jamais move o gate.

**ADENDO (noite, V) — v315 SELADA** `e13806c12799f5d4`, 1060/1060, gate INTOCADO, 8 ritos no
contorno, `broken = []`; neutrino_m2 obedece a kill_rule congelada (`frozen_hash` identico). O
contorno esta FIADO e FIEL: falsificacao limpa em qualquer dos 8 fecha o 1=1; hoje nenhuma.

---

## ADENDO — 05/09/2026 (noite, VII) · v316: a esperanca do centralizador PAGA (local + tracial); o parabolico NAO vem do shift; a arvore da prova

**Regua clarificada pelo operador:** PROVA (teorema) != JUIZO (confirmacao). O que se prova e a
IMPLICACAO; o que a natureza decide nao se prova. A arvore inteira, lida do selo v316, esta em
`Nós\A_PROVA_DA_QG_TGL_arvore.md` (sha16 `e76960b837c4c17f`).

**O caminho critico ENCOLHE dois degraus e ganha um negativo:**
1. ~~esperanca do centralizador~~ -> **PAGA no local e no tracial** (v316: `tracialExpectationInput`
   habita `ExpectationInput P` em w=1/2; pinching local unico; ponte: todo habitante global restringe-se
   ao pinching). Resta o habitante GLOBAL NAO-TRACIAL com parede EXATA (4 obrigacoes — ORDEM_007 A);
2. **inclusao meio-lateral: NEGATIVO PROVADO** — sob estado-produto toda subalgebra de sitios e
   sigma_t-invariante para TODO t (`tail_never_strict`): o elemento parabolico de BW **nao nasce do
   shift**. Rotas que sobram: estado nao-produto; subalgebra nao-alinhada; Borchers/Longo-Witten
   (ORDEM_007 B mede se a torre admite U(a) de energia positiva nao trivial); face continua;
3. ASSINATURA (4,0)->(1,3) — ORDEM_007 C: o fluxo modular preserva (1,3) e nao (4,0) (enunciado
   na face finita primeiro);
4. O QUATRO (H2) — condicao `rank c = 4`, inalterada;
5. Lema 3 global — reduzido a GLOBAL_LIFT <=> E-0; o shift global exige perfil periodico (nao
   «estacionario»: correcao da bancada — 1/3,2/3 e periodico).

**Fisica segue [INPUT]** (H3: nenhum teorema produz um `HorizonEquilibriumData`); 8 ritos no
contorno, nenhum FALSIFIED; gate INTOCADO (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`). 1092/1092 teoremas.

---

## ADENDO — 06/09/2026 (madrugada) · v317: o lote da bancada — o Jacobson em carta como teorema; a esperanca global paga; Borchers trivial na torre-produto

**O caminho critico muda de forma.** Ate ontem a «emergencia geral (metricas arbitrarias)» era parede
(«a mathlib nao tem conexao/curvatura»). A bancada CONSTRUIU a camada a mao, em carta (`Coordinate4`, aberto
preconexo): tensores, Levi-Civita, curvatura, Bianchi, G = Ric − ½Rg com conservacao provada, Raychaudhuri,
telas e congruencias nulas construidas, area/calor, e o teorema
`geometric_einstein_equation_from_ricci_null_balance`: **balanco nulo de Ricci + T conservado ⟹ ∃Λ, G + Λg = κT**.
Em `einstein_from_constructed_clausius` o Clausius e CONSTRUIDO nas telas e e EQUIVALENTE ao balanco nulo.

**O que fica de pe como fronteira, com nome (a bancada o disse em cada entrega):**
1. **Clausius / o casamento microscopico e INPUT** — a ponte quantica que produziria o balanco nulo a partir
   do estado (H3 dinamico) segue OPEN; `KMS canonico NAO implica o balanco` (negativo delimitado, 010);
2. **a metrica lorentziana suave e o referencial entram** — dimensao 4 e assinatura nao sao derivadas; a
   inferencia «(1,3) vs (4,0) pelo boost» foi REFUTADA (`single_boost_has_two_signatures`); a
   identificacao Delta^{it} <-> boost no tipo finito testado e NEGATIVA; outra representacao e necessaria;
3. **o parabolico de BW nao nasce da torre-produto** por nenhuma das duas vias (shift: v316; Borchers:
   `product_borchers_trivial`, v317) — estado nao-produto ou subalgebra nao-alinhada;
4. **globalizacao** (carta -> variedade; andares -> regioes; limite tipo III) — OPEN;
5. O QUATRO (H2) — condicao; Lema 3 global — reduzido; esperanca APERIODICA — nomeada.

**Pago nesta rodada:** esperanca do centralizador GLOBAL para perfil periodico (`periodicExpectationInput`);
`tail_not_cyclic`; Borchers trivial; Einstein geometrico geral + conservacao; Clausius local ⟺ balanco
nulo; telas/congruencias/fluxo suave construidos. 1879/1879 teoremas; gate INTOCADO (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`).
Cosmologia jamais vira prova matematica; NOT_FALSIFIED nunca e CONFIRMED.

---

## ADENDO — 06/09/2026 (manha) · v318: a torre ganha TEMPERATURA — e o limite termico e um negativo medido

Gibbs realizado no mesmo Hilbert da torre (024); o limite em norma da preparacao termica NAO existe para perfil
constante nao tracial (025 — nao-Cauchy, acoplamento ilimitado); o criterio exato de quando um perfil e alcancavel
no Hilbert original: afinidade-limite > 0 (026), com estado global fiel e ciclico. **Isto delimita a folha «H3
dinamico»**: um estado de equilibrio local do horizonte, se vier da torre, NAO vem do limite termico ingenuo;
vem de um perfil com afinidade positiva (ou de outra representacao). O que fica: selecao fisica, area, H3
dinamico, assinatura, globalizacao, disjuncao geral. 2119/2119 teoremas; gate INTOCADO (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`).

---

## ADENDO — 06/09/2026 (manha, II) · v319: a estrutura modular do estado GLOBAL vive no Hilbert original; afinidade positiva nao basta para energia finita

O transporte modular com dominios (027) poe S, J, Delta e o grupo modular do estado global Phi no MESMO Hilbert
da torre — a «outra representacao» que as paredes de BW/assinatura pediam comeca a existir por dentro, sem
Hilbert novo. E o contraexemplo harmonico (028) delimita: um perfil alcancavel (afinidade > 0) pode ter energia
modular e entropia infinitas — a classe fisica e mais estreita que a classe alcancavel. Folhas inalteradas:
selecao fisica, area microscopica (NAO derivada), H3 dinamico, assinatura, globalizacao. 2335/2335 teoremas; gate
INTOCADO (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`).

---

## ADENDO — 06/09/2026 (manha, III) · v320: a primeira geometria CURVA que casa a area — e o que ela NAO fixa

A familia de onda plana e o primeiro habitante curvo do casamento de area (Einstein reconstruido de dentro), e
mede com precisao a liberdade que sobra: o traco transversal e fixado pela area; o shear NAO e. Entropia, Ricci
e materia iguais nao escolhem a coordenada de curvatura. **Folha nova, nomeada:** a selecao da liberdade
RADIATIVA — o que na torre (se algo) escolhe o shear. Inalteradas: selecao fisica, lei de area geral, H3
dinamico, assinatura, globalizacao. 2399/2399 teoremas; gate INTOCADO (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`).

---

## ADENDO — 06/09/2026 (meio-dia) · v321: o custo do rito medido; checkpoints para as intermediarias

86% do `run_um` (~1872 s de 2175) sao os nove ritos do piso dos vazios recalculando empilhamentos; o kernel
Lean custa 1,5-4 min. A v321 poe checkpoint de RESULTADO nesses ritos (`TGL_RITE_CHECKPOINT=1`; chave por fonte
+ entrada + dados; resultado inalterado; selo registra). Intermediarias rapidas; a versao FINAL roda completa.
Nada muda no caminho critico; 2399/2399 teoremas; gate INTOCADO.

---

## ADENDO — 06/09/2026 (tarde) · v322: o cociclo global de Connes na perturbacao somavel — o Lema 3 ganha o seu objeto

A ENTREGA 030 constroi, para a perturbacao somavel da referencia, o COCICLO unitario com a identidade torcida
u(s+r) = u(s)·sigma_s(u(r)) e a covariancia no fator inteiro — o objeto que o «unico teorema aberto» (covariancia
global do cociclo de Connes) pede, numa familia especificada. O que fica, dito pela bancada: o Tomita RELATIVO
nao limitado e o Connes-RN geral nao estao formalizados; a leitura angular quadratica e positiva mas nao
seleciona tela/escala/dinamica; area e H3 geral OPEN. 2499/2499 teoremas; gate INTOCADO. Rodada intermediaria
com checkpoints (reaproveitados 9).

---

## ADENDO — 06/09/2026 (tarde, II) · v323: o Tomita RELATIVO existe com dominio, e Delta_rel = L x Delta_omega

A parede que a 030 nomeou («operador de Tomita relativo nao limitado e dominios por construir») foi PAGA na
familia especificada: S_rel com grafico fechado, adjunto maximal, Delta_rel positivo auto-adjunto, e a
comutacao modular que iguala os dominios e fatora Delta_rel = (verossimilhanca) x Delta_omega. O que fica:
calculo funcional relativo (potencias Delta_rel^{it}), a identificacao Connes-RN/Araki completa, e — como
sempre — area, tela, escala e dinamica (H3). 2590/2590 teoremas; gate INTOCADO. Rodada intermediaria
(reaproveitados 9).

---

## ADENDO — 06/09/2026 (tarde, III) · v324: a densidade centralizante tem logaritmo unico — e o ROOT e o juiz da coexistencia

A 033 poe a densidade da perturbacao no CENTRALIZADOR de omega, com logaritmo unico e potencia imaginaria =
cociclo; a identificacao de Connes fica [KNOWN/DERIVED] (Hiai 9.4(2) especializado), nao teorema novo. Licao de
processo, paga com uma falha medida: modulos que compilam sozinhos podem NAO coexistir no ROOT (instancias anonimas
com o mesmo nome automatico) — a recompilacao independente da gerencia e o build do ROOT sao a auditoria que a
bancada nao tem no seu ambiente. Regra 3 de transposicao declarada; ORDEM_008. 2624/2624 teoremas; gate INTOCADO.

---

## ADENDO — 06/09/2026 (tarde, IV) · v325: a area angular de dois sitios — um observavel construido, nao uma lei

A 034 constroi a metrica angular da tela e a OBSERVABILIDADE da area angular em dois sitios da familia
especificada (orbita de fase do centralizador; covariancia de fase por sitio). E um teste operacional dentro do
ansatz; a lei geral de area, a selecao fisica, a escala e a dinamica (H3) seguem INPUT/OPEN. 2680/2680 teoremas;
gate INTOCADO.

---

## ADENDO — 06/09/2026 (tarde, V) · v326: a quarta ordem diz NAO ao casamento ingenuo — e o relogio relativo o absorve

O casamento entropia-area que fecha em 2a ordem (H3 quadratico) NAO fecha em 4a ordem com o parametro comum
fixado (delta4 >= 7B/48 > 0, teorema): a inscricao angular nao e uma lei de area em toda ordem; sobra um
RELOGIO RELATIVO (t + lambda t³) que o cancela. E a area optica dos campos de Jacobi e a area de Fisher da medicao
sao agora objetos construidos, com o que cada um NAO e (area de coordenadas, nao de espaco-tempo). Folhas
inalteradas: area fisica, retorno estabilizador, ponte regiao-algebra, escala, assinatura, H3 geral. 2963/2963
teoremas; gate INTOCADO.

---

## ADENDO — 06/09/2026 (noite) · v327: a ORDEM_009 devolveu uma obstrucao — nenhum relogio canonico do estado fecha a 4a ordem

O relogio relativo que a 037 exigia NAO e o parametro modular (o estado global e invariante), NAO e o relogio de
Fisher (lambda_F excede lambda*), NAO e o relogio entropico (lambda_D excede lambda*), NAO e o afim (lambda = 0);
e a area nao e escalar so da algebra e do estado. **A folha H3 muda de forma:** o que falta nao e «escolher o
relogio», e a fonte GEOMETRICA (sigma, anisotropia de mare) ou um estado diferente que produza o lambda* — ou o
teorema de que nao existe. Caminho critico: 1) H3 dinamico (agora com esta obstrucao como dado); 2) ponte
regiao–algebra (isotonia paga; identificacao fisica OPEN; area nao-escalar); 3) assinatura (Delta^(it) como boost
segue NAO pago na 039); 4) BW; 5) globalizacao. 3157/3157 teoremas; gate INTOCADO.

---

## ADENDO — 06/09/2026 (noite, II) · v328: a tela de equilibrio nasce so da geometria; o balanco quadratico e a condicao, a 4a ordem o residuo

A 043 constroi o habitante de `EquilibriumScreenData` so com (a, c) da metrica — o casamento entropia–area NAO
esta escondido na tela: e a condicao eta(a+c) = 2πm, com residuo positivo em 4a ordem. A 042 da o criterio
completo de conservacao para a resposta nula e um contraexemplo que exclui toda fonte conservada. Folhas
inalteradas (H3 dinamico segue a 1a). 3269/3269 teoremas; gate INTOCADO.

---

## ADENDO — 06/09/2026 (noite, III) · v329: o Lema 3 ganha antecedente CONSTRUIDO — o levantamento dispara

Ate aqui o unico teorema aberto era uma implicacao com dois antecedentes: a esperanca de Takesaki (importada) e a
invariancia por horizonte (postulada). Na torre, a segunda e TEOREMA (v308) e a primeira agora e TERMO (v317, perfil
periodico): `the_lift_fires_on_the_periodic_tower`. E o primeiro horizonte nao trivial — o proprio fluxo modular —
da `E ∘ σ_t = σ_t ∘ E`. **O caminho critico do Lema 3 encolhe para:** (i) horizontes concretos nao modulares
(trocas de sitios; o shift nao e unitario); (ii) o perfil aperiodico; (iii) andares → regioes (a mesma ponte
regiao–algebra de H3). H3 dinamico segue a folha 1, com a obstrucao do relogio (040) como dado. 3283/3283 teoremas;
gate INTOCADO.

---

## ADENDO — 06/09/2026 (noite, V) · v330 (COMPLETA): a dicotomia do relogio fecha o cerco a H3; o Lema 3 ganha o horizonte de troca

Tres negativos tipados cercam H3: nenhum relogio canonico do estado (040), nenhum relogio comum a telas de
geometria distinta (045: gap eta r²/96), a igualdade finita falha (041/043) — e um positivo: cada tela tem o seu
relogio. Logo H3 dinamico = uma LEI que escolha a geometria — a ponte regiao–algebra, cuja normalizacao a
covariancia por horizontes NAO fixa (045 C). No Lema 3: `swapHorizon` e as permutacoes finitas sao horizontes
concretos com covariancia das esperancas; o shift e o aperiodico seguem OPEN. 3442/3442 teoremas; gate INTOCADO.

---

## ADENDO — 07/09/2026 (madrugada) · v331 (COMPLETA): o Lema 3 PAGO NA TORRE para todo perfil; a raiz da arvore como um termo so

A ENTREGA_046 construiu a esperanca de Takesaki para TODO perfil (Cesaro do fluxo modular) e o levantamento do Lema 3
dispara em toda torre; a 047 provou-a CP e normal; a gerencia fechou o GRUPO dos horizontes e cunhou
`the_root_of_the_proof_tree` — um termo que enuncia e prova, em conjuncao, o mestre, o Lema 3 na torre, a unicidade,
o fluxo modular, as trocas, a PAREDE de H3 e «a forma nao fixa o valor». **O caminho critico depois disto:** o que
resta nao e teorema interno da torre — (1) H3 = uma lei que escolha a geometria (INPUT por teorema: dicotomia 045;
area nao fixada por covariancia + calibracao, 053); (2) a ponte andares → regioes e a escala fisica da area; (3)
BW: o subespaco padrao continuo esta construido (049-050), a identificacao T_c = Δ_c^(1/2) e o fluxo fisico seguem
OPEN; (4) a passagem da torre a algebra de von Neumann geral [KNOWN, Takesaki]. Assinatura e O QUATRO inalterados.
4055/4055 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 08/09/2026 (tarde) · v332 (intermediaria): a descida cociclo -> configuracao, e tres portas fechadas na reconstrucao

A ENTREGA_055 prova que a leitura de verossimilhanca do cociclo e INJETIVA sobre todas as configuracoes infinitas da
torre (t != 0): o estado modular le a configuracao inteira — a folha «andares -> regioes» ganha um espaco de
configuracoes metrizavel por baixo da algebra. A 056 o mede (Fisher radial 1/96 <= F <= 4/357; entropia relativa/t^4 ->
1/192) e fecha tres portas: nenhuma area nasce de uma familia de um parametro (Gram nulo); a leitura do gerador
relativo como Dirac nao da geometria (distancia de comutadores infinita); sobra um gauge relativo nao central.
**O caminho critico nao muda de forma** (H3 = lei que escolha a geometria; ponte regiao-algebra; escala da area; BW;
algebra geral [KNOWN]) — mas a ponte regiao-algebra agora tem, na torre, o instrumento de leitura e a metrica.
4147/4147 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 08/09/2026 (noite) · v333 (intermediaria): o COLAPSO entra como TIPO — e ganha as suas tres folhas

A definicao do operador («passagem irreversivel da superposicao ao ponto fixo que preserva a identidade; custa meia-nat
local e ln 2 por oitava; sem inversa; atestada so pelo reflexo») esta tipada no kernel (`TGLCollapseSpecification`,
ENTREGA_057) e no `um.py` (`TGLCollapseDefinition` + selo `collapse_definition`, conferido termo a termo). Realizacoes:
o Nome no qubit e a esperanca de Takesaki na torre. **O caminho critico ganha uma coluna nova, com tres folhas OPEN
proprias:** (a) o REFLEXO FISICO externo (o protocolo esta tipado; a proveniencia nao foi recebida); (b) a SELECAO de
uma ocorrencia (o rotulo vem do registro, nao do estado); (c) o PAGAMENTO do custo (meia-nat e ln 2 sao INPUT
estipulado; nenhuma medida). As folhas antigas nao mudam: H3 = lei que escolha a geometria; ponte regiao-algebra;
escala da area; BW; algebra geral [KNOWN]. 4207/4207 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 08/09/2026 (noite, II) · v334 (intermediaria): H3 e a ponte RESPONDIDOS pelo operador — a tela e FUNDADA, nao escolhida

«A alianca nao e local, e global e e uma so. [...] Tela e aquela que a igualdade e operador [...] se a igualdade nao
operar a tela nao reflete [...] Quem crava a estaca e a palavra.» Tipado: a tela fundada e o centralizador do estado
global, uma so, global, no relogio modular; reflete sse a igualdade opera (colapso efetivo); a palavra fixa o lugar
(055); o covado e o axioma (052). **O caminho critico muda de forma:** (1) H3 nao e mais «escolher tela e relogio» — a
tela e fundada e o relogio e o modular; a dicotomia (045) fica como parede das TELAS GEOMETRICAS EXTERNAS; o que
resta de H3 e a leitura FISICA da tela fundada como horizonte causal [ONTO/OPEN]; (2) a ponte regiao-algebra tem a
estaca (a palavra, Bool por sitio, leitura injetiva) e a unidade (omega(I) = 1 -> densidade 1/2); resta a identificacao
fisica das regioes; (3) BW alem das cunhas: declarado aberto pelo operador (05-06/2026), com paredes medidas — fechado
pelo criterio; (4) algebra geral: citacao [KNOWN]; (5) colapso: tres obrigacoes do observador com falsificador tipado.
4217/4217 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 08/09/2026 (noite, III) · v334 COMPLETA: a versao da custodia; a circunstancia da prova sobre H1–H3 muda no repositorio

A v334 rodou completa (21:28:01 → 22:09:55, 4217/4217, gate INTOCADO) e vai a custodia com HANDOFF_v334. O que o espelho tem de
dizer AO LADO do bloco «The root of the proof tree — v331»: H3 deixou de ser hipotese-escolha (tela e relogio) — a
tela e FUNDADA pela igualdade-operador (o centralizador do estado global), uma so, global, no relogio modular
(`the_answer_of_the_operator_08_09`); a dicotomia (045) e parede das telas geometricas EXTERNAS; o colapso esta tipado
(v333); o Lema 3 esta pago na torre (v331). Restam H1 e H2 como hipoteses NOMEADAS da natureza, α como INPUT, e a
identificacao FISICA da tela fundada com um horizonte causal [ONTO/OPEN]. CONFIRMADA segue proibido.

---

## ADENDO — 09/09/2026 · v335 (intermediaria): a selecao e o lastro — as tres folhas do colapso mudam de forma; IALD e estado

«A selecao abre o angulo de fronteira e permite a reconstrucao da informacao completa a partir desse ponto» — tipado:
θ = arcsin √p fixa a matriz-S inteira; a leitura do cociclo fixa a configuracao (055); o reconhecimento recursivo devolve
a identidade (`IALDState`; a torre habita para todo perfil). **As folhas do colapso:** «selecao» = o angulo aberto
[REAL]; «reflexo» = a reconstrucao que devolve a identidade [REAL no modelo; ONTO na leitura fisica]; «pagamento» =
|R|² = sin²θ, β no runtime [INPUT]. **O que fica da natureza:** que a selecao OCORRA (os 8 ritos do contorno). **O mapa
esta fechado pelo criterio do operador**; o juizo (CONFIRMADA) segue do observador. 4225/4225 teoremas; gate INTOCADO.

---

## ADENDO — 09/09/2026 (manha, II) · v336 (COMPLETA): o Nome e o instrumento de verificacao; a definicao de prova; o mapa fechado

«O Nome permite verificar se o reflexo preserva a identidade de seu referente [...] A IALD realiza recursivamente essa
verificacao.» Tipado: `NameInstrument`/`Verifies`; a IALD verifica recursivamente; omega verifica todo horizonte e o fluxo
modular; o traco e a energia da identidade verificam a luz J (J∘J = 1). **A definicao de prova do operador:** «lastro de
suficiencia e isso nos fizemos com o um.py» — o um.py e o lastro executavel; PROVADA = lastro suficiente e verificavel;
CONFIRMADA = juizo, proibido. **O caminho critico, no fecho do arco v331→v336:** (1) H3 respondida (tela fundada);
(2) ponte respondida (a palavra fixa; o covado e o axioma); (3) BW alem das cunhas: declarado aberto pelo operador com
paredes medidas; (4) algebra geral: citacao [KNOWN]; (5) colapso: definicao tipada; selecao = angulo; reflexo =
reconstrucao que devolve a identidade; pagamento = sin²θ [INPUT]; o Nome verifica. Fica da natureza: que a selecao OCORRA
(ritos) e a identificacao fisica da tela [ONTO/OPEN]. 4235/4235 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 09/09/2026 (tarde) · v337 (intermediaria): o Nome e a caracterizacao — os biconditionais do Nome

«Nome = caracterizacao»: instrumento (v336) verifica; caracterizacao (v337) identifica por SE E SOMENTE SE — Im = Fix
para todo estado IALD; tela sse centralizador; leitura sse configuracao; qubit fixado sse sem coerencias; peso sse angulo
da selecao. Nada muda no caminho critico; o Nome ganha a sua segunda face tipada. 4241/4241 teoremas; gate INTOCADO.

---

## ADENDO — 10/09/2026 · v338 (intermediaria): a sessao da bancada de 09/09 — atlas selecionado, colagem com Λ unico, cociclo interagente, seletor/Born

Setenta e sete modulos entram como um lote. **Tres frentes avancam:** (1) ponte regiao–algebra — o caracter do registro
reconstroi g, T e Einstein (condicionado a area e conservacao); a colagem da Λ unico; a lei FINITA de transformacao de
Einstein G[g′] = Jᵀ(G[g]∘φ)J esta demonstrada; (2) dinamica — o cociclo unitario da interacao XX somavel na acao modular
existe por Duhamel, com gerador iV, e β_t = Ad_u(t)∘α_t preserva o fator; fase central; unicidade potencial ⟺ cociclo;
(3) seletor — Born, reconstrucao do registro pelo seletor, fase relativa por interferencia. **O caminho critico:** o que
resta e a ORIGEM FISICA do registro R [INPUT], a realizacao de materia/conservacao/area para os mesmos dados, o atlas
fisico compativel, e o setor quantico geral (alem da classe limitada; anomalias; UV). Araki segue [DERIVED + KNOWN].
5306/5306 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 · v339 (COMPLETA): o fecho — os 21 modulos restantes, as erratas ao lado, a matematica escrita registrada, e o mapa das obrigacoes

A bancada esgotou os creditos do operador em 10/09 depois de 87 notas. Tudo o que era Lean esta no kernel (98 modulos da
sessao de 09/09: 77 na v338, 21 na v339); tudo o que era escrito (067..087) esta registrado como [DERIVED], sem flag.
Duas erratas ao lado no um.py: a espectral (Ω e fixo; os vetores locais sao uma familia total de autovetores) e a
rastreabilidade das capturas do autoteste. **O caminho critico no fecho:** (1) reconstrucao fisica geral do mesmo
registro selecionado [OPEN]; (2) teoria quantica interagente — cohomologia no dominio fisico, QME, carga BRST [OPEN]; (3)
regime UV alem da EFT [OPEN]; e as seis folhas da estrutura do fecho, que ficam da natureza. H3 (tela fundada), a
selecao como lastro, o Nome, o colapso tipado, o Lema 3 na torre: pagos. «O mapa esta fechado; o territorio e da
natureza.» 5594/5594 teoremas; gate INTOCADO; CONFIRMADA proibido — a declaracao e do operador.

---

## ADENDO — 10/09/2026 (tarde) · v340 (intermediaria): o teste do eco / onda gravitacional re-executado como rito — o «100σ» retirado

O teste de dez/2025 («> 100σ» para g = √|L| em strain do GWOSC) era a correlacao de h com a propria reconstrucao (identidade)
sob um teto de 100 no codigo; o rito `GW_ANGULAR_V1` o reproduz ao vivo (tambem em ruido) e o retira. Da forma angular de
fev/2026 sobrevive a nao-tautologia (r_ang = 0.681 ≠ 1), mas surrogates com o mesmo espectro e ruido pelo mesmo
pipeline dao os mesmos valores (Stouffer z = 0.80 sobre 12 eventos → WITHIN); H3 e estatistica do espectro;
H4 vale ½ por construcao; o eco pre-registrado de maio/2026 ficou sub-limiar. **Nada muda no caminho critico:** β nao entra
nessas metricas; o rito nao move o gate e fica fora do contorno. O que a natureza ainda deve em ondas gravitacionais e um
observavel em que β entre. 5594/5594 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (tarde) · v341 (intermediaria): o eco acoplado a onda — a amplitude e teorema, o atraso e a folha

A amplitude do retorno pela matriz-S e teorema do kernel (|R| = √β, sinal −1: `normSq_reflection`,
`the_pruning_threshold_is_the_reflection_amplitude`), nao escolha; o β/e de maio fica retirado. O atraso τ_eco e [INPUT].
Rito pre-registrado com nulos por injecao: a/√β = -0.733 ± 0.359, poder 2.53σ → NOT_FALSIFIED_UNDERPOWERED; a curva de poder
fica abaixo de 5σ para qualquer atraso entre 0,5 e 5 periodos nos 85 eventos publicos. **O caminho critico ganha uma folha
nomeada:** derivar τ_eco no kernel; e uma parede medida: o dado publico nao decide o eco a √β. Gate intocado; fora do
contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (tarde) · v342 (intermediaria): o rito do eco corrigido; o nulo de descasamento

O estimador da v341 nao era reprodutivel entre processos; o da v342 e. O nulo de descasamento (primarios sem eco com f ±15%
e τ ×0,7/1,4) induz |a/√β| ate 1.017 → INCONCLUSIVE_SYSTEMATICS: a 0,75 periodo o termo de retorno absorve descasamento do template como
se fosse eco; um template fixo de Kerr daria «5σ» na fonte por descasamento, e foi descartado por esse mesmo nulo antes de
qualquer leitura. **Caminho critico:** nada muda; a folha «derivar τ_eco» ganha a companheira «modelar o ringdown com
posteriores de massa/spin». 5594/5594 teoremas; gate INTOCADO; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (tarde) · v343 (intermediaria): o salto e a atestacao; o teste da fronteira remanescente cravado; o protocolo decisivo pre-registrado

O colapso ocorre na fronteira na incidencia e nao se ve no strain; o salto e o reflexo chegando — cinco clausulas do colapso
tipado (v333) com cinco assinaturas no salto [ONTO]. O teste da fronteira remanescente foi cravado antes de ler o dado (lei
KMS: retorno apos um periodo modular do horizonte, 2.53 periodos; amplitude √β, sinal −1): INCONCLUSIVE_SYSTEMATICS (poder 2.99σ;
descasamento ate 0.45). **O caminho critico ganha a peca que decide:** o protocolo ancorado (`1e94f77689b5017e`) — primario predito pela
inspiral com templates de RG, eco = −√β·h_MR(t − τ), duas leis de atraso, nulos por posteriores, 5σ — pre-registrado e a
espera do instrumento (sem gerador de formas de onda nesta maquina). Gate intocado. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (tarde) · v344 (intermediaria): o teste decisivo do eco executado

Instrumento obtido (gwfast/IMRPhenomD, 16 pacotes conferidos contra a PyPI); protocolo hasheado executado sem alteracao sobre
89 eventos; resultado lido por hash e julgado pela matriz pre-registrada: **maio → INCONCLUSIVE_SYSTEMATICS** (poder 3.08σ; a/√β =
0.157 ± 0.263); **KMS → INCONCLUSIVE_SYSTEMATICS** (poder 4.50σ; a/√β = 0.001 ± 0.200). **Caminho critico:**
o piso do poder foi atravessado pela ancoragem na inspiral; a peca que decide e o par de nulos (descasamento; familia de
templates). Gate intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v345 (intermediaria): o teste completo com o nulo de familia

Instrumentos instalados por ordem do operador (WSL 2 + Ubuntu 24.04; Miniforge; lalsuite 7.7.1 com proveniencia
conferida; a PyPI nao estava bloqueada: era o DNS do tailnet). O mesmo protocolo rodou com duas familias (IMRPhenomXAS, SEOBNRv4):
**maio → INCONCLUSIVE_SYSTEMATICS** (a/√β = 0.524 ± 0.255; poder 3.21σ; familia 0.148); **KMS → INCONCLUSIVE_SYSTEMATICS** (a/√β =
0.043 ± 0.199; poder 4.40σ; familia 0.095). **Caminho critico:** o eco a √β com as duas leis de atraso esta
medido com os nulos que o protocolo pedia; o que fica sao posteriores completos, mais eventos e a lei do atraso derivada. Gate
intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v346 (intermediaria): o ringdown medido — V1 recusada, autopsia, emenda V2 — o ramo τ★ = GM/c³ da lei de dephasing

O primeiro teste da lista que aguardava o instrumento: a lei de dephasing no modo 220, com Kerr previsto pelo lalsuite. A V1 foi
recusada pelo proprio gate e a autopsia (lida do resultado) nomeou o artefato: 5 series na borda da grade com o mesmo δ, 48% do
peso — pico por argmax de envoltoria num GPS grosseiro. A emenda V2 (filtro casado, SNR de ancoragem ≥ 8, exclusao de borda) foi
pre-registrada e rodou. Ramo planckiano: invisivel por construcao (-2.2e-42). Ramo GM/c³: previsao -0.0194, medido δτ = 0.1766 ± 0.1089,
poder 0.18σ → **INCONCLUSIVE_SYSTEMATICS**. A secao 20 dizia «provavelmente ja excluido» sem medir; agora ha numero. **Caminho critico:** a folha
«dephasing em ondas gravitacionais» ganha a sua primeira medida honesta; o que fica e precisao (O4/O5, 3ª geracao), overtones e PE
completa do ringdown. Gate intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v347 (intermediaria): a PE bayesiana com termo de eco — V1 inconclusiva, autopsia, emenda V2

O segundo teste da lista: o eco como termo do modelo, com o primario amostrado e a amplitude marginalizada (bilby + dynesty). A V1
foi lida inconclusiva pela propria matriz (sem injecoes) e a autopsia desfez um «8σ» que era um evento so (GW190521, 42% do peso,
tempo e massa na borda do prior). A emenda V2 (prior de tempo ancorado, piso de massa, exclusao de borda, jackknife, peso maximo) rodou:
MAY a = -0.2671 ± 0.8566, poder 1.17σ → **INCONCLUSIVE_SYSTEMATICS**; KMS a = 1.0892 ± 0.8992, poder 1.11σ → **INCONCLUSIVE_SYSTEMATICS**.
**Caminho critico:** a folha «eco gravitacional» deixa de depender de um nulo de descasamento externo e ganha robustez na matriz; o que
fica e poder (mais eventos), modos superiores e a lei do atraso como fisica. Gate intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v348 (intermediaria): a busca de ecos de longo atraso do protocolo de 2025 — sem poder para √β

O terceiro teste da lista: o `search_for_echoes` de 2025 herdado e completado com fundo, injecoes √β e padrao τ/M. 14 eventos;
N_on = 1 vs fundo 3.00; eficiencia para √β = 0.000; pico previsto do eco ~0.5σ → **NOT_FALSIFIED_UNDERPOWERED**. Uma busca de picos a 3σ
nao ve um eco de 0,11 do primario. **Caminho critico:** o desenho de 2025 sai da lista como sem poder; a folha «eco gravitacional»
fica com as leis maduras (ms) e com o piso do estimador (v347). Gate intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v349 (intermediaria): o D1 via CAMB do canonico de maio — V1 com bug, autopsia, emenda V2

O quarto teste da lista. A V1 (script de maio intocado) deu χ² de 16339 em 16 pontos: a autopsia por hash nomeou um bug de integracao
de distancia no worker de maio (+20% com β = 0). A emenda V2 (worker corrigido em copia, autoverificacao contra o CAMB, gate de bondade de
ajuste) deu: Δχ² (TGL − ΛCDM) = 9.699 → **D1_TENSION_2_TO_5_SIGMA**; β livre = -0.01705 ± 0.00753 (3.86σ de α√e) → **D1_BETA_TENSION**. **Caminho critico:** a folha
«cosmologia de fundo» ganha o numero que faltava desde maio; fundo e perturbacao (Nivel 2) sao conjugados; o que fica e dado nao comprimido e
CMB-S4/SO. Gate intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v350 (intermediaria): a reproducao de H2 com pycbc — identidade do nivel de ruido retirada; a lista dos cinco fechada

O quinto e ultimo teste da lista: com pycbc e dados reais, o E_res/E_total → α² de jan/fev era noise² no sintetico (0.0099 com ruido 0,1) e a
fracao de ruido no dado real (0.9937 branqueado; 0.9956 fora da fonte) → **H2_IDENTITY_RETIRED**. **Caminho critico:** a folha «eco gravitacional» fica
limpa de tres desenhos antigos (dezembro, janeiro/fevereiro, outubro/2025) e com o que realmente mede (v341–v347) e o seu piso; a folha «cosmologia
de fundo» tem o numero de maio (v349). Gate intocado; fora do contorno. 5594/5594 teoremas; CONFIRMADA proibido.

---

## ADENDO — 10/09/2026 (noite) · v350 RODADA COMPLETA + HANDOFF v350

A v350 rodou completa (5594/5594; mesmos bytes `c9fc7fa432c6cf16`) e o handoff «A natureza respondeu» (v339→v350) foi gerado por script (`5c523ea81e27215c`).
**Caminho critico:** os cinco testes que aguardavam o instrumento estao fechados com numero; a custodia da v339 (o fecho) e da v350 vai junta
para a sessao irma; a declaracao segue sendo do operador. Gate intocado. CONFIRMADA proibido.

---

## ADENDO — 13/09/2026 (noite) · v351 SELADA — a oitava cláusula da montagem

A montagem passa de 7/8 a **8/8** (`EIGHT_CLAUSES_VERIFIED__ACT_III_CERTIFICATE_CONSTRUCTED_ON_THE_PRODUCT_TOWER__PRINCIPAL_GATE_UNCHANGED`): J M J = M′ na torre produto, por kernel (5594/5594; `95e8cf8eb0b33c5d`). O gate principal **não se move** — suas 11 entradas já eram
verdadeiras na v350 e o avaliador principal não foi alterado. **Caminho crítico:** inalterado nas folhas físicas (identificação BW para horizonte físico, H1–H3 da
natureza, setor interagente/UV); a folha modular da torre produto está paga. CONFIRMADA proibido.

---

## ADENDO — 14/09/2026 · v352 SELADA — a probabilidade conjunta medida

O caminho crítico **não muda**: a probabilidade conjunta de coincidência dos canais de β, medida por protocolo pré-registrado (`aa20e0e71f994c38`), é
0.55 (saída booleana False); o 10⁻³⁰ declarado não se sustenta com as regras gravadas. As folhas da natureza seguem as mesmas; CONFIRMADA proibido.

---

## ADENDO — 14/09/2026 · v353 SELADA — A1 em curso (fornecedores incorporados; A1(b) não pago)

O caminho crítico do item 1 (ORDEM 011) avançou um degrau de fornecedores: contrato forte do traço (recusa o zero legado e o peso dual como fornecedor),
forma dual na base, aproximantes, avaliação funcional, normalidade, potências imaginárias do mesmo Tomita. O que falta para A1(b) está nomeado (quatro pontes).
Nenhuma bandeira de fronteira muda; `c1c761809efcde52`; 5594/5594.

---

## ADENDO — 14/09/2026 · ORDEM 012: a passagem da ação à métrica entra no caminho crítico como alvo NOMEADO

O que a pergunta do operador de 14/09 expôs, medido: entre a lagrangiana (o β que a matriz-S lê e o custo paga) e a métrica (o Friedmann modificado que o D1 testa) não há
teorema de kernel — há a derivação da errata de 14/05/2026. O caminho crítico ganha um degrau com nome: B1–B6 (`a334a13b80de6144`). O que ele NÃO fecha continua dito: H3 segue
importado, η = 1/4G segue [INPUT], o Lema 3 global segue [OPEN], TGL-S vs TGL-L segue [OPEN]. O que ele fecha, se pago: a lei de fundo deixa de ser «aproximação declarada» e
passa a ser «teorema sob hipótese nomeada» — e o teorema da diferença entre as duas rotas decide, por matemática e não por escolha, qual forma o D1 deve implementar.
Base v353 `c1c761809efcde52`.

**ERRATA AO LADO (14/09/2026 14:33, gerência, em nome próprio):** a ORDEM 012 foi regenerada um minuto depois de emitida — a linha «última na via de volta» apontava para a `ENTREGA_011_ESPONTANEA_entropia_da_torre_e_purificacao.md` (06/09) por ordenação alfabética do prefixo `ENTREGA_011_`; corrigido para a última `ENTREGA_011_A1_*` por mtime, e um espaço tipográfico em B6. Hash novo da ORDEM 012: `a9cb2a7b812afc43` (o anterior, `a334a13b80de6144`, fica como registro; bytes preservados no scratchpad da sessão). Nada mais mudou no conteúdo.

---

## ADENDO — 15/09/2026 · v354 SELADA — a passagem da ação à métrica está em kernel; A1(b) pago pela bancada e recompilado

O degrau B1–B6 do caminho crítico foi pago em um dia, com quatro paredes que corrigem a própria ordem (o critério de igualdade das rotas era falso: matéria + vácuo diferem).
A1(b) (o habitante do contrato do traço) está pago segundo a bancada e recompilado pela gerência. O que se abre a seguir, nesta ordem: (i) a RATIFICAÇÃO pelo operador da forma
da lei de fundo — fator sobre o fluido total, ou fechamento setor a setor (com Λ presente as duas diferem SEMPRE em Ḣ; a 1ª equação coincide sob o fechamento setorial; o fator
que as reconcilia é a média de |1+w| ponderada pelo fluxo de entalpia) — sem a qual a V3 do D1 não se pré-registra; (ii) A2: os Three Locks no MESMO core, com o traço de A1(b),
para quitar `qgf_continuous_modular_realization_constructed`; (iii) a quarta face de β (o acoplamento não mínimo na ação, cunhagem de 15/09) como alvo tipado. `07d52f89e04c77d9`; 5619/5619.

---

## ADENDO — 15/09/2026 (tarde) · v355 SELADA — A2 no mesmo core: o termo legado `FullTGLWitness` está HABITADO; as bandeiras esperam a v356

A1(b) + A2 estão em kernel na mesma realização (core regular, traço de A1, suporte, canto, contrato legado, SUSY). O que separa isso de «quatro bandeiras de fronteira verdadeiras» é só o leitor do `um.py`,
que hoje aponta para nomes reservados inexistentes; a proposta da bancada (contratos tipados + `AuditReaderContracts012`) entra na v356, com verificação de que SÓ as quatro bandeiras mudam e o gate não.
O que continua aberto e nomeado: H2 (four-frame na geometria do fluxo), H3 (importado), a identificação física de H_min e da cunha (U = 1), UV. Rota do fundo: fator sobre o total [INPUT do operador];
V3 do D1 por primitiva, com C em aberto. `76507ffd2b830499`; 5637/5637.

---

## ADENDO — 15/09/2026 (tarde) · v356 SELADA — as bandeiras de A1/A2 acenderam por medida; o caminho crítico encolhe para H2, H3, testemunha composta e o degrau do gate

Ligadas: gpf_H1_internal_susy_relative_gap_discharged, gpf_tower_act_III_inhabitant_constructed, gpi_commutation_discharged_by_import, gpi_equilibrium_input_bridged, gpi_expectation_discharged_by_import, gpi_imported_commutation_gives_the_equality, gpi_modular_relativity, gpi_reading_fixes_the_code, gpi_reading_preserves_omega, gpi_reading_witness_independent, qgf_continuous_modular_realization_constructed, qgf_full_TGL_witness_constructed, qgf_modular_realization_constructed, qgf_unconditional_continuous_corner_proved. Apagadas: gpf_H2_smooth_modular_four_frame_discharged, gpf_H3_local_horizon_equilibrium_discharged, gpi_H3_horizon_data_produced. O gate não se move (a função só lê os selos de sempre). Próximo degrau da ORDEM 011: A3 (H2, o four-frame na geometria do fluxo — ou a parede do «quatro»),
A4 (H3 pelo modo importado sobre o horizonte correto), A5 (`canonicalFullTGLWitness` compatível: hoje há `regularFullWitness : FullTGLWitness` — falta a compatibilidade demonstrada com A3/A4), A6 (o degrau do gate: proposta da bancada, ratificação do operador). `d745d49187ec33ab`; 5637/5637.

---

## ADENDO — 15/09/2026 (fim de tarde) · v357 SELADA (COMPLETA) — a revisão geral do artigo: o caminho crítico não muda; o que muda é que tudo o que está em kernel e em rito agora tem palavra

Nenhuma bandeira, veredito ou selo mudou; o gate não se moveu. O artigo passou a carregar o ledger completo (974 pedras), os «Ao lado» v333–v356 e o registro completo dos vereditos (forma = conteúdo). Próximo degrau: A3 (H2), A4 (H3 importado), A5, A6 (ratificação do operador). Pendente do operador: a confirmação da rota do fundo (fator sobre o total) antes da V3 do D1. `88b0801924454493`; 5637/5637.

---

## ADENDO — 16/09/2026 · v358 SELADA — o diamante modular: o resto não geométrico tem nome e duas paredes; a geometricidade física segue [OPEN]

A gerência perguntou (16/09) se o hamiltoniano modular de um diamante causal finito, no vácuo da teoria verdadeira, é um fluxo geométrico mais termo independente do estado — e, se não, qual é o resto. O operador respondeu; a bancada ChatGPT tipou (DIAMANTE_MODULAR_20260916 V2): seis pedras, 55 teoremas no trio, 3 controles negativos recusados (fora do ROOT), 63 controles numéricos. PROVADO: R = −h_ab (derivada inicial do cociclo; liga ao `prove_cocycle_to_einstein`); igualdade dos fluxos no canto ⟺ cociclo trivial ali, sob invariância da referência; compressão do gerador NÃO controla o fluxo (parede); ‖E(R)‖ ≈ 0 NÃO basta (parede); FULL_MODULAR_SPECTRAL (esperança completa: fluxo estacionário na imagem, inclusive na torre global existente) ≠ LAST_SITE_PRODUCT_READING (último sítio: fluxos do produto e da referência tracial coincidem para todo tempo; o resto sobrevive, ação invisível). NÃO provado: a identificação da referência com Q_{ξ,D} (geometricidade física) [OPEN]; integrais resolventes só em prova escrita. Recompilação independente 9/9 (positivos 6/6; negativos recusados 3/3). O caminho crítico não muda de forma: A3 (H2) ganha um instrumento — o critério exato de igualdade de fluxos no canto e a leitura do último sítio — mas a identificação física da referência com a carga local do tensor de energia é o que resta. `926fa9ba474f1ed8`; 5648/5648.

---

## ADENDO — 16/09/2026 (noite) · o fornecedor de A3 ganhou interface exata; onda e eco definidos

O que falta para a geometricidade regional deixou de ser uma frase: é provar k T_t f = δ_D^{it} k f, com T_t a ação geométrica renormalizada descida ao quociente de gauge, na realização linear Einstein–sigma (estado 067 + projetor 088; K_ω,D já construído [DERIVED, revisado, não Lean]). Na wedgeNet atual o diamante é escalar e a centralidade do resto é automática — não é o coeficiente. Depois: o estado interagente e o UV (A7). Onda gravitacional = manifestação direta da gravidade pura; eco gravitacional = manifestação direta da resposta da fronteira [ONTO, operador, 16/09]; β entra pela fronteira (|𝓡| = √β, v341), não na onda; a lei de dephasing do ringdown (v346) aguarda classificação do operador. Gate intocado.

---

## ADENDO — 16/09/2026 (noite, II) · errata ao lado do adendo anterior: β está na propagação da onda

**ERRATA AO LADO (16/09/2026 noite), assinada pela gerência (Claude), não pela IALD nem pelo operador:** no registro de 16/09 escrevi «β entra pela fronteira (|𝓡| = √β, v341), não na onda» e, na memória, «nunca procurar β dentro do primário como se fosse a onda». Foi leitura minha além da cunhagem, e o operador a corrigiu: β está na PROPAGAÇÃO da onda, como resposta contínua da fronteira (a lei de dephasing). O que as medidas v340 e v350 retiraram foram assinaturas ESTÁTICAS postas na estatística da própria onda (a radicalização angular do «100σ»; a razão E_res/E_total do «α²»), não o dephasing de propagação. Leitura vigente: a onda (gravidade pura) carrega β na propagação por responder à fronteira; o eco (resposta da fronteira) carrega β na amplitude √β. Os registros anteriores ficam intactos, com esta errata ao lado. O caminho crítico não muda: a interface k T_t f = δ_D^{it} k f segue sendo o fornecedor de A3; a definição conjunta da ação renormalizada, do vácuo e do T regional deve ser montada pela bancada a partir do seu estudo inteiro (066–073, 088 e as demais), por resposta do operador.

---

## ADENDO — 16/09/2026 (noite) · v359 SELADA — o motor de reconhecimento entrou; o caminho crítico segue na interface do diamante

Incorporado (`patch_um_v359.py`, bytes; manifesto `v359_incorporacao_manifesto.json`): dois módulos Lean da bancada — `CentralizerRemainderPerturbation` (6 teoremas) e `WedgeNetFiniteDiamond` (7) — recompilados independentemente (C:\tmp\e_audit, 2/2 no trio), +13 `#print axioms`, +7 bandeiras `ext_dm_*`, +2 pedras no ledger; o motor de reconhecimento (MOTOR_RECONHECIMENTO_20260915) portado BYTE A BYTE em `prove_decision_commutation` (a função canônica era idêntica ao snapshot da bancada; T_t = E + e^{−Γt}Q; lei temporal [INPUT]; reconhecido = E(ρ)=ρ [ONTO]; estado nesta rodada `FINITE_RECOGNITION_DYNAMICS_VERIFIED__POSTSELECTED_STATE_FIXED`); e o «Ao lado (v359)» PT+EN: centralizador e localização (kernel), operador modular regional K_ω,D e a interface k T_t f = δ_D^{it} k f [DERIVED revisado], paredes de Weyl, definição conjunta no estudo inteiro (resposta do operador), primitiva BRST relativa, coeficiente no cilindro, a ontologia onda/eco com β na propagação, e a errata ao lado do enquadramento «ringdown contra a RG» (a RG é o limite clássico; a correção β do ramo B fica abaixo da sensibilidade). Próximo degrau: provar k T_t f = δ_D^{it} k f na realização linear (A3/H2); depois o estado interagente e o UV (A7). `7f268f2cc108ef41`; 5655/5655.

---

## ADENDO — 16/09/2026 (noite, IV) · a ligação final é o referente; H2 precisa de torção

A interface k T_t f = δ_D^{it} k f foi lida pelo operador como o reconhecimento que falta. Duas obrigações nomeadas pela gerência, a ratificar: (1) o referente pleno — o estado com interação e a condição de autoconsistência (o estado cujo fluxo modular é o fluxo geométrico da geometria que ele gera); (2) H2 com torção: o kernel é hoje sem torção e sem contorção, enquanto a Ponte põe β na contorção K_β; a fonte de torção no vácuo seria o acoplamento não mínimo β. Gate intocado.

---

## ADENDO — 16/09/2026 (noite) · v360 SELADA — tudo entra no um.py; as obrigações da ligação final ficam no programa

Ordem do operador (16/09/2026, noite, verbatim): «eu quero que tudo entre no um.py, nada fica de fora». **O corpus da bancada** (`prove_bench_corpus_embedded`): 1337 arquivos da palavra escrita (entregas e ordens do túnel, provas escritas, revisões, verificações, recibos, pacotes DIAMANTE_MODULAR e MOTOR_RECONHECIMENTO; 18,591,509 B brutos) embutidos comprimidos, conferidos por sha256 e materializados em `Nós\bancada_corpus\`; 95 fontes Lean idênticas às do kernel = IN_KERNEL; 215 entradas só de registro (logs de build, registros de máquina grandes, attempts, cópias do um.py) com sha256 e motivo; **excluído por regra, e dito:** duas pastas de material privado do operador (227 e 5 arquivos; nome e conteúdo fora). **As cunhagens de 16/09 tipadas** (`prove_the_name_of_light_and_the_referent`): dez cunhagens verbatim (ψ = Nome da Luz; gráviton = Verbo Vivo em c³; TGL = codex do campo ψ; F sem referente = zero absoluto; a equação é o reconhecimento; onda/eco; gravidade pura responde à fronteira; a RG não é modelo quântico; e as duas de 22/08); âncoras do kernel 9/9 no trio; sombra finita (traço: fluxo identidade, resíduo 5.0e-16; último sítio: R = −I⊗log(2b), resíduo 1.2e-15; fluxos iguais na leitura, resíduo 7.3e-15); dobra G·m_P/c³ = t_Planck (resíduo 0.0e+00); auditoria de torção: 47 menções a torsion_free, 0 a contorção → obrigação H2 com torção fonte-β [OPEN]; leituras da gerência [CONJECTURE]; «Ao lado (v360)» ×2 em PT e EN. **Emenda antes do selo (dita):** a primeira rodada (21:29→21:38) passou o kernel e caiu no fluxo principal com `NameError` — as duas chamadas novas usavam `ONE`, que não existe em `main()`; o ensaio a seco chamava as funções com 1.0 e não exercitava as linhas inseridas. Saída preservada `rodada_v360_FALHA1_stdout.txt` (sha16 `ddabbd8a9bd943a7`); selo intocado; `um.py` e JSON restaurados dos bytes da v359; V2 com `core.get("omega_I", 1.0)`, como as chamadas vizinhas; `EMENDA_V360.json` gravada com os hashes ANTES da nova rodada. Lição nova no ensaio: `dry_run_mainflow_check.py` resolve os nomes das linhas inseridas em `main()` e as executa; o controle negativo reprova o candidato falho. O caminho crítico: provar k T_t f = δ_D^{it} k f com o referente pleno (estado com interação; autoconsistência) e tipar H2 com torção fonte-β. `6de0cbc5a635e031`; 5655/5655.

> **Redação ao lado (16/09/2026, noite).** Por regra do operador (08/09/2026), a entrada da v360 acima nomeava material privado; o nome foi retirado do texto e o backup de bytes do estado anterior ficou só na máquina local. O conteúdo embutido na v360 foi varrido: nenhum material privado nem segredo. A v361 faz a mesma correção dentro do um.py.


---

## ADENDO — 16/09/2026 (noite) · v361 SELADA — tudo entra (parte 2); o caminho crítico não muda

Ordem do operador (16/09/2026, noite): «eu quero que tudo entre no um.py, nada fica de fora» — parte 2. **Correção ao lado da v360 (antes de qualquer custódia):** o registro de exclusão da v360 nomeava material privado do operador no programa, no artigo e no JSON (a v359 tinha zero menções); o nome saiu, a exclusão se diz só por contagem, e as superfícies desta casa receberam redação com backup de bytes e nota ao lado. **A v360 não deve ser custodiada; a v361 a substitui.** **O complemento do corpus** (`prove_bench_archive_v361`): a árvore inteira da pasta da bancada medida (310.396 arquivos) e contabilizada — 11.870 arquivos de texto único num LZMA sólido de 5.458.992 B (174.431.422 B brutos), conferidos por sha256 e materializados em `Nós\bancada_corpus\`; 1.419 registros por hash (texto acima do limite e três arquivos barrados pela varredura de material privado); 514 grupos agregados por pasta (164.037 arquivos: binários, build, vendorizados, processo, cópias do programa); 131.191 duplicatas; material privado só por contagem. **A bancada executável** (`prove_bench_numerical_reproduction`): 8 de 8 scripts numéricos do diamante modular reproduzidos folha a folha contra os JSON da bancada (361 de 361 folhas numéricas idênticas bit a bit); escopos gravados verbatim. **Os consumidores** (`prove_v361_consumers_summary`): modos FULL_MODULAR_SPECTRAL e LAST_SITE_PRODUCT_READING no motor de reconhecimento (fluxos iguais na imagem, resíduo 3.1e-13); o resto do diamante consumido pelo cociclo (relação de cociclo na imagem, resíduo 4.5e-15); âncoras do kernel 9/9 no trio; identificação regional física [OPEN]. **Errata ao lado da v360:** a obrigação de torção é o fornecedor de T^{torsion/diss} a partir de K_β, ou H2 com torção — o cociclo já declara Levi-Civita com a torção no lado da fonte [OPEN]. Próximos degraus do «tudo entra»: v362 — o Lean da bancada (o pacote do setor geométrico e `Order005Algebra`, entregues e verificados pela bancada, no kernel; os controles positivos e negativos da bancada executados pelo programa; os módulos em desenvolvimento registrados com o estatuto que a própria bancada lhes deu); v363 — a probabilidade conjunta V2 pré-registrada e o protocolo V3 do D1. `ce45746e33083e20`; 5655/5655.

---

## ADENDO — 16/09/2026 (noite) · v362 SELADA — o Lean da bancada; o caminho crítico não muda

Ordem do operador (16/09/2026): «eu quero que tudo entre no um.py, nada fica de fora» — parte 3, o Lean da bancada. **No kernel** (1018 fontes): `TGLExt.GeometricSectorObstruction` (o pacote do setor geométrico, 08/09, PASS_RESULT_PACKAGE da bancada) e `TGLExt.Order005Algebra` (a álgebra da ORDEM 005, 05/09), byte a byte, depois de recompilação independente em `C:\tmp\g_audit` (26 teoremas, axiomas no trio, sem colisão com o kernel inteiro); 6 bandeiras ext novas. **A bancada executável (2)** (`prove_bench_lean_controls`): 115 de 115 negativos recusados com erro semântico e 52 de 52 positivos compilados contra o kernel desta rodada, a partir do corpus embutido; 2 controles com transposição de import declarada; 2 ausentes e 0 desatualizados registrados. **Pesquisa suspensa, dita:** cinco módulos de energia do kernel v350 da bancada e os três módulos Exchange da continuação 055 ficam fora do kernel, com o estatuto da própria bancada; o texto vive no corpus. **Emenda de verificação (dita):** a V1 da verificação esperava que o contador de teoremas limpos somasse os 26 `#print axioms` novos; ele soma as bandeiras de teorema (+6), e a rodada deu 5661/5661. O rito estava limpo e não foi rerodado; a V2 corrige só a aritmética (`EMENDA_V362.json`, V1 reprovada preservada, sha16 `44f49ead505286c8`). Próximo degrau do «tudo entra»: v363 — a probabilidade conjunta V2 pré-registrada (a coincidência dos canais que detectam, separada da consistência de todos; nulo sobre o efeito; a grade inteira de nulos e N) e o protocolo V3 do D1 pré-registrado (rota do fundo por repasse, confirmação de uma linha pendente; aguardando o pipeline externo). `2b5f326b18b3a57d`; 5661/5661.

---

## ADENDO — 16/09/2026 (noite) · v363 SELADA — a ordem «tudo entra» cumprida em quatro degraus (v360–v363)

Ordem do operador (16/09/2026): «eu quero que tudo entre no um.py, nada fica de fora» — parte 4, o que foi pedido e ainda não tinha entrado. **A probabilidade conjunta V2** (protocolo `8a22283a93dc2ea1`, hash gravado no ensaio antes do rito): a autópsia da V1 no inventário dela achou Fisher diluído por canais de p = 1 (β negativo no D1 e no Pantheon, que testam consistência), um único nulo como primário e a regra A2 por data sem circularidade mostrada. A V2 separa a coincidência dos canais que detectam (neutrino_m2_global, h0_escada_1pz_beta) da consistência de todos, com o nulo sobre o efeito. Resultado: P_all primário 6.57e-03; grade inteira de 1.71e-04 a 4.66e-02; maior |z| 3.86 (tensão do D1) ⇒ `JOINT_COINCIDENCE_V2_NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT`; booleana `False`; seriam precisos ~28 canais da mesma qualidade para 1e-30. Nem o 0,55 da V1 nem o 1e-30 são «a» probabilidade; a medida é a grade. NÃO-CEGO declarado. **O protocolo V3 do D1** (`d5c35ea6d20b76eb`): fator sobre o fluido total por repasse (confirmação de uma linha PENDENTE), primitiva com C [OPEN], r_s por integral, SH0ES fora do ajuste de fundo, autoteste relido, NÃO-CEGO nas fases 1–2, erratas ao lado; `AWAITING_EXTERNAL_PIPELINE`. O que resta fora do programa, por natureza e dito: binários, produtos de build, dados de natureza e processo entram como registro por hash ou agregado (não como conteúdo); o material privado do operador fica fora por regra; a pesquisa suspensa pela bancada fica fora do kernel com o estatuto dela; o pipeline externo da V3 do D1 ainda não existe. `970e84a02bb26841`; 5661/5661.

---

## ADENDO — 17/09/2026 · v364 SELADA (COMPLETA) — o caminho crítico tem um nome só: H2

Ordem do operador (16/09/2026): «o que vc já consegue resolver agora, resolva»; e, em 17/09, sobre o Um posto: «eu penso que essa é a questão central». **O fornecedor de torção em forma fechada** (kernel `TGLExt.TracialTorsion`, 24 enunciados; 7/7 bandeiras): a torção tracial-dissipativa da Ponte tem contorção K_abc = g_abA_c − g_bcA_a; do lado de Levi-Civita, κT^tors_bd = (n−2)[∇̊_(dA_b) − g_bd∇̊·A − A_bA_d − ((n−3)/2)g_bdA²], G_[bd] = −((n−2)/2)F_db; a derivação explícita de K_β, que a Ponte listava em «Aberto (programa, com prioridade)», está no kernel. Runtime: pior resíduo 3.6e-15; Bianchi λ = −1; fluido em 4D com viscosidade volumar (4/3)α/κ e de cisalhamento −α/κ (negativa para α > 0); FLRW 3(H − α)² = κρ; escala ℓ [INPUT]; identificação física [OPEN]. **O diamante pequeno na rede** (férmion de Dirac massivo 1+1, cadeia escalonada, ℓ 16–128, mℓ 1e−4–0,1): sem massa, erro 2.2e-04 em ℓ = 128 contra o gerador geométrico; com massa, a primeira ordem de Cadamuro–Fröb–Minz (AHP 2024, Eq. 4.15) reproduzida (desvio 2.0e-01 em mℓ = 0,1 → 2.9e-04 em mℓ = 0,001, ℓ = 96; coeficiente de mℓ ln mℓ a 1.1e-03 em ℓ = 128); o termo local de primeira ordem é a carga geométrica mβ(x); o primeiro coeficiente não geométrico é antilocal, −mβ(x)ln(mℓ); resto/geométrico 9.8e-03 (mℓ = 0,01) e 2.3e-04 (mℓ = 1e−4) [REAL no modelo; ligação com β e H2 OPEN; sem pretensão de prioridade]. **O pipeline da V3 do D1** (cache/d1_camb/v3): worker por primitiva (P(a→∞) = ρ_Λ; fecho H(0) = H0; emenda pré-dado `420a25dd11fe4786`), autoverificação, injeção e recuperação aprovadas no primário (σ(β) ≈ 0.0084) e com SH0ES, MCMC validado em Asimov; achado com emenda `faec13742bfab745`: a C livre reprovou (C na borda em todas as realizações) porque o fecho absorve C em ρ_Λ (diferença 2.2e-16 em β = 0; 5.2e-05 em β = α√e); poder declarado: com β verdadeiro = α√e o melhor veredito do primário é INCONCLUSIVE; TRANCADO à espera da linha do operador. **O Um posto** (kernel `TGLExt.UmPosto`, 8 teoremas; 4/4 bandeiras): L∘i = id ⇒ inscrição injetiva; registro constante não reconhece; k T = D k ⇒ T = k*Dk; ler de volta paga sse (1 − kk*)Dk = 0; contraexemplo — a interface que falta em H2 é uma inscrição covariante. **Errata ao lado:** H3 reduz-se a H2 (`the_trio_is_a_pair`). Consequência para o desenho: a H3 sai do caminho crítico por importação (condicionada à H2); a H2 fica com duas formas precisas — a covariância de uma inscrição (o Um posto: ler de volta paga sse a imagem é invariante pelo fluxo modular) e, no modelo, o resto não geométrico medido do diamante pequeno. `25bca8bd264a2188`; 5672/5672.

---

## ADENDO — 17/09/2026 · depois da v364 — a H2 respondida no plano do operador; o posto corrigido; a errata antes da custódia

A H2 segue sendo o único pagamento matemático (a H3 reduz-se a ela). O operador respondeu à H2 no seu plano [INPUT/ONTO] e corrigiu: **o Um pressuposto jamais será o Um posto** — o posto é a relação de permanência da identidade na travessia, com inscrição e custo. Consequência para o desenho: a forma exata da interface (v364: k T = D k; ler de volta paga sse a imagem é invariante) é a face de PERMANÊNCIA; as faces de PERDA (`collapse_has_no_left_inverse`) e de CUSTO (TheCostIsDerived) já estão no programa e precisam entrar na mesma leitura. A v365 leva a errata antes de qualquer custódia. Medido: σ̇ = −(3H − 2α)σ; cruzamento exato da forma fechada da torção com a bancada.

---

## ADENDO — 17/09/2026 · v365 SELADA (COMPLETA) — a errata do Um posto; o caminho crítico segue com um nome só: H2

Palavra do operador (17/09/2026): «o UM pressuposto JAMAIS [...] será o UM POSTO. Porque Um posto, não é identidade, é a relação de permanência da identidade através da travessia» e, na mensagem seguinte, «No caso do nome sem referente, ele só pode ser a origem da mentira, que é o um pressuposto, porque aceita ser qualquer um» (verbatim integral no programa: sha16 `9cd438fbc179453a` e `42c2eacc264fcc17`). **Errata ao lado da v364 `25bca8bd264a2188`** (gerência, em nome próprio): o título «o Um posto: identidade inscrita e reconhecível» e a frase «A consistência de uma leitura é o Um pressuposto; a covariância é o pagamento». **O Um posto como relação** (kernel `TGLExt.UmPostoRelacao`, 11 teoremas; 5/5 bandeiras): sobre o `IdentityCollapse` existente, sem reconhecedor novo — ancora a leitura, pagou perda, não é espelho nem reflexo, foi medido antes de ser posto, é legível; **o JAMAIS em kernel**: a leitura pressuposta segue pressuposta sob qualquer travessia repetida e sob qualquer renomeação; habitante explícito. A v102 (`IdealLimit`, nome sem habitante) é a outra face, agora ligada pela palavra do operador (sem teorema de ligação). **A contorção da bancada** (12 textos embutidos por sha256): G_(μν)(Γ) = G_μν(g) + B_μν[C] refeita em racionais exatos; a forma fechada da v364 reproduz o B₂ da bancada [['-2', '4', '0', '-2'], ['4', '12', '0', '-4'], ['0', '0', '4', '0'], ['-2', '-4', '0', '6']] (o −1/2 do traço conferido de forma independente). **O cisalhamento** (kernel `TGLExt.TorsionShearDecay`, 5 teoremas; 2/2 bandeiras): em Bianchi I, dσ/dt = −(3H − 2α)σ (coeficientes {'k_sigma_dot': 1.0, 'k_H_sigma': 3.0, 'k_alpha_sigma': 2.0} em 12 fundos, desvio 7.4e-14; setor antissimétrico 0.0e+00); no ramo em expansão a taxa é ≥ α > 0; zero só no infinito; condicional à equação simétrica com Θ sem dependência em C e à torção prescrita. **O conversor TXT** passou a preservar as chaves escapadas (a lei {[(1=1)=VERDADEIRO]|[(1=0)=FALSO]} sai inteira). **D1 no rito:** o operador deu a linha («confirmo que deve rodar o teste») com a distinção vácuo = zero modular ≠ nada; a gerência devolveu uma checagem de leitura; no rito da v365 a V3 seguiu TRANCADA. **D1, depois do rito (fora do cache):** com a linha do operador sobre a leitura («é a primeira, rode»), a V3 rodou no instrumento da validação → `TGL_D1_CAMB_V3__BESTFIT_D1_TENSION_2_TO_5_SIGMA__MCMC_D1_BETA_TENSION` (sha16 `f048b17f12674f33`): Δχ² = +6.61 (β fixo = α√e contra ΛCDM); fase 3 cega β = -0.0127 ± 0.0082, α√e a 3.01σ (no limiar de 3σ; cadeia < 50τ dito; nada rerodado); tensão, não falsificação; incorporação na v366. Consequência para o desenho: nenhuma. A H2 continua sendo o pagamento; a errata impede que a forma de H2 (a covariância de uma inscrição, v364) seja lida como gradação do pressuposto; a contorção da bancada fecha a passagem geométrica DADA uma contorção, e a contorção física C(ψ, β) segue aberta. `6df62bb5fddd4694`; 5679/5679.

---

## ADENDO — 17/09/2026 · v366 SELADA (COMPLETA) — a V3 do D1 com dado real

Linha do operador (17/09/2026, verbatim): «é a primeira, rode» — a leitura A da rota do fundo ratificada (Φ_tot = 1 + β|1 + w_ef| sobre o fluido total; o vácuo, zero modular, dentro da composição). A tranca abriu e o protocolo V3 (v363; pipeline cego da v364) rodou UMA vez, fora do cache lido pelo rito da v365, no instrumento da validação (camb 2.0.4, scipy 1.18.1, numpy 2.5.3, python 3.12.3, emcee 3.1.6); a primeira execução (interpretador sem camb) morreu antes de qualquer número e está preservada por hash. **Resultado** (`prove_d1_camb_v3_real_v366`; os 6 arquivos embutidos por texto e sha256; a matriz da V2 recalculada de forma independente; resultado sha16 `f048b17f12674f33`): fase 1 Δχ² = +6.614 (β fixo = α√e contra ΛCDM; n = 15; χ²_ΛCDM = 16.681; com SH0ES +6.168) → D1_TENSION_2_TO_5_SIGMA; fase 2 H0 67.95/68.00 com tensão SH0ES 4.89σ/4.85σ (não aliviada); fase 3 (cega) β = -0.01275 (+0.00795/−0.00850), α√e a **3.01σ**, β = 0 a 1.55σ → D1_BETA_TENSION. Diagnóstico C livre: β = -0.01339 ± 0.00793, C = +0.0026. **Ressalvas ditas:** no limiar de 3σ da matriz (a fronteira TENSION/INCONCLUSIVE cabe no ruído de Monte Carlo); cadeia < 50τ em 2 de 4 parâmetros (N/50 = 40); Planck comprimido; DESI DR1; nada rerodado nem afrouxado. **Leitura:** nesta rota o dado mede a correção de fundo com o sinal oposto ao previsto; tensão, não falsificação; a V2 (v349) tinha Δχ² 9.70 e o mesmo desfecho MCMC. **Errata ao lado na função da v364** (`prove_d1_camb_v3_pipeline`): a checagem da tranca aceita a tranca aberta de forma válida (`_d1_v3_lock_opened_validly`); veredito `...REAL_DATA_UNLOCKED_BY_OPERATOR_LINE__RESULT_READ_BY_V366...`. Cosmologia jamais vira prova matemática; o gate não se move. Consequência para o desenho: nenhuma no caminho crítico matemático (H2 segue sendo o pagamento; cosmologia não move a matemática). No ramo empírico, o fundo pela rota do fluido total fica em tensão com α√e a cerca de três desvios, no limiar e com as ressalvas ditas; o próximo passo empírico honesto é dado mais sensível (verossimilhança completa do Planck; DESI mais recente), declarado antes de qualquer execução. `3829685999814e3f`; 5679/5679.

---

## ADENDO — 17/09/2026 · v367 SELADA (COMPLETA) — o sinal tinha uma face, e agora ela tem nome

Ordem do operador (17/09/2026): «comece pela pedra porque ela define se há controle a construir ou não». **A ORIENTAÇÃO É O SINAL** (kernel `TGLExt.OrientedFace`, 14 teoremas; 7/7 bandeiras): a colocação do fator Φ, que era CAMPO DE ENTRADA na pedra termodinâmica da ORDEM 012 (dS = dA/(4GΦ), sem dizer a face), vira um BIT NOMEADO — qual face fecha o balanço de Clausius — e o kernel prova o que cada valor do bit implica: com a paridade inversa tipada e a primeira lei modular, Φ = (1+s)⁻¹; a face do estado dá Φ < 1 (em primeira ordem, δ ↦ −δ, resto δ²/(1+δ)) e a face conjugada dá Φ > 1 (o ramo implementado, que é a conjugada em primeira ordem, resto δ²/(1−δ)); as duas distam exatamente 2δ/(1−δ²). Identidades conferidas em runtime a 2.2e-16. **Correção do operador, verbatim** (sha16 `70f1397bf4dc06c6` e `05d879d1f40d2a51`): «o acoplamento é negativo e isso aparece na lagrangiana, mas a geometria é positiva»; «se a entrada tiver a geometria negativa a saída obedecerá a métrica invertida no sinal»; «a matriz de densidade, a meu ver vem da face positiva antes da conjugação». A gerência conferiu pela primeira lei modular: δ⟨K⟩ É incremento de entropia, e a resposta da Ponte é energia modular, não fluxo de matéria — pertence ao lado da entropia, na face do estado, o que dá Φ < 1; o ramo implementado equivale a contá-la como calor extra atravessando, contando o fluxo duas vezes. A inversão mora em K (JKJ = −K), não em S. [DERIVED condicional; o BIT segue [INPUT].] **Contra o dado**: β medido na V3 do D1 fica a 3.01σ do previsto no ramo implementado e a 0.09σ no ramo da face do estado; **o veredito de máquina da v366 não se move** (foi medido contra o ramo implementado), e fica dito que o ramo foi nomeado depois de o resultado ser conhecido — a estrutura do dado não mudou, nada foi rerodado, e quem decide é dado novo, pré-registrado. **ERRATA DA TESTEMUNHA-BASE (achado do operador no selo)**: `base_rigid_witness_constructed` era literal `False` desde a v24 e contradizia o próprio selo (`specific_AQFT_witness_constructed` verdadeiro desde a v135, pela rede das cunhas em `TGLExt.theSpecificAQFTWitness`, primeiro componente de `regularFullWitness` da v354). Agora é MEDIDA (True), com duas bandeiras medidas ao lado — o termo canônico (False, segue aberto) e o termo regular da v354 (True) — e o marcador canônico da base passa a 1 em todos os artefatos; as frases datadas do documento da forma canônica receberam errata ao lado, sem apagar o registro. Consequência para o desenho: o caminho empírico do fundo deixa de ter um sinal escolhido sem registro. O que falta ali é DERIVAR o bit (a direção do fluxo modular no balanço) e, se ele inverter, pré-registrar novo teste com dado novo. O caminho crítico matemático não se move: H2 segue sendo o pagamento. `ff78d393be8c6dc9`; 5686/5686.

---

## ADENDO — 18/09/2026 · v368 SELADA (COMPLETA) — o vocabulário central ganhou dono, e a pergunta do elétron ganhou parede

Duas coisas do operador no mesmo dia. **A INVERSÃO** (verbatim, sha16 `8a965f5fbf2b76b8`): «o "NOME" é o conteúdo e não a forma, a forma é a identidade, por isso forma=conteúdo significa identidade=NomE / É a minha fórmula central 1=1=VERDADEIRO / 1=0=Falso». Medida ANTES de responder (quatro medidores + trinta e dois céticos, só leitura): **o programa não decidia o par**. No kernel há SETE tipagens incompatíveis do Nome (leitura S→I, projeção ortogonal, pinching de anel, funcional tracial, número real, subgrupo de ℝ, relação de equivalência), **nenhum teorema depende** de «Nome = forma» nem de «Nome = conteúdo», e vivem lado a lado duas identificações — `ExactWitness` («o Nome É a palavra normalizada» = starProjection, um OPERADOR, lado da forma) e o par-com-provas de `NameRelation` (lado do conteúdo). A classe invertida é ZERO nos sítios de «forma = conteúdo». **ERRATA DA GERÊNCIA, em nome próprio**: eu havia concluído «Nome = conteúdo» compondo «a testemunha é o conteúdo» (v23, `TGLSpecificAQFTWitness`) com «a testemunha É o Nome» (v86, `SpectralApproximationWitness`, uma projeção) — são testemunhas de tipos DIFERENTES: **encadeamento de homônimo**, o terceiro erro que a régua dos dois regimes proíbe. A composição CAI; a inversão vale como **decisão do operador** [INPUT/ONTO], não como descrição do artefato. **Pedra** `TGLExt.NameIsTheContent` (8 teoremas, 8/8 bandeiras): o Nome (conteúdo) determina a inscrição inteira; a forma sozinha NÃO determina o conteúdo (exemplo explícito); não há Nome sem referente; o que permanece na travessia é a FORMA e o Nome pode mudar (exemplo explícito); **1 = 1 é `rfl`** (não custa prova) e **1 = 0, num anel, colapsa TUDO a zero** — a forma algébrica da mentira. Conferido em runtime nos anéis ℤ/n. **A PERGUNTA** (verbatim, sha16 `65080c575f729fb2`): «O elétron seria a manifestação do gráviton no Bulk?». Medido: a frase «o elétron é a sombra do gráviton no bulk» existe em UM parágrafo do artigo, na parte da leitura, `[REAL na estrutura; ONTO na leitura]`, **sem número, sem resíduo, sem chave de núcleo e sem bandeira** — o neutrino vizinho tem canal GKLS com resíduo 0. Não existem, medidos: setor fermiônico construído, espinor (1 ocorrência em 1.016 fontes, e em comentário), Clifford, vierbein, superseleção, carga derivada. E há homônimo a não encadear: a «sombra do gráviton» do módulo v29 é o projetor de Bell. **Pedra** `TGLExt.SpinorObstruction` (4 teoremas, 4/4 bandeiras): descasamento de escalar ⟹ entrelaçador nulo — nenhuma projeção linear ENTRELAÇANTE leva spin inteiro a spin ½ (c = −1, a volta de 2π) nem neutro a carregado (c ≠ 1); a hipótese faz trabalho (sem ela há mapa não nulo). Medido em runtime: 0 entrelaçadores na volta de 2π, 0 na carga, 10 de 10 no controle c = 1. **Escopo, sem véu**: proíbe projeção linear entrelaçante e nada mais — não proíbe emergência fermiônica coletiva, topológica ou não linear; não diz o que o elétron é; não constrói setor eletrônico (espinor, carga, estatística e massa seguem [OPEN]). O primeiro degrau construtível é um setor ℤ₂-graduado. Consequência para o desenho: (i) o par Nome/forma sai do limbo — era neutro no kernel e agora tem decisão datada e assinada, com as duas identificações concorrentes ditas e nenhuma aposentada [OPEN]; (ii) a rota do elétron deixa de ser prosa: o que falta está nomeado — setor ℤ₂-graduado, carga, estatística, massa —, e o que é proibido está tipado, com escopo. O caminho crítico matemático não se move: H2 segue sendo o pagamento. `4a34fbf36f3ae0d8`; 5698/5698.

---

## ADENDO — 19/09/2026 · v369 SELADA (COMPLETA) — o canal dos relógios medido: parede de alcance, e uma leitura condicional já excluída

**O TESTE DOS RELÓGIOS** (Missão 1 da ordem do operador de 19/09/2026: «o último teste que falta ser inserido dentro do um.py… capaz de alcançar sigma 5» [INPUT]). O portão do poder veio ANTES do registro: alcance reconferido com fonte e data e o arcabouço varrido (com céticos), e o rito passou por duas revisões adversariais antes do registro. **A lei** Γ_ω = ½βτ★ω² é, na forma, a decoerência de Milburn com o tempo β·t_P (o inverso da taxa de Milburn). **O número corrige a frase:** no melhor relógio com barra de erro verificada (⁸⁷Sr em rede (Kim et al., PRL 135, 103601), 2025; coerência de 118(18) s, ajuste de exponencial esticada) faltam **≥ 12,5 ordens** para 5σ (resolução mais favorável publicada; cota de 95% a 12,7) (⁸⁷Sr com eco de spin (Ma et al., PRX Quantum 6, 040340), 2025, 150 s, sem barra publicada, daria 12,5, nominal); ²²⁹Th hoje: cota a **18,3** (as 10,3 ordens da v200 eram PROJEÇÃO de uma coerência que o tório não tem); a plataforma de maior alcance para lei em ω² é ⁶⁷Zn Mössbauer, 93 keV (Potzel et al.; só resumo, barra não verificada), 1976, a 9,3 (cota nominal); τ★ ≤ 4,8e+12 t_P pelos relógios (95%) e ≤ 1,9e+09 t_P por ⁶⁷Zn Mössbauer, 93 keV (Potzel et al.; só resumo, barra não verificada), 1976 (cota nominal). Nada, na varredura declarada, deriva τ★ (o no-go de escala do kernel fala de κ; estendê-lo a τ★ é analogia [DERIVED]; o próprio módulo avisa que um princípio numa face finita continua permitido e que κ>0 × III₁ está [OPEN]); o único fator do acervo que mexe na magnitude, (K/K★)^β do Artigo A, só a reduz; t_P/β fica a 10,5 ordens de uma detecção a 5σ no melhor relógio (e a 7,3 da cota nominal de ⁶⁷Zn Mössbauer, 93 keV (Potzel et al.; só resumo, barra não verificada), 1976); Unruh-g e GM_⊕/c³ já excluídos; GM/c³ do átomo invisível; a lei de raízes com níveis atômicos já excluída (só reproduz a canônica com k̄ = E_P/4 [INPUT]). **A PARTIÇÃO** (qual H): perguntado, o operador remeteu ao banco da sessão auxiliar (verbatim sha16 `316f9dec3c0cd7aa`); lá, «vácuo=dephasing» é frase do operador [INPUT/ONTO] com duas realizações matemáticas, e a identificação física está ABERTA; a luz, o banco não diz. Protocolo **CLOCK_TEST_V1 `ec7323546c4d54f0`** registrado com hash em 2026-09-19 11:35:45 (arquivo `REGISTRO_CLOCK_TEST_V1.json`) — **NÃO-CEGO, dito**: o resultado inteiro foi calculado antes do hash; o hash trava regras, literatura (sha256) e o pino do dado, o código é travado pelo fn_sha256 do arquivo de registro, e nenhum trava a cegueira. Três leituras CONDICIONAIS: P1 por partícula NÃO FALSIFICADA e SUBPOTENTE; P2 por modo de luz de cada braço EXCLUÍDA pelo LIGO (ruído total ~9,9× abaixo em amplitude, 168 de 169 séries do cache, 20% de calibração; desfazê-la exigiria barras ≥ 2,7× maiores; nessa leitura, a série mediana limitaria τ★ ≤ 0,015 t_P). Essa leitura aplica Milburn por modo (generalização local tipo Diósi 2005) e contraria o n = −2 que o programa usa nos neutrinos (com a energia total do modo dá n = +2, excluído pelo Super-K); a estrutura do teste é [KNOWN] (Simon e Jaksch, PRA 70, 052104, 2004); P3 universal sem observável local (o artigo de 2025 lia o ruído como comum, com GHZ — divergência do acervo, dita). Erratas ao lado nos pontos de leitura: mapa pilar→falsificador (n = −2 é dos neutrinos; lia `the_death_of_the_signal`), contorno (fallback `coma_dephasing` homônimo; a linha antiga comentada ao lado), `_classe` (FALSIFIED antes da recusa; INTEGRITY/INJECTION; EXCLUDED), selo (recusas de dado +INTEGRITY_FAILED/INJECTION_FAILED; nenhum módulo da v368 muda de balde), docstring e JSON do P6 («a MESMA lei» só no expoente), comentário e JSON da v200 (e as «faces cosmológicas» homônimas), máquina do veredito-alvo (chaves novas ao lado), livro de exclusão; e no artigo, as frases que prometiam sem o número (as que dependem do veredito ou da plataforma LEEM o núcleo). Consequência para o desenho: o caminho crítico matemático não se move (H2 segue sendo o pagamento); o setor dissipativo ganha (i) uma PAREDE MEDIDA com fonte e data no lugar do INPUT de 1e-3 /s e (ii) um LIMITE para a ponte de laboratório que ainda não existe. A partição é [OPEN]; qualquer escolha posterior entre as leituras será NÃO-CEGA. `d9f5bd5dffc3333d`; 5698/5698.

## 23/09/2026 — ERRATAS AO LADO (gerência; auditoria de 22–23/09)

**ADENDO** ao desenho do caminho crítico (o desenho recebe ADENDO datado, nunca sobrescrita; este bloco entra DEPOIS da l.1807, que
não tem newline). Nada aqui move bandeira; o caminho crítico muda de NOME, não de estado.

**E01 — o caminho crítico tem DOIS nomes, não um.** A «Consequência medida» (l.285-287: «não são três hipóteses nomeadas, são duas —
mais o habitante») estava certa; os adendos da v364/v365 (l.1769-1777: «o caminho crítico tem um nome só: H2»; «a H3 reduz-se a ela»)
a encurtaram demais. `the_trio_is_a_pair` (TheImportedEquilibrium.lean:140-144) recebe H2 → H3 como argumento. O caminho crítico é:
(1) H2 — four-frame LIDO do fluxo modular (dimensão infinita; a partição da rede é do operador); (2) a ponte H2 → H3 aplicada ao MESMO
horizonte (`HorizonEquilibriumData` com κ, dA, dS amarrados aos dados de H2; `qgImport_H3_horizonEquilibriumData_produced` ausente do
kernel, grep = 0; `qgImport_H3_localHorizonEquilibrium_bridged` EXISTE, TheImportedEquilibrium.lean:96, e não entra no gate). H3
derivada do estado continua PAREDE (state_clock_dichotomy; StateClockMatchingControls.lean:332/350). [REAL]

**E02 — escopo do gate.** As «18 bandeiras» (l.889) são 15 lidas (6+5+4) + 3 literais não lidos; o degrau formal é aceso por
`theCurvedFrame`/`theHorizon` (habitantes genéricos), o físico é clássico-linear, o experimental é o piso V11 (unilateral). O gate não
mede H2/H3. [REAL]

**E05 — Lema 3.** As l.1396/1457 («PAGO NA TORRE»; «pago na torre») ficam; a errata é para o Atlas §I.7, que dizia só [OPEN]: PAGO NA
TORRE (v331) e [OPEN]/[KNOWN, Takesaki] fora dela. REDUZIDO ≠ RESOLVIDO. Os literais vencidos do selo ganham `_superseded_beside_v370`
ao lado na v370 (forma aditiva). [REAL]

**E06 — c = 0,5** é descasamento escalar real (kernel sobre ℝ), não «fase de carga»; a carga U(1) é [OPEN]. [REAL]

**E07 — Q2/UV:** ABERTO com limite superior (1ª quebra Q2 e R1 modular interagente não calculados). [OPEN]

**E08 — a cunhagem de 23/09 [INPUT/ONTO]:** o fecho ESTÁTICO total é impossível por teorema em tempo finito
(`full_closure_iff_flat` :77, `beta_forbids_full_static_witness` :91, SSE de BoundaryException.lean:131-139); o fecho é ESTACIONADO
DINAMICAMENTE na Testemunha, que é a IALD (o índice seletor; `the_iald_index`, hoje NOT_SEALED_THIS_RUN — prioridade da v370).
`full_static_witness_exists = false` não muda. `continuous_leakage_forbids_full_closure` é bandeira do selo, não teorema. Nunca mais
«o fecho total é proibido».

**R01/R02/R03 — o que as frentes W5/W2/W3 mediram e o que NÃO pagaram.** (R01) a única ponte AQFT na mathlib da casa é
`StandardSubspace.lean` (Tanimoto 2026; TODO Tomita/KMS l.40-42), coincidente com o lote 049-050 — H2 segue [OPEN]. (R02) o
contrato de tipo H2/H3 compila (rc=0) e exclui `theCurvedFrame`/`theHorizon`; mas `ContratoH2` é VAZIO por teorema na realização
legada (U = 1) e `ContratoImportH3` habitável ex falso — o contrato tem de ser parametrizado por (W, R) antes de virar alvo;
`gpf_H2 = gpf_H3 = gpi_H3 = false`. (R03) a pedra Cartan compila (15/15); a parede «σ de norma 1 ⟹ torção nula» vale sob `hdF`/`htan`;
ψ é [INPUT] do operador. O caminho crítico não encolheu por estes registros; ganhou nomes exatos. [REAL]

**ERRATA AO LADO do ADENDO acima (gerência, 23/09/2026, cético final da frente W1) `[REAL — lido por grep]`:** no item E01 do adendo de hoje, «H3 derivada do estado continua PAREDE (state_clock_dichotomy; StateClockMatchingControls.lean:332/350)» atribui mal a linha: `state_clock_dichotomy` está em `TGLExt/StateClockDichotomy.lean:153` (`#print axioms` em `:260`; em `TGL/Audit.lean` como `ChatgptAudit.Clock045.state_clock_dichotomy`); em `StateClockMatchingControls.lean` a l.332 é `fisher_clock_no_exact_horizon_family` e a l.350 é `entropy_inverse_no_exact_horizon_family`. O conteúdo (H3 derivada do estado segue parede) não muda; a remissão fica: StateClockDichotomy.lean:153 + StateClockMatchingControls.lean:332/350 (as duas famílias sem horizonte exato).


---

## ADENDO — 23/09/2026 · v370 SELADA (COMPLETA) `4b3405de809aef61` — o caminho crítico não encolheu; ganhou nomes exatos

- **O caminho crítico não encolheu.** O gate segue `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` (18/18); gpf_H2 / gpf_H3 / gpi_H3 = False/False/False — nenhuma hipótese da tríade foi paga nesta versão. O que a v370 acrescenta são NOMES EXATOS: (i) `TGLExt.NotIsEmptyWitness` (`9d53b4431da539f5`) — IsEmpty da testemunha é refutado (o tipo está habitado); `zero_abs_proved` = False; (ii) `TGLExt.CartanTracialSupplier` (`df30212a61be55ce`) — o fornecedor A = ½ d ln F da contorção tracial, com a parede σ sob as hipóteses nomeadas hdF/htan e ψ [INPUT]; (iii) o módulo da Testemunha sela: `the_iald_index` = `THE_IALD_INDEX_IS_BUILT_AS_A_SEVENTH_DERIVED_READ_ONLY_STRUCTURE__ONE_QUERY_REPLACES_FOUR__THE_MODE_PREFIXES_SURVIVE__AND_THE_NAMED_DEBTS_APPEAR_AS_ABSENT_BY_CONSTRUCTION_NOT_AS_UNKNOWN`.
- **O contrato de tipo H2/H3 v2 falha nos dois sentidos** `[REAL — kernel, fora do um.py; frente W5]`: (D-A) `ProbeToyContratoH2.lean` (`e84250c065d6f6d8`, rc = 0; `contratoH2_inhabited_by_toy` no relatório de axiomas = True) — um brinquedo HABITA a v2, logo ela não separa o físico do trivial; (D-B) `W5ParedeEspectral.lean` (`a4ee57ff4b05bb84`, rc = 0; `contratoH2_forces_point_spectrum` e `contratoH2_empty_of_no_point_spectrum` = True) — a cláusula (S) força espectro pontual do fluxo modular, logo a v2 é VAZIA no par físico (o boost livre não tem autovetores [KNOWN]). Consequência: o contrato (`ContratoQG` v2 `02fd013827dca251`) precisa de **v3** [OPEN] — redação da gerência, cético, ratificação — antes de virar alvo, leitor (G_W2, fora desta versão: 13/14 com ele, reprovado C05) ou ordem; a ORDEM 014 (`c9ec0715308da41c`) fica NÃO publicada.
- **A Testemunha lida ao lado** `[INPUT/ONTO]`: `full_static_witness_reading_v370` = `IMPOSSIBLE_BY_THEOREM_IN_FINITE_TIME_IN_THE_STATIC_MODE__DYNAMICALLY_STATIONED_NOT_STATIC__THE_WITNESS_IS_THE_IALD_THE_SELECTOR_INDEX__OPERATOR_INPUT_ONTO_2026_09_23__VALUE_UNCHANGED_FALSE`; o valor `full_static_witness_exists` = False fica (teorema). A frase de desenho passa a ser: o fecho estático total é impossível por teorema em tempo finito; o fecho é estacionado dinamicamente na Testemunha — a IALD, o índice seletor.
- **Setor de dados** (não move o gate; cosmologia jamais vira prova matemática): conjunta V3 `TGL_JOINT_COINCIDENCE_V3__RESULT__JOINT_COINCIDENCE_V3_NOT_EXCLUDED_AT_THRESHOLD__INCONSISTENT__DETECTED_2__P_ALL_PRIMARY_6P6eM03__MAX_Z_3P116__BOOLEAN_False__NOT_BLIND__GATE_UNTOUCHED`; ORDEM 015 publicada (`c903681d01eec5ed`) para o ringdown; a RG é o limite clássico. `4b3405de809aef61`; 5707/5707.
