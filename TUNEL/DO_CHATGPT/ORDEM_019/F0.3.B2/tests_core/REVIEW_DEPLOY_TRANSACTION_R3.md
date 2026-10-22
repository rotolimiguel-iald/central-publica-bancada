# Complemento R3 — ensaio transacional em fixture

[REAL — execução sintética delimitada] Atendendo ao pedido posterior da coordenação, o fluxo completo do deploy foi ensaiado sem modificar seu script original. A mesma fonte foi parseada em AST; somente BASE, CANDIDATE e TARGET foram redirecionados para uma fixture sob tests_core/temp. O primeiro cenário introduziu uma falha controlada no os.replace do segundo arquivo. Nenhum caminho de escrita da Bancada instalada permaneceu no AST executado.

Resultados: 2/2 testes aprovados. Na falha, o primeiro arquivo foi restaurado byte a byte, o segundo permaneceu intacto, o manifesto não foi alterado, os backups correspondiam aos bytes antigos, o temporário foi limpo e o recibo listou a restauração. No cenário bem sucedido, três arquivos foram instalados e os três backups corresponderam byte a byte ao estado anterior. O script original permaneceu com o mesmo SHA256 antes/depois. Os cenários usam fixtures separadas; não foi testada uma repetição no mesmo segundo sobre a fixture da falha.

A preparação usou o modo padrão sem --apply, pois o script não oferece opção --prepare. --apply foi executado somente contra os destinos fictícios redirecionados, por autorização específica da coordenação; nenhum builder foi executado. Os logs guardam comandos, início/fim e códigos de saída. A exceção intencional do primeiro cenário é o resultado esperado; o teste passou ao comprovar recuperação.

Este complemento atualiza a ressalva temporal da REVIEW_DEPLOY_MANIFEST_R2: o rollback completo agora foi ensaiado nesse cenário sintético. Não equivale a comprovação de toda falha possível de disco, parada de serviço, restauração em produção ou implantação concluída. Nenhum dado observado, kernel, um.py original, memória ou gate foi alterado.

Resultado: DEPLOY_TRANSACTION_FIXTURE_RESULT.json, SHA256 f725c3c444a345bc3e595f5fb81ba26052bfb46da7595508736288c570ab26d9. Fixtures e logs preservados no caminho registrado nesse resultado.
