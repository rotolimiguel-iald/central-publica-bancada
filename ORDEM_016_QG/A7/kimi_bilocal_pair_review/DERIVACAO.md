[REAL — auditoria exata; DERIVED — correção de tipagem e de alcance distribucional]

## O que foi recebido e o que foi efetivamente entregue

O parecer Kimi bilocal_pair_endpoint_ward foi lido integralmente. A própria
resposta declara não ter expandido a contração métrica da Hessiana do par;
entrega regras de derivada e um exemplo com uma única linha ghost. Portanto
não deve ser contado como cálculo da Ward completa do par solicitado.

As regras de derivada dos coeficientes P1 e distance1 estão certas. O CAS
confere todas as componentes de (partial_X+partial_Y)P1 e as quatro de
distance1, sem ancorar primeiro. Não foi refeita a identidade de transvecção
já registrada: ela continua a fonte para uma mudança geométrica de centro,
que inclui a transformação de índices, e não apenas derivadas de coordenadas.

## A contração do exemplo usa o índice da outra extremidade

A tipagem explícita de bilocal_covariant_jet_engine.py é:

    ghost(o,a,b) = G^a_b'(X,Y),
    a: contravariante em X; b': covariante em Y.

A divergência em Y contrai o índice b' com a derivada elevada em Y:
g_Y^(b'c') nabla^Y_c' G^a_b'. Na âncora Y=0, gY=delta e GammaY=0.
O parecer calcula, em vez disso, sum_a partial_Ya G^a_b'. Isso reproduz
uma soma de componentes, mas contrai um índice de X com uma derivada de Y
sem especificar transporte entre os espaços tangentes. Não é essa divergência.

Para o coeficiente de primeira ordem em K, a conta literal do parecer é

    sum_a partial_Ya G1^a_b'|0 = X_b/z,
    -sum_a partial_Xa G1^a_b'|0 = 3X_b/z.

Esses números foram reproduzidos; a aritmética dessa soma não é o erro.
A contração no índice Y tipado, usando o motor covariante existente, dá

    nabla_Y^b' G1^a_b'|0 = 4X^a/z,
    -sum_b partial_Xb G1^a_b'|0 = 3X^a/z.

Logo o defeito deste comparador ingênuo é +X^a/z, e não -2X^a/z.
O segundo termo acima é expressamente um comparador de derivadas parciais;
não foi anunciado como uma divergência geométrica em X. Uma identificação
geométrica entre extremidades exige a transvecção/ação de fibra já derivada.

Algebricamente, sum_b partial_Yb P1_ab=(Y_a+3X_a)/2. Na âncora, a derivada
do termo -5delta_ab log(z)/4 acrescenta5X_a/(2z); os termos restantes se
anulam nessa contração. Resulta4X_a/z. A conta é até primeira K e fora
da diagonal. Não é um coeficiente de anomalia quântica.

## Uma linha integrável não controla o contato do par

É correto que a primeira derivada de1/z em4D não tem o contato de extensão
discutido aqui. Isso não se estende à primeira derivada de um produto de
duas linhas, que contém1/z². Na MESMA prescrição já fixada,

    R(f)=FP_a[(1-a)mu^(2a)z^a f],

o motor e a expansão de Laurent independente dão

    [R(partial_i z^-2)-partial_i R(z^-2)]/C_E
      = -(1/8) partial_i delta,

onde o símbolo de partial_i delta é q_i no JSON. A derivada radial
produz coeficiente2(a-2) X_i z^(a-3). O resíduo de X_i z^(a-3), dividido
por C_E, é q_i/16; o comutador recebe -2vezes esse resíduo. Assim o
contato acima já está presente com UMA derivada. Não é preciso extrapolar
a tabela de contatos de1/z para justificá-lo.

Portanto a seção de contatos do parecer é utilizável apenas no núcleo
que efetivamente calcula. Ela não fecha o passo de extensão da Hessiana
bilocal, cujo produto é mais singular. A conta dos contatos de um par
continua sendo a dos motores de extensão já existentes.

## Evidência e consequência

Foram104 verificações exatas, CPU0.578125s, rc0: regras de coeficientes,
tipagem das duas somas, limite plano, contato de1/z² em todas as direções
e conferência independente pela extração de Laurent. Sem alteração dos
motores, sem repetir a chamada ao modelo e sem promover o parecer ao cânone.
O aviso qualitativo de que -partial_X não substitui partial_Y em curvatura
permanece válido. O coeficiente e o alcance do exemplo foram corrigidos.

A Ward não coincidente do par até primeira K já tem verificação própria
em bilocal_bulk_ward_closure; este parecer tardio não a substitui nem
fornece a extensão completa que ainda falta. A contribuição do cutoff
e as extensões localizadas continuam sob auditoria. Q2 integral OPEN.
