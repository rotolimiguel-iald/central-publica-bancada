[DERIVED — curvatura das fibras; REAL — CAS exato; OPEN — coeficiente curvo interagente]
# A7.b — o que as massas escalares não representam

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`; UTC 2026-09-24T22:39:01.274556+00:00.

Modelo087, curvatura seccional K, d=4. Aqui K não é o gerador modular nem κ,
o acoplamento. No cálculo algébrico tangente euclidiano fixamos
R^rho_sigma_mu_nu=K(delta^rho_mu delta_sigma_nu-delta^rho_nu delta_sigma_mu).
A matriz Ω_mu_nu é antissimétrica na fibra vetorial; na fibra simétrica age
por ΩH+HΩ^T. A projeção simétrica no tensor de dimensão16 permite conferir,
por outra representação, o traço obtido na base simétrica de dimensão10.

Incluindo a soma sobre pares ORDENADOS de índices μ,ν:

| fibra | posto | tr Ω_mu_nu Ω^mu_nu |
|---|---:|---:|
| covetores/ghost |4| -24K² |
| tensores simétricos |10| -144K² |
| tensores antissimétricos (controle) |6| -48K² |

O índice da representação simétrica é d+2=6 vezes o vetorial; o da exterior
é d-2=2. A soma das duas dá o tensor inteiro. O vetor de traço da métrica é
anulado por Ω; a parte de traço não acrescenta curvatura de conexão escalar.
Os seis geradores preservam a forma de fibra e comutam com E do modelo.

Para os endomorfismos definidos em P=box+E_m e Q=box+E_g da entrega anterior,
E_m=-2K id+2K g tr e E_g=3K id:

    tr E_m=-12K, tr E_m²=72K²;
    tr E_g=12K,  tr E_g²=36K².

Esses E são os das fontes, NÃO uma escolha implícita do sinal E de uma fórmula
de kernel de calor após Wick. Esse dicionário precisa acompanhar qualquer uso
de coeficientes de calor. A combinação algébrica com pesos de determinante
1/2 métrico -1 ghost dá tr Ω² ponderado=-48K²; ainda não é um coeficiente
logarítmico completo, porque faltam os outros invariantes e suas constantes.

Substituir a fibra métrica por dez escalares com massas efetivas produziria
Ω=0, perdendo -144K². O teste recusa essa substituição, a contagem16 em vez10,
e a falta do fator2 dos pares ordenados. Conferir E sozinho não confere um
propagador tensorial curvo nem a segunda variação da ação com gauge de fundo.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/connection_curvature_check.py; rc0,33checks,3negativos; wall
0.05959140002960339s,CPU 0.0625s. Plano, log e hashes no manifesto.
Não foi calculado a4 nem a autoenergia curva nem a anomalia ghost1/forma4.
Este é o próximo insumo exato do ramo A7.b, não conclusão do ramo ou do gate.
