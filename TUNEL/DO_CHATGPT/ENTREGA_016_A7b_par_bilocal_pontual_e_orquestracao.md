[DERIVED — cálculo pontual dos candidatos; verificações exatas locais; Q2 permanece OPEN]

# Par bilocal e ampliação da orquestração

Data: 2026-09-25T08:47:02.791921+00:00. Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

## Cálculo realizado

Foram inseridos os vértices existentes dos setores fantasma e métrico na
divergência em Y, com diferenciação antes de Y=0. Ponto X=(1,0,0,0),
h_X=e11 no frame ortonormal, Dh_X=0. Os resultados guardam as normalizações
dos motores; constantes comuns dos propagadores estão removidas.

| componente longitudinal, sem log | K0 | K1 |
|---|---:|---:|
| fantasma | 128 | 256 |
| métrico bruto | 128 | 144 |
| combinação −métrico/2+fantasma | 64 | 184 |

Os três componentes transversais e os coeficientes logarítmicos se anulam
neste ponto/jato. O valor não nulo acima NÃO é uma anomalia calculada:
faltam fonte Einstein na mesma orientação, jatos Dh_X, extensão/contatos,
parte suave, tadpoles e aridades restantes. A revisão independente das
conversões de frame está encomendada; os testes não substituem essa revisão.

Ghost: 1731 verificações, CPU
93.109375s, rc0. Métrico v2:
10023 verificações, CPU
493.9375s, rc0.
O v1 também terminou rc0, mas criou floats ao dividir por 16 uma soma vazia.
Seu valor curvo 143.99999999999986 não foi promovido a igualdade exata.
V2 usa Fraction antes da divisão e exige tipos racionais nas saídas.
O v1 e sua errata permanecem preservados, com seus hashes.

## Recorrência derivada

A transvecção k_i^a=delta_i^a−K(X²delta_i^a−XaXi)/3 satisfaz Killing.
As derivações de Lie simultâneas anulam os kernels bilocais truncados:
1.152 verificações simbólicas, dois controles negativos. Delas se obtém,
para os índices inferiores b no extremo Y,

    DY_i G|0 = −LX_i G|0
    DY_j DY_i G|0 = LX_i LX_j G|0
      + K sum_slots(delta_jb G[b→i] − delta_ib G[b→j])|0 + O(K²).

A segunda fórmula foi conferida em 200 identidades de componentes,
simbólicas em X, e dois controles negativos. A demonstração escrita está
em transvection_endpoint_recurrence/DERIVACAO.md. Seu uso em bitensores
com índices derivativos adicionais ainda exige incluir esses índices.

## Orquestração

Duas novas unidades Kimi e uma MiMo aceitas em staging, com request_id,
hashes e previews no catálogo orchestration_bilocal_completion_v2. O
catálogo sem v2 está excluído: sua segunda prévia ultrapassou 24.000
caracteres antes de qualquer submissão. O primeiro pedido manteve seu ID.

A coordenação implantou até três execuções entre fornecedores distintos,
uma por Kimi/MiMo/DeepSeek, mantendo fila única e cinco não terminais.
Recibo registra Kimi e MiMo running simultaneamente; não equivale a
conclusão. Testes relatados: 34 focados e 52 de regressão; quatro testes
web não rodaram por falta de Flask naquele Python. Não houve interrupção
da chamada antiga, duplicação de pedido ou novo heartbeat.

Total local desta entrega: 13106 verificações reportadas (não teoremas
independentes), CPU 596.828125s; incluindo o v1 numérico, CPU 1087.8125s.
Nenhum original, kernel ou gate alterado. Próximo ramo: mesma identidade
bilocal com fonte e domínio de jatos completo, dentro do timebox A7.b.
