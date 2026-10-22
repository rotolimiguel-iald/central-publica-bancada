"""Derive full-family synthetic inputs from a frozen recipe; no fake background.

The real background supplier is called only later by controller/I02. Source
layout/design and covariance primitives are reused. This builder does not call
any former qualification run/main, nor repeat an old execution identity.
"""
import copy
from fractions import Fraction as F
import itertools
import math
from posix_protocol import canonical, document, need, sha


def structure(layout, design):
    # Same documented transformation as cases.structure_from_documents; copied
    # as explicit glue, with actual source reference retained in lineage.
    ids=[c['source_path']+':L'+str(c['source_line'])+'#'+c['observable'] for c in layout['components']]
    rows=[{} for _ in range(16)];ah=['0']*16;cc=['0']*16;scales=[1]*16
    for row in design['rows']:
        scale=5 if row['family'] in ('SN_HF','SBF_HF','megamaser') else 1
        ids.append(row['row_id']);scales.append(scale)
        rows.append({k:str(scale*F(v)) for k,v in row['X'].items()})
        ah.append(str(scale*F(row['a_h'])));cc.append(str(scale*F(row['c_C'])))
    return {'row_ids':ids,'row_units':['dimensionless']*16+['mag']*267,
        'native_to_output_row_scale':scales,'nuisance':{'columns':design['eta_columns'],
        'X_sparse_rows':rows,'dimension':63,'measure':'common kappa d_eta; no absolute evidence'},
        'response_columns':{'a_h':ah,'c_C':cc}}


def pair_correlation(left,right,partition,sign):
    if left==right:return F(1)
    for group in partition:
        if left in group and right in group:
            def polarity(key):
                fields=key.split('&');method=next(x for x in fields if x.startswith(('ceph_','trgb_','jagb_')))
                negative=(sign=='cepheid_opposite' and method.startswith('ceph_')) or (sign=='SH0ES_JAGB_opposite' and method.startswith('jagb_') and fields[-1]=='SH0ES')
                return -1 if negative else 1
            return F(polarity(left)*polarity(right))
    return F(0)


def independent_star(meta,scenario,checkpoint):
    # Independent pairwise transcription, not builder's matrix slicing/products.
    # Quarter fractions and dyadic variances are exactly representable as f64.
    u,v,p,q=map(F,scenario['fraction_strings']);need(u+v<1 and p+q<1,'INTERIOR_FAMILY')
    g=meta['groups'];sign=scenario['sign_scenario'];rows=meta['stellar_graph'];out=[]
    for left in rows:
        checkpoint('SYNTHETIC_PAIRWISE_REFERENCE',{})
        line=[]
        for right in rows:
            rm=(1-u-v)*int(left['MAS']==right['MAS'])+u*pair_correlation(left['MAS'],right['MAS'],g['MAS_same_program_at_N4258'],sign)+v*pair_correlation(left['MAS'],right['MAS'],[g['MAS_JAGB_reference_pair']],sign)
            rh=(1-p-q)*int(left['HMS']==right['HMS'])+p*pair_correlation(left['HMS'],right['HMS'],g['HMS_by_eleven_hosts'],sign)+q*pair_correlation(left['HMS'],right['HMS'],[g['HMS_N5643_JAGB_pair']],sign)
            line.append(float(F(left['anchor']==right['anchor'],16)+rm/4+rh))
        out.append(line)
    return out


def build(*, package, source_map, source_pins, modules, auxiliary, recipe_raw,
          decision_raw, runtime_raw, loaded_raw, guard_raw, review_raw, roots, checkpoint):
    recipe=document(recipe_raw);decision=document(decision_raw);unit=decision['execution_unit_id']
    np=modules['numpy'];consumer=modules['consumer'];theta=modules['theta'];node=modules['node'];precision=modules['precision']
    def source(role):return (package/source_map[role]).read_bytes()
    meta_raw=source('family_metadata');meta=document(meta_raw)
    need(sha(meta_raw)==recipe['family_metadata_sha256'] and len(meta['family_labels'])==600,'FULL_FAMILY_METADATA')
    layout=document(source('layout'));design=document(source('design'));st=structure(layout,design)
    consumer._structure(st) # Pinned structural identity, no likelihood or solver.
    st_raw=canonical(st);resources=recipe['resources'];sr=recipe['synthetic']
    need(sr['data_kind']=='SYNTHETIC' and recipe['family']=='EXACT_600_ORDERED_LABELS_NO_DEDUP','SYNTHETIC_FULL_FAMILY')
    need(sr['sigma_anchor']==.25 and sr['sigma_MAS']==.5 and sr['sigma_HMS']==1.,'FROZEN_DYADIC_REFERENCE')
    artifacts={'source:'+role:source(role) for role in source_pins}
    def add(name,raw):
        need(type(raw) is bytes and name not in artifacts,'ARTIFACT_DUPLICATE_OR_NOT_BYTES')
        artifacts[name]=raw;return name
    resource_key=add('derived:resources',canonical(resources))
    runtime_key=add('actual:runtime',runtime_raw);loaded_key=add('actual:loaded',loaded_raw)
    guard_key=add('actual:guard',guard_raw);recipe_key=add('input:recipe',recipe_raw)
    fixture={'id':unit+':full600-synthetic-recipe','recipe_sha256':sha(recipe_raw),'data_kind':'SYNTHETIC',
        'fixed_recipe':sr,'source_structure_sha256':sha(st_raw),'all_labels_retained':True,
        'support_rank_reference':'I03 exact incidence106 plus105 independent nonstellar dimensions; interior labels preserve span',
        'I03_reference_sha256':sha(source('I03_independent_receipt')),
        'actual_Linux_or_solver_execution_proven_here':False}
    fixture_raw=canonical(fixture);add('reference:fixture',fixture_raw)
    add('actual:independent-review',review_raw)
    ref=lambda suffix:{'id':unit+':'+suffix,'sha256':sha(fixture_raw)}
    bref={'artifact_sha256':sha(fixture_raw),'clause':fixture['id'],'status':'SYNTHETIC_FIXTURE'}
    # Pure recipe y: never obtained by a solver, catalogue, observed centre or fit.
    yy=list(sr['y_background'])+[float(F(v))*math.log10(70.) for v in st['response_columns']['a_h'][16:]]
    scales=np.array(st['native_to_output_row_scale'],dtype='<f8')
    y=np.array(yy,dtype='<f8')/scales;origin=np.zeros(283,dtype='<f8')
    y_key=add('synthetic:y',y.tobytes());origin_key=add('synthetic:origin',origin.tobytes())
    ids_key=add('structural:ids',canonical(st['row_ids']));structure_key=add('structural:structure',st_raw)
    config=document(source('configuration_template'));points=[];n=1<<recipe['last_level']
    for indices in itertools.product(range(n+1),repeat=3):
        key=theta._node_key(indices,n)
        points.append({'id':'grid_'+'_'.join(str(x) for x in key[:3])+'_over_'+str(key[3]),'theta':list(theta._theta(key))})
    need(len(points)==resources['max_solver_calls'] and resources['max_callback_calls']==600*len(points),'EXACT_COLD_GRID_BUDGET')
    config.update(request_id=unit+':background',status='SYNTHETIC_INTEGRATED_ENGINEERING_INPUT',
        points=points,point_selection='Full frozen nested dyadic prior box; no data selection',next_authority='Original outer ROOT decision only')
    config['resources'].update(points=len(points),max_solver_calls=len(points),threads=1,profiles=1,workers_parallel=1,
        automatic_retries=0,timeout_seconds_per_worker=resources['nominal_native_call_seconds'],total_timeout_seconds=resources['nominal_wall_seconds'])
    config_raw=canonical(config);config_key=add('derived:configuration',config_raw)
    assembly_raw=canonical({'schema':'F9_ASSEMBLY_ADMISSION_V1','status':'ENGINEERING_STRUCTURAL_ADMISSION',
        'layout_sha256':sha(source('layout')),'sources':modules['assembler'].SOURCE_PINS,
        'engine_configuration_sha256':sha(config_raw),'runtime_sha256':sha(runtime_raw)})
    assembly_key=add('derived:assembly',assembly_raw)
    loaded_ref={'id':unit+':loaded-objects','sha256':sha(loaded_raw)}
    runtime_ref={'id':unit+':runtime','sha256':sha(runtime_raw)}
    backend_raw=canonical({'schema':'F9_QUALIFIED_BACKEND_CALLER_RECEIPT_V1',
        'source_pins':{k:consumer.SOURCE_PINS[k] for k in ('linear_gaussian','support')},
        'runtime_reference':runtime_ref,'class_module':modules['linear'].FlatNuisanceGaussian.__module__,
        'class_name':'FlatNuisanceGaussian','caller_verification_reference':loaded_ref})
    backend_key=add('actual:backend-binding',backend_raw)
    primitive=auxiliary['primitive'];builder_mod=auxiliary['builder']
    primitive_receipt=canonical({'schema':'F9_COVARIANCE_PRIMITIVE_BINDING_V1',
        'primitive_source_sha256':sha(source('primitive_source')),'primitive_name':'block_correlation',
        'primitive_module':primitive.__module__,'runtime_reference':{'artifact_sha256':sha(runtime_raw),'clause':unit+':runtime','status':'REVIEWED_IMPLEMENTATION'},
        'loaded_callable_and_numpy_global_reference':{'artifact_sha256':sha(loaded_raw),'clause':unit+':primitive-binding','status':'REVIEWED_IMPLEMENTATION'}})
    builder=builder_mod.JointCovarianceBuilder(meta_raw,numpy_module=np,block_correlation=primitive,
        runtime_receipt_json=primitive_receipt,runtime_receipt_sha256=sha(primitive_receipt))
    need(builder.family_metadata()==meta['family_labels'],'ORDERED_FAMILY_CHANGED')
    blocks={b['name']:b for b in meta['blocks']}
    def matrec(values,left,right):
        a=np.array(values,dtype='<f8',order='C')
        return {'values':a,'row_ids':blocks[left]['row_ids'],'column_ids':blocks[right]['row_ids'],
            'coordinates':'NATIVE_F9_283','values_f64le_sha256':sha(a.tobytes()),'reference':bref,
            'zero_policy':'EXPLICIT_INPUT_ZERO' if bool((a==0).all()) else 'EXPLICIT_MATRIX'}
    common={}
    for name in builder_mod.COMMON:
        size=len(blocks[name]['row_ids']);a=np.eye(size,dtype='<f8')
        if name=='PLANCK':a[0,0]=sr['PLANCK_first_variance']
        if name=='SN_HF':a[0,0]=sr['SN_HF_variance']
        common[name]=matrec(a,name,name)
    cross={}
    for i,left in enumerate(builder_mod.BLOCKS):
        for right in builder_mod.BLOCKS[i+1:]:
            a=np.zeros((len(blocks[left]['row_ids']),len(blocks[right]['row_ids'])),dtype='<f8')
            if (left,right)==('PLANCK','SN_HF'):a[0,0]=sr['PLANCK_SN_HF_cross']
            cross[left+'|'+right]=matrec(a,left,right)
    sigmas={kind:{k:value for k in meta['primitive_keys'][kind]} for kind,value in
        (('anchor',sr['sigma_anchor']),('MAS',sr['sigma_MAS']),('HMS',sr['sigma_HMS']))}
    stellar={'sigma_by_primitive':sigmas,'sigma_f64le_sha256':{k:sha(np.array(list(v.values()),dtype='<f8').tobytes()) for k,v in sigmas.items()},
        'reference':bref,'D0_policy':'EXPLICIT_ZERO_BASELINE_RECIPE','D0_reference':bref}
    mm={'recipe':builder_mod.MM_RECIPE,'dependence_policy':'EXPLICIT_DIAGONAL_WORKING_INPUT',
        'dependence_reference':bref,'reference_endogeneity_reference':bref,
        'rows':[{'row_id':key,'variance_dex2':(i+1)/64,'distance_reference_mpc':sr['MM_distance_reference'],
            'velocity_reference_km_s':sr['MM_velocity_reference'],'U_reference_km_s':sr['MM_U_reference'],
            'fixed_reference':bref,'variance_recipe_reference':bref} for i,key in enumerate(blocks['MM']['row_ids'])]}
    measure=unit+':same-kappa-deta';specs=[];cov_records=[]
    cbinding={'family_common_input_sha256':sha(fixture_raw),'five_model_response_sha256':sha(st_raw),
        'consumer_structure_sha256':sha(st_raw),'fixed_affine_support_reference':bref,'normalization_recipe_reference':bref,
        'common_measure_id':measure,'model_and_O01_O02_reference':bref,'compression_reference':bref}
    for index,scenario in enumerate(meta['family_labels']):
        checkpoint('BEFORE_SYNTHETIC_COVARIANCE',{'scenario_id':scenario['label']})
        sbf={'recipe_id':scenario['sbf_id'],'variance_dex2':sr['SBF_variances'][scenario['sbf_id']],
             'variance_reference':bref,'compression_reference':bref}
        built=builder.build_case(scenario['label'],common_blocks=common,cross_blocks=cross,stellar=stellar,sbf=sbf,mm=mm,bindings=cbinding)
        C=built['C_native'];cov_records.append(built['record'])
        expected=np.zeros((283,283),dtype='<f8')
        for i in list(range(16))+list(range(194,283)):expected[i,i]=1.
        expected[0,0]=2.;expected[276,276]=1/16;expected[277,277]=sr['SBF_variances'][scenario['sbf_id']]
        for i in range(5):expected[278+i,278+i]=(i+1)/64
        expected[0,276]=expected[276,0]=1/64
        expected[16:194,16:194]=np.array(independent_star(meta,scenario,checkpoint),dtype='<f8')
        need(bool(np.array_equal(C,expected)),'INTEGRATED_PAIRWISE_COVARIANCE_MISMATCH')
        ckey=add('synthetic:C:'+str(index),C.tobytes())
        refs={k:ref(k) for k in ('statistical_model','covariance_and_cross_blocks','fixed_affine_support',
            'compression_and_offsets','common_nuisance_measure','MM_conditional_model','structure_review','synthetic_fixture')}
        admission={'schema':'F9_CONSUMER_ADMISSION_V1','scope':'ENGINEERING_POINTWISE_ONLY','scenario_id':scenario['label'],
            'data_kind':'SYNTHETIC','input_sha256':{'y_native_f64le':sha(artifacts[y_key]),'C_native_f64le':sha(artifacts[ckey]),
            'affine_origin_native_f64le':sha(artifacts[origin_key]),'row_ids_canonical_json':sha(artifacts[ids_key])},
            'structure_sha256':sha(st_raw),'source_pins':consumer.SOURCE_PINS,'backend_receipt_sha256':sha(backend_raw),
            'prediction_admission_sha256':sha(assembly_raw),'coordinates':consumer.COORDINATES,'output_measure':consumer.OUTPUT_MEASURE,
            'common_measure_id':measure,'MM_status':'CONDITIONAL_UNRATIFIED','expected_support_rank':sr['support_rank'],
            'tolerances':recipe['tolerances'],'references':refs}
        ar=canonical(admission);akey=add('derived:consumer:'+str(index),ar)
        plan={'schema':'F9_THETA_INTEGRATION_PLAN_V1','preparation_request_id':theta.REQUEST_ID,
            'execution_unit_id':unit+':'+scenario['label'],'source_pins':theta.SOURCE_PINS,
            'consumer_admission_sha256':sha(ar),'assembly_admission_sha256':sha(assembly_raw),'engine_configuration_sha256':sha(config_raw),
            'callback_reference':{'id':node.REQUEST_ID+':durable-callback','sha256':source_pins['durable']['sha256']},
            'controller_reference':{'id':recipe['preparation_request_id']+':controller','sha256':sha((package/'controller.py').read_bytes())},
            'first_level':recipe['first_level'],'last_level':recipe['last_level'],'max_callback_calls':len(points),
            'absolute_log_refinement_target':recipe['absolute_log_refinement_target'],'common_measure_id':measure}
        pr=canonical(plan);pkey=add('derived:theta:'+str(index),pr)
        coupling={'schema':'F9_NODE_COUPLING_ADMISSION_V1','preparation_request_id':node.REQUEST_ID,
            'source_pins':node.SOURCE_PINS,'theta_plan_sha256':sha(pr),'anchors':recipe['anchors'],
            'precision':{**recipe['precision'],'services':{'log_exp_quad_interval':{'id':precision.LOG_SERVICE_ID,'sha256':source_pins['precision']['sha256']},
                'positive_quad_1d':{'id':precision.QUAD_SERVICE_ID,'sha256':source_pins['precision']['sha256']}},'caller_verification_reference':loaded_ref},
            'runtime_sha256':sha(runtime_raw),'background_scope_id':unit+':background',
            'supplier_reference':{'id':recipe['preparation_request_id']+':background-supplier','sha256':sha((package/'background_supplier.py').read_bytes())},
            'loaded_objects_reference':loaded_ref,'resource_limits_reference':{'id':unit+':resources','sha256':sha(artifacts[resource_key])},
            'profile_enabled':recipe['profile_enabled']}
        kkey=add('derived:coupling:'+str(index),canonical(coupling))
        specs.append({'scenario_id':scenario['label'],'consumer_admission':akey,'backend_receipt':backend_key,'structure':structure_key,
            'row_ids':ids_key,'y_native':y_key,'C_native':ckey,'affine_origin_native':origin_key,'theta_plan':pkey,'coupling_template':kkey})
    summary=builder.summarize_family(cov_records)
    add('actual:covariance-family',canonical(summary))
    family_key=add('derived:scenario-manifest',canonical({'ordered_scenario_ids':[s['label'] for s in meta['family_labels']],
        'family_metadata_sha256':sha(meta_raw),'recipe_sha256':sha(recipe_raw),'deduplicated':False}))
    request={'schema':'F9_CONTROLLER_REQUEST_V1','preparation_request_id':recipe['preparation_request_id'],'execution_unit_id':unit,
        'artifact_pins':{k:{'bytes':len(v),'sha256':sha(v)} for k,v in artifacts.items()},
        'global_artifacts':{'engine_configuration':config_key,'assembly_admission':assembly_key,'runtime_inventory':runtime_key,
            'resource_plan':resource_key,'loaded_objects_receipt':loaded_key,'guard_contract':guard_key,'scenario_manifest':family_key},
        'scenarios':specs,'store_root':roots['nodes'],'run_store_root':roots['runs'],
        'family_scope':'EXACT_DECLARED_SCENARIOS_NOT_UNIVERSAL','input_recipe_sha256':sha(recipe_raw)}
    return canonical(request),artifacts,summary
