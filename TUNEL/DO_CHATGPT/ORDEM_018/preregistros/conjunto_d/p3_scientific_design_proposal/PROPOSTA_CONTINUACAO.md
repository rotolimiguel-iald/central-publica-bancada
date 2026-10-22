# Proposta de continuação científica sintética P3

[INPUT — proposta, não autorização] Recomenda-se a alternativa A: manter o Dynesty estático com 256 pontos vivos, rwalk/25, os dois casos congelados e suas sementes, propondo 100.000 chamadas de likelihood e 100.000 gerações de waveform por caso, com os limites de tempo abaixo. A mudança é de orçamento e de avaliação documental da recuperação; não é reparo de imports disfarçado de justificativa científica. O operador pode aceitar, reduzir ou recusar esse investimento antes de qualquer novo contrato de execução. Esta pasta não contém comando executável, nova unidade científica, CLAIM, AUTH ou decisão ROOT.

## Evidência que motivou a proposta

[REAL — leitura de JSONs, não reprodução] O RESULT do GR em INIT003 registra STOPPED_NOT_CONVERGED, 9.738 chamadas de likelihood e waveform, 857,9152041240595 s de parede, 857,333447926 s de CPU, 814,7409760054434 s no contador de waveform, delta_logz=57,275736336318445 e ESS=null. O recibo de encerramento registra cinco operações bloqueadas pelo audit hook. Portanto, nem o posterior parcial nem o exit0 do supervisor constituem resultado científico aceito. O contador de waveform é o contador do wrapper, não um inventário de todas as funções C auxiliares.

O RB foi interrompido pela coordenação por causa da falha da campanha: o último registro completo contém 1.173 chamadas e 98,83394302404486 s, mas não é recibo final de custo ou convergência. A parede total registrada da campanha é 958,936355162994 s. Não somar o progresso RB como se fosse custo final, nem transformar ESS ausente em zero.

[REAL — documental] A qualificação de imports 5e391d57 concluiu sem chamadas científicas ou PE. Ela removeu uma incerteza operacional daquela invocação; não mediu recuperação, mistura, adequação do orçamento ou custo de PE. Os controles anteriores não serão repetidos nesta proposta.

[INFERENCE] Existe evidência de insuficiência do trajeto observado sob o envelope antigo, além de invalidação por auditoria. Não existe uma curva validada de chamadas necessárias, nem uma separação experimental entre limite de orçamento e exploração inadequada. Assim, 100.000 chamadas é uma alocação máxima proposta, não uma estimativa de convergência calculada de 57,2757.

## Alternativas antes de qualquer nova medição

| Alternativa | Sampler e sementes | Limites por caso | Vantagem e limite |
|---|---|---|---|
| A — recomendada | Static NestedSampler, nlive=256, bound=multi, rwalk, walks=25; sementes 180602/180603 preservadas | 100.000 likelihood e 100.000 waveform; trabalho até 14.400 s; supervisor até 14.410 s; CPU 13.200/13.205 s; 8 GiB | Isola a ampliação do orçamento, mantendo o mecanismo de exploração. Não corrige eventual dificuldade de mistura, modos omitidos ou ESS insuficiente. |
| B — não selecionada | Mesmo nlive/bound/sementes, sample=rslice, slices=15; walks não aplicável | Mesmos limites de A | Altera a exploração por fatias aleatórias; pode ter custo/eficiência diferentes, não medidos aqui. Muda a sequência de propostas mesmo com a mesma semente e exige delta específico de sampler e sua revisão. Não é fallback automático. |
| C — referência de decisão | Manter o envelope de 10.000 chamadas sem nova execução | Consumo adicional zero | Preserva a conclusão incompleta atual; não resolve a pergunta de recuperação. Repeti-lo apenas após reparar imports não tem finalidade científica nova demonstrada. |

[KNOWN — fonte primária local por pin] A documentação embutida em dynesty/dynesty.py, linhas 265–295, descreve nlive maior como posterior mais finamente amostrado com mais iterações, e usa rwalk em auto para 10≤ndim≤20. As linhas 402–416 definem walks e slices; rslice tem padrão 3+ndim, aqui 15. Isso sustenta que B é implementável pela API existente, não que seria superior. O número 256 não é reivindicado como ótimo. Não se propõe aumentar nlive junto com o orçamento porque isso acrescentaria outra mudança sem diagnóstico que a selecione.

A e B são mutuamente exclusivas nesta decisão. A proposta é de no máximo dois casos, não de quatro execuções para comparar algoritmos. Trocar A por B após um resultado desfavorável exigiria outra decisão científica; não está incluído.

## Pergunta e invariantes

A pergunta nova é: sob a mesma likelihood e os mesmos dados sintéticos congelados, o algoritmo A alcança os critérios numéricos herdados e produz evidência interpretável de recuperação de DTau220 dentro de um envelope ampliado, previamente fixado? Uma resposta negativa ao teto é resultado útil de viabilidade limitada, sem autorizar extensão.

O modelo é o IMR alinhado pSEOBNRv4HM_PA, com somente DTau220 livre entre as deformações QNM; DOmega220=DTau440=DOmega440=0. GR_GAUSS e RB_GAUSS nomeiam injeções, não duas hipóteses de likelihood. Os 12 parâmetros livres, priors e transformação condicionada de massas permanecem integrais: área admitida 3477,5 Msol², q em [0,2;1], nenhuma concentração do prior ao redor da verdade ou redução dimensional.

Conservam-se duração 32 s, amostragem 4096 Hz, geração 8192 Hz, banda 20–1024 Hz, referência 20 Hz, janela/época/geometria H1/L1, PSD analítica aLIGOZeroDetHighPower, SNR ótimo de rede 20 e todos os valores de injeção documentados. O ruído é o congelado de semente 180601, pareado entre casos e não regenerado. As sementes do sampler 180602/180603 também permanecem. Não há restart/resume dos estados terminais nem leitura dos diagnósticos NPZ antigos.

A íntegra desses campos é transportada como metadados no JSON desta proposta e vinculada ao contrato lido. Os pins de arrays nele mencionados são referências históricas declaradas pelo contrato, não hashes reconferidos nesta preparação. Nenhum array, strain, PSD, ASD, posterior ou observado foi aberto ou hashado. A reconferência bruta permanece fora da autorização desta unidade e não pode ser contornada pela montagem futura.

A atualização geral para um.py v388 não migra esses dados, a fonte de waveform ou os priors congelados. Não se recalcula a injeção RB a partir de uma versão nova. Esta proposta tampouco libera d72, D ou qualquer provedor.

## Envelope concreto proposto

[INPUT — escolha de investimento, não previsão] Por caso: 100.000 chamadas de likelihood incluindo os pontos vivos iniciais; no máximo 100.000 gerações no wrapper waveform; trabalho nominal até 14.400 s; supervisor nominal até 14.410 s, incluindo recolhimento/persistência; CPU soft 13.200 s e hard 13.205 s; espaço de endereçamento 8.589.934.592 bytes; um worker, um thread, um caso de cada vez. Ordem GR e depois RB, no máximo dois casos.

[DERIVED — aritmética dos tetos, não medição] Para os dois casos: no máximo 200.000 chamadas de cada contador, 28.820 s nominais de supervisor (8 h 00 min 20 s) e soma dos limites hard de CPU de 26.410 s (7 h 20 min 10 s). CPU refere-se ao processo científico conforme o mecanismo contratado; não é promessa de limite de CPU de todo o sistema. Os tempos são orçamento nominal sujeito a agendamento/FS, não hard real time. A contagem de chamadas pode parar antes desses tetos. A reserva de 10 s por caso é parte dos 14.410 s, sem janela extra ilimitada de cleanup.

O teto de chamadas é 10 vezes o antigo; trabalho e CPU soft são 4 vezes os antigos. Essas razões descrevem a escolha, não a produtividade ou probabilidade de êxito. Não se multiplicam custos do GR interrompido por 10 para anunciar duração esperada; não se extrapola para os 14 candidatos D. Não há previsão de chamadas necessárias a partir de delta_logz.

## Parada, integridade e resultado

1. Os contadores externos ao sampler são verificados antes de cada avaliação, incluindo inicialização; o parâmetro maxcall de Dynesty não substitui esse limite. O sampler local usa sua própria contagem e compara ncall>maxcall (sampler.py 1074–1084); isso explica por que a fronteira deve continuar externa, sem assumir igualdade entre os dois contadores.
2. Pin/identidade divergente, auditoria bloqueada, EDOM, erro nativo indeterminado, waveform None, valor não finito ou violação temporal encerra caso e campanha como falha. Nada é convertido silenciosamente em −infinito, rejeição do prior ou sucesso parcial. Latch/journal/checkpoints e classificação reconhecido/indeterminado permanecem.
3. Só um término limpo por orçamento, com identidade/processo e recibo final certos, pode permitir o segundo caso já previsto. Não convergência GR não autoriza mudar qualquer parâmetro RB. Falha ou estado incerto impede RB. Timeout/kill não é parcial limpo por inferência. Nunca repetir/resumir, aumentar teto, alterar sementes ou escolher B durante a execução.
4. Convergência numérica candidata por caso: delta_logz<0,1 antes de adicionar os pontos vivos finais, live likelihood não plana, limite de chamadas não atingido e nenhuma falha; após a adição final, pesos válidos e ESS ponderado≥100. Preserva-se o critério herdado. O delta usa estimativa da evidência restante do sampler, não certificado de todos os modos ou erro verdadeiro. ESS é 1/Σw² para pesos normalizados, não tamanho amostral independente de cadeia.
5. CLEAN_PARTIAL pode ser um recibo operacional íntegro, mas nunca aceite científico. DLOGZ_REACHED_ESS_LOW e ausência de ESS continuam incompletos. Ambos os casos precisam atingir os critérios para a classificação PAIR_NUMERICALLY_CONVERGED; somente um caso não fecha o par. Qualquer evidência de auditoria invalida essa classificação, mesmo com exit0.
6. Recibo e diagnóstico devem separar status operacional, critérios numéricos e avaliação de recuperação. Campos de diagnóstico ausentes são indisponíveis, não zero. São necessárias identidade de contrato/dados/runtime, contadores completos, recurso medido, término certo e revisão independente. Esta proposta não implementa nem executa esse avaliador.

## Recuperação não se confunde com convergência

[INPUT — regra documental candidata, nova e visível] Somente para um resultado limpo e numericamente convergido, a revisão independente registra para DTau220: quantis ponderados q05/q50/q95, largura W90=q95−q05, deslocamento q50−verdade, percentil da verdade Fw(verdade), fração posterior nos 5% de cada borda do prior e comparação W90/2,52. Os quantis seguem inf{x:Fw(x)≥p}, com pesos normalizados e ordenação por DTau220, sem interpolação ou reamostragem aleatória. As massas nas bordas usam [-0,8;−0,66] e [1,86;2], com endpoints incluídos.

A largura central de 90% do prior uniforme [-0,8;2] é 2,52 [DERIVED, apenas geometria do prior]. Propõe-se rotular como evidência favorável, restrita ao caso, a inclusão da verdade em [q05;q95] junto com W90<2,52. A combinação impede que a mera reprodução do prior inteiro conte como recuperação informativa, mas admite contração pequena: é um diagnóstico fraco, não calibração de precisão. Nenhum PASS automático nasce dessa inclusão; a revisão deve expor bordas, forma/multimodalidade e limites de ESS. Ausência desses diagnósticos mantém recuperação OPEN.

Se a verdade estiver fora do intervalo, o resultado é incompatibilidade com esse critério de recuperação para aquela realização; não prova defeito do sampler, física falsa ou falta de cobertura populacional. Se o intervalo permanecer amplo, o modelo pode ser subidentificado neste caso. As regras não exigem que todos os 12 parâmetros individualmente atinjam um limiar artificial de recuperação.

[OPEN] ESS≥100 é um diagnóstico mínimo herdado: as caudas de 5% podem ter pouca massa efetiva, e os quantis não ganham certificado uniforme de precisão por esse limiar. As métricas serão apresentadas com essa limitação, sem inventar tolerância inferida do resultado. A regra candidata acima deve ser aceita ou alterada por decisão explícita antes da execução, sem seleção de critério após o posterior.

Dois casos com ruído pareado são duas injeções determinísticas sobre uma realização comum. Nem 2/2 intervalos contendo as verdades constituem cobertura frequentista, nem seu quociente é uma estimativa binomial independente. Não medem viés populacional ou descoberta global de modos. Diferença de logZ entre os dois datasets não é Bayes factor. Mesmo um par favorável só qualifica esses casos e este envelope, sem liberar PE D.

## Próximo passo útil e decisão pendente

ROOT pode apresentar A e B ao operador com seus tetos e o alcance dos critérios. A aceitação exige uma decisão específica sobre o novo desenho e a alocação, além de resolver o acesso de integridade às entradas congeladas sem contornar a recusa já registrada. Depois disso, a montagem separada pode incorporar o delta visível, preservar todas as fronteiras de auditoria e receber revisão antes de qualquer autorização de execução. Nenhuma alteração foi feita no candidato do autor, em INIT003, no pacote imports-only ou na base v388.

Novos IDs, se algum dia autorizados, servem à custódia: não tornam repetível uma unidade terminal nem transferem autorizações antigas. O objeto novo é um experimento com orçamento científico explicitamente diferente. Enquanto essa decisão não existir, a ação é somente considerar esta proposta. F3 recuperação/convergência permanecem OPEN; nenhuma comprovação empírica ou conclusão final foi produzida.

## Fontes de leitura

- RECIBO_ROOT_P3_ADEQUACAO_ENVELOPE.json: diagnóstico ROOT e fronteira de autorização.
- p3_init_qualified_003/CONTRATO_P3.json: linhas 6–112 (modelo/prior), 114–228 (grid/dados/metadados das injeções), 231–306 (sampler/limites/critério/custo).
- INIT003/RESULT.json: linhas 2–13, 92–93 e 123 em diante; RECIBO_ROOT_ENCERRAMENTO_INIT003.json: descarte científico e RB parcial.
- p3_startup_pin_preparation/CONTRATO_CANDIDATO.json e RECIBO_ROOT_ACEITE_IMPORTS.json: escopo e sucesso apenas de imports.
- p3_startup_pin_preparation/driver_p3.py: linhas 159–200; result_acceptance.py: linhas 73–77; distinção do limite externo e aceite parcial.
- proveniencia/p3_runtime_snapshot/dynesty__dynesty.py: linhas 265–295 e 402–416; dynesty__sampler.py: linhas 1064–1100. Fontes primárias copiadas, hashes iguais às entradas correspondentes do RUNTIME_P3_READONLY.json lido; runtime Linux não reaberto.
- Mapa ringdown.ramo_b_preregistro_v386: consulta anterior contendo 682–685, preservada em MAPA_ANTES.json.

Hashes e tamanhos vêm dos bytes das fontes documentais/código efetivamente lidos nesta unidade e constam de RECIBO_FONTES_LIDAS.json. Pins referidos dentro de JSONs não equivalem a leitura de seus destinos.
