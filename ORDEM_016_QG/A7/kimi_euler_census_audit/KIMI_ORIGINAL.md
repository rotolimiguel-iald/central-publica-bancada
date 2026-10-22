# A7.b — Descendente com inserção $E_h\,[G,\chi]\,w$: censo de grafos a dois vértices, colapso de linha e contatos locais

**Unidade científica nova — uma pergunta. Resultado `[DECLARADO]` até auditoria local.**
Documento textual: nenhum arquivo alterado, nenhuma execução de CAS ou ferramenta alegada. Auxiliar **euclidiano** $\mathbb{R}^4$; nenhuma identificação automática com a teoria lorentziana. Estatutos preservados: `[INPUT]` (dados do enunciado e da fonte local), `[HIPÓTESE]`, `[DECLARADO]`, `[VERIFICADO LOCAL]` (as identidades do arquivo de convenções, verificadas por CAS *na fonte*, não aqui), `[OPEN]`. `NOT_FALSIFIED ≠ CONFIRMED`.

---

## 1. Dados `[INPUT]` e hipóteses de convenção `[HIPÓTESE]`

**Campos** (paridade, número fantasma gh): $h_{\mu\nu}$ (par, 0), $b_\mu$ (par, 0), $c_\mu$ (ímpar, +1), $\bar c_\mu$ (ímpar, −1); antifields-fonte $h^\dagger$ (ímpar, −1), $c^\dagger$ (par, −2) — **fontes sem propagadores**.

**Operadores e transformações** `[INPUT]`: $Gc=\partial_\mu c_\nu+\partial_\nu c_\mu$; $Ch=\partial_\mu h_{\mu\nu}-\partial_\nu\,\mathrm{tr}\,h/2$; $Z=L_c h$, $w=c\cdot\partial c$; $s_0h=Gc$, $s_0c=0$, $s_0\bar c=-b$, $s_0b=0$; $s_1h=Z$, $s_1c=w$; $s_0Z=-Gw$ (consequência de $\{s_0,s_1\}=0$ sobre $h$, algebricamente verificável). $S_0=\tfrac12\langle h,Hh\rangle+\langle b,Ch\rangle-\langle b,b\rangle/2\ell+\langle\bar c,Qc\rangle$, com $Q=\Box$ euclidiano (convenção BV069: o símbolo de Fourier carrega $i^2$ em separado). $V_{\mathrm{af},\chi}=\int\chi(h^\dagger Z+c^\dagger w)$, $s_0h^\dagger=E_h$, $s_0c^\dagger|_{h^\dagger}=-G^*h^\dagger$.

- **H1 — Euler completo e eliminação de $b$.** $E_h:=\delta S_0/\delta h$ **inclui o setor $b$**: com $(C^\dagger b)_{\mu\nu}=-\partial_{(\mu}b_{\nu)}+\tfrac12\eta_{\mu\nu}\,\partial\!\cdot\!b$ (adjunto computado na pareação $\langle\cdot,\cdot\rangle$; sinal a travar — L3),
$$E_h^{\mu\nu}=(Hh)^{\mu\nu}-\partial^{(\mu}b^{\nu)}+\tfrac12\eta^{\mu\nu}\partial\!\cdot\!b .$$
A equação algébrica $E_b:=\delta S_0/\delta b=Ch-b/\ell=0\Rightarrow b=\ell Ch$ dá $E_h=G_F h$, $G_F:=H+\ell C^\dagger C$. A abreviatura antiga "$E_h=Hh$" está **falsificada pela convenção livre** (`wrong_free = 40 ≠ 0`, `[VERIFICADO LOCAL]` na fonte). As apresentações (bloco $(h,b)$ / $b$ eliminado) são equivalentes no nível livre; adoto $b$ eliminado.
- **H2 — Propagadores.** $P_h$ com $P_hG_F=I\delta$ (dado pelo enunciado); $P_c$ com $QP_c=I\delta$ (sinal a travar — L3). **Não há** linhas $h^\dagger$–, $c^\dagger$–, $c$–$c$, $\bar c$–$\bar c$, $h$–$c$, $h$–$\bar c$, $h$–$b$ (após eliminação). Não se inventa propagador de antifield.
- **H3 — Ordenamento normal.** Vértices normal-ordenados $:\!V_i\!:$ (§7).
- **H5 — $\chi$** escalar liso inerte; exponenciais apenas marcadores de jato.
- **H6 — Vértices** $V_1:=\int\chi h^\dagger Z$, $V_2:=\int\chi c^\dagger w$, $V_3:=V_{\mathrm{gh},\chi}$ (pré-IBP $\int\chi\bar c\,CZ$; pós-IBP $-\int[\chi\,\partial_\mu\bar c_\nu+(\partial_\mu\chi)\bar c_\nu]\bar Z^{\mu\nu}$, $\bar Z=Z-\tfrac12\eta\,\mathrm{tr}Z$).
- **H7 — Posição da inserção (a travar).** A inserção $I:=\int E_h\,[G,\chi]\,w$ é o pedaço de comutador-$\chi$ de $s_0(\text{Termo }A)$, pois $\chi\,Gw=G(\chi w)-[G,\chi]w$; identidade-elo declarada e verificável, ver §5.
- **H8 — Convenção de fontes fixada.** Se se usarem antifields canônicos diferentes, a transformação de sinal (p.ex. $(b,c^\dagger)\mapsto(-b,-c^\dagger)$ com os flips induzidos) deve ser **explicitada** e jamais reinterpretada como mudança de loop físico (ordem do enunciado; L6).

---

## 2. O objeto e seus invariantes formais

$$I=\int E_h^{\mu\nu}\,[G,\chi]_{\mu\nu}{}^{\sigma}\,w_\sigma,\qquad [G,\chi]w=(\partial_\mu\chi)\,w_\nu+(\partial_\nu\chi)\,w_\mu=2\,\partial_{(\mu}\chi\,w_{\nu)} ,$$
pois $G$ é de primeira ordem (símbolo $\sigma_G(\partial\chi)$). Portanto: suporte em $\partial\chi$; $\mathrm{gh}(I)=2$; paridade par. **Controle estrutural: $\chi\equiv$const $\Rightarrow I=0$.** $w=c\cdot\partial c$ no mesmo ponto é composto — sua normalização própria é L5. $s_0w=0$; $s_0E_h=0$ (de $s_0S_0=0$ por invariância de gauge livre e $s_0$ comutando com $\delta/\delta h$ no sentido declarado), logo $s_0I=0$ no nível livre — cociclo candidato; a consistência homogênea é L2, **não** assumida.

---

## 3. Censo de bubbles de duas linhas (2 vértices, 2 linhas internas)

Conteúdo propagante: $V_1\sim h^\dagger+(c,h)$; $V_2\sim c^\dagger+(c,c)$; $V_3\sim\bar c+(c,h)$. Linhas disponíveis: $h$–$h$ via $P_h$; $c$–$\bar c$ via $P_c$ (orientada). **Antifields não contraem.**

| par | contrações possíveis | veredito |
|---|---|---|
| $(V_1,V_1)$ | $h$–$h$ (1); $c$–$c$ ✗ | **impossível** (1 linha < 2) |
| $(V_1,V_2)$ | nenhuma dupla | **impossível** |
| $(V_2,V_2)$ | $c$–$c$ ✗ | **impossível** |
| $(V_2,V_3)$ | $c$–$\bar c$ (1); $c$–$h$ ✗ | **impossível** (contração simples = árvore, não loop) |
| $(V_1,V_3)$ | $h$–$h$ **e** $c$–$\bar c$ | **$\Gamma_a$** (externos $h^\dagger,c$) |
| $(V_3,V_3)$ | $\{c$–$\bar c,\ h$–$h\}$ | **$\Gamma_b$** (externos $\bar c,c$) |
| $(V_3,V_3)$ | $\{c$–$\bar c,\ \bar c$–$c\}$ | **$\Gamma_c$** (externos $h,h$) |
| $(V_3,V_3)$ | $\{h$–$h,\ h$–$h\}$ | **impossível** (um $h$ por vértice) |

**Tadpoles** (1 vértice): $V_3$ auto $c$–$\bar c$ existe e é eliminado por H3 (§7); $V_1,V_2$: nenhum.

**Bubbles que só aparecem após variação BV.** Com Leibniz graduado ($\varepsilon(h^\dagger)=1$):
$$s_0V_1=\int\chi\,E_h Z+\int\chi\,h^\dagger G w\;=:\;\text{Termo }A+\text{Termo }B,\qquad s_0V_2\supset\underbrace{-\!\int\!\chi(G^*h^\dagger)w}_{\text{Termo }B'}+\underbrace{\int\!\chi(Q^{T}\bar c)\,w}_{\text{Termo }C}$$
($s_0w=0$; sinal de $Q^T$ a travar — L3).

| par | contrações | veredito |
|---|---|---|
| $A=(h/b,c,h)$ × $V_3$ | $(h/b)$–$h$ **e** $c$–$\bar c$ | **$\Gamma_d$** (externos $(h/b),c$) — **só pós-variação** |
| $A$ × $A$ | duas linhas $h$-tipo | **$\Gamma_f$** (externos $c,c$) — **só pós-variação**; sem $\partial\chi$ ⇒ setor Ward **não-localizado**, fora do descendente (§8) |
| $B,B'$ = $h^\dagger+(c,c)$ × qualquer | no máx. 1 linha | **impossível** |
| $C=\bar c+(c,c)$ × $V_3,A,V_1,C$ | no máx. 1 linha | **impossível** |
| $I=(h/b,c,c)$ × $V_3$ | $(h/b)$–$h$ **e** $c$–$\bar c$ | **$\Gamma_e$** (externos $c,c$) |
| $I$ × $V_1,V_2,A$ | sem $\bar c$ ou sem 2ª linha | **impossível** |

**Fecho do censo** `[DECLARADO]`: bubbles de duas linhas existentes = $\{\Gamma_a,\Gamma_b,\Gamma_c\}$ pré-variação; $\{\Gamma_d,\Gamma_e,\Gamma_f\}$ só pós-variação BV. Todo o resto é impossível por contagem de campos com antifields sem propagadores.

---

## 4. ħ, sinais ímpares e pesos `[DECLARADO — sinais a travar em auditoria, L3]`

| grafo | ħ | linhas | sinal | peso | externos |
|---|---|---|---|---|---|
| $T_0=I$ | $\hbar^0$ | — | — | 1 | $(h/b),c,c$ |
| $\Gamma_a$ | $\hbar^1$ | $h$ + fantasma | $-$ (loop com 1 propagador ímpar) | 1 | $h^\dagger,c$ |
| $\Gamma_b$ | $\hbar^1$ | $h$ + fantasma | $-$ | 1 | $\bar c,c$ |
| $\Gamma_c$ | $\hbar^1$ | 2 fantasmas | $-1$ (loop ímpar fechado) | $\tfrac12$ (vértices idênticos) | $h,h$ |
| $\Gamma_d$ | $\hbar^1$ | $h$ + fantasma | $-$ | 1 | $(h/b),c$ |
| $\Gamma_e$ | $\hbar^1$ | $h$ + fantasma | $-$ | 1 (normalização própria de $I$: L5) | $c,c$ |
| $\Gamma_f$ | $\hbar^1$ | 2 linhas $h$ | $+$ (loop bosônico) | $\tfrac12$ | $c,c$ |

Sinais graduados adicionais: Leibniz de $s_0$ (acima), reordenação de campos ímpares na escrita dos vértices, adjuntos euclidianos com $i^2$ em separado (convenção BV069).

---

## 5. Colapso de linha com $P\,G_F=I\delta$; o produto remanescente na diagonal

Onde $E_h$ aparece (Termo $A$, $I$, ou via $s_0h^\dagger$), o campo $h$ de $E_h=G_Fh$ contrai com o $h$ de $V_3$:
$$\big\langle G_F^{(x)}h(x)\,h(y)\big\rangle=G_F^{(x)}P_h(x,y)=I\,\delta^4(x-y)\quad\Rightarrow\quad\text{a linha }h\text{ COLAPSA num contato.}$$
Cada grafo com $E_h$ decompõe-se, de forma **separada e declarada**:
$$\Gamma=\Gamma^{\mathrm{reg}}+\Gamma^{\mathrm{ct}},\qquad \Gamma^{\mathrm{ct}}=\kappa\!\int d^4x\;\chi(x)\,A\big[\partial\chi;\,G_F,C,L\text{-operadores}\big]\;N_c^{\mu\nu}(x)\,(\text{campos externos locais}),$$
$$N_c^{\mu\nu}(x):=\big\langle c^\mu(x)\,\bar c^\nu(x)\big\rangle_{\mathrm{ren}}\;=\;\text{o PRODUTO REMANESCENTE NA DIAGONAL, com normalização independente (input de renormalização).}$$
**Não se assume $f(0)=0$** (proibido pelo enunciado). $\Gamma^{\mathrm{reg}}$ = o mesmo bubble com a linha $h$ fora da diagonal; a prescrição de subtração que o define (point-split/Hadamard) é L7. $\kappa$ é coeficiente da álgebra de vértices — **não computado nesta rodada** (sem CAS); nenhum cancelamento numérico é prometido (não há números fornecidos). Colapso no setor fantasma ($QP_c=I\delta$) só ocorreria via fator $Q\bar c$ num vértice (Termo $C$), que não gera bubbles (§3): **nenhum colapso adicional a dois vértices** `[DECLARADO]`.

**Identidade-elo (H7, verificável):** $s_0(\text{Termo }A)=\int\chi\,E_h\,s_0Z=-\int\chi\,E_h\,Gw=-\int E_h\,[G,\chi]w-\int E_h\,\chi\,Gw$ — a inserção $I$ é exatamente o pedaço de comutador-$\chi$; correspondentemente $\Gamma_e$ é o pedaço $[G,\chi]$ dos grafos $s_0\Gamma_d$. Isto posiciona o descendente na rede BV sem anunciar obstrução.

---

## 6. Fórmula-esqueleto (kernels livres e vértices dados)

Com $V_3$ pós-IBP, $\mathcal D^{(\mu)}(y):=\chi(y)\partial_\mu+(\partial_\mu\chi)(y)$:
$$\Gamma_e=-\,\kappa_e\!\int_x\!\int_y\Big[E_h^{\partial}(x)\,2\partial_{(\mu}\chi(x)\,w_{\nu)}(x)\Big]_{\text{3 campos}}\;P_h^{(h)\leftrightarrow(h\text{ em }Z)}(x,y)\;P_c^{(c\text{ em }w)\leftrightarrow(\bar c)}(x,y)\;\Big[\mathcal D^{(\mu)}(y)\,\bar Z^{\mu\nu}(y)\Big]\;c^{\mathrm{ext}}(x)\,c^{\mathrm{ext}}(y)\;\;+\;\Gamma_e^{\mathrm{ct}}[N_c],$$
e analogamente $\Gamma_d$ (com Termo $A$ no lugar de $I$), $\Gamma_a,\Gamma_b,\Gamma_c$. Cada símbolo é **lido dos dados**: $E_h^\partial=G_F=H+\ell C^\dagger C$; $Z=L_ch$; $\bar Z=Z-\tfrac12\eta\,\mathrm{tr}Z$; nenhum propagador de antifield; $N_c$ separado. Com $V_3$ pós-IBP, cada bubble cinde em pedaço $\chi\chi$ e pedaço $\partial\chi$: $\Gamma^{\partial\chi}$ é contribuição **ao descendente**; $\Gamma^{\chi\chi}$, à identidade Ward não-localizada (separação exigida pelo controle C2).

---

## 7. Ordenamento normal × contatos com EOM — o que é compatível e o que falta verificar

- **Ordenamento normal** elimina **autocontrações no mesmo vértice** (tadpoles $\to0$) e nada mais. É **compatível** com todas as identidades `[VERIFICADO LOCAL]` da fonte (clássicas/polinomiais: comutadores diferenciais $[C,\chi]$ sobre $\bar Z$, nilpotência graduada polarizada em duas ondas planas ímpares, identidade de borda fantasma, $J_{\mathrm{gf}}^\mu$) — nenhuma delas toca loops ou $N_c$.
- **Produtos temporais com inserções de EOM** ($E_h$, $E_b$, $Q\bar c$) **não** são removidos pelo ordenamento normal: geram contatos via $P\,G_F=I\delta$ (§5). As duas operações são distintas e não se substituem — exatamente a distinção pedida.
- **Ainda a verificar:** (i) consistência homogênea do setor externo de kernels de contato $(h,c)$ para $\chi$ variável — **não demonstrada** (enunciado); não anunciar obstrução cohomológica por resíduo isolado; (ii) tabela de sinais de adjuntos ($Q^T,G^*,C^\dagger$) e a ordem $G_FP_h$ vs $P_hG_F$; (iii) relação entre $\kappa_d,\kappa_e$ e os membros $\langle b,[C,\chi]Z\rangle$, $\langle\bar c,[Q,\chi]w\rangle$ — **sem promessa de cancelamento**; (iv) se a normalização de $w$ no mesmo ponto (L5) se esgota no ordenamento normal.

---

## 8. Receita finita implementável (R1–R8) `[DECLARADO — sem execução nesta rodada]`

- **R1** Fixar H1–H8 e a tabela de sinais (L3) num pré-registro local.
- **R2** Gerar $V_1,V_2,V_3$ dos dados; derivações funcionais **antes** de pôr fontes a zero; fontes $\to0$ **após** (ordem do enunciado).
- **R3** Enumerar pares; aplicar o censo (§3); podar impossíveis.
- **R4** Vestir linhas com operadores; escrever $\Gamma_a,\Gamma_b,\Gamma_c$ simbolicamente.
- **R5** Aplicar variação BV onde indicado; recontar; incluir Termo $A$ ($\Gamma_d,\Gamma_f$); excluir $B,B',C$ por contagem.
- **R6** Aplicar o colapso $P\,G_F=I\delta$; separar $\Gamma^{\mathrm{ct}}$ com $N_c$ **sem** $f(0)=0$; explicitar a subtração de $\Gamma^{\mathrm{reg}}$ (L7).
- **R7** Rodar os controles $\chi$-constante (C1–C4, §9).
- **R8** Confrontar os lados da identidade Ward; registrar compatibilidades e lacunas; **selar como `[DECLARADO]`**.

---

## 9. Controles de $\chi$ constante (obrigatórios)

- **C1** $\chi\equiv\chi_0\Rightarrow[G,\chi]=[C,\chi]=[Q,\chi]=0\Rightarrow I=0$ e **todo** item do descendente deve anular: cada contribuição listada deve carregar $\partial\chi$ ou $[\cdot,\chi]$ explícito ($T_0$ ✓ via $[G,\chi]$; $\Gamma_e$ ✓; $\Gamma_d^{\mathrm{ct}}$ deve carregar $\partial\chi$ via $A$ — se não carregar, há erro).
- **C2** $\Gamma_a,\Gamma_b,\Gamma_c,\Gamma_f$ **não** se anulam em $\chi$ const: pertencem à identidade Ward **não-localizada** (correções de loop), **não** ao descendente — a separação é exigida.
- **C3** Pré-IBP × pós-IBP de $V_3$ devem dar o mesmo descendente **módulo** a identidade $[C,\chi]$ `[VERIFICADO LOCAL]` — teste cruzado obrigatório.
- **C4** Jatos: exponenciais só marcadores; resultado polinomial em jatos × $\partial\chi$; nenhum kernel não-local além de $P_h,P_c$ nos bubbles e de $N_c$.

---

## 10. Lacunas específicas `[OPEN]`

- **L1** $N_c$ (e $N_h$, se aplicável): normalização independente, não fornecida; separada por construção.
- **L2** Consistência homogênea do setor externo $(h,c)$ para $\chi$ variável: **não demonstrada**; nenhuma obstrução cohomológica anunciada por resíduo isolado (ordem literal do enunciado).
- **L3** Tabela de sinais de adjuntos euclidianos e ordem $G_FP_h$ vs $P_hG_F$: a travar.
- **L4** Setor antifield completo ($\bar c^\dagger,b^\dagger$) e contrações de corrente quântica: fora de escopo (como na fonte: `full_Q2=False`); diagramas mistos $b$–$h$ e de corrente fantasma permanecem.
- **L5** Normalização própria de $w=c\cdot\partial c$ no mesmo ponto: a verificar se se esgota no ordenamento normal.
- **L6** Transformação de sinais entre antifields canônicos: a exibir quando usada; nunca reinterpretar como mudança de loop físico.
- **L7** Prescrição de subtração que define $\Gamma^{\mathrm{reg}}$ (point-split/Hadamard): a explicitar.
- **L8** $s_1\bar c$, $s_1 b$, $s_1E_h$: não fornecidos; necessários para nilpotência completa além do nível livre.
- **L9** Dressing dos kernels ($\Gamma_b,\Gamma_c$ renormalizam $P_c,P_h$): fora do censo estrito; declarado.

## 11. O que **não** se afirma

Sem propagador de antifield inventado; sem $f(0)=0$; sem obstrução cohomológica por resíduo isolado; sem cancelamento de resíduo numérico (não fornecido); sem resposta numérica desejada; sem refazer a corrente de campo em $X/Y$ nem o tadpole ordinário com referência variável (outras unidades); sem identificação com a teoria lorentziana; sem alteração de arquivos; sem execução de CAS nesta rodada; resultado **`[DECLARADO]` até auditoria local**; `NOT_FALSIFIED ≠ CONFIRMED`.

## 12. Resultado (uma linha)

A dois vértices: ao **descendente** ($\partial\chi$-suportado, gh 2, inserção $E_h[G,\chi]w$ com $E_h=G_Fh$ **completo**) contribuem a árvore $T_0=I$, o bubble $\Gamma_e$ ($I\times V_3$), os pedaços $\partial\chi$ dos bubbles $\Gamma_a,\Gamma_d$, e os contatos colapsados $\propto N_c$; à **identidade Ward** (não-descendente) contribuem $\Gamma_a,\Gamma_b,\Gamma_c$ e, **só após variação BV**, $\Gamma_d$ (e $\Gamma_f$ no setor não-localizado); **todos os demais bubbles de duas linhas são impossíveis por contagem de campos com antifields sem propagadores** — com $N_c$ separado, sem $f(0)=0$, e as lacunas L1–L9 nomeadas.