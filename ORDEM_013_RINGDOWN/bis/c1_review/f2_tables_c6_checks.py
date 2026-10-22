"""Transport audit from archived JSON/CSV only; never open strain/posteriors."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,math,csv,hashlib,statistics
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.interpolate import make_interp_spline
R=Path(__file__).resolve().parents[2]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def get(p):return json.loads((R/p).read_bytes())
def close(x,y,msg):need(math.isclose(x,y,rel_tol=3e-13,abs_tol=1e-14),msg)
def put(p,data):
    need(not p.exists(),'Output exists');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    need(t.read_bytes()==data,'Write differs');need(not p.exists(),'Output appeared');t.rename(p)
out=R/'bis/c1_review/f2_tables_c6_results.json';need(not out.exists(),'Output exists')
t=get('bis/F2_ALL_READING_TABLES.json');c=get('C6_ADENDO_REALIZADO.json')
names=set(t['source_sha256'])|set(c['source_sha256'])|{'bis/F2_ALL_READING_TABLES.json','bis/F2_ALL_READING_TABLES.csv','C6_ADENDO_REALIZADO.json','refeito/summarize_f2_tables_013bis.py','refeito/record_c6pre_013bis.py','tgl_ringdown_prediction.py','c6_engine.py'}
hashes={n:sha(R/n) for n in names}
for d,code in [(t,'refeito/summarize_f2_tables_013bis.py'),(c,'refeito/record_c6pre_013bis.py')]:
    for n,h in d['source_sha256'].items():need(hashes[n]==h,'Source hash '+n)
    need(d['code_sha256']==hashes[code],'Code hash')
    need(d['opening_sha256']==sha(R.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'),'Opening hash')
reg=get('REGISTRO_C6.json')
for n in ['tgl_ringdown_prediction.py','QNM_GRID.json','c6_engine.py']:need(reg['code_and_input_hashes'][n]==hashes[n],'Transitive dependency '+n)
need(c['supersedes']=='C6_RESULTS.json' and c['supersedes_sha256']==hashes['C6_RESULTS.json'],'C6 origin')
readings={r['reading'] for r in get('C1_LEITURAS_v4.json')['rows']}
groups={}
for row in t['rows']:groups.setdefault(row['dataset'],[]).append(row)
need(len(groups)==6 and len(t['rows'])==60 and all(len(v)==10 and {r['reading'] for r in v}==readings for v in groups.values()),'60-row coverage')
cat=get('C4_CATALOG_220.json');old=get('C4_GWTC3_220.json');comb=get('C4_CATALOG_COMBINATION.json')
old10=get('C4_GWTC3_PUBLISHED_COMBINATION.json');old18=get('C4_GWTC3_COMBINATION.json');py=get('C4_PYRING.json')
datasets={
 'GWTC5_31':([e for e in cat['rows'] if e['event'] in comb['selected_events']],comb['catalog']['release_figure_selection_31'],next(d for d in comb['common_deformation_GR_diagnostics'] if d['selection']=='release_figure_selection_31' and d['bandwidth']==1)),
 'GWTC5_33':(cat['rows'],comb['catalog']['all_available_33'],next(d for d in comb['common_deformation_GR_diagnostics'] if d['selection']=='all_available_33' and d['bandwidth']==1)),
 'GWTC3_10':([e for e in old['rows'] if e['event'] in old10['selected_events']],old10['catalog'],next(d for d in old10['common_deformation_GR_diagnostics'] if d['bandwidth']==1)),
 'GWTC3_18':([e for e in old['rows'] if e['event'] in old18['selected_events']],old18['catalog'],next(d for d in old18['common_deformation_GR_diagnostics'] if d['bandwidth']==1))}
def sigma(e):
    r=next(r for r in e['rows'] if r['reading']=='R-B');return abs(r['shift_05_50_95'][1])/r['correction_over_sigma']
catalog_checks=[]
for dataset,(events,summary,diag) in datasets.items():
    need(len(events)==int(dataset.rsplit('_',1)[1]) and len({e['event'] for e in events})==len(events),'Event coverage')
    ws=[sigma(e)**-2 for e in events];norm=math.fsum(ws);ws=[v/norm for v in ws];sd=norm**-.5
    center=math.fsum(w*e['quantiles']['dtau220'][1] for w,e in zip(ws,events))
    for row in groups[dataset]:
        reading=row['reading'];analytic=reading in ['R-PROP','R-RAIZ-COHERENT'];need(row['analytic']==analytic,'Analytic flag')
        lines=[] if analytic else [next(r for r in e['rows'] if r['reading']==reading) for e in events]
        lbs=[0.]*len(events) if analytic else [r.get('lnB',r.get('lnB_conditional_uniform_prior')) for r in lines]
        bands=[0.,0.,0.] if analytic else [math.fsum(r['lnB_bandwidth'][i] for r in lines) for i in range(3)]
        shift=0. if analytic else math.fsum(w*r['shift_05_50_95'][1] for w,r in zip(ws,lines))
        total=math.fsum(lbs);jack=[math.fsum(lbs[:i]+lbs[i+1:]) for i in range(len(lbs))]
        expected={'lnB':total,'lnB_bandwidth_min':min(bands),'lnB_bandwidth_max':max(bands),'delta_L_weighted':shift,'sigma':sd,'observed_center':center,'z':(center-shift)/sd,'correction_over_sigma':abs(shift)/sd,'GR_z':center/sd,'GR_HPD':diag['GR_HPD_content'],'jackknife_lnB_min':min(jack),'jackknife_lnB_max':max(jack),'max_information_fraction':max(ws),'max_abs_lnB_fraction':0. if not any(lbs) else max(map(abs,lbs))/math.fsum(map(abs,lbs))}
        for k,v in expected.items():close(row[k],v,dataset+'/'+reading+'/'+k)
        need(row['N_events']==len(events) and row['event_ids']==[e['event'] for e in events],'Event ids')
        if not analytic:need(row['verdict']==next(s for s in summary if s['reading']==reading)['verdict'],'Verdict transport')
        need(row['would_cross_BF_rule_without_relative_clause']==all(b<=-math.log(100) for b in bands),'BF crossing')
        catalog_checks.append(dict(dataset=dataset,reading=reading,**expected))
fallbacks=[]
gw=next(e for e in cat['rows'] if e['event']=='GW250114_082203')
for dataset,event in [('GW250114_pSEOB',gw),('GW250114_pyRing',py)]:
    qs=event['quantiles']['dtau220'];sd=sigma(event) if dataset.endswith('pSEOB') else (qs[2]-qs[0])/(2*statistics.NormalDist().inv_cdf(.95))
    for row in groups[dataset]:
        src=[r for r in event['rows'] if r['reading']==row['reading']]
        need(len(src)<=1,'Duplicate source reading')
        close(row['sigma'],sd,'Single sigma');close(row['GR_HPD'],event['GR_HPD_content'],'Single HPD')
        if src:
            r=src[0];delta=r['shift_05_50_95'][1]
            for k,v in [('lnB',r['lnB']),('delta_L_weighted',delta),('lnB_bandwidth_min',min(r['lnB_bandwidth'])),('lnB_bandwidth_max',max(r['lnB_bandwidth']))]:close(row[k],v,'Single transport')
            need(row['verdict']==r['verdict'] and not row['analytic'],'Single verdict')
        else:
            delta=0.;need(row['analytic'] and row['lnB']==0,'Fallback marker');fallbacks.append(dict(dataset=dataset,reading=row['reading']))
        close(row['z'],(qs[1]-delta)/sd,'Single z');close(row['correction_over_sigma'],abs(delta)/sd,'Single correction')
need(t['positive_medians_31']==sum(e['quantiles']['dtau220'][1]>0 for e in datasets['GWTC5_31'][0]),'Positive medians')
with (R/'bis/F2_ALL_READING_TABLES.csv').open(newline='',encoding='utf-8') as f:csvrows=list(csv.DictReader(f))
need(len(csvrows)==60,'CSV count')
for csvrow,row in zip(csvrows,t['rows']):
    for k,v in csvrow.items():
        if isinstance(row[k],(int,float)):close(float(v),row[k],'CSV number '+k)
        else:need(v==row[k],'CSV text '+k)
csv_missing=[k for k in ['analytic','analytic_scope','scope','reason','N_events','observed_center','GR_z','event_ids'] if k not in csvrows[0]]
need(len(c['rows'])==10 and {r['reading'] for r in c['rows']}==readings,'C6 coverage')
primary=[r for r in get('C6_RESULTS.json')['results'] if r['primary_start'] and r['amplitude_prior_sd_strain']==1e-20]
reference=next(r for r in primary if r['reading']=='R-GLOBAL')
mass=reference['mass_05_50_95'][1];spin=reference['spin_05_50_95'][1]
need(mass==c['primary_reference']['mass_detector_solar'] and spin==c['primary_reference']['spin'],'C6 median')
gate={r['reading']:r for r in get('PORTAO_DO_PODER_013_v2.json')['readings'] if r['base']=='GW250114_MEASURED_NORM_10tM'}
qnm=get('QNM_GRID.json')['modes']['220'];w=complex(make_interp_spline(qnm['spins'],np.asarray(qnm['real'])+1j*np.asarray(qnm['imag']))(spin))
beta=7.2973525693e-3*math.sqrt(math.e);G=6.67430e-11;C=299792458.;hb=6.62607015e-34/(2*math.pi);tp=math.sqrt(hb*G/C**5);tm=mass*1.3271244e20/C**3
wr=1.5251-1.1568*(1-spin)**.1292;Q=.7+1.4187*(1-spin)**(-.499);omega=wr/tm;tau=2*Q*tm/wr
def deltas(z):
    z1=1+z;root=math.sqrt(1-spin*spin);kh=root/(2*(1+root))
    w0=mass*1.3271244e20/G*C*C/(hb*z1*z1)
    xx={'R-A':beta*(tp*z1)*omega*omega*tau/2,'R-B':beta*wr*Q,'R-RAIZ-0':beta*Q,'R-LIN':2*beta*Q,'R-GLOBAL':0.,'R-RAIZ-EP4':beta*omega**2*tau/(2*(math.sqrt(1/(4*tp*z1)+omega)+math.sqrt(1/(4*tp*z1)))**2),'R-RAIZ-REST':beta*omega**2*tau/(2*(math.sqrt(w0+omega)+math.sqrt(w0))**2),'R-MOD':beta*math.pi*(w.real-spin/(1+root))**2/(kh*(-w.imag))}
    return {k:-v/(1+v) for k,v in xx.items()}
d0=deltas(0);dz=deltas(reg['reference_redshift']);prediction_checks=[]
for row in c['rows']:
    reading=row['reading'];need(row['sigma_effective_actual_route'] is None and row['z_actual_route'] is None and row['verdict']=='INCONCLUSIVE_SYSTEMATICS','Invented sigma or verdict')
    need(row['optimistic_fixed_source_reference']==gate[reading]['fixed_source'] and row['single_220_free_source']==gate[reading]['unknown_source_single_220'],'Fisher transfer')
    matching=[r for r in primary if r['reading']==reading]
    if matching:close(row['lnB_220plus440'],matching[0]['lnB_vs_GR'],'C6 lnB transfer')
    elif reading in ['R-A','R-RAIZ-EP4','R-RAIZ-REST']:need(row['lnB_220plus440']==0 and reading in reg['subresolution_readings'],'C6 numerical alias')
    else:need(row['lnB_220plus440'] is None and row['delta_L_at_GR_median'] is None,'Open physical mapping')
    if reading in d0:
        value=row['delta_L_at_GR_median'];need(math.isclose(value,d0[reading],rel_tol=1e-12,abs_tol=0),'C6 delta arithmetic')
        prediction_checks.append(dict(reading=reading,stored=value,independent_z0=d0[reading],registered_z=reg['reference_redshift'],at_registered_z=dz[reading],relative_change=None if value==0 else dz[reading]/value-1))
need(c['timing']==get('bis/C3_C6_TIMING_013BIS.json')['rows'],'Timing transport')
for row in c['noise']:
    n=next(r for r in get('C5_EMPIRICAL_NOISE.json')['detectors'] if r['detector']==row['detector'])
    se=math.sqrt(2/n['whitened_dof']/n['N_held_out']);close(row['mean_standard_error_iid_approx'],se,'Noise SE');close(row['z_unit_scale_iid_approx'],(n['reduced_chisquare_mean']-1)/se,'Noise z')
need(c['differences_from_pyRing']==get('C6_PYRING_START_COMPARISON.json')['differences'],'pyRing scope transfer')
audit=R.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_2_C6.txt';need(sha(audit)==c['only220_variant']['source_sha256'],'Auditor hash')
at=audit.read_text(encoding='utf-8')
for reading,value in c['only220_variant']['lnB'].items():need(f'{reading} −{abs(value):.4f}'.replace('.',',') in at,'Auditor transcription')
need(before_status:=c['only220_variant']['status']=='DECLARADO_INDEPENDENT_AUDITOR__NOT_RERUN_IN_F5','Auditor status')
need(hashes=={n:sha(R/n) for n in hashes},'Inputs changed')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='TRANSPORT_NUMBERS_PASS__STATUTE_AND_REDSHIFT_FINDINGS',input_hashes=hashes,script_sha256=sha(Path(__file__)),tables=dict(rows=60,csv_rows=60,groups={k:len(v) for k,v in groups.items()},catalog_checks=catalog_checks,single_source_fallbacks=fallbacks,analytic_rows=sum(r['analytic'] for r in t['rows']),csv_missing_context=csv_missing,positive_medians_31=t['positive_medians_31']),C6=dict(rows=10,primary_computed_readings=len(primary),predictions=prediction_checks,source_auditor_hash=sha(audit),actual_sigmas_all_null=True,no_strain_read_by_this_audit=True),inputs_unchanged=True)
put(out,(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode());print(json.dumps(dict(status=result['status'],csv_missing=csv_missing,predictions=prediction_checks,positive_medians=t['positive_medians_31']),indent=2))
