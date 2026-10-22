# Adendo: revisão do delta BG-01/BG-02, manifesto revisão2

[REAL — revisão estática delimitada] Os dois achados da revisão original estão resolvidos neste candidato. Não encontrei defeito material remanescente nesse delta. O pacote está tecnicamente apto à decisão da ROOT sobre o piloto de cinco pontos teóricos × duas precisões. Este aceite não é execução nem autorização por si, não qualifica todo o prior e não aprova ciência observada.

Mapa consultado antes: seq467; antecedente da revisão: seq462. Request f132a1d5-7477-405d-963b-b1659db63328. O snapshot original desta revisão permanece intacto; este adendo e seu manifesto são independentes.

## BG-01: admissão antes do solver

A nova execute_worker_once reserva primeiro uma identidade lógica por request_id + SHA256 do protocolo + ponto + perfil. O caminho da saída não entra nessa chave: trocar o nome da saída não cria outra tentativa. O hash do motor é registrado, mas não entra na identidade; um reparo do código com o mesmo protocolo também não libera repetição.

A abertura exclusiva x do claim é a decisão atômica de admissão. O arquivo é escrito, flush e fsync ocorrem antes da chamada ao solver. Em seguida há reserva exclusiva do caminho de saída, também flush/fsync, e nova checagem de arquivo final/parcial antes da chamada. Assim, tentativas distintas não concorrem pela mesma saída; a mesma tentativa com outro caminho continua recusada.

O claim lógico permanece em sucesso, exceção, interrupção e gravação parcial. O tratador BaseException registra o terminal de falha quando possível; morte abrupta pode impedir esse terminal, mas o claim preexistente continua bloqueando. Não há exclusão automática nem leitura obrigatória de JSON íntegro para detectar um claim parcial. Um claim sem terminal é incerteza; não é permissão de retry. O branch CLI --worker agora chama execute_worker_once.

[REAL — diferença de fonte] Pela comparação AST, somente main mudou entre as funções existentes e execute_worker_once foi acrescentada. prediction_worker, compare, run_controls, validação física, limites e fórmulas permaneceram iguais. O protocolo também mantém seus bytes. Nenhuma extensão do lote foi introduzida.

## Controles simulados e unidade real

[REAL — conferência do recibo e dos artefatos existentes] VALIDACAO_WORKER_CLAIM.json contém13 controles distintos aprovados e3 chamadas stand-in, zero CAMB. O script redireciona HERE para subpastas de fixture e injeta funções falsas; a fixture CLI substitui prediction_worker por fake. As duas saídas simuladas bem-sucedidas estão marcadas TEST_STAND_IN_NOT_SCIENCE. Claims, terminais e hashes de saída conferem; a falha simulada deixa terminal e o caso incerto deixa claim truncado.

Esses controles não reservam a unidade cosmológica real: suas chaves vivem em worker_claims sob cada fixture. No diretório real do candidato, worker_claims e theory_controls_01 estavam ausentes durante esta leitura. Isso separa os testes de admissão de uma execução científica. Nenhum dos13 controles foi repetido nesta revisão.

## BG-02: ambiente Windows

A errata foi acrescentada ao lado do texto original. Ela limita a ausência de módulos ao subprocesso sandbox/token consultado e cita o recibo normal-user com Python3.14.3 em C:/Python314/python.exe e NumPy2.4.3. Não infere disponibilidade ou ausência de SciPy/CAMB nesse outro ambiente e distingue WSL. O hash citado do preflight262 confere. Não houve nova sondagem, instalação ou execução do preflight.

## Custódia e alcance

[REAL] Os25 arquivos do novo manifesto conferem; FINAL_CHECK_WORKER_FIX e VALIDACAO_WORKER_CLAIM apontam para o hash medido do motor atual. O backup do manifesto anterior corresponde ao previous_manifest_sha256. Os backups de bytes do motor e da nota correspondem ao snapshot inicialmente revisado. A nota, recibo, mapa e manifesto anteriores da revisão independente foram preservados.

O recibo deste adendo traz todos os hashes atuais, os pins dos backups e das fixtures. A revisão anterior continua válida quanto ao prior, escalas, BBN/neutrinos/recombinação e limites. O único encaminhamento aqui é a decisão delimitada da ROOT para cinco pontos × duas precisões teóricas, com os limites já fixados e sem retry. Não executamos solver, import CAMB, centros, S/g, likelihood, ajuste, H0, lnB ou novo composto.
