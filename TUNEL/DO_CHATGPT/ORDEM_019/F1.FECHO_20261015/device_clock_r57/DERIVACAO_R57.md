# R57 — leitura OH, gerador completo e referência de fase

Autor: codex-device-clock-r57. F1.FECHO_20261015, reivindicação de equipe 938; requisito R4.
Referência: `C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json`.

**Resultado:** construção parcial explícita e obstrução exata; **R4 NÃO está satisfeito**.
O cálculo simbólico verificou 34 identidades, sem aproximação, tolerância, dado observado
ou ajuste. Não é uma compilação Lean. Saída: `SYMBOLIC_RESULT_R57.json`.

## 1. Fontes e domínio do cálculo

O gerador foi reaproveitado de `F1.REDE/finite_device/run_finite_device.py:166–185`,
da patente v2 `PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex:343–370`,
e do original de janeiro recém-custodiado, parágrafos 71–80. Não foi reconstruído
um outro modelo: fatores na ordem entrada, saída, OH, cada um de dimensão 2.
As hipóteses de truncamento e perdas convencionais são as já explícitas no ensaio
finito da casa. Os pinos integrais constam de `SCOPE_R57.json`.

O original de janeiro, parágrafo 154, especifica medição lock-in de amplitude e
fase **da saída relativamente à entrada**. A v2, linhas 474–478, multiplica o
campo de saída pelo escalar `G_OH`; nas linhas 506–516 define
`G_OH(t)=a exp(i omega_OH t)`, `a=tanh(P_MW/P_th)`. Essa definição documental
não é por si uma demonstração de que a polarização OH do gerador tem essa evolução.
O relógio de referência externa e uma polarização livre do sistema são objetos distintos.

No modelo finito, todos os operadores são limitados; o GKLS é uma EDO linear
em matrizes 8×8. Usamos `h=H/hbar`, `Z=|g><g|-|e><e|`, `sigma+=|e><g|` e
`sigma-=|g><e|`:

```
h = omega_c (n_in+n_out) + omega_OH n_e
    + g_JC (a_in† sigma- + sigma+ a_in)
    + Omega_Rabi (sigma+ + sigma-),
J = a_out† sigma- + sigma+ a_in,
L(rho) = -i[h,rho] + kappa_in D[a_in](rho) + kappa_out D[a_out](rho)
         + gamma_OH D[sigma-](rho) + gamma_phi D[Z](rho) + lambda D[J](rho).
```

Todos os coeficientes e taxas são mantidos **estritamente positivos**. Nenhum termo
foi desligado. `lambda=beta*gamma_Lambda`; beta foi vinculado em runtime a
`ALPHA_FINE_CODATA_2018*sqrt(e)` da fonte pinada, não ajustado nem escrito como literal.
Os contraexemplos abaixo valem para todo lambda positivo, portanto também para esse vínculo.

Frequências `omega_c, omega_OH, g_JC, Omega_Rabi` têm dimensão s⁻¹ em h;
as taxas de GKLS `kappa_in, kappa_out, gamma_OH, gamma_phi, lambda` têm dimensão s⁻¹.
A amplitude a e o quociente de potências são adimensionais. Esses símbolos não
receberam calibração em segundos nesta entrega. Kappa de perda da cavidade não
foi identificado com normalização de Killing. O V0/hbar da face R9 não foi
identificado com Omega_Rabi, omega_OH ou o dobro de qualquer um deles.

## 2. Equação de Heisenberg completa, derivada

Para `D[J]†(A)=J†AJ-(J†JA+AJ†J)/2`, o cálculo fornece:

```
L†(sigma+) = (i omega_OH - gamma_OH/2 - 2 gamma_phi) sigma+
             + i g_JC a_in† Z + i Omega_Rabi Z
             + lambda [a_in† a_out† sigma-
                        - (n_in + a_out a_out†) sigma+/2].
```

Essa igualdade foi conferida entrada a entrada, com o Hamiltoniano e os cinco
dissipadores completos. A forma com `a_out a_out†` evita transferir indevidamente
CCR bosônicas ao cutoff: **a_out a_out†=I-n_out** neste modelo. No núcleo algébrico
de Fock sem truncamento, a mesma conta formal troca esse fator por `I+n_out`;
existência do semigrupo não limitado e condições de domínio não foram provadas aqui.

A componente diagonal `|000><000|` de
`L†(sigma+) - i omega_OH sigma+` é **i Omega_Rabi**, não zero.
Logo sigma+ não é eigenobservável universal de frequência omega_OH quando o
bombeamento está ligado. Os termos de JC e do salto holográfico também fazem
a equação depender de correlações entre modos e OH.

## 3. Contraexemplo que já começa com a amplitude prescrita

Para qualquer `0<a<1`, tome

```
rho0 = |0><0|_in ⊗ |0><0|_out ⊗ [[1/2,a/2],[a/2,1/2]],
z(t) = 2 Tr(rho(t) sigma+),
Gamma = gamma_OH/2 + 2 gamma_phi + lambda/2.
```

É uma densidade válida: os autovalores OH são `(1+a)/2` e `(1-a)/2`, positivos,
e o traço é 1. Pode-se tomar exatamente `a=tanh(P_MW/P_th)` para potências
positivas finitas. Portanto não foi fabricada uma divergência na amplitude inicial.

O cálculo exato dá:

```
z(0)  = a,
z'(0) = a(i omega_OH - Gamma),
z''(0)= a(i omega_OH - Gamma)^2 - a g_JC^2
        + 2 i Omega_Rabi (gamma_OH + lambda).
```

A forma documental `a exp(i omega_OH t)` exigiria `z'(0)=i omega_OH a`.
O residual é **-a(gamma_OH+4 gamma_phi+lambda)/2 < 0**. Assim a evolução
da polarização não é obrigatoriamente o fator documental, mesmo começando
com o mesmo valor e mantendo todos os termos físicos do modelo.

Também não basta descartar a amplitude e guardar apenas o argumento. Como a>0,
há um ramo local da fase perto de t=0. Para `phi=arg z`,

```
phi'(0) = omega_OH,
phi''(0)= Im[z''(0)/z(0) - (z'(0)/z(0))^2]
         = 2 Omega_Rabi (gamma_OH+lambda)/a > 0.
```

O bombeamento produz aceleração da fase nesse estado. O acoplamento JC aparece
explicitamente no termo `-a g_JC²` da segunda derivada. As perdas das cavidades
estão no gerador, embora algumas contribuições iniciais se anulem nessa preparação
de vácuo; não foram postas iguais a zero.

## 4. A redução OH, sozinha, não fecha universalmente

Use a mesma densidade OH `[[3/4,1/4],[1/4,1/4]]`, de determinante 1/8 e traço 1,
e vácuo de saída. Compare entrada em vácuo com entrada em `|+><+|`.
As duas preparações têm a mesma marginal OH e a mesma leitura inicial z=1/2.
Contudo:

```
z'_entrada_plus(0) - z'_entrada_vacuo(0) = i g_JC/2 - lambda/8 != 0.
```

Logo não existe, para todas essas preparações, uma lei autônoma na marginal OH
que reproduza o gerador completo. Esta é uma obstrução à redução mais simples,
não uma proibição de preparação fixa, descrição com memória, subespaço invariante
especial ou dilatação maior que venha a ser construída.

## 5. Construção positiva: leitor da fronteira fixa com fator escalar

A fonte multiplica por G_OH. A codificação que preserva a abertura é, portanto,

```
A_beta(z) = z S(theta_M),  theta_M = thetaMiguel(beta),
phaseReading(A_beta(z)) = z exp(i theta_M),
D_beta(w) = [w exp(-i theta_M)] S(theta_M).
```

As identidades de leitura e reconstrução foram conferidas exatamente.
Os pesos da primeira coluna são `|z|² beta` e `|z|²(1-beta)`; quando z≠0,
as proporções normalizadas continuam beta e 1-beta. Isto distingue o fator
escalar da órbita `S(theta_M+Omega*t)` de R56, que varia essas proporções.
Quando z=0, a matriz nula ainda é reconstruída, mas não há fase ou proporção
normalizada a informar.

O observável concreto candidato é `z(rho)=2 Tr(rho sigma+)`; ele é uma leitura
de expectativa da polarização. Positividade da marginal OH dá `|z|<=1`.
Isso produz uma codificação informacional explícita, não uma medição instantânea
exata em um exemplar, nem uma implementação física de canal com parâmetro dependente
do estado desconhecido. A identificação de z com o fator previsto G_OH foi testada
acima e não vale automaticamente para o gerador completo.

Também verificamos `z P+ + conj(z) P-` como decodificador da família de fases
opostas com amplitude real; essa família auxiliar não é a multiplicação escalar
da fonte e não deve substituí-la silenciosamente.

## 6. Construção positiva: referência externa por mudança de quadro

O lock-in do original lê fase relativa a uma entrada. Sob a hipótese explicitamente
nomeada **LAB_PHASE_LOCKED_DRIVE**, escreva um bombeamento no laboratório:

```
h_lab(t) = h0 + Omega_Rabi [exp(-i omega_d t) sigma+ + exp(i omega_d t) sigma-],
h0 = omega_c N_c + omega_OH n_e + g_JC(a_in† sigma- + sigma+ a_in),
N_total = N_c+n_e,  R(t)=exp(i omega_d t N_total),
rho_rot=R rho_lab R†.
```

Foi verificado exatamente:

```
h_rot = R h_lab R† + i R'R†
      = (omega_c-omega_d)N_c + (omega_OH-omega_d)n_e
        + g_JC(a_in† sigma- + sigma+ a_in) + Omega_Rabi(sigma++sigma-).
```

O salto J e Z são invariantes; os três saltos de abaixamento recebem apenas uma
fase de módulo 1, que cancela em seus dissipadores. Todos os termos de interação,
bombeamento e dissipação sobrevivem à mudança de quadro.
Por ciclicidade do traço e `R sigma+ R†=exp(i omega_d t)sigma+`, segue

```
z_lab(t) = exp(i omega_d t) z_rot(t).
```

Assim se obtém uma portadora de referência com envelope determinado pela dinâmica.
Se uma preparação estacionária rotativa for construída, seu z_rot constante será
calculado desse estado. **Não o fixamos em tanh(P/Pth)** para conseguir a conclusão.
Nem provamos aqui primitividade/estacionariedade geral, nem excluímos todos os
possíveis modos periféricos do gerador.

As frequências no H constante da patente são nomeadas como frequências absolutas.
O Hamiltoniano faseado e as detunings acima são modelagem adicional explícita;
não se reescreveu a fonte como se ela já tivesse declarado esse quadro.
Escolher ressonância omega_d=omega_OH, fixar uma preparação e justificar sua
resposta em potência continuam obrigações próprias.

## 7. Árvore de continuidade e critério R4

1. **Realização completa:** não demonstrada. O fator G_OH foi definido na fonte,
   mas não é consequência universal do H/J para a polarização natural examinada.
2. **Redução/dilatação:** a redução OH autônoma universal falha pelo par de estados
   acima. A mudança de quadro com referência externa foi construída sem retirar
   JC, bombeamento ou perdas; ela separa portadora e envelope, mas não deriva
   a lei tanh nem calibra o sistema físico.
3. **Obstrução tipada entregue:** equação adjunta completa, dois contraexemplos,
   aceleração da fase normalizada e codificação compatível com fronteira fixa.

Para satisfazer R4, ainda são necessários o observável implementado no receptor,
a relação laboratório/quadro de referência, a preparação/estado de operação,
as calibrações dos coeficientes e a lei que produz a amplitude do sinal. O gerador
de comutação também não fixa uma constante aditiva Eref no Hamiltoniano:
`[H+Eref I,rho]=[H,rho]`; a origem positiva exigida pela lei-raiz permanece uma
obrigação distinta já documentada em R7. Não se deduziu V0/Eref/Killing-kappa da fase.

O resultado orienta a próxima construção para o circuito fonte–sistema–receptor
com portadora explícita e envelope calculado. Não contradiz uma definição externa
de G_OH nem invalida a patente por nome; apenas impede promovê-la a saída derivada
do gerador sem os elos indicados. R5, H3 universal, originais, Bancada, memória
canônica e gate permanecem intactos. Esta entrega é candidata à revisão real distinta.
