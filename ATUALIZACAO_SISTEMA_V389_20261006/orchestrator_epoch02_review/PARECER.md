# Revisão independente — orquestrador v389, epoch02

**PASS restrito à revisão estática. Nenhum bloqueador concreto localizado no delta.** Os achados ORCH389-01 e ORCH389-02 do candidato anterior ficam fechados somente para este sucessor; o parecer BLOCKED anterior permanece íntegro.

Identidade da revisão: 26408df4-1cd0-41c7-a160-943664ab45d1. Instante UTC: 2026-10-06T19:58:14.071328+00:00. Manifesto lido: 6297 bytes, SHA256 62d9de03137db9f59b1a9263d3cca74cdac4fa28ce5082caa18b08a7d54ac2d8.

## Evidência e escopo

Foram conferidos os 21 membros do manifesto por bytes/SHA256, os 17 destinos planejados e seus baselines: 16 arquivos novos em uma raiz de geração nova e uma substituição do módulo comum. Os quatro baselines de módulo, catálogo histórico, manifesto antigo e índice antigo conferem. A raiz nova e os três marcadores de instalação ainda estavam ausentes.

Os 22 pins do pacote anterior continuam íntegros. As 13 fontes e o índice novo são os mesmos bytes já examinados nele. Recalculei a geração ordenada 95d3f03e1b8dc91ef4e57e1ea2543cc9d3c86da38bbaf2e701823c7555141c3c; descriptor, selo, programa, resultados e manifesto formal ligam-se pelos pins. O index_sha256 confere. Nenhum rito, compilação ou resultado científico foi reproduzido.

A comparação textual mostra uma única substituição de constante MEMORY; removida essa atribuição, os ASTs completos são iguais. Isto conserva as restrições, allowlist, orçamento/contexto, recusa de reconstrução automática de snapshots e os estatutos anteriores. O manifesto de instalação difere do manifesto de estágio somente pelos caminhos explicitamente retargetados. Não altera catálogo histórico ou fila.

## ORCH389-01 — fechado pelo isolamento da geração

Em canonical_memory.py:14, o novo default passa à raiz releases/v389_95d3f03e1b8dc91e. Os defaults de load e prepare já carregados em residentes continuam vinculados à raiz antiga. Em prepare:252 e 279, o mesmo argumento directory orienta a validação e a abertura SQLite. O instalador não substitui o índice/manifesto antigo; portanto, o interleaving apontado na primeira revisão já não troca o conteúdo do caminho aberto pelo leitor residente.

Em install_epoch.py:50–54, os 16 arquivos da raiz nova são escritos, relidos e validados por cm.load(target, refresh=False). Só depois das reconferências de fontes antigas e CAS do módulo, linhas55–59, a constante passa a ser publicada para importações novas. A diretoria parcialmente construída não é o default de leitor algum. Não depende de supor quiescência nem de duplo polling.

O alcance é uma atualização por geração, não hot reload: residentes continuam históricos até seu próprio ciclo de recarga. A apresentação de versão deve continuar usando o recibo real de cada processo.

## ORCH389-02 — fechado pela reserva exclusiva

install_epoch.py:12–15 usa open('xb'), escreve, flush, fsync e relê o marcador. A aquisição está na linha47, antes da primeira escrita de destino na linha52. Uma segunda instância não pode substituir esse marcador por save_json: FileExistsError encerra a aquisição. Falha ou incerteza preserva o marcador; a presença da raiz nova também recusa reinício na linha28.

Não foi executada disputa concorrente. A conclusão deriva das operações exclusivas e da ordem do código, não de mocks nem de sucesso de instalação.

## Admissão, paths e recuperação

Linhas18–25 vinculam o manifesto exato ao PASS independente, à decisão ROOT separada, ao hash do recibo de revisão e ao pin da auditoria científica. Linhas26–44 fixam a raiz, o conjunto exato dos17 destinos, fontes dentro do pacote, baseline e conteúdo. Não há concessão de execução científica/provedor nem escrita na fila. A invocação deve usar Python normal sem -O, pois as validações do instalador usam assert.

safe_files.py preserva backup de bytes antes da única substituição existente e usa temporário, conferência e os.replace. Não há atomicidade multi-arquivo nem garantia contra queda do sistema. Se uma falha ocorrer depois de os.replace do módulo, mas antes do retorno de replace_bytes, switched pode ainda ser false (linhas58–63): não se deve inferir rollback; conferir os hashes reais e recuperar manualmente com a tentativa preservada. O novo diretório já está validado nesse ponto, logo isso não reintroduz a mistura de geração do achado01. Falha de gravação do recibo posterior também não autoriza repetir.

A reserva exclusiva cobre este pacote; o CAS é otimista, não exclusão geral contra outro implantador arbitrário. O plano examinado não introduz esse escritor concorrente. A imutabilidade das raízes é operacional e conferida por hashes; não é alegação de ACL imutável do sistema operacional.

## Próximo passo e limites

ROOT pode decidir a instalação local específica usando REVIEW.json desta pasta e o manifesto pinado. Este PASS não é autorização, não é instalação e não certifica transporte real. Depois de eventual instalação, conferir em processo novo a raiz, geração, integridade e recuperação documental; não atribuir recarga aos residentes antigos.

Auditoria científica consultada: science_audit/controller_static_20261006/MANIFESTO_AUDITORIA.json e PARECER_INDEPENDENTE.md, com estatuto estático próprio. A ligação do selo aqui não promove validação formal a confirmação física. Nenhum candidato importado, instalador executado, fonte científica executada, provedor chamado, memória/ledger ou mapa remoto alterado.
