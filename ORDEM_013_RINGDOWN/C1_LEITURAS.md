[DERIVED condicional; INPUT/CONJECTURE por leitura; REAL na recuperação dos números e fontes]

# C1 — contrato completo das leituras

Complemento aditivo: `C1_LEITURAS_E_RELOGIOS.md` explica as derivações; `C1_TABLES.json` contém os números originais. Nenhuma leitura foi selecionada. Não se repetiu a estimação nem se alterou o programa canônico.

As colunas de relação com as falas do operador e de escolha física permanecem vazias (`null`), conforme a ordem. `excluded_if_universal=null` significa indecidível sem a partição explícita, nunca “não excluído”. Todos os hashes abaixo foram lidos nesta execução.

| Leitura | Operador / relógio | Fonte e estatuto | Universalidade | FP-5 / unidade |
|---|---|---|---|---|
| R-A | H=hbar*omega*N; K=tau_star*H/hbar; L_phys=sqrt(beta/tau_star)*K; tau_star,src=t_P; tau_star,det=(1+z)*t_P | EXISTING_QUADRATIC_LAW__EFFECTIVE_QNM_BRIDGE_INPUT; INPUT_PRINCIPLED_IDENTIFICATION; cache/casa/um.py:190966; cache/casa/ringdown_dephasing_v2.py:141 | None: PARTITION_DEPENDENT: v369 P1 not excluded; P2 light-mode interpretation excluded. No universal verdict from ringdown alone. | Compatível sob escala fornecida; s^-1 |
| R-B | H=hbar*omega*N; K=tM*H/hbar; L_phys=sqrt(beta/tM)*K; tau_star,src=G*M_src/c^3; tau_star,det=tM | EXISTING_V346_BRANCH__NOT_DERIVED_CLOCK; INPUT_SOURCE_MASS_CLOCK; cache/casa/um.py:190966; cache/casa/ringdown_dephasing_v2.py:141 | None: A source-dependent mass clock is not one universal constant. v369 G*m_atom/c^3 is invisible; G*M_Earth/c^3 is excluded. Reusing a BH mass clock in an atom would be a different, excluded common-clock assumption. | Compatível sob escala fornecida; s^-1 |
| R-MOD | K=(2*pi/kappa)*(omega-m*Omega_H)*N+log(Z); d rho/ds=-(beta/2)[K,[K,rho]]; ds/dt=kappa/(2*pi), with Kerr kappa and positive corotating gap | NEW_MANAGEMENT_HYPOTHESIS__NOT_TGL_CANON; CONJECTURE_KMS_OSCILLATOR_IDENTIFICATION; cache/casa/TheHorizonRate.lean:48; C2_MAPEAMENTO_ANALITICO.md:64 | None: Not a universal Unruh-g identification. Extension to arbitrary accelerated matter is an additional hypothesis; v369 excludes its terrestrial-clock analogue. The finite KMS model is not a physical global Kerr-state construction. | Compatível sob escala fornecida; s^-1 |
| R-RAIZ-0 | K=tau_star*omega*N>=0; L_phys=sqrt(beta/tau_star)*sqrt(K); coherence 0 to 1; s=t/tau_star; tau_star cancels from the positive-root gap | FINITE_ROOT_FORM_CANON__OSCILLATOR_READOUT_CONDITIONAL; INPUT_POSITIVE_GENERATOR_AND_VACUUM_COHERENCE; cache/casa/um.py:2311; cache/casa/um.py:2838 | True: EXCLUDED_IF_UNIVERSAL to the measured Sr atomic transition, as recorded in v369. Does not by itself exclude a BH-only partition or a macroscopic coherent state. | Compatível sob escala fornecida; s^-1 |
| R-RAIZ-EP4 | K=tau_star*(omega0+omega*N)>=0; L_phys=sqrt(beta/tau_star)*sqrt(K); omega0=1/[4*t_P*(1+z)] from an E_P/4 source offset | EXISTING_V369_OFFSET_RECONCILIATION__PHYSICAL_IDENTIFICATION_INPUT; INPUT_BACKGROUND_E_P_OVER_4; cache/casa/um.py:2311; cache/casa/um.py:2838 | False: For the atomic matter readout in v369, the Planckian quadratic limit is not excluded. This does not decide the separate light-mode P2 partition. | Compatível sob escala fornecida; s^-1 |
| R-RAIZ-REST | Same positive-root generator with source-rest-energy background; omega0=M_src*c^2/[hbar*(1+z)] | ATOMIC_OFFSET_TEST_CANON__REMNANT_TRANSPOSITION_NEW; CONJECTURE_REMNANT_REST_OFFSET; cache/casa/um.py:2311; cache/casa/um.py:2838 | True: EXCLUDED_IF_UNIVERSAL using the rest energy of each atomic system, recorded in v369. The BH rest-energy offset is a distinct, explicitly conditional transposition. | Compatível sob escala fornecida; s^-1 |
| R-RAIZ-COHERENT | Positive-root generator of N on a coherent state with mean occupation Nbar; Root clock cancels; Nbar=E_mode/(hbar*omega_src) needs an excitation model | NEW_COHERENT_READOUT_OF_EXISTING_ROOT_FORM; CONJECTURE_OCCUPATION_AND_READOUT; cache/casa/um.py:2311; C2_MAPEAMENTO_ANALITICO.md:64 | None: No universal exclusion follows from the 0-to-1 atomic test without specifying occupation and observable. Nbar=10^78 is a scenario, not a measured source energy. | Compatível sob escala fornecida; s^-1 |
| R-LIN | Schur generator D(rho_nm)=-beta*omega*abs(n-m)*rho_nm; Cauchy phase representation; Physical spectral gap omega*abs(n-m); coefficient 1 is a bridge assumption | CANON_LINEAR_GAP_COMMENT__PHYSICAL_QNM_BRIDGE_NEW; CONJECTURE_LINEAR_GAP_PHYSICAL_BRIDGE; cache/casa/NoFullWitness.lean:25 | True: DERIVED conditional exclusion if the coefficient-1 linear law is universal on Sr: rate is twice the already-excluded root vacuum rate. This is not a new clock measurement. | Compatível sob escala fornecida; s^-1 |
| R-GLOBAL | Common total-Hamiltonian time noise on system AND reference; relational observable commuting with total H; Same time noise in system/reference; cancellation is conditional | V369_P3_CONDITIONAL_NO_LOCAL_OBSERVABLE; INPUT_RELATIONAL_PARTITION; cache/casa/um.py:191013 | None: No local observable under the declared cancellation assumptions, hence no local exclusion. Not a statement that every measurement is insensitive to global dephasing. | Compatível sob escala fornecida; s^-1 |
| R-PROP | Independent local quadratic time noise on propagated spectral components in FLRW; Local source/rest clock t_P along the path; FLRW time-redshift relation | NEW_PROPAGATION_TRANSPOSITION__NOT_A_RINGDOWN_RATE; CONJECTURE_PROPAGATION_MODEL; C2_MAPEAMENTO_ANALITICO.md:64 | None: Atomic limits bound the universal clock conditionally; they do not fix spatial noise correlations or the propagation readout. Source-mass clock over the whole path would be a further assumption. | Compatível sob escala fornecida; s^0 |

## Medidas já executadas

| Leitura | Evento | Gamma (s^-1) | Gamma/omega | x | delta_tau | Tipo |
|---|---|---:|---:|---:|---:|---|
| R-A | GW150914_legacy_remnant | 7.9740665e-40 | 5.08540805e-43 | 3.22563834e-42 | -3.22563834e-42 | ENSEMBLE_ADDITIVE_RATE |
| R-A | GW250114_public_posterior_medians | 8.60125759e-40 | 5.499614e-43 | 3.51878648e-42 | -3.51878648e-42 | ENSEMBLE_ADDITIVE_RATE |
| R-B | GW150914_legacy_remnant | 4.93479986 | 0.0031471359 | 0.0199620603 | -0.0195713753 | ENSEMBLE_ADDITIVE_RATE |
| R-B | GW250114_public_posterior_medians | 4.94916297 | 0.00316447749 | 0.0202470948 | -0.0198452854 | ENSEMBLE_ADDITIVE_RATE |
| R-MOD | GW150914_legacy_remnant | 9.68169506 | 0.00620773864 | 0.0394863925 | -0.0379864448 | ENSEMBLE_ADDITIVE_RATE |
| R-MOD | GW250114_public_posterior_medians | 9.27534086 | 0.00596126066 | 0.0382487979 | -0.0368397228 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-0 | GW150914_legacy_remnant | 9.43271301 | 0.0060156502 | 0.0381568435 | -0.0367544112 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-0 | GW250114_public_posterior_medians | 9.40832518 | 0.0060156502 | 0.0384895896 | -0.0370630481 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-EP4 | GW150914_legacy_remnant | 7.9740665e-40 | 5.08540805e-43 | 3.22563834e-42 | -3.22563834e-42 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-EP4 | GW250114_public_posterior_medians | 8.60125759e-40 | 5.499614e-43 | 3.51878648e-42 | -3.51878648e-42 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-REST | GW150914_legacy_remnant | 3.22129257e-80 | 2.05435798e-83 | 1.30306473e-82 | -1.30306473e-82 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-REST | GW250114_public_posterior_medians | 3.73707799e-80 | 2.38947459e-83 | 1.52884382e-82 | -1.52884382e-82 | ENSEMBLE_ADDITIVE_RATE |
| R-RAIZ-COHERENT | GW150914_legacy_remnant | 2.35817825e-78 | 1.50391255e-81 | N/A | N/A | INITIAL_SLOPE_ONLY |
| R-RAIZ-COHERENT | GW250114_public_posterior_medians | 2.35208129e-78 | 1.50391255e-81 | N/A | N/A | INITIAL_SLOPE_ONLY |
| R-LIN | GW150914_legacy_remnant | 18.865426 | 0.0120313004 | 0.0763136871 | -0.0709028306 | ENSEMBLE_ADDITIVE_RATE |
| R-LIN | GW250114_public_posterior_medians | 18.8166504 | 0.0120313004 | 0.0769791792 | -0.0714769429 | ENSEMBLE_ADDITIVE_RATE |
| R-GLOBAL | GW150914_legacy_remnant | 0 | 0 | 0 | -0 | ENSEMBLE_ADDITIVE_RATE |
| R-GLOBAL | GW250114_public_posterior_medians | 0 | 0 | 0 | -0 | ENSEMBLE_ADDITIVE_RATE |

R-PROP: Xi=3.010403355438708e-23 no FLRW ilustrativo dos insumos. Não se declara x nem delta_tau de ringdown. Distância, redshift e hipóteses estão no JSON.

## Limites da conclusão

A regra FP-5 é respeitada porque nenhuma escala é inferida de alpha/beta. Isso não identifica o relógio físico. A realização modular finita prova a taxa condicional, não que um estado global de Kerr tenha sido construído. A leitura R-LIN usa um gerador de Schur/Cauchy, não um único salto raiz disfarçado. A distinção das leis permanece explícita.
Os testes atômicos são resultados da v369 na partição declarada; não são uma nova medição nem autorização para transportar exclusões entre sistemas sem a hipótese de universalidade. O conteúdo das quatro línguas do operador não foi reinterpretado para escolher uma linha.

Axiomas: N/A — sem Lean novo. JSON companheiro contém âncoras, hashes, dimensões conferidas por script e medidas fonte.
