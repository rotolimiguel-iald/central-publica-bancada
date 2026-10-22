"""Prepared I03 controls. Pairwise rational covariance oracle, no observed data."""
import copy
from fractions import Fraction as F
import hashlib
import json
import math
import sys
import time

def need(ok,msg):
    if not ok: raise AssertionError(msg)

def raw(d):return json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def reference(doc):return {'artifact_sha256':sha(raw(doc)),'clause':doc['id'],'status':'SYNTHETIC_FIXTURE'}
def consumer_ref(doc):return {'id':doc['id'],'sha256':sha(raw(doc))}

def pair_correlation(left,right,partition,sign):
    if left==right:return F(1)
    for group in partition:
        if left in group and right in group:
            def s(key):
                fields=key.split('&')
                method=next(v for v in fields if v.startswith(('ceph_','trgb_','jagb_')))
                negative=(sign=='cepheid_opposite' and method.startswith('ceph_')) or (sign=='SH0ES_JAGB_opposite' and method.startswith('jagb_') and fields[-1]=='SH0ES')
                return -1 if negative else 1
            return F(s(left)*s(right))
    return F(0)

def star_pairs(meta,scenario,deadline):
    g=meta['groups'];u,v,p,q=map(F,scenario['fraction_strings']);sign=scenario['sign_scenario']
    rows=meta['stellar_graph'];out=[]
    for i,a in enumerate(rows):
        need(time.monotonic()<deadline,'PAIRWISE_REFERENCE_DEADLINE')
        line=[]
        for b in rows:
            rm=(1-u-v)*int(a['MAS']==b['MAS'])+u*pair_correlation(a['MAS'],b['MAS'],g['MAS_same_program_at_N4258'],sign)+v*pair_correlation(a['MAS'],b['MAS'],[g['MAS_JAGB_reference_pair']],sign)
            rh=(1-p-q)*int(a['HMS']==b['HMS'])+p*pair_correlation(a['HMS'],b['HMS'],g['HMS_by_eleven_hosts'],sign)+q*pair_correlation(a['HMS'],b['HMS'],[g['HMS_N5643_JAGB_pair']],sign)
            line.append(F(a['anchor']==b['anchor'],16)+rm/4+rh)
        out.append(line)
    return out

def exact_support(meta,structure,deadline,bits):
    # Exact column span of the unweighted latent incidence, sparse Fractions.
    basis={}
    def reduce(vector):
        v={i:F(x) for i,x in enumerate(vector) if x}
        for pivot,b in sorted(basis.items()):
            coeff=v.get(pivot,F(0))
            if not coeff:continue
            for i,x in b.items():
                value=v.get(i,F(0))-coeff*x
                need(value.numerator.bit_length()<=bits and value.denominator.bit_length()<=bits,'FRACTION_BIT_CAP')
                if value:v[i]=value
                else:v.pop(i,None)
        return v
    for kind in ('anchor','MAS','HMS'):
        for key in meta['primitive_keys'][kind]:
            need(time.monotonic()<deadline,'EXACT_SUPPORT_DEADLINE')
            v=reduce([int(row[kind]==key) for row in meta['stellar_graph']])
            if v:
                k=min(v);a=v[k];basis[k]={i:x/a for i,x in v.items()}
                need(all(x.numerator.bit_length()<=bits and x.denominator.bit_length()<=bits for x in basis[k].values()),'NORMALIZED_FRACTION_BIT_CAP')
    rank=len(basis)
    for key in [c['key'] for c in structure['nuisance']['columns']]:
        need(not reduce([F(row.get(key,'0')) for row in structure['nuisance']['X_sparse_rows'][16:194]]),'X_NOT_IN_STELLAR_SUPPORT')
    for key in ('a_h','c_C'):
        need(not reduce(list(map(F,structure['response_columns'][key][16:194]))),'RESPONSE_NOT_IN_STELLAR_SUPPORT')
    need(rank==106,'EXACT_INCIDENCE_RANK_DIFFERS_FROM_DOCUMENTED_106')
    return rank+105

def run(np,builder_module,primitive,consumer,backend,helpers,contract,meta,layout,design,runtime_ref,emit,deadline):
    rid=contract['request_id'];limit=contract['budgets'];acc=contract['acceptance']
    structure=helpers.structure_from_documents(layout,design)
    # These two helpers only construct metadata/synthetic means, never old run().
    packet,bg,prediction,directions=helpers.make_packet(structure,layout,consumer,rid)
    origin=np.zeros(283,dtype='<f8');origin[16]=.125;origin[276]=.375
    for model in consumer.MODELS:
        packet['models'][model]['mean_without_nuisance']=[v+float(o) for v,o in zip(packet['models'][model]['mean_without_nuisance'],origin)]
    packet['fixture_provenance']='SYNTHETIC_I03_REFERENCE_ORIGIN_SHIFT; ASSEMBLER_NOT_EXECUTED'
    packet_raw=helpers.raw(packet);p_sha=sha(packet_raw);structure_raw=helpers.raw(structure)
    rank=exact_support(meta,structure,deadline,limit['max_reference_fraction_bits'])
    selected=[]
    for spec in contract['selected_scenarios']:
        records=[r for r in meta['family_labels'] if r['label']==spec['label']]
        need(len(records)==1 and records[0]==spec,'EXACT_FAMILY_SELECTION');selected.append(records[0])
    star0=star_pairs(meta,selected[0],deadline);star1=star_pairs(meta,selected[1],deadline)
    need(star0!=star1,'SELECTED_CASES_MUST_DIFFER')
    base_ref=reference({'id':rid+'/explicit-synthetic-inputs','sigma_anchor':'1/4','sigma_MAS':'1/2','sigma_HMS':'1',
        'D0':'explicit zero','MM':'conditional fixed diagonal fixture, no observed values','no_independence_inferred':True})
    keys=meta['primitive_keys'];blocks={b['name']:b for b in meta['blocks']}
    slices={k:slice(b['start'],b['stop']) for k,b in blocks.items()}
    def matrix_record(values,left,right):
        a=np.array(values,dtype='<f8',order='C')
        return {'values':a,'row_ids':blocks[left]['row_ids'],'column_ids':blocks[right]['row_ids'],
            'coordinates':'NATIVE_F9_283','values_f64le_sha256':sha(a.tobytes()),'reference':base_ref,
            'zero_policy':'EXPLICIT_INPUT_ZERO' if bool((a==0).all()) else 'EXPLICIT_MATRIX'}
    common={}
    for name in builder_module.COMMON:
        size=blocks[name]['stop']-blocks[name]['start'];a=np.eye(size,dtype='<f8')
        if name=='PLANCK':a[0,0]=2.
        if name=='SN_HF':a[0,0]=1/16
        common[name]=matrix_record(a,name,name)
    cross={}
    for i,left in enumerate(builder_module.BLOCKS):
        for right in builder_module.BLOCKS[i+1:]:
            a=np.zeros((len(blocks[left]['row_ids']),len(blocks[right]['row_ids'])),dtype='<f8')
            if (left,right)==('PLANCK','STELLAR'):a[0,:]=[float(x/8) for x in star0[0]]
            if (left,right)==('PLANCK','SN_HF'):a[0,0]=1/64
            cross[left+'|'+right]=matrix_record(a,left,right)
    sigma={kind:{k:v for k in keys[kind]} for kind,v in (('anchor',.25),('MAS',.5),('HMS',1.))}
    stellar={'sigma_by_primitive':sigma,
        'sigma_f64le_sha256':{kind:sha(np.array([sigma[kind][k] for k in keys[kind]],dtype='<f8').tobytes()) for kind in sigma},
        'reference':base_ref,'D0_policy':'EXPLICIT_ZERO_BASELINE_RECIPE','D0_reference':base_ref}
    sbf={'recipe_id':'SBF_UPSTREAM_M_ONLY','variance_dex2':1/8,'variance_reference':base_ref,'compression_reference':base_ref}
    mm={'recipe':builder_module.MM_RECIPE,'dependence_policy':'EXPLICIT_DIAGONAL_WORKING_INPUT',
        'dependence_reference':base_ref,'reference_endogeneity_reference':base_ref,
        'rows':[{'row_id':key,'variance_dex2':(i+1)/64,'distance_reference_mpc':10.,
                 'velocity_reference_km_s':700.,'U_reference_km_s':700.,'fixed_reference':base_ref,
                 'variance_recipe_reference':base_ref} for i,key in enumerate(blocks['MM']['row_ids'])]}
    bindings={'family_common_input_sha256':base_ref['artifact_sha256'],'five_model_response_sha256':p_sha,
       'consumer_structure_sha256':sha(structure_raw),'common_measure_id':rid+'/common-kappa-deta',
       'fixed_affine_support_reference':base_ref,'normalization_recipe_reference':base_ref,
       'model_and_O01_O02_reference':base_ref,'compression_reference':base_ref}
    receipt={'schema':'F9_COVARIANCE_PRIMITIVE_BINDING_V1',
       'primitive_source_sha256':contract['sources']['primitive']['sha256'],
       'primitive_name':'block_correlation','primitive_module':primitive.__module__,
       'runtime_reference':runtime_ref,'loaded_callable_and_numpy_global_reference':base_ref}
    rr=raw(receipt)
    with open(contract['sources']['metadata']['path'],'rb') as f:metadata_raw=f.read()
    counts={k:0 for k in ('builder_constructors','build_attempts','primitive_calls','consumer_prepare_attempts','backend_constructors','evaluate_attempts')}
    profile_codes={builder_module.JointCovarianceBuilder.__init__.__code__:'builder_constructors',
       builder_module.JointCovarianceBuilder.build_case.__code__:'build_attempts',primitive.__code__:'primitive_calls',
       consumer.prepare_joint.__code__:'consumer_prepare_attempts',backend.__init__.__code__:'backend_constructors',
       consumer.PreparedJoint.evaluate_five.__code__:'evaluate_attempts'}
    def profile(frame,event,arg):
        if event=='call':
            need(time.monotonic()<deadline,'COOPERATIVE_DEADLINE')
            key=profile_codes.get(frame.f_code)
            if key:counts[key]+=1;need(counts[key]<=limit[key],key+'_CAP')
    def build(label,cross_input=cross):
        return builder.build_case(label,common_blocks=common,cross_blocks=cross_input,
                      stellar=stellar,sbf=sbf,mm=mm,bindings=bindings)
    def expected(star):
        # Independent placement loops, not a copy of the builder block slicer.
        C=[[F(0) for j in range(283)] for i in range(283)]
        for i in list(range(16))+list(range(194,283)):C[i][i]=F(1)
        C[0][0]=F(2);C[276][276]=F(1,16);C[277][277]=F(1,8)
        for i in range(5):C[278+i][278+i]=F(i+1,64)
        for i in range(178):
            for j in range(178):C[16+i][16+j]=star[i][j]
            C[0][16+i]=C[16+i][0]=star0[0][i]/8
        C[0][276]=C[276][0]=F(1,64)
        return np.array([[float(x) for x in row] for row in C],dtype='<f8')
    def consume(built,bad_pin=False):
        record=built['record'];C=built['C_native'];scales=np.array(structure['native_to_output_row_scale'],dtype='<f8')
        need(record['bindings']==bindings and tuple(structure['row_ids'])==built['row_ids'],'COVARIANCE_BINDINGS')
        need(record['C_native_f64le_sha256']==sha(C.tobytes()) and record['coordinates']=='NATIVE_F9_283','NATIVE_C_PIN')
        ckeys=[c['key'] for c in structure['nuisance']['columns']]
        X=np.array([[float(F(row.get(k,'0'))) for k in ckeys] for row in structure['nuisance']['X_sparse_rows']],dtype='<f8')
        eta=np.array([(i%3-1)/16 for i in range(63)],dtype='<f8')
        y=np.array(packet['models']['H2_LCDM']['mean_without_nuisance'],dtype='<f8')+X@eta;y[1]+=.25
        yn=np.array(y/scales,dtype='<f8');on=np.array(origin/scales,dtype='<f8')
        back={'schema':'F9_QUALIFIED_BACKEND_CALLER_RECEIPT_V1',
           'source_pins':{k:consumer.SOURCE_PINS[k] for k in ('linear_gaussian','support')},
           'runtime_reference':{'id':runtime_ref['clause'],'sha256':runtime_ref['artifact_sha256']},
           'class_name':backend.__name__,'class_module':backend.__module__,
           'caller_verification_reference':consumer_ref({'id':rid+'/loaded-backend','pins':contract['sources']})}
        br=helpers.raw(back)
        refs={k:consumer_ref({'id':rid+'/'+k,'builder_record_sha256':record['record_sha256'],'fixture':True})
              for k in ('statistical_model','covariance_and_cross_blocks','fixed_affine_support','compression_and_offsets',
              'common_nuisance_measure','MM_conditional_model','structure_review','synthetic_fixture')}
        admission={'schema':'F9_CONSUMER_ADMISSION_V1','scope':'ENGINEERING_POINTWISE_ONLY',
           'scenario_id':record['label'],'data_kind':'SYNTHETIC',
           'input_sha256':{'y_native_f64le':sha(yn.tobytes()),'C_native_f64le':record['C_native_f64le_sha256'],
             'affine_origin_native_f64le':sha(on.tobytes()),'row_ids_canonical_json':sha(helpers.raw(structure['row_ids']))},
           'structure_sha256':bindings['consumer_structure_sha256'],'source_pins':consumer.SOURCE_PINS,
           'backend_receipt_sha256':sha(br),'prediction_admission_sha256':prediction['sha256'],
           'coordinates':consumer.COORDINATES,'output_measure':consumer.OUTPUT_MEASURE,'MM_status':'CONDITIONAL_UNRATIFIED',
           'common_measure_id':bindings['common_measure_id'],'expected_support_rank':rank,
           'tolerances':{'relative_cutoff':1e-12,'absolute_cutoff':0.,'support_tolerance':1e-8,'design_relative_cutoff':1e-12},
           'references':refs}
        if bad_pin:admission['input_sha256']['C_native_f64le']=sha(C.tobytes()+b'deliberate-negative-control')
        ar=helpers.raw(admission)
        joint=consumer.prepare_joint(yn,C,built['row_ids'],affine_origin_native=on,structure_json=structure_raw,
           admission_json=ar,admission_sha256=sha(ar),backend_receipt_json=br,numpy_module=np,flat_gaussian_class=backend)
        need(joint._admission_sha256==sha(ar),'ACTUAL_CONSUMER_ADMISSION')
        need(joint._admission['input_sha256']['C_native_f64le']==record['C_native_f64le_sha256'],'ADMISSION_C_IDENTITY')
        target=(scales[:,None]*C)*scales[None,:]
        need(joint._transformed_covariance_sha256==sha(target.tobytes()),'TCT_ONCE')
        need(np.allclose(joint._y,y,atol=1e-12,rtol=1e-12) and np.array_equal(joint._origin,origin),'Y_ORIGIN_ONCE')
        need(joint._engine.support.rank==rank and joint._engine.p==63,'EXACT_REFERENCE_RANK')
        return joint,admission
    records=[];old=sys.getprofile();sys.setprofile(profile)
    try:
        builder=builder_module.JointCovarianceBuilder(metadata_raw,numpy_module=np,block_correlation=primitive,
             runtime_receipt_json=rr,runtime_receipt_sha256=sha(rr))
        goods=[]
        for case,scenario,star in (('V01',selected[0],star0),('V02',selected[1],star1)):
            emit(case+'_STARTED',{'case':case,'label':scenario['label']})
            built=build(scenario['label']);want=expected(star)
            need(np.array_equal(built['C_native'],want),'PAIRWISE_ENTRY_REFERENCE')
            need(not built['C_native'].flags.writeable,'IMMUTABLE_C')
            record=copy.deepcopy(built['record']);saved=record.pop('record_sha256')
            need(sha(raw(record))==saved,'BUILDER_RECORD_SHA')
            need(record['actual_rank'] is None and record['support_receipt'] is None and record['normalization_receipt'] is None,'BUILDER_MUST_NOT_CERTIFY_SUPPORT')
            joint,admission=consume(built)
            point=joint.evaluate_five(packet_raw,assembly_sha256=p_sha)
            need(all(point['models'][m]['status']=='FINITE_LOG_FLAT_INTEGRAL' for m in consumer.MODELS),'ALL_FIVE_FINITE')
            expected_delta=-1/32
            measured_delta=point['models']['H2_LCDM']['log_integral_deta']-point['normalization']['log_prefactor']
            need(abs(measured_delta-expected_delta)<=acc['quadratic_absolute_tolerance'],'H2_INDEPENDENT_QUADRATIC')
            need(point['lnB'] is None and point['sigma'] is None,'NO_PHYSICAL_PROMOTION')
            rec={'case':case,'status':'PASS','label':scenario['label'],'matrix_equal_to_pairwise_rational_reference':True,
              'rank_from_exact_incidence':rank,'C_native_sha256':built['record']['C_native_f64le_sha256'],
              'consumer_admission_sha256':joint._admission_sha256,'H2_log_minus_prefactor':measured_delta,
              'H2_reference_minus_one_over_32':expected_delta,'normalization_scope':'existing qualified backend; no new independent absolute normalization oracle',
              'all_five_finite':True,'conditional_MM':True}
            emit(case+'_RESULT',rec);records.append(rec);goods.append(built)
        def refusal(case,call,cls,code,cause=None):
            emit(case+'_STARTED',{'case':case,'expected_code':code})
            try:call()
            except cls as exc:
                need(exc.code==code,'WRONG_ERROR_'+case)
                if cause is not None:need(isinstance(exc.__cause__,ValueError) and cause in str(exc.__cause__),'EXPECTED_CAUSE_'+case)
            else:raise AssertionError('MISSING_REFUSAL_'+case)
            rec={'case':case,'status':'PASS','error_code':code,'cause_contains':cause}
            emit(case+'_RESULT',rec);records.append(rec)
        missing=dict(cross);missing.pop('PLANCK|DESI')
        refusal('V03',lambda:build(selected[0]['label'],missing),builder_module.CovarianceError,'SCHEMA_ERROR')
        badmm=dict(cross);matrix=np.zeros((3,5),dtype='<f8');matrix[0,0]=1/128
        badmm['PLANCK|MM']=matrix_record(matrix,'PLANCK','MM')
        refusal('V04',lambda:build(selected[0]['label'],badmm),builder_module.CovarianceError,'OPEN_MODEL_COMPONENT')
        before=counts['backend_constructors']
        refusal('V05',lambda:consume(goods[0],bad_pin=True),consumer.ConsumerError,'PIN_ERROR')
        need(counts['backend_constructors']==before,'HASH_REJECTION_AFTER_BACKEND')
        indefinite=dict(cross);matrix=np.zeros((3,13),dtype='<f8');matrix[1,0]=2
        indefinite['PLANCK|DESI']=matrix_record(matrix,'PLANCK','DESI')
        def bad_joint():return consume(build(selected[0]['label'],indefinite))
        refusal('V06',bad_joint,consumer.ConsumerError,'BACKEND_PREPARATION_FAILED','Indefinite covariance')
    finally:sys.setprofile(old)
    need([x['case'] for x in records]==contract['case_order'],'COMPLETE_CASES')
    for key,value in counts.items():need(value==limit[key],key+'_COUNT')
    return {'status':'PASS','request_id':rid,'cases':records,'counts':counts,'observed_data':False,
            'solver_calls':0,'physical_sigma':None,'all_600_scenarios_qualified':False,
            'absolute_normalization_requalified':False,'provisional_until_supervisor_exit_zero':True}
