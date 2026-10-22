# R66 — reservatório de colisões, entrada coerente e o gerador completo

Em nome de codex-device-clock-r57, `/root/miguel_r56_review`.
**[DERIVED — candidato matemático]** Prova em dimensão finita. A campanha numérica ainda depende do pré-registro e da revisão independente. Nenhum parâmetro físico é ajustado.

## Objeto reaproveitado

O sistema S é a mesma face de dimensão8, fatores `(entrada,saida,OH)` de dimensão2, usada em R62/R64. Isso é o corte independente0/1 dos dois modos ópticos, **não** o corte por número total da construção bosônica separada da raiz. Reutilizam-se as funções puras de `finite_device_functions_r62.py`, a parametrização e o vínculo beta em runtime.

Defina `sigma_-=|g><e|`, `sigma_+=sigma_-†`, `Z=|g><g|-|e><e|` e

\[
h_0=\omega_c(n_i+n_o)+\omega_{OH}n_e+
g_{JC}(a_i^\dagger\sigma_-+\sigma_+a_i),\quad
h=h_0+\Omega(\sigma_++\sigma_-).
\]

Todos os cinco canais são conservados:

\[
L_1=\sqrt{\kappa_i}a_i,\quad L_2=\sqrt{\kappa_o}a_o,
\quad L_3=\sqrt{\gamma_{OH}}\sigma_-,\quad
L_4=\sqrt{\gamma_\phi}Z,\quad
L_5=\sqrt{\beta\gamma_\Lambda}J,
\quad J=a_o^\dagger\sigma_-+\sigma_+a_i.
\]

O alvo é exatamente `L(rho)=-i[h,rho]+sum_j D[Lj](rho)`. O canal5 tem um **único** índice de banho para a soma J. Dois banhos separados para suas parcelas mudam o alvo. O índice do canal não implica escolha exclusiva entre dispositivos nem localização espacial já demonstrada.

## 1. Colisão explícita e CPTP em cada passo

Uma ancilla é E=C6, base `|0>,|1>,...,|5>`. Defina

\[
V=\sum_{j=1}^5(L_j\otimes|j\rangle\langle0|
-L_j^\dagger\otimes|0\rangle\langle j|),\qquad
U_\delta=\exp(\sqrt\delta V-i\delta h_0\otimes I_E).
\]

V é anti-adjunto, h0 é auto-adjunto; portanto Uδ é unitário para todo δ>=0. Para qualquer estado normalizado ηδ de E, `Phiδ(rho)=Tr_E Uδ(rho tensor ηδ)Uδ†` é CPTP. No caso puro `ηδ=|bδ><bδ|`, os Kraus são `Kj=<j|Uδ|bδ>` e `sum Kj†Kj=I`. Esta é uma dilatação explícita, não a repetição da definição abstrata de um canal.

**[INPUT instrumental]** A cada passo entra uma ancilla nova no mesmo estado, independente do sistema, das anteriores e das futuras. O canal é homogêneo; não há realimentação nem correlação inicial oculta entre bins. A cadeia é uma realização matemática escolhida do gerador. Sua implementação física e a atribuição dos portos ao aparelho permanecem próprias de R4.

## 2. Vácuo: expansão com erro local de ordem2

Primeiro, `bδ=|0>` e h0 qualquer Hamiltoniano limitado. Escreva ε=sqrtδ. A expansão da exponencial dá

\[
K_0=I+\delta\left(-ih_0-\tfrac12\sum_jL_j^\dagger L_j\right)+O(\delta^2),
\qquad K_j=\sqrt\delta L_j+O(\delta^{3/2}).
\]

Se `P=|0><0|-sum_j|j><j|`, então `(I tensor P)V(I tensor P)=-V` e P comuta com h0 tensor I. Logo `U(-ε)=P U(ε)P`. O canal de vácuo é par em ε: todos os termos de ordem ímpar desaparecem após o traço parcial. A analiticidade de matrizes finitas fornece, uniformemente para δ pequeno,

\[
\Phi_\delta=I+\delta\left(-i[h_0,\cdot]+\sum_jD[L_j]\right)+O(\delta^2).
\]

A paridade é necessária para justificar a ordem2: uma expansão de U até ε², sozinha, só daria uma estimativa grosseira em δ^(3/2).

## 3. O bombeamento sai de uma entrada coerente

Suponha `gamma_OH>0`, como na instância reutilizada. No canal3, prepare

\[
b_\delta={|0\rangle+\sqrt\delta\,\alpha|3\rangle\over
\sqrt{1+\delta|\alpha|^2}},\qquad
\alpha={i\Omega\over\sqrt{\gamma_{OH}}}.
\]

As amplitudes de Kraus agora são

\[
K_0=I+\delta\left(-ih_0-\tfrac12\sum_jL_j^\dagger L_j
-\alpha L_3^\dagger-\tfrac12|\alpha|^2 I\right)+O(\delta^2),
\]
\[
K_j=\sqrt\delta\,(L_j+\alpha\,\delta_{j3}I)+O(\delta^{3/2}).
\]

Somando `Kj rho Kj†`, os termos `|alpha|² rho` se cancelam e os termos lineares em alpha são

\[
[\alpha^*L_3-\alpha L_3^\dagger,\rho]
=-i[h_{drive},\rho],\qquad
h_{drive}=i(\alpha^*L_3-\alpha L_3^\dagger).
\]

Com a fase acima, `hdrive=+Omega(sigma_-+sigma_+)`. Não há fator1/2: o alvo escrito na patente é `Omega sigma_x`. O sinal oposto de alpha troca o sinal da bomba; alpha=0 a retira. Todos os dissipadores permanecem, inclusive `gamma_OH D[sigma_-]`.

Também aqui `b(-ε)=P b(ε)`, e a mesma conjugação mostra que o canal reduzido é par em ε. Assim

\[
\Phi_\delta=I+\delta\mathcal L+O(\delta^2)
\]

para o **mesmo gerador completo R62/R64**. Não se pôs a bomba diretamente no h0 usado nesta realização. Uma segunda realização de controle usa ancilla em vácuo e h completo; converge ao mesmo alvo. Se gamma_OH=0, a fórmula para alpha não existe; a alternativa válida é drive clássico externo em h, não divisão por zero ou bombeamento fictício.

Os símbolos estão em unidades adimensionais da instância. Em unidades físicas, Lj tem dimensão `tempo^-1/2`, alpha a mesma dimensão, εLj e εalpha são adimensionais. A conversão integral de tempo/portas/filtros do R65 continua necessária para calibrar o aparelho.

## 4. Convergência do processo reduzido

Para T fixo e δ=T/N, cada Phiδ é CPTP e `exp(δ L)` também. Em norma diamante, ambas têm norma1. A analiticidade e a expansão fornecem `||Phiδ-exp(δL)||_diamond <= C δ²` em algum intervalo `0<=δ<=δ0`, com C finita dependente dos operadores fixados. Pelo telescópio,

\[
\|\Phi_{T/N}^{N}-e^{T\mathcal L}\|_\diamond
\le N C(T/N)^2=CT^2/N=CT\delta\longrightarrow0.
\]

Isso prova a convergência para todo estado do sistema, inclusive quando entrelaçado com uma referência finita. A prova é de dimensão finita e não exige ajuste empírico. Não foi calculado aqui um valor ótimo de C. A campanha verifica erro de superoperador em norma de Frobenius, distinto de uma medição da norma diamante; sua ordem numérica é um controle, não substituto da prova.

## 5. Ponte concreta para bins temporais de Fock

Para uma partição uniforme de[0,T], defina `f_k=1_bin_k/sqrtδ` e cinco canais ortogonais. No espaço de um quantum `L²([0,T];C5)`, os vetores `f_k tensor e_j` são ortonormais. Pela fatoração de Fock em soma ortogonal de modos, cada E_k=C6 inclui-se isometricamente como o vácuo e os cinco estados de uma excitação de seu bin. O produto de N ancillas inclui-se em Fock sobre esses modos e, depois, no Fock temporal completo, com vácuo nos modos complementares.

Para cada bin, Uδ atua no sistema tensor esse subespaço. Pode ser estendido por identidade no complemento ortogonal, formando um unitário no sistema tensor Fock do bin. A composição cronológica conserva as ancillas anteriores como saída e usa somente a nova ancilla em cada etapa. Logo o canal de N passos tem uma dilatação exata por esse reservatório Fock temporal **com cortes locais no ambiente**. Não se alegam CCR exatos para as matrizes `|j><0|` isoladas nem um limite unitário HP já demonstrado.

O estado coerente de amplitude constante alpha no canal3 tem amplitude `z=alpha sqrtδ` em cada bin. A projeção normalizada dele sobre vácuo/uma excitação é exatamente bδ. Se `x=δ|alpha|²`, a fidelidade quadrática por bin é `e^-x(1+x)`. Para o produto,

\[
1-|\langle b_\delta^{\otimes N}|\mathrm{coh}(\alpha1_{[0,T]}e_3)\rangle|^2
\le N x^2/2=T\delta|\alpha|^4/2\longrightarrow0.
\]

Usou-se `e^-x(1+x)>=1-x²/2`, provada derivando a diferença para x>=0. A aproximação de banho converge ao estado coerente temporal; o erro de distância de traço dos estados puros é no máximo a raiz do lado direito. A convergência do canal reduzido já foi provada no item4. Isso não prova automaticamente convergência forte das dilatações, de todos os observáveis de saída, de uma rede de Poincaré, nem igualdade entre o sistema hard-core e o sistema bosônico não limitado da patente.

## 6. Controles e interpretação

O pré-registro fixa uma única campanha, quatro passos δ=1/N com N=16,32,64,128, a parametrização R62, beta em runtime e gammaLambda=1 como INPUT. Conserva h0, acoplamento e cinco dissipadores. Verifica unidade/Kraus/Choi, expansão local, erro global e ordem de convergência nas duas realizações do drive. Os controles negativos comparam os geradores de banho dividido, bomba ausente e fase invertida; a soma J no mesmo canal tem de conservar os termos cruzados.

R65 demonstrou que D[J] não é covariante sob o h0 livre fora da ressonância. A construção presente resolve a existência matemática de um reservatório não restrito àquela hipótese secular de equilíbrio; não alega derivar esse J do banho térmico Davies da patente. As colisões e a entrada coerente são hipóteses instrumentais/recursos externos explícitos. R4/R5 integrais, calibração beta/Gamma, sistema bosônico global e localização permanecem fora do aceite deste componente.
