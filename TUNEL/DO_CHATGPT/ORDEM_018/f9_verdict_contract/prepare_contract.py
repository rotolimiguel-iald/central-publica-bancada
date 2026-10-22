"""Documentary verdict contract. No statistics evaluated on data or simulations."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
ID='18dced03-6d38-4a2e-a2c8-a44ab39ed171'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,obj):
 p=HERE/name;b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();t=p.with_name(p.name+'.new')
 if p.exists():raise FileExistsError(p)
 with t.open('xb') as f:f.write(b)
 assert t.stat().st_size==len(b);t.rename(p)
request=json.loads((ROOT/'F9_VERDICT_MANAGER_REQUEST.json').read_text());assert request['request_id']==ID
expected=request['source_candidate']['sha256'];src=ROOT/'FASE9_V1_CANDIDATE.json'
if sha(src.read_bytes())!=expected:
 candidates=[x for x in ROOT.glob('FASE9_V1_CANDIDATE.json.bak_*') if sha(x.read_bytes())==expected]
 if not candidates:raise RuntimeError('Requested candidate snapshot missing; no repin')
 src=sorted(candidates)[-1]
paths=[('F9_CANDIDATE_PINNED.json',src),
 ('F9_MANAGER_REQUEST.json',ROOT/'F9_VERDICT_MANAGER_REQUEST.json'),
 ('F9_ASSEMBLY.md',ROOT/'F9_LIKELIHOOD_ASSEMBLY_CANDIDATE.md'),
 ('LINEAR_DESIGN.md',ROOT/'h0dn_documentary_review/linear_design/PROJETO_LINEAR_E_MEDIDA.md'),
 ('LINEAR_SPEC.json',ROOT/'h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json'),
 ('NUISANCE_MEASURE.json',ROOT/'h0dn_documentary_review/linear_design/MEDIDA_NUISANCE_CANDIDATA.json'),
 ('FLAT_CONTROL_PROTOCOL.json',ROOT/'covariance_support/LINEAR_GAUSSIAN_PROTOCOL.json'),
 ('STELLAR_PROTOCOL.json',ROOT/'covariance_support/STELLAR_FAMILY_PROTOCOL.json'),
 ('PREFLIGHT_262_RESULT.json',ROOT/'derivacoes/preflight_262/PREFLIGHT_262_RESULT.json'),
 ('PREFLIGHT_262_NOTE.md',ROOT/'derivacoes/preflight_262/NOTA_PREFLIGHT_262.md'),
 ('PREFLIGHT_262_PROTOCOL.json',ROOT/'derivacoes/preflight_262/PROTOCOLO_PREFLIGHT_262.json'),
 ('USE_NOVELTY.md',ROOT/'proveniencia/NOTA_PROVENIENCIA_F1.md'),
 ('H5_NOTE.md',ROOT/'h5_contract/NOTA_H5_ESCALAS_ACUSTICAS.md'),
 ('BACKGROUND_PROTOCOL.json',ROOT/'f9_background_prediction/PROTOCOL.json')]
(HERE/'sources').mkdir(exist_ok=False);pins=[]
for name,p in paths:
 b=p.read_bytes();out=HERE/'sources'/name
 with out.open('xb') as f:f.write(b)
 assert out.read_bytes()==b
 pins.append({'source_path':str(p),'snapshot':'sources/'+name,'bytes':len(b),'sha256':sha(b),'role':'custodied_document_or_error_metadata_no_observed_vector'})
save('SOURCES.json',{'files':pins,'requested_candidate_sha256':expected,'candidate_matches_request':True,'primary_sources_not_reopened':'Provenance audit reused with its scope; no originals/network/upstream imports'})
pre=json.loads((HERE/'sources/PREFLIGHT_262_RESULT.json').read_text())
models={
 'H1_TGL':{'beta':'ALPHA_FINE_CODATA_2018*sqrt(e) runtime','h':'log10(H0)+I(theta)*beta_TGL/ln(10)','delta_C':'0','bao':'rd_CAMB(theta)','physical_dimension':3},
 'H2_LCDM':{'beta':'0','h':'log10(H0)','delta_C':'0','bao':'rd_CAMB(theta)','physical_dimension':3},
 'H3_beta_free':{'beta':'b in [-.05,.05]','h':'log10(H0)+I(theta)*b/ln(10)','delta_C':'0','bao':'rd_CAMB(theta)','physical_dimension':4,'contains':['H1_TGL','H2_LCDM'],'role':'diagnostic not redefinition of TGL'},
 'H4_Cepheid':{'h':'log10(H0)','delta_C':'-5log10(1+s), s in [-.15,.15]','bao':'rd_CAMB(theta)','physical_dimension':4,'response':'c_C delta_C in elementary network; not uniform total-H0 shift'},
 'H5_rd_free':{'h':'log10(H0)','delta_C':'0','bao':'r in [130,160] Mpc','cmb':'standard rstar(theta), NOT r','physical_dimension':4,'role':'phenomenological BAO ruler, not EDE'}}
claims=[
 {'id':'COMPAT_H1','statistic':'G_1,s=inf_(xi1,eta) residual^T C_s^+ residual','null':'H1_TGL','tail':'upper','question':'absolute fit of complete route/model/data contract'},
 {'id':'LAW_H1_VS_FREE','statistic':'Q_1,s=2*(ellhat_3,s-ellhat_1,s)','null':'H1_TGL','tail':'upper','question':'fixed beta law against its free-beta extension; nonnegative only if nested fits qualified'},
 {'id':'H2_TO_H1','statistic':'T_21,s=2*(ellhat_1,s-ellhat_2,s)','null':'H2_LCDM','tail':'upper','direction_condition':'T_21,s>0 for all admitted s'},
 {'id':'H4_TO_H1','statistic':'T_41,s=2*(ellhat_1,s-ellhat_4,s)','null':'H4_Cepheid','tail':'upper','direction_condition':'T_41,s>0 for all admitted s'},
 {'id':'H5_TO_H1','statistic':'T_51,s=2*(ellhat_1,s-ellhat_5,s)','null':'H5_rd_free','tail':'upper','direction_condition':'T_51,s>0 for all admitted s'}]
contract={
 'id':ID,'version':1,'status':'CANDIDATE_FOR_REVIEW_NOT_RATIFIED_NOT_EXECUTED','scope':'F9 R-A Planck-compressed + DESI_DR2 + local V01 network; same observations once',
 'source_candidate_sha256':expected,'opening_authorized':False,'observed_values_read':False,'science_executed':False,
 'models':models,'definitions':{'theta':'(H0,ombh2,omch2)','I':'(2/3)ln E_standard(1089.95;theta)','eta':'same R^63 physical modulus/magnitude coordinates','ellhat':'sup of full normalized sampling log likelihood over each model physical domain and shared eta; not log of flat-marginal integral','G_domain':'Gaussian common fixed C_s and common affine support, ranks/units qualified; extension to parameter-dependent estimated errors requires separate generative contract'},
 'physical_priors':{'theta':'independent normalized uniforms H0[50,90],wb[.015,.03],wc[.08,.18]; density50/3 in these coordinates','beta_free':'Uniform[-.05,.05], density10','H4_s':'Uniform[-.15,.15], density10/3; pi_delta=ln(10)/1.5*10^(-delta/5) on transformed interval','H5_rd':'Uniform[130,160] Mpc, density1/30; pi_q_given_theta=rd_CAMB(theta)/30, variable endpoints','flat_eta':'kappa d eta common to all models; relative ratios only, not absolute evidence or a sampling prior'},
 'systematics':{'stellar_labels':300,'SBF_labels':['UPSTREAM_M_ONLY','INDEPENDENT_M_ADDITION_CONDITIONAL'],'candidate_cartesian_labels':600,'interpretation':'restricted finite conditional sensitivity family, not measured distribution of truth','dedup_rule':'full covariance + response + likelihood normalization hashes, preserving original label map; no presumed count of full distinct matrices','boundary_singular_cases':'excluded from this interior family and separate contract','policy':'every case, no data-selected best case; p_robust=max_s p_s, Bayes intervals=min/max_s log-ratios','incomplete_family':'explicit SYSTEMATICS_COVERAGE_LIMITED always; cannot certify all physical systematics','no_automatic_prior_over_s':True},
 'primary_family':{'routes':['F9_R-A_joint'], 'claims':claims,'m':5,'scope':'within this fixed preregistered family; not experiment-wide all historical searches','secondary_routes':'Planck-only, other maps/data reuse remain descriptive until included in a separately frozen larger family; no independent combination'},
 'calibration':{'p_per_s':'sup_(xi in null domain, eta if invariance not proved) Pr_null,xi,s[T_j(Y*) >= T_j(Yobs)]','continuous_nuisance':'finite grid maximum is not certified supremum; validated bounding or stated conditional qualification required','eta_reduction':'only after proving invariance to Y_local -> Y_local+Xv of the full estimator/statistic/support procedure; then simulate eta=0 representative, not improper flat prior sampling','systematic_null_union':'p_robust_j=max_s p_j,s; valid for union of the explicitly admitted scenarios if every p_j,s is valid for its null','multiplicity':'p_FWER_j=min(1,5*p_robust_j); Bonferroni, arbitrary dependence; same5used for all claims','sigma_convention':'Z_eq=Phi^-1(1-p_FWER) upper-tail Gaussian equivalent only, no measured Gaussian residual assumption','alpha5_definition':'0.5*erfc(5/sqrt(2))','two_sided_warning':'not the two-sided |z| tail; do not call sqrtDeltaChi2 a calibrated sigma','no_Wilks_assumption':True,'no_Bayes_to_sigma':True,'no_product_of_correlated_p':True,
 'monte_carlo':'at fixed simple null, exchangeable independent full-pipeline replicates: (1+exceedances)/(N+1); no zero p; finite runs do not qualify composite nuisance supremum','tail_budget':'standard Monte Carlo may need at least ceil(5/alpha5)-1 draws merely to resolve the Bonferroni5sigma threshold at zero exceedances; no such run authorized here. Rare-event alternatives require independently verified bounds/weights.','numerical_and_MC_error':'use conservative upper bounds; if confidence bounds used as guarantees, allocate total certification failure probability within overall alpha budget, not an arbitrary 1% beside5sigma','unqualified_tail_output':'CALIBRATION_UNAVAILABLE plus raw statistics if valid; no numeric sigma claim'},
 'bayesian_relative':{'measure':'flat eta integrated with existing qualified formula; proper physical/model-specific priors','J_i_s':'integral L_bg_i * L_local_flat_i * pi_i over physical parameters','output':'all five log J_i up to same arbitrary constant; ten pairwise ln B_ij=ln J_i-ln J_j per scenario, numerical uncertainty, ranges','requirements':'finite nonzero integrals, common support/eta/units/Jacobians, full prior coverage; no table-missing=zero','weights':'no summing/multiplying/minimizing scenarios or routes; mixture would need prior weights fixed first','legacy_thresholds':'optional separate reporting flags min_s lnB12>=5 and min_s lnB13>=-1; not sigma or substitute for compatibility; H1 lies within H3 so cannot reject whole H3 in favor of contained H1','absolute_evidence':False},
 'verdict':{'shape':'separate fields, never single early-return underpowered gate','fields':['availability','integrity','support','calibration','systematics_coverage','per_scenario_residuals','compatibility','comparisons','relative_evidence','use_novelty','information_power'],
 'priority_rules':[
 'If unopened/missing input/ratification: AWAITING_DATA_OR_RATIFICATION, all observed fields null, keep contract/preflight.',
 'If invalid common support/integrity/numerics: explicit failure with safe raw diagnostics; do not label physical rejection from a failed instrument.',
 'If calibration unavailable: retain valid raw G/Q/T and lnB separately; no5sigma claim.',
 'Evaluate calibrated residual/rejection and every scenario BEFORE considering power.',
 'If robust adjusted COMPAT_H1 or LAW_H1_VS_FREE p<=alpha5: ROUTE_H1_REJECTED_AT_5SIGMA_CONDITIONAL_CONTRACT; keep each scenario and systematic limits, regardless low expected power.',
 'If only some scenarios reject/prefer: SYSTEMATICS_SENSITIVE_RESULT, report all, no robust claim.',
 'If T_j1 positive across family and p_FWER<=alpha5 with H1 not rejected: H1_DISCRIMINATES_FROM_Hj_AT_CALIBRATED_LEVEL_CONDITIONAL_CONTRACT for eachj=2,4,5 separately; not proof of H1 or rejection of H3.',
 'If no rejection: NOT_FALSIFIED_IN_THIS_CONTRACT; power state is additional NOT_EVALUATED/CONDITIONAL_LOW_POWER/CONDITIONAL_ADEQUATE_POWER, never a shortcut.',
 'If systematic family incomplete: SYSTEMATICS_COVERAGE_LIMITED stays visible even when conditional significance extreme.'
 ],'no_CONFIRMED':True,'no_gate_change':True},
 'information_without_centres':{'allowed':'reuse preflight262 error-only I and sigma metadata; no new matrix assembly','full_network':267,'preflight_subset':262,'excluded_MM':5,'rank_C_subset':190,'nullity_subset':72,'rank_eta':63,
 'preflight_sigma_h_joint_dex':[x['ideal_joint_sigma_h_dex'] for x in pre['variants']],
 'preflight_sigma_delta_C_joint_mag':[x['ideal_joint_sigma_delta_C_mag'] for x in pre['variants']],
 'interpretation':'local h and Cepheid jointly free, conditional on two baseline SBF variants; not a posterior, full family/global power or beta error','simple_gaussian_design':'D^2=Delta_mu^T P Delta_mu for fully specified simple alternatives after nuisance; power=1-Phi(Phi^-1(1-alpha)-D) only under its simple Gaussian assumptions; D=5 at an uncorrected5sigma test gives50% power, not guaranteed detection','not_measured':['centres','Delta_mu for F9 full experiment','global_power','observed_beta','observed_h','relative_evidence']},
 'use_novelty':{'rule':'retrodição sem ajuste é evidência; no temporal novelty veto','evidence':'reuse pinned provenance audit; fixed alpha*sqrt(e), law and caller dependence, declared choices/source hashes; no new broad archive scan','limits':'do not inherit inverse-fit beta or optimally selected variant; preserve historical contrary branches and audit limitations; selection/multiplicity separate from coefficient provenance','test_preregistration':'freeze this contract, data IDs, variants, priors, functions, numerical/calibration methods and selection ledger before compound, not pretend prior ignorance of individual data'},
 'alternatives':[
 {'id':'A','name':'Calibrated frequentist family plus separate relative Bayes reporting','recommended':True,'why':'can support explicitly bounded significance for5sigma objective without lnB/Wilks shortcuts','limitation':'tail and composite-null calibration not done; documentary contract not an order to run large simulations'},
 {'id':'B','name':'Bayesian relative comparison and proper conditional predictive checking','recommended':False,'why':'permits coherent evidence/preference reporting without global-sigma assertion','condition':'proper predictive generative measure or justified nuisance-invariant quotient; common improper eta measure alone cannot generate prior-predictive samples','limitation':'posterior predictive tail is not uniform frequentist p; no5sigma reinterpretation'}],
 'operator_decisions':['choose A for calibrated significance or B with no sigma claim','ratify five model maps, shared data/background and physical domains','ratify finite systematic family and exact scope of robust claims','ratify primary5 tests, alpha convention and selection ledger','ratify common nuisance measure and prior transport','ratify numerical/tail certification thresholds and resources in later unit before observed opening'],
 'outputs_now':{'fit':None,'y':None,'S':None,'g':None,'H0':None,'lnB':None,'sigma':None,'global_power':None}}
save('UNIDADE.json',{'request_id':ID,'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'DOCUMENTARY_VERDICT_CONTRACT_ONLY','science_runs':0,'providers':0,'network':False})
save('F9_VERDICT_CONTRACT_CANDIDATE.json',contract)
print(json.dumps({'sources':len(pins),'candidate_sha256':expected,'status':contract['status']}))