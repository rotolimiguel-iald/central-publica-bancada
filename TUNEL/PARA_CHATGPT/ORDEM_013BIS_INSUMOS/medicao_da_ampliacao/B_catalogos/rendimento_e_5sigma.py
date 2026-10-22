"""Rendimento de eventos com ringdown util (pSEOBNR) por era e N para 5 sigma por leitura.
Fontes locais lidas com sha16; numeros publicos com URL. beta em runtime."""
import json,hashlib,math,re,numpy as np
ALPHA=7.2973525693e-3; BETA=ALPHA*math.sqrt(math.e)
def sha16(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
BENCH=r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
cat=json.load(open(BENCH+r"\C4_CATALOG_220.json",encoding='utf-8'))
sel31=set(json.load(open(BENCH+r"\C4_CATALOG_COMBINATION.json",encoding='utf-8'))['selected_events'])
t5=json.load(open('gwtc5_tgr_table2_3_parsed.json'))
# SNR por evento: O4b (Tabela 2 do GWTC-5.0 TGR) + pre-O4b (Tabela 1 do GWTC-4.0 TGR III, lido do txt)
snr={d['event']:d['snr'] for d in t5}
t4=open('gwtc4_tgr3.txt',encoding='utf-8').read().replace('\n',' '); t4=re.sub(r'\s+',' ',t4)
i1=t4.find('Table 1. Event selection table'); tab=t4[i1:i1+16000]
for m in re.finditer(r'(GW\d{6}(?: \d{6})?)\*? (\d+\.\d)\+',tab):
    nm=m.group(1).replace(' ','_'); 
    if nm=='GW150914': nm='GW150914_095045'
    if nm=='GW170104': nm='GW170104_101158'
    snr.setdefault(nm,float(m.group(2)))
z90=1.6448536
ev=[]
for r in cat['rows']:
    q=r['quantiles']['dtau220']; sig=(q[2]-q[0])/(2*z90)
    pred={rr['reading']:rr['median_prediction']['delta_tau_ensemble_exact'] for rr in r['rows'] if rr['reading'] in ('R-B','R-RAIZ-0','R-MOD','R-LIN')}
    ev.append(dict(event=r['event'],in31=r['event'] in sel31,snr=snr.get(r['event']),sigma_dtau=sig,dtau_med=q[1],pred=pred))
miss=[e['event'] for e in ev if e['snr'] is None]; print('sem SNR:',miss)
e31=[e for e in ev if e['in31'] and e['snr']]
S=np.array([e['snr'] for e in e31]); G=np.array([e['sigma_dtau'] for e in e31])
# ajuste sigma = A / SNR^p em log
p,lnA=np.polyfit(np.log(S),np.log(G),1); A=math.exp(lnA)
print('ajuste sigma_dtau = %.3f * SNR^(%.3f)  (31 eventos)'%(A,p))
# ajuste com p=-1 fixo: A1 = exp(mean(ln(sigma*SNR)))
A1=math.exp(np.mean(np.log(G*S))); print('com p=-1 fixo: sigma_dtau = %.3f / SNR'%A1)
resid=np.log(G)-(lnA+p*np.log(S)); print('dispersao log residual',resid.std())
out={'beta_runtime':BETA,'sources':{'C4_CATALOG_220.json':sha16(BENCH+r"\C4_CATALOG_220.json"),'C4_CATALOG_COMBINATION.json':sha16(BENCH+r"\C4_CATALOG_COMBINATION.json"),'arxiv_2607.19293_gwtc5_tgr.pdf':sha16('arxiv_2607.19293_gwtc5_tgr.pdf'),'arxiv_2603.19021_gwtc4_tgr3.pdf':sha16('arxiv_2603.19021_gwtc4_tgr3.pdf')},
 'sigma_vs_snr_fit_31':{'A':A,'p':p,'A_p_fixed_-1':A1,'log_resid_sd':float(resid.std()),'events':[(e['event'],e['snr'],round(e['sigma_dtau'],4)) for e in e31]}}
# rendimento por era (contagens lidas das tabelas / GraceDB / abstracts)
yield_={
 'O1-O3 (GWTC-3 TGR set)':{'TGR_events':49,'pSEOBNR_used':10,'pSEOBNR_products':12,'source':'168-72-5-42=49 (GWTC-5.0 TGR abs + GWTC-4.0 TGR abs); Tabela 13 GWTC-3 TGR (10) + 2 controles','estatuto':'[REAL lido]/[DERIVED subtracao]'},
 'O4a (GWTC-4.0)':{'sig_gracedb':81,'TGR_events':42,'TGR_events_incl_5_reanalysis':47,'pSEOBNR':7,'pyRing_sel':22,'QNMRF':2,'months':7.8,'source':'GraceDB O4a; arXiv:2603.19021 Tabela 1 (parse); GWTC-5.0 TGR Tabela 3','estatuto':'[REAL lido]'},
 'O4b (GWTC-5.0)':{'sig_gracedb':105,'catalog_pastro':161,'catalog_FAR<1yr':104,'TGR_events':72,'pSEOBNR':14,'RD_rho_pp>=10':6,'QNMRF':4,'months':9.6,'source':'GraceDB O4b; arXiv:2605.27225 abs; arXiv:2607.19293 Tabela 2 (parse)','estatuto':'[REAL lido]'},
 'O4c (GWTC-6, previsto)':{'sig_gracedb':68,'months':9.7,'source':'GraceDB O4c 68 (77-9 retratados); O4c 28/01/2025-18/11/2025','estatuto':'[REAL contagem GraceDB]; TGR/pSEOBNR [DERIVED por fracao O4a+O4b]'},
}
fTGR=(42+72)/(81+105); fPS=(7+14)/(42+72); fPS_sig=(7+14)/(81+105)
yield_['fracoes_O4ab']={'TGR_por_significativo':fTGR,'pSEOBNR_por_TGR':fPS,'pSEOBNR_por_significativo':fPS_sig,'pSEOBNR_por_TGR_cumulativo_168':31/168}
yield_['O4c (GWTC-6, previsto)'].update({'TGR_est':68*fTGR,'pSEOBNR_est':68*fPS_sig})
# taxa anual O4 (a+b): 21 pSEOBNR em 7.8+9.6 meses
rate_O4=21/((7.8+9.6)/12); yield_['taxa_pSEOBNR_por_ano_O4ab']=rate_O4
out['rendimento']=yield_
# N para 5 sigma, por leitura, com sigma reais (31) e escalas
res={}
for rd in ['R-B','R-RAIZ-0','R-MOD','R-LIN']:
    dl=np.array([e['pred'][rd] for e in e31]); z2=(dl/G)**2; mz2=z2.mean(); dmed=float(np.median(np.abs(dl)))
    N_O4=25/mz2
    # O5: mesma populacao, SNR x g, deteccoes x g^3 (alcance BBH 2500 vs 1400-1600)
    g_lo,g_hi=2500/1600,2500/1400
    N_O5_lo,N_O5_hi=N_O4/g_hi**2,N_O4/g_lo**2
    # 3G: ancora empirica GW250114: sigma 0.058 em SNR_RD~40 (pos-fusao ~40 por ORDEM 1.3); sigma ∝ 1/SNR_RD
    sig40=min(G); 
    def N_at(snr_rd): s=sig40*40/snr_rd; return 25/(dmed/s)**2
    res[rd]={'delta_tau_pred_med':dmed,'N_O4like_5sigma':N_O4,'anos_O4like_a_%.1f_por_ano'%rate_O4:N_O4/rate_O4,
             'N_O5like_5sigma_range':[N_O5_lo,N_O5_hi],'anos_O5_a_taxa_x4.6..5.7':[N_O5_lo/(rate_O4*g_lo**3),N_O5_hi/(rate_O4*g_lo**3)],
             'SNR_RD_5sigma_evento_unico':40*5*sig40/dmed,'N_5sigma_SNR_RD_50':N_at(50),'N_5sigma_SNR_RD_100':N_at(100),
             'anos_3G_com_100/ano_SNR_RD>=50':N_at(50)/100,'anos_3G_com_10/ano_SNR_RD>=100':N_at(100)/10}
out['N_5sigma']=res
out['premissas']=['z_i=delta_pred_i/sigma_i; sigma_i=(q95-q05)/(2*1.645) da marginal real de dtau220 (pSEOB); 5 sigma = sum z_i^2 >= 25 (deformacao comum, sem sistematica, sem vies +0.03 nem familia SEOB/Phenom ~0.9 do efeito)',
 'O5: alcance BBH aLIGO 2500 Mpc vs O4 1400-1600 (Observing Scenarios P1200087 v55, Tabela 2): SNR fonte fixa x1.56-1.79, deteccoes x3.8-5.7',
 '3G: ~10^2 eventos/ano com SNR_RD>=50 e O(10)/ano com SNR_RD>=100 em ET+CE (Berti et al. 2025/2026 Sec. 7.1, Fig. 76, citando Bhagwat et al. 2023)',
 'ancora empirica: menor sigma real = %.4f (GW250114, SNR rede 76.9, pos-fusao ~40)'%sig40]
json.dump(out,open('RENDIMENTO_E_5SIGMA.json','w'),indent=1,ensure_ascii=False)
print(json.dumps({k:out[k] for k in ['rendimento','N_5sigma']},indent=1,ensure_ascii=False))
