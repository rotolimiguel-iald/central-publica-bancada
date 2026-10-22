# Delta estático V2 do instrumento racional

TI-01: recibo FROZEN_DOMAIN_FAMILY obrigatório em tail e agregação. Payload expõe toda a lista ordenada, test/null, família/modelo/algoritmo; o verificador externo confere essa representação contra o manifesto congelado. O pin científico não é redefinido. Fixture sintético aceita só domínios exatos conhecidos; truncamento com mesmo pin, alteração de ordem e ausência de recibo de família são novos negativos N08.

TI-02: finalização pura com callbacks injetados. Sucesso dos controles gera apenas evidência provisória. O consumidor deve exigir exit0 externo após duas checagens do deadline (persistência+leitura+hash e output+flush), além dos pins e ausência de invalidação. Não há I/O depois da última checagem no caminho que retorna0. Falha tardia/erro de I/O emite ou tenta emitir FINALIZATION_FAILURE e sai não zero. N09 prepara seis cenários de doubles; não executados. Não se promete tempo real do OS.

TI-03: opção mínima documental adotada. communicate conserva cap de aceitação pós-coleta, explicitamente sem limitação de retenção de memória. O worker continua o mesmo processo local fixo, sem produtor arbitrário ou nova execução.

Mesma request_id e zero tentativas. Fórmulas d>0, raiz inteira, guardad0, N/Q, input512/scratch524288, T01–T08, modelo/alpha/família/Bonf5 científicos permanecem. A interface de família ganhou a ligação documental que faltava; não ganhou certificado físico. Pasta507, proposta498/502, parecer510 e memórias não foram alterados. Apenas arquivos novos/V2, backups de bytes e AST/pins; nenhum módulo importado, caso executado ou autorização/CLAIM criado.
