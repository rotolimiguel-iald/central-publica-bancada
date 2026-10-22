# Contrato final provisório dos seis módulos PE/controlador

[REAL — implementação draft + 25 mocks e toy analítico; NÃO REGISTRADO] Edição autorizada exclusiva dos seis módulos. Os nulos, fetch e injection_design permanecem do principal. Estado anterior em ownership_backup_002. Hashes finais devem ser reobtidos ao congelar toda a árvore.

## Registro

`checked_registration()` continua retornando `(reg_original, digest)` e funciona somente no `/opt/lal_env` pinado. Nunca passar uma view mesclada para reconstruir/verificar o mapa original.

Campos novos/obrigatórios:

- `registered_utc`, UTC com timezone; `registration_id` para futura guarda de unblinding.
- Testemunha em `TUNEL/DO_CHATGPT`: linhas únicas `registro_sha256: <hash>` e `registered_utc: <UTC>`. UTC da testemunha ≥UTC do registro e ≤agora; mtime não anterior à UTC interna (tolerância de filesystem 2 s). Hash e cronologia verificados antes de ciência.
- `extra_code_roots`: lista de `{relative_to_Chatgpt, files_sha256}`; cada mapa contém **todos os .py recursivos**, paths relativos ao root. Usar isso no lugar do campo draft `extra_code_trees`, ou converter antes de registrar. Incluir raiz E7 e preparação Kerr quando finalizadas; arquivo acrescentado depois invalida o mapa.
- `test_candidates[event].publication_census_scope`: obrigatório, texto do corpus auditado. Ausência de deformação nesse corpus não é inexistência universal. `eligible` e ausência no corpus continuam exigidas.
- `allocation_policy`: opcional `{relative_to_Chatgpt: "ORDEM_013_RINGDOWN/ORCAMENTO_40H.json", max_job_wall_seconds: ...}`. A ausência do arquivo não bloqueia o piloto estático.

Alocação futura: JSON com `parent_registration_sha256`, `registered_utc`, `witness_relative_to_Chatgpt`, `jobs_relative_to_Chatgpt`, `jobs_sha256`. Testemunha em D contém `allocation_sha256: <sha do ORCAMENTO_40H.json>` e `registered_utc`. Jobs file com `{schema_version:"E2_PE_JOBS_V2", parent_registration_sha256, jobs:{...}, downloads:{...}}`. Sem substituição de chaves estáticas. Cada job cego precisa de `publication_metadata_review:{review_passed:true,scope,relative_to_Chatgpt,sha256,reviewed_utc}`; reviewed_utc ≥registro e documento pinado. Rechecagem atual da elegibilidade é responsabilidade desse recibo.

`load_jobs(reg,digest)` retorna jobs estáticos+alocação validada. `load_authorized_configuration(reg,digest)` retorna **view derivada** com esses pe_jobs e downloads; exportada para fetch. Downloads dinâmicos exigem `license_receipt_relative_to_Chatgpt` e `license_receipt_sha256`, além dos campos de licença/URL/checksum do fetch. A view inclui `_parent_registration_sha256` e `_allocation_sha256`. Não cria registro, alocação, testemunha ou autorização por conta própria.

## Job piloto

Mantidos: `variant="220_plus_440_free"`, `onsource_roll_off_s`, `sampler.minimum_effective_samples`. Acrescentar:

```json
{"fixed_deformation_parameters": {}, "privacy_mode": "procedural_same_host"}
```

Piloto aceita o schema dos demais campos do draft001; o novo draft pode usar 8 s/start1420878135 sem modificar código. Todos mass_1/mass_2/chi_1/chi_2/distância/ângulos/tempo e quatro desvios livres; mass_ratio é Constraint derivada. Variante futura: `variant="registered_fixed_deformation_variant"` e mapa explícito de desvios fixos, exatamente iguais aos respectivos priors numéricos. O piloto não pode usar essa variante para fingir M/spins livres. Campos físicos não podem ser números fixos.

Time prior deve ficar dentro da região não atenuada da janela. Por proposta, source verifica limites escalares LAL `SimInspiralChirpTimeBound`, `MergeTimeBound`, `FinalBlackHoleSpinBound`, `RingdownTimeBound`, com cauda escalada pelo maior 1+dtau. Falha aborta com `WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION`; não retorna likelihood inválida para truncar silenciosamente o prior. Nenhuma dessas funções/ondas foi avaliada nesta preparação: assinaturas foram lidas do binding instalado. Oito segundos são suportados, **não certificados por ensaio de waveform nesta rodada**. O futuro smoke deve conferir o suporte real e, se preciso, ampliar janela por alteração testemunhada antes da PE.

Waveform arguments novos: `analysis_time_contract:{start_GPS,duration_s,roll_off_s}`; source agora recebe `geocent_time` pareado. Injection pSEOB precisa passar esses mesmos argumentos (ou seu próprio contrato registrado coerente com o segmento de injeção). Nenhuma alteração semântica foi feita em IMRPhenomXPHM por este agente.

## Invocação e privacidade

Somente `run_controlled.py --job <id>`. Ele cria cache/<nome> exclusivo, LAUNCH_CONTEXT.json, PRIVATE.log e inicia `pe_runner.py --job ... --launch-context ...` em sessão/grupo próprios. O runner valida pai/start_ticks, PGID/SID, hash do config, deadline e stdout/stderr apontando ao log privado regular; cria LAUNCH_CLAIM exclusivo. Chamada direta sem contexto falha. O grupo inteiro é sondado/encerrado mesmo se o líder já saiu. Reserva 12 s para TERM/grace/KILL/reap/recibo dentro do teto. Uma emergência de SO não é garantia hard-real-time; cleanup não comprovado aparece como falha.

Privacidade é **procedural no mesmo host**, com chmod solicitado e descritores verificados; não se afirma custódia humana separada ou isolamento de ACL do NTFS. Logs/checkpoints/resultados brutos só devem ser lidos pelo custodiante. Nenhuma seed real lida nesta preparação.

## Convergência e custo

`check_point=False`, `check_point_plot=False`, seeds Bilby+NumPy e seed explícito no sampler. Subclasse declara `external_sampler_name="dynesty"`. Observador captura `delta_logz` imediatamente após sample() e antes dos live points. Posterior só é elegível após dlogz, ncall, ESS ponderado, tamanho e finitude coerentes. maxcall, plateau, ESS insuficiente, campos ausentes ou captura ausente nunca são sucesso; dados parciais ficam privados e `ANALYST_STATUS.json` sem posterior tem rc3.

Distinção: `sampler_ncall` não é `source_calls`. Source counter compartilhado em workers fork mede chamadas efetivas e soma wall por chamada, incluindo inicialização/erros, sem se confundir com CPU ou parede total. Dynesty pode ultrapassar maxcall ao finalizar iteração/lote; overshoot é registrado e caso ≥limite não é aceito. Teto absoluto é de parede pelo controlador, não promessa de exatamente 3 milhões de chamadas.

Saída elegível contém **15 colunas pareadas**: 11 físicas componentes/geométricas e quatro desvios. Em cego, desvios recebem offsets; colunas físicas continuam pareadas. Massas componentes não são Mf; chi_1/2 não são af; Mf/af/z ficam OPEN sem um fit/conversão nomeados. Nuisance/gate sistemático não ficam verdes porque sampler convergiu.

`cfg.injection` opcional: após construir todos ifos/strain/PSD e antes do generator de recuperação, chama `injection_design.inject_into_ifos(ifos,cfg,reg)`. Exige calibração, recibo dict, grava PRIVATE_INJECTION.json. Recuperação sempre pSEOB livre; o módulo de injeção do principal deve validar ancoragem, ruído real, trigger e família. Outra família TGL permanece NÃO PAGO se não houver convenção física justificada.

## Evidência de teste e pendências

OWNED_V2_TESTS.json: 25 testes finitos, sem PE/waveforms/strain/seed. Toy analítico 1D: `toy_adaptor_002/TOY_RECEIPT.json`; convergido delta_logz≈0,296517<0,3, ESS≈84,9156, ncall1155; caso maxcall50 parou ncall59, rejeitado mesmo com 10 amostras. Primeira tentativa encontrou import recordeddynesty inválido e foi preservada em toy_adaptor_001/FAILED_ADAPTER_IMPORT.json; correção validada. Toy executou plumbing real Bilby/dynesty, não PE física nem campanha de MC E2. Bilby grava pickle próprio no toy: não foi unpickled.

Necessários antes do registro: revisão independente do principal sobre fontes finais, mocks finais após últimas mudanças, revisão do injection_design/fetch/null_runner e integração com a preparação Kerr. Os hashes dos toys identificam versões de código testadas; alterações posteriores exigem declarar alcance, nunca reutilizar o hash como se fosse o novo. Nenhum registro E2 criado.
