# P2 — consolidação Lean

[REAL] 157 unidades ativas com rc=0, incluindo o import conjunto. 2291 nomes auditados na elaboração (inclui tipos, campos e auxiliares importados; não é contagem de teoremas novos).

Todos os axiomas próprios são subconjunto do trio; nenhuma declaração axiomática nova. A lista por declaração está no JSON. A cópia de fontes v371 foi conferida pelo manifesto; os builds canônicos foram copiados, não recompilados nesta rodada. Compilador limitado a 12 GiB; isso não apaga recusas históricas sob 8 GiB.

212 colisões explícitas nas fontes originais foram listadas, com as adaptações; zero colisões não resolvidas entre declarações próprias. Repetições dos auxiliares importados .eq_N estão listadas e excluídas da contagem de novidades. Módulos de fonte sem declarações no censo e a limitação lexical estão em P2_COLISOES.json.

As falhas iniciais e os controles negativos estão separados dos imports de produção. Não mover gate pela soma de rc.
