"""Five prepared full-matrix synthetic controls; NEVER run during preparation.

The oracle uses exact pivot coordinates of X, not the candidate eig/SVD solver.
Background packets are explicitly synthetic fixtures, not outputs of CAMB.
"""
import copy
from fractions import Fraction as F
import hashlib
import json
import math
import sys
import time

MODELS=('H1_TGL','H2_LCDM','H3_beta_free','H4_Cepheid','H5_rd_free')

def need(ok, label):
    if not ok: raise AssertionError(label)

def raw(doc):
    return json.dumps(doc,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode()

def sha(b): return hashlib.sha256(b).hexdigest()

def ref(doc): return {'id':doc['id'],'sha256':sha(raw(doc))}

def structure_from_documents(layout,design):
    ids=[c['source_path']+':L'+str(c['source_line'])+'#'+c['observable'] for c in layout['components']]
    rows=[{} for _ in range(16)]; ah=['0']*16; cc=['0']*16; scales=[1]*16
    for row in design['rows']:
        t=5 if row['family'] in ('SN_HF','SBF_HF','megamaser') else 1
        ids.append(row['row_id']); scales.append(t)
        rows.append({k:str(t*F(v)) for k,v in row['X'].items()})
        ah.append(str(t*F(row['a_h']))); cc.append(str(t*F(row['c_C'])))
    return {'row_ids':ids,'row_units':['dimensionless']*16+['mag']*267,
            'native_to_output_row_scale':scales,
            'nuisance':{'columns':design['eta_columns'],'X_sparse_rows':rows,
                        'dimension':63,'measure':'common kappa d_eta; no absolute evidence'},
            'response_columns':{'a_h':ah,'c_C':cc}}

def exact_pivots_and_inverse(X, deadline, bits):
    # Rational row elimination selects original rows; no covariance computation.
    echelon={}; pivots=[]
    def bounded(v):
        need(v.numerator.bit_length()<=bits and v.denominator.bit_length()<=bits,'EXACT_REFERENCE_SIZE_CAP')
        return v
    for row_id,row in enumerate(X):
        need(time.monotonic()<deadline,'REFERENCE_DEADLINE')
        v=row[:]
        for col,basis in sorted(echelon.items()):
            coeff=v[col]
            if coeff: v=[bounded(a-coeff*b) for a,b in zip(v,basis)]
        col=next((i for i,x in enumerate(v) if x),None)
        if col is not None:
            pivot=v[col]; echelon[col]=[bounded(x/pivot) for x in v]; pivots.append(row_id)
        if len(pivots)==63: break
    need(len(pivots)==63,'FROZEN_X_NOT_EXACT_FULL_RANK')
    m=[X[r][:]+[F(i==j) for j in range(63)] for i,r in enumerate(pivots)]
    det=F(1)
    for j in range(63):
        need(time.monotonic()<deadline,'REFERENCE_DEADLINE')
        k=next((i for i in range(j,63) if m[i][j]),None)
        need(k is not None,'REFERENCE_PIVOT')
        if k!=j: m[j],m[k]=m[k],m[j]; det=-det
        pivot=m[j][j]; det=bounded(det*pivot)
        m[j]=[bounded(v/pivot) for v in m[j]]
        for i in range(63):
            if i==j or not m[i][j]: continue
            coeff=m[i][j]; m[i]=[bounded(a-coeff*b) for a,b in zip(m[i],m[j])]
    need(all(m[i][j]==(i==j) for i in range(63) for j in range(63)),'EXACT_INVERSE_IDENTITY')
    return pivots,[row[63:] for row in m],det

def dot(a,b): return math.fsum(x*y for x,y in zip(a,b))

class CoordinateOracle:
    def __init__(self,X,pivots,inverse,det,singular):
        self.X=[[float(x) for x in row] for row in X]
        self.pivots=pivots; self.inv=[[float(x) for x in row] for row in inverse]
        self.tail=[i for i in range(283) if i not in pivots and not(singular and i==2)]
        need(0 in self.tail and self.tail[0]==0 and self.tail[-1]>=16,'CROSS_DOMAIN_SHEAR')
        self.rank=282 if singular else 283
        self.logK=-.5*(self.rank-63)*math.log(2*math.pi)-math.log(abs(det.numerator))+math.log(det.denominator)

    def coords(self,v):
        eta=[dot(row,[v[i] for i in self.pivots]) for row in self.inv]
        tail=[v[i]-dot(self.X[i],eta) for i in self.tail]
        tail[0]-=.25*tail[-1]
        return tail

    def point(self,y,mu):
        r=self.coords([a-b for a,b in zip(y,mu)])
        return self.logK-.5*dot(r,r)

    def quadratic(self,y,mu,direction):
        r=self.coords([a-b for a,b in zip(y,mu)]); d=self.coords(direction)
        return self.logK-.5*dot(r,r),dot(d,d),dot(r,d)

def log_window(logbase,a,b,x0,lo,hi,t,logdensity):
    if a==0:
        need(b==0,'REFERENCE_FLAT_B'); return logbase
    m=x0+b/a
    z=math.sqrt(a/2)
    window=math.sqrt(math.pi/(2*a))*(math.erf(z*(hi-m-t/a))-math.erf(z*(lo-m-t/a)))
    need(window>0 and math.isfinite(window),'REFERENCE_ERF_RANGE_NOT_RESOLVED')
    return math.fsum((logbase,b*b/(2*a),t*m,t*t/(2*a),math.log(window),logdensity))

def rd_reference(logbase,a,b,x0,panels):
    # Fixed Simpson in r_d; candidate integrates adaptively in reciprocal q.
    if a==0:
        need(b==0,'REFERENCE_FLAT_B')
        return logbase,0.,0
    lo,hi=130.,160.; qlo,qhi=1/hi,1/lo
    m=x0+b/a; peak=min(qhi,max(qlo,m)); d=peak-x0
    anchor=logbase+b*d-.5*a*d*d
    def f(r):
        u=1/r-x0
        return math.exp(math.fsum((logbase,b*u,-.5*a*u*u,-anchor)))
    h=(hi-lo)/panels
    values=[f(lo+h*i) for i in range(panels+1)]
    average=h/(3*(hi-lo))*math.fsum(v*(1 if i in(0,panels) else 4 if i%2 else 2) for i,v in enumerate(values))
    z=max(abs(qlo-m),abs(qhi-m)); R=lo
    u1=a*z/R**2; u2=a/R**4+2*a*z/R**3
    u3=6*a/R**5+6*a*z/R**4; u4=36*a/R**6+24*a*z/R**5
    bound=h**4*(u4+4*u1*u3+3*u2*u2+6*u1*u1*u2+u1**4)/180
    need(0<=bound<average and math.isfinite(average),'REFERENCE_SIMPSON_BOUND_NOT_USABLE')
    return anchor+math.log(average),-math.log1p(-bound/average),panels+1

def make_packet(structure,layout,consumer,rid):
    theta=[70.,.022,.12]; pars=dict(zip(('H0','ombh2','omch2'),theta))
    E=math.exp(3); I=(2/3)*math.log(E)
    beta=float(layout['alpha']['decimal_token'])*math.sqrt(math.e)
    ah=[float(F(x)) for x in structure['response_columns']['a_h']]
    cc=[float(F(x)) for x in structure['response_columns']['c_C']]
    # Arbitrary synthetic mean, no use of observed centres or solver output.
    base=[1.5,300.,theta[1]]+[1+i/4 for i in range(13)]+[a*math.log10(theta[0]) for a in ah[16:]]
    bg={'schema':'F9_BACKGROUND_PACKET_V1','status':'ENGINEERING_RESULT','error':None,
        'identity':{'theta':theta,'synthetic_fixture':rid},
        'result':{'theta':theta,'I_law':I,'E_law':E},
        'fixture_provenance':'HAND_CONSTRUCTED_NOT_A_SOLVER_EXECUTION'}
    bgraw=raw(bg)
    prediction=ref({'id':rid+'/synthetic-prediction-input','producer':'fixture','solver_executed':False})
    packet=dict(structure)
    packet.update(schema='F9_FIVE_MODEL_PREDICTIONS_V1',status='ENGINEERING_ONLY',
        identity={'admission_sha256':prediction['sha256'],
          'layout_sha256':consumer.SOURCE_PINS['layout']['sha256'],
          'sources':consumer.ASSEMBLY_SOURCE_PINS,'background_packet_sha256':sha(bgraw),
          'background_identity':bg['identity']},
        certification={'status':'UNBOUNDED_THEORY_ERROR','uniform_error_bound':None,'certified':False,'numerical_certificate':None},
        observed_outputs={'chi2':None,'p':None,'sigma':None,'lnB':None},
        fixture_provenance='HAND_CONSTRUCTED; ASSEMBLER_NOT_EXECUTED',models={})
    for model in MODELS:
        p=dict(pars); mu=base[:]; extra='1'
        if model in ('H1_TGL','H3_beta_free'):
            bt=beta if model=='H1_TGL' else .01
            mu=[m+I*bt/math.log(10)*a for m,a in zip(base,ah)]
            if model=='H3_beta_free':p['beta']=.01; extra='10'
        elif model=='H4_Cepheid':
            p['s']=.02; extra='10/3'; delta=-5*math.log1p(.02)/math.log(10)
            mu=[m+delta*c for m,c in zip(base,cc)]
        elif model=='H5_rd_free':
            p['rd_Mpc']=142.; extra='1/30'; mu[3:16]=[m*145/142 for m in base[3:16]]
        packet['models'][model]={'parameters':p,'mean_without_nuisance':mu,
            'prior':{'coordinates':list(p),'common_theta_density_exact':'50/3',
                     'extra_density_exact':extra,'measure':'uniform_in_listed_coordinates'}}
    directions={'H3_beta_free':[I/math.log(10)*a for a in ah], 'H4_Cepheid':cc,
                'H5_rd_free':[0.]*3+[m*145 for m in base[3:16]]+[0.]*267}
    return packet,bgraw,prediction,directions

def run(np,consumer,prior,precision,backend,contract,lineage,runtime_ref,emit,deadline):
    rid=contract['request_id']; limits=contract['budgets']; acc=contract['acceptance']
    def checktime(): need(time.monotonic()<deadline,'WORKER_COOPERATIVE_DEADLINE')
    sources=contract['sources']
    with open(sources['layout']['path'],'rb') as f: layout=json.load(f)
    with open(sources['design']['path'],'rb') as f: design=json.load(f)
    structure=structure_from_documents(layout,design); structure_raw=raw(structure)
    # Use source metadata, never candidate-produced X or residualized arrays, for oracle.
    keys=[x['key'] for x in structure['nuisance']['columns']]
    X=[[F(row.get(k,'0')) for k in keys] for row in structure['nuisance']['X_sparse_rows']]
    pivots,inv,det=exact_pivots_and_inverse(X,deadline,limits['max_reference_fraction_bits'])
    need(all(i>=16 for i in pivots),'BACKGROUND_HAS_NO_NUISANCE')
    packet,bgraw,prediction,directions=make_packet(structure,layout,consumer,rid)
    packet_raw=raw(packet); packet_sha=sha(packet_raw)
    counter={k:0 for k in ('prepare_attempts','backend_constructors','evaluate_attempts','integration_calls',
             'curve_constructors','real_precision_calls','service_evaluations','curve_log_calls','h5_reference_evaluations')}
    code_keys={consumer.prepare_joint.__code__:'prepare_attempts',backend.__init__.__code__:'backend_constructors',
        consumer.PreparedJoint.evaluate_five.__code__:'evaluate_attempts',prior.integrate_at_fixed_theta.__code__:'integration_calls',
        prior._Curve.__init__.__code__:'curve_constructors',prior._Curve.log_likelihood.__code__:'curve_log_calls'}
    def profile(frame,event,arg):
        if event!='call': return
        checktime(); code=frame.f_code
        name=code_keys.get(code)
        if name:
            counter[name]+=1; need(counter[name]<=limits[name],name+'_CAP')
        if code.co_filename==precision.__file__ and code.co_name=='integrand':
            counter['service_evaluations']+=1
            need(counter['service_evaluations']<=limits['service_evaluations'],'SERVICE_CAP')
    def window(*args,**kwargs):
        counter['real_precision_calls']+=1; before=counter['service_evaluations']
        result=precision.log_exp_quad_interval(*args,**kwargs)
        need(result['evaluations']==counter['service_evaluations']-before,'WINDOW_COUNT')
        return result
    def quad(callback,*args,**kwargs):
        counter['real_precision_calls']+=1; count=0; seen=set()
        def wrapped(u):
            nonlocal count
            need(u not in seen,'REPEATED_QUADRATURE_NODE'); seen.add(u);count+=1
            counter['service_evaluations']+=1
            need(counter['service_evaluations']<=limits['service_evaluations'],'SERVICE_CAP')
            return callback(u)
        result=precision.positive_quad_1d(wrapped,*args,**kwargs)
        need(result['evaluations']==count,'QUADRATURE_COUNT'); return result
    services={'log_exp_quad_interval':window,'positive_quad_1d':quad}
    for name in services: need(callable(services[name]),'SERVICE_WRAPPER')
    backend_doc={'schema':'F9_QUALIFIED_BACKEND_CALLER_RECEIPT_V1',
      'source_pins':{k:consumer.SOURCE_PINS[k] for k in ('linear_gaussian','support')},
      'runtime_reference':runtime_ref,'class_module':backend.__module__,'class_name':backend.__name__,
      'caller_verification_reference':ref({'id':rid+'/source-byte-loader','pins':sources})}
    backraw=raw(backend_doc)
    contexts={}
    def prepare(singular,zero=False,wrong_rows=False):
        oracle=CoordinateOracle(X,pivots,inv,det,singular)
        L=np.zeros((283,oracle.rank),dtype='<f8'); L[:,:63]=np.array(oracle.X,dtype='<f8')
        for j,i in enumerate(oracle.tail): L[i,63+j]=1
        L[oracle.tail[0],-1]=.25
        covariance=L@L.T
        need(covariance[0,oracle.tail[-1]]!=0,'NONZERO_CROSS_DOMAIN_COVARIANCE')
        coordinates=np.array([(j%3-1)/16 for j in range(63)]+[(j%7-3)/32 for j in range(len(oracle.tail))])
        base=np.array(packet['models']['H2_LCDM']['mean_without_nuisance'])
        y=base+L@coordinates
        origin=np.array([(i%5-2)/8 for i in range(283)],dtype='<f8'); origin[2]=base[2]
        scales=np.array(structure['native_to_output_row_scale'],dtype='<f8')
        yn=np.array(y/scales,dtype='<f8'); cn=np.array(covariance/scales[:,None]/scales[None,:],dtype='<f8')
        on=np.array(origin/scales,dtype='<f8')
        if zero: yn[2]+=1/8
        ids=structure['row_ids'][:]
        references={k:ref({'id':rid+'/'+k,'fixture':'synthetic exact-coordinate covariance',
                 'rank':oracle.rank,'no_observations':True}) for k in
            ('statistical_model','covariance_and_cross_blocks','fixed_affine_support',
             'compression_and_offsets','common_nuisance_measure','MM_conditional_model','structure_review','synthetic_fixture')}
        admission={'schema':'F9_CONSUMER_ADMISSION_V1','scope':'ENGINEERING_POINTWISE_ONLY',
            'scenario_id':'synthetic-'+str(oracle.rank)+('-outside' if zero else ''), 'data_kind':'SYNTHETIC',
            'input_sha256':{'y_native_f64le':sha(yn.tobytes()),'C_native_f64le':sha(cn.tobytes()),
                           'affine_origin_native_f64le':sha(on.tobytes()),'row_ids_canonical_json':sha(raw(ids))},
            'structure_sha256':sha(structure_raw),'source_pins':consumer.SOURCE_PINS,
            'backend_receipt_sha256':sha(backraw),'prediction_admission_sha256':prediction['sha256'],
            'coordinates':consumer.COORDINATES,'output_measure':consumer.OUTPUT_MEASURE,
            'common_measure_id':rid+'/same-kappa-deta', 'MM_status':'CONDITIONAL_UNRATIFIED',
            'expected_support_rank':oracle.rank,
            'tolerances':{'relative_cutoff':1e-12,'absolute_cutoff':0.,'support_tolerance':1e-8,'design_relative_cutoff':1e-12},
            'references':references}
        ar=raw(admission)
        if wrong_rows: ids[0],ids[1]=ids[1],ids[0]
        joint=consumer.prepare_joint(yn,cn,ids,affine_origin_native=on,structure_json=structure_raw,
            admission_json=ar,admission_sha256=sha(ar),backend_receipt_json=backraw,
            numpy_module=np,flat_gaussian_class=backend)
        for actual,expected in ((joint._y,scales*yn),(joint._origin,origin),
                                (joint._engine.support.positive_vectors.shape[0],283)):
            need(np.allclose(actual,expected,atol=acc['array_absolute_tolerance'],rtol=acc['array_relative_tolerance']),'TRANSFORM_OR_DIMENSION')
        transformed=(scales[:,None]*cn)*scales[None,:]
        need(joint._transformed_covariance_sha256==sha(transformed.tobytes()),'TCT_HASH')
        need(np.allclose(transformed,covariance,atol=acc['array_absolute_tolerance'],rtol=acc['array_relative_tolerance']),'TCT_EXPECTED')
        need(joint._structure==structure and not joint._y.flags.writeable and not joint._origin.flags.writeable,'STRUCTURE_IMMUTABILITY')
        need(abs(joint._engine.log_prefactor-oracle.logK)<=acc['pointwise_log_absolute_tolerance'],'COMMON_MEASURE_NORMALIZATION')
        return joint,oracle,(scales*yn).tolist(),ar,admission
    def integrated(joint):
        p=contract['precision']
        prec={'schema':'F9_PHYSICAL_PRIOR_PRECISION_V1','source_pins':prior.SOURCE_PINS,
           'consumer_admission_sha256':joint._admission_sha256,'assembly_sha256':packet_sha,
           'services':{k:{'id':getattr(precision,'LOG_SERVICE_ID' if k=='log_exp_quad_interval' else 'QUAD_SERVICE_ID'),
                          'sha256':sources['precision']['sha256']} for k in services},
           'max_quadrature_evaluations':p['quadrature_cap'],'max_window_evaluations':p['window_cap'],
           'absolute_log_error_target':p['absolute_log_error_target'],
           'absolute_scaled_error_target':p['absolute_scaled_error_target'],
           'relative_scaled_error_target':p['relative_scaled_error_target'],
           'caller_verification_reference':ref({'id':rid+'/precision-wrappers','source':sources['precision']})}
        pr=raw(prec)
        return prior.integrate_at_fixed_theta(joint,packet_raw,assembly_sha256=packet_sha,background_json=bgraw,
            consumer_module=consumer,precision_json=pr,precision_sha256=sha(pr),services=services)
    records=[]
    previous=sys.getprofile();sys.setprofile(profile)
    try:
        for case,singular in (('J01',False),('J02',True)):
            emit(case+'_STARTED',{'case':case,'scope':'synthetic full matrix join'})
            joint,oracle,y,ar,admission=prepare(singular); contexts[case]=(joint,oracle,y)
            point=joint.evaluate_five(packet_raw,assembly_sha256=packet_sha)
            result=integrated(joint); differences={}; references={}
            need(result['base_theta_prior']['applied'] is False and result['lnB'] is None and result['sigma'] is None,'NO_GLOBAL_OR_PHYSICAL_PROMOTION')
            for model in MODELS:
                mu=packet['models'][model]['mean_without_nuisance']
                expected=oracle.point(y,mu)
                need(abs(point['models'][model]['log_integral_deta']-expected)<=acc['pointwise_log_absolute_tolerance'],model+'_POINTWISE')
                bound=0.
                if model in directions:
                    logbase,a,b=oracle.quadratic(y,mu,directions[model]); geometry=result['models'][model]['geometry']
                    for name,value in (('a',a),('b',b)):
                        need(math.isclose(geometry[name],value,abs_tol=acc['coefficient_absolute_tolerance'],rel_tol=acc['coefficient_relative_tolerance']),model+'_'+name)
                    if model=='H3_beta_free': expected=log_window(logbase,a,b,.01,-.05,.05,0.,math.log(10))
                    elif model=='H4_Cepheid':
                        lam=math.log(10)/5; x0=-5*math.log1p(.02)/math.log(10)
                        expected=log_window(logbase,a,b,x0,-5*math.log1p(.15)/math.log(10),-5*math.log1p(-.15)/math.log(10),-lam,math.log(lam/.30))
                    else:
                        expected,bound,count=rd_reference(logbase,a,b,1/142,acc['h5_reference_panels'])
                        counter['h5_reference_evaluations']+=count
                    prec=result['models'][model]['precision']
                    need(a>0 and prec['converged'] is True and prec['error_kind']=='ESTIMATED_NOT_CERTIFIED',model+'_NONFLAT_PRECISION')
                value=result['models'][model]['log_conditional_integral']
                allowance=acc['integrated_log_base_tolerance']+bound+acc['h5_reference_roundoff_allowance']
                need(abs(value-expected)<=allowance,model+'_PRIOR_AVERAGE')
                differences[model]=value-expected; references[model]={'log_expected':expected,'allowance':allowance}
            record={'case':case,'status':'PASS','rank':oracle.rank,'eta_dimension':63,
              'normalization_reference':oracle.logK,'conditional_log_differences':differences,'references':references,
              'inputs':admission['input_sha256'],'admission_sha256':sha(ar),
              'common_measure_id':admission['common_measure_id'],'uniform_certificate':False}
            emit(case+'_RESULT',record);records.append(record)
        emit('J03_STARTED',{'case':'J03','scope':'genuine off-support data in fixed affine model'})
        joint,oracle,y,ar,admission=prepare(True,zero=True)
        before=counter['real_precision_calls']
        point=joint.evaluate_five(packet_raw,assembly_sha256=packet_sha); result=integrated(joint)
        for model in MODELS:
            need(point['models'][model]['status']=='ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT','OUTSIDE_SUPPORT_STATUS')
            need(point['models'][model]['log_integral_deta']==float('-inf') and result['models'][model]['log_conditional_integral']==float('-inf'),'LEGITIMATE_ZERO')
        need(counter['real_precision_calls']==before,'ZERO_NO_PRECISION')
        record={'case':'J03','status':'PASS','all_models':'negative infinity on support complement; not underflow'}
        emit('J03_RESULT',record);records.append(record)
        emit('J04_STARTED',{'case':'J04','scope':'changed mean support must fail, not yield zero'})
        bad=copy.deepcopy(packet);bad['models']['H1_TGL']['mean_without_nuisance'][2]+=.125; badraw=raw(bad)
        try: contexts['J02'][0].evaluate_five(badraw,assembly_sha256=sha(badraw))
        except consumer.ConsumerError as exc: need(exc.code=='AFFINE_SUPPORT_CHANGED','WRONG_SUPPORT_ERROR')
        else: raise AssertionError('MISSING_SUPPORT_REFUSAL')
        record={'case':'J04','status':'PASS','error_code':'AFFINE_SUPPORT_CHANGED'};emit('J04_RESULT',record);records.append(record)
        emit('J05_STARTED',{'case':'J05','scope':'row order mismatch before backend construction'})
        before=counter['backend_constructors']
        try: prepare(False,wrong_rows=True)
        except consumer.ConsumerError as exc: need(exc.code=='ROW_ERROR','WRONG_ROW_ERROR')
        else: raise AssertionError('MISSING_ROW_REFUSAL')
        need(counter['backend_constructors']==before,'ROW_REFUSAL_TOO_LATE')
        record={'case':'J05','status':'PASS','error_code':'ROW_ERROR'};emit('J05_RESULT',record);records.append(record)
    finally: sys.setprofile(previous)
    for key,value in counter.items(): need(value<=limits[key],key+'_FINAL_CAP')
    for key in ('prepare_attempts','backend_constructors','evaluate_attempts','integration_calls','curve_constructors','real_precision_calls','h5_reference_evaluations'):
        need(counter[key]==limits[key],key+'_EXACT_EXPECTED')
    need([r['case'] for r in records]==contract['case_order'],'COMPLETE_CASE_SET')
    return {'status':'PASS','request_id':rid,'cases':records,'counts':counter,
        'exact_pivot_rows':pivots,'exact_det_Xp':str(det),'source_design_sha256':sources['design']['sha256'],
        'reference_scope':'exact rational coordinate construction; floats and quadrature bounds are not interval-certified',
        'observed_data':False,'solver_calls':0,'physical_sigma':None,'uniform_certificate':False,
        'provisional_until_supervisor_exit_zero':True}
