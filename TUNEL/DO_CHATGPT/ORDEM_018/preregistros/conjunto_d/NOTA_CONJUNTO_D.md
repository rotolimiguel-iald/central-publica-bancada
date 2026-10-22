# F3 — Conjunto D: metadados e piloto sintético propostos

[REAL — revisão local de metadados/código; preparação parcial] Os 14 candidatos têm identidade única e GPS recuperado no catálogo residente cujo hash coincide com o manifesto V1. Existem 28 HDF5 e 28 recortes NPZ H1/L1 nos caminhos nomeados. Todos os 28 tamanhos HDF5 conferem com o manifesto; todos os GPS ficam nas janelas dos recortes; todas as URLs H1/L1 aparecem também no catálogo. Existência/tamanho foram conferidos por stat. **Nenhum conteúdo de strain ou posterior foi aberto**, nem para recomputar hash.

[INPUT — escopo] Esta entrega é uma **proposta não ratificada**. Preserva a ordem dos 14, os quatro holds, os oito pendentes de metadados GR fora da lista e o V1. Não constitui congelamento final, PE, nova injeção, teste composto, veredito científico ou alteração do Atlas/gate.

## Proposta de preenchimento dos GPS

O campo original continua null. GPS_proposed existe apenas no manifesto desta pasta. A precisão e versão são as do catálogo; não foi feita nova medição subamostral do instante.

| Evento | GPS no catálogo | Catálogo / versão | Situação V1 |
|---|---:|---|---|
| GW230919_215712 | 1379195850.0 | GWTC-4.1 / 2 | Sem hold no V1 |
| GW240513_183302 | 1399660400.9 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW240515_005301 | 1399769599.1 | GWTC-5.0 / 1 | HOLD preservado |
| GW240615_160735 | 1402502873.4 | GWTC-5.0 / 1 | HOLD preservado |
| GW240920_073424 | 1410852882.5 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW240923_204006 | 1411159224.1 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW240930_035959 | 1411704018.0 | GWTC-5.0 / 1 | HOLD preservado |
| GW241102_144729 | 1414594067.7 | GWTC-5.0 / 1 | HOLD preservado |
| GW241111_111552 | 1415358970.6 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW241130_034908 | 1416973766.6 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW241210_060606 | 1417845984.8 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW250104_015122 | 1419990700.3 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW250109_010541 | 1420419959.5 | GWTC-5.0 / 1 | Sem hold no V1 |
| GW250118_170523 | 1421255141.2 | GWTC-5.0 / 1 | Sem hold no V1 |

Fontes de identidade: catalogo_v3.csv e GWOSC_O4_32S_V1.manifest.json, com pins V1 conferidos em PROPOSTA_MANIFESTO_METADATA_D.json. Os hashes das séries são **DECLARADOS no manifesto pinado**, não recomputados nesta entrega. OK/nan=0 no manifesto não remove holds nem substitui avaliação DQ.

## GR e PSD: o que existe e o que falta

[REAL] O índice T08 e os três recibos públicos Zenodo têm hashes concordantes. Nomeiam um arquivo de release GR para cada candidato: um no registro 17602505, nove no 20348005 e quatro no 20348006. Foram lidos somente descritores: identidade, URL, tamanho, checksum declarado, licença e atualização. **Não houve download nem busca/abertura de posteriores D.** Isso demonstra disponibilidade documental no retrato do release, não integridade atual do conteúdo remoto.

[DECLARADO] Mf_det e chi_f constam no V1 com origem GWTC4_TGR_III_table1 ou GWTC5_TGR_tables2_3. Fonte exata de tabela e convenção de mediana ainda precisam ser ratificadas para o manifesto final. O catálogo residente também tem massa final source-frame e redshift, mas produto de medianas não é mediana do produto. Nenhuma Mf_det foi substituída por Mf_source×(1+z). Chi_eff não foi usado como chi_f.

[OPEN] Não há descritor PSD nas linhas D do manifesto de strain. Os dois artefatos T07 nomeados não têm linhas dos 14 candidatos. Isso é **ausência de PSD identificado nesses insumos**, não busca exaustiva nem prova de inexistência. Recortes de 32 s não são uma PSD congelada.

strain_io.offsource_psd já oferece seleção do primeiro bloco de comprimento fixo aprovado por flags/finitude, sem escolha pelo nível de PSD, seguida de Welch/Hann/50%/mediana. Não foi executado. Antes de PE real será preciso autorizar e congelar intervalos offsource, exclusão, DQ, estimador, unidades, grade e hash de PSD. O piloto sintético independe de D.

## Instrumento e impedimentos precisos

Base: ORDEM_013_RINGDOWN/bis/e2_code_v1_1_2. Leitura estática, sem importação.

- injection_design.py: 12017563c123df76b856ddedecf9166ddc4c25fe26a5c8b773bc82086b6c842d; coincide do pin integral de R5.
- pe_runner.py: 11c5588fabf5ae0e97d855008a22255bceec7c39380eb94701948a3df55fd370; difere do pin integral de R5.
- pseob_source.py: 58cb22bbe37f9207b526281801855ab38ebbda4fdc229596da92917b4f12098d; coincide do pin integral de R5.
- registration_guard.py: 4dd3005ed34b30a2736c0bb96a9a23d0776ecbe791c9ba463fe632d0a8036a83; difere do pin integral de R5.
- strain_io.py: a52faf32e88088320c57d303987a31ec2b9b59c93e162923d603c2c96b21a5b6; coincide do pin integral de R5.
- synthetic_null.py: be0fa6d4b678993edcbc7dec15f311950c51e466020dc99c5d0f043763eb65f1; coincide do pin integral de R5.
- temporal_contract.py: c8f4ecbc28d4312e3885d61c14f174062c6055eee0bbd54897e725a18240b605; coincide do pin integral de R5.

Os recibos R5 registram 1015/1015 waveforms finitas, sem crash, em geração 8192 Hz/Nyquist 4096 Hz; análise 20–1024 Hz. Há 15 controles focados de fonte, 18 controles de cadeia e comparação de bins nativos. Recibos/hashes foram inspecionados, **não reexecutados**. O pe_runner posterior difere do pin integral do INPUT_MANIFEST R5; não se transfere automaticamente a qualificação antiga ao driver atual.

Impedimentos:
1. inject_into_ifos exige REAL_OFFSOURCE e identidade/GPS real. O novo escopo exige PSD analítica e ruído gaussiano sintético.
2. validate_truth_support trata coordenadas como priors dict; o driver aceita priors numéricos fixos. Só-220 requer DOmega220=DTau440=DOmega440=0 fixos, não tratados por essa função.
3. O adaptador não encaminha generation_sample_rate_hz/generation_maximum_frequency_hz exigidos pelo gerador vigente.
4. R5 qualifica a fonte, não a ativação/registro nem a cadeia completa de injeção/PE.

“Só-220” significa **DTau220 como única deformação livre no IMR pSEOBNRv4HM_PA**. Os harmônicos superiores GR permanecem. Não significa modelo só de ringdown ou retirada dos modos GR.

## Piloto e custos

PLANO_PILOTO_SINTETICO_SO220.json fixa uma proposta revisável:

- P0: contrato sintético separado, hashes, seeds, recursos e proibição de caminhos D.
- P1: adaptação/qualificação de cópia; guards reais preservados, zeros fixos, dicionário LAL novo, sequência GR→RB→GR, grade e contadores.
- P2: fontes sintéticas SYN_A=(50,35;0.3,0.1), SYN_B reservado=(90,60;0.7,0.3), PSD analítica, SNR ótimo de rede 20; controles em ruído zero antes do ruído gaussiano.
- P3: somente após contrato/qualificação, dois jobs pareados SYN_A GR/RB no mesmo ruído sintético; proposta 256 live points, até 10000 calls/job, 1 worker e 3600 s/job. Esses limites medem custo; não garantem convergência.
- P4: dimensionar outra campanha de viés/cobertura com custos medidos. Duas recuperações não certificam cobertura nem C2.

β é calculado em runtime como ALPHA_FINE_CODATA_2018×sqrt(e). A verdade RB será calculada pela lei exata V1 e spin remanescente obtido por fit GR previamente pinado para o progenitor sintético. Os exemplos algébricos de spins 0/0.68/0.9 no plano são fórmulas ilustradas, não dados ou injeções observadas.

[DERIVED — proxy] R5 registrou 86.047283 s CPU e 89.403866 s wall para 1015 gerações: média 0.084776 s CPU/fonte. As 20152 chamadas propostas em P1–P3 dão 1708.399 s CPU como proxy de fonte. Margem de planejamento 3×: 5125.197 s; fator INPUT, não overhead medido. Teto wall proposto: 8700 s. Contrato ainda não ratificado.

**Novo piloto nesta entrega: 0 s de computação; waveforms/injeções/PE executados: 0.** Houve somente leitura de metadados, stat, hashes e aritmética. O tempo efetivo desta auditoria de metadados está no JSON. O proxy não é piloto medido, não estima a análise completa dos 14 e não contrata infraestrutura.

A árvore de falhas consta no plano: medir cada recusa com caso/log/custo, ampliar janela somente antes do congelamento pareado, não reduzir prior por erro numérico, não reiniciar/estender automaticamente. Protocolo anti-parede consultado; esta preparação não declara parede ou impossibilidade.

## Próximo passo independente

Revisar/ratificar proposta de metadados e contrato de uma cópia sintética isolada. Somente com esse contrato autorizado, adaptar a cópia e qualificar controles sem dados D. Isso independe dos quatro holds e da abertura de posteriores. Preparação real de PSD/DQ é etapa própria. Nenhuma edição de V1/original, instalação ou execução foi feita.

## Integridade

- PROPOSTA_MANIFESTO_METADATA_D.json: 946e0a64d6c8a8d405ccc1435d17594eac48602e71b5dbd29719e19529e9ccc7
- AUDITORIA_INSTRUMENTO_SO220.json: 05455249436c0376f665956d978a7980179a3b446c33807e53c6f05391f09543
- AUDITORIA_METADATA_D.json: 6be59c1a21e266afde4c0f8a9706c0f7aa05734341f32d5f8223a86933a2d4a9
- PLANO_PILOTO_SINTETICO_SO220.json: 7d42ad140e895211ad99a6b1b981f67a93cebf986b0658792541a8effae785ac

audit_metadata_d.py lê somente allowlist explícita de documentos/código e usa stat nas séries. build_synthetic_plan.py produz plano e aritmética. Escrita temporária/verificada/atômica; qualquer edição conserva backup dos bytes. Nada promovido ao cânone.
