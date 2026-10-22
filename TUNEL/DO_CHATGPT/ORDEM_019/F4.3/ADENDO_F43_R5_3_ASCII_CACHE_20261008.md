# F4.3 — R5.3 ao lado: número ASCII canônico e cache

[REAL — consulta antes de produzir] O Nós Vivo F4.3 aponta o V1 do ramo B, o controle C7 e as camadas R5/R5.1/R5.2. A auditoria c1 a47334e0 aprovou a R5.2 e localizou uma ressalva menor: a regex com \d aceita dígitos Unicode e zeros à esquerda. Esta camada conserva a função e os sete recibos de produção da R5.2; muda só a grafia do átomo de poder.

[REAL — regra executável] O número do token POWER usa apenas [0-9], com re.ASCII. A parte inteira é 0 ou começa em 1–9, sem zero à esquerda; a parte fracionária opcional usa P maiúsculo da casa ou ponto decimal, seguida de pelo menos um dígito ASCII. Assim POWER_0P2 e POWER_4.9 são aceitos, enquanto ٤P2, ４P2, 0P٢, 00P2, 04P9 e 00 são recusados. O poder do token NOT_FALSIFIED_UNDERPOWERED permanece < 5. O token oficial continua atômico, sem prefixo composto; n<10 continua emitindo o sufixo local INSUFFICIENT_SAMPLE. O novo gate pina por hash o veredito R5.3 e os artefatos R5.2/R5.1/R5 existentes.

[REAL — teste] f43_r5_3_selftest.py foi rodado com Python -B, sem dado observacional: 24 verificações sintéticas passaram, inclusive a grafia P válida, dígitos Unicode, zeros à esquerda, prefixo composto, amostra insuficiente e recusa do modo de produção sem recibos. Este teste não mede poder nem calibra as caudas.

[REAL — higiene] O diretório F4.3\__pycache__ continha exclusivamente dois arquivos .cpython-314.pyc gerados pelo interpretador, sem subdiretório ou reparse point. Os caminhos, bytes, datas e hashes foram registrados em CACHE_F43_R5_3_REMOVAL_20261008.json. O caminho absoluto foi resolvido dentro de F4.3 antes da remoção; depois, o diretório não existia. Os comandos de teste desta camada usam -B.

[OPEN] A campanha exata de injeções e o adaptador full IMR aguardam o levantamento do ADENDO 001. Poder não foi medido. O pedido ao operador permanece SUSPENSO. Nenhum dado observacional foi aberto, nenhuma mudança ocorreu na Bancada ou no gate.