# Delta WSL V2 — captura íntegra e retenção limitada

**PREPARATION_ONLY_NOT_AUTHORIZED_NOT_EXECUTED.** Mesmo request ainda não consumido `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf`; mesmo caso `WSL_CACHE_LATCH_001`. Pacote separado em `guard_wsl_integration_preparation_v2`. O snapshot514 e o parecer519 permanecem byte a byte intactos. Nenhuma autorização, CLAIM, WSL, candidato importado/executado, hook, journal ou controle criado nesta unidade.

## Fontes e alternativas

Lidos o parecer `revisao_guard_wsl_estatica/PARECER_REVISAO_WSL.md` e seu manifesto; quatro pins da revisão conferidos. O P2 WSL-01 identifica que a thread de stderr pode morrer por erro sem sinalizá-lo ao aceite; o P3 WSL-02 identifica até4096 bytes lógicos transitórios a mais no buffer Linux. São achados estáticos, não falhas reproduzidas por execução.

| Recorte | Alternativa escolhida | Alternativa descartada |
|---|---|---|
| WSL-01 | Manter a captura existente e acrescentar estado de erro/EOF por fluxo, exigido em wait/join e registrado no recibo | Trocar o transporte/threading inteiro por outra infraestrutura; delta maior sem necessidade para o achado |
| WSL-02 | Recortar o chunk ao espaço restante antes de append e continuar recusando overflow | Aumentar/documentar limite maior; mudaria o teto congelado de32768 sem necessidade |

## Alteração WSL-01

`Capture.read` registra exceção por fluxo (`type`, `message`) e só marca EOF quando lê exatamente `b""`. A morte da thread já não basta. `wait` consulta erros durante a espera e após join; `join` exige ausência de erro, todas as threads terminadas, EOF normal dos dois fluxos e ausência de overflow. Os dois snapshots de captura, principal e limpeza, entram no recibo final, inclusive no caminho de falha.

[DERIVED do fluxo] Um erro de leitura de stderr deixa seu EOF falso e seu erro registrado; ele é rejeitado mesmo com stdout completo e subprocesso0. A limpeza já prevista permanece no finally e a unidade termina nãozero. Se a captura permanecer incompleta/incerta, não se promove o buffer vazio a captura íntegra. O rótulo conservador herdado de falha/estado incerto não é prova de órfão físico: os recibos de limpeza e captura preservam seus papéis separados.

## Alteração WSL-02

Linux calcula `room = 32768 - len(buffer)`, acrescenta somente `chunk[:room]` e recusa `len(chunk) > room`. Assim a quantidade lógica retida no buffer não ultrapassa32768 antes da recusa. O chunk lido continua podendo ter4096 bytes temporários; não se promete limite igual para RSS, capacidade interna do bytearray, buffers do sistema ou memória total.

## Preservação e diretório separado

As quatro fontes adaptam seus caminhos fixos Windows/Linux para a pasta V2. Fora disso, `common.py` e `worker.py` são idênticos à preparação514. Guard original/cópia idênticos. Nenhum novo caso/campanha, parâmetro científico ou limite foi introduzido. Request/caso, STOP/gate/flock, PID/nonce/pidfd, sinal restrito, claims prévios,60 s nominais, checks pós-recibo/pós-stdout, ausência de replay e exigência de exit final foram preservados. O main Windows só ganhou a chave de recibo `capture_state`; isso foi comparado por AST.

A V2 tem seu próprio contrato por hash e comando proposto, ambos não executados. A coordenação deverá nomear especificamente esse contrato em eventual revisão/decisão. A pasta514 segue histórica, sem autorização/CLAIM; não se autoriza o snapshot com defeito nem duas execuções do mesmo request pela existência de duas pastas. Qualquer consumo incerto/terminal desse request impede nova tentativa.

## Recibo e limites

[REAL documental/estático]80 conferências registradas: AST, delta delimitado, invariantes de contrato, funções preservadas, seis pins V2,23 pins do snapshot514, quatro da revisão519 e ausência de consumo nas duas pastas. Não são80 testes comportamentais: nenhum candidato/stub/controle foi executado, nenhuma campanha adicional foi criada. Os14 pins Linux do contrato foram preservados do recibo admitido; não houve nova leitura UNC ou inicialização WSL.

O pacote mantém o alcance stdlib: SourceFileLoader real, cache sintético, journal físico e checkpoint de callback trivial. Dinâmica V2 permanece [OPEN] até revisão independente e decisão específica de ROOT. Nada autoriza LAL/numpy/bilby, source/driver científico, waveform/likelihood/sampler, PE/D ou reabertura INIT003. Prazos continuam nominais/cooperativos, sem garantia absoluta de SO; o aceite requer recibo físico, captura completa, exitcode final e observação externa do encerramento.
