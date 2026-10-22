[DERIVED — adjunção exata e contato de localização da fonte; Q2 integral OPEN]

# Adjunção não é comutação com a extensão

O parecer Kimi9118 tem a orientação adequada E_X(A-div_Y B), mas a
fórmula de adjunção acrescenta um contato no lugar errado. Para um
kernel já estendido U e teste compacto T, a definição de derivada
distribucional e E*=E dão exatamente

    <E U,T>=<U,E T>.

Não há parcela extra nessa igualdade. Se f é inicialmente definido
fora da diagonal e R é a extensão fixada, defina

    C_E(f)=R(E f)-E R(f).

Então, e somente então, a comparação com a derivada ordinária estendida é

    <R(E f),T>=<R(f),E T>+<C_E(f),T>.

Confundir E R(f) com R(E f) transfere indevidamente o defeito para a
adjunção. O teste escalar plano ilustra a diferença: para u=1/r² e
phi=exp(-r²), integral u Delta phi=-4pi²=<-4pi²delta,phi>.
A igualdade já contém o contato da derivada distribucional. Acrescentar
outro contato à adjunção o contaria duas vezes. O exemplo usa teste de
Schwartz e a distribuição temperada correspondente; a definição para
testes compactos não depende desse exemplo.

O E aqui é o operador Einstein linearizado formalmente autoadjunto no
pareamento e suporte já fixados. Não trocar por um operador mínimo
gauge-fixado, nem transportar índices de X para Y apenas pelo nome.

## Correções pontuais ao parecer

A tabela de derivadas de 1/z até terceira ordem é consistente com a
prescrição fixa na orientação D R-R D (oposta à do motor de contatos).
Mas a frase de que log z nunca produz contato é ampla demais:

    [R(partial_i partial_j partial_k partial_l log z)
       -partial_i partial_j partial_k partial_l R(log z)]/C_E
      =-(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)delta/6.

Em particular, quatro derivadas na direção0 dão -delta/2. Duas
derivadas de log z, isoladamente, não dão esse contato.

Também não falta a tipagem da densidade externa T mencionada em J4:
a nota covariant_source_density/DERIVACAO.md já especifica

    T=sqrt(g) P t P^t,
    P=I+K(zI-xx^t)/6, sqrt(g)=1-Kz/2,
    T1=-(z t+xx^t t+t xx^t)/6.

O parecer usa o sinal oposto do transporte e conclui ausência de uma
definição já existente. A identidade da densidade foi reconferida.
As demais proposições do parecer, em especial as fórmulas genéricas de
comutadores de Laplacianos, não receberam aprovação global nesta auditoria.

## A derivada do cutoff na fonte efetivamente calculada

Use o coeficiente plano da fonte de dois vértices já construído:

    C_ab,r=-12 delta_ab Xr/z4
            -30(delta_ar Xb+delta_br Xa)/z4+96 Xa Xb Xr/z5.

Essa fonte é mais singular que uma única linha U/z. Não aplicar a ela
uma tabela de uma linha sem conservar multiplicadores e graus.

Para um operador de segunda ordem E=A^{ij}partial_i partial_j+
termos de ordem inferior, e R que comuta com multiplicação por funções
suaves na prescrição fixada, a regra do produto prova

    C_E(chi C)=chi C_E(C)
              +2 A^{ij}(partial_i chi) C_partial_j(C),

quando A é simetrizado nos dois índices de derivada. Para E plano as
parcelas inferiores são zero. A segunda derivada de chi multiplica C,
e cancela no comutador porque R comuta com essa multiplicação.
Essa ausência de Hessiana de chi é específica deste comutador: o
operador E(chi R(C)) separado possui, sim, segundas derivadas de chi.

O script calcula a parcela do primeiro jato de chi por duas rotas:
(1) diferencia o regulador z^a, substituindo D_i por D_i+lambda b_i,
e extrai o resíduo; (2) aplica a regra acima com os contatos de primeira
derivada e multiplica deltas pela regra X_i partial^nu delta.
O sinal observado é R E-E R, dividido pelo escalar C_E=-4pi².

Para r=0, b=e0, componente ab=11, o resultado é

    (-5q0^4-2q0²q1²+8q0²q2²+8q0²q3²+3q1^4
       +16q1²q2²+16q1²q3²+13q2^4+26q2²q3²+13q3^4)/128.

q significa derivada de delta. Não é um momento de Fourier com um i
omitido. Na direção q=e0 o coeficiente é -5/128: ignorar o primeiro
jato do cutoff perde uma contribuição local não nula. O fator chi
externo deve continuar multiplicando a distribuição, e não ser
substituído por chi(0) sem a respectiva regra de multiplicação.

## Evidência e limite

674 controles exatos, CPU2.28125s, rc0. Incluem os contatos de todas
as componentes até as ordens indicadas, a expansão da densidade e
as duas extrações do primeiro jato para b=e0,e1 e r=0. São28 componentes
não nulas do novo contato. A fórmula geral decorre da regra do produto;
os controles não pretendem substituir a prova pelo número de casos.

Este é o estágio em X da fonte plana depois da redução fora da diagonal
em Y. Ainda não inclui o cutoff em Y, a localização completa dos dois
vértices, sua corrente EH, primeira curvatura ou todas as aridades.
Não substituir a soma completa por esta parcela. Ela fornece um termo
necessário para a montagem e uma correção do critério de comparação.
Nenhuma mudança de prescrição, original, kernel ou gate.
