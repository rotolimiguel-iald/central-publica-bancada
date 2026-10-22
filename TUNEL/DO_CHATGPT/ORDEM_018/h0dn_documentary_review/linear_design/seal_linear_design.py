from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from decimal import Decimal
import json,importlib.util
ROOT=Path(__file__).resolve().parent
P=ROOT.parent;J=P/'jagb_extension';ORD=P.parent

def digest(p):return sha256(p.read_bytes()).hexdigest()
def put_bytes(p,b):
    p.parent.mkdir(exist_ok=True,parents=True)
    if p.exists():
        assert p.read_bytes()==b,'Artifact changed: '+str(p);return
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.stat().st_size==len(b);t.replace(p)
def put(n,d):put_bytes(ROOT/n,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())

def main():
    spec=json.loads((ROOT/'ESPECIFICACAO_LINEAR.json').read_text(encoding='utf-8'))
    pins=json.loads((ROOT/'INPUTS_PINADOS.json').read_text(encoding='utf-8'))
    expected=next(i['sha256'] for i in pins['inputs'] if i['path'].endswith('F9_ASSEMBLY_MANIFEST.json'))
    historical=next(p for p in ORD.glob('F9_ASSEMBLY_MANIFEST.json.bak*') if digest(p)==expected)
    snap=ROOT/'source_snapshots'
    put_bytes(snap/'F9_MANIFESTO_INICIAL.json',historical.read_bytes())
    current=ORD/'F9_ASSEMBLY_MANIFEST.json';fm=json.loads(current.read_text(encoding='utf-8'))
    source=next(i for i in fm['sources'] if i.get('logical_source_path','').endswith('FASE9_V1_CANDIDATE.json'))
    assert digest(Path(source['path']))==source['sha256']
    prior=next(i for i in pins['f9_dependency_checks'] if not i['matches'])
    assert prior['expected_sha256']==source['sha256']
    assert digest(Path(fm['note']['path']))==fm['note']['sha256']
    for item in fm['sources']: assert digest(Path(item['path']))==item['sha256'],item['path']
    put_bytes(snap/'F9_MANIFESTO_RESOLVIDO.json',current.read_bytes())
    put_bytes(snap/'F9_NOTA_CONFERIDA.md',Path(fm['note']['path']).read_bytes())
    resolution={'status':'RESOLVED_BY_OWNER_WITH_ORIGINAL_CONTENT_SNAPSHOT','initial_manifest_recovered_from':str(historical),
      'initial_manifest_sha256':expected,'resolved_manifest_sha256':digest(current),
      'resolved_source_snapshot':source,'old_V1_hash_preserved':True,'new_V1_contents_not_consumed':True,
      'note_hash_unchanged':fm['note']['sha256'],'no_scientific_analysis_repeated':True}
    put('RESOLUCAO_CUSTODIA_F9.json',resolution)
    e=json.loads((J/'residual_systematics/ERROR_COMPONENTS.json').read_text(encoding='utf-8'))
    active={v['MAS'] for v in spec['mas_hms_graph']}
    assert all(Decimal(r['sigma_mag'])>0 for r in e['mas_reference_errors'] if r['mas_key'] in active)
    assert all(Decimal(r['sigma_mag'])>0 for r in e['primitive_hms_groups'])
    previous=json.loads((J/'CEPHEID_RESPONSE_CANDIDATE.json').read_text(encoding='utf-8'))
    c={r['row_id']:r['c_C'] for r in spec['rows']}
    assert all(c[r['row_id']]==str(r['c_C']) for r in previous['rows'])
    counts=spec['counts']
    measure={'status':'CANDIDATE_NO_PRIOR_CHOSEN_NO_LIKELIHOOD_EVALUATED','unit_id':spec['unit_id'],
      'common_eta_dimension':counts['eta_dimension'],'eta_columns':spec['eta_columns'],
      'common_to':['TGL_fixed_R-A','LCDM','beta_free_diagnostic','differential_Cepheid','H5_A_conditional'],
      'physical_h_mapping_source':'source_snapshots/F9_NOTA_CONFERIDA.md',
      'a_h_and_c_C':'ESPECIFICACAO_LINEAR.json',
      'proper_prior_options':[
        {'family':'Gaussian','normalized':True,'mean':None,'covariance':None,'formula':'N(y; X m_eta+a_h h+c_C delta_C, C+X V_eta X.T)','scope':'independent prior on physical eta, not repetition of anchor/MAS/HMS measurement errors'},
        {'family':'Uniform_finite_domain','normalized':True,'domain':None,'formula':'L_flat * Pr[N(eta_hat,F^-1) in Omega] / Vol(Omega)','scope':'X inside C support, full column rank, common data measure'}],
      'flat_measure_ratio':{'absolute_evidence':False,'common_arbitrary_multiplier':'kappa','dimension':counts['eta_dimension'],'domain':'R^63',
        'formula':'(2pi)^(-(r-63)/2) / sqrt(pdet(C)*det(F)) * exp(-b.T P b/2)',
        'definitions':{'F':'X.T C+ X','P':'C+ - C+ X F^-1 X.T C+','b':'y - a_h h - c_C delta_C'},
        'required':['common physical eta and measure','finite nonzero marginal integrals','full X column rank inside C support','common affine data support','compatible deterministic constraints','proper priors for model-specific parameters','Jacobians retained'],
        'computable_prefactors_cancel_only_when':'same X,C,r independent of all integrated parameters; otherwise keep inside each integral',
        'kappa_cancellation':'single constant common to all models; different eta dimensions or unidentified flat directions invalidate automatic cancellation'},
      'support':{'known_stellar_constraints':counts['host_cycle_constraints'],'cycles_annihilate_X_a_h_c_C':True,'observed_constraints_checked':False,'nonhost_support_verified':False},
      'compression':{'SN_and_SBF_intercepts_are_data_not_extra_eta':True,'q0_j0_fixed_in_pinned_V01_config':True,'parameter_dependent_reduction_requires_complete_likelihood_normalization':True},
      'adopted_choice':None,'proper_prior_hyperparameters_selected':False,'data_centres_used':False,'new_verdict':None}
    put('MEDIDA_NUISANCE_CANDIDATA.json',measure)
    validation={'status':'STRUCTURAL_DOCUMENTARY_VALIDATION_ONLY','counts':counts,
      'all_active_MAS_HMS_errors_positive':True,'c_C_matches_previous_candidate':True,
      'exact_cycle_checks':'all72 annihilate HMS/MAS/anchor and X,a_h,c_C; performed by identifier script',
      'X_column_rank_proof':63,'X_and_h_column_rank_proof':64,'X_h_c_C_column_rank_proof':65,
      'numeric_C_rank_not_computed':True,'new_centre_conversion':False,'upstream_executed':False,'D_opened':False,'remote_models':0,'fit_or_S_g_H0_lnB':False,
      'F9_drift_resolved_by_original_snapshot':True,'original_failed_check_preserved':'VALIDACAO_INICIAL.json',
      'sources_checked_now':[{'path':str(p),'sha256':digest(p)} for p in [J/'residual_systematics/ERROR_COMPONENTS.json',J/'CEPHEID_RESPONSE_CANDIDATE.json']]}
    put('VALIDACAO_ESTRUTURAL.json',validation)
    helper=Path(r'C:\IALD\Central de Patentes\Chatgpt\TGL_BANCADA_OFICIAL\record_universe_delivery.py')
    sp=importlib.util.spec_from_file_location('memory_append',helper);mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
    text='''## Adendo de custódia — snapshot resolvido pela coordenação

[REAL] O proprietário identificou a evolução posterior do candidato V1 e apontou o manifesto F9 para o backup imediato que conserva exatamente o hash da versão usada na revisão. Esta unidade verificou o hash desse snapshot e o da nota: a dependência histórica está resolvida, sem repinar o conteúdo novo e sem repetir o estudo. O manifesto inicial foi recuperado por hash e ambos os manifestos foram copiados em `source_snapshots/`; `RESOLUCAO_CUSTODIA_F9.json` mantém os caminhos e hashes. A falha inicial permanece registrada como história, não como bloqueio atual. Esta resolução não ratifica o V1 evoluído.
'''
    mod.append(ROOT/'PROJETO_LINEAR_E_MEDIDA.md',text,'F9_SNAPSHOT_RESOLVED_EC4872EC')
    files=['UNIDADE.json','derive_identifier_design.py','seal_linear_design.py','ESPECIFICACAO_LINEAR.json','INPUTS_PINADOS.json','VALIDACAO_INICIAL.json','PROJETO_LINEAR_E_MEDIDA.md','RESOLUCAO_CUSTODIA_F9.json','MEDIDA_NUISANCE_CANDIDATA.json','VALIDACAO_ESTRUTURAL.json']
    files += ['source_snapshots/F9_MANIFESTO_INICIAL.json','source_snapshots/F9_MANIFESTO_RESOLVIDO.json','source_snapshots/F9_NOTA_CONFERIDA.md']
    put('MANIFESTO_ENTREGA.json',{'unit_id':spec['unit_id'],'scope':'INDEPENDENT_DOCUMENTARY_LINEAR_DESIGN_AND_COMMON_MEASURE_NO_FIT',
      'files':[{'path':str(ROOT/n),'bytes':(ROOT/n).stat().st_size,'sha256':digest(ROOT/n)} for n in files],
      'mutable_metadata_excluded':['MEMORIA_DA_UNIDADE.md','route_registration'],'inheritance':'INPUTS_PINADOS plus RESOLUCAO_CUSTODIA_F9; historical mutable reference resolved via verified snapshot'})
    print(json.dumps({'counts':counts,'manifest_files':len(files),'report_sha256':digest(ROOT/'PROJETO_LINEAR_E_MEDIDA.md'),'resolved_F9_source_sha256':source['sha256']},indent=2))
if __name__=='__main__':main()