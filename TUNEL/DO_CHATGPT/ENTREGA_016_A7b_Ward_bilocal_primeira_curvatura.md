[DERIVED — identidade bilocal fora da diagonal até O(K), CAS exato; Q2 completa OPEN]

# Soma de laços e fonte na mesma orientação

Data: 2026-09-25T09:23:00.795789+00:00. Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

O cálculo passou a incluir todos os jatos h_X e D_Xh_X, a divergência
covariante em X e o termo de fonte Einstein calculado separadamente.
Na referência singular euclidiana 4D, com z=X² e X diferente de Y:

    B0 = (EC)0 = 0,
    B1_ab,r = 144 delta_ab Xr/z4
               +48(delta_ar Xb+delta_br Xa)/z4 -384 Xa Xb Xr/z5,
    (EC)1_ab,r = -B1_ab,r,
    B = -metrico/2 + ghost.

A junção verifica os 64 componentes nas duas ordens (128 identidades
racionais), sem ajuste de coeficiente. Três controles detectam omitir
D_Xh_X, retirar a fonte e inverter seu sinal. A divergência de frame foi
auditada por conversão independente para coordenadas (84 identidades).
Fonte: 128 verificações; reconstrução dos laços: 480 verificações.

**Alcance:** paga a identidade não coincidente deste truncamento. O
resíduo anterior com D_Xh=0 não testava a identidade forte completa.
Faltam contatos da extensão temporal, parte suave geral, ordem K²,
contribuições locais restantes e demais aridades para declarar Q2/WZ e
sua classe. A própria saída dos laços preserva o rótulo de candidato;
a auditoria e a soma posteriores estão em arquivos novos, sem apagar
aquele estado. Gate e originais intactos.

## Auditoria das contribuições Kimi

- Quártico: o vértice concorda exatamente com o existente em 12 exemplos
  densos. Dois autotestes originais falharam: momento usado na ação de
  Lie e métrica total entregue a uma função que esperava perturbação.
  Controles independentes corrigidos passam, inclusive 12 Ward com
  momento ghost não nulo. Foram 35 verificações; nenhum vértice foi
  alterado. O antigo gerador de momentos tornava o ghost zero em todos
  os exemplos. Um controle sqrt(det) antigo era float, registrado como
  tal, sem promovê-lo a identidade racional.
- Dicionário radial: 48 verificações locais, 16 contraexemplos aos
  sinais/fatores mistos e ao exemplo de derivar uma correção constante.
  A sugestão de acrescentar Kp0 a um símbolo homogêneo de quarta ordem
  não foi aceita sem escala adicional. A parte algébrica do operador de
  Lichnerowicz foi conferida; não é prova do matching bilocal inteiro.

## Orquestração e custo

Kimi referência harmônica, MiMo contatos angulares e DeepSeek adjunto
Einstein foram despachados e estão simultaneamente em execução segundo
o recibo da coordenação. Kimi primitiva curva terminou, ainda DECLARADO
até auditoria local; sua resposta foi preservada para o próximo passo.
Preservados os pedidos já existentes, memória comum e uma execução por
unidade. MiMo 4bdcaf7f e 88e54d74 terminaram IncompleteRead: sem resposta/uso medido,
custo desconhecido, não zero; nenhuma repetição. Kimi radial recebido
com 317.871 tokens de entrada e 40.169 de saída (cache 312.064 informado).

Total desta entrega: 903 verificações reportadas (contagens de
execução, não quantidade de teoremas), CPU 657.359375s. A tentativa antiga de
fonte foi encerrada só depois de a representação compacta equivalente
concluir; preserva 21 testes anteriores, rc-1 e limite inferior medido
de CPU 780,890625s, sem inventar duração final. Demonstração detalhada,
recibos e hashes em bilocal_bulk_closure_delivery/manifest.json.
Próximo ramo: extensão/contatos na prescrição fixada, dentro de A7.b.
