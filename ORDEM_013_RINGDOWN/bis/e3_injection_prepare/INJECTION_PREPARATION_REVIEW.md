# E3 — preparação finita de injeções, após o piloto

[REAL: leitura de código/metadados; DERIVED: geometria e escalares; INPUT: desenho candidato; OPEN: execução e calibração]

**CANDIDATO NÃO ALOCADO.** O caminho congelado implementa injeções GR de duas famílias de spins alinhados — pSEOBNRv4HM_PA e IMRPhenomXPHM — recuperadas sempre por pSEOBNRv4HM_PA com os 15 parâmetros livres, inclusive os quatro desvios QNM. Não existe matriz recíproca de recuperação XPHM. O desenho tem dez templates revisáveis; `wall_budget_seconds` e `sampler.maxcall` são null, tornando-os deliberadamente não executáveis até E3.2. Não criei ORCAMENTO_40H, jobs ativos, saídas de execução ou campanha nova/ressuscitada.

## Fonte, priors e famílias

O vetor candidato [INPUT próprio, não verdade LVK] é m1=40, m2=30 M☉ **detector-frame**, chi1=0,2, chi2=−0,1, distância inicial500 Mpc, theta_jn=1, phase=0,3, ra=1, dec=0,2, psi=0,4 rad; quatro desvios=0 para RG. q=0,75 é derivado; não inserir a=0/1, tilt, spin cartesiano, remanescente ou outro campo em `injection.parameters`, que aceita exatamente as coordenadas físicas/deformacionais e q opcional. `a` da matriz TGL é rótulo da hipótese, não spin nem parâmetro do gerador.

Priors preservados do piloto: m1[15,100], m2[10,100], q[0,125,1], chi1/chi2[−0,99,0,99], D[100,2000] Mpc; theta_jn Sine[0,π], dec Cosine[−π/2,π/2]; phase/ra Uniform[0,2π] periódicos, psi Uniform[0,π] periódico. DTau220 e DOmega220/440 Uniform[−0,8,2]; DTau440 Uniform[−0,8,4]. O prior temporal inteiro é transladado, sem mudar largura0,3s. A verdade e a distância reescalada precisam permanecer no suporte; massa/remanescente não ficam fixos na recuperação.

XPHM recebe |chi| e tilt0/π conforme o sinal: **subespaço alinhado**, apesar do nome de uma família capaz de precessão. Somente as injeções GR são suportadas nessa família; qualquer desvio não nulo recusa. Priors fixos numéricos não são suportados por `validate_truth_support`: usar variant=`220_plus_440_free`, fixed_deformation_parameters={}. Fixar440=0 na verdade de uma hipótese não é fixá-lo na recuperação. Não reabrir os fechamentos anteriores nem mudar fonte para contornar isso.

## SNR e distância

Bins propostos [INPUT] de SNR de rede publicado: [12,14), [14,20), [20,30), [30,60), [60,100); alvos de SNR ótimo da injeção:13,16,25,45,80. Contagens dos14 candidatos registrados nesses bins: 9, 5, 0, 0, 0; holds por bin: 3, 1, 0, 0, 0. Os bins vazios neste conjunto são controles de extrapolação, não eventos adquiridos. GW250114 é a âncora de ruído/calibração; não use resultado ou largura de posterior para escolher bin. Qualquer prioridade/alocação depende do custo real após o piloto.

A rotina normaliza o **SNR ótimo de rede IMR completo**, na PSD/banda20–1024Hz e redeH1/L1 do job. Não é SNR_RD nem se iguala automaticamente ao SNR de detecção GWOSC. Para rho0 no ponto inicial500Mpc, factor=target/rho0, h→factor·h e Dnew=500·rho0/target. O código exige100<Dnew<2000, revalida toda a verdade e confirma o SNR alvo. Isso implica0,2·target<rho0<4·target; os cinco alvos simultaneamente exigiriam16<rho0<52 **na mesma resposta de referência**. Não medi rho0. Cada família/GPS/PSD/sky precisa passar sua checagem; nenhum SNR ou Dfinal foi inventado. A distância final das famílias geralmente difere se ambas forem normalizadas ao mesmo SNR.

## Tempo, céu e ruído off-source

**Só GW250114_082203 tem `event_reference_GPS` em E2.** Células sob esse evento podem variar fontes/SNR e usar o seu ruído. Não podem ser apresentadas como calibração no ruído de cada um dos14 candidatos. Trocar para outro evento de calibração falha por falta de âncora GPS; o carregador dinâmico de jobs não acrescenta âncoras a E2. Eventos de teste não podem usar o ramo calibration.

Mantém-se event_GPS real=1420878141.2; ele não é o tempo injetado. Sem abrir HDF, os nomes pinados indicam arquivo off-source[1420873728,1420877824). Janela candidata inicial[1420874240.0,1420874256.0); tinj=start+12,2; prior geocêntrico≈[start+12,05,start+12,35]. Slots avançam32s; cada bin/réplica tem janela16s; as duas famílias partilham um slot como par. A geometria admite no máximo112 slots/22 réplicas completas de cinco bins antes de verificar DQ — **não é alocação, disponibilidade ou tamanho suficiente de amostra**.

Para cada detector, `data.onsource_path/sha256` deve ser **igual** ao seu `offsource_path/sha256`, apontando ao arquivo off-source já pinado; onsource significa apenas a janela analisada pelo runner. A janela inteira deve terminar≤event_GPS−16 ou iniciar≥event_GPS+16. A PSD vem do primeiro bloco256s válido do mesmo arquivo, escolhido apenas por flags/finitude, com Welch Hann8s, overlap50%, mediana. A escolha termina≤min(event_GPS−16,segment_start). Antes de alocar todas as réplicas, exigir bloco PSD comum terminando antes da primeira janela; não basta presumir que o início do arquivo passa DQ. Não existe chave de configuração para escolher arbitrariamente GPS de PSD. Se não houver bloco válido, recusar/preservar e rever a alocação, sem escolher PSD favorável.

RA/dec/psi ficam iguais entre famílias e réplicas por convenção de céu inercial. Mover o GPS muda antena/atraso; não preserva resposta de detector. A rotina recalcula atrasos por detector e exige chegada dentro da região sem taper. Não trocar para um céu otimizado para SNR. Dados devem ter4096Hz e epoch exato: não há reamostragem implícita.

[REAL — somente limites escalares LAL] No ponto GR, pré-pico1,128808527s, cauda0,046632712s; usando todo o prior temporal proposto, margens10,699191473s/3,381367288s. Vinte pontos de fronteira, incluindo q=0,125 e estiramento máximo de cauda5 da recuperação, têm margens mínimas6,333286003s/1,617376685s. São limites genéricos; não provam todo o prior contínuo, suporte exato ou vazamento FFT. Ambos os geradores usam reserva±0,022s; uma violação aborta, não vira rejeição científica de proposta/prior.

Compartilhar PSD, fonte e janela entre famílias cria dependência: analisar diferenças pareadas e propagar covariância. Não somar réplicas/famílias como eventos independentes. A seleção DQ e os intervalos disponíveis permanecem OPEN; não li strain nem suas máscaras.

## TGL a=1: o que o código permite

| Leitura/objeto | Implementabilidade sem mudar fontes |
|---|---|
| RG a=0 | Ambas as famílias, quatro desvios exatamente0; recuperação livre. |
| R-B/R-MOD/R-RAIZ-0/R-LIN ensemble | pSEOB pode receber DTau constante por modo, se mapeamento físico/pins/suporte forem previamente declarados. R-MOD exige QNM exato e domínio corrotante admissível. Não há cálculo dessas verdades nesta preparação. |
| R-A/R-RAIZ-EP4/R-RAIZ-REST | Parametrização constante possível em pSEOB, mas correções sub-resolução não ganham poder numérico por serem passadas como float; impedir promessa de distinguibilidade. |
| R-GLOBAL | Desvios zero; coincide com GR neste observável, não uma célula TGL independente. |
| R-RAIZ-COHERENT/R-PROP | Sem DTau constante único na fonte pinada. Não substituir inclinação inicial/propagação por amortecimento pós-pico. |
| XPHM a=1 não trivial | Não implementado: qualquer desvio não zero é recusado. Parâmetros todos zero são apenas controle GR. |
| Realização browniana, Cauchy ou saltos / jitter populacional TGL | Geradores atuais não implementam trajetórias estocásticas. DOmega constante livre não é um desenrolamento GKSL nem calibração de transferência; não amostrar desvios para simular essa equivalência. |
| C7 envelope, overtones compartilhando Gamma, fonte precessante/NR/v5 | Não estão expostos nesse contrato congelado; não renomear como DTau pSEOB. |

O mapa de ensemble é DTau_lmn=−x_lmn/(1+x_lmn), x=Gamma·tau_GR; DOmega=0. Para a escala a, documentar x→a·x e só então mapear; não interpolar DTau linearmente sem convenção. Beta permanece ALPHA_FINE_CODATA_2018×sqrt(e) em runtime. Remanescente é obtido dos parâmetros físicos por convenção pinada, não inferido desta revisão. 440 exige QNM externo com procedência; a função escalar só tem ajuste220 embutido. Escolha only220 versus220+440 é INPUT explícito; não priorizar leitura pelo resultado. Relógios dependentes de redshift exigem dizer como a reescala de distância muda/não muda o redshift de verdade: o injetor não recalcula DTau após reescalar D. A verdade final e a convenção devem ser coerentes antes da execução, ou a célula permanece OPEN.

## Reuso LVK e requisitos antes de alocar

[REAL] Os dois grupos NR_with_44/NR_without_44 dos metadados locais têm verdade física nula, injection_parameters=None e injection_file/dict=None. Seu config cita SEOBNRv5PHM,8s,2048Hz,20–896Hz. Esses metadados não fornecem vetor de injeção reproduzível nem se confundem com o prior amplo/16s/4096Hz deste piloto. Reuse como referência do diagnóstico já arquivado e da lacuna, sem abrir posterior nem inferir verdade da mediana recuperada.

- **M1_PILOT — OPEN:** After-pilot cost, terminal convergence/acceptance receipt and family/configuration comparison, with hashes. Do not read/assume new pilot posterior in this preparation.
- **M2_BUDGET — OPEN:** E3.2 actual remaining 40h budget, N per family/bin, maxcall and wall per job, stopping precision, all five alternatives costed. Candidate carries null wall/maxcall deliberately.
- **M3_NOISE — OPEN:** Future authorized metadata/DQ verification of pinned H1/L1 offsource file extents, common valid 16s windows and flags; PSD first valid 256s block must end before earliest planned analysis window. No strain read here.
- **M4_DISTANCE — OPEN:** At execution, family/time/sky-specific reference optimal SNR at D0=500 Mpc and registered PSD/band; Dnew=D0*rho0/target strictly inside (100,2000). Freeze infeasible-bin disposition before results; never widen prior to obtain a pass.
- **M5_POPULATION — OPEN:** Ratify arbitrary aligned source point and five SNR-bin targets as INPUT or provide a predeclared source grid; one source/one epoch is not population calibration. LVK metadata contains no recoverable physical truth vector.
- **M6_METRICS — OPEN:** Independent analysis specification: per-family/bin bias, paired covariance, uncertainty on c, within/between-family df scatter, coverage levels and binomial intervals, failures counted, precision/stop criterion and systematic-gate computation. No such campaign results claimed.
- **M7_ALLOCATION — OPEN:** Populate E2_PE_JOBS_V2 jobs, parent registration hash, unique names/output dirs/seeds, config SHA, ORCAMENTO_40H allocation and tunnel witness before jobs. Do not replace existing jobs or edit E2.
- **M8_TGL — OPEN:** For nonzero a=1 candidates, per-reading/per-mode remnant/QNM/clock/redshift provenance, signed-spin admissibility, deformation convention and truth support, with 220-only versus 220+440 INPUT explicit. No values computed here.
- **M9_IMPLEMENTATION_LIMITS — NOT_IMPLEMENTED_IN_FROZEN_PATH:** Keep recovery all four deviations free. XPHM non-GR/precessing truths, stochastic unravelings, exact coherent/propagation signals, fixed-deformation recovery and new event GPS anchors are unsupported by this frozen path; separate reviewed/versioned implementation if later authorized.

E3.2 deve comparar as cinco alternativas da ordem: piso de outras leituras; bins altos; PE reduzida; acervo LVK; v5 em ambiente próprio. As duas primeiras são escolhas de desenho/orçamento, não garantias de sucesso; PE reduzida, instalação v5 ou recuperação alternativa exigem caminho separado revisado. Um ponto LVK não paga curva de cobertura/c(SNR). Nenhuma dessas alternativas ressuscita a campanha C5 encerrada.

O envelope final aceito é `schema_version=E2_PE_JOBS_V2`, `parent_registration_sha256`, `jobs={nome:cfg}`. A alocação precisa referenciar seu arquivo/hash e testemunha no túnel, com `registered_utc` posterior a E2. Não substituir GW250114_PILOT. Cada config completa mantém `mode=calibration`, evento autorizado, privacy_mode procedural_same_host, orçamento individual≤28800s (teto da alocação E2, embora o controlador tenha teto mais amplo), workers≤28, seeds distintos e critérios dlogz/ESS/amostras. O resultado esperado do sampler é apenas CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW; tempo/cap/baixa ESS não viram posterior aceito.

O custo e N permanecem null até o piloto. N≈(sigma_inj/piso)² é planejamento condicional, não cobertura garantida. Reportar viés c com incerteza, famílias separadas, cobertura com IC, dispersão df e suas componentes, falhas e precisão alcançada; piso primário estrito |delta|/5, /15 apenas sensibilidade. Limiar vermelho mantém INCONCLUSIVE_SYSTEMATICS; nada aqui paga5σ, IV físico, significância ou admissão. NOT_FALSIFIED nunca CONFIRMED.

## Artefatos e pins

- Candidato: `INJECTION_CANDIDATE_DESIGN.json` — `b1424da9c067abc1411d9b6613770a5ba871b58c3864a2433c88d13062faad28`.
- Checagens finitas de metadados: `FINITE_METADATA_CHECKS.json` — `0a5ec3ca3fb2c01bbac7c21a17eeefedea4de051a3253b5caaf6a1030b256d8b`.
- `ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json` — `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416`.
- `TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` — `a907d07bc484b53cc6db237dc5972f4dcc47be03ad084c832201bb648981454b`.
- `ORDEM_013_RINGDOWN/bis/f2_injection/METADATA.json` — `b56c22e54d99b98d0693e915326f410f193063928248e859902df6692625f305`.
- `ORDEM_013_RINGDOWN/bis/e4_e5_prepare/PE_R1_R2_R3_CLOSING_REVIEW.md` — `1da6c752d3313e18e2dd8e086d7254555d472a7aa8c0f9dcf14759d1569ef30f`.
- `ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py` — `fd0fc446e1c732f3d782210c6effa7cb7faeaeb7a51a434d4f397f1da89bd652`.
- `ORDEM_013_RINGDOWN/bis/e3_injection_prepare/SCALAR_TIME_BOUND_OBSERVATION.json` — `ce9bb95c23abe12419a6fe700925cbc9e15209ef87932aa7ceff66cf87723115`.
- `ORDEM_013_RINGDOWN/bis/e3_injection_prepare/build_candidate_checklist.py` — `198e4a83cf8938b8f736b6b7b9fe7917daf1ee0289a0f87fcc3c6f55c8a619d7`.
- `ORDEM_013_RINGDOWN/bis/e2_code/injection_design.py` — `12017563c123df76b856ddedecf9166ddc4c25fe26a5c8b773bc82086b6c842d`.
- `ORDEM_013_RINGDOWN/bis/e2_code/temporal_contract.py` — `c8f4ecbc28d4312e3885d61c14f174062c6055eee0bbd54897e725a18240b605`.
- `ORDEM_013_RINGDOWN/bis/e2_code/pseob_source.py` — `2c9a053177bd2671da1879f60343434b3605b3274994b42d68aa50cd68f4ff2f`.
- `ORDEM_013_RINGDOWN/bis/e2_code/pe_runner.py` — `6712610a0392abe629b6ea5b5f4fa5a45b2c8b9a3dfb123c952513f18cef68fa`.
- `ORDEM_013_RINGDOWN/bis/e2_code/strain_io.py` — `a52faf32e88088320c57d303987a31ec2b9b59c93e162923d603c2c96b21a5b6`.
- `ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py` — `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7`.
- `ORDEM_013_RINGDOWN/bis/e2_code/run_controlled.py` — `7b5dd6484014942ee5fdd9fc3e529eaf05f9dffe463f35cdd10a01bdcf86334d`.
- `ORDEM_013_RINGDOWN/bis/e2_code/remnant_conversion.py` — `87604de5c8fa7139cd6aa4d0c4fde09476105769735e44d476f3b9a55aa11bc1`.

Pins de arquivos de strain nos templates são referências copiadas do registro, não hashes verificados contra os arquivos nesta revisão. Fontes de produção apenas lidas; todos os novos arquivos ficam nesta pasta.
