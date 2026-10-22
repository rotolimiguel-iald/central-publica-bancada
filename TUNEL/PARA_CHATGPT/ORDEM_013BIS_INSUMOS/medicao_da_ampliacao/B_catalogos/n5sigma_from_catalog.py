"""N eventos para 5 sigma a partir das larguras reais por evento (GWTC-5.0 pSEOB, 33 eventos)
e das predicoes por leitura da bancada (C4_CATALOG_220.json). Somente leitura da pasta da bancada.
beta em runtime: ALPHA_FINE_CODATA_2018*sqrt(e)."""
import json,hashlib,math,numpy as np
ALPHA=7.2973525693e-3; BETA=ALPHA*math.sqrt(math.e)
P=r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_220.json"
b=open(P,'rb').read(); sha16=hashlib.sha256(b).hexdigest()[:16]
d=json.loads(b); rows=d['rows']
sel31=set(json.load(open(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_COMBINATION.json",encoding='utf-8'))['selected_events'])
out={'source':P,'sha16':sha16,'beta_runtime':BETA,'N_rows':len(rows),'per_event':[],'readings':{}}
readings=['R-B','R-RAIZ-0','R-MOD','R-LIN']
z90=1.6448536  # metade da largura de 90% = 1.645 sigma (gaussiana)
for r in rows:
    q=r['quantiles']['dtau220']; sig=(q[2]-q[0])/(2*z90)
    e={'event':r['event'],'in31':r['event'] in sel31,'dtau_med':q[1],'sigma_dtau_gauss':sig,'snr_like':None,'spin_med':r['quantiles']['spin'][1],'Mdet_med':r['quantiles']['mass_detector'][1]}
    for rr in r['rows']:
        if rr['reading'] in readings:
            mp=rr.get('median_prediction',{})
            e[rr['reading']]={'delta_tau_pred':mp.get('delta_tau_ensemble_exact'),'z_pred':(mp.get('delta_tau_ensemble_exact') or 0)/sig}
    out['per_event'].append(e)
ev31=[e for e in out['per_event'] if e['in31']]
sig=np.array([e['sigma_dtau_gauss'] for e in ev31])
out['sigma_dtau_stats_31']={'min':float(sig.min()),'median':float(np.median(sig)),'mean':float(sig.mean()),'max':float(sig.max()),'sigma_combined_inverse_variance':float(1/np.sqrt((1/sig**2).sum()))}
for rd in readings:
    dl=np.array([e[rd]['delta_tau_pred'] for e in ev31]); z2=(dl/sig)**2
    fisher_z=float(np.sqrt(z2.sum()))
    out['readings'][rd]={'delta_tau_pred_median_over_events':float(np.median(dl)),'delta_tau_pred_min':float(dl.min()),'delta_tau_pred_max':float(dl.max()),
        'z_combined_31_events_fixed_prediction':fisher_z,'mean_z2_per_event':float(z2.mean()),
        'N_events_O4like_for_5sigma':float(25/z2.mean()) if z2.mean()>0 else None,
        'N_events_O4like_for_5sigma_using_best5_only':float(25/np.sort(z2)[-5:].mean()) if z2.mean()>0 else None,
        'N_events_for_5sigma_at_common_sigma_0.036':float(25/((np.median(dl)/0.036*np.sqrt(31))**2/31)) if np.median(dl)!=0 else None}
# escalas: O5 e 3G por SNR
# fonte fixa: sigma ∝ 1/SNR; deteccoes ∝ alcance^3
out['scalings_note']='sigma_i ∝ 1/SNR; N_det ∝ range^3 (mesma populacao). O5 aLIGO BBH range 2500 Mpc vs O4 1400-1600 (Observing Scenarios P1200087 v55 Tabela 2) => SNR x1.56-1.79 a fonte fixa; N_det x(2500/1500)^3=4.6'
for name,gain in [('O5_snr_gain_1.56',1.56),('O5_snr_gain_1.79',1.79)]:
    out['readings_'+name]={rd:{'N_events_for_5sigma':out['readings'][rd]['N_events_O4like_for_5sigma']/gain**2} for rd in readings}
json.dump(out,open('N5SIGMA_FROM_CATALOG.json','w'),indent=1)
print(json.dumps({k:v for k,v in out.items() if k!='per_event'},indent=1))
print('sigma per event (31):',sorted(round(x,3) for x in sig))
