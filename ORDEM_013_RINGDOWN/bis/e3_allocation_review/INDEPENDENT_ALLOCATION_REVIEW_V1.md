# Revisão independente E3.2 — candidatos de alocação, versão 001

[REAL — revisão de código e fixtures finitas] **CHANGES_REQUESTED_FOR_RENDERER_BOUNDARIES**: corrigir duas fronteiras do helper antes de usá-lo para produzir candidatos. Isso não suspende a ordem nem escolhe uma alocação. O produtor permaneceu intocado; correção posterior requer nova versão/snapshot e revisão dos casos afetados.

## Achados que exigem correção

**F1 [P2] Saída pode escapar do diretório prometido por link simbólico.** `render_allocation_candidates.py:218–221` constrói `HERE/candidates/slug` sem verificar o destino resolvido. Com `candidates` apontando para outra pasta, os três arquivos são gravados fora do sidecar. A fixture `finding_symlink_output_escape` reproduziu o caso, inteiramente dentro da pasta desta revisão. Corrigir rejeitando symlink/junction e verificando contenção do destino resolvido antes de criar/publicar. Não houve escrita em alocação real; os nomes fixos dos candidatos também não são os nomes ativos do E2.

**F2 [P2] Limite de arquivo não é aplicado à saída serializada.** `read_json` limita a entrada, mas `encoded`/`publish_exclusive` (`:87–95`, `:218–224`) não verificam os bytes finais. Proposta fictícia de **83,876 bytes** produziu em memória orçamento candidato de **32,769,335 bytes**, acima de 25 MB. Somente a função de publicação foi interceptada; serialização original intacta. Nenhum arquivo grande foi gravado. Corrigir conferindo o tamanho de todos os payloads antes de criar o diretório e repetindo a guarda em `publish_exclusive`, preservando publicação exclusiva e falhas visíveis.

## Fronteira candidato → ativação

[REAL] A execução normal em cópia isolada produziu apenas candidatos; alocação ativa, jobs futuros e testemunha ficaram ausentes. `load_jobs` do guard congelado retornou somente o job estático. Copiar somente o orçamento ao caminho ativo fictício foi recusado por falta de testemunha. Foram recusados hash de testemunha errado/duplicado, pin de jobs alterado e substituição de job estático. Reexecução com mesmo slug foi recusada e os bytes anteriores ficaram iguais.

[REAL] Ao publicar deliberadamente **somente no universo fictício** orçamento + jobs com hash + testemunha correta, o guard aceitou os jobs mesmo com `status: CANDIDATE_NOT_PUBLISHED`. O contrato já declara isso corretamente: status e extensão CANDIDATE não são gates. A proteção efetiva é não escrever nos caminhos ativos e não emitir testemunha. O helper não chama ativação, controlador ou launcher. A publicação real continua ato explícito revisado do principal.

[REAL] Reviews vazias de publicação/qualidade podem atravessar o serializador, que verifica presença. O guard `load_jobs` as recusou; aceitou as referências fictícias completas e recusou alteração dos bytes da evidência. Não confundir `authorize_event` com fronteira de lançamento. `checked_registration`/`validate_launch` reais não foram executados nesta auditoria.

## Pins, prazo e recursos

[REAL] **47/47 verificações finitas corresponderam às expectativas**, incluindo a reprodução dos defeitos e dos limites documentados; não significa que 47 proteções foram aprovadas. Recibos: `FIXTURE_RESULTS_001.json` (40 casos) e `BOUNDARY_ADDENDUM_001.json` (7 casos). Código copiado byte a byte e executado com Python `-B -O`; fixtures usam apenas biblioteca padrão e metadados inventados.

Negativos exercitados: pins de E2/controller/convergência/budget; deadline expirado/naive; data futura ou anterior ao fim do piloto; soma serial + reserva além do tempo restante; reserva zero; teto de 8 h e teto registrado mais estrito; 25 workers e booleano; cleanup não pago; contador negativo; reutilização de nomes/saídas/destinos; caminhos de jobs/testemunha fora dos subdomínios; hold de qualidade sem resolução.

Dois jobs fictícios de 24 workers cada foram aceitos com soma serial de tetos de 60 s. Isso representa pico previsto de 24 **apenas se executados em série**. Não autoriza 48 simultâneos. `ordered_job_names` é metadado; nem o helper nem o guard impõem agendamento serial ou soma global de workers. A fila/controlador do principal deve demonstrar o teto agregado, incluir trabalhos concorrentes e revalidar o deadline antes de cada lançamento. O orçamento continua preso ao deadline original; não reinicia 40 h.

O helper não certifica código/runtime E2, configuração científica completa, suporte temporal/PSD/priors ou conteúdo científico das cinco alternativas. O contrato é honesto sobre essa divisão. Limite adicional reproduzido: `five_alternatives='abcde'` satisfaz `len==5`; a revisão/publicação deve exigir lista com alternativas identificadas 1–5 e conteúdo real. Recomenda-se endurecer essa validação estrutural, sem alegar que estrutura certifica custo/informação.

## Piloto parcial não é custo convergido e não interrompe a ordem

[REAL] `accepted_for_analysis=False` é recusado em `:122`, como documentado. **É limitação desta interface opcional de projeção, não permissão para parar E3.2/E3.3, aguardar indefinidamente ou fabricar custo.** Se o piloto for parcial: registrar tempo efetivamente gasto, counters, estado de convergência e limite obtido; custo por injeção convergida fica null/OPEN. O principal pode prosseguir com orçamento/parede honestos e alternativas explicitamente condicionais, mediante interface nova revisada ou preparação documental adequada. Não mudar `accepted_for_analysis` para contornar o helper.

O custo do controlador e os três counters permanecem distintos. Convergência aceita não substitui revisão independente do piloto ou comparação entre famílias. `pilot_independent_review` é declaração preservada pelo helper, não recibo autenticado por ele. Nenhum custo observado de piloto real foi lido ou estimado nesta revisão.

## Alternativa 5: entrada documental, sem velocidade instalada

[INPUT/DECLARADO na origem] `bis/E3_ALTERNATIVE5_METADATA_ONLY_V1.json` foi lido e pinado: **3456eac1a5d0805b114151f500f14d3840a399bb7ee9e0fb074764b988c98814**. O estado `DOCUMENTARY_FEASIBILITY_ONLY_NOT_INSTALLED_OR_BENCHMARKED` é apropriado. `find_spec`/PATH registrados pela principal são descoberta de metadados; não executamos novamente essas consultas. Falta de executável no PATH não prova ausência de bibliotecas/headers. A documentação citada descreve interface GR precessante, não um adaptador pSEOB de deformações revisado para o runner congelado.

Custo de instalação, tempo por waveform e parede PE ficam **null/OPEN**, sem promessa de speedup. Nenhuma instalação, importação científica, waveform ou benchmark realizado. O backend atual não muda por editar um campo de jobs; alternativa nova exige implementação/runtime e emenda testemunhada revisados. Esta nota não seleciona a alternativa 5.

## Coeficientes condicionais: conferência independente

[REAL — aritmética finita sobre INPUT] **60/60 linhas**, cobertura completa das dez leituras × três sigmas × dois pisos. Método independente: razão quadrática com `Fraction` exato sobre os valores binários publicados, comparação numérica, teto do número binário publicado e multiplicação inteira por dez; não importamos/executamos o produtor. Maior erro relativo **1.8105790913046955e-16**, abaixo da tolerância declarada **1.7763568394002505e-15**. Pins de código, E0 e ordem conferidos.

Para R-B, piso principal, os pares sigma INPUT → teto por célula → dez células são:

| Sigma INPUT | N contínuo por célula | Teto por célula | Dez células |
|---|---:|---:|---:|
| 0.0497 | 156.7971220597121 | 157 | 1570 |
| 0.058 | 213.5410121124621 | 214 | 2140 |
| 0.24 | 3656.35026684834 | 3657 | 36570 |

Os aproximados “213” e “3.650” da ordem não são os tetos inteiros do E0 publicado: os tetos conferidos são 214 e 3.657. Não é custo medido nem alocação. Os três sigmas (.0497/.058/.24) são ilustrações da ordem; dez células com sigma comum não medem cinco bins distintos. A regra 1/√N exige independência e ausência de viés residual não calibradas; não paga cobertura, seleção, normalização ou cauda 5σ. Piso /15 é sensibilidade ao lado, não substituição do principal /5.

**18 linhas** mantêm alvo null por efeito zero/aberto. **18 linhas** excedem o regime de inteiros exatos do binary64: `ceil` do valor publicado está correto, mas não certifica o teto matemático exato da razão antes do arredondamento. A fonte declara essa limitação; conservar “escala ilustrativa”, sem planejar contagem exata astronômica. Horas alocadas e custo por injeção convergida continuam null em todas as linhas. Nenhum coeficiente prioriza leitura.

## Custódia e fechamento desta revisão

- E2 efetivo, somente pin e contrato consultados: `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416`.
- Guard: `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7`, igual ao pin na árvore congelada E2.
- Renderer revisto: `89c7ea0b6a04600018548943f4850542ff244f5705d790371f02e399a6076ea9`.
- Coeficientes: `f984ebe58ae2b788b97762e1ba9b64917d58c74c09f93742ec80bca55a302649`.
- Fontes completas, cópias byte a byte e pins: `SOURCE_SNAPSHOT_001.json`, `snapshot_001/`, `coefficient_snapshot_001/`.
- Resultados independentes: `FIXTURE_RESULTS_001.json`, `BOUNDARY_ADDENDUM_001.json`, `COEFFICIENT_REVIEW_001.json`.

Nenhum original, produtor E4/E7/E6 ou artefato selado foi alterado. E6 permanece não executado; E7 sem extração. Não houve leitura de seed real, posterior, strain ou recibo privado de piloto real. Nenhuma ativação E2, publicação de jobs/alocação reais, seleção de alocação ou campanha científica. Fixtures preservadas em pasta própria, inclusive defeitos. Esta revisão não conclui a ORDEM013BIS.
