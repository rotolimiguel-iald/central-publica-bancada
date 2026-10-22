# Alternativas antes de executar

[INPUT/DERIVED — preparação autorizada] A especificação V2 e o aceite503 permitem preparar o instrumento, sem executar seus controles. Esta unidade usa pasta nova e request_id próprio; não reabre6273 nem o snapshot498.

A: aritmética inteira/racional, exponenciação limitada por quadratura, raiz inteira e certificado exato. Selecionada para implementar o envelope racional256 aprovado como especificação. Não usa SF, exp, log ou floats de cauda. Floats ficam restritos ao relógio operacional.

B: aritmética Decimal dirigida com intervalos e arredondamento para fora. Não selecionada: exigiria qualificar contexto e direção de todas as operações, sem vantagem demonstrada nesta unidade. Não será executada como fallback.

C: avaliação intervalar da Chernoff original ou SF exata. Permanece alternativa documental da proposta; não será implementada ou medida aqui.

Limite de confiança: a API exige verificador externo explícito e recibo vinculado ao hash da requisição/registro e às referências de certificados. A interface não prova a semântica física dessas referências. Não há verificador físico instalado neste pacote. Os controles usam registro exato de fixtures sintéticas, rotulado SYNTHETIC_CONTROL_ONLY, não flags de prova científica. Uma futura aplicação física exige implementação/revisão independente desse verificador e seus certificados.

Nesta preparação: somente escrita de código e verificação AST/pins; sem importar o módulo, executar casos, avaliar caudas ou criar CLAIM/autorização.

## Delta estático TI-01/TI-02/TI-03, antes de qualquer medição

TI-01: (A) recibo de domínio/família com lista ordenada e identidades completas; (B) redefinir o pin como hash canônico direto dessa lista. Selecionada A: liga o manifesto integral ao verificador sem redefinir silenciosamente o hash científico já existente.

TI-02: (A) persistir PASS e depois invalidá-lo se o deadline for ultrapassado; (B) manter todo recibo/saída de sucesso provisório e exigir exit0 externo após checar relógio depois de persistência/releitura/hash e de saída com flush. Selecionada B, com invalidação separada nas falhas; não há operação de I/O adicional no caminho que retorna0 depois da última checagem. O OS continua sem garantia de tempo real.

TI-03: (A) descrever communicate honestamente como coleta seguida de caps de aceitação; (B) implementar captura incremental com retenção limitada. Selecionada A para preservar o mecanismo do worker fixo; a limitação de memória NÃO é alegada. Nenhum benchmark/medição motivou esta escolha.
