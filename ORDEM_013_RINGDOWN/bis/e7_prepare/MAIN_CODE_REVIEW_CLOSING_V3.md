# Fechamento da revisão do código principal — v3

[REAL] **20/20 verificações incrementais passaram.** Nos bytes fotografados abaixo, os problemas de recibo agregado e mapa GPS foram corrigidos; a fronteira `load_jobs` recusa quality holds sem resolução válida. Nenhum novo bloqueador foi encontrado nessas fronteiras. Esta revisão limitada não executa nem registra E2 e não encerra ORDEM013BIS.

Snapshot: `MAIN_CODE_REVIEW_SNAPSHOT_V3.json`, SHA256 `dcab9fda683201c68d8fcaa1ff0d47eb6e8af24e86fbcd4402009adf316db47a`. Resultados: `MAIN_CODE_REVIEW_FIXTURES_V3.json`, SHA256 `87f2ffd39e03effba6ab6f2eb3592b86be030f7910c79929f02057e487337618`. Script: `review_main_closing_fixtures_v3.py`, SHA256 `303344508d31996d9130268847c7794a1941fbf1243dbed0c8f255a3550f5a8f`. Os módulos foram compilados dos bytes fotografados. Fontes alteradas depois das fixtures: bis/e2_code/pseob_source.py. A nova revisão de pseob_source/contratos temporais pertence a B; este fechamento não aprova automaticamente esses bytes posteriores. Null, fetch e guarda conferidos aqui permanecem iguais ao snapshot.

## Correção ao lado da interpretação da v2

O resultado v2 27/34 permanece preservado. **As quatro sondas de `authorize_event` não demonstravam bypass de lançamento:** essa função classifica identidade/papel; o bloqueio de resolução de qualidade pertence a `load_jobs`/`validate_job_reviews`, chamado na cadeia de lançamento. A afirmação preliminar de ausência desse bloqueio fica retirada. Os novos testes exercitam essa fronteira, com testemunha simulada e verificação real dos hashes, datas e flags da evidência sintética.

- Os quatro eventos sob hold são recusados sem `data_quality_resolution`. Resolução reprovada ou SHA divergente também é recusada. Controle com resolução válida passa. A mesma regra foi testada para job de alocação dinâmica. Nenhum job foi lançado.
- `null_campaign` agora publica `SYNTHETIC_NULL_CAMPAIGN_FAILED` para exceção do deadline anterior ao filho, recibo de célula inconsistente e TimeoutExpired com stdout/stderr em bytes. Fixtures tiveram 0, 1 e 1 chamadas ao stub; nenhum subprocesso científico. Os 25 callbacks de sucesso já haviam sido verificados na v2 e não foram repetidos.
- Downloader: handler de prazo global levanta TimeoutError; cleanup restaura handler e desarma timer; timer preexistente é recusado. Teste determinístico simulado, sem sinal real/socket/rede; não demonstra latência máxima do sistema operacional. Comentário agora distingue timeout de inatividade e prazo global.
- Draft003: `validate_config` passa com duração 16 s e início GPS 1420878129; mapa `event_reference_GPS` coincide com o piloto em 1420878141.2; há exatamente 25 células registráveis. Não é validação de waveform/cobertura numérica do sinal.
- Integração de `derive` em `pe_runner` e publicação de recibo privado foram conferidas estaticamente. Nenhuma PE/conversão numérica foi executada nesta rodada; os dois remanescentes sintéticos do parecer original são evidência anterior distinta.

## Fechamento dos achados anteriores

A v2 já reproduziu as correções de disjunção da janela inteira de injeção contra GPS real pinado; segunda família XPHM somente GR; parâmetros Planck18 iguais ao INPUT nomeado; transferência truncada/tamanho/checksum ausente; recipe/allocation/jobs SHA e revalidação antes da promoção. Essas fixtures não foram repetidas indiscriminadamente. Arquivos idênticos entre snapshots v2/v3: blinding.py, null_runner.py, pseob_source.py, remnant_conversion.py, route_iv_null.py, run_controlled.py, strain_io.py, synthetic_null.py.

As conclusões científicas do parecer original permanecem condicionais: composição balanceada fixa nos matched nulls difere da composição multinomial da rota IV; ceil(N90) herdado do forecast sem nuisance não se torna N90 calibrado com nuisance. As larguras e seeds são INPUTs congelados; covariância local não vira covariância física. Nenhum novo nulo/MC foi calculado aqui. O censo continua ausência no escopo, não ausência universal de publicação; nove conhecidos ficam em calibração, 14 têm escopo e quatro exigem resolução de qualidade.

## Limites para o freeze

Montagem final deve conferir próprias árvores, extra_code_roots E7/E4, pins, runtime, orçamento e testemunha real. Draft003 não é registro. Integração de guarda real, lançamento, monitoramento de deadline e resultados de PE não foram executados por este revisor. Fatores de Bayes físicos, seleção e covariância calibrada continuam OPEN.

E7 é obra deste autor e precisa do fechamento independente de Russell. A v3 corrigiu F1/F2 e passou 46 testes do autor, mas isso não é aprovação independente. O principal autorizou o montador a rehashar explicitamente a guarda final antes de E2, conservando a proveniência do fragmento v3 e a revisão correspondente. O pin do fragmento v3 tornou-se histórico durante as alterações concorrentes; não declarar que coincide automaticamente com a guarda final. Não alterar registro publicado para fazê-lo passar. Não foi necessário emitir fragmento v3.1: integração final permanece do principal.

Nenhum arquivo anterior foi sobrescrito; nenhuma rede, posterior real, strain, PE, waveform ou MC. Nenhuma leitura C1 foi escolhida por este revisor. NOT_FALSIFIED não significa CONFIRMED.

## Pins das fontes do fechamento

| Fonte relativa a ORDEM_013_RINGDOWN | SHA256 |
|---|---|
| bis/e2_code/blinding.py | `7d4407fde07c66929651b017501873ecd4bd69ca80fd3e6cd03eaf8e653c6bc5` |
| bis/e2_code/fetch_registered.py | `a6066c933d29f13fea6a786dac8d9c6c2ecd4496bc0ff2c6d36a543e798132cb` |
| bis/e2_code/injection_design.py | `12017563c123df76b856ddedecf9166ddc4c25fe26a5c8b773bc82086b6c842d` |
| bis/e2_code/null_campaign.py | `9fa748e79ba55312543220542f4e470b8759360cd30040ae7fc1f35bf7859785` |
| bis/e2_code/null_runner.py | `1b6bf00beced255d45ac642de5209d32440e486f8a3af469e92a47c58fe1c561` |
| bis/e2_code/pe_runner.py | `6712610a0392abe629b6ea5b5f4fa5a45b2c8b9a3dfb123c952513f18cef68fa` |
| bis/e2_code/pseob_source.py | `21f619e45ae01883a9ee1c23a29f21e8cce9881545d1d6c9b367d530f24d17ef` |
| bis/e2_code/registration_guard.py | `9576db51615627c1264ef51ba228c47a12f162c6c62f68b939306135e1ae3743` |
| bis/e2_code/remnant_conversion.py | `87604de5c8fa7139cd6aa4d0c4fde09476105769735e44d476f3b9a55aa11bc1` |
| bis/e2_code/route_iv_null.py | `dfcf9491ab98f9d32aae119177f53a3622289593c19c528e50cd091ebd7000cd` |
| bis/e2_code/run_controlled.py | `7b5dd6484014942ee5fdd9fc3e529eaf05f9dffe463f35cdd10a01bdcf86334d` |
| bis/e2_code/strain_io.py | `a52faf32e88088320c57d303987a31ec2b9b59c93e162923d603c2c96b21a5b6` |
| bis/e2_code/synthetic_null.py | `be0fa6d4b678993edcbc7dec15f311950c51e466020dc99c5d0f043763eb65f1` |
| bis/e2_code/temporal_contract.py | `c8f4ecbc28d4312e3885d61c14f174062c6055eee0bbd54897e725a18240b605` |
| bis/E2_DESIGN_DRAFT_003.json | `8764abbabffb05987c4afe3b7cb31e2ab4a172c8c1aea697c9b6bbf560287e0c` |
