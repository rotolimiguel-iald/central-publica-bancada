# -*- coding: utf-8 -*-
"""Consolida os numeros da frente D lidos dos resultados d1/d2/d3 (nunca de memoria)."""
import json, hashlib, os
def sha16(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
d1=json.load(open('d1_resultado.json')); d2=json.load(open('d2_resultado.json')); d3=json.load(open('d3_resultado.json'))
A={(c['reading'],c['unraveling']):c for c in d1['parts']['A_unraveling_dependence_ref_68p1_0p68_128samples']}
out=dict(frente='D', inputs_sha16={f:sha16(f) for f in ('d1_resultado.json','d2_resultado.json','d3_resultado.json')},
 beta_runtime=d1['beta_runtime'],
 realizacao_unica_referencia_68p1_0p68=dict(
   ensemble_dtau=A[('R-B','brownian')]['ensemble_dtau'],
   RB_brownian=dict(sd_df=A[('R-B','brownian')]['sd_df'], mean_dtau=A[('R-B','brownian')]['mean_dtau'], se=A[('R-B','brownian')]['se_mean_dtau'], sd_dtau=A[('R-B','brownian')]['sd_dtau'], frac_of_ensemble=A[('R-B','brownian')]['mean_dtau']/A[('R-B','brownian')]['ensemble_dtau']),
   RB_cauchy=dict(sd_df=A[('R-B','cauchy')]['sd_df'], mad_df=A[('R-B','cauchy')]['mad_df'], mean_dtau=A[('R-B','cauchy')]['mean_dtau']),
   RB_kick_pi_half=dict(sd_df=A[('R-B','kick_0.5')]['sd_df'], mad_df=A[('R-B','kick_0.5')]['mad_df'], mean_dtau=A[('R-B','kick_0.5')]['mean_dtau'], P_no_kick_window=0.857),
   RB_telegraph=dict(sd_df=A[('R-B','kick_1.0')]['sd_df'], mad_df=A[('R-B','kick_1.0')]['mad_df'], P_no_kick_window=0.926),
   RB_deterministic=dict(sd_df=0.0, dtau=A[('R-B','ensemble_deterministic')]['mean_dtau']),
   RRAIZ0_brownian=dict(sd_df=A[('R-RAIZ-0','brownian')]['sd_df'], mean_dtau=A[('R-RAIZ-0','brownian')]['mean_dtau'], ens=A[('R-RAIZ-0','brownian')]['ensemble_dtau']),
   RMOD_brownian=dict(sd_df=A[('R-MOD','brownian')]['sd_df'], mean_dtau=A[('R-MOD','brownian')]['mean_dtau'], ens=A[('R-MOD','brownian')]['ensemble_dtau']),
   RLIN_brownian=dict(sd_df=A[('R-LIN','brownian')]['sd_df'], mean_dtau=A[('R-LIN','brownian')]['mean_dtau'], ens=A[('R-LIN','brownian')]['ensemble_dtau']),
   RLIN_cauchy=dict(sd_df=A[('R-LIN','cauchy')]['sd_df'], mad_df=A[('R-LIN','cauchy')]['mad_df'], mean_dtau=A[('R-LIN','cauchy')]['mean_dtau']),
   C2_bancada_lido=d1['C2_lido']['R-B'], C2_RG_ruido_lido=d1['C2_lido']['R-GLOBAL'],
   C2_coherent_sd_df_N4_64_256=[d1['C2_lido']['R-RAIZ-COHERENT_N%d'%n]['NONE']['sd_df'] for n in (4,64,256)]),
 escala=dict(spin_window=[dict(spin=c['spin'],win=round(c['window_tau'],1),x=c['x'],Q=c['Q'],sd_df=c['sd_df'],env=c['gerencia_envelope_sd_df'],mean_dtau=c['mean_dtau'],ens=c['ensemble_dtau']) for c in d1['parts']['B_scaling_spin_window_mass'] if c['mass']==68.1],
            mass=[dict(mass=c['mass'],sd_df=c['sd_df'],mean_dtau=c['mean_dtau']) for c in d1['parts']['B_scaling_spin_window_mass'] if abs(c['window_tau']-6)<0.05 and c['spin']==.68]),
 snr=[dict(snr=c['snr'],GR_sd_df=c['GR']['sd_df'],GR_mean_df=c['GR']['mean_df'],GR_mean_dtau=c['GR']['mean_dtau'],RB_sd_df=c['RB']['sd_df'],RB_mean_dtau=c['RB']['mean_dtau'],excess_quad=c['sd_df_excess_quadrature']) for c in d1['parts']['C_snr_white_noise']],
 poder=dict(limiar=d2['threshold'], sigma_ref=d2['sigma_meas_reference'], casos=d2['cases'], z_esperado_catalogo31=d2['expected_z_with_current_31_sigmas'], peso_catalogo_em_GW250114=d2['catalog_31_weight_in_GW250114_units'], canal=d2['channel_comparison_GW250114']),
 exploratorio_nao_cego={a['label']:dict(N=a['N'],var_med=a['observed_variance_of_medians'],mean_s2=a['mean_sigma_i2'],ratio=a['ratio_obsvar_over_mean_sigma2'],chi2=a['chi2_homogeneity'],dof=a['dof'],p_chi2=a['p_chi2'],score_z=a['score_z'],sjit_mle=a['sigma_jit_MLE'],sjit_90=a['sigma_jit_profile_90'],mu=a['mu_at_MLE']) for a in d3['analyses']},
 nulo_calibracao_31=d3['null_calibration_31'])
json.dump(out,open('D_consolidado.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
print(json.dumps(out['escala'],indent=0)[:1500]); print('mu 31:',out['exploratorio_nao_cego']['GWTC5_31_df220']['mu'])
print('sha16 D_consolidado.json',sha16('D_consolidado.json'),'d4',sha16('d4_consolida.py'))
