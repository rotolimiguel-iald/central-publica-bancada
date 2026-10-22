# Revisão independente — snapshot orquestrador v389

**BLOCKED.** A integridade do snapshot preparado conferiu, mas este instalador não está apto à ativação. Há dois bloqueadores de concorrência: leitores podem atravessar a troca do índice e associar conteúdo novo a pins antigos; o marcador de tentativa não é adquirido exclusivamente.

A revisão foi local: bytes, JSON, AST e SQLite em modo read-only/immutable. Não executou prepare_snapshot.py, install_snapshot.py, um.py, ciência, provedores ou testes de corrida; não alterou fila, catálogo, código comum ou memória de produção. Não houve registro no mapa externo. O status BLOCKED e o hash exato do REVIEW_MANIFEST estão no recibo consumível pelo instalador, que portanto deve recusar esta revisão.

## ORCH389-01 — P1: troca index→manifest não fecha a corrida de leitura

install_snapshot.py:33 e47 observam a fila duas vezes, mas não a bloqueiam. As linhas51–54 substituem arquivos sequencialmente, com índice antes do manifesto.

canonical_memory.load:196–211 verifica snapshot e hash do índice e relê o manifesto. Isso rejeita corretamente um par estacionário incompatível. Entretanto canonical_memory.prepare chama load em252 e só abre a conexão SQLite nas linhas279–292, após load já ter retornado e liberado seu LOCK. O mapa de hashes usado nas referências é criado do manifesto anteriormente carregado (296–309).

Interleaving concreto: leitor termina load com a geração antiga válida; instalador substitui index.sqlite3; leitor abre o mesmo caminho e obtém trechos v389; as referências e a geração ainda são as do manifesto antigo. Não há revalidação final ligando a conexão consultada à identidade antes carregada. Portanto a alegação de fail-closed entre índice e manifesto não vale para todo leitor concorrente.

ROOT confirmou que não havia quiescência externa. Um novo worker pode iniciar após o polling; uma consulta de preview também pode ler sem existir tentativa de executor em curso. Dois snapshots da fila não constituem exclusão.

O sucessor deve separar raízes de leitura imutáveis por geração ou prover exclusão/detecção completa que também alcance previews. ROOT informou que prepara a primeira alternativa em pacote separado: leitores residentes manteriam sua raiz histórica, novos processos usariam uma raiz nova completa. Esta alternativa ainda não foi examinada nem aprovada neste parecer.

## ORCH389-02 — P2: no-repeat não é uma reserva exclusiva

install_snapshot.py:21 testa ausência de INSTALL_STARTED.json, mas só o escreve em48 por save_json. safe_files.py:27–28 chama replace_bytes; suas linhas13–23 aceitam arquivo existente, fazem backup e o substituem. Logo duas instâncias podem passar pelo teste inicial antes de qualquer marcador e ambas ultrapassar a suposta aquisição da tentativa.

A validação de snapshot ausente e os CAS por arquivo não são um lock de instalação. Reserva por criação exclusiva, com identidade persistente e recusa de nova aquisição, é o reparo mínimo deste ponto. Nenhuma nova tentativa deste candidato foi proposta ou executada.

## O que conferiu

Os22 membros do REVIEW_MANIFEST correspondem aos bytes lidos. O plano contém16 destinos:13 fontes científicas, um descritor de snapshot, índice e manifesto; são14 novos e2 substituições. Os destinos permaneciam nos baselines declarados na conferência final; nenhuma instalação foi observada/realizada por esta revisão.

As13 identidades científicas são exatamente as mesmas do catálogo histórico, excluindo seus2 PDFs como já faz o código comum. Seus hashes correspondem aos manifestos de estágio/instalação e ao SEALED_SNAPSHOT. Programa, resultado JSON e proof manifest correspondem aos três pins do selo v389; formal_source_hash coincide entre selo, proof e descritor. A geração foi recalculada da lista ordenada de nomes/hashes e coincide em todas as peças. Isso é ligação documental, não reprodução da ciência ou nova compilação formal.

O SQLite de estágio passou quick_check em leitura e contém20279 trechos distribuídos pelas13 fontes, sem nomes adicionais. Seu hash coincide com index_sha256 dos manifestos/descritor. A leitura não executou os textos indexados.

As três recuperações registradas em PREPARATION usam a geração nova e declaram cobertura parcial, sem alteração de pesos. São recibos do preparo, não chamadas externas repetidas por este revisor. O catálogo staged retém os campos históricos de v369 como referência de comparação; os pins atuais derivam dos bytes e aparecem nos manifestos novos. O catálogo histórico de produção permanece byte-idêntico e não é destino de instalação.

As duas peças de preparo/instalação e os auxiliares canonical_memory.py/safe_files.py têm AST válida. O pin do módulo comum e o do catálogo correspondem ao baseline. As restrições de pedidos antigos não são escritas por este instalador: o acesso à fila no código é SQLite mode=ro/query_only. Isso não prova exclusão de escritores concorrentes; apenas limita o que este código pretende escrever.

## CAS, rollback e limites

Antes de mutar, o instalador confere membros revistos, review PASS vinculada ao manifesto, decisão separada vinculada ao hash do review, auditoria científica por pin, destinos exatos, raízes resolvidas, symlinks, fontes, baselines e ordem índice→manifesto. safe_files conserva backup imediato de bytes, verifica temporário e readback e usa os.replace por arquivo.

A recuperação percorre os destinos escritos em ordem reversa e só restaura arquivos antigos quando o atual ainda coincide com o novo pretendido. Novas cópias ficam para auditoria; conflitos aparecem como unresolved; não há retry automático previsto. Essas são proteções úteis, mas não tornam a operação multi-arquivo transacional nem fecham os dois achados. Erro adicional durante rollback pode interromper a recuperação e exigir reconciliação manual; o marcador deve continuar impedindo nova tentativa, sem alegar rollback universal.

Depois da instalação, o receipt distinguiria geração local e necessidade de checagem em novo processo, sem prometer hot reload. Este parecer não permite produzir esse receipt como sucesso: status BLOCKED preservado. A auditoria científica v389 continua tarefa separada de ROOT/controller.

## Decisão

Integridade documental aceita no recorte descrito; ativação deste candidato bloqueada pelos achados ORCH389-01/02. Não houve mitigação presumida, alteração do candidato ou execução. Um sucessor separado deve receber seu próprio manifesto e revisão. O pacote anterior e este parecer permanecem preservados.
