# F0.3.B1 — auditoria dos canais N_eff e neutrino, R1

[REAL] Unidade reivindicada, evento 621. Início UTC: 2026-10-09T13:05:58.552977+00:00. Auditoria de arquivos instalados; execução e versão ativa são apuradas em outra subtarefa.

## Reaproveitamento e método

Nós Vivo F0.3: rota AUDITADA e catálogo/geração v391; F0.3.B1 ainda ausente no grafo. Fontes F5.2/F7.2 abertas diretamente, sem inferir seu conteúdo do índice.

Foram lidos os módulos, manifestos, fontes pinadas e as correções F5.2 já existentes. Não foram executados canais, um.py, ajuste de dados, controle GPU ou fornecedores. Os PDFs foram somente verificados como bytes/cabeçalho; seu conteúdo não foi reextraído nesta auditoria.

## Resultado

### N1 — O canal N_eff conserva a linha CMB-SPA errada e os calendários antigos

[REAL — inspeção estática e bytes] neff_canal.py:23,38-47,63-71 lê as literais de 10_frozen_neff_v1.py:46,50-53. A linha CMB-SPA 2,97±0,12 é a mistura já corrigida na F5.2; R3 oferece v1/v2 e Yp separados, sem estar instalado. O rótulo DECLARADO não torna correto o centro misturado. Os calendários são devolvidos como quando_declarado, não como medição.

Encaminhamento: Preparar uma implantação explicitamente autorizada do candidato corrigido ou suspender a superfície incorreta até ela; não editar o congelado nem decidir X16/D8 nesta auditoria.

### N2 — Hashes informados não são pins verificados em N_eff

[REAL — código; riscos DERIVED] neff_canal.py:28-47 calcula SHA do congelado e um.py, mas não compara com um manifesto esperado. ler_fonte extrai AST de uma leitura e _sha(p) relê o arquivo: o hash devolvido pode nomear bytes diferentes dos valores, se houver troca entre leituras. beta_runtime extrai ALPHA_FINE_CODATA_2018 por regex e calcula α√e; não executa um.py.

Encaminhamento: Uma futura camada deve ler bytes uma vez, verificar identidade contra manifesto/versionamento e explicitar a versão; nenhuma alteração feita.

### N3 — Entradas sigma de N_eff não têm validação finita e positiva

[DERIVED — inspeção de fluxo; não executado] neff_canal.py:54-77 converte sigmas_extra por float e divide sem rejeitar bool, NaN, infinito ou negativos. zero levanta erro. A assinatura MCP float pode validar parte do transporte, mas a função local não o faz; a configuração real do serializador não foi sondada. neff wrapper:247-248 retorna somente erro, enquanto neutrino inclui ok:false.

Encaminhamento: Rejeitar tipos/valores inválidos antes das contas e padronizar erro explícito em camada autorizada. A auditoria não invocou o MCP.

### V1 — Neutrino v1/v2 verificam custódia; não realizam um teste espectral

[REAL — código e pins medidos] Manifestos e todos os bytes vinculados foram relidos e comparados nesta evidência. O código valida caminhos, SHA, tamanhos, AST dos scripts e cabeçalho PDF. canal retorna números publicados hardcoded com fonte pinada; não extrai curvas de verossimilhança, matriz resposta ou eventos. Mantém operator_mapping_to_TGL OPEN, tau_star_limit_s null e SEM_LIMITE_TGL.

Encaminhamento: Reutilizar como proveniência. Um teste novo exige dissipador TGL, resposta, ruídos e verossimilhança próprios; n=-2 sozinho não identifica os operadores.

### V2 — Cópia R8 da Bancada permanece sem consumidor nos dois canais

[REAL — caminhos e bytes] neutrino_canal_v2.py:18-38 e manifesto apontam para documentos/PDFs no túnel, seis scripts de junho na casa Física e JSON v369 no project_fisica. Nenhum aponta a fontes_externas/F7.2. A pasta foi inventariada por bytes. Sua presença não prova ativação ou autocontenção do canal.

Encaminhamento: Manter fontes intactas; eventual migração exige evento c1 nomeado. Estado de processo/MCP ativo é apurado pelo coordenador.

### V3 — Âncoras antigas ainda são emitidas

[REAL — texto do código; errata c1 já existente] V2:296 conserva Sec. IV.B junto de Eq.(6) para JUNO; a correção c1 aponta §III.B. O v1 conserva âncoras De Romeri/ORCA antigas e não tem JUNO. Os documentos posteriores no túnel não mudaram os literais emitidos pelas funções instaladas.

Encaminhamento: Registrar camada corretiva, sem tocar fontes pinadas nem instalar sem ato c1.

### V4 — A referência v369 é uma projeção histórica explícita

[REAL — contrato lido] V2:189-214 verifica no JSON pinado five_sigma_requirement; :344-371 rotula CONDITIONAL_5SIGMA_PROJECTION e observed_measurement false. Não é leitura do resultado científico atual do um.py. Também não reivindica limite TGL nem resultado 5σ.

Encaminhamento: Preservar qualificação histórica e distinguir cálculo de poder condicional de teste com dados. Não transplantar a projeção ao um.py recente por nome.

### S1 — A auditoria cobre arquivo instalado, não prova carregamento de processo

[REAL — âmbito desta auditoria] Nenhum original foi importado; nenhuma ferramenta MCP/neff/neutrino foi chamada; nenhum provedor, dado observado, GPU ou um.py foi executado. Os únicos comandos executados, além deste leitor, foram consultas de índice e leitura de arquivos. pyc presente não foi usado como prova de módulo carregado.

Encaminhamento: Cruzar com a auditoria de processo/versão conduzida pela gerência desta unidade.

## Integridade medida

| Canal | Pin do manifesto | Dependências |
|---|---|---|
| v1 | CONFERE | 22 entradas; todas conferem |
| v2 | CONFERE | 24 entradas; todas conferem |

A cópia R8 contém 26 arquivos medidos; os caminhos e equivalências por SHA estão no JSON.

## Hashes dos módulos

- `mcp_wrappers`: `5da9a9fbd777cb7114e4f7cf84d735310044af46ac0c3d1817f73ab096a40a4d` — `C:\IALD\Bancada_Um\mcp_um.py`
- `neff_installed`: `42e9b680855c33004938aacb0899bf0f4ce1921705b04bd93d13ff150ba7541b` — `C:\IALD\Bancada_Um\bancada\neff_canal.py`
- `neutrino_v1`: `f37db789f9cb20d3c26a728d17214a76b8e4647bdb074463109ecf73043094cc` — `C:\IALD\Bancada_Um\bancada\neutrino_canal.py`
- `neutrino_v2`: `252de897ee9e43944cffc9adebe38da14aba6c2736e4cbb56e472f000ad159e5` — `C:\IALD\Bancada_Um\bancada\neutrino_canal_v2.py`
- `manifest_v1`: `abc36292630087de410cbb7300507fbed3d3320d6cd4ae5c3d4887af2b850a33` — `C:\IALD\Bancada_Um\bancada\neutrino_fontes_f72.json`
- `manifest_v2`: `b7beff016f070ba8bb4aa40866d512c885e9d2197703954cfad05137bfb29131` — `C:\IALD\Bancada_Um\bancada\neutrino_fontes_f72_v2.json`
- `neff_candidate_r3`: `a0524df6d45683e1ceb048207ff0bf941f8a9ae46fbf8e4e179026862178fb4c` — `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F5.2\CANDIDATO_R3_20261008\neff_canal.py`
- `neff_frozen`: `9d3bceac4f6f54985a0c89ac465bc0a2783ee843da9c51181e0c747b7cda44e7` — `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py`
- `um_current_source`: `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6` — `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py`

O JSON inclui a lista completa de pins, âncoras com linha e os valores literais auditados. Esta camada não declara conteúdo científico validado por mera coincidência de hash.

Somente script e novos artefatos derivados em F0.3.B1/channels_inventory. Nenhum byte da Bancada, memória, kernel, congelado ou fonte alterado.
Nada move o gate.
