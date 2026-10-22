# Revisão independente da propagação SN/SBF por erros

[REAL — revisão estática em 06/10/2026 UTC] **Nenhum defeito material encontrado nas fórmulas, na ordem das linhas ou nos rótulos de alcance da entrega congelada.** Aceite técnico restrito à prescrição upstream fixada e à variante SBF explicitamente condicional. Não é adoção física da segunda variante nem fechamento de NS-01.

Foram conferidos qualify_flow_errors.py, FLOW_ERROR_PROTOCOL.json e FLOW_ERROR_RESULT.json, contra o pré-registro do mapa seq454, os metadados de erros e os consumidores upstream já pinados. O verificador independente passou 32/32 verificações de integridade, configuração, ordem e campos. Não executou NumPy, o programa qualificador ou upstream; não repetiu autovalores, inversas ou propagação numérica. Os três artefatos revisados estão preservados como SNAPSHOT_*.

## Propagação e unidades

[DERIVED] Para SN, a conversão de velocidades nas linhas 24–31 corresponde a equations.py:464–491 e intercept.py:22–51,159–176: usa zcmb, compõe multiplicativamente o redshift peculiar 2M++ e retorna à convenção relativística de velocidade. O passo elimina um ida-e-volta redundante zcmb→vcmb→zcmb do upstream; a equivalência é algébrica, não uma promessa de igualdade bit a bit.

O código forma V = C_mag/25 + diag{[log10(1+240/v_corr)]²}. O fator 1/25 converte magnitude² em unidades de alpha², porque alpha contém −0,2 m. O termo de velocidade é a mesma prescrição de deslocamento finito do upstream, não uma nova propagação diferencial completa dos erros em cosmografia.

Com V positiva definida, Cholesky resolve V u=1 e calcula Var(alpha)=1/(1ᵀu), w=u/(1ᵀu). Isso corresponde à compressão de intercepto constante por mínimos quadrados generalizados de intercept.py:225–239. A ordem das soluções triangulares é correta. Não há necessidade de formar uma inversa completa. A checagem do posto efetivo precede a Cholesky; não há jitter nem substituição silenciosa por pseudoinversa.

Para SBF, as linhas 42–48 usam a velocidade 2M++ já extraída e V_i=(σ_m,i/5)²+[log10(1+240/v_i)]². A compressão diagonal σ_alpha=[Σ_i(1/V_i)]^(−1/2) corresponde ao ramo simplificado de intercept.py:128–155, com a seleção sem corte usada neste snapshot. A variante acrescenta (σ_M,i/5)² a cada diagonal. Esse é exatamente um acréscimo independente condicional; não representa automaticamente erros comuns de inclinação/calibração.

Os números são incertezas de alpha em logaritmo decimal, não magnitudes, percentuais, significâncias ou incertezas finais de H0. A comparação SBF abaixo não é evidência entre hipóteses e não mede o impacto em um ajuste da rede.

## Identidade e resultado existente

[REAL documental do recibo da coordenação; não reproduzido numericamente nesta revisão]

| Quantidade | Resultado existente |
|---|---:|
| Linhas SN / nomes distintos preservados | 277 / 238 |
| Posto de C_mag e V_SN | 277 / 277 |
| Menor autovalor de C_mag | 0,005295993328634611 |
| Condição de V_SN | 35,219414400647295 |
| Resíduo máximo da solução V u=1 | 1,9984014443252818e−15 |
| σ_alpha SN condicional upstream | 0,0018926416391806479 |
| Linhas SBF | 61 |
| σ_alpha SBF upstream, somente e(m110) | 0,0031037757826860514 |
| σ_alpha SBF com e(M110) independente adicional | 0,004031412599817339 |

A sequência SN retém L2…L278; SBF retém L2…L62. Não houve agrupamento por nome de SN nem reordenação em relação ao metadado previamente auditado. A correspondência física da matriz sem rótulos à ordenação publicada continua sendo o INPUT upstream já documentado; a revisão verificou a preservação dessa convenção, não inventou identificação interna ausente no arquivo.

Pins dos quatro inputs do protocolo, hash do protocolo no resultado e pin do mapa seq454 conferem. Também conferem as condições fixas da extração: 2M++, dispersões de 240 km/s, sem corte adicional de redshift, sem SN IR, sem descarte dos termos fora da diagonal e com incremento intrínseco SN configurado em zero. Isso justifica as constantes do script **neste snapshot**. O script não deve ser apresentado como interface genérica para configurações futuras.

## Limites que permanecem

- [OPEN — NS-01] O parecer anterior estabelece que um offset comum não absorve integralmente erro de cor/largura intrínseca. A coluna e(M110) ainda não foi decomposta por componente. Sua adição diagonal pode ser uma variante finita declarada, mas não é correção física validada. Os rótulos do protocolo e resultado preservam essa distinção.
- C_mag positiva definida e V_SN bem condicionada qualificam a operação numérica. Não provam completude de componentes, ausência de contagem dupla de velocidade, covariâncias entre blocos ou adequação das hipóteses de independência.
- q0/j0 entram nas médias implementadas no upstream, não nesta fórmula condicional dos erros. A ausência deles neste cálculo não valida, por si, mudança de cosmologia ou de propagação quando o contrato passar a variar esses parâmetros.
- A matriz conjunta, normalizações completas e dependências com calibradores não foram montadas. Os dois sigmas de intercepto não podem ser tratados como estimativas finais independentes de H0.
- MM continua não avaliado: σ_D/D exige distância central que não integra a extração permitida.
- Esta revisão não qualifica novamente limites externos de processo. O resultado registra wall 0,046743599930778146 s e CPU 0,03125 s; a imposição externa do orçamento de execução está fora desta revisão estática. Nenhuma reexecução é necessária para o aceite das fórmulas e rótulos aqui dado.

Nenhum centro de catálogo, alpha, H0, S/g, likelihood, evidência, fit ou D foi aberto/calculado nesta revisão. Não houve busca externa, execução upstream ou novo executor. A entrega permanece preparação técnica; nenhuma adoção de V1 ou veredito físico decorre dela.
