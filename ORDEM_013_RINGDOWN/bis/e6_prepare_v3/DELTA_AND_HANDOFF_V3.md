# E6 V3 — correção focal O5, congelada para R

**READY_FOR_FOCUSED_INDEPENDENT_CLOSING_NOT_AUTHORIZED.** Diretório definitivo: `bis/e6_prepare_v3`. V1 e V2 preservadas; V2 reconferida byte a byte contra seu manifesto. O snapshot integral anterior permanece em `superseded_freeze_001/` nesta V3. Manifestações V2 copiadas nesta árvore são proveniência histórica; o manifesto corrente é `PREPARATION_MANIFEST_V3.json`.

Delta executável **exatamente uma substituição de rótulo** em `assemble_baselines`: `operational_information_target` O5 recebe `sum_inverse_variance_dtau`, em vez de `source_declared_information`. Fonte declarada: `e0_rate_and_o5_scenarios_013bis.py` transporta `r['I_tau_target90']`; `calculate_e0_core.py` define informação de dtau como soma de 1/sigma². Os dois arquivos foram apenas lidos e pinados no manifesto. Nenhum número recalculado, fonte editada ou contrato expandido.

O contrato/schema semântico continua V2 e é byte a byte idêntico ao congelado. O nome V3 identifica esta revisão do pacote/código. R1/R2/R4/R5 e demais ramos R3 não mudaram. Os 32 valores não nulos entre 80 cenários O5 apontados por R deixam de falhar pela unidade; a presente verificação de execução usa somente um O5 fictício, não monta dados reais.

Rodada preservada `FIXTURE_RESULTS_V2_002.json`: **60/60 checks**, negativos aceitos=0. Inclui positivo O5 com informação dummy não nula e pointer preservado; negativo rejeita o antigo rótulo sem tipo. Inclui regressão dos cinco achados e 180 células vazias. A rodada foi concluída antes da separação dos diretórios V2/V3; hashes do código testado e script conferem com estes bytes. V2 foi restaurada de seu snapshot sem divergências; nenhuma fonte científica foi executada na operação.

Encaminhar a R este delta, manifesto V3 e evidências para fechamento focal. Não executar E6. Nenhuma autorização real E6, nenhum estágio real, nenhuma extração E7 ou conclusão da ordem. O helper de paredes será preparado separadamente depois deste freeze.
