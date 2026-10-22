# Revisão independente estática do controle WSL

**Parecer: corrigir WSL-01 antes de consumir a unidade.** Há um P2 de propagação de erro da captura Windows e um P3 de precisão do teto de retenção Linux. Não localizei outro bloqueador no recorte lido. Isso é uma revisão do código, não uma execução, uma autorização ROOT ou qualificação do runtime WSL.

[REAL documental] Mapa consultado antes, rota `ringdown.ramo_b_preregistro_v386`, preparação514. Request `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf`. Fontes principais `common.py`, `linux_control.py` e `launch_windows.py` lidas integralmente, além de worker, guard, contrato, manifesto e recibos. Nenhum arquivo do pacote foi alterado.

## WSL-01 — P2: erro da thread leitora pode terminar em PASS

`launch_windows.py:18–26` não guarda exceções de `stream.read(4096)`. O `join` só informa que as threads terminaram; não distingue EOF normal de erro. `wait`, linhas34–41, verifica overflow e término, mas não uma falha de leitura. O caminho principal aceita stderr vazio em60 e75, e pode manter `PASS_WSL_STDLIB_INTEGRATION_ONCE` e retornar0 em104.

[DERIVED] Um caminho concreto é: a thread de stderr lança OSError antes de guardar bytes; a captura stdout recebe o JSON completo e o subprocesso termina0; o leitor de stderr morreu, logo `join` retorna verdadeiro. As verificações de JSON físico, identidade e stdout podem passar; o buffer stderr vazio satisfaz a condição atual, embora a captura de stderr seja desconhecida. A mesma falta vale para a captura do helper de limpeza. O traceback padrão da thread aparece no stderr do launcher, não no buffer do filho que `main` examina. A inspeção externa pode detectá-lo, mas o status/exit0 do próprio launcher não são invalidados por esse erro. Não foi executado nenhum stub ou processo para demonstrar isso: a conclusão vem do fluxo lido.

Recomendação mínima A: estado de erro e de EOF por fluxo; leitor registra exceção e `wait/join` exigem término normal por EOF dos dois fluxos, sem erro e sem overflow. A falha deve manter a limpeza autorizada e terminar nãozero. Alternativa B seria substituir o mecanismo de captura por outro transporte de erros explícito, com delta maior; não parece necessário. Nenhuma alteração de caso, identidade, prazo60, ciência ou autorização se segue desse reparo.

## WSL-02 — P3: retenção Linux excede32KiB antes da falha

`linux_control.py:37–40` lê até4096 bytes, acrescenta tudo ao buffer e só então verifica `len<=32768`. [DERIVED] Com32768 já retidos, o próximo chunk pode elevar o tamanho lógico a36864 antes da exceção. O buffer permanece limitado e overflow é falha, portanto não é risco de coleta ilimitada; a afirmação exata de32KiB por fluxo no contrato e nota está maior que a garantia do código por até4KiB. Isso não é medição da capacidade interna do bytearray ou da memória RSS.

A correção mínima preserva o contrato: calcular espaço restante, reter somente essa parte e recusar o excesso. A captura Windows já usa recorte antes de append (`raw[:room]`). Alternativamente pode-se declarar com precisão a margem Linux, se ROOT deliberar, sem chamá-la de32KiB.

## Aspectos conferidos no recorte

- Identidade: autorização específica e contrato/revisão por hash; claims exclusivos, fsync e readback antes de WSL/filho/caso. IDs/nonce/argv/exe são confrontados. Parent start_ticks liga a encarnação no worker. Registro de boot_id é evidência adicional; não o tratei como comparação presente em toda função.
- Sinal: `exact_signal` abre pidfd antes da leitura de identidade e usa esse descritor no SIGKILL; não há sinal por PID solto, grupo amplo ou término da distribuição. Se o PID examinado desaparecer/trocar, o pidfd não passa a apontar ao novo processo. A identificação por argv inclui request/nonce e exe exatos. Não é confinamento contra processo hostil deliberadamente imitando a unidade.
- Fence: STOP é persistido antes da limpeza. Supervisor segura o mesmo flock entre checagem STOP e Popen; limpeza inspeciona sob esse gate. Um supervisor atrasado deve recusar lançar filho ao encontrar STOP. A ausência afirmada continua restrita às identidades vivas inspecionadas, sem ausência absoluta do SO. PermissionError em processo de mesmo UID torna a limpeza incerta.
- Consumo: entrada Windows bloqueia CLAIM/RUN/RESULT existentes; claims Linux e caso são exclusivos. Um único Popen de controle Linux; o helper separado executa zero controles. Nenhum caminho de retry/resume foi encontrado. Captura parcial/incerta não autoriza repetir.
- Prazo: clocks começam após import time e antes dos demais imports/pré-validação. Windows inclui partidaWSL e limpeza no nominal60; supervisor15, trabalho9 e helper12 são limites cooperativos. As três saídas verificam relógio depois da persistência física e depois de stdout/flush antes do retorno0. Uma falha tardia pode deixar JSON provisoriamente PASS no disco, mas exit nãozero invalida o aceite pelo contrato. Não exigi deadline absoluto de SO nem prova que um PASS rápido cobre os caminhos de timeout.
- Recibos: Linux cruza stdout/arquivo físico, retorno0, identidade, journal, latch e callback0; Windows exige retorno0 Linux e cleanup sem alvos sinalizados no caminho de sucesso. Ressalva WSL-01 acima impede aceitar captura íntegra só porque o leitor terminou.
- Escopo: a cópia do guard é idêntica aos bytes da fonte nomeada. Worker usa uma fixture `VALUE = 42` e um caso. Não há import científico declarado nos cinco ASTs lidos. A presença estática dessas proteções não comprova seu efeito no runtime não executado.

## Custódia e limite da revisão

[REAL] O auditor estático próprio registrou94 observações/conferências:23 entradas do manifesto,6 pins locais do contrato,3 binários Windows,14 correspondências documentais Linux, fonte/cópia do guard, AST/imports e condições estruturais. Os pins locais/Windows foram relidos. Os14 pins Linux foram confrontados com o recibo já admitido; esta revisão não reabriu UNC nem iniciou WSL para medi-los novamente. A contagem não representa94 testes comportamentais aprovados: inclui constatação estrutural dos próprios achados.

Zero candidato importado/executado, WSL, hook, journal instanciado, dadoD, PE, waveform, likelihood, sampler, rede ou provedor. Nenhum CLAIM/autorização criado. O recibo e manifesto desta revisão não concedem permissão de execução. O snapshot514 continua íntegro; um eventual delta deve ser separado/preservar backups e submetido à decisão ROOT. Não repetir unidades consumidas Windows/INIT003.
