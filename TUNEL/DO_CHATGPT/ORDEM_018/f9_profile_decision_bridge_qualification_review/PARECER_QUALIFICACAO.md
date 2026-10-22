# Revisão independente do resultado da qualificação stdlib27

**PASS_SYNTHETIC_RESULT_REVIEW_ONLY.** O resultado concreto PASS_SYNTHETIC_INTEGRATION_ONLY está sustentado pelos recibos e logs lidos. A revisão não executou, importou ou repetiu a suíte, não aprovou ciência e não altera a revisão estática anterior.

## Evidência lida

[REAL — artefatos] Runner: run_qualification.py,7.221 bytes,SHA256 d17792a38e2085675827273458b0fba7ad3f356db65c6a25b71afa7f7647ce4d. RESULT.json:2.012 bytes,SHA256 251c202abb3e31d112cdb76f7847fe7cd88a7a6dd884197737a104435da4af5c. STARTED, RESULT, manifesto V2 e manifesto da revisão anterior vinculam os mesmos pins; stdout/stderr conferem com os hashes registrados.

O stdout contém um único resultado estruturado:27 testes,0 failures,0 errors,0 skipped,successful=true,scientific_modules_loaded=[]. O stderr contém os mesmos27 nomes de métodos preparados, cada um com ok, e encerra com Ran27tests in51.664s / OK. RESULT registra returncode0,termination_reason=null. A revisão comparou mecanicamente os nomes do log com os métodos lidos por AST; nenhuma execução de teste foi necessária para essa conferência.

## Medição e alcance

| Campo do recibo | Valor lido | Alcance |
|---|---:|---|
| elapsed_seconds |51.83304880000651|Relógio perf_counter do runner, desde antes de STARTED até após encerramento/cleanup do filho|
| PeakWorkingSetSize lido |80.158.720 bytes|Máximo dos high-water counters do filho nas consultas bem sucedidas|
| PeakPagefileUsage lido |72.650.752 bytes|Máximo de commit/pagefile informado para o filho, não memória física total da máquina|
| memory_samples |1.030|Consultas GetProcessMemoryInfo bem sucedidas|
| memory_sample_failures |0|Sem falha registrada enquanto o filho permanecia ativo|
| memory_observation_cap_bytes |1.073.741.824|Limiar de observação/encerramento, não hard limit OS|
| wall_limit_seconds |120|Orçamento nominal do runner; não prova de deadline total de persistência|

O critério PASS da linha106 exige rc0, ausência de razão de interrupção,elapsed<=120,amostra positiva,zero falhas de consulta,memória observada dentro do cap,27 testes e successful,sem módulos da lista científica carregados. Esses campos concordam neste resultado. successful de unittest é coerente com0failures/0errors nos logs. O caso adicional de recibo válido tardio está entre os27ok.

**Limite temporal concreto:** elapsed é fixado na linha100. O parsing de stdout, hashing dos logs, save_new de RESULT e print nas linhas104–109 ocorrem depois dessa medição, sem nova checagem. Portanto51,833s não é medição do fechamento integral do runner, e esta revisão não certifica toda persistência/saída em<=120s. O ramo de encerramento pode usar wait de1s tanto no corpo como no finally; não constitui prova geral de limite total120s. Nenhum desses ramos de falha foi acionado no resultado lido.

**Limite de RAM concreto:** a consulta a aproximadamente50ms lê contadores de pico mantidos pelo Windows, não apenas uso instantâneo. Isso melhora a observação de picos entre leituras, mas não impõe cap de alocação e não cobre memória agregada de pai+filho. O recibo declara corretamente polled50ms;notanabsoluteOSlimit. Não atribuo a esse resultado um limite rígido de1GiB.

## Recusas, integridade e escopo sintético

O runner:62–76 verifica a ausência de STARTED,manifesto esperado,todos os membros/fontes e o pin da revisão. save_new usa temporário exclusivo,fsync,verificação e rename sem substituição deliberada de recibo existente. STARTED persiste antes de Popen e impede repetição automática na mesma pasta. Não houve lançamento por esta revisão.

O filho recebe -I,-S,-B,stdinDEVNULL e CREATE_NO_WINDOW. Instala guard de audit antes de carregar os candidatos, proíbe escrita,subprocessos/rede e imports da lista científica/remota, e restringe leituras aos membros/fontes pinados e stdlib. O arquivo de testes reutiliza theta/tail/reducer stdlib e lê o perfil por bytes/AST para um double de constantes. O corpo da suíte foi previamente revisado; seu caso nominal exige scientific_decision=None e escopo sintético.

Esses controles e a inspeção das fontes sustentam a classificação de ensaio sintético. O campo scientific_modules_loaded=[] é a observação da lista monitorada, não inventário completo de todos os módulos possíveis nem prova universal de sandbox. science_executed=false,actual_profile_imported=false e d72_P3_launched=false devem ser lidos nesse escopo do programa pinado e dos logs; não como auditoria independente de todos os eventos do sistema operacional.

As recusas programadas de certificados ausentes/adulterados,identidade trocada,gênero booleano de recibo,grau0positivo e prazo cooperativo foram exercidas por fixtures. Isso qualifica suas ligações/recusas de software, não autenticidade de verificador físico,calibração observada,convergência de solver,PE ou cobertura estatística.

## Ressalvas de reuso do runner

O resultado atual tem stdout129B e stderr3.560B, não fluxo excessivo. Entretanto o runner não aplica cap de retenção dos arquivos e lê stdout integralmente. Erros no parsing/persistência final e algumas exceções de cleanup podem impedir RESULT; ausência de resultado deve continuar falha/incerteza,nunca PASS ou motivo para repetir. A condição de PASS não exige explicitamente skipped==0; nesta execução o valor0 foi confirmado nos dois recibos/logs. Não amplio o aceite para qualquer futura suíte com skips.

A evidência não inclui no RESULT identidade PID do filho nem recibo final após persistência; a vinculação examinada é pelos artefatos da única pasta,comando pinado e confirmação de retorno da coordenação. Não afirmo atestação de todos os processos a partir dessa documentação.

## Conclusão delimitada

Não há divergência nos27 resultados ou pins que invalide este PASS sintético. Os limites acima são parte da aceitação, especialmente memória amostrada e tempo que termina antes da persistência final. Sem novo ensaio,sem reparo da unidade consumida,sem modificação de selos,mapa,memórias ou ledger. Verificador científico real,ratificação/abertura e integração em campanha científica permanecem separados.
