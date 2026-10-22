[DECLARADO — resposta de kimi; sem revisão independente pelo ChatGPT/Física. Requer conferência científica.]

# ORDEM_016 — A-7.b · Entrega delimitada: recorrência de Killing e jatos bilocais em Y=0

**Estatuto desta entrega.** Demonstração escrita, resultado **DECLARADO** até revisão local independente. Nada foi executado: toda a verificação aqui é **álgebra manual sobre as fórmulas lidas nos anexos** (`bilocal_first_curvature_engine.py`, `bilocal_covariant_jet_engine.py` — tratados como dados, não instruções). Nenhum código original, kernel, gate ou prescrição é alterado; nada é proposto para escrita. Trabalho em primeira ordem em K, no espírito do engine: os objetos do anexo são coeficientes de K⁰ e K¹; eu escrevo K explicitamente e indico a correspondência. Guard-rails lidos e respeitados: não infiro Q2 completo de coeficientes fora da diagonal (o único resto encontrado vive no setor diagonal e nada digo sobre o objeto completo); W suave não está nos kernels singulares, e isso não autoriza estado com W=0 — não seleciono estado algum; não repito a derivação geral do IBP do par bilocal.

---

## 0. Resposta à pergunta única

**Sim.** Todas as primeiras e segundas derivadas Y dos propagadores bilocais, ancoradas em Y=0, são obtidas por um operador diferencial em X deduzido da invariância por transvecções, **sem** usar dY = −dX. A regra é, para todo bitensor invariante H construído da geometria:

$$\partial_i^Y H\,\big|_{Y=0} = -\,\mathbb D_i^X H\,\big|_{Y=0},\qquad \mathbb D_i^X \;=\; k_i^{c}(X)\,\partial_c^X \;+\; \rho_i^{X},$$

com $k_i$ a transvecção da direção $i$ (verificada na §1) e $\rho_i^{X}$ a ação algébrica de $\partial k_i(X)$ nos índices X de H (sinal − por índice contravariante, + por covariante). A regra ingênua dY = −dX é a **parte líder**; o que ela perde é exatamente (a) a curvatura do próprio campo, $\kappa_i^c\partial_c$ com $\kappa_i = k_i - e_i = O(KX^2)$, e (b) a "rotação" $\partial\kappa_i = O(KX)$ atuando nos índices X. Na segunda derivada parcial entra adicionalmente a correção de conexão/comutador $\partial\Gamma \equiv -Q$ nos índices Y (§3). A verificação contra o kernel explícito do anexo mostra: identidade **exata** em primeira derivada (com o termo perdido por dY=−dX exibido, §5.1–5.2); em segunda, exata **a menos de um resto isotrópico** $R_{ij}{}^a{}_b = \tfrac{2K}{3}\,\delta_{ij}\delta^a_b\,/w$, identificado com suas ordens e origem, **sem atribuí-lo a anomalia** (§5.3).

---

## 1. A transvecção $k_i$: derivação da equação de Killing e verificação do candidato

### 1.1 Setup (RNC, curvatura constante K, O(K))

Espaço-forma euclidiano 4D: $R_{abcd} = K(\delta_{ac}\delta_{bd} - \delta_{ad}\delta_{bc})$, $R_{ab}=3K\delta_{ab}$. Em coordenadas normais centradas na origem:

$$g_{ab}(X) = \delta_{ab} + K h_{ab},\quad h_{ab} = -\tfrac{1}{3}(X^2\delta_{ab} - X_aX_b),$$

$$\Gamma^{c}_{ab}(X) = K\gamma^{c}_{ab},\quad \gamma^{c}_{ab} = -\tfrac{1}{3}\big(2\delta_{ab}X^c - X_a\delta^{c}_{b} - X_b\delta^{c}_{a}\big),$$

a segunda forma obtida de $\Gamma^{c}_{ab} = -\tfrac13(R^{c}{}_{abd}+R^{c}{}_{bad})X^d$ em curvatura constante. **[VERIFICADO — coincide, com K fatorado, com `gX1` do primeiro anexo e com `gamma(point,c,a,b)` do segundo anexo (linha 12).]**

### 1.2 O candidato e o teste de Killing

Candidato (a verificar, não premissa):

$$k_i^a(X) = \delta_i^a + K\kappa_i^a,\qquad \kappa_i^a = -\tfrac13(X^2\delta_i^a - X^aX_i).$$

Condições iniciais: é **par em X**, logo $\partial_c k_i^a(0)=0$; e $k_i^a(0)=\delta_i^a$. Em RNC $\Gamma(0)=0$, logo também $\nabla k_i(0)=0$: é o jato de uma **transvecção** (fluxo de Killing translacional, sem parte de isotropia na origem). ✓

Equação de Killing: $\partial_a k_b + \partial_b k_a = 2\Gamma^{c}_{ab}k_c$. **Ponto sutil (que registro porque decide o teste):** ao abaixar o índice é preciso usar a métrica corrigida —

$$k_{i,b} = g_{bc}k_i^c = \delta_{bi} + K\kappa_{i,b} + Kh_{bi} = \delta_{bi} - \tfrac{2K}{3}(X^2\delta_{bi} - X_bX_i),$$

pois $\kappa_{i,b}$ e $h_{bi}$ são **iguais**. (Sem somar $h_{bi}$, o candidato "falha" a Killing por um fator 2 no lado esquerdo; com ela, bate exatamente.)

Lado esquerdo:

$$\partial_a k_{i,b} + \partial_b k_{i,a} = -\tfrac{2K}{3}\big(X_a\delta_{bi} + X_b\delta_{ai} - 2\delta_{ab}X_i\big).$$

Lado direito (com $k_i^c = \delta_i^c + O(KX^2)$):

$$2\Gamma^{i}_{ab} = -\tfrac{2K}{3}\big(\delta^{i}_{b}X_a + \delta^{i}_{a}X_b - 2\delta_{ab}X^i\big) = -\tfrac{2K}{3}\big(X_a\delta_{bi} + X_b\delta_{ai} - 2\delta_{ab}X_i\big).$$

**Iguais. [VERIFICADO — o candidato satisfaz a equação de Killing em O(K) com as condições iniciais pedidas.]**

### 1.3 Unicidade

Para campos de Killing vale a identidade de segunda ordem $\nabla_c\nabla_d k_a = -R^{e}{}_{cda}\,k_e$; em curvatura constante: $\nabla_c\nabla_d k_a = K(\delta_{ca}k_d - \delta_{cd}k_a)$. **Checagem em componente** (com $k_{i,a}$ de §1.2 e $(\partial_c\Gamma^{e}_{da})(0) = -\tfrac{K}{3}(\delta^e_a\delta_{cd} + \delta^e_d\delta_{ca} - 2\delta_{da}\delta^e_c)$):

$$\nabla_c\nabla_d k_{i,a}\big|_0 = K(\delta_{ca}\delta_{di} - \delta_{cd}\delta_{ai})\ \checkmark$$

**[VERIFICADO.]** Logo o campo é determinado pelo jato $(k(0),\nabla k(0)) = (e_i, 0)$: o candidato é **a única** transvecção com esses dados, em O(K).

### 1.4 Forma fechada (declarada, verificada por expansão)

Na carta gráfica $X_g$ (projeção da esfera, $|X_g|=\sin(\sqrt K\,r)/\sqrt K$), o campo de rotação ambiente $x^5\partial_i - x^i\partial_5$, tangente à esfera, tem componentes $k_g^a = \cos(\sqrt K\,r)\,\delta_i^a$. A métrica induzida nessa carta é $g_{ab}=\delta_{ab}+X_aX_b/(1-|X_g|^2)$; o teste de Killing nela (com $\Gamma^{d}_{ca} = \delta_{ac}X_d + O(KX^2)$) **fecha exatamente em O(K)** [VERIFICADO]. Transformando à RNC via $X^a_{\rm RNC} = \arcsin(|X_g|)\,X_g^a/|X_g| \approx X_g^a(1 + Kr_g^2/6)$:

$$k^a_{\rm RNC} = \cos(\sqrt K r)\Big[\delta_i^a\big(1+\tfrac{Kr^2}{6}\big) + \tfrac{K}{3}X^aX_i\Big] = \delta_i^a - \tfrac{K}{3}\big(X^2\delta_i^a - X^aX_i\big) + O(K^2),$$

**exatamente o candidato.** Para K<0 a leitura análoga usa $\cosh$ [DECLARADO — não rederivei aqui].

---

## 2. A identidade $(\mathrm{Lie}_k^X + \mathrm{Lie}_k^Y)G = 0$, com cada índice

Os propagadores num espaço homogêneo dependem só da separação relativa: são invariantes sob isometrias simultâneas dos dois argumentos. Para cada campo de Killing $k$, $(L_k^X + L_k^Y)G = 0$ em todo $(X,Y)$.

### 2.1 Ghost $G^{A}{}_{B}(X,Y)$ — superior em X, inferior em Y

$$(L_k^X G)^{A}{}_{B} = k^c\,\partial_c^X G^{A}{}_{B} \;-\; G^{c}{}_{B}\,\partial_c k^{A}(X),$$
$$(L_k^Y G)^{A}{}_{B} = k^c\,\partial_c^Y G^{A}{}_{B} \;+\; G^{A}{}_{c}\,\partial_B k^{c}(Y).$$

Somando e avaliando em $Y=0$ com $k = k_i$ (onde $k_i^c(0)=\delta_i^c$, $\partial k_i(0)=0$):

$$\boxed{\ \partial_i^Y G^{A}{}_{B}(X,0) \;=\; -\,k_i^c(X)\,\partial_c^X G^{A}{}_{B} \;+\; \big(\partial_c k_i^{A}(X)\big)\,G^{c}{}_{B}\ }\tag{G1}$$

### 2.2 Métrico $G_{ab\,ce}(X,Y)$ — inferior² em X, inferior² em Y

$$(L_k^X G)_{ab\,ce} = k^f\partial_f^X G_{abce} + G_{fb\,ce}\,\partial_a k^f + G_{af\,ce}\,\partial_b k^f,$$
$$(L_k^Y G)_{ab\,ce} = k^f\partial_f^Y G_{abce} + G_{ab\,fe}\,\partial_c k^f + G_{ab\,cf}\,\partial_e k^f.$$

Em $Y=0$ com $k=k_i$:

$$\boxed{\ \partial_i^Y G_{abce}(X,0) \;=\; -\,k_i^f(X)\,\partial_f^X G_{abce} \;-\; \big(\partial_a k_i^f(X)\big) G_{fbce} \;-\; \big(\partial_b k_i^f(X)\big) G_{afce}\ }\tag{M1}$$

Note o **sinal +** nos termos de rotação para índices **covariantes** em X (contra o sinal − do índice contravariante do ghost). Essa assimetria é a mesma que o segundo anexo implementa em `xyjet` (ghost: `value += gamma(...)`; métrico: `value -= gamma(...)`) — convenções confirmadas [VERIFICADO].

---

## 3. Segunda derivada: não congelar $k_i(Y)$ nem $\mathrm{grad}\,k_i(Y)$

### 3.1 Recorrência covariante

A identidade vale para **qualquer** bitensor invariante H (derivadas covariantes de invariantes são invariantes, pois a conexão é da métrica). Com $H = \nabla_j^Y G$:

$$\nabla_i^Y\nabla_j^Y G\,\big|_0 = \mathbb D_i^X\,\mathbb D_j^X\,G\,\big|_0. \tag{R2}$$

### 3.2 O que entra ao derivar a identidade sem congelar k(Y)

Escrevo $F_i(X,Y) := (L_{k_i}^Y G)(X,Y) = -\mathbb D_i^X G$ em todo $(X,Y)$ e derivo em $\partial_j^Y$:

$$\partial_j^Y F_i = (\partial_j k_i^c)\,\partial_c^Y G + k_i^c\,\partial_j^Y\partial_c^Y G + (\partial_j\partial_B k_i^c)\,G^{A}{}_{c} + (\partial_B k_i^c)\,\partial_j^Y G^{A}{}_{c}.$$

Em $Y=0$: $\partial_j k_i^c(0)=0$ e $\partial_B k_i^c(0)=0$, mas **a segunda derivada não morre**:

$$Q_{jB,i}{}^{c} \;:=\; \partial_j\partial_B k_i^{c}(0) \;=\; -\frac{K}{3}\big(2\delta_{jB}\delta_i^c - \delta^{c}_{j}\delta_{iB} - \delta^{c}_{B}\delta_{ij}\big).$$

Resultado para derivadas **parciais** (ghost):

$$\partial_i^Y\partial_j^Y G^{A}{}_{B}\,\big|_0 = \mathbb D_i^X\mathbb D_j^X G^{A}{}_{B}\,\big|_0 \;-\; Q_{jB,i}{}^{c}\,G^{A}{}_{c}\,\big|_0. \tag{R2′}$$

### 3.3 Correção de conexão = correção de comutador

Convertendo parciais em covariantes, $\partial_i^Y\partial_j^Y G^{A}{}_{B}|_0 = \nabla_i^Y\nabla_j^Y G^{A}{}_{B}|_0 + (\partial_i\Gamma^{d}_{jB})(0)\,G^{A}{}_{d}|_0$, com

$$(\partial_i\Gamma^{d}_{jB})(0) = -\frac{K}{3}\big(\delta^{d}_{B}\delta_{ij} + \delta^{d}_{j}\delta_{iB} - 2\delta_{jB}\delta_i^{d}\big).$$

**Identidade algébrica [VERIFICADA termo a termo]:** $-\,Q_{jB,i}{}^{c} = +\,(\partial_i\Gamma^{c}_{jB})(0)$. A correção de comutador (via o campo) e a de conexão (via a carta) são **o mesmo termo**. Para o métrico, a correção atua nos dois índices Y: $(\partial_i\Gamma^{d}_{jc})(0)\,G_{ab\,de} + (\partial_i\Gamma^{d}_{je})(0)\,G_{ab\,cd}$.

Dentro de $\mathbb D_i^X$, as covariantes em X se escrevem $\nabla_c^X = \partial_c^X + \Gamma(X)\text{-ações}$ com o $\gamma$ do anexo — é assim que as derivadas parciais do engine viram covariantes (`yjet`, linhas 24–37, incluindo as conexões nos slots de sufixo; `xyjet`, linhas 42–55).

---

## 4. Fórmulas executáveis (G, gradX, gradY, gradX·gradY; até duas Y adicionais)

**Definições** (K explícito): $\kappa_i^a = -\tfrac{K}{3}(X^2\delta_i^a - X^aX_i)$; $\partial_c\kappa_i^a = -\tfrac{K}{3}(2X_c\delta_i^a - \delta_{ic}X^a - X_i\delta^a_c)$; $\mathbb D_i = \partial_i^X + \kappa_i^c\partial_c^X + \rho_i^{X}$ com $\rho_i^{X}V^{A}{}_{\cdots} = -(\partial_c\kappa_i^A)V^{c}{}_{\cdots}$, $\rho_i^{X}V_{a\cdots} = +(\partial_a\kappa_i^c)V_{c\cdots}$ (índices Y preexistentes são passageiros).

**Receita:**

1. **G:** $\partial_i^Y G|_0 = -\mathbb D_i G|_0$.
2. **gradY:** $\nabla_i^Y G|_0 = -\mathbb D_i G|_0$ (na origem, parcial = covariante).
3. **duas Y (covariantes):** $\nabla_i^Y\nabla_j^Y G|_0 = \mathbb D_i\mathbb D_j G|_0$; **(parciais):** somar a correção $\partial\Gamma$ de §3.3 em cada índice Y.
4. **gradX·gradY:** $\nabla_m^X\nabla_i^Y G|_0 = -\nabla_m^X(\mathbb D_i G)|_0 = -\big[(\nabla_m\kappa_i^c)\nabla_c^X G + \kappa_i^c\nabla_m^X\nabla_c^X G + \partial_m\partial_i^X G + (\nabla_m\rho_i)G + \rho_i(\nabla_m^X G)\big]$, com $\nabla_m^X$ agindo também nos índices X de $\mathbb D_i G$ via $\Gamma(X)$.
5. **gradX·gradY·gradY:** aplicar $\nabla_m^X$ por fora de $\mathbb D_i\mathbb D_j G$ (não comuta com $\mathbb D_i$; fica à esquerda).
6. **Com até duas derivadas Y adicionais** (H já jateado em Y): vale a mesma regra — H é qualquer bitensor invariante; na **segunda nova derivada parcial**, a correção $\partial\Gamma$ atua em **todos** os índices Y, preexistentes incluídos.

Compatível com o engine: `raw` = meu $G|_{\text{sem derivadas}}$; `yjet(word=(i,))` = $-\mathbb D_i[\text{raw}]$; `yjet(word=(i,j))` = $\mathbb D_i\mathbb D_j[\text{raw}] + \partial\Gamma\text{-correções}$; `xyjet` = $\nabla^X \circ (-\mathbb D)$. A função `coordinate_yward` (linhas 60–86) recebe os mesmos jatos e correções de $\partial\Gamma$ na primeira divergência (linhas 80–83).

---

## 5. Teste algébrico contra o kernel bilocal explícito

Convenção: os objetos do anexo são coeficientes de K (ordens 0 e 1). Faço as contas em coeficientes de K¹ (ordem em que as correções aparecem), com $w = (X-Y)^2 \to X^2 =: xx$ ao ancorar.

### 5.1 Ghost — primeira derivada [VERIFICADO — bate exatamente]

Do anexo: $G^{(1)a}{}_b|_0 = (xx\,\delta^a_b - X^aX_b)/(6w) + \delta^a_b(\tfrac14 - \tfrac54 L)$, pois $P_1|_0 = (xx\delta - XX^{\mathsf T})/6$ e `distance1`|₀ = 0.

**Lado Y** (regra `derivative` do anexo, $\partial_i^Y(1/w) = 2X_i/w^2$; só $\partial_i^Y P_1|_0 = (X_a\delta_{ib} - \delta_{ia}X_b)/2$ e o polo contribuem):

$$\partial_i^Y G^{(1)}\Big|_0 = \frac{X^a\delta_{ib} - \delta_i^a X_b}{2w} + \frac{X_i\,(xx\,\delta^a_b - X^aX_b)}{3w^2}.$$

**Menos lado X:**

$$-\partial_i^X G^{(1)}\Big|_0 = -\frac{2X_i\delta^a_b - \delta_i^aX_b - X^a\delta_{ib}}{6w} + \frac{X_i\,(xx\,\delta^a_b - X^aX_b)}{3w^2}.$$

**Diferença** (= o que dY = −dX perde):

$$\boxed{\;T_i{}^{a}{}_{b} \;=\; \frac{K\big(X^a\delta_{ib} + X_i\delta^a_b - 2X_b\delta_i^a\big)}{3w}\;}\qquad [\text{em coef. de } K:\ \tfrac{1}{3}(X^a\delta_{ib} + X_i\delta^a_b - 2X_b\delta_i^a)/w]$$

**Pela identidade:** $T = -(\kappa_i\partial + \rho_i)G^{(0)}$ com $G^{(0)} = \delta^a_b/w$. O pedaço diferencial morre porque $\kappa_i\cdot X = 0$ (a correção da transvecção é perpendicular ao radial — identidade útil: $\kappa_i^cX_c = 0$ [VERIFICADO]). Sobra $-(\rho_i G^{(0)})^a{}_b = +(\partial_b\kappa_i^a)/w = \tfrac{K}{3}(X^a\delta_{ib} + X_i\delta^a_b - 2X_b\delta_i^a)/w$. **Bate exatamente.**

**Componente não axial exibido** (dY=−dX preveria zero noutros canais): i=0, a=1, b=0 dá $T_0{}^1{}_0 = K X_1/(3w)$ — termo transversal à direção da derivada, presente no kernel e explicado pelo $\partial\kappa_i$.

### 5.2 Métrico — primeira derivada, um componente [VERIFICADO]

Com $S_{abce} = \tfrac12(\delta_{ac}\delta_{be} + \delta_{ae}\delta_{bc} - \delta_{ab}\delta_{ce})$, $M = xx\delta - XX^{\mathsf T}$, e `lower1`|₀ = $-M/6$: para i=0, $(a,b,c,e)=(1,1,2,2)$ (componente com pares, não trivial):

- lado Y: $\partial_0^Y\,\text{metric}^{(1)}_{1122}|_0 = X_0(xx - X_1^2)/(3w^2)$;
- menos lado X: $-\partial_0^X\,\text{metric}^{(1)}_{1122}|_0 = -X_0/(3w) + X_0(xx - X_1^2)/(3w^2)$;
- diferença: $+X_0/(3w)$;
- identidade: $T = -\big[(\partial_a\kappa_i^f)S_{fbce} + (\partial_b\kappa_i^f)S_{afce}\big]/w$ (sinal de covetor, §2.2) $= -\big[2\cdot(-\tfrac16 X_0)\big]/w\cdot(\text{dois termos}) = +X_0/(3w)$. **Bate.**

### 5.3 Ghost — segunda derivada [VERIFICADO: parte explicada bate; resto identificado]

**Do anexo** (computando $\partial_i^Y\partial_j^Y$ de $P_1/w$, de $-d_1\delta/w^2$ com $\partial_i^Y\partial_j^Y d_1|_0 = 2X_iX_j/3$, e o lado X correspondente; os termos $/w^3$ cancelam nos dois lados):

$$C_{ij}{}^{a}{}_{b} := \partial_i^Y\partial_j^Y G^{(1)}\Big|_0 - \partial_i^X\partial_j^X G^{(1)}\Big|_0 = \frac{-2\delta_{ij}\delta^a_b + \delta_j^a\delta_{ib} + \delta_i^a\delta_{jb}}{3w} + \frac{2\big(X_iX^a\delta_{jb} + X_jX^a\delta_{ib} + X_iX_j\delta^a_b - 2X_i\delta_j^aX_b - 2X_j\delta_i^aX_b\big)}{3w^2}.$$

**Pela identidade** ($\mathbb D_i\mathbb D_j G|^{(K^1)}$ + correção $\partial\Gamma \equiv -Q$ de §3.3):

$$\frac{\delta_i^a\delta_{jb} + \delta_j^a\delta_{ib} - 2\delta_{ij}\delta^a_b}{3w}\ \checkmark \qquad \frac{-4X_iX_b\delta_j^a - 4X_jX_b\delta_i^a + 2X_iX^a\delta_{jb} + 2X_jX^a\delta_{ib} + 2xx\,\delta_{ij}\delta^a_b + 2X_iX_j\delta^a_b}{3w^2}.$$

O termo $/w$ bate **exatamente**; o termo $/w^2$ bate **a menos de** $+\,\tfrac{2}{3}\,xx\,\delta_{ij}\delta^a_b/w^2$. Ou seja:

$$C_{ij}{}^{a}{}_{b} = \underbrace{\big[\text{parte explicada pela identidade de transvecção}\big]}_{\text{bate termo a termo}} \;+\; \boxed{\;R_{ij}{}^{a}{}_{b} \;=\; \frac{2K}{3}\,\delta_{ij}\,\delta^a_b\,\frac{xx}{w^2} \;=\; \frac{2K}{3}\,\frac{\delta_{ij}\delta^a_b}{w}\;}$$

**Componentes conferidos um a um** (previsto − kernel = $\tfrac{2}{3}\delta_{ij}\delta^a_b\,xx/w^2$ em todos): $(i,j;a,b) = (0,0;1,1),\ (1,1;0,0),\ (2,2;3,3),\ (0,0;0,0)$; e os nulos que devem ser zero porque $\delta_{ij}\delta^a_b=0$: $(0,1;2,3),\ (0,1;0,0),\ (0,1;1,1),\ (0,0;1,2),\ (0,0;0,1)$ — todos consistentes. Componente não axial com resto nulo: $C_{01}{}^{1}{}_{2} = -4X_0X_2/(3w^2)$, que dY=−dX preveria zero e a identidade reproduz exatamente.

**Identificação precisa do resto, sem anomalia:**
- **Ordens:** $K \times w^{-1} = K/\text{distância}^{2}$ — um polo do mesmo grau da singularidade plana, com um fator $K$ a mais; isotrópico (proporcional a $\delta_{ij}\delta^a_b$), **vive no setor diagonal/traço** (nada infiro sobre Q2 completo, conforme o guard-rail).
- **Origem rastreada:** é o pedaço **escalar** da correção da transvecção, $\kappa_i^j \supset -\tfrac{K}{3}xx\,\delta_i^j$, atuando na torre de polos do kernel plano: $(\kappa_i^c\partial_c)(\partial_j^X G^{(0)}) = -2\delta^a_b\,\kappa_i^j/w^2 = \tfrac{2}{3}(xx\,\delta_{ij} - X_iX_j)\delta^a_b/w^2$; o pedaço $X_iX_j$ bate no kernel, o pedaço $xx\,\delta_{ij}$ não tem contraparte — o numerador do anexo, $P_1|_0 = (xx\delta - XX^{\mathsf T})/6$, fornece o mesmo termo $-\delta_{ij}(xx\delta^a_b - X^aX_b)/(3w^2)$ nos dois lados e o cancela.
- **Leitura:** é um **déficit do truncamento algébrico do parametrix em segunda derivada** — localizado, quantificado e isotrópico —, não uma obstrução estrutural (anomalia). Em princípio é absorvível por um termo aditivo $O(K)$ ao ghost cuja dupla derivada Y em Y=0 forneça $\tfrac{2}{3}\delta_{ij}\delta^a_b/w$; **não prescrevo a correção** (fora de escopo; nenhum código muda). Não especulo sobre sua correspondência com a expansão de van Vleck do propagador completo: chequei que a contagem direta não fecha com o coeficiente ingênuo e deixo a origem profunda **ABERTA e nomeada**.

### 5.4 Estado da identidade no parametrix truncado

Primeira derivada: **vale exatamente** (com o termo perdido por dY=−dX exibido em §5.1–5.2). Segunda derivada: vale **a menos do resto** $R_{ij}{}^{a}{}_{b} = \tfrac{2K}{3}\delta_{ij}\delta^a_b/w$, com ordens e origem identificadas. A decomposição honesta é

$$\partial_i^Y\partial_j^Y G^{(1)}\Big|_0 \;=\; \partial_i^X\partial_j^X G^{(1)}\Big|_0 \;+\; C^{(\kappa,\rho,\partial\Gamma)}_{ij} \;+\; R_{ij},$$

onde $C^{(\kappa,\rho,\partial\Gamma)}_{ij}$ é a parte que a identidade de transvecção explica (e que dY=−dX perde), e $R_{ij}$ é o que a identidade não encontra no truncamento.

---

## 6. Escopo novo: recorrência de Killing para acelerar/verificar os jatos

Sem repetir o IBP do par bilocal. A recorrência §3 oferece um **controle independente** do engine e um caminho mais barato:

1. **Verificador:** para cada `kind`, `order`, `indices`, conferir `yjet(kind,order,indices,(i,))` contra $-\mathbb D_i[\texttt{raw}]$ (diferenciação em X de `raw` + ações $\rho_i$); e `yjet(...,(i,j))` contra $\mathbb D_i\mathbb D_j[\texttt{raw}]$ + correções $\partial\Gamma$ de §3.3. Os componentes da §5 são os casos de teste (já calculados à mão).
2. **Acelerador:** derivadas Y passam a ser **diferenciações em X de `raw`**, independentes do ponto-base Y — a mesma conta serve para todo Y; a recursão atual do engine re-deriva tudo por diferenciação simbólica em Y a cada palavra.
3. **Derivadas mistas:** `xyjet` = $\nabla^X \circ (-\mathbb D)$ aplicado a `yjet`, com o `gamma` do anexo fazendo as conexões X (linhas 42–55) — exatamente a regra §4.4.
4. **Composição com `coordinate_yward`:** os jatos $-\mathbb D_i$ entram nos mesmos slots; as correções de $\partial\Gamma$ na primeira divergência (linhas 80–83) são as de §3.3.

A implementação disso **não** faz parte desta entrega (nenhum código muda); fica como receita auditável.

---

## 7. Lacunas e pendências (declaradas)

1. **Sem execução:** toda a verificação é álgebra manual sobre as fórmulas lidas; a revisão local independente deve rodar os dois anexos e conferir os componentes da §5 (listados em 5.1, 5.2, 5.3). Resultado **DECLARADO**, não selado.
2. **Métrico, segunda derivada:** identidade estrutural escrita (M1 + §3.3); verificação numérica **pendente** — espero estrutura análoga de resto, mas não afirmo o coeficiente sem a conta.
3. **Forma fechada K<0** (cosh): declarada, não rederivada.
4. **Origem profunda do resto** $\tfrac{2K}{3}\delta_{ij}\delta^a_b/w$: rastreada até o pedaço escalar de $\kappa_i$ (§5.3); a correspondência com a expansão de van Vleck do propagador completo ficou **ABERTA e nomeada** (o coeficiente ingênuo não fecha; não especulo).
5. **Guard-rails:** o resto vive no setor diagonal — nada inferi sobre Q2 completo; W suave ausente dos kernels singulares — nenhum estado selecionado (em particular, nenhum com W=0).
6. **Escopo:** o IBP do par bilocal não foi repetido, conforme instruído.

---

**Síntese.** A transvecção candidata foi derivada e verificada na equação de Killing (com a correção de métrica ao abaixar o índice, sem a qual o teste falha), é única pelo jato $(e_i,0)$, e tem forma fechada na carta gráfica que expande ao próprio candidato. A identidade de invariância com todos os índices (ghost superiorX/inferiorY; métrico inferiorX²/inferiorY²) gera o operador de descida $\mathbb D_i^X = k_i^c\partial_c^X + \rho_i^X$, que responde à pergunta única afirmativamente e sem dY=−dX. Na segunda derivada, as correções de conexão ($\partial\Gamma$) e de comutador ($-Q$) foram derivadas e provadas iguais. Contra o kernel explícito: primeira derivada exata, com o termo perdido por dY=−dX exibido; segunda derivada exata a menos do resto isotrópico $\tfrac{2K}{3}\delta_{ij}\delta^a_b/w$, identificado com ordens $K/\text{distância}^2$ e origem, sem anomalia. Entrego a recorrência de Killing como acelerador/verificador dos jatos, e declaro o que falta: execução independente, segunda derivada do métrico, e a origem profunda do resto.