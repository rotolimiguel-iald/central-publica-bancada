"""Prepare a reviewable E2 draft. Does NOT create registration or blind seed."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math,argparse
B=Path(__file__).resolve().parents[1];R=B.parent

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def read(n):return json.loads((B/n).read_bytes())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);args=parser.parse_args()
    if not args.tag.isalnum():raise ValueError('Alphanumeric tag required')
    out=B/'bis'/('E2_DESIGN_DRAFT_'+args.tag+'.json')
    if out.exists():raise FileExistsError(out)
    gate=read('PORTAO_DA_AMPLIACAO_V1.json');census=read('bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.json')
    publication=read('bis/e2_publication_census/PUBLICATION_CENSUS.json')
    anchor_GPS=read('cache/gwosc/metadata_2.json')['events']['GW250114_082203-v1']['GPS']
    calibration=sorted(set(census['corpus']['deduplicated_event_list'])|set(publication['published_exclusions']));candidates={}
    scoped=set(publication['not_found_scope_events'])
    for row in census['SNR_ge12_metadata_rows']:
        if row['event'] in calibration:continue
        candidates[row['event']]={**row,'eligible':row['GR_input_eligibility'],
          'published_deformation_at_registration':False if row['event'] in scoped else None,
          'publication_status':'NOT_FOUND_IN_FROZEN_PRIMARY_CENSUS__NOT_UNIVERSAL_ABSENCE' if row['event'] in scoped else 'AWAITING_PUBLICATION_CENSUS',
          'publication_census_scope':publication['definition'] if row['event'] in scoped else None,
          'data_quality_hold':row['event'] in publication['data_quality_holds'],
          'admission_requires':'Absent in witnessed publication corpus, no prior sample exposure; eligible; strain quality; convergence; calibrated nuisance gate'}
    nullcells={};serial=0
    for target in gate['planning_targets']:
        if target['population'] not in ('GWTC5_31','GWTC5_33') or target['N90_mixture_illustration_not_selection'] is None:continue
        for model,label in [('gaussian','G'),('elliptical_t5_measurement_plus_gaussian_nuisance','T5M_GN')]:
            serial+=1;key=target['population']+'_'+target['reading'].replace('-','_')+'_'+label
            nullcells[key]={'kind':'matched_projection','population':target['population'],'reading':target['reading'],
              'N_target_balanced_catalog':math.ceil(target['N90_mixture_illustration_not_selection']),
              'model':model,'draws':100_000_000,'chunk':1_000_000,'seed':13220000+serial,
              'catalog_convention':'Fixed balanced cycles of original full sample std widths and paired E0 point predictions; no data selection by width',
              'not_claimed':'Original target guarantees no power after nuisance addition; covariance/selection/waveform calibration remain OPEN'}
    for j,t in enumerate(gate['route_IV']['validated_grid_targets']):
        key='IV_'+t['population']+'_N'+str(t['N90_validated'])
        nullcells[key]={'kind':'route_IV','population':t['population'],'N_target':t['N90_validated'],
          'target_power_scenario_jitter':t['sigma_jit'],'draws':1_000_000,'chunk':10_000,'seed':13221000+1000*j,
          'sigma_sys_INPUT':0.,'scope':'Empirical p/upper confidence bound at target; 1M cannot certify 5sigma tail even with zero exceedances'}
    def uniform(lo,hi):return {'kind':'Uniform','minimum':lo,'maximum':hi}
    priors={'mass_1':uniform(15,100),'mass_2':uniform(10,100),'mass_ratio':{'kind':'Constraint','minimum':.125,'maximum':1},
      'chi_1':uniform(-.99,.99),'chi_2':uniform(-.99,.99),'luminosity_distance':uniform(100,2000),
      'theta_jn':{'kind':'Sine','minimum':0,'maximum':math.pi},'phase':{**uniform(0,2*math.pi),'boundary':'periodic'},
      'ra':{**uniform(0,2*math.pi),'boundary':'periodic'},'dec':{'kind':'Cosine','minimum':-math.pi/2,'maximum':math.pi/2},
      'psi':{**uniform(0,math.pi),'boundary':'periodic'},'geocent_time':uniform(anchor_GPS-.15,anchor_GPS+.15),
      'dtau220':uniform(-.8,2),'dtau440':uniform(-.8,4),'domega220':uniform(-.8,2),'domega440':uniform(-.8,2)}
    data={};pins={}
    def pin(n):pins['ORDEM_013_RINGDOWN/'+n]=sha(B/n)
    names=['PORTAO_DA_AMPLIACAO_V1.json','NUISANCE_V1.json','REGISTRO_C4.json','bis/PART_B_BUDGET_START.json',
      'bis/e0_core/DATASET.json','bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.json',
      'bis/e1_selection/GR_O4A_ADENDO.json','bis/E0_ROUTE_IV_PROVENANCE.json',
      'bis/e2_publication_census/PUBLICATION_CENSUS.json','bis/e2_publication_census/PUBLICATION_CENSUS.md',
      'bis/E2_REMNANT_BRIDGE_INPUT.json','cache/gwosc/metadata_2.json',
      'refeito/e0_mc_guarded_013bis.py','refeito/e0_route_iv_power_013bis_v2.py',
      'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json','bis/E2_NULL_GUARD_CONTROLS.json']
    for n in set(names+list(read('bis/E0_ROUTE_IV_PROVENANCE.json')['files'])):pin(n)
    for det,prefix in [('H1','H'),('L1','L')]:
        data[det]={}
        for kind,gps in [('onsource',1420877824),('offsource',1420873728)]:
            folder='on_source' if kind=='onsource' else 'offsource'
            n=f'cache/gwosc/{folder}/{prefix}-{det}_GWOSC_O4b_4KHZ_R1-{gps}-4096.hdf5'
            pin(n);pin(n+'.receipt.json');receipt=read(n+'.receipt.json')
            if pins['ORDEM_013_RINGDOWN/'+n]!=receipt['sha256']:raise ValueError('Cached strain receipt mismatch')
            data[det][kind+'_path']='ORDEM_013_RINGDOWN/'+n;data[det][kind+'_sha256']=receipt['sha256']
    pilot={'event':'GW250114_082203','mode':'calibration','variant':'220_plus_440_free',
      'privacy_mode':'procedural_same_host','fixed_deformation_parameters':{},
      'remnant_conversion_INPUT':read('bis/E2_REMNANT_BRIDGE_INPUT.json'),
      'output_directory_name':'E3_PSEOB_PILOT_V1','label':'GW250114_pSEOBv4HM_PA_pilot',
      'event_GPS':anchor_GPS,'segment_start_GPS':float(math.floor(anchor_GPS)-12),'duration_s':16,'sample_rate_hz':4096,
      'minimum_frequency_hz':20.,'maximum_frequency_hz':1024.,'reference_frequency_hz':20.,
      'psd_duration_s':256,'psd_segment_s':8,'offsource_exclusion_s':16.,'onsource_roll_off_s':.2,
      'quality_required':['DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3'],
      'injection_flags_required':['NO_CBC_HW_INJ','NO_BURST_HW_INJ','NO_DETCHAR_HW_INJ','NO_STOCH_HW_INJ'],
      'detectors':['H1','L1'],'data':data,'priors':priors,'wall_budget_seconds':8*3600,
      'sampler':{'seed':132203,'workers':24,'nlive':512,'dlogz':.1,'walks':50,'maxcall':3_000_000,
        'minimum_posterior_samples':1000,'minimum_effective_samples':100},
      'prior_scope':'INPUT broad pilot priors, not a reproduction of every published prior; full source masses/spins/sky/distance/deformations free',
      'family_scope':'Aligned-spin pSEOBNRv4HM_PA versus released precessing pSEOBNRv5PHM; difference not attributable without calibration'}
    design={'status':'DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION','created_utc':datetime.now(timezone.utc).isoformat(),
      'witness_relative_to_Chatgpt':'TUNEL/DO_CHATGPT/ENTREGA_013BIS_E2_REGISTRO_V1.md',
      'budget_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json','budget_sha256':sha(B/'bis/PART_B_BUDGET_START.json'),
      'runtime_manifest_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json',
      'runtime_manifest_sha256':sha(B/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json'),
      'calibration_event_ids':calibration,'test_candidates':candidates,'readings':gate['readings'],
      'event_reference_GPS':{'GW250114_082203':anchor_GPS},
      'publication_census':{'path':'ORDEM_013_RINGDOWN/bis/e2_publication_census/PUBLICATION_CENSUS.json',
        'sha256':sha(B/'bis/e2_publication_census/PUBLICATION_CENSUS.json'),
        'known_pseob_unique':39,'additional_published_exclusions':publication['published_exclusions'],
        'scope':'48 exposed/published calibration identities; only39 belong to prior pSEOB dataset. Fourteen eligible absent in scoped census, not universal absence; four quality holds',
        'incidental_exposure':publication['incidental_exposure']},
      'quality_INPUT':gate['quality_INPUT'],'planning_targets':gate['planning_targets'],
      'input_pins_relative_to_Chatgpt':pins,'own_code_tree_sha256':{},'extra_code_trees':{},
      'observables':{'primary':'Full paired pSEOB posterior dtau220 with calibrated c(sigma)/c(SNR) and normalized selection',
        'secondary':'dtau440, variants only220 and220+440; deformation440 INPUT','route_IV':'Population width of df220 from full posterior likelihoods, common mean free'},
      'statistics':{'ln_B':'Relative restricted-model evidence versus GR, same normalized nuisance prior and selection; absent normalization => null, never KDE score relabeled BF',
        'relative_exclusion_rule':read('REGISTRO_C4.json')['exclusion_rule'],
        'matched_z':'delta.T C^-1 (y-Xm)/sqrt(delta.T C^-1 delta); E1 local covariance only synthetic INPUT until physically calibrated',
        'one_sided_p5':.5*math.erfc(5/math.sqrt(2)),'LRT_IV_threshold_strict_greater':25.,
        'multiple_readings':'Report all ten; no selection. Any global claim requires Bonferroni p<=p5/number_testable_readings and separate secondary-channel accounting; per-reading5 remains labeled per-reading',
        'jackknife':'All leave-one-event-out results and verdict changes; a discovery needs every deletion same direction and no relative exclusion reversal',
        'maximum_information_weight_INPUT':.20,'weight_dominance':'Compute tau inverse-variance and IV inverse-fourth-weight shares; above cap blocks population discovery but does not drop event',
        'split_null_seed':132299,'split_null':'Seeded event permutation alternating halves; compare nuisance-corrected means with covariance including shared nuisance. p<.01 blocks combination; calibration required',
        'offset_fixed_zero':'PROIBIDA_COMO_TESTE'},
      'systematic_gate':{'sigma_c_requirement':'strictly below abs(predicted_delta)/5; /15 displayed separately',
        'floor_divisor_primary_INPUT':5,'floor_divisor_sensitivity_only':15,'sigma_c_current':None,
        'calibration_required':'two-family injected free source recovery at relevant SNR; covariance, coverage, selection and transfer, hash-linked review',
        'admit_event_only_after_green':True,'red_maximum':'INCONCLUSIVE_SYSTEMATICS','physical_z_when_red':None},
      'nulls':{'dataset_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/e0_core/DATASET.json',
        'nuisance_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/NUISANCE_V1.json','cells':nullcells,
        'E2_now':'synthetic posterior nulls only; Gaussian marginal and t5 measurement shared catalog scale plus independent Gaussian nuisance',
        'E3_3_later':'Two-family PE injection bias/c(SNR)/sigma_sys and brownian transfer; N/seeds/jobs in witnessed E3.2 allocation before execution',
        'interpretation':'Empirical p and confidence intervals, analytic checks; no pass/fail tuning or declaration of physical 5sigma. IV empirical UL explicit; target jitter only labels prospective N'},
      'route_IV':{'model_primary_INPUT':'brownian','ensemble_delta_f':0.,'common_nonzero_mean':'systematic, not TGL prediction',
        'sigma_jit_recovered':None,'sigma_sys':None,'targets':gate['route_IV']['validated_grid_targets'],
        'target_status':'LOWER_BOUND_UNTIL_PIPELINE_TRANSFER_AND_SYSTEMATICS',
        'weights':'Fisher for variance scales sigma^-4; full likelihood used, no posterior-width selection',
        'secondary_jumps':'Center by jointly fitted nuisance mean; count posterior outlier probabilities abs(df-mu)>3*sigma_i; mixture fraction free Uniform[0,1]; empirical null and trials required, otherwise descriptive only',
        'other_unravelings':{'deterministic':'zero excess frequency-width signal','Cauchy':'variance undefined in ideal process, robust MAD required; never equate to Gaussian sd','Poisson_pm_pi_over_2':'zero-jump component plus outliers; separate mixture test, not Brownian width likelihood'}},
      'conventions':{'primary':'Fractional pSEOB DTau220/DTau440 postpeak QNM deformation',
        'alternatives':'C7 native envelope22/44 and C5 shared Gamma for overtones; keep separate with mapping report',
        'partition_clock_unraveling_and_440':'INPUT; all C1 readings parallel; no selected reading'},
      'pe_jobs':{'GW250114_PILOT':pilot},'downloads':{},
      'allocation_policy':{'relative_to_Chatgpt':'ORDEM_013_RINGDOWN/ORCAMENTO_40H.json',
        'max_job_wall_seconds':8*3600,'requires':'Parent E2 hash, pinned E2_PE_JOBS_V2 config, allocation hash witness in tunnel before jobs; publication and quality reviews per event'},
      'blinding':{'status':'SEED_NOT_YET_CREATED_DRAFT','seed_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/cache/E2_PRIVATE/BLIND_SEED_V1.bin',
        'seed_commitment_sha256':None,'offset_half_range':1.,
        'minimum_information_to_unblind':max(t['I_tau_expected_target90'] for t in gate['planning_targets'] if t['population']=='GWTC5_31' and t['I_tau_expected_target90'] is not None),
        'scope':'Procedural same-host blinding, not independent custody; raw sampler logs/checkpoints private; no reading means/signs before gate',
        'release_requires':'Target per reading plus systematic gate green and independent review receipt bound to registration/eventset; unresolved mappings never unblind to claim'},
      'future_allocation':'E3.2 signed-by-hash manifest with parent registration and tunnel witness, permitted pipeline/config schema only; scientific code edits require new witnessed amendment before any new test bytes',
      'permitted_verdicts':['NOT_FALSIFIED_UNDERPOWERED','NOT_FALSIFIED_POWERED','INCONCLUSIVE_SYSTEMATICS','EXCLUDED_IN_READING','FALSIFIED_IN_READING','AWAITING_DATA'],
      'forbidden_verdicts':['CONFIRMED','PROVED'],'stopping':'Target attained, red gate with measured no correction route, operator, or hard40hdeadline; do not stop at deliverable milestone',
      'future_catalogs':'AWAITING_DATA; schedule OPEN/DECLARADO from primary chronology sources; no promise',
      'unpaid_before_execution':['Normalized hierarchical selection','Physically calibrated nuisance','PE pilot convergence','Two-family injection campaign','Blind event PE','Full posterior extraction E7'],
      'draft_builder_sha256':sha(Path(__file__))}
    with out.open('x',encoding='utf-8') as f:json.dump(design,f,indent=2,ensure_ascii=False,allow_nan=False)
    print(json.dumps({'draft':out.name,'sha256':sha(out),'null_cells':len(nullcells),'new_execution_authorization':False}))

if __name__=='__main__':main()
