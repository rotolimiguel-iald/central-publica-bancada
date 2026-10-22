[DERIVED — primeira ordem em K, fora da diagonal; verificação CAS separada]

# Recorrência entre os dois extremos por transvecções

O domínio é o espaço-forma auxiliar euclidiano de dimensão quatro, na mesma
carta de coordenadas normais. K é a curvatura, não o gerador modular. Os
resultados seguintes são identidades para os propagadores truncados nessa
ordem. Não incluem extensão de distribuições, estado interagente ou Q2.

Escreva

    g_ab(X) = delta_ab - K (X² delta_ab - Xa Xb)/3 + O(K²),
    k_i^a(X) = delta_i^a - K (X² delta_i^a - Xa Xi)/3 + O(K²).

A equação de Killing segue diretamente de

    partial_i g1_ab + partial_a k1_i,b + partial_b k1_i,a = 0.

Além disso k_i(0)=e_i e partial k_i(0)=0. Para o bitensor G que é natural
sob a ação simultânea das isometrias, a identidade usada é

    (L_i^X + L_i^Y) G = 0.

L é a derivada de Lie tensorial: cada índice inferior contribui com
`+partial_b k^c G[...,c,...]`; cada índice superior com o sinal negativo
e a posição transposta. O teste `transvection_bilocal_identity_check.py`
conferiu a identidade nas quatro direções, para todas as componentes dos
propagadores ghost e métrico explícitos, sem escolher valor de X ou Y.
Isso verifica a identidade efetivamente usada para esses kernels; não
pressupõe que qualquer escolha adicional de parte suave seja invariante.

## Primeira derivada

Todos os índices Y dos kernels aqui usados são inferiores. Em Y=0,
L_i^Y G = partial_Yi G, porque partial k_i(0)=0. Logo

    partial_Yi G|0 = - L_i^X G|0.

As conexões em Y=0 também se anulam, portanto a primeira derivada parcial
coincide aí com a covariante. A derivada X é uma derivada de Lie completa;
substituí-la apenas por partial_Xi perde os termos de curvatura e de fibra.

## Segunda derivada

Diferencie a identidade de Lie em Y_j ANTES de ancorar. O coeficiente
k_i(Y) tem primeira derivada nula na origem, mas a ação sobre os índices
inferiores tem segunda derivada não nula. Assim,

    partial_Yj partial_Yi G|0
      = L_i^X L_j^X G|0
        - sum_slots (partial_j partial_b k_i^c)(0) G[b -> c]|0.

A composição L_i^X L_j^X tem a ordem indicada: os rótulos dos campos de
Killing são fixos. Para converter em derivadas covariantes, subtraia ainda
`sum_slots (partial_j Gamma^c_ib)(0) G[b -> c]`. A conexão sobre o índice
da primeira derivada é zero em Y=0. As duas contribuições somam

    partial_j partial_b k_i^c + partial_j Gamma^c_ib
      = K (-delta_jb delta_ic + delta_jc delta_ib).

Portanto, para cada índice inferior b no extremo Y,

    D_Yj D_Yi G|0
      = L_i^X L_j^X G|0
        + K sum_slots (delta_jb G[b -> i] - delta_ib G[b -> j])|0
        + O(K²).

O termo final usa G de ordem zero quando se trabalha até primeira K.
Índices derivativos adicionais em Y também são índices inferiores e
precisam entrar na soma se esta fórmula for aplicada a outro bitensor,
como D_Y G. A extensão a esses bitensores exige conservar suas ações
de Lie; não foi executada pelo verificador de componentes desta entrega.

## Conferências e limites

`transvection_endpoint_recurrence_check.py` verifica as primeiras e segundas
derivadas, nas quatro direções, em cinco componentes de fibra, como funções
simbólicas de X, nas ordens K0 e K1: 200 igualdades. Omitir o termo de
curvatura produz controles não nulos ±1/5 para X=(1,2,0,0).

As 1.152 verificações da identidade de Killing/Lie e as 200 verificações
da recorrência têm escopos diferentes. Não são 1.352 teoremas independentes.
Esta recorrência pode reduzir o custo de diferenciação e conferir os
motores bilocais. Não autoriza trocar a prescrição R, ignorar contatos,
declarar uma anomalia nula ou mover o gate.
