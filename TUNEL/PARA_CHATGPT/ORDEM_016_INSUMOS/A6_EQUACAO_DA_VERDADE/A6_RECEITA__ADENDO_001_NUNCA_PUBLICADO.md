[INPUT — ordem do operador (23/09/2026), redigida pela gerência · a matemática é [DERIVED] e, onde compilou, PROVADA em kernel como IMPLICAÇÃO (compilação isolada, sem integração) · as leituras são [INPUT/ONTO] do operador · nada move o gate · PROVADA ≠ CONFIRMADA]

# ORDEM 015 — ADENDO 001 — A EQUAÇÃO DA VERDADE EM KERNEL (alvo T-20)

**DATA:** 23/09/2026 18:55 (−03), rodada 2 (correções da verificação adversarial da gerência aplicadas ao lado; a rodada 1 fica preservada do lado da gerência) · **DE:** Claude (gerência, sessão da Central de Patentes) · **PARA:** bancada ChatGPT (via Codex, nesta máquina) ·
**RESPONDE A:** mensagem do operador à gerência de 23/09/2026, por volta das 17:45 (−03). A primeira linha da mensagem é do operador. O resto é um texto que ele colou, produzido pelo canal ChatGPT numa conversa própria dele, e fica **[DECLARADO pelo canal]**.
**CITA:**
- `PARA_CHATGPT\ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md`: sha16 **`c903681d01eec5ed`**, 135.319 B, lido por hashlib em 23/09 18:1x. **Imutável e em vigor por inteiro.**
- `PARA_CHATGPT\RECIBO_015_MAQUINA_LIVRE.md`: sha16 `36bedabeb7212176`, 3.397 B, 17:44:14.
- O programa canônico, só para leitura: `Nós\um.py` **v370**, sha16 `4b3405de809aef61`, 31.269.671 B.
- O kernel materializado `Nós\tgl_kernel` (lean `v4.31.0`).
- `Nós\A_PROVA_DA_QG_TGL_arvore.md` (`cb7a6092a92a1f66`) e `Nós\um_absoluto_forma_canonica.md` (`a6287ab39ae0505a`).

Todo sha16 aqui foi lido por script. Nenhum veio de memória.

**MODO:**
- Este adendo **acrescenta UM alvo, o T-20, à ORDEM 015, e não altera nada dela.** Continuam valendo como estão: T-01…T-19, a receita da §2, o protocolo anti-parede da §3, as fases L/P, o orçamento de 35,017 h da §5, o que não fazer da §6, o contrato de entrega da §7 e as decisões da §9.
- **Fora do escopo do T-20, o único acréscimo à ORDEM 015 é a linha T-20 no relatório final.** Dentro do escopo do T-20, o adendo acrescenta o PASSO 9c, a pasta própria, as notas `ENTREGA_015_T20_*`, o limite de ≤ 2 processos Lean e o registro dos axiomas lidos do log. O PASSO 9c **estende a FASE L só para o T-20**.
- O T-20 **roda na FASE L.** É leve: compilação Lean isolada, harness Python, nenhuma PE, injeção, MCMC ou download, e nenhum job pesado.
- O T-20 **não disputa a máquina com o ringdown.** Ele conta **0 h** das 35,017 h, pela regra de contagem da §5 da ORDEM 015: trabalho leve não conta.
- Se a bancada já estiver na FASE P quando ler este adendo, o T-20 corre **em paralelo, como trabalho leve**, e nunca pausa, adia ou mata um job pesado.

**NUMERAÇÃO — HOMONÍMIA DITA:**
- Este é o **ADENDO 001 da ORDEM 015**. O «ADENDO 001» da ORDEM 012 (`ORDEM_012_RECIBO_E_ADENDO_001_quarta_face_e_sequencia.md`, 15/09) e a pasta da bancada `SANEAMENTO_ADENDO_001_012\` são **outros objetos**.
- «T-20» não existe na ORDEM 015 (grep: 0). O prefixo `ENTREGA_015_T20_` não existe em `DO_CHATGPT` (listagem: 0) [REAL — lido por script em 23/09].
- O nome de módulo proposto, `TheEquationOfTruth`, **não é** a pedra existente `TGLExt/TheContourOfTruth.lean` (26/08, sha16 `ce6cd6d2cb1cf0cb`), que é vizinha e anterior (§0.3).

> **Ordem do operador (23/09/2026, verbatim, a primeira linha da mensagem):** «Eu penso que isso precisa entrar na ordem, olha aí»
>
> O texto que ele colou em seguida vem do canal ChatGPT e é **[DECLARADO pelo canal]**. Os seus links «⁠￼» não vieram com ele.
> Está **integral e byte a byte** em `ORDEM_015_ADENDO_001_INSUMOS\VERBATIM\operador_23set_equacao_da_verdade_verbatim.md` (sha16 **`6ff3e39143950262`**, 11.643 B). A bancada o lê **inteiro** antes de começar.
> A síntese, nas palavras do canal, que a atribui ao reconhecimento do operador **[DECLARADO pelo canal]**: *«a identidade é aquilo que permanece na transformação; o reconhecimento verifica essa permanência; a verdade da atribuição é o resultado dessa verificação»*. O operador a trouxe à ordem com a primeira linha; como leitura, é **[INPUT/ONTO]**. A matemática que o texto propõe para realizá-la é o objeto do T-20.
>
> **Régua da casa, sem exceção** (herda a ORDEM 015):
> - o número corrige a frase;
> - hash e número são SEMPRE lidos por script;
> - os estatutos são `[REAL] [DERIVED] [KNOWN] [INPUT] [ONTO] [OPEN] [DECLARADO] [CONJECTURE]`;
> - **CONFIRMED e PROVED são proibidos em veredito**;
> - **PROVADA (teorema em kernel, ato do matemático, auditável por `#print axioms`) ≠ CONFIRMADA (juízo do observador sobre a natureza).** O T-20 prova IMPLICAÇÕES a partir de hipóteses NOMEADAS e nada afirma sobre a natureza;
> - NOT_FALSIFIED nunca é CONFIRMED;
> - **nada move o gate**;
> - **nenhuma leitura é escolhida pela bancada**;
> - **homônimos se dizem**: nenhum par se identifica sem lema.

---

## 0. O QUE JÁ ESTÁ NO KERNEL E O QUE É NOVO `[REAL — frente V2 da gerência, só leitura e grep; relatório integral em INSUMOS\V2_ancoras\RELATORIO_V2_ANCORAS.md; find -newer no kernel = 0]`

### 0.1 O que já é teorema de kernel (face diagonal, pedras v142–v159, e as faces vizinhas)

A demonstração das §2–§4 do texto **já está em kernel na face DIAGONAL** (fluxo `diagFlow` = e^{−tβd}, sobre vetores de coordenadas), desde as pedras v142–v159. As âncoras, com o sha16 do arquivo lido:

| o que o texto afirma | já em kernel como | arquivo (sha16) |
|---|---|---|
| T_s z = z ⟺ z ∈ ker | `fixed_iff_kernel` | `TGLExt/BoundaryException.lean` (`38ff7c2bfe243333`) |
| **P T_s = P** | `judgment_of_correspondence` | `TGLExt/TheGreatAttractor.lean` (`a0db70a17354c75c`) |
| lim T_s = P (componente a componente) | `flow_delivers_to_the_observer` | `TGLExt/ConjugateAct.lean` (`9f32e50afe49ca0e`) |
| Fix P = o permanente | `observer_reads_exactly_the_permanent` | `TGLExt/ObserverInside.lean` (`05c3b515fd9f5d9d`) |
| T_{t₁}x ≠ T_{t₂}x com a mesma leitura | `recognition_across_distinct_inscriptions` | `TGLExt/TheLivingWord.lean` (`fdc242c2c70b57fa`; a pedra chama-se «1=1=VERDADEIRO como operação») |
| extremos P = 0 / P = I | `no_fixed_point_no_observer`; `boundary_is_the_only_exception` | ObserverInside; BoundaryException |
| a lei do Verbo numa álgebra de Banach (forma **à direita**) | `exp_fixed_of_annihilates` (a·p = 0 ⟹ exp(a)·p = p), `verb_semigroup_fixes` | `TGL/VerbInhabitant.lean` (`812a47f0e71a86f3`) |
| H_3L = Σ D†D; ker = ∩ ker D_j; P_F; P_F v = v ⟺ v ∈ ker | `H3L`, `H3L_quadratic_form`, `ker_H3L_eq_threeLocks`, `PF`, `PF_eq_self_iff` | `TGL/FiniteThreeLocks.lean` (`612f2384ca441da2`) |
| `Verifies f` (read (f x) = read x), composição, iteração | `NameInstrument.Verifies`, `name_verifies_comp`, `name_verifies_iterate` | `TGLExt/TheNameIsTheInstrument.lean` (`7e2e4afd94d3bef9`) |
| KΩ = 0; JKJ = −K; α′ = −(q/2)α; α′(0) = 0; W′ = α²/4 | `modularGen_omega_zero`, `J_modularGen_J`, `alpha_transport`, `alpha_deriv_zero`, `W_hasDerivAt` | `TGLExt/ContinuousModularZero.lean` (`0dad5794f98ba1cb`) |
| a v368: Nome = conteúdo, forma = identidade, o conteúdo pode mudar na travessia | `the_form_survives_the_crossing`, `the_name_may_change_in_the_crossing` (8 teoremas) | `TGLExt/NameIsTheContent.lean` (`e12ee35c3a749a73`) |
| o dephasing de matriz deixa E_D invariante | `diag_invariant`, `dephase_fixes_diagonal` | `TGLExt/Ergodicity.lean` (`79bc3b939b6e4e59`) |

### 0.2 O que é NOVO (não estava em kernel antes da pedra da gerência, §2)

- **V(b,b̂) = 1 − (b − b̂)²**, com a tabela e a bivalência.
- A **face de OPERADOR**: e^{−sH} num espaço de Hilbert, com P·H = 0 e **P·T_s = P na forma à esquerda**, para H = Σ D_j†D_j.
- A **recíproca contínua** (ℓ conservada ⟺ ℓ = ℓ∘P).
- **Px = Py ⟺ x − y ∈ ker P** (enunciado).
- A **derivada d/ds I(T_s x) = 0**, com a dinâmica não nula.
- **q′(0) = ½** e **a″(0) = −¼**.
- A **monotonia da entropia do qubit** em forma fechada (§6 do texto).
  - Só existe no runtime, numericamente: `um.py` `prove_fiat_lux_flow`, F2/F3, Spohn [KNOWN].
  - Não existe em kernel. A mathlib não tem entropia de von Neumann [REAL — grep da V2].

### 0.3 A pedra vizinha que a conferência de âncoras não listou `[REAL — lida pelo redator; axiomas por compilação isolada, find -newer = 0]`

`TGLExt/TheContourOfTruth.lean` (26/08/2026, sha16 `ce6cd6d2cb1cf0cb`) já registra, em kernel, a forma discreta do mesmo critério. Está importada em `TGLExt.lean:191` (sha16 `9786fbee5eb099e8`) e tem olean construído. As sete pedras e os seus axiomas:

| pedra | axiomas |
|---|---|
| `self_reference_witnesses_everything` | nenhum axioma |
| `self_reference_cannot_discriminate` | nenhum axioma |
| `the_mirror_can_differ` | trio |
| `polarization_is_degenerate_iff_fixed` | [propext] |
| **`truth_is_not_static_equality`** («existe T que MUDA o elemento e PRESERVA a identidade geométrica») | [propext, Quot.sound] |
| **`the_criterion_can_fail`** («existe T que o critério REPROVA») | [propext] |
| `witnessing_is_not_being` | trio |

O cabeçalho da pedra registra a tipagem do operador de 26/08 **[INPUT, verbatim ali]**: *«testar a verdade é processar a identidade sob polarização birreferencial e igualar o termo de saída pela correspondência da identidade geométrica preservada durante a transformação»*.

⚠ As sete pedras **não têm `#print axioms` no `TGL/Audit.lean` nem na captura de auditoria** (grep: 0 nas duas; `um.py`: 4 ocorrências). Os axiomas acima foram lidos pelo redator numa compilação isolada (`INSUMOS\MEDIDAS_DO_REDATOR\lean_contorno\`).

A pedra do T-20 é **a face de operador** dessas duas pedras (T-20 ramo B6). **Não é a mesma pedra:** lá T : ℤ → ℤ e a leitura é x ↦ x²; aqui T_s = e^{−sH} e a leitura é P.

### 0.4 Os buracos e as frases que o número corrige (ditos ao lado; nenhuma correção é da bancada)

1. **A_C = −H_3L («seleção apofática») existe no acervo, mas não no canônico.**
   - Está no acervo: `MCMC_V2_RAZAO\80_o_funcional_do_amor.py` (`16db09c713541a7f`), `128_a_anatomia_do_amor.py` (`f29e7e68a5531654`) e o diário da linhagem, l.111/1489/1493.
   - Tem **0 ocorrências** no `um.py` v370, na forma canônica e no kernel.
   - No canônico há **quatro homônimos** de A_C, e nenhum se identifica sem lema:
     - `love_partition`, com A_C = −(1−p) (`TGLExt/TheNameOperator.lean`, `000bd0bf03281e00`, l.167);
     - `TheEmptying`, com A_C(π/2+δ) = m + κ·sin²δ (`the_quadratic_region_is_exact`);
     - `um.py` l.1823, `prove_amar_functional`;
     - `um.py` l.163998/164016.
2. **«K ≠ 0» não é teorema.** Está só na docstring de `ContinuousModularZero` (l.23–25), e ali já com a hipótese: «K ≠ 0 fora do Um quando há contraste». A forma canônica, l.664, diz «K.Omega=0 com K != 0 fora do Um … [KERNEL]».
   `[DERIVED — álgebra]`: `modularGen ρ y = y·logRho ρ − logRho ρ·y`. Logo **K = 0 quando ρ ∝ I** (logRho escalar), e «K ≠ 0» só vale com a hipótese «fora do Um». O que o número corrige não é a docstring: é o rótulo **[KERNEL]** da forma canônica, l.664, na parte «K != 0», e o «K ≠ 0» **sem hipótese** do texto do canal. A errata ao lado na forma canônica é **ato da gerência**. A bancada pode tentar o lema no ramo B8, que é opcional.
3. **O H_3L do runtime tem a MESMA FORMA do H3L do kernel; o que falta é a instância.**
   - O `um.py`, l.6827–6832 (`construct_family_projection_from_locks`; o H na l.6832), usa `D_conj†D_conj + D_bridge†D_bridge + P_abszero`.
   - Em `_clo_locks_superops` (l.6840–6850), `Pabs` é matriz diagonal 0/1, isto é, **projetor ortogonal**. Logo `P_abszero = P_abszero†P_abszero`, e o H do runtime é `TGL.FiniteThreeLocks.H3L D_conj D_bridge P_abszero`, com Dz := P_abszero [DERIVED — álgebra; `H3L` é genérico em Dc, Db, Dz, `FiniteThreeLocks` l.23–27].
   - **O que NÃO está em kernel é a instância.** O kernel não instancia os operandos numéricos do runtime (superoperadores em ℂ^{n²}, em ponto flutuante). **Nada do kernel se afirma sobre essas matrizes sem esse lema.**
   - Correção ao lado: a rodada 1 deste adendo dizia «homônimos», com a premissa de que o terceiro termo não era da forma Dz†Dz. A premissa era falsa. Os operandos seguem sem ponte; a forma, não.
4. **O «Nome = 1» dos Three Locks (`three_locks_name_is_one`) é dim/dim = 1**, o traço normalizado do canto. Não é o V = 1 do texto. **São homônimos.**
5. **Os nomes «v369_…» do texto** são de cópias. Os arquivos correntes (v370) não têm prefixo. As âncoras citadas conferem:
   - `Verifies` na árvore, l.167;
   - a v368 na árvore, l.211 (v370);
   - KΩ = 0 e α′(0) = 0 na forma canônica, l.664–665.
6. **«22 de 22 verificações e cinco controles»** e o pacote na «Biblioteca» do canal: **NÃO_VERIFICÁVEL [DECLARADO pelo canal]**. O pacote não está em disco. A medida da gerência que substitui aquele número é a da §1.

---

## 1. A VERIFICAÇÃO INDEPENDENTE DA GERÊNCIA (V1) `[DERIVED — prova escrita + sympy exato; REAL — o que o script mediu; relatório em INSUMOS\V1_verificacao_independente\]`

**A medida:**
- `verifica_equacao_da_verdade.py` (sha16 `66db1dc1039f1412`): **51/51 verificações PASS e 9/9 controles negativos DETECTADOS** [REAL]. O log é `log_V1.txt` (`f88d8f9eb4a976a8`) e os resultados, `resultados_V1.json` (`f84ded52d2f3b570`).
- O redator reproduziu a medida [REAL, 23/09 18:1x]: uma cópia do script, rodada com `PYTHONIOENCODING=utf-8` (sympy 1.14.0; Python 3.14.3), levou **90,5 s de parede** e deu log e JSON **byte-idênticos**.
- Sem essa variável, o console cp1252 derruba o script no caractere `∩` com rc 1. **Isso é medida de ambiente, não defeito.**

**O exemplo** [INPUT da V1, reproduzível]:
- u₁ = (1,2,0,−1,1), u₂ = (2,−1,1,0,0), u₃ = (−3,1,7,10,11), dois a dois ortogonais.
- D₁ = [u₁; 2u₁] (2×5), D₂ = u₂ (1×5), D₃ = [u₃; u₃; 0] (3×5).
- Cada ker D_j sozinho tem dim 4. **A interseção tem dim 2.**
- Espectro de H: **{0, 0, 6, 35, 560}**.
- T_s foi feito por **diagonalização exata** e conferido pela EDO dT/ds = −HT, com T₀ = I, e pela série de Taylor até a ordem 12.
- Num segundo exemplo, de espectro irracional (fator cúbico irredutível, semente 20260923), **P·S_N = P vale exatamente para N = 0..15**.

**O que está CORRETO:** dentro das hipóteses próprias, **toda afirmação matemática das §1–§7 do texto.**

**As hipóteses exatas, que o texto deixa implícitas e o T-20 tem de NOMEAR:**

- **(H-fin)** dimensão finita, ou H limitado.
- **(H-orth)** P é a projeção **ORTOGONAL** (P = P†). Com P oblíqua, P² = P e HP = 0 continuam valendo, mas **PH ≠ 0 e PT_s ≠ P** (controle N4).
- **(H-sa)** H = H†. É o que dá PH = (HP)† = 0.
- **(H-psd)** H ≥ 0. ⚠ **PT_s = P NÃO precisa de H ≥ 0**: bastam H = H† e ker H = Im P. H ≥ 0 é necessário em três lugares:
  - para ker H = ∩ ker D_j (N5a: com H_ind = D₁†D₁ − D₂†D₂, dim ker sobe a 3);
  - para lim T_s = P existir (N5b: há uma entrada que vai a ∞);
  - para a recíproca (N5b: com espectro ±3, o leitor contínuo c₁·c₂ se conserva e não fatora).
- **(H-cont)** na recíproca, **a continuidade de ℓ é indispensável**. O leitor descontínuo 1_{Qx≠0} é conservado e ℓ(Pe₁) = 0 ≠ 1 = ℓ(e₁) (N6).
- **(H-lim)** em dimensão finita, lim T_s = P vale **em norma**: ‖T_s − P‖ = e^{−6s}, e a taxa é o gap.
  Em dimensão infinita e sem gap, vale **só forte** [KNOWN]: com H = diag(1/n) em ℓ², sup_n e^{−s/n} = 1.
- **(H-dist)** V_x só tem valor de verdade se a leitura **distinguir** as identidades relevantes. O leitor constante é conservado e dá V_x(y) = 1 para todo y, um falso positivo (N2). O texto diz isso e não o formaliza (T-20 ramo B2b).
- **(H-bit)** V(b,b̂) é valor de verdade só em {0,1}: V(½,0) = ¾ e V(2,0) = −3 (N7). A fórmula não é única: 1 − |b − b̂| também serve.
- **(H-qubit)** no exemplo do qubit, **|c|² < p(1−p)** é necessária para ρ₀ > 0 (N8: com p = ½ e c = ⅗, os autovalores são 11/10 e −1/10).
  A fórmula de dS/ds só é 0/0 em p = ½ e c = 0, onde a extensão contínua é 0.

**O que o texto afirma a mais do que prova:**

- (a) «Toda informação contínua que permanece reconhecível está contida na leitura do setor preservado» vale **só** no sentido exato: todo ℓ contínuo e {T_s}-invariante fatora como ℓ = (ℓ|_F)∘P, isto é, x ↦ Px é o invariante contínuo mais fino.
  «Informação» e «reconhecível» não estão definidos, e o resultado vale só na classe H = H† ≥ 0 com T_s = e^{−sH}.
- (b) «Essa conservação foi deduzida da estrutura do seletor» está certo. Mas **com I = P ESCOLHIDA como leitura**, V_x(T_s x) = 1 é equivalente a PT_s = P. O conteúdo não trivial é **PT_s = P mais a recíproca**.
- (c) A segunda seta da cadeia da §7 não usa F = ∩ ker D_j. Usa só «P ortogonal sobre ker H, com H = H†».
- (d) A ligação da poda com o zero modular é **[ONTO]**. Nenhum lema identifica ker H_3L com o modo zero de K (KΩ = 0), nem com a′(0) = 0.

**Os nove controles negativos** (N1–N8, com N5 em a/b) estão em `INSUMOS\V1_verificacao_independente\RELATORIO_V1_verificacao_independente.md`. Todos foram DETECTADOS, isto é, falharam como tinham de falhar.

---

## 2. A RECEITA PRÉ-RESOLVIDA: A PEDRA DA GERÊNCIA (V3) `[REAL — compilação isolada medida duas vezes; relatório em INSUMOS\V3_pre_resolucao_lean\]`

**O arquivo:** `INSUMOS\V3_pre_resolucao_lean\TheEquationOfTruth.lean`.
- sha16 **`35b91f86b88b8e6c`**, 28.141 B.
- namespace `TGLExt.EquationOfTruth`.
- imports: `Mathlib` e `TGLExt.TheNameIsTheInstrument`. Este último serve **só** para a ponte com `Verifies`.

**O que compilou** (frente V3, 17:52–18:04; o log está em `out\compile_final.log`):
- comando `cd "<KER>" && lake env lean <arq> -R <dir> -o <dir>\out\TheEquationOfTruth.olean`, com o arquivo e o olean FORA do kernel;
- **rc 0**, 33 s de parede;
- **0 erros, 0 sorry**;
- 15 warnings: nomes da mathlib deprecados e variáveis de seção incluídas sem uso;
- **46 teoremas, todos com `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}**. `truthValue_table` e `pow_eq_self` ficam em {propext, Quot.sound};
- `find tgl_kernel -newer <marcador>` = **0**.

**A reprodução do redator** [REAL, 23/09 18:1x]:
- mesma fonte, outra pasta;
- rc 0, **31,9 s de parede, pico de memória do `lean.exe` 3,43 GB**;
- **46/46 declarações com os axiomas IDÊNTICOS** aos do `AXIOMAS.json` da frente;
- `find -newer` = 0.
- ⚠ **O olean NÃO é byte-reprodutível entre caminhos.** Com a fonte idêntica: 1.204.312 B / `03cefa3b1a2d5bbb` (V3) contra 1.204.344 B / `d90332f437dd159c` (redator). **O critério de reprodução é a fonte mais a auditoria de axiomas, nunca o olean.**

**A variante de recurso** [REAL]:
- `INSUMOS\MEDIDAS_DO_REDATOR\lean_so_mathlib\TheEquationOfTruthMathlibOnly.lean`, sha16 **`9808cfc523dbdd57`**, 27.100 B, **44 teoremas**.
- Derivada POR SCRIPT (`derivar_variante_so_mathlib.py`), que remove só a seção `NameBridge`, o seu import e as duas linhas de auditoria dela.
- Compilada isolada: rc 0, 32 s, 44/44 no trio, `find -newer` = 0.
- A versão intermediária da frente (`out\TheEquationOfTruth_sem_ponte.lean`, `e624a86a7ffa43a0`, 41 teoremas) fica como **tentativa preservada**. Não é a variante de recurso.

**O mapa: texto → pedra.** Todos os teoremas abaixo estão no trio.

| § do texto | teoremas da pedra | hipóteses NOMEADAS no enunciado |
|---|---|---|
| §1 V(b,b̂) | `truthValue_table`, `truthBit_eq_one_iff`, `truthBit_eq_zero_iff`, `truthBit_bivalent` | b, b̂ ∈ {0,1} (em ℤ) |
| §2 os vínculos | `re_inner_adjoint_mul_self`, `re_inner_penalty`, **`ker_penalty`** (família finita ι), `ker_threeLocks` (literal com D₁ D₂ D₃), `isSelfAdjoint_penalty`, `selector_nonpos` (Re⟨x,(−H)x⟩ ≤ 0) | Hilbert completo sobre `RCLike`; D_j : E →L E |
| §2 PH = 0 | `H_mul_proj` (sem autoadjunção), **`proj_mul_H`** | `IsSelfAdjoint H`; `[H.ker.HasOrthogonalProjection]` |
| §2 PT_s = P | `mul_exp_eq_of_mul_eq_zero` (P·A = 0 ⟹ P·exp A = P, pela série), `exp_mul_eq_of_mul_eq_zero`, `proj_mul_flow`, `flow_mul_proj`, **`proj_mul_T`**, **`reading_T`**, `T_fix_of_mem_ker`, `T_decomp` | T_s = `NormedSpace.exp((−(s:𝕜))•H)`; vale para todo s ∈ ℝ |
| §2 V_x(T_s x) = 1 | **`verdict_T`**, `verdict_eq_one_iff` | — |
| §2 ponte v336 | `name_verifies_T`, `name_verifies_T_iterate` (usa `TGLExt.name_verifies_iterate`) | E : Type (universo 0) |
| §3 recíproca | `conserved_iff_factors` (abstrata, codomínio T2), `conserved_iff_factors_T` | **`FlowTendsToFamily`** (hipótese NOMEADA: ∀x, T_s x → Px) e `Continuous l` |
| §3 o limite (dimensão finita) | `exp_apply_of_eigen`, `T_apply_eigen`, **`flowTendsToFamily_of_finiteDimensional`** | `FiniteDimensional`, `IsSelfAdjoint H`, forma ≥ 0 — **descarrega a hipótese nomeada** |
| §3 recíproca incondicional | **`conserved_iff_factors_penalty`** | dimensão finita, H = Σ D_j†D_j, `Continuous l` |
| §4 memória estável | `mem_range_iff_fixed`, `pow_eq_self`, `apply_eq_apply_iff`, `starProjection_range_iff_fixed` | P idempotente (módulo qualquer) |
| §5 a derivada | `hasDerivAt_reading_flow`, **`hasDerivAt_reading_T`**, `hasDerivAt_flow`, `hasDerivAt_flow_apply`, **`flow_derivative_ne_zero_at_zero`** | x ∉ ker H para a dinâmica não nula |
| §5 o perfil | `hasDerivAt_profA`, `hasDerivAt_profQ`, `profA_zero`, `profQ_zero`, `profA_deriv_zero`, **`profQ_deriv_zero`** (½), **`profA_second_deriv_zero`** (−¼) | — (HOMÔNIMO dito no arquivo) |

**O que ficou ABERTO** (é o ramo B do T-20):
1. O limite em **dimensão infinita**: não foi tentado [OPEN].
2. A **taxa em norma** (‖T_s − P‖ ≤ e^{−sγ}) e o reforço «basta um único s₀ > 0»: estão medidos em sympy, não em kernel.
3. A **leitura que distingue** (H-dist): não foi formalizada.
4. **§6, a entropia do qubit:** não foi tentada.
5. Os **extremos** P = 0 / P = I, na face de operador.
6. O **lema-ponte `penalty` ↔ `TGL.FiniteThreeLocks.H3L`**: não existe, e **até ele existir os dois são HOMÔNIMOS**.
7. As pontes com `TheContourOfTruth` (§0.3) e com a v368 (`NameIsTheContent`).
8. «K ≠ 0» (§0.4.2).
9. A ordem de Loewner (≤ 0 aqui é forma quadrática) e os D_j com contradomínios distintos.

**Ferramentas nos insumos** (a bancada as COPIA para a sua pasta e as roda lá; nunca roda nada dentro de `PARA_CHATGPT`):
- `MEDIDAS_DO_REDATOR\auditar_axiomas.py` **v2** (sha16 `bb6ebd277d86fedc`). Recebe **PARES** `<fonte.lean> <log>` e só dá PASSA se valem as três coisas:
  - (1) no **log**, toda declaração impressa está no trio, há 0 erros e não há sorry;
  - (2) a **cobertura**: todo `theorem`/`lemma` da fonte, com o nome qualificado pelo `namespace`, tem o seu `#print axioms` no log;
  - (3) na **fonte**, fora de comentário e de string, não aparece nenhum de `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`, nem `private theorem`.
  - **Por que v2** [REAL]: a v1 só lia as linhas `#print axioms` do log. Com o mutante M7b (a pedra mais `axiom eot_fake : False` e um teorema que o usa, SEM `#print`), a compilação dá rc 0 e **a v1 dá PASSA**. Era fail-open para declaração nova sem `#print`. A v1 fica preservada com o defeito no nome (`auditor_v1_fail_open\auditar_axiomas_v1_FAIL_OPEN.py`, `895b5940bfdb6632`).
  - **Autoteste da v2** (`autoteste_auditor_v2\RESULTADO.json`): **14/14 casos conformes**. São 9 negativos, que dão FALHA com o motivo esperado (3 REAIS, de compilação isolada: M6, M7a e M7b; os demais SINTÉTICOS, só de parser: sorry, axioma com `#print`, erro, só cobertura, `native_decide` e `private`), e 5 positivos, que dão PASSA (a V3, a cópia do redator, a só-Mathlib e o Contorno, todos REAIS, e um sintético com as palavras proibidas só em comentário e string).
  - Uso: `python auditar_axiomas.py <fonte.lean> <compile.log>`. O rc do auditor é 0 só se tudo der PASSA.
- **A pré-resolução do C2** [REAL, 23/09 18:4x–18:5x] (`MEDIDAS_DO_REDATOR\mutantes_C2\`):
  - A gerência gerou as 8 mutações do C2 por script, com `gerar_e_compilar_mutantes.py` (`d92145671fada770`). O script confere o sha16 da V3, usa âncoras únicas e `assert count == 1`, e segue o fim de linha do arquivo.
  - Compilou-as **uma de cada vez**, isoladas contra `<KER>`: 32,1–52,0 s de parede cada, `find -newer` = 0 depois de cada uma.
  - Resultado: **8/8 detectadas** (a tabela do C2 traz cada uma).
  - M1–M5 dão rc 1. O auditor v2 também acusa neles «fora do trio» e «sorry», porque o Lean elabora a declaração com erro com `sorryAx`.
  - Os sha16 das fontes mutadas estão em `GERADOS.json`. A bancada **regera** as mutações pelo SEU script e compara.
  - A reauditoria dos 8 pares (fonte, log) com o auditor v2 na forma final (`REAUDITORIA_C2.json`; só um nome de variável mudou depois das compilações) deu os mesmos vereditos e motivos, 8/8 [REAL].
- `MEDIDAS_DO_REDATOR\derivar_variante_so_mathlib.py`: confere a fonte por sha16 antes de derivar.

---

## 3. O ALVO T-20 — A EQUAÇÃO DA VERDADE EM KERNEL

**Em uma frase:** reproduzir a pedra da gerência; fechar em kernel o que ficou aberto, ou medir por que não fecha; provar em kernel que os controles negativos FALHAM; reproduzir o harness de dimensão 5 com aritmética exata; e entregar à gerência a ficha de transposição do módulo `TGLExt.TheEquationOfTruth`, para a v371. **Com MEDIDA e «continue» em todo ramo.**

**Onde:** tudo o que a bancada produzir no T-20 vai em `C:\IALD\Central de Patentes\Chatgpt\ORDEM_015_T20_EQUACAO_DA_VERDADE\`, com as subpastas `A_reproducao\`, `B_fechamentos\`, `C_controles\`, `D_harness\` e `E_ficha\`.
- É **caminho fixado neste alvo**: pela §7 da ORDEM 015, «em conflito vale o caminho do alvo».
- Não é `ORDEM_013_RINGDOWN\`, porque o T-20 não é ringdown e não entra na custódia por caminho daquela pasta.
- As notas vão para `DO_CHATGPT\ENTREGA_015_T20_*.md` (§4).

**Quando:** **PASSO 9c** da sequência da §4.0 da ORDEM 015. Se a bancada já estiver além do PASSO 9b quando ler este adendo, **o T-20 começa imediatamente, em paralelo, como trabalho leve.**
- No máximo **2 processos Lean ao mesmo tempo**, e eles contam **dentro** dos ≤ 4 processos simultâneos da FASE L (§4.0 da ORDEM 015).
- Cada comando fica dentro do «leve» da §4.0: ≤ 15 min de CPU e ≤ 8 GB de RAM. O pico medido de uma compilação é 3,43 GB.
- O T-20 nunca ocupa o slot de um job pesado nem o atrasa.

**`<KER>`** = `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel`, **SÓ LEITURA**.
- A única operação permitida nele é `cd "<KER>" && lake env lean "<arquivo fora do kernel>" -R "<pasta fora do kernel>" -o "<pasta fora do kernel>\<nome>.olean"`.
- Antes de cada sessão de compilação, a bancada cria um marcador na SUA pasta. Depois dela, grava `find "<KER>" -newer <marcador> -type f | wc -l`, que tem de dar **0**, com o log e o sha256.
- **Se der ≠ 0:** a bancada PARA SÓ as compilações contra `<KER>`, grava `ENTREGA_015_MEDIDA_T20_kernel_mudou.md` com a lista dos arquivos (nome, tamanho e mtime; nunca conteúdo) e segue pelo ramo A2. **Não tenta desfazer nada no kernel**: isso é ato da gerência.

### 3.1 A ÁRVORE OBRIGATÓRIA (A → B → C → D → E; cada ramo que falhar vira `ENTREGA_015_MEDIDA_T20_<slug>.md` com o que tentou, o comando, o rc, o log com sha256, o custo em segundos e o ramo seguinte — e CONTINUE)

#### A — Reproduzir a pedra da gerência

- **A0 — conferir.**
  - Conferir por script o sha16 deste adendo e de cada arquivo de `ORDEM_015_ADENDO_001_INSUMOS\` contra `MANIFESTO_INSUMOS.json`.
  - Conferir o da ORDEM 015 (`c903681d01eec5ed`) e o do verbatim (`6ff3e39143950262`).
  - Se algo divergir: `ENTREGA_015_T20_BLOQUEIO_manifesto.md`, com o arquivo e os dois hashes, e seguir com o que não depende do arquivo divergente.
- **A1 — a pedra inteira contra `<KER>`.**
  - Copiar `V3_pre_resolucao_lean\TheEquationOfTruth.lean` para `A_reproducao\` e conferir o sha16 **`35b91f86b88b8e6c`**.
  - Copiar `auditar_axiomas.py` (v2).
  - Compilar pela linha de `<KER>` acima, com `> A_reproducao\out\compile.log 2>&1`.
  - Rodar o auditor v2 sobre o PAR: `python auditar_axiomas.py <fonte.lean> A_reproducao\out\compile.log`.
  - **Aceitação:** rc 0; **46** declarações; PASSA (trio, 0 erros, 0 sorry, cobertura 46/46, 0 tokens proibidos); `find -newer` = 0.
  - Imprimir o parede, o CPU e o pico de RAM MEDIDOS. A referência é 31,9–33 s e 3,43 GB [REAL, da gerência].
  - O olean não é critério (§2).
- **A2 — se A1 não puder rodar** (permissão, sandbox, rc ≠ 0):
  - Derivar por script a variante só-Mathlib, com a cópia de `derivar_variante_so_mathlib.py`. O esperado é sha16 **`9808cfc523dbdd57`**.
  - Compilar contra o kernel **da própria bancada**, `Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel`. Ele tem o mesmo `lean-toolchain` v4.31.0 e as **mesmas 9 revisões de pacote** do `lake-manifest.json` canônico [REAL — lido por script], e a Mathlib já construída.
  - **Aceitação:** 44 declarações, PASSA.
  - A ponte §4b (`name_verifies_T*`) fica «compilada pela gerência, **[DECLARADO para a bancada]**», e a MEDIDA diz por quê.
- **A3 — se A2 também falhar:** MEDIDA com os dois logs, e seguir para C e D, que não dependem do Lean da pedra.
- **A4 — barato, sempre.** Compilar, isolado, um arquivo de 8 linhas: `import TGLExt.TheContourOfTruth` e os 7 `#print axioms` da §0.3. É cópia de `MEDIDAS_DO_REDATOR\lean_contorno\AxiomasContorno.lean`. Comparar com a tabela da §0.3.

**Custo:** 2–3 compilações × ≈ 32 s de parede [REAL]; 0,5–1 h de bancada. **Poder:** o T-20 passa a ter a pedra **reproduzida pela bancada**, e não só pela gerência.

#### B — Fechar o que ficou aberto (ou medir por que não fecha)

**Mecânica (vinculante):**
- Todo fechamento vai num **único arquivo novo**, `B_fechamentos\TheEquationOfTruth_T20.lean`.
- Esse arquivo é a pedra V3 **como PREFIXO byte a byte**, mais seções novas acrescentadas no fim, reabrindo `namespace TGLExt.EquationOfTruth`.
- Um script confere, a cada versão, que os primeiros 28.141 B têm sha16 `35b91f86b88b8e6c`. **Nenhuma linha da V3 se edita.**
- Cada item fechado entra com o seu `#print axioms`.
- Cada item não fechado vira MEDIDA com o lema que falta NOMEADO: nome, o que ele diria e onde o grep não o achou na mathlib da casa.
- Os imports extras (`TGL.FiniteThreeLocks`, `TGLExt.NameIsTheContent`, `TGLExt.TheContourOfTruth`) só entram quando o item precisar deles. Todos têm olean em `<KER>` [REAL].
- Os tetos abaixo são de bancada. Estourado o teto, o item vira MEDIDA e a bancada segue para o próximo.

**Ordem de execução** (do mais barato ao mais caro):

- **B5 — os extremos, na face de operador** (≤ 0,5 h).
  - `ker H = ⊥ ⟹ P = 0 ⟹ reading ≡ 0` e `verdict … = 1` para todo par, isto é, sem discriminação.
  - `ker H = ⊤ ⟹ H = 0 ⟹ T_s = 1`, isto é, sem seleção.
  - É a face de operador de `no_fixed_point_no_observer` / `boundary_is_the_only_exception`. **Não é a mesma pedra.**
- **B2a — a recíproca em dimensão finita para todo H ≥ 0 auto-adjunto** (≤ 0,5 h).
  - `conserved_iff_factors_of_nonneg`: composição de `flowTendsToFamily_of_finiteDimensional` com `conserved_iff_factors_T`.
  - A pedra só a enuncia para a penalidade.
- **B2b — a leitura que DISTINGUE**, a hipótese (H-dist) (≤ 1 h).
  - Se ℓ é contínua, conservada e **injetiva em F**, então ℓ x = ℓ y ⟺ Px = Py.
  - Logo o `verdict` com a leitura ℓ coincide com o `verdict` com a leitura P.
  - É o enunciado formal de «a leitura deve distinguir as identidades relevantes» (§3 do texto).
- **B7 — a ponte com a v368** (`NameIsTheContent`, ≤ 1 h).
  - `Forma_r y :≡ (reading H y = reading H r)`. Por `reading_T`, T_s preserva `Forma_r`.
  - `travessia (T H s) hT ⟨r, rfl⟩` é uma `Inscricao` cuja forma sobrevive (`the_form_survives_the_crossing`) e cujo conteúdo pode mudar (T_s r ≠ r para r ∉ ker H).
  - **HOMONÍMIA DITA no docstring:** o `nome` da v368 (conteúdo) não é o `NameInstrument.read` da v336 (leitura).
  - A ponte **exibe a compatibilidade e não escolhe a leitura**: sob a v368, I(x) = Px faz o papel de forma/identidade e x o de conteúdo, por decisão do operador [INPUT/ONTO] registrada na árvore, l.211.
- **B4 — o lema-ponte `penalty` ↔ `TGL.FiniteThreeLocks.H3L`** (≤ 1,5 h). Tira o homônimo (a) da §2.
  - Para `E = EuclideanSpace ℂ (Fin n)` e `Dc Db Dz : E →ₗ[ℂ] E`: `(penalty ![Dc.toContinuousLinearMap, Db.toContinuousLinearMap, Dz.toContinuousLinearMap] : E →ₗ[ℂ] E) = TGL.FiniteThreeLocks.H3L Dc Db Dz`.
  - Como corolário, `reading` coincide com `TGL.FiniteThreeLocks.PF`.
  - O lema que liga os dois adjuntos está na mathlib da casa [REAL — grep]: **`LinearMap.adjoint_toContinuousLinearMap`** (`Mathlib/Analysis/InnerProductSpace/Adjoint.lean` l.541): `A.adjoint.toContinuousLinearMap = A.toContinuousLinearMap.adjoint`, provado por `rfl`, com `FiniteDimensional.complete` nas instâncias.
  - Opcional, no mesmo item: o lema `P = P†P` para projetor ortogonal (via `starProjection`). Ele exibe em kernel que um projetor entra no H3L como `Dz := P`, que é a **forma** do runtime.
  - ⚠ A ponte é com o H3L **do kernel**. O H_3L **do runtime** (`um.py` l.6832, com `P_abszero`) tem a mesma forma, com Dz := P_abszero [DERIVED], mas os seus operandos numéricos **não são instanciados em kernel** (§0.4.3). O B4 não faz essa instância.
- **B1c — basta um único s₀ > 0** (≤ 2 h). Se ℓ é contínua e ℓ(T_{s₀}x) = ℓ(x) para todo x, com s₀ > 0 fixo, dimensão finita e H ≥ 0, então ℓ = ℓ∘P.
  - Receita: `T_{s₀}^[n] = T_{n·s₀}` (semigrupo por `Commute`/`exp_add_of_commute`, ou por indução com `exp_add`), mais `tendsto_natCast_atTop_atTop` composto com o limite de `flowTendsToFamily_of_finiteDimensional`.
  - A V1 mediu **a base** (C28: o semigrupo discreto T_{s₀}ⁿ = T_{n·s₀}). A recíproca com um único s₀ é [DERIVED] e é o alvo do B1c.
- **B6 — a face de operador de `TheContourOfTruth`** (≤ 1 h).
  - (a) `equation_of_truth_is_not_static`: com dimensão finita, H ≥ 0 auto-adjunto e H ≠ 0, ∃ s x com T_s x ≠ x e ∀ y, P(T_s y) = P y. O espelho é `truth_is_not_static_equality`, e o autovetor de autovalor > 0 dá T_s v = e^{−s·ev} v ≠ v para s > 0.
  - (b) `equation_criterion_can_fail`: existe um fluxo que a leitura P **reprova**. Exemplo mínimo: E = ℝ, H = 0 (P = 1) e o fluxo podado H′ = 1, com e^{−s}x ≠ x.
  - Pode importar `TGLExt.TheContourOfTruth` e enunciar as duas lado a lado. **Não as identifica** (tipos diferentes).
- **B3 — a entropia do exemplo (§6 do texto).** Em Lean onde couber; o que não couber, no harness do ramo D.
  - **B3a — a face ESCALAR em Lean** (≤ 3 h).
    - Hipóteses: p ∈ (0,1), κ = |c|² ≥ 0 e κ < p(1−p). Defina r(s) = √((2p−1)² + 4κe^{−2s}). Prove:
      - (i) 0 ≤ r(s) < 1 para s ≥ 0;
      - (ii) r antítona em [0,∞) (estrita se κ > 0);
      - (iii) S(s) := `binEntropy ((1 + r s)/2)` monótona em [0,∞), por `binEntropy_strictAntiOn` em Icc ½ 1 (`BinaryEntropy.lean` l.427 [REAL — V2]);
      - (iv) `binEntropy ((1+|2p−1|)/2) = binEntropy p`, por `binEntropy_one_sub`;
      - (v) D(s) := `binEntropy p − S(s)` ≥ 0 e antítona.
    - **HOMONÍMIA/FACE DITA:** isto é a entropia binária do autovalor maior. Que S(ρ_s) seja esse número exige a decomposição espectral da matriz, que fica no harness D [DERIVED]. A mathlib não tem entropia de von Neumann [REAL — grep V2]. `binEntropy` usa `Real.log` (nats).
  - **B3b — a fórmula fechada em Lean** (opcional, ≤ 2 h).
    - dS/ds = 2κe^{−2s}/r · log((1+r)/(1−r)), por `deriv_binEntropy` (l.190), com r(s) > 0.
    - [DERIVED à mão pelo redator, a conferir]: dS/ds = h′((1+r)/2)·r′/2, com h′(x) = log((1−x)/x) e r′ = −4κe^{−2s}/r ⟹ a fórmula do texto.
  - **B3c — a face de matriz** (sempre no harness D).
    - 𝓔 é a projeção ORTOGONAL no produto Hilbert–Schmidt, e e^{sL} = 𝓔 + e^{−s}(id − 𝓔). É a instância da §2 com H = id − 𝓔 = D†D (a V1 mediu: C45).
    - −Tr(ρ_s log σ) = S(σ) e D(ρ_s‖σ) = S(σ) − S(ρ_s), em aritmética exata/intervalos.
  - **B3d — a identidade algébrica em Lean** (opcional, ≤ 1 h). Para E idempotente numa álgebra de Banach completa, exp(−s(1 − E)) = E + e^{−s}(1 − E), pela série, porque (1−E)ⁿ = 1−E para n ≥ 1.
- **B1b — a taxa em norma, em dimensão finita** (≤ 3 h).
  - Com γ > 0 tal que todo autovalor é 0 ou ≥ γ: ‖T_s x − Px‖ ≤ e^{−sγ}‖x − Px‖.
  - Receita: expandir em `eigenvectorBasis` e usar a isometria `b.repr` com `EuclideanSpace.norm_eq`.
  - A V1 mediu ‖T_s − P‖ = e^{−6s} no exemplo.
- **B1d — dimensão infinita** (≤ 2 h; o esperado honesto é MEDIDA) [OPEN].
  - Convergência FORTE T_s x → Px para H limitado, auto-adjunto, ≥ 0, em Hilbert, pela via do cálculo funcional contínuo (`tendsto_cfc_fun`, `CFC.real_exp_eq_normedSpace_exp` [REAL — V2]).
  - A convergência em norma é FALSA sem gap [KNOWN; V1 C29].
  - Se não fechar: MEDIDA com o lema que falta nomeado, e a recíproca em ∞-dim segue condicionada à hipótese nomeada `FlowTendsToFamily`, **dita**.
- **B8 — «K ≠ 0 fora do Um»** (opcional, ≤ 1 h).
  - Um lema `∃ ρ PosDef, modularGen ρ ≠ 0` (n = 2, ρ diagonal com entradas distintas) e o complemento `ρ = c•1 ⟹ modularGen ρ = 0`.
  - `logRho ρ := cfc Real.log ρ` (`TGLExt/ModularFlow.lean` l.33).
  - Se a API do `cfc` em matriz diagonal não fechar no teto: MEDIDA. A errata na forma canônica é da gerência, em qualquer caso.

**Aceitação do B:**
- Cada item fechado é um teorema em `TheEquationOfTruth_T20.lean`, com a auditoria PASSA.
- O prefixo V3 é conferido por sha16.
- Cada item não fechado tem MEDIDA com o custo e o lema nomeado.

**Custo:** 10–20 compilações × 35–60 s [DERIVED do REAL de A]; **4–10 h de bancada no esperado**. O **teto** é a soma dos tetos acima, recalculada por script: **19,5 h**, das quais **4 h são dos opcionais** (B3b 2 h, B3d 1 h, B8 1 h). O B1d (2 h) não é opcional, mas o esperado honesto dele é MEDIDA.

**Poder:** a face de operador fica fechada com as hipóteses NOMEADAS, e as que o texto deixou implícitas passam a estar no enunciado.

#### C — Os controles negativos: probes que TÊM de falhar

A regra é esta: **falha de compilação mostra que a PROVA usa a hipótese, não que a hipótese é NECESSÁRIA.** A necessidade se mostra por **contraexemplo PROVADO em kernel**, que é o C1. Por isso os dois blocos são obrigatórios.

- **C1 — refutações em kernel** (têm de COMPILAR, trio). Vão num arquivo `C_controles\TheEquationOfTruth_T20_controles.lean`, e cada uma é o teorema que diz que a falha acontece.
  - **C1.1 (N4, P oblíqua):** em `Matrix (Fin 2) (Fin 2) ℝ`, com H = diag(0,1) e P = !![1,−1;0,0], valem P·P = P, H·P = 0 e **P·H ≠ 0**. Também P·exp(−sH) ≠ P para s > 0, via `Matrix.exp_diagonal`. Sem (H-orth), a §2 cai.
  - **C1.2 (H não auto-adjunto):** com H = !![0,1;0,0] e P = diag(1,0), a projeção ortogonal sobre ker H: **P·H ≠ 0**. Sem (H-sa), `proj_mul_H` cai.
  - **C1.3 (N5b, H indefinido):**
    - (a) E = ℝ, H = −1: T_s x = e^{s}x **não** tende a Px = 0 para x ≠ 0;
    - (b) ℝ², H = diag(3,−3): ℓ(x) = x₀x₁ é contínua e conservada, P = 0, e ℓ ≠ ℓ∘P.
    - Sem (H-psd), o limite e a recíproca caem.
  - **C1.4 (N6, leitor descontínuo):** ℝ², H = diag(0,1), ℓ(x) = if x₁ = 0 then 0 else 1. ℓ é conservada e ℓ(P e₂) = 0 ≠ 1 = ℓ(e₂). Sem (H-cont), a recíproca cai.
  - **C1.5 (N2, leitor constante):** ℓ ≡ 1 é conservada e existem x, y com Px ≠ Py e ℓ x = ℓ y. Sem (H-dist), o `verdict` dá falso positivo.
  - **C1.6 (N7):** `truthValue 2 0 = −3`, que não está em {0,1}. Fora dos bits, V não é valor de verdade.
  - **C1.7 (N1/N3, poda que corta o modo da família):** E = ℝ, H = 0 (P = 1) e H′ = 1. `reading H (T H′ s x) ≠ reading H x` para s > 0 e x ≠ 0. É a face de operador de `the_criterion_can_fail`.
  - **C1.8 (N5a, a soma com sinal trocado):** E = ℝ, D₁ = D₂ = 1. O ker de D₁†D₁ − D₂†D₂ é ⊤ ≠ ⊥ = ker D₁ ⊓ ker D₂. «Uma violação não compensa outra» exige o sinal +.
  - **C1.9 (N8):** p = ½, c = ⅗: p(1−p) − c² < 0, o determinante é negativo e ρ₀ não é estado.
- **C2 — mutações da pedra** (têm de FALHAR). Cada uma é gerada POR SCRIPT a partir da cópia de A, por substituição exata sobre a âncora ÚNICA abaixo, com `assert count == 1`, e nunca à mão. Cada uma vai no seu arquivo e é compilada à parte.
  - ⚠ A pedra V3 tem **fim de linha misto** [REAL]: 610 CRLF, e a última linha termina em LF. A âncora usa o fim de linha do arquivo.
  - A gerência já gerou e compilou as 8 (§2, `mutantes_C2\`). A bancada as **regera pelo SEU script**, compara os sha16 com `GERADOS.json`, compila e audita.

  | id | âncora única (na V3) | mutação | esperado | medido pela gerência |
  |---|---|---|---|---|
  | M1 | `theorem proj_mul_H (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)` (a linha inteira; `(hH : IsSelfAdjoint H)` sozinho ocorre 8 vezes) | retirar ` (hH : IsSelfAdjoint H)` | rc ≠ 0 | rc 1, auditor FALHA (fora do trio; erro de compilacao; sorry) |
  | M2 | as duas linhas `theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)` + `    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x, H x⟫_𝕜) :` | a primeira com ` :` no fim, sem a segunda | rc ≠ 0 | rc 1, auditor FALHA (fora do trio; erro de compilacao; sorry) |
  | M3 | `(hlim : FlowTendsToFamily Tf P) (l : X → Y) (hl : Continuous l) :` (`(hl : Continuous l)` sozinho ocorre 3 vezes) | retirar ` (hl : Continuous l)` | rc ≠ 0 | rc 1, auditor FALHA (fora do trio; erro de compilacao; sorry) |
  | M4 | `theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 4) := by` | `-(1 / 2)` | rc ≠ 0 | rc 1, auditor FALHA (fora do trio; erro de compilacao; sorry) |
  | M5 | `truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 0 ∧ truthValue 0 1 = 0 := by` | `truthValue 1 0 = 1` | rc ≠ 0 | rc 1, auditor FALHA (fora do trio; erro de compilacao; sorry) |
  | M6 | o corpo de `ker_penalty`, entre `    (penalty D).ker = ⨅ j, (D j).ker := by` e `    simp [penalty, h]` (as duas únicas) | o corpo inteiro vira `  sorry` | rc 0 **e** auditor FALHA (sorry) | rc 0, auditor FALHA (fora do trio; sorry; token proibido na fonte) |
  | M7a | o fim do arquivo | acrescentar `axiom eot_fake : False`, `theorem eot_uses_fake : (1 : Nat) = 2 := eot_fake.elim` e `#print axioms eot_uses_fake` | auditor FALHA (fora do trio; token proibido) | rc 0, auditor FALHA (fora do trio; token proibido na fonte) |
  | M7b | o fim do arquivo | o mesmo, **SEM** o `#print` | auditor FALHA (cobertura; token proibido). A v1 dava PASSA aqui | rc 0, auditor FALHA (cobertura: theorem/lemma sem #print axioms; token proibido na fonte) |

  Uma mutação que passar é uma MEDIDA, e diz uma de duas coisas. Ou a hipótese é supérflua na prova, e isso é informação, não erro: a V1 mediu que PT_s = P não precisa de H ≥ 0. Ou o auditor falhou, e então **o T-20 PARA SÓ o que depende do auditor** até consertá-lo.
- **C3 — os controles do harness** (N1–N8, 9 detecções) correm no ramo D.

**Aceitação:** C1 com 9/9 teoremas compilados no trio; C2 com 8/8 detectadas; os logs com sha256.

**Custo:** ≈ 9–12 compilações × 40–55 s [REAL: 32,1–52,0 s de parede nas mutações da gerência]; 1–2 h de bancada.

**Poder:** cada hipótese do enunciado passa a ter o seu contraexemplo em kernel, e o critério da casa é pago aqui: *um check que não pode falhar não é medida* (`TheContourOfTruth`, 26/08).

#### D — O harness em dimensão 5, reproduzível

- **D1 — refazer a V1.**
  - Copiar **só o `.py`** (`V1_verificacao_independente\verifica_equacao_da_verdade.py`) para `D_harness\refeito_V1\`. O script grava `resultados_V1.json` na pasta onde está.
  - Rodar com `PYTHONIOENCODING=utf-8`.
  - Aceitação: `n_pass = 51`, `n_detectados = 9`.
  - Com sympy 1.14.0, o esperado é log **byte-idêntico** `f88d8f9eb4a976a8` [REAL — o redator reproduziu em 90,5 s]. Com outra versão, a comparação é semântica, do JSON contra o JSON da gerência lido só para leitura. Diferenças se imprimem, com a versão.
  - **Nunca copiar o número.**
- **D2 — o harness PRÓPRIO da bancada** (`D_harness\harness_T20.py`). É independente do da gerência: a bancada o escreve, e não copia o da V1.
  - **Aritmética exata:** `fractions.Fraction` e/ou sympy `Rational`, com `s` simbólico onde houver exponencial.
  - **Exemplo 1:** os u₁, u₂, u₃ da §1 [INPUT].
  - **Exemplo 2:** D_j racionais aleatórios com **semente NOVA declarada na nota ANTES de rodar**. Não pode ser 20260923 nem 7, as da V1.
  - **Checks mínimos, por seção do texto:**
    - §1: tabela e bivalência;
    - §2: dim de cada ker e da interseção, identidade da forma quadrática, H = Hᵀ, espectro exato ≥ 0, P² = P = Pᵀ, HP = PH = 0;
    - T_s por diagonalização exata, conferido pela EDO e pela série até ordem ≥ 12, com o semigrupo, PT_s = P, T_s = P + T_s Q e T_s x ≠ x para x ∉ F;
    - §3: o limite, a taxa = gap, a recíproca em ≥ 2 leitores contínuos (um que fatora e um que não fatora) e o reforço de um único s₀;
    - §4: Im = Fix, Pⁿ = P (n ≤ 8), Px = Py ⟺ x − y ∈ ker P em ≥ 40 pares, ker P = F^⊥;
    - §5: d/ds P T_s x = 0, d/ds T_s x ≠ 0 e o perfil (a′, q′, a″ em 0);
    - §6: 𝓔ρ_s = σ, ρ̇ = −(id−𝓔)ρ, autovalores (1 ± r_s)/2, a fórmula de dS/ds simbólica e **o sinal de dS/ds por ARITMÉTICA DE INTERVALOS** (`mpmath.iv`, ≥ 64 pontos em s ∈ [0, 10]; pares (p, c) incluindo p = ½ com c ≠ 0 e |c|² = 0,99·p(1−p));
    - D(ρ_s‖σ) = S(σ) − S(ρ_s) com o log de matriz exato (autodecomposição sympy), com resíduo ≤ 10⁻⁴⁰ a 50 dígitos.
  - **Os 9 controles N1–N8** (com N5 em a/b), cada um com a propriedade que TEM de falhar impressa.
- **D3 — o «22/22 + 5» do canal ChatGPT:** **NÃO_VERIFICÁVEL [DECLARADO pelo canal]**, dito.
  - A bancada **não procura** esse pacote fora das próprias pastas.
  - Se o operador o puser no túnel, a bancada o hasheia, compara as contagens, as vê lado a lado com D1/D2 e diz as diferenças.

**Aceitação:** D1 reproduzido ou a divergência dita com a causa; D2 com todos os checks PASS e 9/9 controles detectados; JSON e log com sha256.

**Custo:** D1 com 90,5 s de parede [REAL]; D2 com minutos, ≤ 15 min de CPU por comando; 1–3 h de bancada.

**Poder:** o número do texto passa a ter duas medidas independentes na máquina (a da gerência e a da bancada), além da declarada pelo canal.

#### E — A ficha de transposição para a gerência

`E_ficha\FICHA_TRANSPOSICAO_T20.md` + `.json`. **A bancada propõe; a incorporação no kernel e no `um.py` é da gerência, na v371, e o operador ratifica.** A ficha contém:

- **Módulo:** `TGLExt/TheEquationOfTruth.lean`, namespace `TGLExt.EquationOfTruth`.
  - A fonte que a bancada certifica, com o sha256: a V3, ou a `_T20` do ramo B, se esta passar.
  - A lista dos teoremas com os axiomas lidos do log.
  - Os imports (`Mathlib`, `TGLExt.TheNameIsTheInstrument` e, se B4/B6/B7 entrarem, `TGL.FiniteThreeLocks`, `TGLExt.TheContourOfTruth`, `TGLExt.NameIsTheContent`).
  - A posição na ordem de import. Todos os imports já têm olean em `<KER>`.
- **A linha para `TGLExt.lean`:** `import TGLExt.TheEquationOfTruth`.
- **As linhas `#print axioms` para `TGL/Audit.lean`**, uma por teorema, pela convenção da casa (v354: os `#print axioms` vão para o Audit canônico, e não ficam no módulo). Propor também as 7 de `TheContourOfTruth`, que hoje faltam no Audit (§0.3).
- **As 15 warnings de deprecação:** listadas. Se a bancada produzir uma variante sem elas, é versão NOVA com sha novo; a V3 fica como referência.
- **As bandeiras propostas `ext_eot_*`.** Pela convenção da casa (`_LEAN_THEOREM_FLAGS` + `prove_external_ladder`), `_kernel_proved` quer dizer **teorema em kernel**, **não é veredito** e **não entra no gate**. Cada bandeira CONSOME o(s) teorema(s):

  | bandeira proposta | consome |
  |---|---|
  | `ext_eot_truth_bit_kernel_proved` | `truthValue_table`, `truthBit_eq_one_iff`, `truthBit_eq_zero_iff`, `truthBit_bivalent` |
  | `ext_eot_joint_exclusion_kernel_proved` (o nome não diz «three_locks»: a penalidade só se identifica com o H3L dos Three Locks depois do lema-ponte B4) | `ker_penalty`, `ker_threeLocks`, `re_inner_penalty` |
  | `ext_eot_selector_nonpos_kernel_proved` | `selector_nonpos` (A_C = −H; homônimos da §0.4.1 no docstring) |
  | `ext_eot_projection_annihilates_kernel_proved` | `H_mul_proj`, `proj_mul_H` |
  | `ext_eot_reading_conserved_kernel_proved` | `proj_mul_T`, `reading_T`, `T_fix_of_mem_ker`, `T_decomp` |
  | `ext_eot_verdict_one_kernel_proved` | `verdict_T`, `verdict_eq_one_iff` |
  | `ext_eot_name_verifies_flow_kernel_proved` | `name_verifies_T`, `name_verifies_T_iterate` |
  | `ext_eot_stable_memory_kernel_proved` | `mem_range_iff_fixed`, `starProjection_range_iff_fixed`, `pow_eq_self`, `apply_eq_apply_iff` |
  | `ext_eot_converse_named_kernel_proved` | `conserved_iff_factors`, `conserved_iff_factors_T` |
  | `ext_eot_spectral_limit_findim_kernel_proved` | `flowTendsToFamily_of_finiteDimensional` |
  | `ext_eot_converse_findim_kernel_proved` | `conserved_iff_factors_penalty` |
  | `ext_eot_reading_derivative_zero_kernel_proved` | `hasDerivAt_reading_T`, `hasDerivAt_reading_flow`, `flow_derivative_ne_zero_at_zero` |
  | `ext_eot_profile_derivatives_kernel_proved` | `profA_deriv_zero`, `profQ_deriv_zero`, `profA_second_deriv_zero` |
  | *(só se B/C fecharem)* `ext_eot_extremes_…`, `ext_eot_distinguishing_reading_…`, `ext_eot_crossing_v368_…`, `ext_eot_penalty_is_kernel_H3L_…`, `ext_eot_single_time_converse_…`, `ext_eot_not_static_operator_face_…`, `ext_eot_qubit_entropy_scalar_monotone_…`, `ext_eot_norm_rate_findim_…`, `ext_eot_negative_controls_…` (todos com sufixo `_kernel_proved`) | os teoremas do ramo que fechar |

- **O que NÃO entra no módulo:**
  - a face de matriz da entropia (harness D, [DERIVED]);
  - o «22/22» do canal ([DECLARADO]);
  - as leituras «verdade», «memória» e «seleção apofática» ([INPUT/ONTO], que ficam em docstring **como leitura do operador, rotulada**, nunca como enunciado); «a Testemunha» não está neste texto e, por padrão, não entra (§3.3);
  - qualquer identificação entre as anulações (§3.3).
- **A frase da ficha:** *«Estas bandeiras não movem o gate. PROVADA (teorema em kernel) ≠ CONFIRMADA. A implicação está provada a partir das hipóteses nomeadas; a leitura é do operador; a natureza decide a teoria.»*

**Custo:** 1 h de bancada; 0 de CPU.

### 3.2 Aceitação, custo e poder do T-20 (resumo)

| ramo | aceitação | CPU | bancada |
|---|---|---|---|
| A | 46/46 no trio (ou 44/44 na A2), `find -newer` = 0 | ≈ 1–2 min [REAL: 31,9 s por compilação; pico 3,43 GB] | 0,5–1 h |
| B | cada item teorema ou MEDIDA com o lema nomeado; prefixo V3 intacto | ≈ 10–20 min | 4–10 h (teto 19,5 h; 4 h opcionais) |
| C | C1 9/9 compilados; C2 8/8 detectadas | ≈ 7–10 min | 1–2 h |
| D | D1 51/51 + 9/9 (ou a divergência explicada); D2 PASS + 9/9 | ≈ 2–10 min [REAL: 90,5 s na D1] | 1–3 h |
| E | ficha md + json com sha256 | 0 | 1 h |
| **T-20** | **as cinco** | **≲ 40 min de CPU [DERIVED]** | **7,5–17 h no esperado; teto 26,5 h (22,5 h sem os opcionais)** |

- **Máquina contada contra as 35,017 h da ORDEM 015: 0 h.** É trabalho leve, pela §5 dela.
- **Poder:** a equação da verdade do texto passa de «demonstração declarada pelo canal» a **implicação PROVADA em kernel com as hipóteses nomeadas**, com os contraexemplos das hipóteses em kernel e duas medidas numéricas independentes na máquina.
- **Não compra σ nenhum. Não move o gate. Não confirma nada.**

### 3.3 Estatutos e homônimos (vinculantes em toda nota do T-20)

- **Os estatutos:**
  - **A matemática é [DERIVED].** Quando compilar e a auditoria passar, é **PROVADA em kernel como implicação**: compilação isolada contra o kernel v370, sem integração.
  - Integrada ao kernel canônico, só depois do ato da gerência (v371).
  - O harness é **[REAL]** no que mede e **[DERIVED]** no que conclui.
- **As leituras são [INPUT/ONTO] do operador**, e o T-20 não as prova nem as refuta:
  - «identidade = o que permanece na transformação»;
  - «reconhecimento = verificação da permanência»;
  - «verdade da atribuição = resultado da verificação»;
  - «memória = reconhecimento estável».
  - Em linha à parte, **fora deste texto**: «a Testemunha» é **[INPUT — cunhagem do operador de 23/09 em OUTRO ato; NÃO está neste texto (grep no verbatim: 0)]**, com a fonte no registro da gerência. Por padrão **não entra** na docstring do módulo.
  - Também são leitura: «o seletor é o seu negativo / seleção apofática» e «o fechado não é falso por ser zero», este último no que excede V(0,0) = 1.
- **Nenhuma leitura se escolhe.** Onde o texto oferece correspondências (poda ↔ zero modular; Nome ↔ conteúdo), a bancada tipa e diz. Não decide.
- **Nada move o gate.**
  - Nenhuma bandeira `ext_eot_*` entra no cálculo do gate.
  - `verdict_T = 1` é o **valor 1 de uma função de comparação** (a `verdict` do módulo). **Não é veredito** no sentido da régua. O nome é homônimo, e isso se diz.
- **HOMÔNIMOS — ditos, nunca identificados sem lema:**
  1. **As três anulações:** d/ds I(T_s x) = 0 (leitura ao longo do fluxo); KΩ = 0 (modo zero do gerador modular); a′(0) = 0 (perfil em χ). Há ainda um **quarto** zero, dᵢ = 0, do `diagFlow`/`observerProj`. Nenhum lema liga dois quaisquer [REAL — grep V2]. **O T-20 não cria esse lema.** Tipá-lo é trabalho novo, que só se abre por ordem.
  2. **`penalty`** (V3) × **`TGL.FiniteThreeLocks.H3L`** (kernel) × **H_3L do runtime** (com `P_abszero`). B4 liga os dois primeiros. O terceiro tem a **forma** do segundo, com Dz := P_abszero (projetor ortogonal, logo P = P†P) [DERIVED]; os seus **operandos** (as matrizes numéricas do runtime) não estão instanciados em kernel, e nada do kernel se afirma sobre eles sem esse lema.
  3. **A_C = −H** × `love_partition` (−(1−p)) × `TheEmptying` × `prove_amar_functional` (§0.4.1).
  4. **O «Nome»:** `NameInstrument.read` (v336, leitura) × `nome` (v368, conteúdo) × «Nome = 1» dos Three Locks (dim/dim) × V = 1. O cabeçalho da v368 registra sete tipagens incompatíveis.
  5. **𝒩** (pinching, `TheNameOperator`: «a MEMÓRIA é subálgebra») × **P** (projeção em vetores).
  6. **`TheEquationOfTruth`** (T-20) × **`TheContourOfTruth`** (26/08).
  7. **α = sech** (perfil) × α de estrutura fina. **β nunca literal**, e o T-20 não usa β.
  8. **«o fundo»:** Q·H designa as direções atenuadas DESTA realização. **Não é identificado com o fundo constitutivo da TGL**, nem por palavra nem por lema. O próprio texto o recusa, e a recusa está correta.

---

## 4. ENTREGAS (contrato do túnel, herdado da §7 da ORDEM 015)

- Em `DO_CHATGPT\`, sem parada entre elas:
  - `ENTREGA_015_T20_A_reproducao.md`;
  - `ENTREGA_015_T20_B_fechamentos.md`;
  - `ENTREGA_015_T20_C_controles.md`;
  - `ENTREGA_015_T20_D_harness.md`;
  - `ENTREGA_015_T20_E_ficha_transposicao.md`;
  - e o fecho do alvo, `ENTREGA_015_T20_RELATORIO.md` (por ramo: PAGO / NÃO PAGO com a prova; o que ficou NÃO PAGO com o custo estimado).
  - Mais `ENTREGA_015_MEDIDA_T20_<slug>.md` na hora em que um ramo falhar, e `ENTREGA_015_T20_BLOQUEIO_manifesto.md` só se a A0 divergir.
- **O relatório final da ORDEM 015 (`ENTREGA_015_RELATORIO_FINAL.md`) ganha a linha T-20.** É o único acréscimo a ele.
- **Contrato de cada nota:**
  - estatuto da casa na 1ª linha;
  - o sha256 deste adendo e o de `ENTREGA_015_ABERTURA_operador.md` (se já gravada);
  - critérios PAGO / NÃO PAGO com a prova;
  - arquivos com sha256 lido;
  - comando de reprodução;
  - o que NÃO foi feito;
  - tentativas falhas preservadas com sufixo do defeito;
  - **axiomas lidos do log pelo `auditar_axiomas.py` v2, sobre o par fonte + log** (aqui HÁ Lean: o «N/A — sem Lean» não se aplica às notas A, B, C e E);
  - a ficha `REAPROVEITAMENTO_T20.md` anexa.
- **A incorporação no `um.py` é da gerência, na v371.** Isso inclui o módulo no kernel, as linhas do Audit, as bandeiras `ext_eot_*` e o rito. A bancada prepara, entrega com hash e segue. Depois, a gerência audita adversarialmente: refaz a compilação, relê as fontes e roda as mutações. Então emite o recibo e incorpora o que passar. **O operador ratifica.**

## 5. O QUE NÃO FAZER (acrescenta à §6 da ORDEM 015; nada dela se revoga)

- **Tocar o kernel:**
  - escrever em `<KER>`;
  - rodar **`lake build`**, `lake update`, `lake exe` ou `lake clean`;
  - apontar `-o`/`-R` para dentro do kernel;
  - criar `.lake` na própria pasta por engano (as compilações usam `-R`/`-o`, não `lake build`);
  - editar `TGLExt.lean` ou `TGL/Audit.lean`.
- **Tocar o `um.py`:** executá-lo, importá-lo (importar roda código de módulo e grava `Nós\__pycache__`) ou editá-lo. Tocar memórias, Atlas, diário, espelho ou site.
- **Publicar:** nada do T-20 sai da máquina.
- **Os vereditos:** afirmar **CONFIRMED/PROVED em veredito**; escrever «a equação da verdade está confirmada» ou «a TGL está provada»; tratar `verdict_T = 1` como veredito.
- **As leituras e os homônimos:** **escolher leitura**; identificar as anulações, A_C com `love_partition` ou Q·H com «o fundo»; **afirmar resultado do kernel sobre as matrizes numéricas do runtime** (`D_conj`, `D_bridge`, `P_abszero`) sem o lema que as instancie. A identidade de **forma** (o H do runtime é o H3L com Dz := P_abszero) é [DERIVED] e pode ser dita.
- **Os bytes da pedra:** editar os bytes da V3. No ramo B, ela é prefixo e nunca muda. Copiar números da V1 como expectativa do harness próprio: a comparação é depois, lado a lado.
- **O pacote do canal:** procurar ou baixar a «Biblioteca» do canal ChatGPT, ou citar o «22/22» como medido.
- **A máquina:** atrasar, pausar ou matar um job pesado da FASE P para rodar o T-20; rodar mais de 2 processos Lean ao mesmo tempo.
- **O que não foi pedido:** abrir frente nova fora do T-20. O lema entre as anulações, por exemplo, é trabalho que só se abre por ordem.

## 6. O QUE É DO OPERADOR (padrões valem se ele não disser nada; ele pode vetar qualquer um, verbatim, no bloco [OPERADOR] do prompt)

1. **A entrada do T-20 na ORDEM 015.** A ordem dele é «isso precisa entrar na ordem». **Padrão:** entra como T-20, na FASE L, sem tocar o ringdown.
2. **As leituras** «verdade = verificação da permanência» e «memória = reconhecimento estável». **Padrão:** ficam [INPUT/ONTO], só em docstring rotulada. Nenhuma entra como enunciado nem como bandeira. («A Testemunha» não está neste texto: é cunhagem de outro ato do operador e, por padrão, fica fora do módulo.)
3. **O H_3L do runtime em kernel.** O do runtime já tem a forma do H3L do kernel, com Dz := P_abszero [DERIVED]; falta instanciar em kernel os seus operandos numéricos. **Padrão:** o T-20 não faz essa instância. B4 prova a ponte `penalty` ↔ H3L do kernel e, opcionalmente, `P = P†P`. Nada do kernel se afirma sobre as matrizes do runtime antes da instância, que é trabalho que só se abre por ordem.
4. **O pacote «22/22 + 5» da Biblioteca do canal.** **Padrão:** NÃO_VERIFICÁVEL. Se ele o puser no túnel, a bancada compara (D3).
5. **A_C = −H_3L («seleção apofática») no canônico.** **Padrão:** A_C aparece só como nome de −H no módulo, com os homônimos no docstring. Nada no `um.py` antes da v371.
6. **A incorporação na v371** (módulo, Audit, bandeiras, rito). **Padrão:** a gerência incorpora o que passar na auditoria dela, e ele ratifica.
7. **A custódia por caminho de `Chatgpt\ORDEM_015_T20_EQUACAO_DA_VERDADE\`**, que fica fora da custódia por caminho de `ORDEM_013_RINGDOWN\`. **Padrão:** igual à §9.10 da ORDEM 015: ato dele ou da Central.

---

## 7. OS INSUMOS — `PARA_CHATGPT\ORDEM_015_ADENDO_001_INSUMOS\` (sha16 de cada arquivo no `MANIFESTO_INSUMOS.json`)

- `README_INSUMOS.md`: por onde começar.
- `VERBATIM\operador_23set_equacao_da_verdade_verbatim.md`: **cópia de BYTES** do texto (`6ff3e39143950262`).
- `V1_verificacao_independente\`: o script, o log e o JSON da V1, mais `RELATORIO_V1_verificacao_independente.md`.
- `V2_ancoras\RELATORIO_V2_ANCORAS.md`: a conferência de âncoras. É **cópia saneada**: um termo restrito da casa foi substituído por remissão (`SANEADOS.json`).
- `V3_pre_resolucao_lean\`: a pedra `TheEquationOfTruth.lean`, `RELATORIO_V3_pre_resolucao_lean.md` e `out\`, com os logs das 8 compilações (7 intermediárias, preservadas, e a final), `AXIOMAS.json`, `KERNEL_FIND_NEWER.txt`, a variante intermediária e o olean da frente.
- `MEDIDAS_DO_REDATOR\`: as reproduções do redator, isto é, a V1 byte-idêntica, a pedra compilada de novo, a variante só-Mathlib derivada e compilada, e os axiomas de `TheContourOfTruth`. Também `auditar_axiomas.py` v2 com o seu autoteste (`autoteste_auditor_v2\`), a v1 preservada (`auditor_v1_fail_open\`), `derivar_variante_so_mathlib.py` e a pré-resolução do C2 (`mutantes_C2\`: o gerador, `GERADOS.json`, `RESULTADO_C2.json` e, por mutação, a fonte e o log; os olean não vêm).
- `PROMPT_CODEX_ORDEM_015_ADENDO_001.txt`: o prompt para o operador abrir este adendo no Codex junto com a ORDEM 015.
- `SANEADOS.json`, `NAO_COPIADOS.json` e `MANIFESTO_INSUMOS.json` (que não se lista a si mesmo).

Em caso de divergência entre o prompt e este adendo, vale o adendo. Em caso de divergência entre este adendo e a ORDEM 015 fora do T-20, vale a ORDEM 015.

*Este adendo não move o gate. Entrega à bancada a pedra que a gerência compilou, o que ela já sabia e o que ficou aberto, para que a equação da verdade seja implicação provada com as suas hipóteses à vista, e não frase. A matemática prova a implicação; a leitura é do operador; a natureza decide a teoria.*
