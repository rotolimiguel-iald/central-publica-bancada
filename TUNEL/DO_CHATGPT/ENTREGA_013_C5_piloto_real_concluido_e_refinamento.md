[REAL — rodada e auditorias aritméticas concluídas; OPEN — convergência e calibração]

# ORDEM 013 — Piloto Phenom completo, precisão parcial e próxima proposta

Registro: 2026-09-22T09:33:57.591395+00:00. N/A — sem mudança no cânone, no Lean ou em C6.

**Terminou:**54722,código0. Foram contabilizadas todas as16384 propostas:
8554 vetores válidos e7830 integrandos zero fora do suporte. Nenhum ponto
difícil foi descartado. O original62818 permanece falho e preservado.

**Auditorias passaram:** densidade logarítmica com erro
1.7763568394e-15; jacobiano relativo
2.00942151807e-10; erro máximo de
soma independente (inclui ESS)=2.67164068646e-12.
Erro no próprio lnB=8.71525074331e-15.

**Precisão local:**512/1200 conjuntos,
contra0/1200 na rodada8192. ESS mínimo/mediano/máximo:
2.01271029/106.811129/422.661465.
Isso não é aceitação física nem calibração:688 conjuntos continuam falhando,
e120 mudaram mais de0.2 em lnB na comparação
com8192. Maior mudança=0.9111832448.
Não combinar as simulações como eventos nem converter esses lnB em sigma.

**Controles antigos:** máximos numéricos disponíveis para426 pontos; para8128
somente o fato de terem atravessado os testes antes da gravação, conforme
implementação preservada. Essa limitação segue explícita. Os próximos blocos
guardam os controles dentro do mesmo NPZ, junto com os vetores.

**Diagnóstico da próxima amostragem:**12 candidatos comparados em duas metades,
com seleção pela eficiência prevista, nunca pelo sinal da evidência.
Venceu `rms_K6_scale1`: pior-metade, décimo percentil de ganho
1.05218204; ganho mediano
1.58857409. É previsão incerta, não precisão
conquistada. A hipótese de envelope foi testada e não venceu.

**Registrada, ainda não iniciada:**32768 propostas,seed130972,
`phase_real_refined`. Mesmos priors físicos e likelihood;70% mistura ajustada,
20% mistura anterior e10% prior completo. Oráculo independente32768/seed130850:
normalização1.0189618 ±0.0159708441;
maior desvio padronizado dos13 momentos=1.45705351.
O novo amostrador reaproveita o código existente, altera o leitor já validado
e acrescenta apenas a persistência dos controles aos blocos.

**Ativos:**40860(SEOB16384);15254(controle de resolução SEOB,186/196);
57200(controle de resolução Phenom,169/347). Revalidar os handles.
Os controles de resolução são nos pontos dominantes, não um limite global
de erro do posterior. Antes de lançar `run_real_phase_importance.py --processes 4`,
ler seus resultados; se algum reprovar, tratar a falha primeiro.

**Demais próximos passos:** concluir/auditar/comparar SEOB; executar a combinação
já registrada `combine_continuation_families.py run` somente após os dois
resultados e auditorias de densidade. Esse registro usa a continuação Phenom
16384 e SEOB16384; a nova proposta32768 não substitui esse caminho em silêncio.
Precisão integral, repetição, posterior contínuo e viés/cobertura continuam abertos.
Não repetir as cadeias C1-C4/C6/C7 já verificadas.


## Adendo 2026-09-22T09:35:04.375010+00:00 — controle SEOB concluído

[REAL]15254 terminou com código0. Controle8192→16384Hz nos196 pontos dominantes: máximo |ΔlogL|=0.080030965721221037, abaixo de0.1. PASS no escopo pontual; não é um limite global do posterior. O piloto SEOB continua0/1200 em precisão. Ativos revalidados:40860(repetição SEOB) e57200(controle Phenom,233/347). A nova rodada Phenom32768 permanece registrada, não iniciada, aguardando o controle Phenom.
