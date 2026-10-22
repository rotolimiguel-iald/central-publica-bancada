[DERIVED — par ghost e combinação parcial; REAL — CAS; OPEN — Ward completo]
# A7.b — contato finito do par ghost na mesma referência
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:28:40.454028+00:00.

Aplicamos a mesma extensão R e os mesmos projetores harmônicos ao kernel
ghost DIRETO, com vértice não mínimo, dois bitensores e transposição do
segundo vértice na contração orientada. Não inferimos a amplitude de um
determinante mínimo ou do coeficiente de calor livre. Jatos e sinais de
integração por partes são os mesmos usados no par métrico.

PrimeiraK, base K[p²trAB,p²trA trB,pAp trB,pBp trA,pABp]:

    ['-1571/1728', '1291/2304', '-1681/3456', '-1681/3456', '199/192']

SegundaK, base K²[trAB,trA trB]:

    ['325/144', '-325/576']

Com os pesos existentes (-1/2 para o par métrico cru, +1 para este par
ghost direto), a combinação de DIFERENÇAS LOCAIS, ainda dividida por C, é:

    K1: ['-667/576', '6071/6912', '-1895/3456', '-1895/3456', '5/18']
    K2: ['-218/27', '109/54']

Os termos logarítmicos foram avaliados separadamente, não omitidos por
hipótese. Os coeficientes de troca das duas pernas são iguais nesta conta.
Para K1 foram escolhidos cinco pares por posto na ordem inversa à seleção
métrica; quatro pares NÃO utilizados no ajuste e um momento não axial
reproduziram os coeficientes. K2 usou dois pares e duas verificações novas.
São 7 verificações, rc0, CPU38.21875s.

A combinação é não nula. Não é Q2: faltam o contato da fonte com sua
Hessiana, o tadpole finito, W admissível e a contribuição Ward da própria
referência diferencial. Não foi escolhida uma subtração para cancelar o
resultado. Original um.py, kernel, gate e prescrição permanecem intactos.
