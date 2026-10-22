[REAL/OPEN] E7 preparada para revisão e inclusão pelo principal; nenhuma extração real executada. Esta etapa não conclui a ORDEM013BIS. Axiomas N/A — sem Lean.

## Entrega concreta

- `producer/extrai_posteriores_pseob.py`: extrator h5py de cinco colunas pareadas integrais, com priors textuais, origem HDF5/arquivo, runtime e pins. Default e único modo implementado: sem thinning. Recusa produto ponderado, metadado incompatível e identidades duplicadas. JSON novo diretamente em B/cache, tornado read-only após publicação. O programa não extrai o arquivo tar/zip; confere seu hash e usa HDF5 já custodiado.
- `producer/tgl_ringdown_ampliacao.py`: consumidor NumPy + biblioteca padrão; guarda E2 autorizada importada somente após conferir SHA; todos os códigos produtores e inputs conferidos. Matriz de 10 leituras × 2 variantes. Sem teste: `AWAITING_DATA`; com sistemática aberta: `INCONCLUSIVE_SYSTEMATICS`. Não emite exclusão, falsificação, BF nem significância física.
- `EXTRACTION_PLAN.json`: plano concreto dos 33 produtos do conjunto GWTC5_33 previamente fixado por E0, sem reextração. Amostras reais não foram abertas; origem e N vêm de metadados existentes. Priors derivados Mfdet/af/z continuam OPEN. Priors de deformação são declarações literais, não função de densidade implementada.
- `E2_INCLUDE_FINAL.json`: fragmento atualizado para o principal, com árvore produtora, inputs, plano, nuisance e alvos condicionais. **Substitui para integração o E2_INCLUDE.json inicial**, preservado como tentativa preparatória. Não é registro nem autorização. O pin da guarda é observação de arquivo em edição; o principal deve conferi-lo após Averroes finalizar.
- `SOURCE_PINS.json`: fontes/metadados lidos, com SHA medido; nenhum pin de HDF5/tar foi fabricado. Esses pins do plano são DECLARADOS nos metadados anteriores e serão medidos pelo extrator antes de abrir valores.
- `UNIT_TESTS_FINAL.log`: 23 testes passaram em 0,497 s de execução da suíte, Python do WSL `/opt/lal_env`; NumPy 2.5.3 e h5py 3.16.0. Sem instalações, PE, MC, strain, waveform ou catálogo real.

## Diagnósticos efetivamente implementados

`fullsample_diagnostics(events, statistics)` calcula N, médias, desvios ddof=1 e matriz de covariância das cinco colunas de cada posterior completo. Calcula participações 1/sigma_tau² e 1/sigma_df⁴, registra dominância sobre o teto E2 sem retirar evento, médias descritivas leave-one-out e partição nominal com a semente E2. Nenhum desses números é uma likelihood populacional ou teste calibrado. LRT, p do split, sigma_pop físico, z físico e lnB permanecem null. Sem inputs reais, nenhum diagnóstico real foi produzido nesta etapa.

`conditional_projection(delta, sigma, design)` implementa a projeção gaussiana condicional com nuisance livre por SVD. Verificações analíticas: correção constante é absorvida pelo intercepto; contraste ortogonal preserva a informação esperada; desenho singular recusa. Não usa a covariância local E1 como física e não roda MC. Não há predição nova por leitura: a likelihood restrita que dependeria de predições amostra a amostra permanece NÃO PAGA.

## Revisão do draft E2 recebido

[REAL — leitura de E2_DESIGN_DRAFT_001.json, hash no fragmento final] O draft explicita que lnB depende de modelo restrito normalizado/seleção; matched_z usa covariância E1 apenas como INPUT sintético; LRT IV estritamente >25; nuisance livre; teto de peso 0,2; split seed 132299; correção de multiplicidade; jackknife; piso /5 com /15 ao lado; gate vermelho sem z. Esses itens são desenho, não execução ou validação física paga. O consumidor exige os vereditos exatos e invariantes centrais do esquema, e recusa status de draft.

O campo `extra_code_trees` do draft observado não é a chave `extra_code_roots` lida pela versão de `registration_guard.py` observada nesta preparação. O fragmento final usa **extra_code_roots**. Principal deve unificar a chave ao consolidar E2 e incluir `producer/` inteira. E2 também precisa incorporar o objeto `e7` do fragmento. A função externa esperada é `checked_registration() -> (reg, digest)`, mais `authorize_event(reg,event,mode)` e `utc(timestamp)`. O consumidor compara registro retornado com os bytes cujo SHA foi solicitado. Não há fallback permissivo.

## Interface para o principal

1. Revisar os dois módulos e o plano; incorporar `e7`, `extra_code_roots` e `input_pins_relative_to_Chatgpt` de E2_INCLUDE_FINAL.json, preservando entradas já existentes. Atualizar `e7.guard_sha256` com o arquivo final. O guard também verifica runtime, orçamento e testemunha; não removê-los para fazer smoke passar.
2. Publicar o registro E2 e a testemunha no túnel. Nenhum arquivo desta entrega se passa por essa testemunha.
3. Autorizar depois de E2: recibo JSON com `status=AUTHORIZED_BY_PRINCIPAL_AFTER_E2`, `registered_utc` com timezone posterior ao E2, `registration_sha256`, `plan_sha256`, `producer_tree_sha256`. Transportar seu SHA por argumento. Esta etapa não produziu esse recibo.
4. Executar futuramente, somente após autorização: `/opt/lal_env/bin/python -B producer/extrai_posteriores_pseob.py --root <Chatgpt> --registration <E2> --registration-sha256 <SHA> --authorization <recibo> --authorization-sha256 <SHA> --output <B/cache/POSTERIORES_PSEOB_GWTC5_33.json>`.
5. Consumir com `tgl_ringdown_ampliacao.py` usando `--root`, `--registration`, `--registration-sha256`, `--posterior`, `--posterior-sha256` e `--output`. Sem `--posterior`, emite somente matriz AWAITING_DATA, após todas as verificações E2. O SHA de transporte do JSON recém-produzido vem do principal/custódia; não é possível pré-fixar bytes ainda inexistentes em E2. Não alterar o registro científico para encaixar um resultado.

## Critérios e limitações honestas

| Critério | Estado e evidência |
|---|---|
| Código, contratos e hashes antes de E2 | PAGO como preparação; MANIFEST_FINAL.json e fragmento final |
| Leitura metadata-only de esquemas/dataset/calibrações | PAGO; SOURCE_PINS.json |
| NumPy sem h5py/scipy no consumidor | PAGO; teste AST e revisão do import |
| Pares completos, sem thinning, duplicatas | PAGO no código e fixture determinística; não executado em catálogo real |
| Priors completos normalizados | NÃO PAGO; derivados e fatorização OPEN; não inventados |
| Todos os dez cenários, sem preferência | PAGO na matriz 20 células; previsões/likelihood física continuam NÃO PAGAS |
| Guarda strict code/input/witness | Interface implementada; integração real final NÃO PAGA até E2/guarda final e revisão adversarial |
| Diagnóstico fullsamples | Implementado e testado sinteticamente; execução real NÃO PAGA |
| BF, seleção, covariância física, 5sigma | NÃO PAGO; null, explicitamente recusados |
| Dados cegos/liberação de offset | NÃO PAGO; esta versão recusa antes de abrir JSON cujo plano contém teste |
| Extração secundária 440/rota IV calibrada | NÃO PAGO; variantes matriciais não são dados ou posterior 440 |
| Revisão independente | NÃO PAGO; houve revisão pelo próprio autor, não selo adversarial |
| Originais, memórias, ordem e canônico | Intocados; só escritas sob e7_prepare |

Falhas de ambiente: primeiro acesso WSL retornou E_ACCESSDENIED no sandbox; acesso autorizado ao runtime existente depois funcionou. Não foi rejeição do auto-review. Buscas constataram C:/IALD/AGENTS.md e MANIFESTO_DOWNLOADS.json local ausentes; usaram-se instruções fornecidas e recibos de arquivo existentes. Nenhuma falha foi rotulada sucesso. Não houve teste científico com resultado real nem entrega final da ordem.
