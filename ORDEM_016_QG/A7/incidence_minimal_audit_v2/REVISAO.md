[REAL — revisão local do inventário Kimi; OPEN — inventário corrigido e inserções Ward]
# A7.b — não usar as contagens antes de corrigir a identificação dos vértices
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T01:18:51.614205+00:00.
Resposta one_loop_incidence lida inteira, código extraído sem alterações e
inspecionado antes de executar. Só importações itertools/collections; nenhum
acesso de rede/arquivo pelo código recebido. Executado Emax1 e controles pequenos,
sem chamar main/controles, que repetiriam a enumeração completa E6.

1. **Defeito reproduzido:** certificado_e_aut devolve somente a matriz de
adjacência; atrib_vistos usa esse valor sem as classes. No vértice único
trilinear com tadpole, METRIC_ORD e GHOST_ORD colidem. inventario(emax=1)
devolve só METRIC_ORD, embora atribuicoes_linhas([CB,C,H],((1,),)) produza
uma linha ghost de tadpole, deixando um H externo. Portanto a contagem
não cobre sequer esse setor básico e não pode ser usada como lista completa.

2. **Controle ineficaz:** permitir_antifield_em_linha não cria opções de
contração novas em _opcoes_linha. As duas enumerações E1 têm a mesma saída.
O negativo anunciado como aumento por propagação de antifield não testa
essa adulteração. O validador também aceita zero linhas ou ('INVALID',7,9)
para uma matriz de tadpole e gh=99. As duas contagens C/CB são a mesma
expressão; a compreensão `for s in ()` nunca executa. Esses checks não
validam incidências/slots/ghost. Um validador real deve reconstruir esses dados.

3. **Escopo a completar:** todos os vértices listados têm ghost total zero,
e cada linha C-CB remove ghost zero. Logo o inventário atual só pode produzir
gh externo zero. A inserção Ward de ghost1 não surge só de marcar a saída;
precisa entrar como classe própria, com os contatos/cutoffs correspondentes.
A fonte reconhece essas classes como pendentes. Isso não é prova de anomalia
zero nem objeção à identidade combinatória de valências já derivada.

4. **Crítica não confirmada:** comparei o filtro de monotonia de opções com
backtracking sem filtro, em2187casos: dois vértices, contadores H/C/CB de0a2,
1a3arestas paralelas. Saídas idênticas. Aqui M, Gida e Gvolta consomem recursos
disjuntos; a mudança de índice não basta para demonstrar perda de casos.
Não transportamos a crítica estática da coordenação como resultado medido.
Isso não audita automaticamente extensões futuras com outros propagadores.

A observação textual de que duas linhas ghost exigem dois C num lado e dois
CB no outro só cobre orientações iguais. Duas orientações opostas podem ligar
dois vértices cbar-c-h. A conclusão para a família(3,7) continua: o vértice7
não tem classe ghost neste catálogo; a razão deve ser essa tipagem específica.
Automorfismos da matriz não bastam para pesos do grafo com classes, tipos e
orientações; os pesos corretamente permanecem pendentes no próprio parecer.

Execução v2 rc0,CPU0.03125s; quatro defeitos/limites acima e comparação
2187casos. V1 percorreu os checks, mas falhou na exportação JSON por chave tupla;
v2 só serializa esses contadores como registros. Arquivos e traceback preservados.
Próximo passo: certificado incluindo decoração completa, validador independente
de slots/arestas e categoria Ward explícita, antes da enumeração maior.
Uso recebido317969entrada/37719saída/355688total; custo não informado, não zero.
Nenhuma chamada extra, alteração de original ou gate.
