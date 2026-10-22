"""E6 sidecar: copy reviewed JSON fields, never calculate scientific values.

Prepared only. Activation plus reviewed E3.2/E3.3/TEST receipts are mandatory.
No posterior, strain, seeds, model imports, PE, MC, rates or waveform calculation.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import re
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
LIMIT = 25 * 1024 * 1024
ROUTES = ('TAU220_POPULATION', 'TAU440_FIXED_SOURCE_FISHER', 'DF220_POPULATION_WIDTH_IV')
GROUPS = ('O4_HOJE', 'O4_CEGO', 'O4C_GWTC6', 'O5_BANDA', 'ET', 'CE')
METRICS = ('z_expected_conditional', 'N90_information_target', 'N90_count_scenario',
           'GW250114_equivalents', 'delta', 'sigma', 'correction_over_sigma',
           'rate_per_year', 'rate_CI', 'z_physical', 'lnB')
GATE_FIELDS = ('sigma_c_calibrated', 'floor5_INPUT', 'floor15_sensitivity',
               'sigma_sys_df', 'sigma_jit_recovered', 'correction_over_sigma_physical')
STAGES = ('E3.2', 'E3.3', 'TEST')
PAID_FLAGS = ('physical_calibration_paid', 'null_calibration_paid', 'selection_paid',
              'normalization_paid', 'independent_review_passed')
FUTURE_GROUPS = ('O4C_GWTC6', 'O5_BANDA', 'ET', 'CE')
EVIDENCE_VERDICTS = ('NOT_FALSIFIED_UNDERPOWERED', 'NOT_FALSIFIED_POWERED',
                     'EXCLUDED_IN_READING', 'FALSIFIED_IN_READING')
# Labels are semantic types, not conversion instructions. No automatic conversion.
SEMANTIC_UNITS = {
    'TAU220_POPULATION': {
        'z_expected_conditional': ('dimensionless','dimensionless_conditional','dimensionless_optimistic'),
        'N90_information_target': ('sum_inverse_variance_dtau',),
        'N90_count_scenario': ('event_count','events_illustrative','events_illustrative_only'),
        'GW250114_equivalents': ('target_equivalents_sigma_tau_0.058','current_equivalents_sigma_tau_0.058'),
        'delta': ('fractional_dtau220',), 'sigma': ('fractional_dtau220','fractional_dtau220_illustrative'),
        'correction_over_sigma': ('dimensionless','dimensionless_common_weighted'),
        'rate_per_year': ('per_year',), 'rate_CI': ('per_year_CI90',),
        'z_physical': ('dimensionless',), 'lnB': ('dimensionless',),
        'sigma_c_calibrated': ('fractional_dtau220',), 'floor5_INPUT': ('fractional_dtau220',),
        'floor15_sensitivity': ('fractional_dtau220',), 'sigma_sys_df': (), 'sigma_jit_recovered': (),
        'correction_over_sigma_physical': ('dimensionless',)},
    'TAU440_FIXED_SOURCE_FISHER': {
        'z_expected_conditional': ('dimensionless','dimensionless_local_GR'),
        'N90_information_target': ('sum_inverse_variance_dtau440',),
        'N90_count_scenario': ('event_count','continuous_identical_source_count'),
        'GW250114_equivalents': ('current_dtau440_information_equivalents','target_dtau440_information_equivalents'),
        'delta': ('fractional_dtau440',), 'sigma': ('fractional_dtau440',),
        'correction_over_sigma': ('dimensionless','absolute_delta_over_sigma_local_GR'),
        'rate_per_year': ('per_year',), 'rate_CI': ('per_year_CI90',),
        'z_physical': ('dimensionless',), 'lnB': ('dimensionless',),
        'sigma_c_calibrated': ('fractional_dtau440',), 'floor5_INPUT': ('fractional_dtau440',),
        'floor15_sensitivity': ('fractional_dtau440',), 'sigma_sys_df': (), 'sigma_jit_recovered': (),
        'correction_over_sigma_physical': ('dimensionless',)},
    'DF220_POPULATION_WIDTH_IV': {
        'z_expected_conditional': ('dimensionless',),
        'N90_information_target': ('local_information_variance_df220',),
        'N90_count_scenario': ('event_count','scenario_events_lower_bound'),
        'GW250114_equivalents': ('current_df_variance_information_equivalents','target_df_variance_information_equivalents'),
        'delta': ('fractional_df220',), 'sigma': ('width_fractional_df220',),
        'correction_over_sigma': ('dimensionless',),
        'rate_per_year': ('per_year',), 'rate_CI': ('per_year_CI90',),
        'z_physical': ('dimensionless',), 'lnB': ('dimensionless',),
        'sigma_c_calibrated': (), 'floor5_INPUT': (), 'floor15_sensitivity': (),
        'sigma_sys_df': ('width_fractional_df220',), 'sigma_jit_recovered': ('width_fractional_df220',),
        'correction_over_sigma_physical': ('dimensionless',)}
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def load(path):
    require(Path(path).stat().st_size <= LIMIT, 'JSON exceeds 25 MiB')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key: '+key)
            result[key] = value
        return result
    obj = json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                     parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
    def finite(value):
        if isinstance(value, float): require(math.isfinite(value), 'Nonfinite JSON')
        elif isinstance(value, dict):
            for x in value.values(): finite(x)
        elif isinstance(value, list):
            for x in value: finite(x)
    finite(obj)
    return obj


def pinned(ref):
    require(isinstance(ref, dict) and set(ref) == {'path', 'sha256'}, 'Pin contract')
    relative = Path(ref['path'])
    require(not relative.is_absolute(), 'Absolute custody path prohibited')
    p = (ROOT/relative).resolve()
    require(p.is_relative_to(ROOT.resolve()) and p.suffix.lower() in ('.json', '.md'), 'Reviewed JSON/MD paths only')
    require(not any(part.upper() == 'E2_PRIVATE' for part in p.parts), 'Private inputs prohibited')
    require(re.fullmatch('[0-9a-f]{64}', ref['sha256']) and sha(p) == ref['sha256'], 'Pin mismatch: '+str(p))
    return p


def utc(text):
    require(isinstance(text, str), 'Timestamp required')
    value = datetime.fromisoformat(text.replace('Z', '+00:00'))
    require(value.utcoffset() is not None, 'Timezone required')
    return value.astimezone(timezone.utc)


def pointer(obj, path):
    require(isinstance(path, str) and (path == '' or path.startswith('/')), 'JSON pointer required')
    value = obj
    if path:
        for part in path[1:].split('/'):
            part = part.replace('~1', '/').replace('~0', '~')
            value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def missing(reason, unit='OPEN_NOT_ASSIGNED'):
    return dict(value=None, status='OPEN', unit=unit, source=None, reason=reason)


def copy_metric(sources, alias, path, unit, scope, optional=False):
    ref, obj = sources[alias]
    try:
        value = pointer(obj, path)
    except (KeyError, IndexError):
        require(optional, 'Missing required source field: '+alias+path)
        value = None
    return dict(value=value, status='OPEN' if value is None else 'INPUT_CONDITIONAL_COPIED',
                unit=unit, source=dict(**ref, pointer=path), reason=scope)


def new_scenario(identity, scope):
    return dict(id=identity, scope=scope, metrics={k:missing('NO_REVIEWED_COMPATIBLE_FIELD') for k in METRICS},
                gate=dict(color='OPEN', status='OPEN_NOT_PHYSICALLY_CALIBRATED',
                          **{k:missing('NO_REVIEWED_CALIBRATION') for k in GATE_FIELDS}),
                verdict='AWAITING_DATA', physical_test_present=False, references=[])


def check_metric(name, value, route=None):
    require(set(value) == {'value','status','unit','source','reason'}, 'Metric shape')
    require(all(isinstance(value[k], str) and value[k] for k in ('status','unit','reason')), 'Metric labels')
    data=value['value']
    if data is None:
        require(value['status'] == 'OPEN', 'Null must remain OPEN')
    else:
        if name == 'rate_CI':
            require(isinstance(data,list) and len(data)==2 and
                    all(type(v) in (int,float) for v in data) and 0<=data[0]<=data[1], 'Rate CI endpoints')
        else:
            require(type(data) in (int,float), 'Metric must be a number or null')
        require(value['source'] is not None, 'Numerical value without source')
        if route is not None:
            require(route in SEMANTIC_UNITS and name in SEMANTIC_UNITS[route]
                    and value['unit'] in SEMANTIC_UNITS[route][name], 'Incompatible semantic unit: '+route+'/'+name)


def check_timeline(receipt, predecessor, predecessor_ref, activation_floor, authorization_time):
    """Check documentary source times, separately from later adapter issuance.

    Hashes bind reviewed evidence, not independent proof of physical execution.
    A pre-existing operator GO may predate E2; effective activity may not.
    """
    require(receipt['predecessor'] == predecessor_ref, 'Stage predecessor pin differs')
    timeline=receipt['timeline'];evidence=load(pinned(timeline['evidence']))
    kind=timeline['kind'];issued=utc(receipt['issued_utc'])
    require(activation_floor<=issued<=authorization_time, 'Stage receipt predates E2 activation')
    if predecessor is not None:
        require(utc(predecessor['issued_utc'])<=issued, 'Adapter receipts out of order')
        linked=pointer(evidence,timeline['predecessor_evidence_sha256_pointer'])
        require(linked==predecessor['timeline']['evidence']['sha256'], 'Source predecessor evidence pin differs')
    if kind=='NO_EXECUTION':
        require(receipt['outcome'] in ('PARTIAL','BLOCKED','UNAVAILABLE'), 'Completed stage cannot declare no execution')
        reason=pointer(evidence,timeline['reason_pointer'])
        require(isinstance(reason,str) and reason.strip(), 'No-execution wall must have a sourced reason')
        start=finish=utc(pointer(evidence,timeline['recorded_utc_pointer']))
    else:
        require(kind==('ALLOCATION_REGISTERED' if receipt['stage']=='E3.2' else 'EXECUTED'), 'Wrong stage activity type')
        require(receipt['outcome'] in ('COMPLETED','PARTIAL'), 'Blocked/unavailable stage must use no-execution wall')
        if predecessor is not None:
            require(predecessor['timeline']['kind']!='NO_EXECUTION', 'Execution cannot follow a missing prerequisite')
        start=utc(pointer(evidence,timeline['started_utc_pointer']))
        finish=utc(pointer(evidence,timeline['finished_utc_pointer']))
        authorized=utc(pointer(evidence,timeline['authorized_utc_pointer']))
        require(authorized<=start, 'Activity precedes its sourced authorization')
    require(activation_floor<=start<=finish<=issued<=authorization_time, 'Actual activity/wall chronology invalid')
    if predecessor is not None:
        require(predecessor['_verified_timeline']['finished_utc']<=start, 'TEST/calibration precedes prerequisite activity')
    return dict(started_utc=start,finished_utc=finish,kind=kind)


def activate(args):
    require(args.execute and args.authorization and args.authorization_sha256,
            'AWAITING_REVIEWED_E3_2_E3_3_TEST_AND_PRINCIPAL_ACTIVATION')
    require(sha(args.authorization) == args.authorization_sha256, 'Activation pin')
    auth = load(args.authorization)
    require(auth['status'] == 'AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST', 'Activation status')
    require(auth['new_scientific_computation_allowed'] is False, 'No scientific computations')
    package = {n:sha(HERE/n) for n in ('generate_reach_table.py','CONTRACT.json','SOURCE_PINS.json','OUTPUT_SCHEMA.json')}
    require(auth['package_sha256'] == package, 'E6 sidecar package changed')
    regpath = pinned(auth['registration']); reg = load(regpath)
    require(regpath == (BASE/'RINGDOWN_5SIGMA_V1.json').resolve(), 'Wrong E2 identity')
    require(reg['status'] == 'REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST', 'Unregistered E2')
    issued = utc(auth['issued_utc']); now = datetime.now(timezone.utc)
    require(utc(reg['registered_utc']) <= issued <= now, 'Invalid activation chronology')
    witness = pinned(auth['witness'])
    require(witness == (ROOT/reg['witness_relative_to_Chatgpt']).resolve() and
            witness.is_relative_to((ROOT/'TUNEL/DO_CHATGPT').resolve()), 'Witness location')
    require(re.findall(r'^registro_sha256: ([0-9a-f]{64})\s*$', witness.read_text(encoding='utf-8-sig'), re.M)
            == [auth['registration']['sha256']], 'Witness differs')
    contract = load(HERE/'CONTRACT.json')
    require(reg['readings'] == contract['readings'], 'All ten E2 readings/order required')
    sources = {}
    for alias, ref in load(HERE/'SOURCE_PINS.json')['sources'].items():
        sources[alias] = (ref, load(pinned(ref)))
    require(sources['E2'][0] == auth['registration'], 'Frozen E2 source differs')
    activation=sources['E2_ACTIVATION'][1]
    require(pinned(sources['E2_ACTIVATION'][0]) == (ROOT/reg['activation']['receipt_relative_to_Chatgpt']).resolve()
            and activation['status']=='E2_ACTIVATION_COMPLETE'
            and activation['registration_sha256']==auth['registration']['sha256']
            and activation['witness_sha256']==auth['witness']['sha256']
            and activation['review_application_sha256']==reg['activation']['review_application_sha256'],
            'E2 activation receipt mismatch')
    require(utc(activation['finished_utc'])<=issued, 'E6 predates E2 activation')
    require(set(auth['reviewed_stages']) == set(STAGES), 'All three reviewed stage receipts required')
    stages = {}
    for stage in STAGES:
        ref = auth['reviewed_stages'][stage]; receipt = load(pinned(ref))
        require(receipt['schema'] == 'E6_REVIEWED_STAGE_V2' and receipt['stage'] == stage and
                receipt['registration_sha256'] == auth['registration']['sha256'], 'Stage contract/E2 differs')
        require(receipt['outcome'] in ('COMPLETED','PARTIAL','BLOCKED','UNAVAILABLE'), 'Explicit stage outcome')
        require(utc(reg['registered_utc']) <= utc(receipt['issued_utc']) <= issued, 'Stage chronology')
        result = load(pinned(receipt['artifact'])); review = load(pinned(receipt['review']))
        require(review['status'] == 'ACCEPTED_FOR_E6_MAPPING' and review['stage'] == stage and
                review['registration_sha256'] == auth['registration']['sha256'] and
                review['artifact_sha256'] == receipt['artifact']['sha256'] and review['blocking_findings'] == [],
                'Review absent, mismatched or blocking')
        require(utc(receipt['issued_utc']) <= utc(review['reviewed_utc']) <= issued, 'Review chronology')
        require(review['bindings'] == receipt['bindings'], 'Review must pin exact field mapping')
        require(review['timeline']==receipt['timeline'] and review['predecessor']==receipt['predecessor'],
                'Review must cover exact timeline mapping and predecessor')
        require(review['outcome'] == receipt['outcome'], 'Review must accept the explicit outcome')
        require(isinstance(receipt['bindings'], list), 'Bindings list required')
        require(isinstance(review['reviewer'],str) and review['reviewer'].strip(), 'Named reviewer')
        previous=stages[STAGES[STAGES.index(stage)-1]] if stage!='E3.2' else (None,sources['E2_ACTIVATION'][0])
        receipt['_verified_timeline']=check_timeline(receipt,previous[0],previous[1],utc(activation['finished_utc']),issued)
        alias = 'STAGE_'+stage; sources[alias] = (receipt['artifact'], result)
        stages[stage] = (receipt, ref)
    require(re.fullmatch('[a-z][a-z0-9_]{0,47}',auth['run_id']), 'Run id')
    target = HERE/'runs'/auth['run_id']
    require(target.resolve().is_relative_to(HERE.resolve()) and not target.exists(), 'Existing/escaped run')
    return auth, reg, contract, sources, stages, target


def assemble_baselines(contract, sources):
    cells = {(route,reading,group):dict(route=route,reading=reading,data_group=group,
             reading_statute=contract['reading_statutes'][reading],scenarios=[],rate_contexts=[],notes=[])
             for route in ROUTES for reading in contract['readings'] for group in GROUPS}
    e0=sources['E0'][1];e4=sources['E4_RESULT'][1];e2=sources['E2'][1]
    def add(key,scenario): cells[key]['scenarios'].append(scenario)
    def bind(row,name,alias,path,unit,scope,optional=False):
        row['metrics'][name]=copy_metric(sources,alias,path,unit,scope,optional)
    for i,item in enumerate(e0['planning_targets']):
        reading=item['reading'];scope='NONBLIND_OFFSET_ZERO_PLANNING_ONLY_PROIBIDA_COMO_TESTE'
        row=new_scenario('E0_planning_'+str(i),scope);root='/planning_targets/'+str(i)
        for name,field,unit in (
            ('z_expected_conditional','z_signal_planning_offset_zero','dimensionless_conditional'),
            ('N90_information_target','I_tau_expected_target90','sum_inverse_variance_dtau'),
            ('N90_count_scenario','N90_mixture_illustration_not_selection','events_illustrative'),
            ('GW250114_equivalents','GW250114_equivalents_reference_sigma_0p058','target_equivalents_sigma_tau_0.058')):
            bind(row,name,'E0',root+'/'+field,unit,scope)
        row['population']=item['population'];row['notes']=['Archives may include earlier runs; not a pure O4 population','Not an operational N90 or test statistic']
        add(('TAU220_POPULATION',reading,'O4_HOJE'),row)
        row=new_scenario('E0_intercept_free_'+str(i),'CONDITIONAL_FREE_INTERCEPT_PLANNING')
        bind(row,'z_expected_conditional','E0',root+'/z_slope_free_intercept','dimensionless_conditional',row['scope'])
        bind(row,'N90_count_scenario','E0',root+'/N90_slope_illustration','events_illustrative',row['scope'])
        row['population']=item['population'];add(('TAU220_POPULATION',reading,'O4_HOJE'),row)
    for population,conventions in e0['all_calibration_combinations'].items():
        for reading,item in conventions['std_ddof1'].items():
            if reading == 'GR_FALSE_FALSIFIER':
                continue  # Named GR control is not an eleventh physical reading.
            require(reading in contract['readings'],'Unexpected calibration reading')
            path='/all_calibration_combinations/'+population+'/std_ddof1/'+reading
            row=new_scenario('E0_ratio_'+population,'NONBLIND_COMMON_WEIGHTED_CORRECTION_ONLY')
            for name,field,unit in (('delta','delta_weighted','fractional_dtau220'),('sigma','sigma_combined','fractional_dtau220'),
                                    ('correction_over_sigma','z_common','dimensionless_common_weighted'),
                                    ('GW250114_equivalents','GW250114_equivalents_tau_reference_0p058','current_equivalents_sigma_tau_0.058')):
                bind(row,name,'E0',path+'/'+field,unit,row['scope'],True)
            row['population']=population;add(('TAU220_POPULATION',reading,'O4_HOJE'),row)
    for i,item in enumerate(e4['E4_fisher']):
        group={'O4':'O4_HOJE','O5':'O5_BANDA','ET':'ET','CE':'CE'}[item['psd']]
        row=new_scenario('E4_fisher_'+str(i),'INPUT_FIXED_SOURCE_ISOLATED440_LOCAL_FISHER_NOT_PHYSICAL_Z')
        path='/E4_fisher/'+str(i)
        row['context']={k:item[k] for k in ('variant','profile','snr_route','rho_440_used','rho_440_O4_anchor_INPUT',
                                              'rho_440_equal_per_PSD_INPUT','snr_kind','power_scope')}
        for name,field,unit in (('z_expected_conditional','expected_local_z','dimensionless_local_GR'),
                                ('N90_count_scenario','N90_conditional','continuous_identical_source_count'),
                                ('delta','delta_tau_440','fractional_dtau440'),
                                ('sigma','sigma_delta_tau_local_GR','fractional_dtau440'),
                                ('correction_over_sigma','expected_local_z','absolute_delta_over_sigma_local_GR')):
            bind(row,name,'E4_RESULT',path+'/'+field,unit,row['scope'])
        row['notes']=['N90 information and 440-to-GW250114 equivalent conversion not supplied; remain null']
        add(('TAU440_FIXED_SOURCE_FISHER',item['reading'],group),row)
    for i,item in enumerate(e0['conditional_rates_scenarios']['forecasts']):
        row=new_scenario('E0_O5_'+str(i),'INPUT_O5_SCENARIO_NOT_DETECTION_PROMISE')
        path='/conditional_rates_scenarios/forecasts/'+str(i)
        row['context']={k:item[k] for k in ('gain_label','gain','exposure_status','reference_population','rate_population','scope')}
        if item['gain_label']=='BNS_ONLY_UPPER_CONTROL':row['scope']='BNS_ONLY_CONTROL_NOT_BBH_FORECAST'
        for name,field,unit in (('z_expected_conditional','z_optimistic_same_source_quality_plus_volume','dimensionless_optimistic'),
                                ('N90_count_scenario','N90_at_fixed_source_improved_sigma','events_illustrative'),
                                ('N90_information_target','operational_information_target','source_declared_information')):
            bind(row,name,'E0',path+'/'+field,unit,row['scope'])
        row['rate_only_z_interval']=dict(value=item['z_optimistic_CI90_rate_only'],status='INPUT_NOT_TOTAL_UNCERTAINTY',
                                        source=dict(**sources['E0'][0],pointer=path+'/z_optimistic_CI90_rate_only'))
        row['quality_invariant_control']=dict(value=item['z_detection_threshold_quality_invariant_control'],
            source=dict(**sources['E0'][0],pointer=path+'/z_detection_threshold_quality_invariant_control'))
        add(('TAU220_POPULATION',item['reading'],'O5_BANDA'),row)
    for reading in contract['readings']:
        for i,item in enumerate(e2['route_IV']['targets']):
            row=new_scenario('E2_IV_target_'+str(i),'INPUT_COMMON_BROWNIAN_SCENARIO_NOT_READING_SPECIFIC_PREDICTION')
            row['context']=item.copy();row['notes']=['Reading-to-recovered-jitter transfer OPEN; repeated common reference, not ten independent measurements']
            bind(row,'N90_count_scenario','E2','/route_IV/targets/'+str(i)+'/N90_validated','scenario_events_lower_bound',row['scope'])
            add(('DF220_POPULATION_WIDTH_IV',reading,'O4_HOJE'),row)
        for i,item in enumerate(e4['E5_information']):
            row=new_scenario('E5_IV_information_'+str(i),'INPUT_LOCAL_VARIANCE_INFORMATION_SIGMA_SYS_ZERO_SCENARIO')
            row['population']=item['population']
            bind(row,'GW250114_equivalents','E4_RESULT','/E5_information/'+str(i)+'/N_GW250114_equivalent',
                 'current_df_variance_information_equivalents',row['scope'])
            add(('DF220_POPULATION_WIDTH_IV',reading,'O4_HOJE'),row)
    for i,item in enumerate(e0['threeG_fixed_anchor_calculations']):
        for group in ('ET','CE'):
            row=new_scenario('E0_generic_3G_anchor_'+str(i),'INPUT_GENERIC_RD_SNR_ANCHOR_NOT_DETECTOR_SPECIFIC')
            root='/threeG_fixed_anchor_calculations/'+str(i)
            row['context']={k:item[k] for k in ('SNR_RD_target_INPUT','anchor_SNR_INPUT','anchor_scope','scope')}
            row['notes']=['Same generic scenario displayed under ET and CE, not independent forecasts',
                          'No selected population, mode transport or detection rate; operational information stays OPEN']
            bind(row,'sigma','E0',root+'/sigma_projected','fractional_dtau220_illustrative',row['scope'])
            bind(row,'N90_count_scenario','E0',root+'/N90','events_illustrative_only',row['scope'])
            add(('TAU220_POPULATION',item['reading'],group),row)
    # Rate intervals remain contextual and are never relabeled as N/z intervals.
    for i,item in enumerate(e0['conditional_rates_scenarios']['rates']):
        for category in ('rare_SNR_ge78','calibration_O4_subset'):
            path='/conditional_rates_scenarios/rates/'+str(i)+'/'+category
            context=dict(category=category,exposure=item['exposure'],scope=item['scope'],
                         rate=copy_metric(sources,'E0',path+'/rate_mle_per_year','per_year','INPUT_EXPOSURE_NOT_LIVE_TIME'),
                         rate_CI=copy_metric(sources,'E0',path+'/rate_CI90_per_year','per_year_CI90','STATIONARY_POISSON_PUBLISHED_UNIVERSE_ONLY'))
            for cell in cells.values():
                if cell['data_group']=='O4_HOJE':cell['rate_contexts'].append(context)
    # The historical 220 floor is never relabeled as a 440 or route-IV calibration.
    for i,item in enumerate(e0['systematic_conditions']):
        require(item['reading'] in contract['readings'], 'Unknown systematic reading')
        for group in GROUPS:
            cell=cells[('TAU220_POPULATION',item['reading'],group)]
            context=dict(color='red' if item['gate_green'] is False else 'OPEN',
                         status='INPUT_HISTORICAL_220_REFERENCE_NOT_CURRENT_CALIBRATION')
            for name,field in (('sigma_c_calibrated','sigma_c_calibrated'),
                               ('floor5_INPUT','floor5_INPUT'),('floor15_sensitivity','floor15_INPUT')):
                context[name]=copy_metric(sources,'E0','/systematic_conditions/'+str(i)+'/'+field,
                                         'fractional_dtau220',context['status'])
            cell['historical_gate_context']=context
    return cells


def append_reviewed(cells, sources, stages, readings, verdicts):
    calibration_rows={}
    for stage in STAGES:
        receipt,ref=stages[stage];alias='STAGE_'+stage
        for binding in receipt['bindings']:
            key=tuple(binding[k] for k in ('route','reading','data_group'))
            require(key in cells and binding['reading'] in readings,'Unknown reviewed cell')
            identity=stage+':'+binding['scenario_id']
            require(not any(r['id']==identity for r in cells[key]['scenarios']),'Duplicate reviewed scenario')
            row=new_scenario(identity,binding['scope'])
            row['stage_outcome']=receipt['outcome']
            row['references']=[ref,receipt['review'],receipt['artifact']]
            require(set(binding['metrics'])<=set(METRICS),'Unknown metric mapping')
            for name,mapping in binding['metrics'].items():
                if name in ('z_physical','lnB'):require(stage=='TEST','Physical results require reviewed TEST')
                row['metrics'][name]=copy_metric(sources,alias,mapping['pointer'],mapping['unit'],binding['scope'])
                check_metric(name,row['metrics'][name],key[0])
            if binding.get('gate_pointer') is not None:
                require(stage in ('E3.3','TEST'),'Gate requires calibration/test evidence')
                gate=pointer(sources[alias][1],binding['gate_pointer'])
                require(gate['color'] in ('green','red','OPEN'),'Gate color')
                require(all(type(gate[f]) is bool for f in PAID_FLAGS),'Explicit paid/unpaid flags')
                row['gate']=dict(color=gate['color'],status=gate['status'],
                                 source=dict(**sources[alias][0],pointer=binding['gate_pointer']),
                                 paid_flags={f:gate[f] for f in PAID_FLAGS})
                for name in GATE_FIELDS:
                    require(isinstance(gate['units'][name],str) and gate['units'][name], 'Gate units required')
                    row['gate'][name]=copy_metric(sources,alias,binding['gate_pointer']+'/'+name,gate['units'][name],binding['scope'])
                    check_metric(name,row['gate'][name],key[0])
                require(stage=='TEST' or gate['correction_over_sigma_physical'] is None,
                        'Calibration stage cannot publish observed physical significance')
                if gate['color']=='green':
                    require(gate['decision_reviewed'] is True,'Green decision requires explicit review')
                    if key[0]=='DF220_POPULATION_WIDTH_IV':
                        require(all(type(gate[n]) in (int,float) and gate[n]>=0 for n in ('sigma_sys_df','sigma_jit_recovered')),
                                'Green variance gate lacks measured systematics/transfer')
                    else:
                        require(type(gate['sigma_c_calibrated']) in (int,float) and type(gate['floor5_INPUT']) in (int,float)
                                and 0<=gate['sigma_c_calibrated']<gate['floor5_INPUT'],
                                'Green damping gate contradicts numerical floor')
                if stage=='E3.3':
                    calibration_rows[(key,binding['scenario_id'])]=row
            if stage=='TEST':
                summary=pointer(sources[alias][1],binding['test_summary_pointer'])
                require(summary['verdict'] in verdicts and type(summary['test_data_present']) is bool,'Reviewed test status')
                row['physical_test_present']=summary['test_data_present'];row['verdict']=summary['verdict']
                physical=(any(row['metrics'][n]['value'] is not None for n in ('z_physical','lnB'))
                          or row['gate']['correction_over_sigma_physical']['value'] is not None)
                evidence_verdict=row['verdict'] in EVIDENCE_VERDICTS
                if key[2] in FUTURE_GROUPS:
                    require(not row['physical_test_present'] and not physical and row['verdict']=='AWAITING_DATA',
                            'Future groups are conditional projections only in this contract')
                if physical or evidence_verdict:
                    require(receipt['outcome']=='COMPLETED' and stages['E3.2'][0]['outcome']=='COMPLETED'
                            and stages['E3.3'][0]['outcome']=='COMPLETED', 'Incomplete stages forbid physical readout')
                    require(binding['calibration_receipt_sha256']==stages['E3.3'][1]['sha256'],
                            'Test must link the reviewed E3.3 receipt')
                    calibrated=calibration_rows.get((key,binding['calibration_scenario_id']))
                    require(calibrated is not None and calibrated['gate']['color']=='green'
                            and all(calibrated['gate'].get('paid_flags',{}).get(f) is True for f in PAID_FLAGS),
                            'No compatible independently reviewed E3.3 green gate')
                    require(all(row['gate'][n]['value']==calibrated['gate'][n]['value'] for n in GATE_FIELDS if n!='correction_over_sigma_physical'),
                            'Test and E3.3 numerical gate differ')
                    require(all(row['gate'][n]['unit']==calibrated['gate'][n]['unit'] for n in GATE_FIELDS if n!='correction_over_sigma_physical'),
                            'Test and E3.3 units differ')
                    require(row['physical_test_present'] and row['gate']['color']=='green' and
                            all(row['gate'].get('paid_flags',{}).get(f) is True for f in PAID_FLAGS) and
                            summary['unblinding_authorized'] is True and summary['population_checks_passed'] is True,
                            'Physical readout before reviewed calibrated green gate')
                    require(summary['decision_rule_paid'] is True and summary['reading_multiplicity_paid'] is True,
                            'Decision rule and reading correction must be reviewed')
                    if row['verdict']=='EXCLUDED_IN_READING':
                        require(summary['relative_exclusion_rule_paid'] is True, 'Relative exclusion still open')
                    if row['verdict']=='NOT_FALSIFIED_UNDERPOWERED':
                        require(summary['power_assessment']=='INSUFFICIENT_REVIEWED', 'Underpowered requires reviewed insufficient power, not a high-power threshold')
                if not row['physical_test_present']:
                    require(not physical and row['verdict']=='AWAITING_DATA','No test data means AWAITING_DATA with no physical number')
                elif row['gate']['color']!='green':
                    require(not physical and row['verdict']=='INCONCLUSIVE_SYSTEMATICS',
                            'Present test data with red/OPEN gate means INCONCLUSIVE_SYSTEMATICS')
                else:
                    require(row['verdict']!='AWAITING_DATA','Present test data cannot be labeled absent')
            cells[key]['scenarios'].append(row)


def render(value):
    lines=['# Quadro de alcance — transcrição de fontes revisadas', '',
           'Cenários INPUT/DERIVED separados de resultados físicos. Null não é zero; nenhum cálculo científico novo.', '',
           '| Rota | Leitura / estatuto | Dado | Cenário / escopo | z esperado condicional | N90 informação | N90 contagem cenário | Equiv. GW250114 | Correção/sigma | Taxa / IC | Gate e números | Veredito |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|']
    def safe(x):return str(x).replace('|','\\|').replace('\n',' ')
    def metric(row,key):
        item=row['metrics'][key]
        return 'OPEN: '+safe(item['reason']) if item['value'] is None else safe(item['value'])+' ['+safe(item['unit'])+']'
    for cell in value['cells']:
        for row in cell['scenarios']:
            gate=row['gate'];numbers='; '.join(n+'='+str(gate[n]['value']) for n in GATE_FIELDS)
            values=[cell['route'],cell['reading']+' ['+cell['reading_statute']+']',cell['data_group'],row['id']+' / '+row['scope']]+[
                metric(row,k) for k in ('z_expected_conditional','N90_information_target','N90_count_scenario','GW250114_equivalents','correction_over_sigma')]+[
                metric(row,'rate_per_year')+' / '+metric(row,'rate_CI'),gate['color']+'; '+numbers,row['verdict']]
            lines.append('| '+' | '.join(safe(x) for x in values)+' |')
    lines+=['','## Contextos de taxa e pisos históricos','','Não são taxas selecionadas de cada rota nem calibrações físicas pagas.']
    for cell in value['cells']:
        if cell['rate_contexts'] or cell.get('historical_gate_context'):
            lines+=['',cell['route']+' / '+cell['reading']+' / '+cell['data_group']]
        for context in cell['rate_contexts']:
            lines.append('- '+safe(context['category'])+': taxa='+safe(context['rate']['value'])+
                         '; IC90='+safe(context['rate_CI']['value'])+' por ano; exposição='+safe(context['exposure'])+
                         '; '+safe(context['scope']))
        if cell.get('historical_gate_context'):
            gate=cell['historical_gate_context']
            lines.append('- Referência histórica 220: '+gate['color']+'; '+gate['status']+'; '+
                         '; '.join(n+'='+str(gate[n]['value']) for n in ('sigma_c_calibrated','floor5_INPUT','floor15_sensitivity')))
    lines+=['','Todos os ponteiros de origem estão no JSON pareado. None/null significa OPEN, nunca zero. Nenhum alvo vira promessa de anos ou 5sigma real.']
    return '\n'.join(lines)+'\n'


def write_new(path,raw):
    require(len(raw)<=LIMIT,'Output exceeds 25 MiB')
    fd,name=tempfile.mkstemp(prefix='.e6-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        require(Path(name).stat().st_size==len(raw),'Short staged write')
        os.link(name,path)
    finally:Path(name).unlink(missing_ok=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--execute',action='store_true')
    ap.add_argument('--authorization',type=Path);ap.add_argument('--authorization-sha256');args=ap.parse_args()
    auth,reg,contract,sources,stages,target=activate(args)
    cells=assemble_baselines(contract,sources)
    append_reviewed(cells,sources,stages,contract['readings'],reg['permitted_verdicts'])
    for cell in cells.values():
        if not cell['scenarios']:
            cell['scenarios']=[new_scenario('NO_REVIEWED_COMPATIBLE_RESULT','OPEN_AWAITING_DATA_OR_MODEL_BRIDGE')]
        for row in cell['scenarios']:
            require(set(row['metrics'])==set(METRICS),'Incomplete metrics')
            for name,value in row['metrics'].items():check_metric(name,value,cell['route'])
            for name in GATE_FIELDS:check_metric(name,row['gate'][name],cell['route'])
        for context in cell['rate_contexts']:
            check_metric('rate_per_year',context['rate'],cell['route']);check_metric('rate_CI',context['rate_CI'],cell['route'])
    result=dict(schema='E6_REACH_TABLE_V2',status='ASSEMBLED_REVIEWED_SOURCES_NOT_NEW_SCIENCE',
        registration_sha256=auth['registration']['sha256'],authorization_sha256=sha(args.authorization),
        generator_sha256=sha(Path(__file__)),readings=contract['readings'],routes=list(ROUTES),data_groups=list(GROUPS),
        cells=list(cells.values()),reviewed_stage_receipts=auth['reviewed_stages'],
        source_pins={k:v[0] for k,v in sources.items()},new_scientific_computations=False,
        E1_gate_context=dict(value=sources['E1'][1]['gate'],source=dict(**sources['E1'][0],pointer='/gate')),
        GR_limit_context='GR is the classical limit/control; never equate NOT_FALSIFIED with CONFIRMED',
        lnB_recomputed=False,E7_extraction_authorized=False,order_completed=False)
    raw=(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode()
    md=render(result).encode()
    require(len(raw)<=LIMIT and len(md)<=LIMIT,'Output exceeds 25 MiB')
    for ref,obj in sources.values():pinned(ref)
    for receipt,ref in stages.values():pinned(ref);pinned(receipt['review']);pinned(receipt['timeline']['evidence'])
    require(all(sha(HERE/name)==digest for name,digest in auth['package_sha256'].items()),'Sidecar changed during assembly')
    require(sha(args.authorization)==args.authorization_sha256,'Activation changed')
    target.mkdir(parents=True,exist_ok=False)
    write_new(target/'QUADRO_DE_ALCANCE_V1.json',raw)
    write_new(target/'QUADRO_DE_ALCANCE_V1.md',md)
    write_new(target/'RESULT_RECEIPT.json',(json.dumps(dict(status=result['status'],
        json_sha256=sha(target/'QUADRO_DE_ALCANCE_V1.json'),markdown_sha256=sha(target/'QUADRO_DE_ALCANCE_V1.md'),
        registration_sha256=result['registration_sha256'],generator_sha256=result['generator_sha256'],
        E7_extraction_authorized=False),indent=2)+'\n').encode())
    print(json.dumps(dict(path=str(target),status=result['status'])))


if __name__=='__main__':main()
