"""Freeze existing metadata and produce an inactive zero-science budget candidate.

Only Python standard library. No production imports, posterior/strain reading,
sampler, waveform, download, installation, activation or witness generation.
"""
import argparse
import hashlib
import json
import math
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent
ORDER = 'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
SOURCES = [ORDER] + ['ORDEM_013_RINGDOWN/'+p for p in [
    'RINGDOWN_5SIGMA_V1.json', 'bis/PART_B_BUDGET_START.json',
    'bis/e3_blind_prepare/CANDIDATES_SORTED.json', 'bis/e3_blind_prepare/EXPECTED_INFORMATION.json',
    'bis/e3_blind_prepare/FINITE_INTERFACE_CHECKS.json', 'bis/e3_blind_prepare/TWO_PHASE_HASH_SEQUENCE.md',
    'bis/e0_metadata/GWOSC_EVENTS.csv', 'bis/E0_SNR_INFORMATION_FIT.json', 'bis/E0_SNR_FIT_REVIEW.md',
    'bis/e0_core/E0_CORE.json', 'bis/e3_publication_refresh/PUBLICATION_METADATA_REVIEW_INDEX.json',
    'bis/e3_pilot_failure_diagnostic/DIAGNOSIS.json', 'bis/e3_pilot_failure_diagnostic/SOURCE_HASH_ADDENDUM.json',
    'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSTIC_INDEPENDENT_REVIEW.json',
    'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json',
    'bis/e3_kerr_failure_diagnostic/DIAGNOSTIC.json',
    'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json',
    'cache/E3_KERR220_CALIBRATION_V1/COST.json', 'cache/E3_KERR220_CALIBRATION_V2/COST.json',
    'cache/E3_PSEOB_PILOT_V1/CONTROLLER.json', 'cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json',
    'bis/F2_INJECTION_INDEPENDENT_REVIEW.md',
    'bis/e3_allocation_prepare/CONTRACT_SCHEMA.json', 'bis/e2_code/registration_guard.py',
]]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_bytes())
def put(path, obj):
    if isinstance(obj, bytes): raw = obj
    elif isinstance(obj, str): raw = obj.encode('utf-8')
    else: raw = (json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if path.stat().st_size != len(raw): raise OSError('Incomplete output')
def require(condition, message):
    if not condition: raise ValueError(message)
def frozen(rel): return HERE/'frozen_inputs'/'ORDEM_013_RINGDOWN'/rel
def load(rel): return read(frozen(rel))

def validate(candidate, jobs):
    require(candidate['status'] == 'CANDIDATE_AWAITING_INDEPENDENT_REVIEW_NOT_ACTIVE', 'Inactive status')
    require(candidate['registered_utc'] is None and candidate['witness_relative_to_Chatgpt'] is None, 'No activation')
    require(jobs['jobs'] == {} and jobs['downloads'] == {}, 'No new jobs/downloads')
    require(candidate['allocation']['new_PE_count'] == candidate['allocation']['new_injection_count'] == 0, 'Zero allocation')
    require(candidate['cost_per_converged_IMR_posterior_seconds'] is None, 'Unknown cost must remain null')
    require(len(candidate['alternatives']) == 5, 'All five alternatives')
    require(len(candidate['events']) == 14 and sum(e['data_quality_hold'] for e in candidate['events']) == 4, '14/10/4')
    require(len(candidate['Ncalib']['readings']) == 10, 'All ten readings')
    require(all(e['allocated_PE_jobs'] == 0 and e['admission'] is None for e in candidate['events']), 'No admission')
    w = candidate['wall_accounting']
    require(0 <= w['finalization_reserve_seconds'] <= 7200, 'Bounded reserve')
    require(math.isclose(w['elapsed_seconds'] + w['remaining_seconds'], 144000, abs_tol=1e-6), '40h identity')
    require(math.isclose(w['finalization_reserve_seconds'] + w['unused_science_seconds_released_not_spent'], w['remaining_seconds'], abs_tol=1e-6), 'Returned wall identity')
    require(datetime.fromisoformat(w['finalization_stop_utc']) <= datetime.fromisoformat(w['hard_deadline_utc']), 'Final stop')

def verify():
    manifest = read(HERE/'MANIFEST.json')
    for row in manifest['files']:
        path = HERE/row['relative_path']
        require(sha(path) == row['sha256'], 'Artifact changed: '+row['relative_path'])
    inputs = read(HERE/'FROZEN_INPUTS.json')
    for row in inputs['files']:
        require(sha(ROOT/row['source_relative_to_Chatgpt']) == row['sha256'], 'Source changed: '+row['source_relative_to_Chatgpt'])
        require(sha(HERE/row['frozen_relative_path']) == row['sha256'], 'Frozen input changed')
    candidate = read(HERE/'ORCAMENTO_40H_CANDIDATE.json')
    jobs = read(HERE/'ZERO_JOBS_V2_CANDIDATE.json')
    validate(candidate, jobs)
    require(sha(HERE/'ZERO_JOBS_V2_CANDIDATE.json') == candidate['jobs_sha256'], 'Jobs pin')
    print(json.dumps({'status':'VERIFIED_READ_ONLY', 'artifacts':len(manifest['files']),
                      'frozen_inputs':len(inputs['files']), 'candidate_sha256':sha(HERE/'ORCAMENTO_40H_CANDIDATE.json')}))

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--verify', action='store_true'); args = parser.parse_args()
    if args.verify: return verify()
    require(not (HERE/'FROZEN_INPUTS.json').exists(), 'Exclusive new candidate only')
    frozen_rows = []
    for rel in SOURCES:
        source = (ROOT/rel).resolve()
        require(source.is_relative_to(ROOT.resolve()), 'Outside Chatgpt')
        require(source.stat().st_size <= 25*1024*1024, 'Source over25MB')
        raw = source.read_bytes(); target = HERE/'frozen_inputs'/rel
        put(target, raw)
        frozen_rows.append({'source_relative_to_Chatgpt':rel, 'frozen_relative_path':target.relative_to(HERE).as_posix(),
                            'sha256':hashlib.sha256(raw).hexdigest(), 'bytes':len(raw)})
    reg = load('RINGDOWN_5SIGMA_V1.json'); regsha = sha(frozen('RINGDOWN_5SIGMA_V1.json'))
    candidates = load('bis/e3_blind_prepare/CANDIDATES_SORTED.json')
    expected = load('bis/e3_blind_prepare/EXPECTED_INFORMATION.json')
    core = load('bis/e0_core/E0_CORE.json')
    budget = load('bis/PART_B_BUDGET_START.json')
    diag = load('bis/e3_pilot_failure_diagnostic/DIAGNOSIS.json')
    closing = load('bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json')
    pilot = load('cache/E3_PSEOB_PILOT_V1/CONTROLLER.json')
    k1 = load('cache/E3_KERR220_CALIBRATION_V1/COST.json'); k2 = load('cache/E3_KERR220_CALIBRATION_V2/COST.json')
    kr = load('bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json')
    checks = []
    def check(name, condition):
        require(condition, name); checks.append({'name':name, 'passed':True})
    check('E2 matches candidates', candidates['E2']['sha256'] == regsha)
    check('E2 matches diagnostic', diag['original']['controller']['registration_sha256'] == regsha)
    check('Independent diagnosis closed', closing['status'] == 'BOUNDED_DIAGNOSIS_CLOSED_TECHNICAL_WALL_NO_SUPPORTED_PE_ADAPTER' and closing['diagnostic_closure_blocking_findings'] == [])
    for ref in [expected['fit_source'], expected['fit_review'], candidates['publication_refresh_index']]:
        check('source pin '+ref['relative_to_Chatgpt'], sha(ROOT/ref['relative_to_Chatgpt']) == ref['sha256'])
    for name, digest in reg['own_code_tree_sha256'].items():
        check('frozen E2 '+name, sha(B/'bis/e2_code'/name) == digest)
    fits = {f['population']:f for f in expected['fits_preserved']}
    events = []
    for c in candidates['candidates']:
        event = c['event']; registered = reg['test_candidates'][event]
        check('hold '+event, registered['data_quality_hold'] == c['data_quality_hold'])
        check('publication '+event, c['published_deformation_at_registration'] is False)
        check('SNR source '+event, sha(ROOT/c['SNR_source']['relative_to_Chatgpt']) == c['SNR_source']['sha256'])
        weights = [r for r in expected['rows'] if r['event'] == event]
        check('two weights '+event, len(weights) == 2)
        for w in weights:
            fit = fits[w['fit_population']]; a,b = fit['coefficients_log_intercept_slope']; s=fit['residual_sigma_ln_ddof_Nminus2']
            mu=a+b*math.log(c['SNR_network'])
            check('proxy '+event+w['fit_population'], math.isclose(math.exp(-2*mu), w['inverse_squared_conditional_median_proxy'], rel_tol=1e-12))
            check('expectation '+event+w['fit_population'], math.isclose(math.exp(-2*mu+2*s*s), w['expected_inverse_variance_lognormal_s_fixed'], rel_tol=1e-12))
        events.append({'event':event, 'SNR_network':c['SNR_network'], 'SNR_source':c['SNR_source'],
            'data_quality_hold':c['data_quality_hold'], 'registered_eligible':c['registered_eligible'],
            'published_deformation_at_registration':False, 'publication_scope':c['publication_census_scope'],
            'metadata_review':c['publication_metadata_review'], 'admission':None, 'allocated_PE_jobs':0,
            'information_per_hour':None, 'conditional_expected_weights':weights})
    populations = []
    for pop in fits:
        sums = {}
        for group, rows in [('all14',events), ('unheld10',[e for e in events if not e['data_quality_hold']]), ('held4',[e for e in events if e['data_quality_hold']])]:
            weights=[next(w for w in e['conditional_expected_weights'] if w['fit_population']==pop) for e in rows]
            sums[group] = {'N':len(rows), 'sum_inverse_squared_conditional_median_proxy':sum(w['inverse_squared_conditional_median_proxy'] for w in weights),
                'sum_expected_inverse_variance_lognormal_s_fixed':sum(w['expected_inverse_variance_lognormal_s_fixed'] for w in weights),
                'joint_uncertainty':None, 'uncertainty_status':'Shared fit coefficients; intervals cannot be treated as independent. Full fit covariance/row intervals preserved; no new bootstrap.',
                'realized_new_information':0, 'status':'CONDITIONAL_ARITHMETIC_NOT_POWER_OR_INFORMATION_GAIN'}
        reach=[]
        for reading, row in core['combinations'][pop]['std_ddof1'].items():
            target=row.get('I_tau_target90'); sub=row.get('analytic_small_effect_below_1e12_inverse',False)
            usable=target is not None and math.isfinite(target) and target>0 and not sub
            reach.append({'reading':reading, 'I_target90_conditional':target if usable else None,
                'analytic_subresolution_only':{'I_target90':target} if sub else None,
                'fraction_unheld10_of_conditional_target':sums['unheld10']['sum_expected_inverse_variance_lognormal_s_fixed']/target if usable else None,
                'fraction_interpretation':'Descriptive scalar information ratio using E0 offset-zero planning target; not test power. No event-specific blind signal, nuisance or selection calibration.',
                'N_target_operational':None})
        populations.append({'fit_population':pop, 'sums':sums, 'conditional_target_context':reach})
    ncalib=[]
    for row in core['systematics']:
        delta=row['delta_reference_fresh_GW250114']; reading=row['reading']
        sub=bool(core['combinations']['GWTC5_31']['std_ddof1'][reading].get('analytic_small_effect_below_1e12_inverse',False))
        valid=delta is not None and delta != 0 and not sub
        coeff5=25/(delta*delta) if delta is not None and delta != 0 else None
        coeff15=225/(delta*delta) if delta is not None and delta != 0 else None
        ncalib.append({'reading':reading,'delta_reference_GW250114':delta,
            'source_pointer':'/systematics/'+str(core['systematics'].index(row)),
            'coefficient_Ncalib_per_sigma_inj_squared_floor5':coeff5 if valid else None,
            'coefficient_Ncalib_per_sigma_inj_squared_floor15':coeff15 if valid else None,
            'analytic_subresolution_coefficients_only':{'floor5':coeff5,'floor15':coeff15} if sub else None,
            'status':'DERIVED_CONDITIONAL_MEAN_PRECISION_ONLY' if valid else ('SUBRESOLUTION_NOT_OPERATIONAL' if sub else 'OPEN_NO_NONZERO_UNIQUE_EFFECT'),
            'N_target_operational':None,'allocated_injections':0,
            'illustrative_sigma_INPUT_from_order':[
                {'sigma_inj':s,'N_per_cell_floor5_continuous':coeff5*s*s,'N_per_cell_floor5_ceiling':math.ceil(coeff5*s*s),
                 'N_ten_cells_floor5_ceiling':10*math.ceil(coeff5*s*s),'wall_cost_seconds':None}
                for s in (.0497,.058,.24)] if valid else []})
    alternatives=[
        ('i','Calibrar apenas pisos R-LIN/R-MOD','Coeficientes recalculados abaixo; nenhum sigma_inj/custo de recuperação qualificada medido. Piso mais largo não corrige falha nativa.'),
        ('ii','Calibrar somente bins de SNR alto','Menor largura é expectativa condicional; viés abaixo do piso não demonstrado. Nenhum bin ou evento admitido por este candidato.'),
        ('iii','PE reduzida com amplitude marginalizada','Alternativa metodológica da ordem; instrumento diferente, sem implementação/custo/convergência validados neste escopo. Nenhum workaround executado.'),
        ('iv','Reutilizar injeções públicas LVK','Diagnóstico F2 existente revisado pode ser reutilizado descritivamente; duas recuperações com/sem44 não são curva c(SNR), cobertura repetida nem sigma_sys calibrado. Zero PE nova.'),
        ('v','pSEOBNRv5PHM via pyseobnr em venv próprio','Instalabilidade, custo e qualificação não medidos aqui; sem instalação, rebuild ou troca de runtime. Custo permanece null.')]
    alternatives=[{'id':i,'description':d,'decision':'ZERO_NEW_COMPUTE_ALLOCATION','allocated_wall_seconds':0,
                   'estimated_wall_seconds_for_qualified_program':None,'status':'NAO_PAGO_AS_E3_3_CALIBRATION','reason':reason} for i,d,reason in alternatives]
    now=datetime.now(timezone.utc); start=datetime.fromisoformat(budget['started_utc']); deadline=datetime.fromisoformat(budget['hard_deadline_utc'])
    elapsed=(now-start).total_seconds(); remaining=(deadline-now).total_seconds()
    require(0<=elapsed<144000 and remaining>=7200,'Cannot reserve full2h inside existing deadline')
    wall={'measured_utc':now.isoformat(),'started_utc':start.isoformat(),'hard_deadline_utc':deadline.isoformat(),
          'elapsed_seconds':elapsed,'remaining_seconds':remaining,'elapsed_hours':elapsed/3600,'remaining_hours':remaining/3600,
          'finalization_reserve_seconds':7200,'finalization_stop_utc':(now+timedelta(seconds=7200)).isoformat(),
          'finalization_scope':'Independent review, accounting, E6/E7/document integration only; no scientific rerun or pipeline repair.',
          'unused_science_seconds_released_not_spent':remaining-7200,'unused_science_hours_released_not_spent':(remaining-7200)/3600,
          'reserve_spent_seconds':0,'accounting':'Continuous shared wall since PartB start. Job/CPU costs below are explanatory and NOT added to elapsed wall. Returned allocation is not computational expenditure or extension of deadline.',
          'activation_condition':'Reserve starts at this recorded preparation clock and is not reset on review/activation. Any delay reduces remaining reserve; refresh only by explicit versioned accounting, never deadline extension.'}
    jobs={'schema_version':'E2_PE_JOBS_V2','parent_registration_sha256':regsha,'jobs':{},'downloads':{},
          'status':'INACTIVE_ZERO_JOB_CANDIDATE_NOT_A_WITNESS'}
    put(HERE/'ZERO_JOBS_V2_CANDIDATE.json',jobs)
    candidate={'schema_version':'E3_BUDGET_WALL_CANDIDATE_V1','status':'CANDIDATE_AWAITING_INDEPENDENT_REVIEW_NOT_ACTIVE',
       'created_utc':now.isoformat(),'parent_registration_sha256':regsha,'registered_utc':None,'witness_relative_to_Chatgpt':None,
       'jobs_relative_to_Chatgpt':(HERE/'ZERO_JOBS_V2_CANDIDATE.json').relative_to(ROOT).as_posix(),
       'jobs_sha256':sha(HERE/'ZERO_JOBS_V2_CANDIDATE.json'),
       'decision':'Close this E3.1 IMR attempt as measured native instrument wall; allocate zero new PE/injections. Not a general impossibility claim.',
       'independent_native_closing_review':{'relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json',
           'sha256':sha(frozen('bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json')),
           'status':closing['status'],'check_count':closing['check_count'],'closed_findings':closing['closed_findings'],
           'continuation_blocking_findings':closing['continuation_blocking_findings']},
       'allocation':{'new_PE_count':0,'new_injection_count':0,'new_download_count':0,'new_science_wall_seconds':0,'pipeline_repair_seconds':0,
                     'finalization_max_seconds':7200,'event_count_metadata':14,'unheld_candidates':10,'held_candidates':4},
       'cost_per_converged_IMR_posterior_seconds':None,'posterior_cost_status':'NOT_ESTIMABLE_FROM_FAILED_INITIALIZATION; Kerr posterior is a different instrument.',
       'wall_accounting':wall,
       'measured_costs':{
           'Kerr_V1':k1,'Kerr_V2':k2,'Kerr_V1_V2_controller_sum_seconds':k1['wall_seconds']+k2['wall_seconds'],
           'Kerr_V1_V2_CPU_sum_seconds':k1['children_cpu_seconds']+k2['children_cpu_seconds'],
           'Kerr_review_status':kr['status'],'Kerr_equivalent_reproduction_paid':kr['equivalent_reproduction_paid'],
           'Kerr_cost_scope':'Nonblind Kerr calibration; V1 partial and V2 completed. Aggregates overlap component runs; do not sum twice or transfer to IMR deformation cost.',
           'Kerr_Welch_separate_diagnostic':load('bis/e3_kerr_failure_diagnostic/DIAGNOSTIC.json')['cost'],
           'IMR_pilot_failed_controller':pilot,'IMR_native_diagnostic':diag['cost'],
           'other_PartB_computation_itemized_here':False,'other_work_accounting':'Already included by continuous elapsed wall; this candidate does not invent a complete per-job ledger.'},
       'alternatives':alternatives,'events':events,'information_summaries':populations,
       'information_model':{'formula':expected['formula'],'fits_preserved':expected['fits_preserved'],
          'coefficient_intervals':expected['coefficient_intervals'],'stored_bootstrap_grid_preserved':expected['stored_bootstrap_grid_preserved'],
          'scope':'Existing E0 published-width conditional planning fit. Proxy sigma_median^-2 differs from E[sigma^-2]; no candidate posterior reads, no cost/hour ranking, no physical information gain.'},
       'Ncalib':{'formula':'N_continuous=(sigma_inj/(abs(delta)/k))^2 = (k^2/delta^2)*sigma_inj^2; k=5 or15',
          'assumptions':'Independent identically distributed finite-variance unbiased estimator of a common mean within each cell; not verified for new injections. Does not calibrate a5sigma tail or unknown family bias.',
          'source':'bis/e0_core/E0_CORE.json/systematics; illustrative sigma inputs from ORDEM_013BIS line194, not measurements of this instrument.',
          'ten_cells':'Five SNR bins times two families is minimum design count from order, not ten populated cells.', 'readings':ncalib},
       'E3_3_status':{'new_GR_pSEOB_injections':0,'new_GR_XPHM_injections':0,'new_TGL_injections':0,
          'sigma_c':None,'sigma_sys_df':None,'coverage':None,'calibration_paid':False,'gate_green':False,
          'TGL_identifiability':'Free dtau recovery is not TGL injection; per-reading a0/a1 map and correlated truth required. NonGR XPHM second-family injection is not implemented/qualified.'},
       'activation_constraints':['Candidate is deliberately not active: null registration/witness must fail frozen loader.',
          'Independent review must precede any principal-issued active accounting receipt/witness.',
          'Empty jobs extends nothing and DOES NOT revoke original static pilot job/downloads retained by load_jobs/load_authorized_configuration. Principal must not relaunch failed pilot; original output exclusivity/deadline remain.',
          'No fabricated jobs, hashes, admission, provider checksums or new witness. Active ORCAMENTO_40H remains untouched.'],
       'limitations':['Measured failure of this instrument/configuration/runtime; not universal computational or physical impossibility.',
          'No converged IMR posterior, no dtau comparison to release, no calibrated per-event cost, no information/hour ranking.',
          '14 scoped publication-absence candidates do not mean universal unpublished status. Holds retained; no new admission.',
          'Zero future science allocation is a decision, not zero predicted cost of qualified science. Such costs remain null.']}
    check('Kerr sum matches reviewed receipt',math.isclose(candidate['measured_costs']['Kerr_V1_V2_controller_sum_seconds'],kr['cost_review']['V1_plus_V2_controller_wall_seconds'],abs_tol=1e-9))
    validate(candidate,jobs)
    # Finite negative contract controls, in-memory only.
    for label,mutate in [('nonempty_jobs',lambda c,j:j['jobs'].update({'FAKE':{}})),
                          ('fabricated_cost',lambda c,j:c.update(cost_per_converged_IMR_posterior_seconds=0)),
                          ('activation',lambda c,j:c.update(registered_utc=now.isoformat()))]:
        c=json.loads(json.dumps(candidate));j=json.loads(json.dumps(jobs));mutate(c,j)
        try: validate(c,j)
        except ValueError: checks.append({'name':'negative '+label,'passed':True})
        else: raise ValueError('Negative fixture accepted:'+label)
    put(HERE/'ORCAMENTO_40H_CANDIDATE.json',candidate)
    put(HERE/'FROZEN_INPUTS.json',{'created_utc':now.isoformat(),'files':frozen_rows,'source_limit_bytes':25*1024*1024,'copies':'Byte-identical; no posterior or strain payloads copied.'})
    put(HERE/'FINITE_CHECKS.json',{'status':'PASS','checks':checks,'no_scientific_execution':True})
    table='\n'.join('| '+e['event']+' | '+str(e['SNR_network'])+' | '+('HOLD' if e['data_quality_hold'] else 'sem hold')+' | '+' | '.join(f"{w['inverse_squared_conditional_median_proxy']:.3f} / {w['expected_inverse_variance_lognormal_s_fixed']:.3f}" for w in e['conditional_expected_weights'])+' |' for e in events)
    text=f'''# E3.2 — candidato de orçamento por parede instrumental

**INATIVO, para revisão independente antes de qualquer ativação.** Nova PE=0; novas injeções=0; downloads=0; rebuild/workaround=0. Encerra esta tentativa E3.1 IMR por falha nativa medida, sem afirmar impossibilidade geral. Custo por posterior IMR convergido=null, não11s. Kerr não substitui qualificação da recuperação de deformações.

Relógio em {now.isoformat()}: {elapsed/3600:.6f}h decorridas; {remaining/3600:.6f}h restantes. Reserva final máxima2h, encerrando em {(now+timedelta(seconds=7200)).isoformat()}; {((remaining-7200)/3600):.6f}h de ciência não alocadas/devolvidas, **não gastas**. Deadline global {deadline.isoformat()} intacto. A reserva não reinicia na ativação; atraso de revisão consome-a. Contabilidade contínua inclui orquestração e todos os trabalhos; não somar novamente custos dos jobs abaixo.

Kerr V1 {k1['wall_seconds']:.6f}s +V2 {k2['wall_seconds']:.6f}s de controladores = {k1['wall_seconds']+k2['wall_seconds']:.6f}s; CPU {k1['children_cpu_seconds']+k2['children_cpu_seconds']:.6f}s. São calibração não cega, equivalent_reproduction_paid=false. Piloto IMR falhou em {pilot['wall_seconds']:.6f}s. Diagnóstico nativo: {diag['cost']['sum_child_wall_seconds']:.6f}s wall somado, {diag['cost']['sum_child_CPU_seconds']:.6f}s CPU,10processos/16chamadas. Diagnóstico Welch consta separado no JSON. Tempos de launcher/runner/componentes se sobrepõem; não somar com total do controlador.

## Cinco alternativas exigidas (ORDEM:194)

'''+ '\n\n'.join(f"{a['id']}. **{a['description']}** — {a['reason']} Alocação0; custo de programa qualificado=null/NÃO PAGO." for a in alternatives)+f'''

##14 candidatos,10 sem hold e4 com hold

Ausência de publicação é limitada ao censo auditado; elegibilidade documental não é admissão. Cada entrada conserva fonte SNR/path/linha/hash, reviews e flags. Nenhum hold removido. Pesos abaixo: **proxy / E[I]**, respectivamente exp(−2μ) e exp(−2μ+2s²). Ajustes31/33 não são somados entre si; covariância dos coeficientes e intervalos preservados no JSON. Erros de seleção/transferência, s, SNR e nova família permanecem abertos. Sem leitura de posterior candidato.

| Evento | SNR | Flag | Ajuste31 proxy/E[I] | Ajuste33 proxy/E[I] |
|---|---:|---|---:|---:|
{table}

Somas condicionais e frações dos alvos E0 constam do JSON por ajuste, separando10/4/14. Não são poder, ganho realizado ou evidência física. A incerteza conjunta não é a soma de erros independentes. Não há ranking por custo/hora.

## Ncalib e alcance

N=(k²/δ²)σ_inj², k5/15. Coeficientes das10 leituras recalculados dos deltas E0; σ=.0497/.058/.24 são INPUTs ilustrativos da ordem, não resultados deste piloto. Cinco bins×duas famílias é desenho mínimo, não matriz paga. Contas pressupõem média sem viés de replicações independentes de variância finita; não pagam cauda5σ ou viés desconhecido. Leituras subresolução ficam com N_target_operational=null e coeficientes analíticos separados. Nenhum N ilustrativo vira job/alocação.

GR nas duas famílias, TGL por leitura, c(SNR), sigma_sys(df), cobertura e440 não foram calibrados por nova PE: NÃO PAGO. dtau livre na recuperação não equivale a injeção TGL; família alternativa nãoGR permanece não implementada. Gate não verde.

## Esquema, preservação e revisão

`ORCAMENTO_40H_CANDIDATE.json` usa esquema documental próprio; registered_utc/witness=null tornam-no deliberadamente não ativável. `ZERO_JOBS_V2_CANDIDATE.json` tem contrato E2_PE_JOBS_V2 com jobs={{}} e downloads={{}} e parentE2 pinado. **Empty jobs não revoga o piloto estático nem downloads originais**: o guard agrega. Não relançar piloto. O principal integra o fechamento documental após revisão independente; nenhum registro, testemunha ou ORCAMENTO ativo foi escrito aqui. Serializer opcional anterior não foi usado/importado.

`frozen_inputs/` contém cópias byte a byte dos metadados/fontes selecionados; `FROZEN_INPUTS.json` dá pins e origens. Nenhum posterior/strain/pickle. Fontes limitadas25MB. `FINITE_CHECKS.json`: {len(checks)} controles positivos/negativos, sem experiências. Todos os arquivos escritos enumerados em `MANIFEST.json` (auto-hash omitido para evitar circularidade).

Verificação somente leitura:

```powershell
C:\\Python314\\python.exe -B "{HERE/'build_budget_wall.py'}" --verify
```
'''
    put(HERE/'CANDIDATE.md',text)
    # Recheck copied sources before finalization; fail visibly on concurrent edits.
    for row in frozen_rows: require(sha(ROOT/row['source_relative_to_Chatgpt'])==row['sha256'],'Source changed during preparation')
    put(HERE/'MANIFEST.json',{'created_utc':datetime.now(timezone.utc).isoformat(),
        'files':[{'relative_path':p.relative_to(HERE).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(HERE.rglob('*')) if p.is_file()],
        'self':'MANIFEST.json: no circular self hash','status':'INACTIVE_REVIEW_PACKAGE'})
    verify()

if __name__=='__main__': main()
