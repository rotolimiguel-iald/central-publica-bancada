# D — inventário documental dos membros de calibração

Pedido `a178d269-5b24-443a-b59b-4060aebe9a4c` — 06/10/2026. Entrega para revisão ROOT.

**[REAL — nomes/cabeçalhos]** Foram obtidos uma vez os dois pacotes oficiais e enumerados seus cabeçalhos. Nenhum membro foi extraído; nenhuma linha numérica de calibração foi interpretada. Não houve abertura de strain/PE/posteriors, execução de ciência, nova chamada a modelos ou retry INIT003.

## Resultado medido

| Pacote | Bytes comprimidos | Cabeçalhos | Arquivos regulares | H1 | L1 |
|---|---:|---:|---:|---:|---:|
| LIGO_O4a_cal_uncertainty.tgz | 35414303 | 8266 | 8264 | 3871 | 4393 |
| LIGO_O4b_cal_uncertainty.tgz | 27856754 | 8142 | 8140 | 3355 | 4785 |

Total: **63271057 bytes**, abaixo de100MiB; cada arquivo abaixo de50MiB. Os **16404** arquivos regulares seguem o padrão de nome documentado. Os outros quatro membros são diretórios. Não apareceram links ou membros especiais. Os nomes são únicos dentro de cada pacote e as épocas são únicas por detector/run.

Os hrefs foram extraídos da [página oficial DCC T2500288-v5](https://dcc.ligo-wa.caltech.edu/LIGO-T2500288/public); tamanho HEAD, GET, arquivo local e ETag foram confrontados. `DISCOVERY.json` e `DOWNLOAD_RECEIPT.json` preservam URLs efetivos e recibos. Os SHA256 são calculados dos arquivos comprimidos locais. Nenhuma URL de pacote foi construída por adivinhação.

## Identidade dos pacotes

- `LIGO_O4a_cal_uncertainty.tgz`: `a10f25661d5ccc0acd0cd3a6fb22d1544bf83550be904e1900eaa5f7e2363670` — [arquivo publicado](https://dcc.ligo-wa.caltech.edu/public/0202/T2500288/005/LIGO_O4a_cal_uncertainty.tgz).
- `LIGO_O4b_cal_uncertainty.tgz`: `3d6e7a5ab65421bb2a2175790a98de5b9fd6e0149845255ce45315cfba808450` — [arquivo publicado](https://dcc.ligo-wa.caltech.edu/public/0202/T2500288/005/LIGO_O4b_cal_uncertainty.tgz).

## Associação aos eventos — candidatos, não escolha científica

Reutilizamos somente o GPS textual do manifesto de metadados já admitido, mantendo sua condição de proposta não ratificada. Não reabrimos catálogos nem refizemos a reconciliação GPS. Para cada run/detector, encontramos a época nominal mais próxima e preservamos os vizinhos. Os nomes completos estão no JSON de associação.

| Evento | GPS candidato H1 | Distância H1(s) | GPS candidato L1 | Distância L1(s) | Hold anterior |
|---|---:|---:|---:|---:|---|
| GW230919_215712 | 1379196018 | 168.0 | 1379196018 | 168.0 | Sem hold anterior; não liberado |
| GW240513_183302 | 1399662018 | 1617.1 | 1399662018 | 1617.1 | Sem hold anterior; não liberado |
| GW240515_005301 | 1399770018 | 418.9 | 1399770018 | 418.9 | Preservado |
| GW240615_160735 | 1402502418 | 455.4 | 1402502418 | 455.4 | Preservado |
| GW240920_073424 | 1410854418 | 1535.5 | 1410854418 | 1535.5 | Sem hold anterior; não liberado |
| GW240923_204006 | 1411160418 | 1193.9 | 1411160418 | 1193.9 | Sem hold anterior; não liberado |
| GW240930_035959 | 1411704018 | 0.0 | 1411704018 | 0.0 | Preservado |
| GW241102_144729 | 1414594818 | 750.3 | 1414594818 | 750.3 | Preservado |
| GW241111_111552 | 1415361618 | 2647.4 | 1415358018 | 952.6 | Sem hold anterior; não liberado |
| GW241130_034908 | 1416974418 | 651.4 | 1416974418 | 651.4 | Sem hold anterior; não liberado |
| GW241210_060606 | 1417845618 | 366.8 | 1417845618 | 366.8 | Sem hold anterior; não liberado |
| GW250104_015122 | 1419991218 | 517.7 | 1419991218 | 517.7 | Sem hold anterior; não liberado |
| GW250109_010541 | 1420419618 | 341.5 | 1420419618 | 341.5 | Sem hold anterior; não liberado |
| GW250118_170523 | 1421254818 | 323.2 | 1421254818 | 323.2 | Sem hold anterior; não liberado |

**[DERIVED — metadados]** Há 28 candidatos temporais únicos para os28pares. A maior distância nominal é 2647.4s. Essa proximidade não comprova validade do envelope nem constitui um corte de seleção.

## Lacunas temporais observadas nos nomes

O intervalo abaixo é a diferença entre as épocas de membros imediatamente anterior/posterior ao GPS do evento. Não é duração de dados ruins, lacuna de strain, validade de calibração ou diagnóstico do instrumento. A cadência horária nominal não garante uma grade sem lacunas.

| Evento | Detector | Espaçamento entre vizinhos(s) | Distância ao mais próximo(s) |
|---|---|---:|---:|
| GW230919_215712 | H1 | 46800 | 168.0 |
| GW240515_005301 | L1 | 18000 | 418.9 |
| GW240615_160735 | H1 | 10800 | 455.4 |
| GW241111_111552 | H1 | 18000 | 2647.4 |
| GW241130_034908 | L1 | 7200 | 651.4 |

Eventos com épocas candidatas H1/L1 diferentes: GW241111_111552. Não impor uma única época aos dois detectores. Um evento exatamente sobre uma época tem espaçamento inclusivo zero no JSON; isso também não prova continuidade ao redor dele.

## Alcance e alternativas

Antes da obtenção, foram comparadas duas rotas: índice remoto oficial versus enumeração limitada dos pacotes. A página consultada e as duas buscas oficiais não forneceram um índice de membros; isso não é prova universal de inexistência. A enumeração dos pacotes foi realizada no mandato específico, com limites de stream e recibos sem repetição automática. `PREPARACAO_E_ALTERNATIVAS.md` conserva a comparação anterior ao download.

A identidade externa ficou concreta: pacote pinado + caminho exato do membro + detector/época extraídos do nome + cabeçalho. **Continuam [OPEN]** colunas, unidades efetivas, grade de frequência, intervalo de validade, correlações, tratamento estatístico e compatibilidade C00/C01 de cada membro. Nada disso foi inferido do nome, diretório ou calendário. Hashes individuais do conteúdo dos membros permanecem nulos; o hash do pacote fixa indiretamente o conjunto de bytes sem interpretar esse conteúdo.

Para avançar depois desta revisão, há duas alternativas de proveniência: (1) qualificação segregada dos envelopes DCC candidatos, mantendo ciência fechada e definindo o tratamento apenas após examinar suas convenções; (2) inventário autorizado de cabeçalhos PE para vincular o produto ao label exato publicado. A segunda aumenta a proximidade com a proveniência PE, mas exige impedir leitura de posteriors. Nenhuma foi executada ou adotada por este inventário.

## O que exatamente foi lido

A transferência e o SHA256 leram os bytes comprimidos. O percurso gzip/TAR necessariamente descomprime e descarta bytes para chegar aos próximos cabeçalhos. O código não chama extract, extractall ou extractfile, não interpreta linhas numéricas e não grava membros separados. A enumeração respeitou também limites adicionais de100000membros/8GiB descomprimidos por pacote. Não afirmar que os bytes comprimidos nunca foram acessados.

Somente cópias textuais admitidas foram usadas para relacionar eventos. Não tocaram contratos, V1, holds, memórias compartilhadas ou resultados do piloto. CAL_B não foi ratificado e D permanece fechado. O inventário facilita a próxima verificação; não fornece resultado físico, posterior ou significância.

## Arquivos de revisão

- `ASSOCIACAO_14_EVENTOS_28_DETECTORES.json`: nomes completos, candidatos, distâncias, vizinhos, pins e campos não observados.
- `LIGO_O4a_cal_uncertainty.tgz.members.json` e `LIGO_O4b_cal_uncertainty.tgz.members.json`: todos os cabeçalhos observados.
- `RESUMO_INVENTARIO.json`, `FONTES_E_PINS.json`, `VALIDACAO_DOCUMENTAL.json`: resultados e limites.
- `MANIFESTO_ENTREGA.json`: identidade por bytes de todos os artefatos da entrega, incluindo pacotes fechados.
- `public_archive_inventory.py` e `build_inventory_delivery.py`: procedimentos auditáveis; não reexecutar fases já iniciadas para repetir downloads.
