# F8.2.NU2 — revisão independente R1

Autor: Codex / nu2_skeptic. Revisão sob a reivindicação 618, 09/10/2026. Esta é verificação independente do cálculo condicional; não é auditoria da gerência nem resultado empírico.

## Veredito

**PASS COM LIMITES DE ESCOPO.** Não encontrei defeito material nas contas espectrais propostas. A reprodução com Decimal de 95 dígitos confirma a escala, a textura e o perfilamento. Não obtivemos significância observada, funcional massa–luminosidade ou previsão de poder para o JUNO real.

## Reprodução independente

O script `independent_decimal_r1.py` não importa o construtor e não executa originais. Lê apenas a constante alfa por atribuição única. Usa pi pela fórmula de Machin, cosseno por série e matrizes de rotação multiplicadas, numa implementação diferente da original. O exponencial é avaliado a 95 dígitos antes de subtrair 1, enquanto o construtor usa `expm1` em float64. Ambos conservam o sinal de ordem 10^-39, que desapareceria na subtração ingênua de duas probabilidades float64.

- [DERIVED, referência condicional] max |deltaP| = 1,7880671599537156 × 10^-39.
- [DERIVED, experimento ideal definido] N não oscilado para separação local nominal de 5 sigma, com normalização perfilada = 8,632408517596056 × 10^79. Diferença relativa contra o construtor = 1,20 × 10^-14.
- [DERIVED] Gamma21:Gamma31:Gamma32 = 1:1111,111111…:1045,444444… para as diferenças de massa declaradas.
- [DERIVED] A matriz PMNS de deltaCP=0 é ortogonal à precisão da avaliação. Uma densidade diagonal na mesma base de massa permanece exatamente inalterada pelo canal, para qualquer força não negativa.
- [DERIVED] Gamma=(beta tau/2)omega^2 tem unidade s^-1; omega=Delta m^2/(2 E hbar). O argumento Gamma L/c é adimensional. `tau=tP` e `Kfac=1` são hipóteses do exemplo.

Para as contagens ideais lambda0=N w P0 e delta lambda=N w deltaP, a informação local é N sum(w deltaP^2/P0). Com normalização livre, projeta-se deltaP em deltaP-P0<deltaP>/<P0>. Esse é o perfilamento usado. A grade de 121 pontos com peso igual é uma definição sintética, sem pretensão de integrar o espectro real.

## Reconciliação de fonte

Li diretamente `A Ponte Einstein Cartan Miguel.tex`, linhas 1367–1371: o coeficiente de desfasamento beta é independente de omega, sem corrida logarítmica. Portanto a derivada beta(E) da resposta anterior não é predição vigente dessa lei. O plano complementar já a marca corretamente como extensão contrafactual. O inventário v388 distingue a constante da fronteira beta0 da leitura de bulk; a identificação física chi(E) segue aberta.

A cota beta<=sqrt(e) é matemática abstrata. O contrato físico `couplingOfAlpha` exige beta<1. O construtor não apresenta sqrt(e) como acoplamento físico instalado, e mantém tau e Kfac fixos ao calcular a razão abstrata.

A identidade de inclinação completa, para Gamma proporcional a tau beta r^beta E^-2, é:

n_eff = -2 + d ln(tau)/d ln(E) + beta'/beta + beta' ln(r) + beta d ln(r)/d ln(E).

Ela foi reproduzida independentemente por diferenças de 10^-20 em log E. Não se pode omitir os termos de r ou tau quando variarem; tampouco inferir tais dependências dos nomes dos fatores.

## Limites físicos que devem acompanhar a entrega

1. Não há transferência direta do limite JUNO da textura gamma21=gamma31, gamma32=0 para a textura calculada. Igualar apenas o expoente n=-2 é insuficiente.
2. A estacionariedade só vale quando a densidade já é diagonal na mesma base do dissipador. Não demonstra ausência de efeitos de produção, colisões ou propagação em matéria.
3. Complete positivity vem do duplo comutador com gerador hermitiano e coeficiente não negativo: o canal é média gaussiana de evoluções unitárias. Os exemplos numéricos confirmam casos; não substituem essa condição.
4. O número enorme de exposições é consequência das hipóteses tau=tP, Kfac=1, vácuo e parâmetros conhecidos. Não é um limite universal para toda extensão da TGL e não pode receber o rótulo de previsão JUNO.
5. Disponibilidade pública de limites, gráficos ou mapas no espaço usual não equivale a likelihood no novo parâmetro. A nota de dados corretamente distingue esses objetos. As verificações web do agente de fontes não foram repetidas por este revisor.
6. A Bancada foi consultada pelo construtor e o recibo identifica um canal de proveniência somente leitura, SEM_LIMITE_TGL. Esse retorno não comprova execução de likelihood física. Não inspecionei o processo MCP por conta própria.
7. Esta revisão não constrói a ligação entre dissipador e taxas fracas/EOS, nem um funcional massa–luminosidade. Ela também não prevê uma nova perda energética a partir de desfasamento que conserva energia.

## Custódia

Os hashes e os valores completos estão em `INDEPENDENT_DECIMAL_R1.json` e `REVIEW_RECEIPT_R1.json`. Escrita nova, modo x. Nenhuma memória, original, quadro, Bancada, kernel ou gate foi alterado pelo revisor. O relatório principal da coordenação ainda não existia ao iniciar esta revisão; o parecer cobre planos, script, resultado e inventários enumerados no recibo.
