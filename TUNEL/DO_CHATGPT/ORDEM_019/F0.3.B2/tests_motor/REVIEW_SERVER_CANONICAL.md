# F0.3.B2 — revisão independente de canonical.py e um_bancada.py

Autor: nu2_theory_sources, sem edição dos dois arquivos revisados. Escopo: identidade, recusa e atividade; somente sondas sintéticas em diretório temporário, sem porta HTTP, Motor real ou dado observado. Os hashes desta fotografia estão em REVIEW_SERVER_CANONICAL_PROBES.json; alterações posteriores da coordenação requerem releitura das respectivas linhas.

## Achados materiais reproduzidos

1. **Atividade ociosa falsa durante carga** — um_bancada.py:124–130 enumera só ev/gw.tarefas. Com motor não pronto, GW carregando e lago carregando, devolveu idle=true. Tarefas pronta/falhou são corretamente terminais e rodando bloqueia idle. Ajustar/comparar/avaliar síncronos também não deixam entrada nesse inventário [REAL — leitura do fluxo, sem executar ajuste]. Antes de usar o endpoint como condição para implantação/reinício, contar requisições ativas, cargas e inicialização sob lock; recarga sem transação não pode confiar só no retrato ocioso.
2. **Escape da pasta UI por prefixo textual** — :205–211 usa startswith(UI). A chamada sintética ../ui_neighbor/probe.txt devolveu HTTP 200 com os bytes da pasta irmã. Resolver caminho e conferir pertinência por Path.relative_to/is_relative_to ou commonpath, inclusive junction/symlink; não apenas prefixo de string.
3. **Coerção HTTP desfaz validação de tipos do motor** — :347–349 converte opcoes falsa para {} e curvas para bool. POST com curvas='false' e opcoes=[] chegou ao avaliador como curvas=True e opcoes={}, HTTP 200 no receptor sintético. Encaminhar tipos originais à validação ou validá-los antes; ausência é diferente de tipo inválido. Estender o mesmo cuidado a bool/int em lago/GW.
4. **Content-Length inválido encerra fluxo sem erro estruturado** — :293 fica antes do try. O texto not-an-integer lançou ValueError, sem send_response. Recusar cabeçalhos inválidos, corpo incompleto e tamanhos fora do limite com resposta tipada.

## Limites reproduzidos da interface canônica

5. **source_bytes não confere geração do manifesto** — canonical.py:101–108 valida bytes contra o registry em RAM, mas não faz a checagem de imutabilidade :62–63. Após alterar o manifesto, check recusou e source_bytes aceitou a mesma fonte pinada. Isso NÃO demonstrou bypass HTTP (as rotas têm guarda antes/depois); demonstra que o leitor de fonte isolado tem contrato mais fraco que require_current. Verificar ao menos hash corrente do manifesto e mesma geração antes de devolver o pin, ou declarar a obrigação de guarda em toda interface consumidora.
6. **Manifesto com code=[] é aceito** — :33 e :80–81 não exigem conjunto mínimo de módulos do instrumento. Na sonda, com script/selo corretos, code=[] passou. Não é adulteração do manifesto real: um manifesto novo é raiz de confiança da implantação. Exigir cobertura dos módulos mandatórios na geração/validação para evitar um pin omitido ser invisível. O mesmo vale para fontes mandatórias de contratos habilitados; read_checked já recusa uma fonte não listada quando usada.

## Controles que passaram

Importar um_bancada deixa B=None e não inicia Motor. A raiz padrão de get_registry (:113–119) é a pasta da Bancada, consistente com require_current(root=RAIZ). Mudança de um byte no código listado e mudança de manifesto foram recusadas. Nenhuma nova alegação física ou significância resulta destas sondas.

## Evidências

- review_server_canonical.py: executor das sondas.
- REVIEW_SERVER_CANONICAL_PROBES.json: pinos, respostas e recusas observadas; SHA256 9c73d1b99b4b72fae0e8388ef8322c670ffafff2e049769fa17f31e18dd9aac1.

A coordenação recebeu todos os achados antes de concluir o manifesto. Nenhuma edição de canonical.py, um_bancada.py, memória, quadro ou Bancada instalada foi feita por esta revisão.
