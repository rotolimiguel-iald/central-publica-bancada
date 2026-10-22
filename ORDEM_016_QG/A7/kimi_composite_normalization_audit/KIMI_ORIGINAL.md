**ORDEM_016 — A-7.b · unidade: normalização local de inserções Euler e derivadas no setor de duas linhas**
Estatuto desta entrega: **[DECLARADO até verificação local]**. Nenhuma execução de código é alegada nesta resposta; toda conta abaixo é manual e auditável linha a linha, e as chamadas da engine residente (`logarithmic_contact_engine.py`) que conferem cada item estão indicadas como pendência. Auxiliar euclidiano R⁴; nenhuma continuação lorentziana presumida; originais intocados; Q2 não anunciada.

---

## 1. Convenções e identidades obrigatórias (independem de esquema)

**(C1)** \(z=x\cdot x\) em R⁴; \(f=1/z\); \(\Box f = C_E\,\delta^4\), \(C_E=-4\pi^2\); \(q\) denota derivada de delta sem fator \(i\); contatos normalizados por \(C_E\).

**(C2)** Família regularizadora: \(z^{a}\,t\), extensão meromorfa em \(a\); \(R(t)=\mathrm{FP}_{a=0}[(1-a)\,\mu^{2a}\,z^a\,t]\), com \(\mathrm{FP}\) = parte finita (subtrai o coeficiente de \(1/a\)). Família de par com distribuição \(\tau\): \(f_a=z^{\tau a-1}\), \(g_a=z^{(1-\tau)a-1}\); \(f_a g_a = z^{a-2}\) para todo \(\tau\).

**I0 — resíduos (provado aqui).** \(\operatorname{res}_{\lambda=-2-k} z^{\lambda} = \dfrac{\pi^2}{4^k\,k!\,(k+1)!}\,\Box^k\delta\), \(k\ge 0\).
*Prova.* Caso \(k=0\): \(\langle z^\lambda,\varphi\rangle \supset 2\pi^2\varphi(0)\int_0^\varepsilon r^{2\lambda+3}dr = \pi^2\varphi(0)/(\lambda+2)+\) finito. Recursão: \(\Box z^\lambda = 4\lambda(\lambda+1)z^{\lambda-1}\) (identidade meromorfa, válida fora dos polos e estendida) aplicada ao caso anterior; em \(\lambda=-2-u\): \(4\lambda(\lambda+1)/(\lambda+2)\to 8\), etc. ∎

**I1 — \(\Box f = C_E\delta\) (consistência).** Avaliar a identidade meromorfa em \(\lambda=-1\): \(4\lambda(\lambda+1)z^{\lambda-1} = 4\lambda\pi^2\delta + O(\lambda+1) \to -4\pi^2\delta\). O ponto estrutural: **\(4\lambda(\lambda+1)\) tem zero em \(\lambda=-1\), que cancela o polo de \(z^{\lambda-1}\)** — a família \(\Box z^{a-1}\) é *analítica* em \(a=0\) com valor \(C_E\delta\).

**I2 — comutação no par ordinário (robusta).** \(C_\Box(z^{-1}) := R(\Box f)-\Box R(f)=0\).
*Prova.* \(R(\Box f)=\mathrm{FP}_{a=0}[(1-a)\mu^{2a}\,4a(a-1)z^{a-2}]\); o produto \(4a(a-1)\cdot(\pi^2\delta/a+\mathrm{Pf})\) é analítico e vale \(-4\pi^2\delta\) em \(a=0\); \(\Box R(f)=\Box f = C_E\delta\). Iguais. ∎ Vale para **qualquer** polinômio de prescrição \(p(a)\) com \(p(0)=1\), não só \(1-a\).

**I3 — monômios contra derivadas de delta (provado por dualidade \(\langle\cdot,\varphi\rangle\)).**
\(x_i\delta=0\); \(x_i\partial_j\delta=-\delta_{ij}\delta\); \(x_i\Box\delta=-2\partial_i\delta\); \(x_ix_j\Box\delta=2\delta_{ij}\delta\); \(x_ix_j\Box^2\delta = 4\delta_{ij}\Box\delta+8\partial_i\partial_j\delta\).
*(Nota de processo: uma primeira passagem minha usou \(x_i^2\Box^2\delta=2\Box\delta\); o valor correto, por \(\Box^2(x_i^2\varphi)(0)=4\Box\varphi(0)+8\partial_i^2\varphi(0)\), é o de I3. Fica registrado porque a tabela muda com ele.)*

**I4 — família do colapso Euler.** \(\Box f_a = 4\tau a(\tau a-1)\,z^{\tau a-2}\to C_E\delta\) quando \(a\to 0\), para todo \(\tau\) (inclusive \(\tau=0,1\), onde o fator zera o polo). O colapso de uma linha é canônico, sem prescrição nova.

---

## 2. O que o \(R\) de pares fixa (já determinado pela prescrição)

- \(R(z^{-1})=z^{-1}\), \(R(\partial_i z^{-1})=\partial_i z^{-1}\); \(C_{\partial_i}(z^{-1})=0\); \(C_{\partial_i\partial_j}(z^{-1})=0\) para \(i\neq j\) (o contato possível, \(x_ix_j\Box\delta=2\delta_{ij}\delta\), zera fora da diagonal).
- \(R(z^{-2})=\mathrm{Pf}(z^{-2})+\pi^2(2\log\mu-1)\,\delta = \mathrm{Pf}+C_E\rho_2\delta\), \(\rho_2=(1-2\log\mu)/4\).
- **\(C_\Box(z^{-2})=R(\Box z^{-2})-\Box R(z^{-2})=-\pi^2\Box\delta = C_E\cdot\tfrac14\,\Box\delta\)** — verificado por duas vias: (i) direta, \(\mathrm{FP}[(1-a)\mu^{2a}\,4(a-2)(a-1)z^{a-3}] = 8\mathrm{Pf}(z^{-3})+\pi^2(2\log\mu-\tfrac52)\Box\delta\), contra \(\Box R(z^{-2})=8\mathrm{Pf}+\pi^2(2\log\mu-\tfrac32)\Box\delta\); (ii) por componentes \(\sum_i\partial_i^2\) com I3. **Não é zero**: em grau \(\ge 2\), derivar antes e depois da regularização difere por contato computável.

---

## 3. As três exigências como equações funcionais

Para monômios de derivadas \(D_1,D_2\) (ordem total \(\le 4\)) aplicados às duas linhas do par \(z=(x-y)^2\):

- **(i) Leibniz:** \(\partial_i N[F_1F_2] = N[\partial_iF_1\,F_2]+N[F_1\,\partial_iF_2]\) *exata* (não só fora da diagonal).
- **(ii) Troca de linhas:** \(N\) simétrica sob \(1\leftrightarrow 2\); em particular invariante sob \(\tau\leftrightarrow 1-\tau\) na família \((f_a,g_a)\).
- **(iii) EOM:** \(T((\Box\varphi)(x)\,\varphi(y)\,X) = C_E\,\delta^4(x-y)\cdot[\text{remanescente estendido}] + T(:\!\Box\varphi\,\varphi\!:X)\), com colapso e remanescente **definidos** (não decretados).

---

## 4. Construção (resposta: **sim**, com a regra e o custo determinados)

**Regra mestra (Leibniz-first sobre o par regularizado):**
\[
N[(D_1f)(D_2f)] \;:=\; \big[\text{termo }(D_1,D_2)\text{ de Leibniz}\big]\; D^{\mathrm{tot}}_{D_1D_2}\,R\!\left(f_ag_a\right)\Big|_{\mathrm{FP,\;sim}}
\]
isto é: (a) o produto é regularizado como par (\(f_ag_a=z^{a-2}\), um único \(a\)); (b) as derivadas totais são aplicadas **depois**, como derivadas de distribuição — Leibniz vale tautologicamente; (c) a atribuição de qual derivada cabe a qual linha é fixada por (ii); (d) a prescrição inclui a **simetrização explícita** \(\tfrac12(N_\tau+N_{1-\tau})\).

**Fixação das atribuições (sem liberdade):**
- ordem 1: \(N[f\,\partial_i f] := \tfrac12\partial_i R(z^{-2})\) — único compatível com (i)+(ii).
- ordem 2: \(A_{ij}:=N[f\,\partial_i\partial_jf]\), \(B_{ij}:=N[\partial_if\,\partial_jf]\): (i)+(ii) fixam \(A_{ij}+B_{ij}=\tfrac12\partial_i\partial_jR(z^{-2})\); a **separação** \(A-B\) vem da prescrição de par ("derivar antes"): \(A^R_{ij}=R[-2\delta_{ij}z^{-3}+8x_ix_jz^{-4}]\), \(B^R_{ij}=R[4x_ix_jz^{-4}]\). A diferença entre as duas leituras é o contato de Leibniz:
\[
\big(A^R_{ij}+B^R_{ij}\big)-\tfrac12\partial_i\partial_jR(z^{-2}) \;=\; \Delta^{(2)}_{ij}\;=\;\text{contato determinado},
\]
cuja agregação \(\sum_i\Delta^{(2)}_{ii} = C_\Box(z^{-2}) = C_E\cdot\tfrac14\Box\delta\neq 0\) (item 2). **Conclusão estrutural:** "derivar antes" (aplicar \(R\) ao produto das famílias derivadas) **não** satisfaz Leibniz em grau \(\ge 2\); a normalização que satisfaz (i) é a Leibniz-first acima, e a diferença é uma **correção local determinada** \(\Delta\), não um ajuste livre.

**O papel de \(\tau\) (diagnóstico, não escolha).** Comparando derivar antes/depois sobre a família: a soma simetrizada das atribuições é \(\tau\)-independente; a assimetria residual \(N_\tau-N_{1-\tau}\) mede a violação potencial de (ii). No colapso bilateral (abaixo) a exigência (ii) seleciona o **ponto fixo** \(\tau=\tfrac12\): é o único valor com \(N_\tau=N_{1-\tau}\); não é assumido — é derivado da exigência. A varredura em \(\tau\) permanece como teste de sensibilidade.

---

## 5. EOM no setor de duas linhas: colapso e produto remanescente, definidos

**Definição (colapso).** A inserção de Euler na linha 1 do par:
\[
N[(\Box f)\,F_2] \;:=\; \mathrm{FP}_{a=0}\!\left[(1-a)\mu^{2a}\,(\Box f_a)\,(D_2 g_a)\right],\qquad \Box f_a = 4\tau a(\tau a-1)z^{\tau a-2}.
\]
**Definição (produto remanescente).** \([\,\delta\cdot F_2\,]_{\mathrm{ext}} := N[(\Box f)F_2]/C_E\) — a extensão do produto proibido \(\delta\cdot f\), obtida da família, **sem** assumir \(f(0)=0\) (que não existe) e sem decretá-lo zero.

**Conta central (duas vias, conferidas entre si).** Com \(F_2=f\):
- via família: \((\Box f_a)g_a = 4\tau a(\tau a-1)z^{a-3}\); o polo de \(z^{a-3}\) (I0, \(k=1\): \(\pi^2\Box\delta/8a\)) dá
\[
N_\tau[(\Box f)f] = -\tfrac{\pi^2}{2}\,\tau\,\Box\delta \;=\; C_E\cdot\tfrac{\tau}{8}\,\Box\delta .
\]
- via Leibniz na família: \((\Box f_a)g_a = \Box(f_ag_a) - 2\nabla f_a\cdot\nabla g_a - f_a\Box g_a\); o coeficiente de \(a\) do lado direito é \(-4\tau\), reproduzindo \(-\tfrac{\pi^2}{2}\tau\Box\delta\). A simetrizada \((\Box f_a)g_a + f_a(\Box g_a)\) dá \(-\tfrac{\pi^2}{2}\Box\delta\); metade:
\[
[\,\delta\cdot f\,]_{\mathrm{ext}} \;=\; C_E\cdot\tfrac{1}{16}\,\Box\delta \qquad(\tau\text{-independente}).\;\;\textbf{[DECLARADO]}
\]
**Duplo colapso (resultado, não hipótese).** \(N[(\Box f)(\Box f)] = \mathrm{FP}[16\tau(1-\tau)a^2(\tau a-1)((1-\tau)a-1)z^{a-4}] = 0\): o fator \(a^2\) mata o polo simples. A extensão atribui **zero** a \(\delta\cdot\delta\) — decorrência, não convenção \(f(0)=0\).

**Definição explícita de \(T((\Box\varphi)(x)\varphi(y)X)\).** Como \(\Box f = C_E\delta\) exatamente (sem parte suave fora da origem), a inserção de Euler é **inteiramente contato**: não há residual suave. Então
\[
T((\Box\varphi)(x)\,\varphi(y)\,X) \;=\; C_E\,\delta^4(x-y)\cdot T(X)_{\mathrm{ext}}
\]
onde \(T(X)_{\mathrm{ext}}\) é o E-produto do remanescente **com os pontos identificados**, definido pela mesma família; quando \(X\) contém a segunda linha do par, o valor é a entrada da tabela (\(C_E\cdot\tfrac1{16}\Box\delta\) para uma linha remanescente livre). Para \(X\) suave na diagonal, \(T(X)_{\mathrm{ext}}=T(X)|_{x=y}\). A inserção normal-ordenada \(:\!\Box\varphi\,\varphi\!:\) é o que sobra após subtrair o colapso — aqui, zero (tudo é contato).

---

## 6. Tabela mínima de contatos (setor de duas linhas, ordem total ≤ 4)

Em unidades de \(C_E=-4\pi^2\), \(\log\mu\) explícito; coluna "status" separa o obrigatório do esquema. Valores numéricos absolutos: **[DECLARADO — verificação local pendente]**; identidades (zeros, \(\tau\)-independência, razões) verificadas por duas vias nesta entrega.

| # | objeto | identidade | valor (unid. \(C_E\)) | status |
|---|---|---|---|---|
| T0 | resíduos | I0 | \(\operatorname{res}_k/C_E = -4^{-(k+1)}/(k!(k+1)!)\,\Box^k\delta\) | obrigatório |
| T1 | \(C_\Box(z^{-1})\) | \(R\Box-\Box R\) | \(0\) | obrigatório (independe de \(p(a)\), \(p(0)=1\)) |
| T2 | \(R(z^{-2})\) | par livre | \(\mathrm{Pf} + \tfrac{1-2\log\mu}{4}\,\delta\) | esquema (\(\log\mu\)) |
| T3 | \(C_\Box(z^{-2})\) | \(R\Box-\Box R\) | \(+\tfrac14\,\Box\delta\) | obrigatório (correção Leibniz agregada) |
| T4 | \(N[f\partial_if]\) | Leibniz-first | \(\tfrac12\partial_iR(z^{-2})\) | fixado por (i)+(ii) |
| T5 | \([\delta\cdot f]_{\mathrm{ext}}\) | colapso bilateral | \(\tfrac1{16}\,\Box\delta\) (unilateral: \(\tau/8\)) | fixado por (iii)+(ii) |
| T6 | \([\delta\cdot\delta]\) | duplo colapso | \(0\) | obrigatório (resultado) |
| T7 | assimetria \(\tau\) | diagnóstico | \(N_\tau-N_{1-\tau} = \tfrac{2\tau-1}{8}\,\Box\delta\) | diagnóstico; zera em \(\tau=\tfrac12\) |
| T8 | monômios × delta | I3 | ver §1 | obrigatório |

Verificação local proposta (engine residente): `contact(1,0,(i,i))` somado em \(i\) deve reproduzir T1; `contact(2,0,(i,i))` somado deve reproduzir T3; `differentiated`+`residue` com \(n=3\) reproduz a família de T5 (a via bilateral exige a identidade de Leibniz da família ou a extensão da engine a dois parâmetros \(\tau\) — pendência técnica, não conceitual).

**Nota de reconciliação (obrigatória antes de selar):** minha leitura manual da engine atual dá, para `contact(1,0,□)`, valor \(-1\cdot C\), enquanto o cálculo direto aqui dá T1 \(=0\); para `contact(2,0,□)`, \(-3\cdot C\) contra \(+\tfrac14 C_E\Box\delta\). O ponto exato da divergência a inspecionar na verificação local: (a) o `factor` da engine usa \(\partial_A\) do coeficiente — que codifica o fator \((1-a)\) da prescrição — contra o valor em \(A=0\) usado na leitura literal de \(R\); (b) a convenção de sinal/normalização de `residue` frente a I0. Registro a discrepância com o ponto, sem resolver por decreto.

---

## 7. Liberdades locais remanescentes; necessidade de T1

- **L1 — \(\log\mu\):** um parâmetro real; desloca todos os coeficientes logarítmicos correlacionadamente (o "MS-bar" da família).
- **L2 — o polinômio de prescrição \(p(a)\), \(p(0)=1\):** a prescrição usa \(1-a\); outras escolhas deslocam constantes finitas por grau, correlacionadas pela mesma família.
- **L3 — \(\tau\):** não é liberdade física; diagnóstico absorvido pela simetrização (ponto fixo \(\tau=\tfrac12\) derivado de (ii)).
- **L4 — T1/referência suave:** **não precisa ser escolhido neste setor.** A família \(z^a\) fornece a referência; não há subdivergência aninhada em duas linhas com inserções locais até ordem 4. T1 será necessário no setor com subdivergências aninhadas (três linhas ou mais) — pendência declarada para a próxima unidade, com o critério de fatoração sobre a mesma família.
- **Não há** liberdade de ajustar coeficientes de contato para cancelar resíduos: T3, T5, T6 são determinados.

---

## 8. Resposta e primeiro conflito (versão endurecida)

**Resposta: sim** — a normalização existe, é forçada e essencialmente única: Leibniz-first sobre o par regularizado, simetrização \(\tau\leftrightarrow 1-\tau\) (ponto fixo \(\tfrac12\) derivado), colapso Euler pela família \(\Box f_a\), remanescente por \([\delta\cdot F]_{\mathrm{ext}}\) definido (T5/T6).

**Primeiro conflito se as exigências forem endurecidas:**
- Se for exigido "derivar antes" literal **com** Leibniz exata **sem** correção: o primeiro conflito aparece já na **ordem 2 do par**: \(R(\Box z^{-2})\neq\Box R(z^{-2})\) (T3, contato \(C_E\Box\delta/4\neq 0\)). A normalização que precisa mudar: de "derivar antes" para "Leibniz-first + correção local determinada" — equivalentemente, adicionar ao esquema a contracção fixa \(-C_E\Box\delta/4\) nesse canal (determinada, não ajustável).
- Se for exigida simetria de troca com \(\tau\) fixo \(\neq\tfrac12\) e sem simetrização: conflito no colapso bilateral (T7: \(N_\tau\neq N_{1-\tau}\)). A mudança: impor a média \(\tfrac12(N_\tau+N_{1-\tau})\) ou o ponto fixo \(\tau=\tfrac12\).

---

## 9. Hipóteses, limites, pendências

**Hipóteses:** R⁴ euclidiano; prescrição \(R\) com \(p(a)=1-a\) e \(\mu\) fixos; extensão meromorfa com polos simples (válida para potências inteiras); Euler livre \(\Box\varphi\) (o setor \(V'(\varphi)\) fica para a próxima unidade); campos externos balanceados, off-shell permitido.

**Limites:** valores absolutos dependem da convenção I0/\(C_E\) (declarada); reconciliação com a engine pendente no ponto marcado (§6); sem continuação lorentziana; \(q\) sem fator \(i\); nenhum coeficiente ajustado a resíduo conhecido; nenhuma concordância de modelos usada como prova.

**Pendências de verificação local:** (i) executar a engine para T1 e T3 e reconciliar o ponto de §6; (ii) conferir T5/T6 pela extensão \(\tau\)-dupla ou pela via Leibniz da família; (iii) confirmar a anomalia isotrópica por componente \(\kappa_i=-\pi^2/8\) em \(\partial_i^2\mathrm{Pf}(z^{-2})\), usada só em conta intermediária e marcada aqui explicitamente.