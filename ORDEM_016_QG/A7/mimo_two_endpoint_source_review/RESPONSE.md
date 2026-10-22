# A7.b — UNIDADE CIENTÍFICA NOVA: REVISÃO INDEPENDENTE DE IDENTIDADES DISTRIBUCIONAIS
### Pergunta única: o contato exato (sinais corretos) entre *localizar-e-estender* e *estender-e-localizar*

---

## 0. Regime, escopo e conformidade

- **REGIME:** `DECLARADO até verificação`. Toda a derivação abaixo é **manual, nesta resposta**. **Nenhuma ferramenta foi executada**, nenhum arquivo de código da bancada foi anexado ou lido, **nenhum resultado computacional é alegado**. Nada aqui é `PROVED`/`CONFIRMED` no sentido da régua da casa: é derivação sujeita a revisão independente.
- **CONFORMIDADE:** não substituo tarefa Kimi; não reenvio tarefa MiMo terminal; **a prescrição não foi modificada**; nenhum contato extra é adicionado à adjunção de distribuições já estendidas; nada é inferido sobre soma de bolhas ou Q2 interagente completa; **nenhum estado físico, Lorentz, contratermo novo ou outro ramo é introduzido**.
- **Separação exigida:** §3 = regra abstrata (qualquer fonte); §4 = exemplo quantitativo.
- Fontes usadas: **apenas os dados fornecidos** na prescrição + o confronto com a fórmula clássica de resíduo de Riesz (usado só como *checagem de consistência*, §2.4).

---

## 1. Convenções e dados `[INPUT]`

$x = X - Y$, $z = x^2$, 4D euclidiano. Derivadas: $\partial_{X_i} = \partial_{x_i}$; $\partial_{Y_i} = -\partial_{x_i}$ sobre a dependência singular em $x$.

**Leitura operacional de $R$** (a única que reproduz `Res(z^{a-n})` do enunciado):
$$\mathscr R[F] \;=\; \mathrm{FP}_{a=0}\big[(1-a)\mu^{2a} z^{a} F\big],$$
de modo que $F = z^{-n}$ dá $\mathrm{FP}_{a=0}[(1-a)\mu^{2a}z^{a-n}]$. $R$ comuta com multiplicação suave. Contato: $C_D(f) := R(Df) - D R(f)$.

**Resíduo (dado):** $\mathrm{Res}(z^{a-n})/C_E^{\rm esc} = -\dfrac{(q^2)^{n-2}}{4^{n-1}(n-1)!(n-2)!}$, $n\ge 2$, com **$C_E^{\rm esc} = -4\pi^2$ fator escalar, não o operador $C_E$**; $q \leftrightarrow \partial\delta$ (não momento Fourier sem $i$); $x_i \leftrightarrow -\partial_{q_i}$.

Logo, com $\rho_p := \mathrm{Res}_{a=0} z^{a-p}$:
$$\boxed{\;\rho_p = \frac{\pi^2}{4^{p-2}(p-2)!(p-1)!}\,\Box^{p-2}\delta(x) = C_E^{\rm esc}\cdot\frac{-(q^2)^{p-2}}{4^{p-1}(p-1)!(p-2)!}\;}$$

---

## 2. A régua de contato de $R$ `[DERIVED — manual; DECLARADO até verificação]`

### 2.1 Fórmula mestre
Como $z^a\partial_k F - \partial_k(z^aF) = -2a\,x_k z^{a-1}F$ e $w(a)=(1-a)\mu^{2a}$ vale $w(0)=1$, o fator $a$ explícito mata o polo e **o contato é o resíduo** (independente do $(1-a)\mu^{2a}$; o $w'(0)=-1+2\ln\mu$ só desloca os *finite parts*, e cancela — checado em 1ª e 2ª ordem):
$$C_{\partial_k}(F) = -2\,\mathrm{Res}_{a=0}\big[x_k z^{a-1}F\big],\qquad
C_{\partial_k\partial_l}(F) = -2\,\mathrm{Res}_{a=0}\big[x_kz^{a-1}\partial_lF + x_lz^{a-1}\partial_kF + \delta_{kl}z^{a-1}F + 2(a-1)x_kx_lz^{a-2}F\big].$$

### 2.2 Tabela (base de monômios $F = x_I z^{-n}$, $|I|=m$)
$$\textbf{(C1)}\;\; C_{\partial_{Y_k}}(F) = +2\,x_k x_I\,\rho_{n+1} = -\,C_{\partial_{X_k}}(F)$$
$$\textbf{(C2)}\;\; C_{\partial_k\partial_l}(F) = -2\Big\{\big[\textstyle\sum_s(\delta_{li_s}x_k+\delta_{ki_s}x_l)x_{I\setminus i_s} + \delta_{kl}x_I\big]\rho_{n+1} - (4n+2)\,x_kx_lx_I\,\rho_{n+2}\Big\}$$
$$\textbf{(C3)}\;\; z\,\rho_{p+1} = \rho_p,\qquad \partial_{x_i}\rho_p = -2p\,x_i\rho_{p+1},\qquad x_i\rho_{p+1} = -\tfrac{1}{2p}\partial_i\rho_p,\qquad x_i(\cdot) \leftrightarrow -\partial_{q_i}(\cdot)$$

### 2.3 Checagens (todas à mão)
- **$n=1$:** $C_{\partial_k}(z^{-1}) = -2x_k\rho_2 = -2\pi^2 x_k\delta = 0$ — correto, $z^{-1}$ é localmente integrável em 4D, $R=\mathrm{id}$.
- **$n=2$, 1ª ordem:** $C_{\partial_{X_1}}(z^{-2}) = -2x_1\rho_3 = \tfrac{\pi^2}{2}\partial_1\delta$ — recalculado por duas rotas independentes (expansão de Laurent explícita), com a correção $\partial_1 T^{(0)}_2 = -4x_1T^{(0)}_3 + 2x_1\rho_3$ (o termo $2x_1\rho_3$ é o que a rota apressada perde).
- **$n=2$, 2ª ordem:** $C_{\partial_1\partial_1}(z^{-2}) = -2\rho_3 + 20 x_1^2\rho_4$ — recalculado explicitamente; coincide com (C2) para $m=0$.
- **Consistência do resíduo dado:** $\mathrm{Res}_{a=0}z^{a-n}$ reproduz a fórmula clássica de Riesz $\frac{\pi^2}{4^{n-2}(n-2)!(n-1)!}\Box^{n-2}\delta$; $n=2 \Rightarrow \pi^2\delta$.

---

## 3. REGRA ABSTRATA (qualquer fonte)

Fonte sem cutoff: $S = A_{uv,r}c^r + B^j_{uv,r}\partial_{Y_j}c^r = C_{uv,r}c^r + \partial_{Y_j}(B^j_{uv,r}c^r)$, com $C = A - \mathrm{div}_Y B$. Cutoffs **independentes** $\chi_X(X)$, $\chi_Y(Y)$.

$$U := \chi_Y C - (\partial_{Y_j}\chi_Y)B^j = \chi_Y A - \partial_{Y_j}(\chi_Y B^j),\qquad
T := \chi_Y R(A) - \partial_{Y_j}\big(\chi_Y R(B^j)\big).$$

**Identidade-chave:** $K := \sum_j C_{\partial_{Y_j}}(\chi_Y B^j)$ e $T = R(U) + K$ (verificação termo a termo, sinais +/− como nas definições).

Como $R$ comuta com $\chi_X$ (suave): $\chi_X R(U) = R(\chi_X U)$; logo $E_X(\chi_X R(U)) = R(E_X(\chi_XU)) - C_E(\chi_X U)$ e

$$\boxed{\;P - Q \;=\; E_X\Big[\chi_X \sum_j C_{\partial_{Y_j}}\big(\chi_Y B^j\big)\Big] \;-\; C_E\Big(\chi_X\big[\chi_Y C - (\partial_{Y_j}\chi_Y)B^j\big]\Big)\;}$$

**Ordem preservada:** no 1º termo $E$ age **depois** do contato (objeto já estendido, suporte $x=0$); no 2º termo $E$ age **antes** de $R$ (fora da diagonal) e $C_E = R\circ E - E\circ R$ mede exatamente essa troca. Os dois cutoffs, suas derivadas e os produtos com derivadas de $\delta$ ficam **dentro** dos parênteses, nunca absorvidos.

**Forma expandida (cutoffs explícitos).** $E(\chi_X F) = \chi_X E(F) + \mathcal L(\chi_X,F)$, com
$$\mathcal L(\chi,F)_{uv}= -2\partial^i\chi\partial_iF_{uv} - (\Box\chi)F_{uv} - \partial_u\chi\partial_v\mathrm{tr}F - \partial_v\chi\partial_u\mathrm{tr}F - \partial_u\partial_v\chi\,\mathrm{tr}F + \partial_u\chi\partial^iF_{iv} + \partial^i\chi\partial_uF_{iv} + \partial_u\partial^i\chi F_{iv} + (u\!\leftrightarrow\! v) + \delta_{uv}\big[2\partial^i\chi\partial_i\mathrm{tr}F + (\Box\chi)\mathrm{tr}F - \partial^i\chi\partial^jF_{ij} - \partial^j\chi\partial^iF_{ij} - \partial^i\partial^j\chi F_{ij}\big].$$
Se se quiser separar os cutoffs do $C_E$: $C_E(\chi_X U) = \chi_X C_E(U) + \sum_i \alpha^i(\chi_X) C_{\partial_{X_i}}(U)$, com $\alpha^i$ lido de $\mathcal L$; e $C_{\partial_{X_i}} = -C_{\partial_{Y_i}}$ sobre amplitudes em $x$ — **tudo se escreve só com $C_E$ e $C_{\partial Y}$**, como pedido.

**Adjunção:** $\partial_{Y_j}$ transferido a $c^r$ por partes **não recebe contato** — o contato vive só em $R$ vs $D$.

---

## 4. EXEMPLO QUANTITATIVO — $R(\mathrm{div}_Y B) - \mathrm{div}_Y R(B)$ para $r=0$

$$B^j_{uv,r}= -2\tfrac{\delta_{jr}\delta_{uv}}{z^3} -4\tfrac{\delta_{ju}\delta_{vr}+\delta_{jv}\delta_{ur}}{z^3} -4\tfrac{\delta_{uv}x_jx_r}{z^4} +16\tfrac{\delta_{jr}x_ux_v}{z^4} -8\tfrac{\delta_{ju}x_vx_r+\delta_{jv}x_ux_r}{z^4} +20\tfrac{\delta_{ur}x_jx_v+\delta_{vr}x_jx_u}{z^4} + 0$$

Aplicando (C1) com $C_{\partial_{Y_j}}=+2x_j(\cdots)\rho_{n+1}$ e $z\rho_5 = \rho_4$:

| termo | $b_m$ | $n$ | $\sum_j C_{\partial_{Y_j}}(T^j_m)$ | contribuição |
|---|---|---|---|---|
|1| $-2$ |3| $2\delta_{uv}x_r\rho_4$ | $-4\delta_{uv}x_r\rho_4$ |
|2| $-4$ |3| $2(\delta_{vr}x_u+\delta_{ur}x_v)\rho_4$ | $-8(\cdots)\rho_4$ |
|3| $-4$ |4| $2\delta_{uv}x_r z\rho_5 = 2\delta_{uv}x_r\rho_4$ | $-8\delta_{uv}x_r\rho_4$ |
|4| $+16$ |4| $2x_rx_ux_v\rho_5$ | $+32x_rx_ux_v\rho_5$ |
|5| $-8$ |4| $4x_ux_vx_r\rho_5$ | $-32x_ux_vx_r\rho_5$ |
|6| $+20$ |4| $2(\delta_{ur}x_v+\delta_{vr}x_u)\rho_4$ | $+40(\cdots)\rho_4$ |
|7| $0$ |5| — | $0$ |

**Soma:**
$$\sum_j C_{\partial_{Y_j}}(B^j_{uv,r}) = \rho_4\big[-12\,\delta_{uv}x_r + 32(\delta_{ur}x_v+\delta_{vr}x_u)\big],\qquad \rho_5:\; 32-32 = 0 .$$

Convertendo $x_i\leftrightarrow-\partial_{q_i}$ ($x_r\Box^2\delta = -4\partial_r\Box\delta$) e com $\rho_4 = \frac{\pi^2}{192}\Box^2\delta$:

$$\boxed{\;K_{uv,r} = \chi_Y(Y)\,\pi^2\Big[\tfrac14\,\delta_{uv}\partial_{x_r}\Box\delta(x) - \tfrac23\big(\delta_{ur}\partial_{x_v} + \delta_{vr}\partial_{x_u}\big)\Box\delta(x)\Big]\;}$$

**Componentes verificáveis ($r=0$):**
- $K_{11,0} = \dfrac{\pi^2}{4}\,\chi_Y\,\partial_0\Box\delta$;
- $K_{01,0} = -\dfrac{2\pi^2}{3}\,\chi_Y\,\partial_1\Box\delta$;
- $K_{00,0} = -\dfrac{13\pi^2}{12}\,\chi_Y\,\partial_0\Box\delta$;
- traço: $\mathrm{tr}\,K_{\cdot,0} = -\dfrac{\pi^2}{3}\,\chi_Y\,\partial_0\Box\delta$.

**Checagens cruzadas:** (i) o coeficiente $-12$ de $\delta_{uv}x_r$ coincide com o numerador da primeira estrutura de $C_{uv,r}$; (ii) a segunda diverge ($-30$ em $C$ vs $+32$ no contato) e a terceira ($96\,x_ux_vx_r/z^5$) **cancela** — logo o contato **não** é $(\text{constante})\times C$; (iii) $\mathrm{tr}\,C_{\cdot,\cdot,0} = -12x_0z^{-4}$ (usando $x_ix_i=z$).

---

## 5. A metade $C_E$ (receita; âncora verificada)

$C_E(F)_{uv} = -C_{\Box}(F_{uv}) - C_{\partial_u\partial_v}(\mathrm{tr}F) + C_{\partial_u\partial^i}(F_{iv}) + C_{\partial_v\partial^i}(F_{iu}) + \delta_{uv}[C_{\Box}(\mathrm{tr}F) - C_{\partial^i\partial^j}(F_{ij})]$, com cada $C_{\partial\partial}$ dado por (C2). Âncora verificada: $C_{\partial_k\partial_l}(z^{-n}) = -2\delta_{kl}\rho_{n+1} + 4(2n+1)x_kx_l\rho_{n+2}$. A aplicação completa a $C_{uv,r}$ (contrações de traço e de $\partial^i C_{iv}$) **não é executada nesta unidade** — ver §9.

---

## 6. $\chi_X\partial^\nu\delta$ vs $\chi_X(Y)\partial^\nu\delta$

- **Pode-se** substituir $\chi_X(X)\partial^\nu\delta(x) \to \chi_X(Y)\partial^\nu\delta(x)$ **como igualdade de distribuições em forma final**, pois o suporte é $x=0$ ($X=Y$). Vale para multiplicação e para a resposta impressa.
- **Não se pode** substituir **antes** de $\partial_X$/$\partial_Y$: $\partial_{X_i}[\chi_X(X)T] = (\partial_i\chi_X)(Y)T + \chi_X(Y)\partial_{x_i}T$, enquanto $\partial_{X_i}[\chi_X(Y)T] = \chi_X(Y)\partial_{x_i}T$ — a substituição prematura **apaga** $(\partial\chi_X, \partial\partial\chi_X)\cdot\partial^\nu\delta$. Idêntico para $\partial_Y$ (que ainda carrega a cadeia $\partial_{Y}=-\partial_x$).
- **Nunca** vale fora do suporte: em $P$, $\chi_X$ multiplica $R(A),R(B)$ com parte **fora da diagonal**, onde $\chi_X(X)\neq\chi_X(Y)$.

---

## 7. Limite $\chi_X=\chi_Y=1$ e a troca indevida $ER = RE$

Com $\chi\equiv 1$: $U = C$, $K = \sum_j C_{\partial_{Y_j}}(B^j)$, $T = R(C)+K$, e $P-Q = E(K) - C_E(C)$: **toda a diferença é o contato** (anomalia da operação $R$), não termos de cutoff.

A troca indevida $ER = RE$ (e $\partial_Y R = R\partial_Y$) dá $P = Q$ e **perde exatamente** a estrutura calculada em §4 — os termos $\propto\Box\delta$ com coeficientes $(-12,+32)$ e o cancelamento $\rho_5$. É a diferença entre *localizar primeiro* e *estender primeiro*: ela é local (suporte na diagonal), bilinear nos dados da fonte, e não é nula. **Nada disto afirma que a soma das bolhas ou a Q2 interagente completa se anula.**

---

## 8. MEMÓRIA CANÔNICA COMPARTILHADA (A7.b)

```
CONV: x=X−Y; z=x²; ∂_X=∂_x; ∂_Y=−∂_x (singular); R[F]=FP_{a=0}[(1−a)μ^{2a}z^a F];
      C_D := R D − D R; ρ_p := Res_{a=0} z^{a−p} = C_E^esc·(−(q²)^{p−2})/[4^{p−1}(p−1)!(p−2)!];
      C_E^esc = −4π² (fator escalar ≠ operador C_E); q ↔ ∂δ; x_i ↔ −∂_{q_i};
      zρ_{p+1}=ρ_p ; ∂_iρ_p = −2p x_iρ_{p+1}.
CONTATOS (F=x_I z^{−n}):  C_{∂_{Y_k}}(F)=+2x_k x_I ρ_{n+1}=−C_{∂_{X_k}}(F);
      C_{∂_k∂_l}(F)=−2{[Σ_s(δ_{li_s}x_k+δ_{ki_s}x_l)x_{I∖i_s}+δ_{kl}x_I]ρ_{n+1}−(4n+2)x_kx_lx_Iρ_{n+2}}.
REGRA (S = Ac + B^j∂_jc = Cc + div_Y(Bc); χ_X,χ_Y independentes):
      U = χ_Y C − (∂_{Y_j}χ_Y)B^j ; T = χ_Y R(A) − ∂_{Y_j}(χ_Y R(B^j)) = R(U)+K ;
      K = Σ_j C_{∂_{Y_j}}(χ_Y B^j)
      P − Q = E_X(χ_X K) − C_E(χ_X U)      [E fora de R no 1º; R fora de E no 2º]
EXEMPLO (dados do operador): Σ_j C_{∂_{Y_j}}(B^j_{uv,r}) = ρ_4[−12δ_{uv}x_r + 32(δ_{ur}x_v+δ_{vr}x_u)]
      (ρ_5 cancela: 32−32) ; K_{uv,r}=χ_Y π²[¼ δ_{uv}∂_r□δ − ⅔(δ_{ur}∂_v□δ+δ_{vr}∂_u□δ)]
      K_{11,0}=(π²/4)χ_Y∂_0□δ ; K_{01,0}=−(2π²/3)χ_Y∂_1□δ ; tr K_{·,0}=−(π²/3)χ_Y∂_0□δ
SUBSTITUIÇÃO: χ_X(X)∂^νδ = χ_X(Y)∂^νδ só DEPOIS de toda derivação; antes apaga (∂χ_X,∂∂χ_X)∂^νδ;
      não vale fora da diagonal. LIMITE χ=1: P−Q = E(K) − C_E(C). ER=RE ⇒ P=Q (falso).
```

---

## 9. Lacunas e pendências (declaradas)

1. **$C_E$ aplicado à fonte $C$ do exemplo** não foi avaliado componente a componente (§5 dá a receita fechada e uma âncora verificada); é passo mecânico de livro-razão, sujeito a verificação independente.
2. **Verificação externa** de toda a derivação manual (resíduos, tabela (C1)–(C2), $K_{uv,r}$): `DECLARADO até verificação` — nenhum número aqui é `VERIFIED`.
3. Não se afirma nada sobre **soma de bolhas**, **Q2 interagente**, contratermos, estado físico, Lorentz ou outros ramos.
4. A leitura $R[F]=\mathrm{FP}[(1-a)\mu^{2a}z^aF]$ é a que reproduz `Res(z^{a-n})` do enunciado; os **contatos independem** dessa normalização (são resíduos), mas os *finite parts* carregam $\ln\mu$ — a precisão do esquema é registrada, não escondida.

**Fecho da unidade:** o contato exato entre *localizar primeiro* e *estender primeiro* é $P-Q = E_X(\chi_X K) - C_E(\chi_X U)$, com $K$ dado explicitamente acima; a diferença é inteiramente local (derivadas de $\delta$), e a sua soma **não** se anula.