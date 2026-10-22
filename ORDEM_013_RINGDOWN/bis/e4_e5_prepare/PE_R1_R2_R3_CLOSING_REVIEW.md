# Fechamento independente PE-R1 / PE-R2 / PE-R3

Data UTC: 2026-09-22T21:06:04.425614+00:00. Escopo: mudanças atuais, controles finitos e fotografia completa de `bis/e2_code`. Parecer novo; `PE_INDEPENDENT_REVIEW.md` e suas evidências permanecem intactos.

**[REAL — código e mocks] R1, R2 e R3 fechados no escopo abaixo. Nenhum bloqueante residual desses três achados na calibração preparada com os 15 parâmetros livres. Não constitui registro E2, autorização de execução ou certificação física.**

## R1 — contrato temporal das duas famílias: FECHADO

`aligned_gr_xphm` recebe `geocent_time` explicitamente e chama `validate_time_contract` antes da função geradora. `pseob_frequency_domain` delega ao mesmo helper, incluindo dtau220/440. A construção da injeção passa `analysis_time_contract` para ambas. A reserva ±0,022s é aplicada nos dois lados da janela sem taper; a cauda usa `max(1,1+dtau220,1+dtau440)`. A violação aborta visivelmente, sem transformar janela inadequada em rejeição silenciosa de prior.

Nos mocks independentes, ambas as famílias aceitam o caso interior e recusam os casos esquerdo/direito antes de qualquer chamada ao gerador de polarizações. Incluí um caso que falharia somente com a reserva de 22ms, a ampliação de cauda pSEOB e limites escalares negativos/NaN/inf. Com os limites artificiais inspiral=1s, merger=0,1s, cauda=0,2s, start=100s, duração=8s, rolloff=0,2s e chegada=103s, margens independentes são 1,678s e 4,578s.

[OPEN] Esses limites genéricos não certificam suporte de nenhuma família nem vazamento FFT. Não se inferiu suficiência física em todo o prior ou igualdade entre famílias. `SHARED_TEMPORAL_REPLAY.json` teve procedência conferida: 32 decisões, todas coerentes com o esperado; aceitações por duração {"8.0": 8, "16.0": 16}. Esse replay reutiliza limites previamente medidos pelo agente autorizado A; não mede waveform e não foi apresentado como execução independente nova desses limites. A janela16s é INPUT de configuração, condicionada a registro; os16 pontos registrados não cobrem interior ou todos os vértices introduzidos por q.

## R2 — verdade injetada versus suporte de recuperação: FECHADO

`validate_truth_support` exige os 15 campos físicos/deformações, prior completo com mass_ratio, nenhum campo inesperado e coerência do q explícito com m2/m1. Confere limites finitos de cada verdade, constraint de q e ordenação de massas. A chamada aparece antes de construir o gerador e novamente depois de reescalar a distância. O teste não altera os priors para acomodar uma injeção.

Para cada família, os testes tentam valor inferior, superior e NaN em cada um dos15 campos, ausência de cada campo, q abaixo/acima, q explícito inconsistente/NaN e campo estranho. Todos recusam antes da geração. Distâncias reescaladas para fora do suporte recusam antes de adicionar sinal aos interferômetros. Mutações sintéticas feitas somente após o retorno do gerador em cada um dos15 campos também recusam antes da injeção, exercitando a segunda guarda.

[ESCOPO] O fechamento refere-se ao contrato integralmente livre avaliado. Não certifica variantes de recuperação com priors de deformação fixos numéricos: a função de suporte atual espera descritores de prior, e tais variantes precisam de contrato próprio antes de uso. A pertinência ao suporte não demonstra cobertura estatística, eficiência de seleção ou calibração física.

## R3 — chamadas reais da likelihood: FECHADO

O runner envolve somente a fronteira `log_likelihood_ratio`. O método completo instalado de Bilby foi lido por AST de arquivo conferido contra o manifesto pinado; ele chama a razão uma vez e soma a likelihood de ruído. Não importei o corpo científico dessa classe. O corpo da razão e o ruído foram substituídos por funções finitas: chamada direta e completa preservam valores, chamada apenas de ruído não incrementa o contador, exceção antes do gerador e `KeyboardInterrupt` são contadas e propagadas.

O ensaio independente com dois processos fork resultou em **26 entradas, 24 retornos e 2 exceções**. Não houve contagem dupla. A soma de tempos é parede por invocação, acumulada entre processos; não é CPU total nem parede da tarefa. Verificadas também as resoluções ativas de astropy/pandas contra os hashes do runtime. O teste A de17 entradas/16 retornos/1exceção é evidência separada, com seus pins conferidos.

Por leitura do runner, o contador é criado antes da likelihood; snapshots cumulativos existem antes/depois do construtor do sampler e depois de `run_sampler`. `likelihood_calls`, `sampler_ncall` e `source_calls` são publicados separadamente. Exceções usuais levam o snapshot ao recibo de falha. A atualização de parede/CPU depois do remanescente, já revisada, continua presente. As cinco funções exercidas pelo toy anterior (`sampler_class`, `terminal_state`, `convergence`, `posterior_columns`, `validate_config`) permanecem AST-idênticas à fotografia desse toy; o sampler não foi reexecutado nesta revisão.

[ESCOPO] `maxcall` permanece limite nominal por iteração/lote de Dynesty, sujeito a ultrapassagem; não virou teto exato de chamadas globais. Retorno da fronteira contado como completed pode ser recusa numérica, não necessariamente avaliação física válida. O contador de fonte só conta a função LAL efetivamente chamada. Interrupção forçada pode impedir o recibo final; o wrapper contar uma BaseException não prova que o `except Exception` do main publicará recibo para ela. Nenhuma promessa de durabilidade após kill.

## Controles, preservação e pin

- Bundled Python `-B -O`: 210 verificações, 186 recusas esperadas; parede 0.367134s, CPU do processo 0.109375s.
- WSL `/opt/lal_env/bin/python -B -O`, modo `--installed`: 216 verificações, 186 recusas esperadas; parede 0.445529s, CPU do pai 0.135781s. Os controles comuns foram repetidos, não somados como casos distintos.
- Zero waveform física, PE, leitura de strain, campanha ou importação de main produtor. Vetores de polarização artificiais e funções escalares falsas somente.
- Os14 fontes foram parseados e seus bytes conferidos antes/depois dos controles. A fotografia de14 é inventário de integridade; não é nova revisão científica dos módulos de nulo/download fora destes achados.
- Nenhum artefato produtor ou parecer anterior foi alterado. Somente fixtures e este fechamento na pasta de ownership. Execuções anteriores de A/principal são do agente autorizado, não do humano.

Evidências: `pe_closing_002/closing_finite.py`, `INDEPENDENT_FINITE.json`, `INDEPENDENT_INSTALLED_FINITE.json`, `snapshot/` e `CLOSING_RECEIPT.json`. SHA256 do recibo consolidado: `2b50a9406556554dc163078f79513fb12ca06ad04cac0aa06cecdd0ad0374b92`. Todos os fixtures Python novos estão prontos. A fotografia recursiva de `e4_e5_prepare/**/*.py` contém 66 arquivos e está no recibo; o principal deve recomputar o mapa no freeze. Não há novo Python ou edição Python pendente deste revisor. Após aviso de freeze, somente MD/JSON.

## Fotografia dos14 fontes atuais

| Fonte | SHA256 lido dos bytes |
|---|---|
| blinding.py | `7d4407fde07c66929651b017501873ecd4bd69ca80fd3e6cd03eaf8e653c6bc5` |
| fetch_registered.py | `a6066c933d29f13fea6a786dac8d9c6c2ecd4496bc0ff2c6d36a543e798132cb` |
| injection_design.py | `12017563c123df76b856ddedecf9166ddc4c25fe26a5c8b773bc82086b6c842d` |
| null_campaign.py | `9fa748e79ba55312543220542f4e470b8759360cd30040ae7fc1f35bf7859785` |
| null_runner.py | `1b6bf00beced255d45ac642de5209d32440e486f8a3af469e92a47c58fe1c561` |
| pe_runner.py | `6712610a0392abe629b6ea5b5f4fa5a45b2c8b9a3dfb123c952513f18cef68fa` |
| pseob_source.py | `2c9a053177bd2671da1879f60343434b3605b3274994b42d68aa50cd68f4ff2f` |
| registration_guard.py | `9576db51615627c1264ef51ba228c47a12f162c6c62f68b939306135e1ae3743` |
| remnant_conversion.py | `87604de5c8fa7139cd6aa4d0c4fde09476105769735e44d476f3b9a55aa11bc1` |
| route_iv_null.py | `dfcf9491ab98f9d32aae119177f53a3622289593c19c528e50cd091ebd7000cd` |
| run_controlled.py | `7b5dd6484014942ee5fdd9fc3e529eaf05f9dffe463f35cdd10a01bdcf86334d` |
| strain_io.py | `a52faf32e88088320c57d303987a31ec2b9b59c93e162923d603c2c96b21a5b6` |
| synthetic_null.py | `be0fa6d4b678993edcbc7dec15f311950c51e466020dc99c5d0f043763eb65f1` |
| temporal_contract.py | `c8f4ecbc28d4312e3885d61c14f174062c6055eee0bbd54897e725a18240b605` |

**Disposição:** R1–R3 deixam de bloquear pelo defeito de implementação descrito nos pareceres anteriores. Permanecem [OPEN] adequação física da janela e do modelo, convergência/cobertura de PE real, calibração de duas famílias e seus gates estatísticos. E4/E5 continua preparado, sem execução. Não transportar este fechamento finito para uma alegação de likelihood populacional calibrada ou suporte FFT certificado.
