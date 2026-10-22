[DERIVED — símbolo logarítmico local; REAL — controles CAS; OPEN — Q2 completa]
# A7.b — operador ordenado K² e controle ghost direto
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T05:02:56.071103+00:00.

**Ordenamento explícito.** A expansão de Taylor covariante atua em A
ou em nabla_i A, conforme o vértice. Se a perna B carrega nabla_j,
transfere-se por partes com sinal− e aplica-se nabla_j a TODO o jato,
inclusive seus índices de derivada. Não se troca esse resultado por
derivadas totalmente simétricas antes de avaliar os comutadores.

O motor novo usa o coframe e=I−KN/6+K²zN/120, N=zI−xx, e a conexão
do espaço-forma até K². São20759 controles: comparação de K0/K1 com
a construção anterior, anulação dos Taylor totalmente simétricos K²,
paralelismo da métrica e comutador de curvatura.388 jatos K² não nulos
foram observados nas duas polarizações não escalares testadas.

Como controle anterior à nova ordem, a contração direta reproduziu
a bolha primeiraK nos pares (01,01):22/9 e (00,11):−4.
Esses dois probes não substituem a auditoria de100 pares anterior.

**Resultado K² integrado:** na base[tr(AB),tr(A)tr(B)] e após retirar
hbar*A0*K², com A0=1/(8pi²), a construção fornece

| setor | coeficientes |
|---|---|
| bolha métrica bruta | ['44', '4'] |
| métrica:−1/2 bolha + tadpole | ['-10', '-2'] |
| ghost | ['25/6', '-25/24'] |
| total | ['-35/6', '-73/24'] |

Os dois coeficientes foram determinados por (01,01) e (00,11).
(00,00) e (11,00) ficaram como controles posteriores e concordaram;
o coeficiente explícito log(z) foi zero nos quatro casos. A estrutura
de dois invariantes decorre da covariância O(4) da construção no ponto,
não de uma reivindicação de varredura numérica de todas as fibras.

O perfil radial anterior era[141,−81/4], ANTES dos adjuntos.
A diferença até o operador integrado é[−97,97/4]. No setor A=B=g
ela anula: a métrica é paralela. A soma nova total nessa direção é−72.
Não apagar o perfil anterior nem apresentá-lo como resultado integrado.

**Ghost sem fatorar o determinante.** Foi calculada a bolha diretamente
do vértice −(nabla_mu barc_nu) vezes a variação de gauge de h com
subtração do traço. A contração dirigida usa o transposto do segundo
vértice; não é a contração de dois vértices métricos simétricos.
O vértice coincide com o Q1 polinomial já existente em160 componentes;
reciprocidade dos Green e não-simetria do vértice completam1361 controles.

Seis pares reproduziram a referência plana. Na primeiraK, cinco
invariantes e um sexto par de controle deram exatamente

    [41/36,−7/3,26/9,26/9,−35/6],

iguais à redução do determinante anterior. As diferenças são todas0;
log(z) também0. Portanto essa fatoração NÃO explica, neste recorte,
o resíduo Ward primeiraK. Essa hipótese foi testada e não sustentada;
o resíduo continua sem alteração. Não houve ajuste para zerá-lo.

**MiMo:** recuperado o mesmo job70db6729-942c-4435-92e6-482d3d842134,
execb592a019-d0ce-4412-b4b4-f27242cedb4f, sem nova chamada. O parecer
é favorável a−571K²/15 no calor livre do fundo fixo e permanece
DECLARADO (revisão textual). Não é Hessiana nem cancelamento Ward.
Correções de justificativa: [E,A]=0 isoladamente não elimina todos
os produtos cruzados; precisam-se ordem em x, paralelismo e traços da
representação concreta. A(0)=0 também não elimina suas derivadas.
O fator(4pi)^−2 e o sinal da integral que define logdet são separados.
Os controles locais anteriores sustentam o valor com esse escopo.

Neste pacote:22128 asserções exatas, mais2 comparações métricas
e6+6 comparações ghost documentadas; CPU399.609375s; cinco execuções rc0.
O manifesto agrega as fontes e logs sem sobrescrever predecessores.

**Ainda aberto:** Ward com contatos finitos, cutoff, estado e a
hierarquia temporal especificada; Wess–Zumino/cohomologia completos.
A conta logarítmica não substitui essa aceitação. Segue a verificação
das ordens de Ward restantes e dos contatos. Nenhum gate/kernel/original
alterado, nenhum resultado repassado aos revisores independentes em fila.
