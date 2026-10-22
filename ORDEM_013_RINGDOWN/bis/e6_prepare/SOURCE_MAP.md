# Mapa de campos-fonte E6 — somente preparação

Os aliases e SHA256 efetivamente lidos estão em `SOURCE_PINS.json`. Índices `i`, populações `p` e leituras `r` abaixo são percorridos, nunca escolhidos por efeito. O gerador não recalcula nenhuma fórmula. As unidades distinguem alvo de informação, contagem de eventos e equivalentes atuais/alvo.

| Canal/contexto | Origem / JSON Pointer | Destino e limite |
|---|---|---|
| Universo de leituras/vereditos | E2 `/readings`, `/permitted_verdicts` | Ordem e enums exatos; não adicionar CONFIRMED |
| Estatuto de leitura | C1 `/rows/i/clock_status`, `/canonical_scope` | INPUT/CONJECTURE; preservar qualificação integral |
| 220 atual: alvo E0 | E0 `/planning_targets/i/{z_signal_planning_offset_zero,I_tau_expected_target90,N90_mixture_illustration_not_selection,GW250114_equivalents_reference_sigma_0p058}` | z condicional, N90 informação/contagem, equivalentes ALVO. Offset zero proibido como teste; preservar população |
| 220 intercepto livre | E0 `/planning_targets/i/{z_slope_free_intercept,N90_slope_illustration}` | Cenário separado; não substituir o cenário primário ou alegar nuisance calibrado |
| 220 correção/sigma | E0 `/all_calibration_combinations/p/std_ddof1/r/{delta_weighted,sigma_combined,z_common,GW250114_equivalents_tau_reference_0p058}` | Correção, sigma, razão comum e equivalentes ATUAIS. Campos ausentes null/OPEN |
| Sensibilidades/GR | E0 `/all_calibration_combinations/p/{sigma_q90,exact_QNM_all_control}` e `/std_ddof1/GR_FALSE_FALSIFIER` | Fontes pinadas para rastreio; não promover controles a leituras/estatística de teste. O quadro principal usa std_ddof1 |
| Piso histórico 220 | E0 `/systematic_conditions/i/{sigma_c_calibrated,floor5_INPUT,floor15_INPUT,gate_green}` | Contexto numérico histórico em todos os grupos 220; não é gate físico atual nem piso 440/δf |
| E1 | E1 `/gate` | Contexto com sigma/normalização/seleção não pagos; `synthetic_E2_nuisance_INPUT` nunca usado como calibração física |
| 440 | E4_RESULT `/E4_fisher/i/{expected_local_z,N90_conditional,delta_tau_440,sigma_delta_tau_local_GR}` | z local, contagem N90, correção/sigma; preservar variant/profile/snr_route/rho e power_scope. PSD O4→O4_HOJE, O5→O5_BANDA, ET/CE próprios. Informação/equivalente não fornecidos ficam OPEN |
| O5 banda | E0 `/conditional_rates_scenarios/forecasts/i/{z_optimistic_same_source_quality_plus_volume,N90_at_fixed_source_improved_sigma,operational_information_target}` | Cenários condicionais; não somar bandas ou interpretar controle BNS como BBH |
| Controle O5 | Mesma linha `/z_optimistic_CI90_rate_only`, `/z_detection_threshold_quality_invariant_control` | IC de z somente devido à taxa e controle de qualidade invariante separados |
| Taxa/IC | E0 `/conditional_rates_scenarios/rates/i/{rare_SNR_ge78,calibration_O4_subset}/{rate_mle_per_year,rate_CI90_per_year}` | Contexto O4 disponível: categorias distintas; preservar `/exposure` e `/scope`. Não transportar automaticamente para rota, instrumento ou população cega |
| 3G genérico 220 | E0 `/threeG_fixed_anchor_calculations/i/{sigma_projected,N90,SNR_RD_target_INPUT,anchor_SNR_INPUT,anchor_scope,scope}` | Referência genérica INPUT sob ET/CE; não previsão específica de detector. z, correção/sigma, informação, equivalente e taxa permanecem OPEN sem fonte compatível |
| IV alvo | E2 `/route_IV/targets/i/{population,sigma_jit,N90_validated,status}` | Contagem N90 inferior condicional, não informação. Cenário Browniano comum repetido sob as dez leituras; não mapeia jitter por leitura |
| IV proveniência | ROUTE_IV `/results`, `/information_df_fourth_power_equivalents`, `/lower_bound_until_transfer_and_systematics` | Arquivo histórico pinado; não reexecutar MC. E2 fornece alvos e E4 fornece equivalentes do quadro |
| IV informação | E4_RESULT `/E5_information/i/{population,N_GW250114_equivalent,statute,sigma_sys,jitter_transfer}` | Equivalentes atuais de informação de variância δf; não somar a equivalentes τ220 nem ponderar likelihood duas vezes |
| Hipóteses | E4_PLAN `/E4/fisher`, `/E5`; E4_REVIEW e E4_RECEIPT | Escopo condicional e revisão de aritmética já efetuada; não prova de likelihood físico |
| Fontes futuras | STAGE_E3.2/STAGE_E3.3/STAGE_TEST, pointers literais nos bindings revisados | Autoridade revisada para novos campos. Nenhuma busca heurística por nomes ou fallback para zero |

## Cobertura que permanece aberta

O4_CEGO e O4C_GWTC6 não recebem números do acervo de calibração para tapar ausência. O5/ET/CE na rota IV não recebem uma conversão inferida de PSD ou SNR. As duas variantes 440 conservam todas as linhas da fonte E4, inclusive zero por construção e leituras sem modelo operacional. R-PROP e R-RAIZ-COHERENT não recebem exponencial ou modelo inventado.

Gate novo: somente bindings E3.3/TEST para `sigma_c_calibrated`, `floor5_INPUT`, `floor15_sensitivity`, `sigma_sys_df`, `sigma_jit_recovered`, `correction_over_sigma_physical`, com unidades do mesmo canal declaradas na fonte. Não se calcula o piso nem se compara uma grandeza δf com um piso δτ. As flags de pagamento são decisões revisadas, não números derivados pelo montador.

O N90 em informação e a contagem N90 são campos diferentes. Um campo disponível não autoriza preencher o outro. Também não se deduz z esperado de N90, nem z físico de Fisher, nem BF de diferença de logdensidades arquivadas. Nenhum calendário ou taxa vira promessa de 5σ real.
