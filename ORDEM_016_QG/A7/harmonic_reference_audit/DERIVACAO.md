[DERIVED — auditoria parcial exata de parecer Kimi; referência fixa preservada]

## A correção necessária à soma

O parecer harmonic_reference_intertwining foi lido integralmente.
Ele parte corretamente de

    R(F)=D_H+C_E N_H δ
        =X_P+D_rem+C_E(N_P+N_rem)δ.

Mas infere incorretamente D_H=X_P+D_rem e N_H=N_P+N_rem,
alegando unicidade da separação entre parte não local e parte local.
Essa separação não é única sem uma seção/escolha adicional: somar
uma distribuição local à parte denominada não local não altera sua
restrição fora da diagonal. A identidade que de fato decorre é

    D_H-X_P-D_rem=C_E(N_P+N_rem-N_H)δ.

Não se mudou R nem se acrescentou outro regulador. O defeito é uma
diferença entre referências diferenciais para a MESMA extensão.

## Contraexemplo com resto zero

Ponha U1=1/z e F=∂i²U1 em quatro dimensões euclidianas.
F é não nulo fora da diagonal. A referência principal é
X_P=∂i²R(U1); a harmônica é

    D_H=(∂i²-Box/4)R(U1).

Na prescrição já adotada, Box R(U1)=C_E δ, N_P=-1/4 e N_H=0.
Logo D_H-X_P=-C_E δ/4 embora F_rem=0. Os quatro valores de i
foram conferidos nos motores existentes. Esse exemplo refuta diretamente
a auditoria A-loc do parecer como requisito universal.

## Aplicação ao mesmo P4 já medido

Para qualquer polinômio homogêneo quartico P(q), o cálculo nas35
derivadas monomiais de U2=z^-2 dá

    N_P-N_H=-3 q² Lap_q(P)/128-q⁴ Lap_q²(P)/9216.

Aqui N_H é a representação harmônica do MESMO kernel P(∂)U2,
não o contato de todo o kernel real de uma bolha. A fórmula foi
verificada em toda a base e depois nos100 pares de fibras simétricas
do P4 da Hessiana principal já calculada.

Na ordem de invariantes
[q⁴trTH,q⁴trTtrH,q²(trT qHq+trH qTq),q²qTHq,qTq qHq]:

| objeto | coeficientes |
|---|---|
| N_P, preservado | (16039/57600,377/3600,-2371/28800,-6617/14400,539/2400) |
| N_H para este mesmo P4U2 | (1939/57600,707/57600,-623/14400,-3017/14400,539/2400) |
| N_P-N_H | (47/192,71/768,-5/128,-1/4,0) |

O defeito tem contração longitudinal não nula, registrada no JSON.
Apagá-lo alteraria a soma de Ward. A transferência correta conserva
o defeito junto da parte diferencial. Não se somam N_P e N_H como
contribuições de diagramas independentes.

## O exemplo harmônico do parecer: parte certa, conclusão excessiva

Para n(x)=6x0²-2x1²-2x2²-2x3², o contato relativo declarado foi
confirmado:

    N(n/z⁴)=5(q²-4q0²)/288.

Sua média angular sem peso é zero, mas o resíduo UV COMPLETO vale

    Res(n/z⁴)/C_E=-n(q)/96,

e não é zero. A média ponderada <n(omega) omega0²>=1/2 também
foi conferida. Portanto o exemplo distingue uma média escalar de
um símbolo tensorial completo; não demonstra invisibilidade dos
harmônicos superiores a esse símbolo. Além disso, este exemplo
tem resíduo de grau2: compará-lo com P4 exige separar as ordens
homogêneas, não atribuir a diferença apenas ao grau angular.

Para comparar funções racionais fora da diagonal, é preciso primeiro
impor z=x·x e reduzir a denominador comum. Por exemplo,
z^-2-(x·x)z^-3 é zero, apesar de seus coeficientes separados por
potência de z não serem individualmente zero. O motor represent
já realiza essa normalização; a formulação textual precisa mantê-la.

## Estatuto

Foram54 verificações da auditoria e340 da aplicação ao P4 efetivo,
CPU total4.390625s; ambos rc0. A resposta original foi preservada.
As amostras curvas e a fase lorentziana do parecer não foram validadas
nesta auditoria. Não se identificou o kernel integral da bolha com
P4U2; o resto não local continua explícito. Nenhuma prescrição,
fonte original, kernel Lean ou gate foi alterado. Q2 completa OPEN.
