# Errata documental ao aceite537 — NC02 terminal

**O aceite estático537 deixou passar uma dependência de runtime não coberta e uma lacuna no relato de falha.** [REAL — fonte e inventário; OPEN — identidade dinâmica] A unidade c8909840-5b14-4bf5-bc2b-dfc71dbdbcaa continua terminal, com zero resultados aritméticos aceitos. Não foi repetida, corrigida ou reaberta.

## Achados

**[P2, NC02-DIAG-01] Dependência estática não confrontada com os pins.** `worker_controls.py:6` importa `ctypes`. A fonte instalada e pinada `C:/Python314/Lib/ctypes/__init__.py:5` importa `sysconfig` incondicionalmente. O arquivo local `C:/Python314/Lib/sysconfig/__init__.py` existe, mas não consta em EXECUTION_INPUTS.json nem RUNTIME_PINS.json; nenhum caminho com sysconfig aparece nesses inventários. O recibo desta revisão fixa os bytes e o hash dessa fonte por leitura.

Isso demonstra uma lacuna de fechamento da dependência estática. A resolução usual pelo importador de arquivos reconhece diretórios com `__init__.py` (`importlib/_bootstrap_external.py:1376–1387`). Se a origem desse pacote for o arquivo local absoluto, a regra `origin in allowed` da linha167 o recusará. **O recibo consumido não mostra o módulo que efetivamente disparou a falha; sysconfig é uma explicação sustentada pela cadeia estática, não uma identidade medida como causadora única.** Também não foi demonstrado que seja a única origem não admitida.

**[P2, NC02-DIAG-02] A recusa perde a evidência que permitiria diagnosticar a origem.** Nas linhas165–167, o worker constrói somente um conjunto de caminhos, perde a associação ao nome do módulo e emite `UNPINNED_IMPORTED_MODULE` sem registrar o conjunto diferencial. `loaded_module_origins` só entraria no report do caminho PASS (linha178). O handler192–195 conserva tipo/mensagem/audit_denied, mas não origens nem nomes. Assim o sistema recusa corretamente, porém seu recibo não distingue dependência omitida, caminho alternativo, alias, módulo frozen com `__file__` ou outra origem inesperada. A revisão537 deveria ter apontado essa falta de diagnóstico antes do consumo.

## O que a evidência realmente demonstra

O recibo terminal informa `FAILED_WORKER_OR_RECEIPT`, worker returncode1, RuntimeError `UNPINNED_IMPORTED_MODULE`, `audit_denied=[]` e ausência de retorno automático. O recibo externo de ROOT confirma exit1 do supervisor, 0,21472480008378625s até a observação após persistência e zero resultados aceitos. Os cinco pins de evidência desse recibo externo conferem; o worker continua byte a byte idêntico ao snapshot da revisão537.

A origem da mensagem no fonte é o pós-check de origens. Isso localiza a etapa de recusa, mas não preserva os valores aritméticos transitórios. Não promover a eventual passagem pelo loop anterior a PASS, mínimo certificado ou resultado parcial recuperado. O veredito aritmético permanece NOT_ESTABLISHED_BY_ACCEPTED_RUNTIME_RECEIPT.

`audit_denied=[]` é compatível com essa falha: os imports stdlib, incluindo ctypes, ocorrem antes de `install_audit` na linha143. A lista vazia não certifica que todas as origens já carregadas estavam pinadas. O mecanismo final permaneceu fail-closed, e não se propõe removê-lo para obter sucesso.

## -I, -S, nomes e evidência contrária

O argv preservado no recibo de identidade é o lançamento Windows com `-I -S -B -X utf8`; não há transporte Windows→Linux nesta falha. Isolar user-site/caminho inseguro e desabilitar o processamento de site não elimina imports transitivos da própria stdlib. A fonte `site.py:719–722` explica o efeito de `no_site` sobre sua extensão de sys.path; não estabelece que qualquer pacote aninhado da stdlib já esteja nos pins. Não foi iniciado outro Python para enumerar seus módulos ou reproduzir a falha.

A busca estática precisa resolver também aliases. Um contraexemplo concreto lido: `inspect.py:150` importa `collections.abc`, mas não existe `C:/Python314/Lib/collections/abc.py` neste recorte. `collections/__init__.py:29,32–33` associa esse nome ao módulo `_collections_abc`; sua fonte está pinada. Portanto ausência de um arquivo com o nome lexical do import não é, sozinha, uma lacuna. Esse candidato foi descartado documentalmente e não entra como módulo faltante.

A identificação dinâmica completa continua [OPEN], pois os recibos não gravaram `sys.modules`, `__spec__.origin`, loader ou o diferencial das origens. Nenhum desses dados foi reconstruído por suposição.

## Correção ao parecer anterior e orientação limitada

Preserva-se o parecer537 sem edição. Suas conferências de integridade dos536 arquivos, leitura das fórmulas, aliases de saída e semântica declarada dos limites continuam sendo o que mediram. Entretanto, integridade dos itens enumerados não demonstra completude da lista. A declaração de ausência de bloqueador e o aceite da cadeia de runtime ficam corrigidos por esta errata: a importação transitiva `ctypes → sysconfig` já era visível nas fontes lidas e não foi confrontada com os pins. O texto anterior distinguia estática de execução, mas essa ressalva não elimina a omissão concreta da revisão.

Para uma implementação futura da F9, incorporar no próprio preparo o confronto de dependências diretas/transitivas e aliases com os arquivos admitidos. Se a fonte sysconfig for a dependência escolhida, seu arquivo e a cadeia realmente necessária devem ter identidade/hash explícitos; não liberar genericamente toda a árvore stdlib. No worker futuro, conservar nome/origem/tipo de loader e a diferença inadmitida ANTES de lançar a recusa, em relato limitado e ligado ao request/pins. Classificar built-in/frozen/arquivo sem fingir que todas as categorias são equivalentes. Essas são orientações de implementação, não código corrigido ou autorização de nova unidade.

Não se cria controle artificial apenas para refazer c890. A inclusão em algum pacote futuro, eventual verificação e qualquer nova execução pertencem à decisão própria de ROOT. Não foram alterados pacote, CLAIM, autorização, memoria compartilhada, ledger, aritmética, solver ou dados. Este diagnóstico grava apenas sua pasta própria; ROOT recebe a errata para a integração que couber.
