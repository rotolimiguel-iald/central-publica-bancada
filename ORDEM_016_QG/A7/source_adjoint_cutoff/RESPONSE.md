# Parecer A7.b — a imagem Einstein bilocal da fonte não-local, na orientação da Hessiana

**Estatuto deste parecer:** [DECLARADO até auditoria da bancada]. Nada aqui foi executado em código; toda identidade é verificável à mão a partir das convenções fixadas. Não modifico originais, kernel, gate, nem proponho ramo fora de A7.b. Os jatos que faltam são listados no §8 e **não** são preenchidos por simetria presumida.

---

## 0. Leitura do objeto dado — o que E é, e a propriedade que licencia a adjunção

Convenções: índices $a,b,c,d,e$ em $X$; $r,s,k$ em $Y$; $z = 2\sigma(X,Y) = x\cdot x$ em RNC($Y=0$); $\Box = \nabla^a\nabla_a$ euclidiano; $C_E=-4\pi^2$.

**0.1 — O operador dado é exatamente $2\,\delta(G_{ab}+\Lambda g_{ab})$ em espaço-forma, $\Lambda=3K$.** Verificação por expansão direta [DERIVED, conferível termo a termo]. Em fundo Einstein, o Lichnerowicz dá

$$
\Delta_L h_{ab}=-\Box h_{ab}-2R_{acbd}h^{cd}+2R_{(a}{}^c h_{b)c}
=-\Box h_{ab}+8K h_{ab}-2K g_{ab}\,\mathrm{tr}\,h ,
$$

usando $R_{acbd}=K(g_{ab}g_{cd}-g_{ad}g_{bc})$ e $R_{ab}=3Kg_{ab}$; e $-2\Lambda\,\mathrm{Itr}(h)=-6K(h-\tfrac12 g\,\mathrm{tr}h)$. Reorganizando o bloco de gauge na forma dada,

$$
2\,\delta(G+\Lambda g)_{ab}
=\underbrace{-\Box h_{ab}+\tfrac12 g_{ab}\Box\,\mathrm{tr}h}_{-\Box\,\mathrm{Itr}(h)}
+\underbrace{\nabla_a C_b+\nabla_b C_a-g_{ab}\nabla^c C_c}_{\mathrm{Itr}\,G\,C(h)}
+2K h_{ab}+K g_{ab}\,\mathrm{tr}h
=E(h)_{ab}.
$$

O $E$ do enunciado fecha com $2\delta(G+\Lambda g)$, $\Lambda=3K$ — sem nenhuma constante ajustada. Consequência imediata (Bianchi linearizada):

$$
E(G(c))=2\,\mathcal L_c(G_{ab}+\Lambda g_{ab})=0
\quad\text{identicamente — Ward zero é teorema, não ajuste.}\ \text{[DERIVED/KNOWN]}
$$

**0.2 — $E$ é formalmente auto-adjunto.** A prova são três identidades algébricas, cada uma verificável em uma linha:

$$
\mathrm{div}\circ\mathrm{Itr}=C,\qquad
\mathrm{tr}\circ G=2\,\mathrm{div},\qquad
\mathrm{Itr}^2=\mathrm{id}\ \ (n=4),
$$

donde $(\mathrm{Itr}\,G\,C)^* = C^*G^*\mathrm{Itr}^* = \big(-\tfrac12(G-g\,\mathrm{div})\big)\circ(-2\,\mathrm{div})\circ\mathrm{Itr} = (G-g\,\mathrm{div})\circ C = \mathrm{Itr}\,G\,C$, pois $\mathrm{Itr}(Gv)=Gv-g\,\mathrm{div}\,v$. As peças restantes ($\Box$, $\mathrm{Itr}$, $2K$, $Kg\,\mathrm{tr}$) são auto-adjuntas e comutam entre si por $\nabla g=0$. Logo

$$
E^*=E.\quad\text{[DERIVED]}
$$

É esta propriedade — e não uma simetria presumida — que torna a adjunção *enunciável*. O que a torna *verdadeira* sobre kernels singulares é o §2.

---

## 1. A expressão bilocal correta de $R_{ab}[c](X)$

**Redução do jato do ghost (orientação do motor: fonte em $X$, ghost em $Y$).** O funcional dado, $\int_X T^{ab}[A_{ab}{}^r c_r+B_{ab}{}^{kr}\nabla_k c_r]$, reduz-se por integração por partes em $Y$ a um kernel único

$$
\boxed{\;K_{cd}{}^r(X,Y)=A_{cd}{}^r(X,Y)-\nabla_k^{Y} B_{cd}{}^{kr}(X,Y)\;}
$$

com $\nabla^Y$ bitensorial (índices $k,r$ em $Y$) e a medida absorvida na lei de densidade de $B$. Isto é álgebra limpa fora da diagonal; o conteúdo distribucional entra no passo seguinte.

**Imagem Einstein, na mesma orientação da Hessiana sobre $G(c)$.** A Hessiana age *para a frente*, sobre o argumento-tensor em $X$. A expressão correta é portanto

$$
\boxed{\;R_{ab}[c](X)=\int_Y dV(Y)\;\big[E_X K\big]_{ab}{}^r(X,Y)\;c_r(Y)\;}
$$

com $E_X$ agindo nos índices $ab$ e nas derivadas $\nabla^X$, explicitamente

$$
E_X K_{ab}{}^r=
-\Box_X K_{ab}{}^r+\tfrac12 g_{ab}\Box_X(\mathrm{tr}_X K)^r
+\nabla_a^X C_b(K)^r+\nabla_b^X C_a(K)^r-g_{ab}\nabla^{c}_X C_c(K)^r
+2K K_{ab}{}^r+K g_{ab}(\mathrm{tr}_X K)^r,
$$

$$
C_b(K)^r=\nabla^c_X K_{cb}{}^r-\tfrac12\nabla_b^X K^c{}_c{}^r .
$$

**O que esta expressão não é** (as duas trocas ilegítimas que o enunciado manda distinguir): (i) não é $E_Y$ agindo sobre índices de $Y$ — isso é a orientação transposta, que só se alcança pela adjunção do §2 *com* os contatos; (ii) não é o kernel reescrito com $X\leftrightarrow Y$ trocados "na variável" — isso exige reancoragem bitensorial (§3), não $p\to-p$.

**$E_X$ sobre o kernel estendido.** Com a parametrix de Hadamard $K=\tfrac{1}{4\pi^2}[U/z+V\ln(\mu^2 z)+W]$ e a extensão fixa $R(u)=\mathrm{FP}_a[(1-a)\mu^{2a}z^a u]$:

$$
\Box_X\frac{U}{z}=\frac{\Box_X U}{z}+2\nabla^a U\,\nabla_a\frac1z+U\,\Box_X\frac1z,
\qquad \Box_X\frac1z=C_E\,\delta^4(X,Y)\ \ (\text{mais FP}),
$$

donde a **regra-mestra do defeito**:

$$
\boxed{\;\big[\Box,\,R\big]=C_E\times(\text{avaliação coincidente do resíduo})\;}
$$

— *conservar os contatos de extensão* é exatamente nunca escrever $\Box R=R\Box$. O termo $\nabla U\cdot\nabla(1/z)\sim K/z$ é polar e vai à FP; o termo $U\,\Box(1/z)$ é o contato, ordem $K^0$ em $C_E\,\delta$ e ordem $K^1$ em $C_E\,u_1\,\delta$. O $\ln z$ **não contata** em 4D (a borda sobre a esfera de raio $\varepsilon$ morre como $\varepsilon^2$); os contatos vivem no polo e na prescrição FP, não no log.

---

## 2. A adjunção e os contatos da troca $R\leftrightarrow E$

**Cadeia de comparação** (orientação do motor $\to$ orientação da bancada):

$$
\int_X T^{cd}(E_XK)_{cd}{}^r c_r
\;\xrightarrow{\ \text{adjunção de }E\ }\;
\int_X (E_XT)^{cd}K_{cd}{}^r c_r \;+\;\mathrm{Contatos}
\;\xrightarrow{\ \text{reancoragem}\ }\;
\text{par da bancada } \langle T(Y),\,G(c)(X)\rangle ,
$$

onde o último passo usa ainda a adjunção *limpa* de $G$ ($\mathrm{div}^*=-G/2$, fora da diagonal).

**Família de contatos** [DERIVED; regra de distribuições FP em $\mathbb{R}^4$, Gel'fand–Shilov/Hadamard — KNOWN]. Com $z=x^2$ e $C_E=-4\pi^2$, por simetria $SO(4)$ mais a recursão $\Box\,\partial_{a_1}\cdots\partial_{a_m}(1/z)=\partial_{a_1}\cdots\partial_{a_m}C_E\delta$:

| ordem da derivada | contato |
|---|---|
| $m=1$: $\partial_a(1/z)$ | nenhum (FP ímpar) |
| $m=2$: $\partial_a\partial_b(1/z)$ | $(C_E/4)\,\delta_{ab}\,\delta^4$ |
| $m=3$: $\partial_a\partial_b\partial_c(1/z)$ | $(C_E/6)\,(\delta_{ab}\partial_c+\delta_{bc}\partial_a+\delta_{ca}\partial_b)\,\delta^4$ |

(traçando qualquer par se recupera $\Box\partial^{m-2}(1/z)=C_E\partial^{m-2}\delta$; a regra geral é $(C_E/2m)\times$ simetrizadores, verificável por recursão). Como $E_X$ é de segunda ordem sobre $K\supset U/z$ e contém $\nabla\nabla\nabla$ efetivos via $C(K)$, os três níveis aparecem:

$$
\begin{aligned}
\mathrm{Contatos}=C_E\Big[
&-\big[\mathrm{Itr}\,U\big]^{cd r}(Y,Y)\;T_{cd}(Y)\,c_r(Y)\\
&+\tfrac14\,\delta_{ab}\big[\dots\big]+\tfrac16\big(\delta_{ab}\partial_c+\cdots\big)\big[\text{jatos}_1\text{ de }T\big]\\
&+\;K^1:\;-\big[\mathrm{Itr}\,u_1\big]^{cd r}T_{cd}c_r+\cdots\Big],
\end{aligned}
$$

com $u_1$ o primeiro coeficiente de Hadamard do setor (J1, §8 — **não fornecido**, não presumido). O termo de ordem $K^1$ é o que faz a troca $R\leftrightarrow E$ pagar curvatura: **sem $u_1$ no contato, a adjunção fecha em $K^0$ e erra em $K^1$** — este é o detector do §7.

**Forma adjunta contra $E(T)$**, pedida explicitamente:

$$
\int_X \big[E_X T\big]^{cd}(X)\;K_{cd}{}^r(X,Y)\;c_r(Y)\,dV_X
=\int_X T^{cd}\big[E_XK\big]_{cd}{}^r c_r\;-\;\mathrm{Contatos}.
$$

A identidade é uma *lei de comparação*: os dois lados são computáveis independentemente (o motor pelo lado esquerdo; a bancada pelo direito, após a reancoragem do §3), e **só se aceita a adjunção se o fechamento for exato com os contatos listados** — nenhuma constante pode ser movida para obtê-lo (a trava Ward do §0.1 é o caso particular $T\sim$ gauge).

**Nota sobre $W$.** A cauda lisa $W$ atravessa a adjunção limpa (não gera contato); excluir $W$ do componente de cálculo não fixa estado algum — a escolha de estado vive em $W$ e este parecer não a toca, conforme a instrução da ordem.

---

## 3. Reancoragem $X\leftrightarrow Y$ **≠** troca $p\to-p$

**$p\to-p$** é a conjugação da transformada de Fourier *local* em RNC($Y$): $\tilde K(p)\to\tilde K(-p)$ equivale a $K(x,0)\to K(-x,0)$. No plano, $K(-x,0)=K(0,x)$ e as duas operações coincidem. Em curvo:

$$
\textbf{reancoragem}=\underbrace{\big[p\!\to\!-p\ \text{covariante via } e^{ip_r\sigma^r}\big]}_{\text{troca de argumentos}}\ \oplus\
\underbrace{\big[\text{jatos }K^1\text{ do transporte e de }\sigma_{ar}\big]}_{\text{o que }p\to-p\text{ jamais gera}} .
$$

Regras (Synge–DeWitt, KNOWN): $\sigma^r(X,Y)=-g^r{}_a\,\sigma^a(X,Y)$; $g_a{}^r=\delta_a^r-\tfrac{K}{6}(\delta_a^r z-x_ax^r)+O(K^2)$; e os jatos de segunda derivada $\sigma_{ab}=\delta_{ab}-\tfrac{K}{3}(\delta_{ab}z-x_ax_b)$, $\sigma_{ar}=-\delta_{ar}+\tfrac{K}{6}(x_ax_r-\delta_{ar}z)$ — que são exatamente as estruturas `metric1`, `lower_cross` e `gamma_contraction` do motor anexo (leitura compatível; convenção de sinal a cravar, J5). Trocar $p$ por $-p$ inverte o sinal dos termos ímpares em $p$ e **não** produz nenhum desses termos de transporte; reancorar produz-os deterministicamente. São operações distintas já em $K^1$.

---

## 4. $E$ não atravessa $F(\Box)$ — e $G$ também não

$$
[E,\Box]=[\mathrm{Itr}\,G\,C,\Box]\neq0,\qquad [G,F(\Box)]\neq0 ,
$$

porque (Weitzenböck, com $\nabla R=0$ em espaço-forma)

$$
[\nabla_a,\Box]c_b=-\mathrm{Ric}_a{}^c\nabla_c\,c_b-2R_a{}^c{}_b{}^d\nabla_c\,c_d
=-3K\nabla_a c_b-2K\big(\nabla_a c_b-\nabla_b c_a\big)\neq0,
$$

e o mesmo mecanismo contamina $[C,\Box]$ e $[\mathrm{Itr}GC,\Box]$ com termos $K\times$(primeiras derivadas). Logo, para $F$ **não polinomial** ($\Box^{-1}$, $\ln\Box$, $e^{s\Box}$, e a família $\mathrm{FP}_a$ de $z^a$), já o primeiro coeficiente da expansão falha: a prescrição é

$$
\boxed{\ \text{ordem fixa: kernel}\ \to\ E_X\ \to\ R(\mathrm{FP})\ \to\ \text{contatos};\quad
E\,F(\Box)\neq F(\Box)\,E,\ \ E\,G\,F(\Box)\neq E\,F(\Box)\,G.\ }
$$

Em particular, no motor, $L=\ln(\mu^2z)$ deve ser tratado como símbolo com $\partial_a L=2x_a/z$ **depois** de $E$ agir — nunca comutado para fora.

---

## 5. Algoritmo calculável (RNC/bitensores; medidas e transporte)

0. **Carta e medida:** RNC em $Y=0$; $z=x\cdot x$; $dV=\sqrt g\,d^4x$, $\sqrt g=1-\tfrac16 R_{cd}x^cx^d=1-\tfrac{K}{2}z+O(K^2x^3)$. *(Compatibilização com o* `δT` *do motor: pendência J4 — não presumir.)*
1. **Jatos do fundo:** $g_{ab}=\delta_{ab}-\tfrac{K}{3}(\delta_{ab}z-x_ax_b)$; $\Gamma^a_{bc}=-\tfrac{K}{3}(\delta^a_b x_c+\delta^a_c x_b-2\delta_{bc}x^a)$ (forma lida do `gamma_contraction`); $g_a{}^r$ e $\sigma_{ar}$ como no §3.
2. **Kernel reduzido:** $K=A-\nabla^Y_k B$ (com $\nabla^Y$ e o jato da medida).
3. **Ação de $E_X$:** derivadas encadeadas ($\partial_a+2x_a\partial_z+(2x_a/z)\partial_L$); traços por $\mathrm{Itr}$ (o motor já subtrai meio-traço — linhas 57 e 60 do `curved_source_jet_engine.py`, leitura compatível).
4. **Separação FP:** classes $z^{-2},\,z^{-1},\,L,\,$constantes; contatos pelas regras do §2; **nunca** $\Box R=R\Box$.
5. **Adjunção:** computar os dois lados da lei do §2 independentemente; exigir fechamento exato com a tabela de contatos.
6. **Reancoragem:** transporte com $g_a{}^r$; fase covariante $e^{ip_r\sigma^r}$; proibido $p\to-p$ sozinho.
7. **Ward:** $E(G(c))=0$ como controle interno exato (§0.1), sem ajuste.

## 6. Controle plano

$K\to0$: $g_a{}^r=\delta$, $\Gamma=0$, FP plana; a adjunção deve devolver Parseval com $\Box(1/z)=C_E\delta$ e $p\to-p\equiv$ reancoragem; o par da bancada e o do motor devem coincidir *numericamente* nas médias esféricas (`spherical_moment` mata o traço-livre; o traço é o contato $C_E/4$). Se o plano não fecha, a adjunção está errada — este controle não pode deixar de quebrar.

## 7. Termo de curvatura que detecta a troca ilegítima

**Reciprocidade bitensorial em $K^1$:** o kernel reancorado por transporte e o kernel trocado por $p\to-p$ diferem por $\propto K\times\{$`lower_cross`, `metric1`, `gamma_contraction`$\}$ — residual isolável e não nulo. **Segunda trava (os contatos):** a troca $R\leftrightarrow E$ feita sem o termo $-C_E\,\mathrm{Itr}\,u_1$ erra o coeficiente de $K^1$ na adjunção por um valor fixado por Hadamard — não por ruído. Uma troca legítima é aquela em que (i) Ward fecha sem ajuste, (ii) os contatos $C_E/(2m)$ aparecem todos, (iii) o residual de reciprocidade é nulo.

## 8. Jatos de dois extremos que faltam (declarados, não presumidos)

- **J1** — o coincidente $u_1$ de Hadamard do setor (métrico **e** ghost), i.e., o pacote de curvatura $P$ de cada campo. Sem ele, o contato $K^1$ do §2 não tem valor. **Não fornecido.**
- **J2** — $g_a{}^r$ em $K^1$ na direção $Y\to X$ e a relação exata $g_{ar}$ vs $-\sigma_{ar}$ além do coincidente (DeWitt). Não é simetria: é inversa de jato, a derivar.
- **J3** — os jatos mistos $\nabla_a^X\nabla_k^Y K$ sem fase (o motor os tem via $p_\mu$ com fase $e^{-ipx}$; a forma bitensorial sem fase, com $\Gamma\Gamma$ e $\partial\Gamma$, não está nos anexos).
- **J4** — a compatibilização do `δT` $=-zT/6-(xx^tT+Txx^t)/6$ com a decomposição $[\sqrt g\times(\text{paralelo})^2]$: verifiquei que **nenhuma** combinação de sinal único ($\sqrt g=1-Kz/2$; paralelo $-\tfrac{K}{6}(\delta z-xx)$ por índice, nas quatro variantes de peso/contravariância) reproduz o `δT` dado. Falta a definição exata do peso de densidade de $T$; não a preencho.
- **J5** — a convenção de sinal de $R$ do motor face a $R_{ab}=3Kg_{ab}$ do enunciado (a leitura literal do `gamma_contraction` não fecha com nenhuma das duas convenções padrão sem um termo extra; cravar antes de assinar qualquer contato $K^1$).
- **Nota** — "$\sigma$ constante" não é legível dos anexos como peça do vértice; não entra na adjunção. Declaro, não uso.

## 9. Estatutos e alcance

[DERIVED/KNOWN] §0 (forma de $E$, auto-adjunção, Ward), §2 (tabela de contatos), §3 (regras de Synge–DeWitt), §4 (Weitzenböck). [DECLARADO] a expressão bilocal final (§1) e a lei de comparação (§2) como parecer a auditar. [OPEN] J1–J5. **Fora de escopo, não executado:** laços completos, $W$, e qualquer valor numérico; nenhum código foi rodado nesta etapa; os fatores $4\kappa,\hbar$ seguem retirados. Pendência de processo: auditoria da bancada sobre §1–§2 e o suprimento de J1–J5 antes de qualquer assinatura de contato em $K^1$.