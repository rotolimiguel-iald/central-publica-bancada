"""Prepare a data-independent background control contract. No solver imports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,math
HERE=Path(__file__).resolve().parent

def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(name,x):
 p=HERE/name; t=p.with_name(p.name+'.new'); b=(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
 if p.exists():raise FileExistsError(p)
 with t.open('xb') as f:f.write(b)
 assert t.stat().st_size==len(b);t.rename(p)

p={
 'schema':'F9_BACKGROUND_PREPARATION_V1','request_id':'f132a1d5-7477-405d-963b-b1659db63328',
 'status':'PROPOSED_NOT_RATIFIED_NOT_RUN','created_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'PREDICTIONS_ONLY_NO_OBSERVED_CENTERS_NO_LIKELIHOOD_NO_EVIDENCE_NO_NETWORK',
 'prior':{'coordinates':['H0','ombh2','omch2'],'units':['km/s/Mpc','dimensionless','dimensionless'],'bounds':{'H0':[50,90],'ombh2':[.015,.03],'omch2':[.08,.18]},'measure':'independent_uniform_in_listed_coordinates','volume_exact':'3/50','density_exact':'50/3','boundary':'closed; endpoints have measure zero','on_solver_or_table_failure':'COMPUTATIONAL_FAILURE_STOP_NOT_ZERO_LIKELIHOOD','on_outside_prior':'DOMAIN_ERROR_NOT_SCIENTIFIC_VERDICT'},
 'background':{'omk':0.0,'w':-1.0,'wa':0.0,'dark_energy_model':'fluid','TCMB_K':2.7255,'mnu_eV':.06,'neutrino_hierarchy':'degenerate','num_massive_neutrinos':1,'nnu':3.046,'standard_neutrino_neff':3.044,'meffsterile':0.0,'YHe':'BBN_consistent','bbn_predictor':'PRIMAT_Yp_DH_ErrorMC_2024.dat','recombination_class':'Recfast','recfast_approx_model':'planck','tau':.054,'need_thermal_history':True,'compute_Cl':False,'compute_matter_power':False,'candidate_not_proven_identical_to_historical_table':True},
 'physical_notes':{'neutrinos':'CAMB thermal massive-neutrino background; not mnu/93.14 matter at all z plus full massless Neff radiation. nnu=3.046 is explicit; BBN reference is 3.044 in installed package.','recombination':'Explicit Planck-era RECFAST approximation; not exact recombination or full CMB likelihood. Primat 2024 table pinned; not asserted as original Planck compression BBN prescription.','helium_domain':'BBN axes verified .005..04 and DeltaN -3..7; proposed baryon prior and DeltaN=.002 lie inside.','remaining_defaults':'Every CAMBparams instance recorded in future output; remaining defaults bound by package hashes. No solver instantiated in preparation.'},
 'redshifts':{'low_z_controls':[0.0,.1,.5,1.0,2.0,3.0],'low_z_domain':[0.0,3.0],'z_star_law':1089.95,'law_redshift_status':'historical INPUT, held fixed; not substituted by derived recombination redshift','recombination_z':'derived zstar','drag_z':'derived zdrag','general_high_z_interpolator_qualified':False},
 'points':[
  {'id':'center','theta':[70,.0225,.13]},
  {'id':'corner_LLL','theta':[50,.015,.08]},
  {'id':'corner_LHH','theta':[50,.03,.18]},
  {'id':'corner_HLH','theta':[90,.015,.18]},
  {'id':'corner_HHL','theta':[90,.03,.08]}],
 'point_selection':'prior midpoint and tetrahedral four-corner design fixed without observational centers; 4 of 8 corners, not whole-domain qualification',
 'accuracy_profiles':{'baseline':{'AccuracyBoost':1.0,'distance_array_tol':1e-5},'reference':{'AccuracyBoost':2.0,'distance_array_tol':1e-7}},
 'precision':{'relative_prediction_tolerance':1e-5,'E0_absolute_tolerance':1e-9,'z0_DM_absolute_Mpc':1e-10,'z0_DV_absolute_Mpc':1e-10,'status':'engineering starting thresholds, not error bound on log evidence or scientific 5sigma threshold','pass_meaning':'only listed theory control points; common-mode recombination error and untested prior regions remain unqualified','strict_relative_fields':'H,DM(nonzero),DH,DV(nonzero),zstar,zdrag,rstar,rdrag,DMstar,E_law,E_at_zstar,Omega_m0,R,lA,I_law; denominator reference absolute value'},
 'resources':{'threads':1,'points':5,'profiles':2,'max_solver_calls':10,'timeout_seconds_per_worker':90,'total_timeout_seconds':960,'workers_parallel':1,'automatic_retries':0,'cost_and_peak_memory':'to be measured per worker; no estimates asserted as benchmarks'},
 'h5_candidate':{'type':'BAO_only_free_rd_not_EDE','rd_uniform_Mpc':[130,160],'density_per_Mpc':'1/30','theory_control_rd_Mpc':[130,145,160],'q_definition':'rd_free/rd_CAMB(theta)','q_conditional_support':'[130/rd_CAMB(theta),160/rd_CAMB(theta)]','q_conditional_density':'rd_CAMB(theta)/30','CMB':'standard rstar and DMstar unchanged','local_H0':'no TGL multiplicative response','status':'candidate not ratified'},
 'table_alternative':{'historical_raw_shape':[11,21,21],'historical_useful_prior_volume_percent':4.32,'spacing_candidate':[2.0,.00025,.002],'full_prior_nodes':[21,61,51],'padding_nodes_each_end':1,'padded_shape':[23,63,53],'padded_nodes':23*63*53,'five_field_payload_bytes':23*63*53*5*8,'time_formula':'padded_nodes * measured_seconds_per_node + independent held-out controls; no forecast before measured pilot','not_implemented_in_unit':True,'needed_extra_fields':'Historical five fields omit H(z), consistent E(z*) and low-z distances. Any table/derivative emulator must also specify these, common parameters and verified redshift interpolation.','coverage':'padding and no extrapolation; any miss is computational error. Continuous interpolation tested off-grid before integration.','accuracy_plan':'after a separately authorized generation: deterministic eight-corner plus face/edge midpoint and space-filling off-grid controls, baseline/reference comparison, adaptive refinement based only on prediction error; hash new table and pins. Not run here.'},
 'required_inputs':[pin(HERE/'TABLE_METADATA.json'),pin(HERE/'RUNTIME_METADATA.json'),pin(HERE/'BBN_METADATA.json')],
 'prohibitions':['observational target vectors','fit','chi2','likelihood','evidence','remote providers','network','D dataset','import um.py','import historical engine'],
 'next_authority':'ROOT reviews/ratisfies this limited protocol before any --run-controls; preparation is not authorization for full F9 or a new grid.'}
save('PROTOCOL.json',p)
sources=[HERE.parent/'reproducao_fase45_conjunta'/n for n in ['T4_PROTOCOLO.json','T4_reproduzir.py','T4_camb_lcdm_v1.npz']]
sources.append(HERE.parent/'h5_contract/NOTA_H5_ESCALAS_ACUSTICAS.md')
save('SOURCES.json',{'files':[pin(x) for x in sources],'historical_table_generator':'not inspected: original C:/IALD/Bancada_Um read denied; copied table has no configuration metadata; no claim about its CAMB settings','metadata_only_runtime':pin(HERE/'RUNTIME_METADATA.json')})
print('Protocol ready; no numerical cosmology executed.')