[DERIVED — contatos logarítmicos e primeiros perfis curvos; REAL — CAS; OPEN — soma causal curva]
# A7.b — a extensão fixa aplicada aos termos de Hadamard
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T01:50:46.711397+00:00.

Conservada a prescrição de um par R(u)=FP[(1-a)mu^(2a)z^a u], definida
em tensor_extension antes dos cálculos finitos. A recorrência escalar
diferencial anterior não é silenciosamente aplicada aos numeradores:
sua correção por resíduos já consta daquela entrega. Aqui L=log(mu²z)
usa a mesma escala fixa. C=box(z^-1)/delta, conforme assinatura.

**Fórmula nova.** Se D[mu^(2a)z^(a-n)]=sum_j c_j(a)T_j(a), e rho_j é
o resíduo simples de T_j, então

    R(D[z^-n L^ell])-D R(z^-n L^ell)
      = -sum_j rho_j [c_j^(ell+1)(0)/(ell+1)
                                  +1_(ell>=1)c_j^(ell)(0)].

Derivação: introduza um segundo parâmetro b para o log e diferencie
ell vezes em b ANTES da parte finita em a. A diferença contém
sum_(t=0)^ell binom(ell,t)[c^(ell-t)(0)-c^(ell-t)(a)]partial_a^t T.
Apenas o polo contribui. Multiplicar por (1-a) dá as duas parcelas;
as somas binomiais são 1/(ell+1) e -1. Descartar polos múltiplos dá
um resultado diferente. O termo extra deriva da prescrição já fixada.

Para um símbolo homogêneo P_m(q), escreva Delta_q para seu Laplaciano.
Depois de retirar C, alguns mapas necessários são:

| núcleo | ordem D | contato |
|---|---:|---|
| z^-1 |3| -Delta_q P3/12 |
| z^-1 L |3| +Delta_q P3/24 |
| z^-1 |4| -Delta_q P4/16 + q² Delta_q²P4/384 |
| z^-1 L |4| 5Delta_q P4/96 + q² Delta_q²P4/768 |
| L |4| -Delta_q²P4/48 |
| L² |4| -Delta_q²P4/24 |

Controles por identidades distributivas: contato(box,z^-1)=-C delta;
contato(box,z^-1 L)=0 (definição do R2 anterior);
contato(box²,z^-1 L)=(3/2)C box delta;
contatos(box²,L)=-4C delta e (box²,L²)=-8C delta.
São 2345 verificações exatas em27mapas, duas assinaturas,
comparando a fórmula fechada com a parte finita completa, mais controles.
CPU 12.125s,rc0. A existência distributiva é insumo analítico,
não teorema provado pelo CAS.

**Aplicação ao começo da expansão curva.** No referencial de transporte
paralelo do espaço-forma, normalize cada propagador pelo fator escalar
1/(4pi²), conservando separadamente a inversa de fibra e as fases:

    G_A = I/z +(K/4)I -(E_A+2K I)L/4 + W_A + jatos superiores.

u0=Delta^(1/2)=1+Kz/4+…; a integral de Mellin do termo t a1 do calor
tem coeficiente -L/4, e a1=E+2K. W_A é o resto suave de referência;
não foi escolhido zero. O produto de dois fatores contém

    I/z² + [(K/2)I+W_A tensor I+I tensor W_B]/z
          -[E_A tensor I+I tensor E_B+4K I] L/(4z) + … .

E_m tem autovalores -2K (sem traço) e6K (traço); E_g=3K. Portanto o
coeficiente L/z vale, respectivamente nos pares (m0,m0),(m0,mtr),
(mtr,mtr),(m0,g),(mtr,g),(g,g): 0,-2K,-4K,-5K/4,-13K/4,-5K/2.
Seis perfis e seus mapas constam no JSON, 17checks,rc0,
CPU 0.125s. Exemplo (m0,g), só a parte geométrica:

    ordem3: -(3K/32)Delta_q P3;
    ordem4: -(37K/384)Delta_q P4-(K/3072)q²Delta_q²P4.

Somam-se os contatos de W_A tensor I+I tensor W_B; esses dados permanecem
explícitos. Ainda faltam a contração dos bitensores, seus jatos direcionais,
os vértices de curvatura, tadpoles e a soma de inserções da hierarquia causal.
Não se usou este perfil escalar como substituto de dez escalares para o
gráviton, nem como amplitude curva completa. A7.b continua ativa; Q2
completa e o gate não são declarados pagos.

Fontes, preregistros, comandos/scripts e logs nos dois manifestos.
