"""Assemble the prescribed V1.1 design beside V1, without registration/activation."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,sys
import numpy as np
from scipy.optimize import brentq
from scipy.stats import chi2,norm
B=Path(__file__).resolve().parents[2];ROOT=B.parent;D=B/'bis/015/t03';C=B/'bis/e2_code_v1_1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def save(p,obj):
    with p.open('xb') as f:f.write((json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
def main():
    sys.path.insert(0,str(C));import registration_guard as guard
    source=B/'RINGDOWN_5SIGMA_V1.json';old=load(source);reg=copy.deepcopy(old);now=datetime.now(timezone.utc).isoformat()
    oldnote=ROOT/old['witness_relative_to_Chatgpt'];scope=D/'R5_SOURCE_CLOSING.json';r5=D/'R5/generation_4096/RESULT.json'
    assert sha(source)==guard.V1_PIN and sha(oldnote)==guard.V1_WITNESS_PIN
    assert load(r5)['status']=='R5_SOURCE_ONLY_QUALIFIED'
    for key in ('activation','registration_provenance','review_candidate_provenance','independent_review_files_sha256','draft_builder_sha256','budget_sha256'):
        reg.pop(key,None)
    reg.update(status='DRAFT_NOT_REGISTERED',registration_id='RINGDOWN_5SIGMA_V1_1',created_utc=now,registered_utc=None,
        parent_registration_sha256=sha(source),v1_witness_sha256=sha(oldnote),statistical_subobject_sha256=guard.statistical_digest(old),
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1.md',
        budget_relative_to_Chatgpt='ORDEM_013_RINGDOWN/bis/PART_015_BUDGET_START.json',
        own_code_tree_sha256={p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')})
    reg['activation_v1_1']=dict(receipt_relative_to_Chatgpt='ORDEM_013_RINGDOWN/bis/015/E2_V1_1_REGISTRATION_RECEIPT.json',
        probes_result_relative_to_Chatgpt='ORDEM_013_RINGDOWN/bis/015/t03/C1_GUARD_MUTATION_TESTS_V1_1.json',
        qualification_R5_relative_to_Chatgpt=r5.relative_to(ROOT).as_posix(),qualification_scope_relative_to_Chatgpt=scope.relative_to(ROOT).as_posix(),
        qualification_scope_sha256=sha(scope),qualification_inputs_relative_to_Chatgpt=(D/'R5/INPUT_MANIFEST.json').relative_to(ROOT).as_posix())
    budget_source=B/'bis/FINAL_DELIVERY_RECEIPT.json'
    reg['budget_rule_v1_1']=dict(budget_relative_to_Chatgpt=reg['budget_relative_to_Chatgpt'],source_receipt_relative_to_Chatgpt=budget_source.relative_to(ROOT).as_posix(),
        source_receipt_sha256=sha(budget_source),machine_free_receipt_relative_to_Chatgpt='TUNEL/PARA_CHATGPT/RECIBO_015_MAQUINA_LIVRE.md',
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_RELOGIO.md',deadline_hours=168,
        count_rule='Union of occupied machine intervals; not sum of parallel workers. Start only immediately before first phase-P heavy job after release.')
    reg['allocation_policy']=dict(pattern='ORCAMENTO_015_v*.json',max_job_wall_seconds=28800,
        chain_rule='Consecutive k, previous allocation hash, witnessed chronology; cumulative jobs/downloads cannot replace earlier values')
    config=load(D/'R5/CONFIG_4096_RESERVED_INPUT.json');config['output_directory_name']='E3_PSEOB_PILOT_V2_S220';config['label']='GW250114_PILOT_V2_S220'
    assert config['sampler']['seed']==load(D/'R5/INPUT_MANIFEST.json')['pilot_seed_INPUT']
    reg['pe_jobs']={'GW250114_PILOT_V2_S220':config}
    target={x['reading']:x['I_tau_expected_target90'] for x in old['planning_targets'] if x['population']=='GWTC5_31'}
    blind=reg['blinding'];blind['minimum_information_to_unblind_global_claim_legacy']=blind.pop('minimum_information_to_unblind')
    blind['minimum_information_to_unblind_by_reading']=target;blind['target_population']='GWTC5_31'
    blind['release_columns_by_reading']={reading:[reading+':'+column for column in ('matched_z','p_empirical','information')] for reading,value in target.items() if value is not None}
    blind['release_requires']='minimum_information_to_unblind_by_reading[reading] paid; systematic gate green; independent receipt bound to this reading, registration and dataset; only namespaced reading summaries. Global claim additionally requires frozen Bonferroni and every testable target; no raw shared posterior release by a per-reading permission.'
    blind['unblinding_dataset_sha256']=None
    # No release dataset exists yet; permission necessarily remains false on this draft.
    cells={};cov_variants=[('zero','VZERO'),('kde_0.7','KDE07'),('WLS_q90','WLS')];seed=15261001
    for name,cell in old['nulls']['cells'].items():
        if cell['kind']=='matched_projection' and cell['model']!='gaussian':
            for variant,suffix in cov_variants:
                x=copy.deepcopy(cell);x.update(seed=seed,draws=100_000_000,chunk=1_000_000,nuisance_covariance_variant=variant)
                cells[name+'_V11_'+suffix]=x;seed+=1
    expected={'GWTC5_31_quality_mixture':{524,996,1588},'GWTC5_33_quality_mixture':{594,1144,1696}}
    found={name:set() for name in expected};seed=15261101
    for _,cell in old['nulls']['cells'].items():
        if cell['kind']=='route_IV' and cell['population'] in expected:
            x=copy.deepcopy(cell);x.update(seed=seed,draws=100_000_000,chunk=1_000_000,
                scope='Synthetic tail only; report empirical count/p and Clopper-Pearson upper; not physical jitter calibration')
            key='IV_'+cell['population']+'_N'+str(cell['N_target'])+'_1e8';cells[key]=x;seed+=1
            found[cell['population']].add(cell['N_target'])
    assert found==expected and len(cells)==30
    assert not set(cells)&set(old['nulls']['cells'])
    assert len({v['seed'] for v in cells.values()})==30 and not {v['seed'] for v in cells.values()}&{v['seed'] for v in old['nulls']['cells'].values()}
    reg['nulls_v1_1']=dict(cells=cells,phase='P_ONLY_AFTER_R7_AND_MACHINE_FREE_RECEIPT',draws_generated_so_far=0,
        covariance_variants='T5 diagnostics V=0, KDE bandwidth0.7, WLS q90; common t5 measurement scale plus independent Gaussian nuisance',
        gauss_scope='Original Gaussian scalar projection is exactly standard normal under its declared synthetic covariance; V1 cells are not rerun')
    measured=D/'statistics_001/RESULT.json';stats=load(measured);equivalents=[]
    for name,cell in old['nulls']['cells'].items():
        if cell['kind']!='matched_projection' or cell['model']=='gaussian':continue
        rp=B/'bis'/('RESULT_E2_NULL_'+name+'.json');v=load(rp);p=v['result']['analytic_tail_control']['p']
        equivalents.append(dict(population=cell['population'],reading=cell['reading'],nominal_z=5,
            synthetic_common_t5_p=p,equivalent_normal_z=float(norm.isf(p)),receipt_relative_to_Chatgpt=rp.relative_to(ROOT).as_posix(),sha256=sha(rp)))
    reg['statistics_v1_1']=dict(statute='INPUT_NULL_MODEL_AND_REAL_NONBLIND_DIAGNOSTICS_NOT_PHYSICAL_NULL_CALIBRATION',
        models=['Gaussian measurement plus Gaussian nuisance','Elliptical t5 measurement with one COMMON scale per catalog plus independent Gaussian nuisance'],
        gaussian_scope='Common covariance specified; independence of event scales is not interchangeable with the common-scale null',
        physical_p_rule='Use empirical p from the registered null including the SHARED component calibrated by E3.3; until paid, physical p=null',
        nominal_z5_common_t5_equivalents=equivalents,moments_and_event_bootstrap_relative_to_Chatgpt=measured.relative_to(ROOT).as_posix(),
        moments_and_event_bootstrap_sha256=sha(measured),bootstrap_unit='31 events; 2000 resamples; WLS posterior-mean diagnostic, not replacement of registered KDE V',
        bootstrap_scope='MEASURED_WLS_DIAGNOSTIC; KDE-fit bootstrap not measured by this receipt',
        scale_status='INPUT not selected by measured kurtosis',new_physical_p=None)
    tails=[]
    for n in (22,39,61):
        r=brentq(lambda x:n*(x-1-np.log(x))-25,1+1e-8,100)
        p=float(chi2.sf(n*r,n-1));tails.append(dict(N=n,critical_variance_ratio=float(r),p_exact_synthetic=p,normal_equivalent_z=float(norm.isf(p))))
    reg['route_IV_v1_1']=dict(homoscedastic_tail='P(chi2[N-1]>N*r), N*(r-1-log(r))=25; exact within this synthetic Gaussian likelihood model',
        homoscedastic_cases=tails,new_mixture_cell_ids=[name for name,v in cells.items() if v['kind']=='route_IV'],
        sigma_sys_and_recovered_jitter_paid=False,physical_p=None)
    reg['stratum_O4b_only_v1_1']=dict(n=14,bandwidth_factor=1.0,rows=stats['O4b_only_bandwidth1'],
        scope='Calibrational local KDE curvature only; intercept uncertainty is comparable to R-B effect, low planning power',
        source_relative_to_Chatgpt=measured.relative_to(ROOT).as_posix(),source_sha256=sha(measured))
    census={name for name,v in old['test_candidates'].items() if v['published_deformation_at_registration'] is None}
    eligibility={name for name,v in old['test_candidates'].items() if v['eligible'] is None}
    changes=[]
    for event in sorted(census|eligibility):
        entry=reg['test_candidates'][event];before=entry['eligible'];entry.update(eligible=None,metadata_only=True)
        changes.append(dict(event=event,eligible=None,promotion=None,metadata_only=True,census_reviewed_utc=None,
            pending_fields=[k for k,group in [('publication_census',census),('eligibility',eligibility)] if event in group],
            changed_fields={'eligible':{'before':before,'after':None}},evidence_relative_to_Chatgpt=source.relative_to(ROOT).as_posix(),evidence_sha256=sha(source)))
    reg['test_candidates_amendments']=changes
    reg['candidate_count_correction']=dict(missing_census=len(census),missing_eligibility=len(eligibility),intersection=len(census&eligibility),
        unique_metadata_events=len(census|eligibility),order_mentions=38,explanation='The eight missing-eligibility events are included in the thirty missing-census events; 38 counts repeated mentions, 30 distinct events. No extra event invented and no promotion.')
    reg['unpaid_before_execution']=['Final full-code mutation controls and immutable registration/witness/receipt',
        'R7 plus machine-free receipt before heavy jobs','Management audit, operator ratification and seed custody before blind events',
        'E3.3 physical systematics calibration before any physical p','Phase-P synthetic draws still unexecuted']
    reg['registration_provenance_v1_1']=dict(builder_relative_to_Chatgpt=Path(__file__).relative_to(ROOT).as_posix(),builder_sha256=sha(Path(__file__)),
        opening015_sha256=sha(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_015_ABERTURA_operador.md'),opening016_sha256=sha(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_016_ABERTURA_operador.md'),
        source_qualification_scope='Source-only R5, 1015 finite cases at4096/8192; finite coverage, not continuum proof')
    guard.verify_statistical_identity(old,reg)
    import pe_runner;pe_runner.validate_config(config)
    save(D/'CANDIDATE_V1_1_001.json',reg)
    summary=dict(status='DRAFT_CANDIDATE_COMPLETE_NOT_REGISTERED',sha256=sha(D/'CANDIDATE_V1_1_001.json'),
        statistical_subobject_sha256=guard.statistical_digest(reg),new_null_cells=len(cells),jobs=list(reg['pe_jobs']),
        metadata_count_correction=reg['candidate_count_correction'],source_R5_sha256=sha(r5),
        real_clock_exists=(B/'bis/PART_015_BUDGET_START.json').exists(),real_registration_exists=(B/'RINGDOWN_5SIGMA_V1_1.json').exists(),
        remaining_machine_hours_read=load(budget_source)['remaining_of_40_hours'])
    assert not summary['real_clock_exists'] and not summary['real_registration_exists']
    save(D/'CANDIDATE_001_RECEIPT.json',summary);print(json.dumps(summary))
if __name__=='__main__':main()
