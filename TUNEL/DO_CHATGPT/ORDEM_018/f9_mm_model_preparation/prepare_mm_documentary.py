"""Custody and symbolic contract assembly only. Never open raw observation files."""
from pathlib import Path
import hashlib
import json
import os
import datetime as dt

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
CHECKS=[]
PINS=[]

def check(label,truth):
    CHECKS.append({'name':label,'passed':bool(truth)})
    if not truth:raise AssertionError(label)

def digest(data):return hashlib.sha256(data).hexdigest()

def opaque_json(data):
    # Numeric JSON tokens are not interpreted. Selected scientific error widths are
    # existing strings; central-value string fields are never selected for output.
    return json.loads(data,parse_float=lambda _:None,parse_int=lambda _:None)

def source(path,expected=None):
    p=Path(path)
    if p.suffix.lower() not in ('.md','.json','.py'):raise ValueError('Raw observation source refused')
    data=p.read_bytes();h=digest(data)
    if expected:check('source pin '+p.name,h==expected)
    PINS.append({'path':str(p),'bytes':len(data),'sha256':h,'read_scope':'byte custody; selected metadata/formula fields only'})
    return data

def write_new(name,obj):
    text=obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
    data=text.encode('utf-8');p=BASE/name;tmp=p.with_name(p.name+'.tmp')
    if p.exists() or tmp.exists():raise FileExistsError(p)
    with tmp.open('xb') as f:f.write(data)
    if tmp.stat().st_size!=len(data):raise RuntimeError('Incomplete write')
    os.replace(tmp,p)

def main():
    request=json.loads(source(ROOT/'F9_MM_MODEL_PREPARATION_REQUEST.json'))
    raw={}
    for key in ('source_draft','source_resolver','source_calibration'):
        pin=request[key];raw[key]=source(pin['path'],pin['sha256'])
        check('request bytes '+key,len(raw[key])==pin['bytes'])
    resolver=opaque_json(raw['source_resolver']);calibration=opaque_json(raw['source_calibration'])
    check('no opening in request',request['data_opening_authorized'] is False)
    check('calibration observed outputs absent',all(v is None for v in calibration['outputs_now'].values()))
    admitted={}
    for sid in ('nonstellar_errors','linear_design','linear_note','flow_review','selection_v01'):
        pin=resolver['sources'][sid];admitted[sid]=source(pin['path'],pin['sha256'])
    error_meta=opaque_json(admitted['nonstellar_errors']);design=opaque_json(admitted['linear_design'])
    code={};codepins={}
    for pin in error_meta['sources']:
        p=Path(pin['path'])
        if p.name in ('data_loader.py','equations.py','intercept.py'):
            data=source(p,pin['sha256']);code[p.name]=data.decode('utf-8').splitlines();codepins[p.name]=PINS[-1]
    check('three code sources admitted',len(code)==3)
    errors=error_meta['megamaser_error_inputs']
    selected=[(i,row) for i,row in enumerate(design['rows']) if row['family']=='megamaser']
    check('five MM input rows',len(errors)==len(selected)==5)
    check('all267linear rows retained',len(design['rows'])==267)
    check('identity order retained',[row['row_id'] for _,row in selected]==[r['row_id'] for r in errors])
    check('no sixth maser anchor',all(r['name'] not in ('NGC_4258','N4258') for r in errors))
    check('native MM responses',[ (r['X'],r['a_h'],r['c_C']) for _,r in selected]==[({},'1','0')]*5)
    configs={k:error_meta['config'][k] for k in ('mm','mm_dz','q0','j0','vpec_error','vcorr_mm')}
    check('distance redshift branch',configs['mm_dz']['value'] is True)
    check('existing2M++ correction',configs['vcorr_mm']['value']=='2M++')
    rows=[]
    safe_error_fields=('name','row_id','distance_minus_Mpc','distance_plus_Mpc','sigma_v_km_s','sigma_distance_Mpc_upstream')
    for k,(err,(index,row)) in enumerate(zip(errors,selected),1):
        check('distance unconverted '+err['name'],err['distance_centre_converted'] is False and err['variance_logH2'] is None)
        published={f:err[f] for f in safe_error_fields}
        symbol='MM'+str(k)
        variance=f"(1/ln(10)^2)*[({err['sigma_distance_Mpc_upstream']} Mpc / D_{symbol})^2 + (({err['sigma_v_km_s']} km/s)^2 + (s_pec)^2)/(v_{symbol})^2]"
        rows.append({'id':symbol,'name':err['name'],'row_id':row['row_id'],'local_index_zero_based':index,
            'source_of_names_and_errors':'METADADOS_ERROS_NAO_ESTELARES_V01.json#/megamaser_error_inputs',
            'published_widths_copied_without_recalculation':published,
            'primitive_symbols':{'D':f'D_{symbol} [Mpc]','v_corr_2Mpp':f'v_{symbol} [km/s]'},
            'protected_references':{'distance_centre':None,'corrected_velocity_centre':None,'y_observed':None,'working_variance_numeric':None},
            'native_design':{'X':{},'a_h':'1','c_C':'0','unit':'dex'},
            'magnitude_scaled_design':{'X':{},'a_h':'5','c_C':'0','unit':'mag equivalent; all blocks transformed'},
            'mean_formula':'h_model(theta) from existing physical model; no new galaxy nuisance',
            'y_formula':f'log10[(U(v_{symbol})/(1 km/s))/(D_{symbol}/(1 Mpc))]',
            'variance_upstream_formula':variance,'variance_unit':'dex^2',
            'variance_magnitude_formula':'25*variance_upstream',
            'full_derivative_alternative':'a=-1/(ln10*D); b=(1+z*Fprime/F)/(ln10*v); V_delta=a^2*Sigma_DD+2*a*b*Sigma_DV+b^2*Sigma_VV',
            'calibrated_distribution':None,'correlations_with_other_rows':None,'physical_interval_level_or_likelihood':None})
    excerpts=[]
    for name,ranges in {'data_loader.py':[(528,542),(549,589)],'equations.py':[(324,324),(630,643)],'intercept.py':[(53,74)]}.items():
        for first,last in ranges:
            snippet='\n'.join(code[name][first-1:last])+'\n'
            excerpts.append({'file':codepins[name]['path'],'source_sha256':codepins[name]['sha256'],'line_start':first,'line_end':last,
                'excerpt':snippet,'excerpt_sha256_utf8':digest(snippet.encode('utf-8')),'executed':False})
    formulae={
        'base_definitions':{'ell':'ln(10)','z':'v/c with c in km/s','A':'(q0+3)/2','B':'(11+7*q0+3*q0^2-j0)/6',
            'F':'1-A*z+B*z^2','U':'v*F(v/c)','y':'log10[(U/v_unit)/(D/D_unit)]','h':'log10(H0/H_unit)',
            'sigmaD':'(abs(d_minus)+abs(d_plus))/2','sigmaV2':'sigma_v^2+s_pec^2'},
        'upstream_variance':'(sigmaD^2/D^2+sigmaV2/v^2)/ell^2',
        'derivatives':{'a_D':'-1/(ell*D)','b_v':'(1/v+Fprime/(c*F))/ell','Fprime':'-A+2*B*z','Fsecond':'2*B',
            'Uprime':'F+z*Fprime','Usecond':'(2*Fprime+z*Fsecond)/c','f_DD':'1/(ell*D^2)',
            'f_vv':'(Usecond/U-(Uprime/U)^2)/ell','f_Dv':'0'},
        'cross_covariance_first_order':'Cij=a_i*a_j*SigmaDDij+a_i*b_j*SigmaDVij+b_i*a_j*SigmaVDij+b_i*b_j*SigmaVVij',
        'distance_endpoint_widths':{'lower_y':'log10(1+d_plus_abs/D)','upper_y':'-log10(1-d_minus_abs/D)','guard':'D>d_minus_abs'},
        'exact_pushforward':'pY(y)=integral pDV(D(y,v),v)*product_i(ln(10)*D_i(y_i,v_i)) d^5v',
        'inverse':'D(y,v)=U(v)/(H_unit*10^y)',
        'mean_bias_second_order':'[SigmaDD/D^2+(Usecond/U-(Uprime/U)^2)*SigmaVV]/(2*ell)',
        'native_to_mag':'y_new=T*y; X_new=T*X; a_new=T*a; c_new=T*c; C_new=T*C*T^T; MM scale5',
        'not_executed':'All expressions are symbolic strings; no primitive observation or variance evaluated.'}
    contract={
        'schema':'F9_MM_SYMBOLIC_PREPARATION_V1','request_id':request['request_id'],
        'status':'CONCRETE_PREPARATION_NOT_RATIFIED_NOT_DATA_OPENING','recommendation':'A_UPSTREAM_FIXED_ERROR_WORKING_GAUSSIAN',
        'ratified':False,'physical_models_changed':False,'local_row_count_preserved':267,'nuisance_count_preserved':63,
        'alpha_priors_selection_MM_exclusion_changed':False,'opening_under_section6':False,
        'rows':rows,'fixed_upstream_config':configs,'formulae':formulae,
        'alternatives':{
            'A':{'sampling_law':'Ystar|Rstar ~ Gaussian_on_common_affine_support(mu_model(theta)+X*eta,C_s(Rstar))',
                'interpretation':'Stipulated working experiment at fixed reference scales, not a proved conditional law of original distance estimators.',
                'recommended_error_recipe':'H0DN_MM_DZ_UPSTREAM_SYMMETRIC; do not silently replace b_up=1/(ln10*v) with full cosmographic derivative',
                'proposed_MM_dependence':'Positive diagonal MM block and zero MM-rest cross block, explicit working INPUT only; not empirical independence.',
                'reference_binding':'D_ref,v_ref and errors/units/hash fixed in future authorized step, common to hypotheses and parameter evaluations; never derive D_ref=U(v)/H0(theta).',
                'reference_endogeneity':'Mandatory provenance: reported/estimated/derived from same observations/independent design. Freezing or independence alone does not prove true covariance.',
                'do_not_condition_on_full_primitives':'Conditioning literally on observed D and v fixes y=f(D,v); nondegenerate Gaussian law does not follow.',
                'ratification_status':None,'common_C_artifact_certificate':None,'physical_sampling_law_adequacy':None,
                'numeric_weights_status':'OPEN_REFERENCE_CENTRES_NOT_READ'},
            'B':{'sampling_law':'Joint positive-domain primitive measurement/calibration distribution with covariance/asymmetry and specified selection; exact pushforward or justified approximation',
                'requires':['Primitive likelihood or generative law; posterior alone is insufficient without original prior','Correct distance type and velocity convention','Cross-galaxy/cross-probe dependence and no duplicate peculiar-velocity component','Normalization and support, positivity/truncation if needed','Global null-tail calibration or separately proved bound'],
                'fixed_covariance_guaranteed':False,'Gaussian_pivot_inherited':False,'adopted':False}},
        'shared_covariance_support':{
            'scope':'C_s fixed and common across five hypotheses within each frozen scenario; scenarios may differ as already registered.',
            'matrix_ready':False,'covariance_numbers':None,'dependence_policy_adopted':None,
            'positivity_guard':'D_ref>0, U(v_ref)>0, finite variances strictly positive; all units and row IDs agree.',
            'no_silent_failure':'Unavailable references or dependence definitions -> OPEN_MODEL_COMPONENT, not dropping MM or zero variance.',
            'MM_rank_statement':'Independent positive5x5block adds5supported noise dimensions. This is conditional, not a measured joint rank.',
            'actual_joint_rank':None,'actual_quotient_rank':None,'actual_global_span_rank':None},
        'calibration_consequences':{
            'source_candidate_pin':request['source_calibration'],
            'A':'Current residual/gain envelopes apply only if entire stipulated Gaussian experiment, common support/C, global span and certificate requirements hold.',
            'conditional_structural_limits':{'local_rows':267,'joint_rows':283,'inherited_constraints':72,'rank_upper':211,'nuisance_rank_required':63,'residual_df_upper':148,'global_span_upper_without_cepheid_shift':17,'global_span_upper_with_cepheid_shift':18},
            'not_a_rank_measurement':True,'no_new_degree_subtraction':True,
            'B':'No automatic transfer of chi-square pivot/global-span envelopes through nonlinear or parameter-dependent primitive likelihood.',
            'known_flag_is_not_proof':True,'estimated_C_even_independent_not_known_C':True,
            'domination_extension':'Only with uniformly proved Gaussian Sigma_true<=a*C_work, compatible support and controlled mean; a not supplied here.'},
        'outputs_now':{'five_numeric_variances':None,'central_D_v':None,'y':None,'joint_C':None,'S':None,'g':None,'H0':None,'F9':None,'likelihood':None,'sigma':None},
        'raw_catalogues_opened':False,'upstream_imported_or_executed':False,'scientific_execution':False,'models_called':0,'downloads':0}
    write_new('CONTRATO_MM_CANDIDATO.json',contract)
    controls=[
        {'id':'MM-P01','target':'Identity/order/unit wiring','fixture':'Synthetic five rows with existing IDs and symbolic/native responses; no actual centres.','expected':'267 rows retained; MM X0,a_h1,c_C0; after magnitude scaling a_h5 and covariance congruence, no sixth N4258.'},
        {'id':'MM-P02','target':'Native versus magnitude likelihood','fixture':'Invented positive-definite covariance with nonzero MM-rest cross-block, synthetic residuals and means.','expected':'Same quadratic form after T; Jacobian common handled on support; scaling only diagonal variances must fail.'},
        {'id':'MM-P03','target':'Full versus upstream derivative','fixture':'Symbolic derivative and later synthetic finite-difference cases with fixed q0/j0.','expected':'b_full=(1+zFprime/F)/(ell*v); upstream b_up=1/(ell*v) distinguished; no silent recipe replacement.'},
        {'id':'MM-P04','target':'Signed cross-covariance','fixture':'Synthetic correlated D,V with known signed joint covariance and external shared component.','expected':'J Sigma J^T including mixed signs; adding the same peculiar budget twice refused.'},
        {'id':'MM-P05','target':'Asymmetric interval transformation','fixture':'Synthetic D and unequal positive lower/upper widths with valid domain.','expected':'Distance upper endpoint maps to lower y; exact widths unequal; D<=lower width produces explicit domain failure, no clipping.'},
        {'id':'MM-P06','target':'Exact nonlinear Jacobian and normalization','fixture':'Invented normalized positive-domain joint p(D,V), not an observed posterior.','expected':'(D,V)->(Y,V) uses product ln10*D; marginal over V normalizes; treating nonsquare Jacobian as determinant or counting Y and D independently fails.'},
        {'id':'MM-P07','target':'Working Gaussian pivot applicability','fixture':'Entirely synthetic fixed common C and X with known support, plus externally fixed Rstar.','expected':'Analytic Gaussian residual pivot applies; future simulations only sanity-check, not independent proof of rare5sigma coverage. Reuse covered C01-C08 results by receipt rather than rerun.'},
        {'id':'MM-P08','target':'Endogenous/estimated variance negative control','fixture':'Synthetic random variance built from same primitive sample and independently estimated variance with known sampling law.','expected':'No unconditional chi-square certificate from a frozen/known flag. Coverage requires the specified law, not conditional rhetoric.'},
        {'id':'MM-P09','target':'Support changes and positive MM block','fixture':'Synthetic rank-known rest block and MM positive block, then singular/correlated variants.','expected':'Independent positive block adds5dimensions; unsupported nuisance/kernel mismatch explicitly fails; never substitute preflight262 for full267.'},
        {'id':'MM-P10','target':'Parameter/model invariance','fixture':'Mock model iterator with declared hypothetical parameters, no cosmology evaluation.','expected':'Same reference/variance/hash/row vector across models and fit points. Attempt D_ref=U(v)/H0(theta) or model-specific q0/j0 in shared data transform rejected.'},
        {'id':'MM-P11','target':'Primitive positive-domain and mean bias','fixture':'Artificial positive/truncated primitive laws with declared normalization and asymmetric variants.','expected':'Nonlinearity can shift mean; no automatic common-C/global-span claim or Gaussian tail certificate. Positivity-based rejection changes law unless normalized.'},
        {'id':'MM-P12','target':'Custody and incomplete references','fixture':'Metadata doubles with changed source hash, missing D_ref/v_ref, wrongunits, nonfinite/nonpositive uncertainty.','expected':'Fail visibly; no raw file discovery, no model/provider fallback, no deletion of a selected maser.'}
    ]
    write_new('PLANO_CONTROLES_SINTETICOS_MM.json',{'request_id':request['request_id'],'status':'PLAN_ONLY_NOT_EXECUTED',
        'controls':controls,'real_values_allowed':False,'execution_authorized_in_this_unit':False,
        'C01_C08_consumed_controls':'Do not reopen/repeat. ROOT may cite existing verified coverage; this unit does not claim to have rerun it.',
        'tail_limit':'Finite synthetic runs do not certify5sigma global tails by themselves; no alpha/MonteCarlo budget allocated here.'})
    write_new('FONTES_E_FORMULAS.json',{'request_id':request['request_id'],'sources':PINS,'code_excerpts':excerpts,
        'allowed_error_fields':list(safe_error_fields),'protected_fields_not_interpreted_or_exposed':['distance centre','v_corr_2mpp_km_s','logh_value','observed H0, y, S, g, likelihood and fits'],
        'source_read_policy':'Source bytes hashed for custody; numeric JSON tokens suppressed before metadata navigation, central string fields omitted. Only selected noncentral error/config strings exported. No .dat/HDF5/NPZ/posterior opened.',
        'primary_paper_interval_semantics':'Not qualified by the admitted metadata/code alone; no new downloads made.',
        'formulas':formulae})
    check('all numeric MM outputs absent',all(all(v is None for v in row['protected_references'].values()) for row in rows))
    check('all observed contract outputs absent',all(v is None for v in contract['outputs_now'].values()))
    check('MM candidate unratified',contract['ratified'] is False and contract['opening_under_section6'] is False)
    check('new synthetic controls only planned',all(c['id'].startswith('MM-P') for c in controls))
    for name in ('CONTRATO_MM_CANDIDATO.json','PLANO_CONTROLES_SINTETICOS_MM.json','FONTES_E_FORMULAS.json'):
        json.loads((BASE/name).read_bytes());check('JSON parse '+name,True)
    write_new('VALIDACAO_DOCUMENTAL.json',{'status':'PASS_CUSTODY_AND_SYMBOLIC_SCHEMA_ONLY','checks_passed':len(CHECKS),'checks':CHECKS,
        'scientific_tests_executed':False,'observed_quantities_calculated':False,'source_code_executed':False,'shared_memories_modified':False})
    files=[]
    for p in sorted(BASE.rglob('*')):
        if p.is_file() and p.name!='MANIFESTO_ENTREGA.json':
            data=p.read_bytes();files.append({'path':str(p.relative_to(BASE)),'bytes':len(data),'sha256':digest(data)})
    write_new('MANIFESTO_ENTREGA.json',{'request_id':request['request_id'],'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'status':'DOCUMENTARY_SYMBOLIC_PREPARATION_COMPLETE_NOT_ADOPTED','files':files,
        'centres_exposed_or_converted':False,'science_executed':False,'remote_model_calls':0,'downloads':0,'originals_gate_memories_changed':False})
    for name in ('ESPECIFICACAO_SIMBOLICA_MM.md','CONTRATO_MM_CANDIDATO.json','MANIFESTO_ENTREGA.json'):
        b=(BASE/name).read_bytes();print(json.dumps({'file':name,'bytes':len(b),'sha256':digest(b)}))
    print(json.dumps({'documentary_checks':len(CHECKS),'sources_pinned':len(PINS),'MM_rows':len(rows),'controls_planned_not_executed':len(controls),'manifest_files':len(files)}))

if __name__=='__main__':main()
