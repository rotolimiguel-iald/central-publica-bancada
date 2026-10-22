"""E1.2/1.3/1.4: archived metadata and array arithmetic only, one thread."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, time, sys
import numpy as np
from lxml import html
B=Path(__file__).resolve().parents[2]; O=Path(__file__).resolve().parent
I=B.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS'
sources={}; started=time.perf_counter()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    p=p.resolve(); raw=p.read_bytes();sources[str(p)]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)};return raw
def load(p): return json.loads(read(p))
def require(ok,msg):
    if not ok: raise ValueError(msg)
def close(a,b): require(math.isclose(float(a),float(b),rel_tol=2e-11,abs_tol=2e-13),(a,b))
def new(name,raw):
    with (O/name).open('xb') as f:f.write(raw)
def dump(name,obj):new(name,(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
for name,pin in [('PORTAO_DA_AMPLIACAO_V1.json','710028a7d2af7b649511afe369d88462d2add95c5fecbb1fb03c517fc91fe8a0'),('PORTAO_DA_AMPLIACAO_V1.md','4fd8568d643525e415ab6d890a33220ce1eeb1447cad77f474d8cfce7e4c2dac')]:
    require(hashlib.sha256(read(B/name)).hexdigest()==pin,'E0 seal '+name)
for name in ['SELECTION_AND_CONTROLS.json','SELECTION_AND_CONTROLS.md','RECEIPT.json','SOURCE_PASSAGES.json']:
    require(not (O/name).exists(),'Existing output '+name)
D=I/'medicao_da_ampliacao/B_catalogos'; passages=[]
for fn,pdf,section,ranges in [
 ('gwtc5_tgr.txt','arxiv_2607.19293_gwtc5_tgr.pdf','7.2',[(4007,4042),(4318,4360),(4490,4515),(4638,4662)]),
 ('gwtc4_tgr3.txt','arxiv_2603.19021_gwtc4_tgr3.pdf','2.2',[(2630,2646),(3060,3104),(3533,3556)])]:
    read(D/pdf);lines=read(D/fn).decode('utf-8').split('\n')
    for a,b in ranges:passages.append({'path':str((D/fn).resolve()),'section':section,'first_line':a,'last_line':b,'text':'\n'.join(lines[a-1:b])})
raw=read(B/'cache/literature/gwtc3_article_v3.html'); tree=html.fromstring(raw)
for ident in ['S8.SS1.SSS2.p5.1','S8.SS1.SSS2.p8.1']:
    node=tree.xpath('//*[@id="'+ident+'"]');require(len(node)==1,ident)
    passages.append({'path':str((B/'cache/literature/gwtc3_article_v3.html').resolve()),'section':'VIII.1.2','html_id':ident,'text':' '.join(node[0].text_content().split())})
read(I/'medicao_da_ampliacao/C_piso_sistematico/s02_measure.py')
read(I/'revisao_da_gerencia/ceticos/c2_refeito/refazer_snr20.py')
old50=load(I/'revisao_da_gerencia/ceticos/c2_refeito/refeito_N50.json')['20.0']
c2=load(B/'C2_TRAJECTORY_RECOVERY.json')
r=next(r for r in c2['rows'] if r['reading']=='R-GLOBAL')
r=next(r for r in r['comparisons'] if r['detector_noise']!='NONE')
values=[f['dtau'] for f in r['fits']]; n=len(values);mean=math.fsum(values)/n
sd=math.sqrt(math.fsum((x-mean)**2 for x in values)/(n-1))
original50={'N':n,'mean':mean,'sd':sd,'se':sd/math.sqrt(n),'median':float(np.median(values))}
old50_comparison={k:abs(old50[k]-v) for k,v in original50.items()}
require(max(old50_comparison.values())<2e-8,'C2 independent replay versus stored fits tolerance')
c2summary=load(I/'revisao_da_gerencia/ceticos/c2_refeito/refeito_N2000.json')
for row in c2summary.values():
    close(row['se'],row['sd']/math.sqrt(row['N']));close(row['z_mean'],row['mean']/row['se'])
    row['mean_times_snr_squared']=row['mean']*row['SNR']**2
    row['residual_against_4_over_snr_squared_in_SE']=(row['mean']-4/row['SNR']**2)/row['se']
    row['verification']='Summary algebra checked; 2000 individual fits not archived in this file; no estimator rerun'
expanded=load(B/'bis/C2_TRAJECTORY_expanded_1000.json')
rg=next(r for r in expanded['rows'] if r['reading']=='R-GLOBAL')
expanded_noise={k:{kk:vv for kk,vv in v.items() if kk!='fits'} for k,v in rg.items() if isinstance(v,dict) and 'fits' in v}
imr=load(B/'C5_IMR_RECOVERY.json');reg=load(B/'REGISTRO_C5_IMR_RECOVERY.json')
require(imr['registration_sha256']==sha(B/'REGISTRO_C5_IMR_RECOVERY.json'),'C5 registration')
arrays={};groups={}
for f in imr['draws']:
    path=B/f['path'];read(path);require(sha(path)==f['sha256'],'C5 array hash')
    with np.load(path,allow_pickle=False) as z:
        key=path.name.split('_')[0];arrays[key]=z['draws'].copy();groups[key]=list(zip(z['H1_original_GPS'],z['L1_original_GPS']))
        require(z['columns'].tolist()==['lnB','a_hat','CI90_lower','CI90_upper'],'C5 columns')
sysdata=load(B/'bis/e0_core/SYSTEMATICS_ADENDO.json');sysreceipt=load(B/'bis/E0_SYSTEMATICS_REVIEW.json')
require(sysreceipt['source_sha256']==sha(B/'bis/e0_core/SYSTEMATICS_ADENDO.json'),'systematics receipt')
floor=load(I/'medicao_da_ampliacao/C_piso_sistematico/C_piso_medicoes.json')
delta=floor['efeito_delta_tau_hat_GW250114_mediana_posterior']['R-B']
for name,pin in floor['sources_sha16'].items():
    if name in ['C5_IMR_RECOVERY.json','C2_TRAJECTORY_RECOVERY.json','C4_CATALOG_220.json']:
        read(B/name); require(sha(B/name).startswith(pin),'Historical floor source '+name)
rows=[]
for idx,row in enumerate(imr['results']):
    if row['reading']!='R-B' or row['injection_family']!=row['recovery']:continue
    x=arrays[row['psd']][row['draws_index']][:,1];require(np.isfinite(x).all(),'a nonfinite')
    require(len(x)==row['N']==206,'C5 N')
    absbias=abs(float(np.median(x))-row['injected_a']);close(absbias,row['absolute_bias'])
    st=sysdata['full_IMR_family_recovery'][idx]
    require(st['locator']=='/results/'+str(idx),'source index')
    ratio=st['x220_recovery'];require(np.all(1+x*ratio>0),'physical damping denominator')
    dt=-x*ratio/(1+x*ratio); truth=-row['injected_a']*ratio/(1+row['injected_a']*ratio)
    n=len(dt);m=math.fsum(dt)/n;s=math.sqrt(math.fsum((v-m)**2 for v in dt)/(n-1))
    ng=len(set(groups[row['psd']])); require(ng==n,'Current selected cells require distinct paired GPS')
    se=s/math.sqrt(n)
    close(m,st['dtau_statistics']['mean']);close(se,st['dtau_statistics']['SE_mean_grouped_conditional'])
    close(float(np.median(dt))-truth,st['bias_median_dtau'])
    # Exact binomial order-statistic interval for a median, conditional on IID noise windows.
    k=max(k for k in range(1,n//2+1) if 2*sum(math.comb(n,j) for j in range(k))/2**n<=.10)
    sorted_dt=sorted(dt);ci=[sorted_dt[k-1]-truth,sorted_dt[n-k]-truth]
    rows.append({**{key:row[key] for key in ['psd','SNR','injected_a','injection_family','recovery','N','draws_index','coverage_90','boundary_hits']},'source_results_index':idx,
        'distinct_paired_GPS':ng,'historical_absolute_bias_proxy':absbias*abs(delta),
        'a_median_signed_bias':float(np.median(x))-row['injected_a'],'x220_family':ratio,
        'exact_mean_bias_dtau':m-truth,'SE_mean_conditional':se,'exact_median_bias_dtau':float(np.median(dt))-truth,
        'median_bias_CI90_order_statistics_IID_conditional':ci,'order_interval_one_based':[k,n-k+1],
        'error_scope':'Conditional on independent noise windows; inter-window dependence/PSD/model error not calibrated. Shared windows across cells: no independence of cells.'})
summaries={}
for snr in [40,200,600]:
    cells=[r for r in rows if r['SNR']==snr]; require(len(cells)==8,'C5 grid')
    vals=[r['historical_absolute_bias_proxy'] for r in cells];want=floor['B_familia_resumo']['R-B'][f'same_SNR{snr}_bias_dtau_abs']
    close(np.median(vals),want['median']);close(min(vals),want['min']);close(max(vals),want['max'])
    summaries[str(snr)]={'cells':8,'N_per_cell':206,'historical_abs_proxy_median':float(np.median(vals)),'historical_abs_proxy_range':[min(vals),max(vals)],
        'exact_abs_median_bias_median_across_cells':float(np.median([abs(r['exact_median_bias_dtau']) for r in cells])),
        'exact_mean_bias_range':[min(r['exact_mean_bias_dtau'] for r in cells),max(r['exact_mean_bias_dtau'] for r in cells)],
        'SE_mean_range':[min(r['SE_mean_conditional'] for r in cells),max(r['SE_mean_conditional'] for r in cells)],
        'pooled_SE':None,'scope':'Eight paired scenarios, not eight independent estimates; range is not confidence interval. SNR>=200 inverse-crime/numerical-waveform caveats remain.'}
for f in ['bis/F2_INJECTION_INDEPENDENT_REVIEW.md','bis/F2_RD_APPLICABILITY_REVIEW.md','bis/F2_RD_APPLICABILITY_REVIEW.json','bis/f2_injection/REPORT.md','bis/f2_injection/RECEIPT.json','bis/f2_injection/DESCRIPTIVE_RESULT.json','bis/f2_injection/PRIOR_CONTRACT.json','bis/c1_review/f2_injection_independent_results.json','bis/f2_review/rd_inventory.json','C5_FISHER_v3.json','C2_ADENDO_OBSERVAVEL_v2.md']:
    read(B/f)
data={'status':'E1_2_3_4_DOCUMENTARY_AND_ARCHIVED_CONTROLS_COMPLETE__SELECTION_EFFICIENCY_OPEN','utc':datetime.now(timezone.utc).isoformat(),'E0_seal_verified':True,
 'reading_scope':{'full_papers_read':False,'method':'Selected primary passages within GWTC3 VIII.1.2, GWTC4 III 2.2, GWTC5 7.2; PDFs archived, no claim of integral reading','passages_file':'SOURCE_PASSAGES.json','web_crosscheck':'GWTC3 v3 accessible; GWTC4/5 HTML returned 404; local primary PDF/text used'},
 'selection':{'LVK_pSEOBNR_operational_indicator':'I_catalog_and_quality(d) * 1[rho_inspiral_GR(d)>=8] * 1[rho_postinspiral_GR(d)>=8]',
   'O4_summary':'Median SNR from SEOBNRv5PHM GR analyses where available, not posterior deformational widths',
   'O1_O3_summary':'MAP GR IMRPhenomXPHM_MSA for later reanalyses; do not retroactively relabel original GWTC3 v4HM recovery',
   'availability':'Published membership can be read from tables; neither split-SNR per-event values nor exact executable implementation/frequency boundary were reconstructed here. Unavailable split SNR remains null, not approximated from GWOSC total.',
   'baseline_catalog_quality':'GWTC4 overview: >=2 detectors, FAR<=1e-3/yr. GWTC5 section2 uses inherited catalog/test criteria; not replaced by total SNR alone.',
   'E0_INPUT_indicator':'1[rho_GWOSC_network>=12] * 1[median_Mf_detector>=40 Msun] * 1[0<=median_chif<0.98]',
   'priority':'rho_GWOSC_network>=30; not extra eligibility cut','missing':'AWAITING_GR_METADATA; null eligibility when required metadata unavailable',
   'statistical_efficiency_definition':'epsilon(theta)=integral I_select(d) p(d|theta) dd; alpha(Lambda)=integral epsilon(theta) p(theta|Lambda) dtheta',
   'efficiency':None,'normalization_alpha':None,'efficiency_status':'OPEN_NOT_CALIBRATED','known_count_is_efficiency':False,
   'inference_scope':'For a population conditioned on N selected detections, alpha(Lambda)^(-N) normalization requires a selection model consistent with the likelihood; Poisson-count formulation is different. No normalization inserted or fitted here.',
   'positive_bias':'LVK says selection may favor positive damping deviations; this is not a quantified correction or proof of unique cause. GWTC3 also discusses prior asymmetry, correlations, noise modeling and finite catalog.',
   'no_transport':['rho_GWOSC != separate inspiral/postinspiral SNR','postinspiral >=8 != pure 220 RD window >=8','published binary selection != calibrated efficiency','c(sigma) fit does not alone pay selection efficiency']},
 'LVK_controls':{'pseobnr_injection':{'independent_injections':1,'recoveries':['NR_with_44','NR_without_44'],'posterior_rows_per_recovery':20000,'prior_220':[-.8,2.],'prior_positive_mass':2/2.8,'prior_440':[-.8,.8],'free_440_nuisance_both':True,'lnB':None,'c_SNR_curve_paid':False,'coverage_curve_paid':False,'scope':'Reuse F2 verified descriptive point. No posterior reread or PE. Two recoveries not independent events; posterior mass at GR not frequentist coverage.'},
   'RD':{'free_220_deformations':False,'physical_220_df_dg_fixed_zero':True,'available_nonKerr':'221 deviations; logarithmic df,dg, not fractional dtau','fractional_mapping':'delta_f=exp(df)-1; delta_tau=exp(-dg)-1','pSEOB_220_robustness_lnB':None,'c_SNR_curve_paid':False,'scope':'Reused F2 schema audit; no new NC/strain access. Unit coordinates not physical deformation; varying Kerr M/chi does not supply free 220.'},
   'gate':'NAO_PAGO_CURVA_C_SNR_PSEOB_AND_SELECTION_EFFICIENCY; handed to E3, no execution here'},
 'C2':{'original_N50_SNR20':original50,'manager_replay_N50_SNR20':old50,'original_vs_replay_absolute_differences':old50_comparison,'comparison_absolute_tolerance':2e-8,'existing_N2000_curve':list(c2summary.values()),'new_readonly_control':'Original 50 dtau fits recomputed; separate manager replay differs at numerical optimizer level, errors recorded. N2000 summaries checked algebraically only','readout':'Single channel whitened RG sinusoid, 128/4096 s, OU+white synthetic noise; variable projection, free df/logtau and amplitude/phase. Same seed/noise across SNR points; correlated controls. Not pSEOB PE.',
   'functional_form_scope':'4/rho^2 descriptive agreement in this conditional estimator, not fitted/adopted universal c(rho). At rho200 mean consistent with zero.',
   'expanded_1000_at_rho20':expanded_noise,'expanded_scope':'Different window 128/2048s and recolored finite noise library of 256; not another point of same synthetic curve.'},
 'C5':{'historical_proxy_definition':'abs(median(a_hat)-a_injected)*abs(delta_RB_GW250114_median); not signed bias, not exact nonlinear conversion','historical_delta':delta,
   'exact_conversion':'delta_tau(a)=-a*x220/(1+a*x220); bias relative to same-family injected truth',
   'scope':'Fixed representative source, fixed family-specific remnant, whole 22/44 deformation; marginal Gaussian quadrature amplitudes and profile a estimate. Not full astrophysical pSEOB posterior PE or calibrated operational c(rho).',
   'snr_basis':'Two illustrative response channels, network norm from 10 tM, reference source 403 Mpc; not GWOSC total network SNR or peak SNR.',
   'summaries':summaries,'cells':rows,'source_systematics_review':'Main-agent review of 2388 comparisons read/hash-checked; this audit separately checks only 24 R-B same-family archived cells.',
   'uncertainty':'Mean SE conditional on 206 distinct paired noise intervals; median order-statistic interval assumes IID. No pooled SE, no model/PSD uncertainty measured; same noise reused.',
   'transfer_to_LVK':'OPEN; do not splice C2 and C5 into one curve; no nuisance fit performed','Fisher':'sigma~2/rho only conditional local fixed-source diagnostic; free single220 M/spin nonidentifiability remains; no new Fisher computation'},
 'not_performed':['new MC/injections','strain','posterior downloads or test posterior access','waveform generation','C5 rerun','nuisance fitting','E2/E3','physical reading selection'],
 'source_hashes':sources,'wall_seconds_before_writes':time.perf_counter()-started}
dump('SOURCE_PASSAGES.json',passages);dump('SELECTION_AND_CONTROLS.json',data)
doc=['# E1.2–E1.4 — seleção e controles existentes','', '[REAL — custódia e contas leves; KNOWN — passagens primárias; OPEN — eficiência estatística e transferência]', '',
 'Selo E0 conferido por bytes: JSON e MD coincidem com os hashes fornecidos. Esta frente fecha leitura documental e controles arquivados; não paga uma curva de calibração pSEOB nem eficiência de seleção. Nenhum nuisance ajustado, posterior novo acessado ou E2/E3 executado.', '',
 '## Seleção: regra de entrada e eficiência são objetos distintos','',
 'O indicador pSEOBNR exige **SNR ≥8 em cada parte: inspiral e pós-inspiral**, além da elegibilidade de catálogo/qualidade. Em O4, onde disponível, a fonte usa a mediana da análise GR SEOBNRv5PHM; até O3b, nas reanálises descritas, usa MAP IMRPhenomXPHM MSA. Não se substituem esses dois números pela SNR total GWOSC, pela SNR do 220 numa janela de 10 tM, nem por largura posterior. Os valores separados e a implementação exata da separação em frequência não foram reconstruídos: função operativa documental especificada, execução por evento ainda não certificada.', '',
 'Separadamente, o INPUT adotado E0.3 é SNR de rede GWOSC≥12, mediana Mf_det≥40 M☉ e 0≤mediana chi_f<0,98; prioridade≥30. Falta de metadados mantém AWAITING_GR_METADATA. Essas medianas são prévias à deformação, sob GR; não são medidas independentes do strain. Critério adotado não significa eficiência conhecida.', '',
 'A eficiência ε(θ)=∫I_seleção(d)p(d|θ)dd e sua média populacional α(Λ)=∫ε(θ)p(θ|Λ)dθ permanecem **null/OPEN**. Para inferência condicionada a N selecionados, a normalização α(Λ)^−N exige modelo consistente; não inserimos α=1, correção numérica ou ajuste. Uma lista publicada, o corte determinístico ou um ajuste c(σ) não medem essa integral.', '',
 'Leitura efetiva: passagens das seções 7.2 do [GWTC-5](https://arxiv.org/abs/2607.19293), 2.2 do [GWTC-4 III](https://arxiv.org/abs/2603.19021) e [VIII.1.2 do GWTC-3](https://arxiv.org/html/2112.06861v3#S8.SS1.SSS2), com hashes e localizadores em SOURCE_PASSAGES/JSON. Não leitura integral. As páginas HTML dos dois primeiros retornaram 404; usamos os PDFs/textos primários já arquivados. A LVK descreve possível seleção favorável a amortecimento positivo e não a inclui na inferência hierárquica citada. Isso não quantifica o efeito nem escolhe sua causa: prior assimétrico, correlações, ruído e amostra finita continuam alternativas.', '',
 '## Uma injeção LVK e alcance do RD','',
 'Reutilizado o diagnóstico F2 auditado: **uma** injeção com duas recuperações com/sem 44, 20.000 linhas posteriores em cada. São o mesmo ponto físico, não 40.000 injeções nem curva em SNR. Priors 220 U(−0,8;2) têm massa positiva 5/7; 440 continua nuisance livre nas duas recuperações. lnB permanece null; conteúdos KDE em GR não são cobertura frequentista. Não se estimou eficiência, c(SNR), poder ou transferência da largura estocástica.', '',
 'No RD arquivado, os desvios físicos 220 estão fixos; há desvios do 221. Sua convenção é logarítmica: δf=exp(df)−1, δτ=exp(−dg)−1. Coordenadas unitárias variáveis e massa/spin Kerr não criam deformação 220 livre. Portanto não fornecem o mesmo lnB220 de robustez nem curva pSEOB. A ausência da curva está registrada como **NÃO PAGO**, a tratar em E3; não é ausência de todo controle útil.', '',
 '## C2: viés com sinal, um estimador sintético','',
 '| SNR do controle | N | média δτ̂ | EP da média | estatuto da conferência |','|---|---:|---:|---:|---|',
 f"|20|50|{mean:.9f}|{sd/math.sqrt(n if n==50 else 50):.9f}|50 estimativas arquivadas recalculadas|"
 ]
# Use archived original SE, avoiding later C5 local variable names.
doc[-1]=f"|20|50|{original50['mean']:.9f}|{original50['se']:.9f}|50 estimativas arquivadas recalculadas|"
for r in c2summary.values():doc.append(f"|{r['SNR']:g}|{r['N']}|{r['mean']:.9f}|{r['se']:.9f}|resumo da gerência; EP=sd/√N conferido|")
doc += ['', 'Os 2000 ajustes individuais não estão no resumo; não foram regenerados. 4/ρ² é aproximação descritiva compatível com estes erros, não lei universal ou nuisance escolhido. Os pontos reutilizam ruído e não são independentes. O ensaio posterior de 1000 trajetórias em SNR20 tem janela/ruído diferentes; não integra esta curva. Cauchy R-LIN não possui variância de fase; a dispersão arquivada é do estimador limitado.', '',
 '## C5: outro estimador e outra base de SNR','',
 'Recalculadas 24 células R-B da mesma família, a=0/1, duas PSDs e SNR40/200/600, com 206 estimativas arquivadas por célula. Não é PE completa de parâmetros astrofísicos: remanescente fixo, amplitudes de quadratura marginalizadas e perfil de a. Todas usam os mesmos pares de ruído entre células; não há N=1648 independente por SNR.', '',
 '| SNR rede desde 10 tM | mediana histórica do proxy absoluto | faixa entre 8 células | faixa EP média δτ exata |',
 '|---:|---:|---|---|']
for snr,s in summaries.items():doc.append(f"|{snr}|{s['historical_abs_proxy_median']:.9f}|{s['historical_abs_proxy_range']}|{s['SE_mean_range']}|")
doc += ['', 'A coluna histórica é proxy linear **absoluta**, não média com sinal. O JSON conserva-a e acrescenta, por célula, a conversão exata −a x/(1+a x), verdade injetada, viés médio/mediano, EP condicional e intervalo da mediana por estatísticas de ordem. As faixas da tabela não são IC. Os erros não incluem incerteza de PSD/modelo nem dependência entre intervalos. Nenhum EP agregado é inventado.', '',
 'O resumo histórico de 0,0083@40 e 0,0011@200 é reproduzido, mas não pode ser unido a +0,030@20 de C2 para formar uma curva. A fonte C5 é representativa a 403 Mpc; SNR é da rede ilustrativa na janela desde 10 tM, diferente da SNR total GWOSC. Mesma família contém o gerador: fechamento condicionado. As limitações de forma de onda/SEOB em SNR≥200 e o crime inverso permanecem; erros pequenos não pagam a calibração física. Fisher 2/ρ é limite local de fonte fixa e não resolve degenerescência de um 220 com massa/spin livres.', '',
 'O parecer principal de sistemáticas (2388 comparações) foi lido e seu vínculo por hash conferido; não é atribuído a esta frente. Aqui foram feitos somente os controles de 24 células descritos. Nenhuma leitura física foi escolhida. Gate sistemático e curva/eficiência operacional permanecem abertos.', '',
 '## Custódia e reprodução leve','',
 'SELECTION_AND_CONTROLS.json contém parâmetros, erros, escopos e SHA256 completos de cada fonte. RECEIPT.json identifica código/saídas e confirma entradas inalteradas. O código recusa destinos existentes e não importa construtores científicos. O replay N50 da gerência e os ajustes N50 originais diferem em menos de 2e−8 nas estatísticas comparadas, não por igualdade de bytes; diferenças registradas. Não houve campanha ou alteração de produção.', '']
new('SELECTION_AND_CONTROLS.md','\n'.join(doc).encode())
require(all(sha(Path(p))==v['sha256'] for p,v in sources.items()),'Input changed during review')
dump('RECEIPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_READONLY_ARITHMETIC_AND_SCOPE','python_optimize':sys.flags.optimize,'threads':1,'wall_seconds':time.perf_counter()-started,'code':{'path':str(Path(__file__)),'sha256':sha(Path(__file__))},'outputs':{name:{'sha256':sha(O/name),'bytes':(O/name).stat().st_size} for name in ['SELECTION_AND_CONTROLS.json','SELECTION_AND_CONTROLS.md','SOURCE_PASSAGES.json']},'input_bytes_unchanged':True,'science_rerun':False})
print(json.dumps({'status':data['status'],'C5_cells':len(rows),'C2_original_draws':len(values),'C5_summary':summaries,'seconds':time.perf_counter()-started}))
