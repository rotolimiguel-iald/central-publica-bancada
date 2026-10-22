# R63 — homodinia bosônica comprimida e decoder de pares

**[DERIVED — candidato à revisão independente]** Resultado novo limitado ao receptor matemático. Foram verificadas 18 identidades simbólicas exatas, com EXIT 0, em 0,049 s; plano e script pinados antes da execução. Não se repetiu a dinâmica R62 nem se construiu outro Liouvilliano. O receptor físico ideal é hipótese explícita; não houve medição ou calibração.

## 1. Reaproveitamento e convenção

O acervo já fornece as quadraturas `X=(a+a†)/√2`, `P=i(a†−a)/√2` em `graviton_appendices.tex:124–127`, e homódino balanceado, oscilador local ajustável e tomografia em `311–333`. O plano R62 já fixa as quatro configurações XX, PP, XP, PX e seu decoder. Sua execução conservou o estado conjunto óptica–OH do gerador finito existente. As fontes e os arquivos estão pinados em `PLAN_R63.json`.

Há Fock e setores concretos em `F1.REDE/fock_construction/BosonicFock.lean:17–25` (vácuo, um fóton, soma de setores) e `BosonicTwoParticle.lean:42–69` (produto tensorial completo e setor simétrico). Essas peças são reaproveitadas como alvo cinemático; não foram reconstruídas ou recompiladas. A isometria abaixo não é declarada como uma nova prova Lean já integrada.

**[INPUT — receptor ideal]** Dois modos bosônicos ortonormais, com homodinia ideal e referências de fase conhecidas. A variável x é a quadratura adimensional, com variância de vácuo 1/2. A fórmula física em volts requer ganho, eficiência e filtro de modo. A transição OH não é um dos dois modos ópticos.

## 2. A POVM contínua no subespaço de zero/um fóton

Seja `P01=|0⟩⟨0|+|1⟩⟨1|` e `Xθ=(e^{−iθ}a+e^{iθ}a†)/√2`. As funções de onda são

\[
\psi_0(x)=\pi^{-1/4}e^{-x^2/2},\qquad \psi_1(x)=\sqrt2x\psi_0(x).
\]

A medida espectral ideal de Xθ, comprimida por P01, tem densidade de efeitos

\[
E^{01}_\theta(x)=\frac{e^{-x^2}}{\sqrt\pi}
\begin{pmatrix}1&\sqrt2xe^{-i\theta}\\\sqrt2xe^{i\theta}&2x^2\end{pmatrix}.
\]

Ela é positiva: a matriz é `w w†`, com `w=(1,√2x e^{iθ})`. A integral é I₂. Os momentos gaussianos utilizados são `μ0=1`, `μ1=0`, `μ2=1/2`, `μ3=0`, `μ4=3/4`; seguem da normalização gaussiana e da recorrência por integração por partes. O verificador usa esses valores exatos racionais, sem quadratura numérica ou tolerância.

Definindo `M_k=∫x^k Eθ01(x)dx`, obtém-se

\[
M_0=I_2,\qquad M_1=P_{01}X_\theta P_{01}
=\frac1{\sqrt2}\begin{pmatrix}0&e^{-i\theta}\\e^{i\theta}&0\end{pmatrix},
\qquad M_2=\begin{pmatrix}1/2&0\\0&3/2\end{pmatrix}.
\]

Mas `M1²=I₂/2`. Logo

\[
\boxed{P_{01}X_\theta^2P_{01}-(P_{01}X_\theta P_{01})^2=|1\rangle\langle1|=:n.}
\]

O setor intermediário |2⟩ produz esse termo. Para conferir os elementos de X² entre |0⟩ e |1⟩, basta incluir os níveis 0,1,2; não se faz uma aproximação desses elementos ao usar essa matriz auxiliar. A testemunha |1⟩ dá segundo momento físico **3/2**, frente ao valor **1/2** da medição espectral de Pauli truncada. A diferença é exatamente 1.

**Consequência:** `Eθ01(dx)` é uma POVM contínua, não a PVM dos dois autovalores de M1. Um estado com suporte somente em zero/um fóton ainda produz resultados homódinos contínuos. Não se devem usar os autovalores de Pauli como amostras de fotodetector. A normalização e a positividade desta POVM foram tratadas algebricamente; nenhum detector foi simulado.

## 3. O decoder sobrevive ao defeito de compressão

Para dois modos distintos e suas POVMs produto, o momento cruzado físico é

\[
\int xy\,E^{01}_{\theta_i}(dx)\otimes E^{01}_{\theta_o}(dy)
=M_{1,i}\otimes M_{1,o}=:UV.
\]

Os efeitos são identidade em OH. O enunciado vale inclusive quando o estado óptica–OH é correlacionado, pois é uma identidade de operadores. Os modos distintos comutam. Se `Q±` são os segundos momentos físicos da soma/diferença dos dois resultados, então

\[
Q_\pm=(U\pm V)^2+n_i+n_o,
\qquad\boxed{(Q_+-Q_-)/4=UV}.
\]

O defeito **cancela exatamente**, com o mesmo estado, as mesmas fases e a mesma normalização nos dois termos. Equivalentemente, no estado ρ, a identidade de polarização usa `||A||²ρ=Tr(ρA†A)`; os dois excessos de segunda ordem são iguais. Ganhos incompatíveis, filtros diferentes ou deriva entre aquisições não são cobertos por esse cancelamento ideal.

Portanto as quatro correlações físicas `qXX,qPP,qXP,qPX` fornecem os mesmos observáveis do decoder R62:

\[
\boxed{C=\langle a_i a_o\rangle=
\tfrac12[q_{XX}-q_{PP}+i(q_{XP}+q_{PX})]},
\quad
\boxed{B=\langle a_i^\dagger a_o\rangle=
\tfrac12[q_{XX}+q_{PP}+i(q_{XP}-q_{PX})]}.
\]

As médias de primeira ordem também são preservadas; assim a centragem por médias medidas preserva as covariâncias correspondentes. O cancelamento não autoriza substituir separadamente cada segundo momento físico pelo quadrado do operador comprimido: variâncias individuais e a soma das variâncias recebem o excesso de ocupação. O resultado R62 de reconstrução cruzada permanece válido; uma alegação de distribuição homódina de Pauli ou de variância física individual exigiria esta correção.

## 4. Isometria cinemática para modos da rede

**[INPUT]** Escolham `fi,fo∈H1`, de norma um e ortogonais. Nas peças de Fock já existentes, defina a inclusão V pelos vetores

\[
|00\rangle\mapsto\Omega,\quad |10\rangle\mapsto f_i,\quad
|01\rangle\mapsto f_o,\quad
|11\rangle\mapsto(f_i\otimes f_o+f_o\otimes f_i)/\sqrt2.
\]

Os quatro vetores têm norma um; os setores diferentes são ortogonais e `fi⊥fo`. Portanto V é isometria. Estenda por identidade no fator OH. Para qualquer estado conjunto finito ρ, `ρphys=VρV†` é positivo e tem traço um. A compressão dos efeitos físicos `V†E V` fornece exatamente a POVM acima e os momentos cruzados do decoder. **[DERIVED — cinemática]** Isso dá uma realização bosônica do contrato de leitura dos estados finitos, sem construir novamente Fock.

O mesmo transporte pode ser aplicado à trajetória R62 como uma família matemática de estados `Vρfin(t)V†`. **Não foi provado que essa trajetória seja gerada pelo Hamiltoniano/GKLS bosônico da patente.** Uma isometria de estados não é automaticamente um entrelaçador dos geradores, nem identifica o pacote físico da luz observado com fi/fo. Permanecem distintos o mapa cinemático, a escolha dos modos e a dinâmica física.

## 5. Campo de saída temporal: contrato que ainda precisa de instância

**[INPUT — proposta explícita, não localizada pronta como realização]** Para um campo viajante com distribuição de operadores `bout(t)`, um modo detectado é

\[
B_f=\int \overline{f(t)}b_{out}(t)dt,\qquad \int|f(t)|^2dt=1.
\]

O contrato deve fornecer as relações de comutação, o domínio e os dois modos acessíveis, em portas distintas ou pacotes ortogonais. O filtro f, a fase do oscilador local e o ganho devem ser conhecidos. Sob esses dados, a corrente homódina filtrada lê a quadratura de Bf; duas configurações de fase em cada ponta produzem as quatro correlações do item 3. Uma única corrente, o HBT de intensidades ou a polarização OH `σ+` não são automaticamente essas quatro leituras.

Mesmo assumindo uma dilatação de entrada–saída com convenção escolhida
`bout(t)=bin(t)+sqrt(κext) a(t)`, segue que Bf contém **campo incidente e integral temporal de a(t)**. Essa equação é aqui uma hipótese tipada de uma possível realização; não foi derivada do acervo nem do gerador finito. Não se identifica Bf com `aout(t0)` apenas pelo nome. O contrato precisa da porta externa, do filtro, do estado incidente/ruído, de eficiência/ganhos e da ligação entre os pacotes escolhidos e os operadores do dispositivo. Um lock-in de tensão relativa, incluindo atraso, também não é por definição o par anômalo C de tempos iguais.

**[OPEN]** Nenhuma igualdade física `G_OH=⟨Bf⟩`, `G_OH=C`, `G_OH=B` ou identificação de β foi inferida. O resultado concreto desta camada é a POVM comprimida positiva e normalizada e a invariância do decoder cruzado sob a correção exata de segundo momento. A identificação instrumental e o entrelaçamento dinâmico seguem necessários para fechar o requisito físico R4.

## 6. Evidência e escopo

`PLAN_R63.json` precede `START_R63.json`; `RESULT_R63.json` registra as 18 identidades, início/fim, duração e pinos. O script não chama provedor, não lê dado observado, não executa um.py, não evolui estado e não altera fonte/kernel/Bancada/memória/gate. Quem constrói não aceita: `mission_memory_review` revisa esta camada. O coordenador conserva as transições da missão e o requisito R4 permanece aberto até sua avaliação completa.
