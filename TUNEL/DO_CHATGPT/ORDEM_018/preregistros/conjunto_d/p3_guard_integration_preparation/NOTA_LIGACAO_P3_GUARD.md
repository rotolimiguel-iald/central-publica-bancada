# P3 — ligação do guard já preparado e mínimo restante

[REAL — leitura, AST e hashes] **A instrumentação necessária já existe; não é preciso escrever outro driver, guard ou validador.** Os cinco módulos candidatos foram preservados. Esta entrega contém somente comparação pinada e contrato documental da ligação. Não é pacote executável, novo job científico nem autorização.

Identidade documental: 51134140-83b5-4f56-b83a-aa7702c82f92, persistida antes dos artefatos. Mapa consultado; início seq617. As63 conferências documentais passaram:26membros da preparação,3membros da revisão anterior,9originais de referência,12dependências locais e verificações da ligação/recibos. COMPARACAO_PINADA.json registra os hashes lidos e as distinções de evidência.

## O que já está ligado

| Peça existente | Ligação observada na fonte | Alcance |
|---|---|---|
| candidate/audit_guard.py | latch anterior à escrita, journal pré-aberto, checkpoints e snapshot sem reset | Guard de4.142bytes, SHA256 ba7e8870e5935ce420013a5a123152bf2f99acc637dc33a139e9b776092f0d8c |
| candidate/driver_p3.py:87–109 | instancia o guard e liga source.set_audit_checkpoint antes de instalar o hook | Recusa absorvida não limpa o latch |
| candidate/driver_p3.py:153–162 | checkpoint pré, budget e guard.evaluate envolvendo likelihood e conversão numérica | O retorno sujo é descartado; exceção permanece rastreável |
| candidate/src/pseob_source.py:87–133 | checkpoints após imports, antes do helper temporal/dicionário/waveform e após a tentativa | Não promete interromper C em curso; contador é de waveform principal concluída |
| candidate/driver_p3.py:195–235 | checkpoints finais, prioridade AUDIT_VIOLATION, journal/hash e saída de falha | Resultado parcial não encobre recusa |
| candidate/launch_p3.py:49–76 e result_acceptance.py | relê journal físico, confere identidade/limites/checkpoints, interrompe antes do próximo filho e propaga saída nãozero | Parcial limpo continua parcial, sem convergência/cobertura inferida |

O adapter inalterado importa de **pseob_source**, o mesmo nome usado por import pseob_source as source no driver; synthetic_only220 chama a função assim importada e generator a fornece ao WaveformGenerator. Não há, na fonte examinada, outra identidade src.pseob_source que recebesse callback diferente. A identidade real do objeto carregado permanece obrigação da futura montagem; AST não observa sys.modules em execução.

[REAL documental] O guard do candidato, de guard_stdlib_integration_preparation/sources e de guard_wsl_corrected_transport_preparation/sources é idêntico byte a byte. O recibo WSL vincula exatamente esse hash. O validador permanece o módulo submetido aos21doubles. Não foi encontrado delta de guard posterior que precisasse ser transplantado para o P3.

## O que foi qualificado, sem repetir

Os recibos ROOT registram21doubles aprovados uma vez, três casos stdlib Windows aprovados uma vez e a unidade WSL corrigida aprovada uma vez. A primeira camada cobre lógica do latch/aceitação com doubles; as duas últimas exercitam hook/importador/journal reais nos respectivos runtimes stdlib. O WSL observou recusa esperada de cache absorvida pelo importador, latch persistente e callback0. Isso não qualifica o driver científico inteiro nem LAL, Bilby, Dynesty, waveform, likelihood, convergência ou cobertura.

Esta rodada apenas leu esses recibos e seus vínculos. Não voltou a executar os casos. INIT003 permanece terminal e operacionalmente não qualificado; não é corrigido retroativamente pela disponibilidade do reparo.

## Delta concreto ainda necessário

**Empacotamento:** a pasta candidate é deliberadamente incompleta e os dois main recusam PREPARATION_ONLY. O contrato mínimo lista os cinco módulos reaproveitados e as12dependências locais inalteradas, com fonte e hash. Uma futura montagem isolada deve piná-los na raiz/estrutura que os imports esperam, acrescentar audit_guard.py e result_acceptance.py aos inputs exatos e fixar runtime/identidade dos objetos carregados. A montagem deve usar contrato e identidade científicos novos, sem copiar autorização, CLAIM, saída ou IDs consumidos. Nada disso foi criado aqui.

O snapshot RUNTIME_P3_READONLY.json contém1.162pins históricos. Nesta rodada foi conferido o arquivo documental, não foram relidos os caminhos Linux ou autenticados objetos instalados. As referências ao arquivo ASD default da factory são apenas metadata já pinada; nenhum conteúdo de PSD foi aberto. Não foram lidos NPZ ou arrays sintéticos, D ou dados observados A/B/C.

**Fecho de imports:** source ainda contém imports tardios de lal, lalsimulation e bilby.gw.source, seguidos de checkpoint; temporal_contract é importado depois e também seguido de checkpoint. INIT003 registrou recusas de sondagens de cache de LAL/lalsimulation/helper temporal nesse trecho. O reparo impede que essa recusa vire avaliação aceita. O sucesso stdlib demonstra a parada desse padrão, não que o caminho científico agora ficará limpo.

Duas rotas estão explicitadas no contrato:

- A: manter os imports tardios e a allowlist rigorosa. É o comportamento já preparado; eventual primeira recusa é terminal. Não resolve, por si, a disponibilidade dos imports conhecidos.
- B: preparar uma fase anterior ao hook, explicitamente pinada e registrada, para carregar somente as dependências científicas conhecidas e conferir sua identidade. Isso muda a fronteira auditada e deve constar do próximo contrato. Não é licença para esconder recusas, aceitar cache inteiro ou dispensar o latch depois.

Nenhuma rota foi implementada ou adotada nesta comparação. Não se inferiu recorrência inevitável das mesmas recusas em um processo que não foi iniciado, nem se prometeu fecho transitivo de todo import. O próximo preparo concreto é escolher e pinçar essa ligação de imports junto da montagem, em vez de produzir outro guard ou refazer testes stdlib.

**Qualificação científica da ligação:** permanece separada do empacotamento. Os componentes lógicos já preparados podem ser usados na decisão de ROOT sobre uma unidade futura delimitada que exercite a ligação real. Esta entrega não define uma nova campanha nem seus jobs; não acrescenta um conjunto genérico de controles e não transfere as autorizações consumidas.

## Interface e comando

CONTRATO_MINIMO_LIGACAO.json fixa reuso, dependências, identidade única do módulo source, checkpoints, aceitação externa e as lacunas exatas. Preserva os limites científicos históricos apenas como referência, inclusive1worker/thread,10000avaliações,3600ssoft/3610sda espera inicial; não aumenta teto nem apresenta cleanup/IO como prazo absoluto.

candidate_command é null. Não há comando executável sustentado enquanto main recusa PREPARATION_ONLY e faltam contrato científico/identidade/raiz fechados. A forma documental da CLI é preservada: supervisor recebe SHA do futuro contrato; filho recebe SHA e job ID registrado nesse contrato. Nenhum ID científico, AUTH, CLAIM ou instrução de execução foi emitido.

[REAL] Zero import de candidato/NumPy/nativas, zero WSL, waveform, likelihood, sampler, PE, controle ou modelo remoto; nenhuma alteração de fonte selada, memória compartilhada, fila ou ledger. O número de verificações desta nota é documental; não é nova qualificação científica.
