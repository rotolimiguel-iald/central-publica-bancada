"""Metadata-only candidate design writer. No producer imports or science execution."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, math, os, re

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
CHAT=B.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def publish(name,value):
    p=HERE/name
    data=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8') if not isinstance(value,str) else value.encode('utf-8')
    temp=p.with_suffix(p.suffix+'.pending')
    with temp.open('xb') as stream:stream.write(data)
    assert temp.read_bytes()==data and data
    os.link(temp,p);temp.unlink()
    return {'file':p.name,'sha256':sha(p),'bytes':len(data)}

regpath=B/'RINGDOWN_5SIGMA_V1.json';reg=read(regpath);rh=sha(regpath)
pilot=reg['pe_jobs']['GW250114_PILOT']
assert pilot['event'] in reg['calibration_event_ids']
assert set(reg['event_reference_GPS'])=={pilot['event']}
code=['injection_design.py','temporal_contract.py','pseob_source.py','pe_runner.py','strain_io.py','registration_guard.py','run_controlled.py','remnant_conversion.py']
for name in code:assert sha(B/'bis/e2_code'/name)==reg['own_code_tree_sha256'][name]
pred=B/'tgl_ringdown_prediction.py'
assert sha(pred)==reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/tgl_ringdown_prediction.py']
order=CHAT/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
lvkpath=B/'bis/f2_injection/METADATA.json';lvk=read(lvkpath)
truth_fields=['mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','ra','dec','psi','geocent_time','dtau220','dtau440','domega220','domega440']
lvk_summary={}
for name,g in lvk['groups'].items():
    m=g['metadata']
    lvk_summary[name]={'physical_truth_present':any(row.get(k) is not None for row in m.get('injection_data',[]) for k in truth_fields),'injection_parameters':m.get('meta_data/other/injection_parameters'),'config_metadata':{k:m.get('config_file/config/'+k) for k in ['waveform_approximant','duration','sampling_frequency','minimum_frequency','maximum_frequency','reference_frequency','injection_file','injection_dict','zero_noise','gaussian_noise']}}
assert not any(v['physical_truth_present'] for v in lvk_summary.values())
selected={k:v for k,v in reg['test_candidates'].items() if v['eligible'] is True and v['published_deformation_at_registration'] is False}
assert len(selected)==14
bins=[('B0',12.,14.,13.),('B1',14.,20.,16.),('B2',20.,30.,25.),('B3',30.,60.,45.),('B4',60.,100.,80.)]
bin_metadata=[]
for name,lo,hi,target in bins:
    events=[k for k,v in selected.items() if lo<=v['SNR_network_GWOSC']<hi]
    bin_metadata.append({'id':name,'observed_network_GWOSC_bin':[lo,hi],'interval':'[lower,upper)','target_network_optimal_SNR':target,'test_candidate_ids_metadata_only':events,'count':len(events),'without_quality_hold':sum(not selected[k]['data_quality_hold'] for k in events),'quality_hold_count':sum(selected[k]['data_quality_hold'] for k in events),'statute':'INPUT_BIN_EDGES_AND_TARGET; REAL_COUNTS_FROM_REGISTERED_METADATA','limit':'Published network detection SNR is not identical to the future optimal SNR in the frozen PSD/band. No equality or selection by recovered width.'})
assert sum(b['count'] for b in bin_metadata)==14
# Parse existing filename metadata only: no stat/open/hash of strain paths.
anchors=[]
for detector,entry in pilot['data'].items():
    match=re.search(r'-(\d+)-(\d+)\.hdf5$',entry['offsource_path']);assert match
    anchors.append((int(match[1]),int(match[2])))
assert len(set(anchors))==1
file_start,file_duration=anchors[0];first_start=file_start+512.;stride=32.
truth={'mass_1':40.,'mass_2':30.,'chi_1':.2,'chi_2':-.1,'luminosity_distance':500.,'theta_jn':1.,'phase':.3,'ra':1.,'dec':.2,'psi':.4,'geocent_time':first_start+12.2,'dtau220':0.,'dtau440':0.,'domega220':0.,'domega440':0.}
families=['pSEOBNRv4HM_PA','IMRPhenomXPHM']
templates={}
finite=[]
for j,b in enumerate(bin_metadata):
    start=first_start+stride*j
    for fi,family in enumerate(families):
        key=f'E3_GR_{b["id"]}_{"PSEOB" if fi==0 else "XPHM"}_R000_CANDIDATE'
        cfg=copy.deepcopy(pilot)
        cfg.update(output_directory_name=key,label=key,segment_start_GPS=start,wall_budget_seconds=None)
        cfg['sampler']['seed']=13231000+2*j+fi
        cfg['sampler']['maxcall']=None
        # Translate the full frozen time prior by the injection's offsource shift.
        new_t=start+12.2;delta=new_t-pilot['event_GPS']
        cfg['priors']['geocent_time']['minimum']=pilot['priors']['geocent_time']['minimum']+delta
        cfg['priors']['geocent_time']['maximum']=pilot['priors']['geocent_time']['maximum']+delta
        p=dict(truth,geocent_time=new_t)
        cfg['injection']={'family':family,'noise_kind':'REAL_OFFSOURCE','target_network_optimal_SNR':b['target_network_optimal_SNR'],'parameters':p}
        for detector,d in cfg['data'].items():
            d['onsource_path']=d['offsource_path'];d['onsource_sha256']=d['offsource_sha256']
        assert cfg['event_GPS']==reg['event_reference_GPS'][cfg['event']]
        assert cfg['fixed_deformation_parameters']=={} and cfg['variant']=='220_plus_440_free'
        assert set(cfg['priors'])==set(truth)|{'mass_ratio'}
        for field,prior in cfg['priors'].items():
            val=p['mass_2']/p['mass_1'] if field=='mass_ratio' else p[field]
            assert math.isfinite(val) and prior['minimum']<=val<=prior['maximum']
        assert p['mass_2']<=p['mass_1'] and set(p)==set(truth)
        assert file_start<=start and start+cfg['duration_s']<=file_start+file_duration
        assert start+cfg['duration_s']<=cfg['event_GPS']-cfg['offsource_exclusion_s']
        assert file_start+cfg['psd_duration_s']<=min(cfg['event_GPS']-cfg['offsource_exclusion_s'],first_start)
        assert cfg['priors']['geocent_time']['minimum']>start+cfg['onsource_roll_off_s']+.022
        assert cfg['priors']['geocent_time']['maximum']<start+cfg['duration_s']-cfg['onsource_roll_off_s']-.022
        assert cfg['wall_budget_seconds'] is None and cfg['sampler']['maxcall'] is None
        finite.append({'job':key,'truth_in_frozen_priors_after_time_translation':True,'analysis_disjoint_protected_event_by_metadata':True,'common_earliest_PSD_geometry_possible':True,'not_launchable_budget_unassigned':True,'input_window':[start,start+cfg['duration_s']],'input_truth_time':new_t})
        templates[key]=cfg
slots=math.floor((file_duration-512-pilot['duration_s'])/stride)+1
missing=[
 {'id':'M1_PILOT','required':'After-pilot cost, terminal convergence/acceptance receipt and family/configuration comparison, with hashes. Do not read/assume new pilot posterior in this preparation.','status':'OPEN'},
 {'id':'M2_BUDGET','required':'E3.2 actual remaining 40h budget, N per family/bin, maxcall and wall per job, stopping precision, all five alternatives costed. Candidate carries null wall/maxcall deliberately.','status':'OPEN'},
 {'id':'M3_NOISE','required':'Future authorized metadata/DQ verification of pinned H1/L1 offsource file extents, common valid 16s windows and flags; PSD first valid 256s block must end before earliest planned analysis window. No strain read here.','status':'OPEN'},
 {'id':'M4_DISTANCE','required':'At execution, family/time/sky-specific reference optimal SNR at D0=500 Mpc and registered PSD/band; Dnew=D0*rho0/target strictly inside (100,2000). Freeze infeasible-bin disposition before results; never widen prior to obtain a pass.','status':'OPEN'},
 {'id':'M5_POPULATION','required':'Ratify arbitrary aligned source point and five SNR-bin targets as INPUT or provide a predeclared source grid; one source/one epoch is not population calibration. LVK metadata contains no recoverable physical truth vector.','status':'OPEN'},
 {'id':'M6_METRICS','required':'Independent analysis specification: per-family/bin bias, paired covariance, uncertainty on c, within/between-family df scatter, coverage levels and binomial intervals, failures counted, precision/stop criterion and systematic-gate computation. No such campaign results claimed.','status':'OPEN'},
 {'id':'M7_ALLOCATION','required':'Populate E2_PE_JOBS_V2 jobs, parent registration hash, unique names/output dirs/seeds, config SHA, ORCAMENTO_40H allocation and tunnel witness before jobs. Do not replace existing jobs or edit E2.','status':'OPEN'},
 {'id':'M8_TGL','required':'For nonzero a=1 candidates, per-reading/per-mode remnant/QNM/clock/redshift provenance, signed-spin admissibility, deformation convention and truth support, with 220-only versus 220+440 INPUT explicit. No values computed here.','status':'OPEN'},
 {'id':'M9_IMPLEMENTATION_LIMITS','required':'Keep recovery all four deviations free. XPHM non-GR/precessing truths, stochastic unravelings, exact coherent/propagation signals, fixed-deformation recovery and new event GPS anchors are unsupported by this frozen path; separate reviewed/versioned implementation if later authorized.','status':'NOT_IMPLEMENTED_IN_FROZEN_PATH'}]
reading_status={}
for reading in reg['readings']:
    if reading in ['R-B','R-MOD','R-RAIZ-0','R-LIN']:
        status='PSEOB_CONSTANT_ENSEMBLE_DTau_CONDITIONAL_MAPPING_REQUIRED'
    elif reading in ['R-A','R-RAIZ-EP4','R-RAIZ-REST']:
        status='PSEOB_CONSTANT_ENSEMBLE_PARAMETER_MAPPABLE_BUT_SUBRESOLUTION_NOT_DISTINGUISHABLE'
    elif reading=='R-GLOBAL':status='GR_EQUIVALENT_ZERO_DEFORMATION_NO_SEPARATE_TGL_POWER_CELL'
    else:status='NO_UNIQUE_CONSTANT_DTau_IN_THIS_SOURCE'
    reading_status[reading]={'pseob_a1':status,'XPHM_a1':'ONLY_IF_ALL_FOUR_DEFORMATIONS_EXACTLY_ZERO_THEN_GR_DUPLICATE; nonzero rejected','recovery':'all four QNM deviations free','scope':'Source-code implementability, not scientific acceptance or universal physical interpretation'}
paths=[regpath,order,lvkpath,B/'bis/e4_e5_prepare/PE_R1_R2_R3_CLOSING_REVIEW.md',pred,HERE/'SCALAR_TIME_BOUND_OBSERVATION.json',Path(__file__)]+[B/'bis/e2_code'/n for n in code]
pins={p.relative_to(CHAT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}
candidate={'schema_version':'E3_INJECTION_PREPARATION_V1_NOT_ALLOCATION','status':'CANDIDATE_METADATA_DESIGN__NO_EXECUTION__BLOCKED_PENDING_PILOT_AND_ALLOCATION','created_utc':datetime.now(timezone.utc).isoformat(),'parent_registration_sha256':rh,'order_locators':['E3.2 lines194','E3.3 lines195','E2.6 lines183'],'scope':'Read-only source/metadata preparation; writes only this folder; no producer/E2 edits, waveform, PE, MC, draws, strain, posterior samples, hidden seed or offset access. No historical campaign resurrection.','accepted_dynamic_job_schema_after_completion':'E2_PE_JOBS_V2','allocation_not_created':True,'launchable':False,'truth_statute':'INPUT_ARBITRARY_ALIGNED_SOURCE_NOT_LVK_REPRODUCTION','truth_reference':truth,'families':families,'recovery_family':'pSEOBNRv4HM_PA','bin_plan':bin_metadata,'minimum_grid':{'bins':5,'families':2,'cells':10,'replicates_per_cell':None,'candidate_templates_represent_first_replica_only':True},'noise_plan':{'anchor_event':pilot['event'],'event_reference_GPS':pilot['event_GPS'],'file_start_from_filename_only':file_start,'file_duration_from_filename_only':file_duration,'first_analysis_start':first_start,'analysis_duration_s':16,'window_stride_s':stride,'replica_rule':'slot=5*replicate_index+bin_index; start=file_start+512+32*slot; both families share a paired noise window','geocent_time_rule':'start+12.2; translate full pilot time prior by truth_time minus real event_GPS','PSD_rule':'Frozen reader chooses first 256s all-flag/finiteness-passing block in same file; require common block end<=first analysis start before any allocated jobs','maximum_geometry_slots_ignoring_DQ':slots,'maximum_complete_five_bin_replicas_ignoring_DQ':slots//5,'scope':'Filename geometry only; common PSD and paired noise imply cross-job dependence, never count as independent exposure/time.'},'distance_rescale':{'formula':'Dnew=D0*rho0/target','reference_distance_Mpc':500,'strict_recovery_support_Mpc':[100,2000],'rho0_interval_per_target':'0.2*target < rho0 < 4*target','rho0_intersection_for_all_five_targets_at_same_response':[16.,52.],'scope':'Algebra only. rho0 unknown and changes with family, GPS, sky and PSD. Per-job checks remain mandatory.'},'LVK_metadata_reuse':lvk_summary,'TGL_a1_implementability':reading_status,'missing_inputs':missing,'candidate_job_templates':templates,'source_pins_relative_to_Chatgpt':pins}
cp=publish('INJECTION_CANDIDATE_DESIGN.json',candidate)
fp=publish('FINITE_METADATA_CHECKS.json',{'status':'PASS_METADATA_PLAUSIBILITY_ONLY__NOT_PRODUCTION_VALIDATION','parent_registration_sha256':rh,'candidate':cp,'source_pins':pins,'checks':finite,'scalar_bounds':'SCALAR_TIME_BOUND_OBSERVATION.json','counts':{'templates':10,'truth_support_and_geometry_checks':len(finite),'waveforms':0,'draws':0,'PE_runs':0},'limits':['No runtime validator/producer executed.','Positive scalar checks cannot prove DQ, achievable SNR, convergence, coverage, calibration or full-prior waveform support.']})
report=f'''# E3 — preparação finita de injeções, após o piloto

[REAL: leitura de código/metadados; DERIVED: geometria e escalares; INPUT: desenho candidato; OPEN: execução e calibração]

**CANDIDATO NÃO ALOCADO.** O caminho congelado implementa injeções GR de duas famílias de spins alinhados — pSEOBNRv4HM_PA e IMRPhenomXPHM — recuperadas sempre por pSEOBNRv4HM_PA com os 15 parâmetros livres, inclusive os quatro desvios QNM. Não existe matriz recíproca de recuperação XPHM. O desenho tem dez templates revisáveis; `wall_budget_seconds` e `sampler.maxcall` são null, tornando-os deliberadamente não executáveis até E3.2. Não criei ORCAMENTO_40H, jobs ativos, saídas de execução ou campanha nova/ressuscitada.

## Fonte, priors e famílias

O vetor candidato [INPUT próprio, não verdade LVK] é m1=40, m2=30 M☉ **detector-frame**, chi1=0,2, chi2=−0,1, distância inicial500 Mpc, theta_jn=1, phase=0,3, ra=1, dec=0,2, psi=0,4 rad; quatro desvios=0 para RG. q=0,75 é derivado; não inserir a=0/1, tilt, spin cartesiano, remanescente ou outro campo em `injection.parameters`, que aceita exatamente as coordenadas físicas/deformacionais e q opcional. `a` da matriz TGL é rótulo da hipótese, não spin nem parâmetro do gerador.

Priors preservados do piloto: m1[15,100], m2[10,100], q[0,125,1], chi1/chi2[−0,99,0,99], D[100,2000] Mpc; theta_jn Sine[0,π], dec Cosine[−π/2,π/2]; phase/ra Uniform[0,2π] periódicos, psi Uniform[0,π] periódico. DTau220 e DOmega220/440 Uniform[−0,8,2]; DTau440 Uniform[−0,8,4]. O prior temporal inteiro é transladado, sem mudar largura0,3s. A verdade e a distância reescalada precisam permanecer no suporte; massa/remanescente não ficam fixos na recuperação.

XPHM recebe |chi| e tilt0/π conforme o sinal: **subespaço alinhado**, apesar do nome de uma família capaz de precessão. Somente as injeções GR são suportadas nessa família; qualquer desvio não nulo recusa. Priors fixos numéricos não são suportados por `validate_truth_support`: usar variant=`220_plus_440_free`, fixed_deformation_parameters={{}}. Fixar440=0 na verdade de uma hipótese não é fixá-lo na recuperação. Não reabrir os fechamentos anteriores nem mudar fonte para contornar isso.

## SNR e distância

Bins propostos [INPUT] de SNR de rede publicado: [12,14), [14,20), [20,30), [30,60), [60,100); alvos de SNR ótimo da injeção:13,16,25,45,80. Contagens dos14 candidatos registrados nesses bins: {', '.join(str(x['count']) for x in bin_metadata)}; holds por bin: {', '.join(str(x['quality_hold_count']) for x in bin_metadata)}. Os bins vazios neste conjunto são controles de extrapolação, não eventos adquiridos. GW250114 é a âncora de ruído/calibração; não use resultado ou largura de posterior para escolher bin. Qualquer prioridade/alocação depende do custo real após o piloto.

A rotina normaliza o **SNR ótimo de rede IMR completo**, na PSD/banda20–1024Hz e redeH1/L1 do job. Não é SNR_RD nem se iguala automaticamente ao SNR de detecção GWOSC. Para rho0 no ponto inicial500Mpc, factor=target/rho0, h→factor·h e Dnew=500·rho0/target. O código exige100<Dnew<2000, revalida toda a verdade e confirma o SNR alvo. Isso implica0,2·target<rho0<4·target; os cinco alvos simultaneamente exigiriam16<rho0<52 **na mesma resposta de referência**. Não medi rho0. Cada família/GPS/PSD/sky precisa passar sua checagem; nenhum SNR ou Dfinal foi inventado. A distância final das famílias geralmente difere se ambas forem normalizadas ao mesmo SNR.

## Tempo, céu e ruído off-source

**Só GW250114_082203 tem `event_reference_GPS` em E2.** Células sob esse evento podem variar fontes/SNR e usar o seu ruído. Não podem ser apresentadas como calibração no ruído de cada um dos14 candidatos. Trocar para outro evento de calibração falha por falta de âncora GPS; o carregador dinâmico de jobs não acrescenta âncoras a E2. Eventos de teste não podem usar o ramo calibration.

Mantém-se event_GPS real={pilot['event_GPS']}; ele não é o tempo injetado. Sem abrir HDF, os nomes pinados indicam arquivo off-source[{file_start},{file_start+file_duration}). Janela candidata inicial[{first_start:.1f},{first_start+16:.1f}); tinj=start+12,2; prior geocêntrico≈[start+12,05,start+12,35]. Slots avançam32s; cada bin/réplica tem janela16s; as duas famílias partilham um slot como par. A geometria admite no máximo{slots} slots/{slots//5} réplicas completas de cinco bins antes de verificar DQ — **não é alocação, disponibilidade ou tamanho suficiente de amostra**.

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

'''
for m in missing:report+=f'- **{m["id"]} — {m["status"]}:** {m["required"]}\n'
report+='''
E3.2 deve comparar as cinco alternativas da ordem: piso de outras leituras; bins altos; PE reduzida; acervo LVK; v5 em ambiente próprio. As duas primeiras são escolhas de desenho/orçamento, não garantias de sucesso; PE reduzida, instalação v5 ou recuperação alternativa exigem caminho separado revisado. Um ponto LVK não paga curva de cobertura/c(SNR). Nenhuma dessas alternativas ressuscita a campanha C5 encerrada.

O envelope final aceito é `schema_version=E2_PE_JOBS_V2`, `parent_registration_sha256`, `jobs={nome:cfg}`. A alocação precisa referenciar seu arquivo/hash e testemunha no túnel, com `registered_utc` posterior a E2. Não substituir GW250114_PILOT. Cada config completa mantém `mode=calibration`, evento autorizado, privacy_mode procedural_same_host, orçamento individual≤28800s (teto da alocação E2, embora o controlador tenha teto mais amplo), workers≤28, seeds distintos e critérios dlogz/ESS/amostras. O resultado esperado do sampler é apenas CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW; tempo/cap/baixa ESS não viram posterior aceito.

O custo e N permanecem null até o piloto. N≈(sigma_inj/piso)² é planejamento condicional, não cobertura garantida. Reportar viés c com incerteza, famílias separadas, cobertura com IC, dispersão df e suas componentes, falhas e precisão alcançada; piso primário estrito |delta|/5, /15 apenas sensibilidade. Limiar vermelho mantém INCONCLUSIVE_SYSTEMATICS; nada aqui paga5σ, IV físico, significância ou admissão. NOT_FALSIFIED nunca CONFIRMED.

## Artefatos e pins

'''
report+=f'- Candidato: `INJECTION_CANDIDATE_DESIGN.json` — `{cp["sha256"]}`.\n- Checagens finitas de metadados: `FINITE_METADATA_CHECKS.json` — `{fp["sha256"]}`.\n'
for p,h in pins.items():report+=f'- `{p}` — `{h["sha256"]}`.\n'
report+='\nPins de arquivos de strain nos templates são referências copiadas do registro, não hashes verificados contra os arquivos nesta revisão. Fontes de produção apenas lidas; todos os novos arquivos ficam nesta pasta.\n'
rp=publish('INJECTION_PREPARATION_REVIEW.md',report)
assert all(sha(CHAT/p)==v['sha256'] for p,v in pins.items())
print(json.dumps({'status':candidate['status'],'candidate':cp,'finite_checks':fp,'report':rp,'bins':bin_metadata},ensure_ascii=False))
