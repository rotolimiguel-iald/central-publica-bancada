"""Contas derivadas do auditor (frente: caminho para o 5 sigma). Todo numero de entrada tem fonte declarada."""
import json, math
out={}
# --- D1/CAMB (um_absoluto.json core.d1_camb_v3_real_v366, sha16 456f0ab149bb13f6)
beta=0.012031300400803142
b_med=-0.013386585042688307; b_sig=0.008224826434777876   # beta_posterior (V3 real), c_free median
z_now=abs(b_med-beta)/b_sig
sig_5=abs(b_med-beta)/5
out['D1']=dict(beta_median=b_med,sigma_now=b_sig,z_vs_alpha_sqrt_e_now=z_now,
   sigma_needed_for_5sigma_if_median_holds=sig_5, shrink_factor_needed=b_sig/sig_5,
   note='5 sigma seria CONTRA alpha*sqrt(e) se a mediana -0.0134 se mantiver; DESI DR2 (BAO ~2x mais preciso que DR1, [KNOWN ordem de grandeza]) e o controle 2 (w0-wa) decidem; z_zero hoje 1.55 -> beta=0 (LCDM) NAO e excluido')
# --- neutrino m2 (core.neutrino_m2)
m2_pred=8.507414099900329; m2_obs=8.677557259966656; sig_obs=0.05761990212461259
out['NEUTRINO']=dict(z_now=(m2_obs-m2_pred)/sig_obs, sigma_m2_for_5sigma_meV=(m2_obs-m2_pred)/5,
   pct_on_m2=(m2_obs-m2_pred)/5/m2_obs*100, pct_on_Dm2_21=2*(m2_obs-m2_pred)/5/m2_obs*100,
   juno_projection_sigma=7.842905784155273, direction='CONTRA a TGL (m2_obs > m2_pred); escala 1 eV e [NORM] declarada; kill_rule exige 2 determinacoes autonomas >= 5 sigma')
# --- blind O4 candidates: information vs target (B3 table E[I]31; RINGDOWN_5SIGMA_V1 planning_targets I_tau_expected_target90)
EI31=[13.47072,12.72304,12.4296,10.19863,9.544175,9.415738,9.288122,9.035349,8.785864,8.417811,8.417811,8.057184,7.938628,7.244706]
I_target={'R-B':95215.9751441496,'R-MOD':30209.42485288899,'R-RAIZ-0':27907.2,'R-LIN':7513.27}
sEI=sum(EI31)
out['BLIND14_INFO']=dict(sum_expected_info=sEI,n_candidates=len(EI31),fraction_of_N90_target={k:sEI/v for k,v in I_target.items()},
   z_expected_if_all_14_converged={ 'R-B':0.0198453*math.sqrt(sEI),'R-MOD':0.0368397*math.sqrt(sEI),'R-RAIZ-0':0.037063*math.sqrt(sEI),'R-LIN':0.0714769*math.sqrt(sEI)},
   note='z = |delta| * sqrt(sum 1/sigma^2) com delta de referencia GW250114 por leitura (E0), sem nuisance; teto, nao poder')
# --- GW250114 sozinho (sigma dtau 0.058): z por leitura
for name,dl in (('R-B',0.0198453),('R-MOD',0.0368397),('R-RAIZ-0',0.037063),('R-LIN',0.0714769)):
    out.setdefault('GW250114_ALONE',{})[name]=dl/0.058
# --- SNR_RD para 5 sigma num so evento (lei sigma = 0.058*34/SNR): 
out['SINGLE_EVENT_SNR_RD_5SIGMA']={n:5*0.058*34/dl for n,dl in (('R-B',0.0198453),('R-MOD',0.0368397),('R-RAIZ-0',0.037063),('R-LIN',0.0714769))}
# --- piloto 220-only: custo (bancada E: 81-542 CPU-h; 22 workers)
out['PILOT_220_ONLY_COST']=dict(cpu_h_range=[81,542],wall_h_at_22_workers=[81/22,542/22],measured_fraction_native_abort_220only=0.0,measured_fraction_native_abort_440free=40/120,measured_fraction_EDOM_fmax1024_GR=10/120,
   source='prior_fraction_result.json (este auditor, N=120, semente 20260923)')
# --- void floor: one-sided 5 sigma already (v92/v41): r_c^cal REVOLVER 0.189 +- 0.017 -> L5
out['VOID_FLOOR']=dict(r_c_cal=0.189,sigma=0.0167,L5=0.189-5*0.0167,ratio_L5_over_beta=(0.189-5*0.0167)/beta,
   note='unilateral NOT_FALSIFIED_POWERED: o limite inferior a 5 sigma esta ~8x acima de beta; kill inalcancavel por tracadores (b>=1); resolucao em beta pede lente/kappa: kappa v9 r_5sigma_hi=0.3 vs beta 0.012 -> falta fator 25 em sigma_r')
# --- rota IV (largura de delta f): N90 validados (registro): 61 (0.019), 39 (0.0228), 22 (0.03) GW250114-like; taxa 0.69/ano O4 (IC90 0.035-3.27)
out['ROUTE_IV']=dict(N90=[61,39,22],rate_O4_per_year=0.69,rate_IC90=[0.035,3.27],years_O4_for_39=[39/3.27,39/0.69,39/0.035])
json.dump(out,open('cenarios_result.json','w'),indent=1)
print(json.dumps(out,indent=1))
