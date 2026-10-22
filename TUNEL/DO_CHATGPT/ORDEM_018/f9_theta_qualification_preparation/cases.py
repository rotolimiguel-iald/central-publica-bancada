"""Prepared analytic/synthetic controls; no case runs on import.

The callback records are explicitly fabricated fixtures, never real background
receipts, df482 computations, covariance admissions or scientific evidence.
"""
import hashlib
import json
import math
import time

REQUEST_ID = '4e9a80ad-dac3-4c6c-8ec5-b7927a9c056d'
CASE_IDS = ('T01','T02','T03','T04','T05','T06',
            'N01','N02','N03','N04','N05','N06','N07','N08','N09')
MODELS = ('H1_TGL','H2_LCDM','H3_beta_free','H4_Cepheid','H5_rd_free')
BOUNDS = ((50.0,90.0),(0.015,0.030),(0.08,0.18))
SCALES = (1.0,2.0,3.0,0.5,5.0)


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def canonical(obj):
    return json.dumps(obj,sort_keys=True,ensure_ascii=True,
                      separators=(',', ':'),allow_nan=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def fixture_hash(role, case_id, node_id=None):
    # A real hash of synthetic bytes; not a fictional hash of an external file.
    return sha(canonical({'schema':'EXPLICIT_SYNTHETIC_FIXTURE_V1',
               'qualification':REQUEST_ID,'case':case_id,'role':role,'node':node_id}))


class Sentinel(RuntimeError):
    pass


def run_case(candidate, case, source_path, deadline, contract):
    cid = case['id']
    need(cid in CASE_IDS, 'UNKNOWN_CASE')
    need(candidate.ThetaIntegrator.run.__code__.co_filename == source_path,
         'ORIGINAL_PINNED_RUN_REQUIRED')
    calls, ids, seen, coordinates = 0, [], set(), set()
    descriptors_chain = sha(canonical({'case':cid,'kind':'synthetic_descriptors'}))
    sentinel = Sentinel('INTENTIONAL_THIRD_CALLBACK_FAILURE')
    context_sha = fixture_hash('joint_admission',cid)
    assembly_sha = fixture_hash('assembly_admission',cid)
    engine_sha = fixture_hash('engine_configuration',cid)
    callback_ref = {'id':REQUEST_ID+':'+cid+':SYNTHETIC_CALLBACK',
                    'sha256':contract['case_source_sha256']}
    plan = {'schema':'F9_THETA_INTEGRATION_PLAN_V1',
            'preparation_request_id':contract['source_request'],
            'execution_unit_id':REQUEST_ID+':SYNTHETIC:'+cid,
            'source_pins':contract['theta_source_pins'],
            'consumer_admission_sha256':context_sha,
            'assembly_admission_sha256':assembly_sha,
            'engine_configuration_sha256':engine_sha,
            'callback_reference':callback_ref,
            'controller_reference':{'id':REQUEST_ID+':SYNTHETIC_CONTROLLER',
                'sha256':contract['driver_source_sha256']},
            'first_level':1,'last_level':2,
            'max_callback_calls':124 if cid=='N01' else 125,
            'absolute_log_refinement_target':1e-9,
            'common_measure_id':'SYNTHETIC_ONLY:'+cid}
    plan_raw = canonical(plan)
    offset = 1000.0 if cid=='T03' else -1000.0 if cid=='T04' else 0.0

    def callback(desc):
        nonlocal calls, descriptors_chain
        need(time.monotonic()<deadline, 'COOPERATIVE_CALLBACK_DEADLINE')
        calls += 1
        need(calls <= case['expected_callbacks'], 'UNEXPECTED_EXTRA_CALLBACK')
        need(desc['node_id'] not in seen, 'DUPLICATE_NODE_CALLBACK')
        seen.add(desc['node_id']); ids.append(desc['node_id'])
        nums, den = desc['dyadic_numerators'], desc['dyadic_denominator']
        need(type(den) is int and den in (1,2,4), 'DYADIC_DENOMINATOR')
        need(all(type(n) is int and 0<=n<=den for n in nums), 'DYADIC_NUMERATORS')
        need(den==1 or any(n%2 for n in nums), 'UNREDUCED_NODE')
        coordinates.add(tuple(n*(4//den) for n in nums))
        need(desc['theta_names']==['H0','ombh2','omch2'] and desc['five_models']==list(MODELS),
             'AXES_OR_FAMILY_CHANGED')
        for k, (lo,hi) in enumerate(BOUNDS):
            expected=lo if nums[k]==0 else hi if nums[k]==den else lo+(hi-lo)*nums[k]/den
            need(abs(desc['theta'][k]-expected)<=2e-14*max(1,abs(expected)), 'THETA_COORDINATE')
        core={k:desc[k] for k in ('execution_unit_id','consumer_admission_sha256',
              'callback_reference','assembly_admission_sha256','engine_configuration_sha256',
              'dyadic_numerators','dyadic_denominator')}
        need(sha(canonical(core))==desc['node_id'], 'INDEPENDENT_DESCRIPTOR_DIGEST')
        descriptors_chain=sha(canonical({'previous':descriptors_chain,'descriptor':desc}))
        if cid=='N02' and calls==3:
            raise sentinel
        u,v,w=tuple((x-lo)/(hi-lo) for x,(lo,hi) in zip(desc['theta'],BOUNDS))
        if cid in ('T02','T03','T04'):
            log_shape=math.log1p(u**3)+math.log1p(v*v)+math.log1p(w)
        elif cid=='T06':
            # Triangle centered at 1/8, half-width1/32, height32; area1.
            log_shape=math.log1p(32.0*max(0.0,1.0-abs(u-0.125)/0.03125))
        else:
            log_shape=0.0
        models={}
        for i,(model,scale) in enumerate(zip(MODELS,SCALES)):
            zero=(cid=='T05' and i==4) or (cid=='N05' and i==2)
            status=('ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT' if zero else
                    'FINITE_LOG_FLAT_INTEGRAL' if i<2 else 'ENGINEERING_ESTIMATE')
            if cid=='N05' and i==2:
                status='ENGINEERING_ESTIMATE'  # Deliberately unexplained -inf.
            models[model]={'log_conditional_integral':float('-inf') if zero else
                          math.fsum((offset, log_shape if cid!='T06' or i==0 else 0.0, math.log(scale))),
                          'status':status,'method':'EXPLICIT_SYNTHETIC_FIXTURE_NOT_DF482_EXECUTION'}
        if cid=='T01':
            models['H3_beta_free']['precision']={'error_kind':'UNASSESSED','converged':False}
            models['H3_beta_free']['counters']={'underflowed_nodes':3}
        background_sha=fixture_hash('background_packet',cid,
                                   'INTENTIONAL_SHARED_HASH' if cid=='N07' else desc['node_id'])
        result={'schema':'F9_CONDITIONAL_PHYSICAL_PRIOR_RESULT_V1','status':'ENGINEERING_ONLY',
                'request_id':contract['prior_request'],'models':models,'theta':list(desc['theta']),
                'base_theta_prior':{'density_exact':'50/3','applied':False,'integrated':False},
                'measure':'common kappa d_eta; no absolute evidence',
                'output_measure':'EUCLIDEAN_ON_FIXED_TRANSFORMED_SUPPORT',
                'normalization':{'rank':283,'eta_dimension':63,'log_prefactor':0.0,
                                 'common_log_kappa_omitted':True},
                'MM_status':'CONDITIONAL_UNRATIFIED',
                'certification':{'status':'UNBOUNDED_THEORY_ERROR','uniform_error_bound':None,
                                 'certified':False,'numerical_certificate':None},
                'precision_scope':'SYNTHETIC_CALLBACK_ONLY_NOT_PHYSICAL_PRIOR_EXECUTION',
                'provenance':{'source_pins':contract['prior_source_pins'],
                              'assembly_sha256':fixture_hash('assembled',cid,desc['node_id']),
                              'background_sha256':background_sha,
                              'consumer_admission_sha256':context_sha,
                              'precision_sha256':fixture_hash('precision',cid,desc['node_id'])},
                'absolute_evidence':None,'theta_integrated_evidence':None,'lnB':None,
                'p':None,'sigma':None,'verdict':None}
        if cid=='N03' and calls==2:
            result['normalization']['log_prefactor']=1.0
        if cid=='N06' and calls==2:
            del result['models']['H5_rd_free']
        if cid=='N08':
            result['base_theta_prior']['applied']=True
        if cid=='N09' and calls==2:
            result['theta'][0]+=0.125
        result_sha=candidate.canonical_conditional_sha256(result)
        if cid=='N04' and calls==2:
            result_sha=fixture_hash('INTENTIONALLY_WRONG_CONDITIONAL_HASH',cid)
        receipt={'node_id':desc['node_id'],'execution_unit_id':plan['execution_unit_id'],
                 'callback_reference':callback_ref,
                 'conditional_result_reference':{'id':cid+':SYNTHETIC_CONDITIONAL', 'sha256':result_sha},
                 'background_execution_reference':{'id':cid+':SYNTHETIC_NOT_EXECUTED',
                      'sha256':fixture_hash('synthetic_receipt',cid,desc['node_id'])},
                 'background_attempts':1,'background_successes':1,
                 'background_origin':'VERIFIED_DURABLE_CACHE','background_calls_this_callback':0,
                 'assembly_admission_sha256':assembly_sha,'engine_configuration_sha256':engine_sha}
        return {'conditional_result':result,'receipt':receipt}

    integration=None; output=None; caught=None; run_attempts=0
    try:
        integration=candidate.ThetaIntegrator(plan_raw,plan_sha256=sha(plan_raw),evaluate_node=callback)
        run_attempts+=1
        output=integration.run()
    except BaseException as exc:
        caught=exc
    expected_code=case.get('expected_exception_code')
    if expected_code:
        need(isinstance(caught,candidate.ThetaError) and caught.code==expected_code,
             'EXPECTED_TYPED_REFUSAL:'+str(expected_code))
        need(output is None, 'PARTIAL_FAMILY_RETURNED')
    elif cid=='N02':
        need(caught is sentinel and output is None, 'SAME_CALLBACK_EXCEPTION_REQUIRED')
    else:
        need(caught is None and type(output) is dict, 'UNEXPECTED_RUN_FAILURE:'+repr(caught))
    need(calls==case['expected_callbacks'], 'CALLBACK_COUNT')
    need(len(seen)==calls, 'CALLBACK_UNIQUENESS')
    diagnostics=None if integration is None else integration.diagnostics()
    if integration is not None:
        need(diagnostics['callback_attempts']==calls and
             diagnostics['callback_completed']==case['expected_completed'], 'INTERNAL_OBSERVED_COUNT')
        need(diagnostics['state']==('COMPLETED' if output is not None else 'FAILED_TERMINAL'), 'TERMINAL_STATE')
    if calls==125:
        need(coordinates=={(i,j,k) for i in range(5) for j in range(5) for k in range(5)},
             'COMPLETE_FINEST_BOX_NOT_ONLY_ENDPOINTS')
    replay=None
    if cid in ('T01','N02'):
        before=calls
        try:
            run_attempts+=1
            integration.run()  # Intentional planned refusal, not a scientific retry.
        except candidate.ThetaError as exc:
            need(exc.code=='REPLAY_ERROR', 'REPLAY_REFUSAL_CODE')
            replay={'code':exc.code,'additional_callbacks':calls-before}
        else:
            raise AssertionError('SINGLE_USE_NOT_ENFORCED')
        need(calls==before,'CALLBACK_REPEATED_AFTER_TERMINAL_STATE')
    comparisons={}
    if output is not None:
        need(output['status']=='ENGINEERING_ONLY' and output['MM_status']=='CONDITIONAL_UNRATIFIED',
             'ENGINEERING_SCOPE')
        need(all(output[k] is None for k in ('absolute_evidence','p','sigma','verdict')),
             'NO_SCIENTIFIC_VERDICT')
        need(output['certification']['certified'] is False and
             output['refinement']['global_convergence'] is None and
             output['refinement']['unresolved_peak_mass_bound'] is None,
             'NO_UNIFORM_CERTIFICATE')
        need([x['nodes_in_rule'] for x in output['levels']]==[27,125], 'NESTED_LEVELS')
        need(output['callback_counts']['attempted']==output['callback_counts']['completed']==125,
             'UNIQUE_NESTED_CALLBACKS_NOT_152')
        need(output['callback_counts']['background_calls']==
             {'new_calls_declared':0,'durable_cache_hits_declared':125}, 'SYNTHETIC_RECEIPT_COUNTS')
        need(output['prior']['density_exact']=='50/3' and output['prior']['box_jacobian_exact']=='3/50'
             and output['prior']['unit_cube_density_exact']=='1', 'NORMALIZED_FULL_BOX_PRIOR')
        multiplier=2.5 if cid in ('T02','T03','T04') else 1.0
        for model,scale in zip(MODELS,SCALES):
            ref=offset+math.log(multiplier*scale)
            value=output['models'][model]['log_relative_evidence_without_common_log_kappa']
            difference=abs(value-ref)
            need(difference<=case['absolute_log_tolerance'], 'ANALYTIC_INTEGRAL:'+model)
            ratio_ref=math.log(scale/2.0)
            ratio_error=abs(output['lnB_against_H2_same_context'][model]-ratio_ref)
            need(ratio_error<=case['absolute_log_tolerance'], 'COMMON_OFFSET_CANCELLATION:'+model)
            comparisons[model]={'observed_log':value,'sampled_rule_reference_log':ref,
                                'absolute_log_difference':difference,'ratio_error':ratio_error}
        need(output['refinement']['all_declared_levels_completed'] is True and
             output['refinement']['early_stopping'] is False,'ALL_LEVELS')
        if cid=='T01':
            need(output['conditional_precision_summary']=={'service_unassessed':125,
                  'service_not_converged':125,'conditional_underflowed_nodes':375}, 'QUALITY_NOT_ERASED')
        if cid=='T06':
            need(output['refinement']['indicator_satisfied'] is True, 'EXPECTED_MISSED_PEAK_INDICATOR')
            for model,scale in zip(MODELS,SCALES):
                factor=2.0 if model=='H1_TGL' else 1.0
                comparisons[model]['true_continuum_log']=math.log(factor*scale)
                comparisons[model]['missed_mass_log_gap']=math.log(factor)
                comparisons[model]['true_log_ratio_against_H2']=math.log(factor*scale/2.0)
            # PASS means the lack of a bound remains visible, not that mass was recovered.
    need(time.monotonic()<deadline,'CASE_DEADLINE')
    return {'case_id':cid,'status':'PASS','scope':'SYNTHETIC_ENGINEERING_ONLY',
            'observed':{'calls':calls,'duplicate_nodes':calls-len(seen)},
            'constructor_attempts':1,'run_attempts':run_attempts,
            'expected_exception_code':expected_code,'same_sentinel':cid=='N02' and caught is sentinel,
            'diagnostics':diagnostics,'planned_reentry':replay,'comparisons':comparisons,
            'descriptor_chain_sha256':descriptors_chain,'plan':plan,'plan_sha256':sha(plan_raw),
            'solver_calls':0,'physical_prior_calls':0,'observed_data':False,
            'fixture_receipts_are_real_executions':False,'uniform_certificate':False}
