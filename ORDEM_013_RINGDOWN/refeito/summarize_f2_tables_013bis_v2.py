"""Generate all-reading nonblind comparisons from frozen C4 JSON, no new fit."""
from pathlib import Path
from datetime import datetime,timezone
import json,math,hashlib,statistics,csv,io
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={}
def read(name):
    p=ROOT/name;sources[name]=sha(p);return json.loads(p.read_bytes())
def new(name,raw):
    p=ROOT/name
    if p.exists():raise FileExistsError(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p);print(name,sha(p))
cat=read('C4_CATALOG_220.json');comb=read('C4_CATALOG_COMBINATION.json')
old=read('C4_GWTC3_220.json');old18=read('C4_GWTC3_COMBINATION.json');old10=read('C4_GWTC3_PUBLISHED_COMBINATION.json');py=read('C4_PYRING.json')
readings=[r['reading'] for r in cat['catalog']]+['R-PROP','R-RAIZ-COHERENT']
if len(set(readings))!=10:raise ValueError('Reading coverage')
EXPECTED_COMPUTED=set(readings)-{'R-PROP','R-RAIZ-COHERENT'}
PYRING_COMPUTED={'R-B','R-RAIZ-0','R-LIN','R-MOD'}
def require_coverage(event, expected):
    found=[r['reading'] for r in event['rows']]
    if len(found)!=len(set(found)) or set(found)!=expected:
        raise ValueError('Computed reading coverage missing, extra or duplicated')
for event in cat['rows']+old['rows']:require_coverage(event,EXPECTED_COMPUTED)
require_coverage(py,PYRING_COMPUTED)
# Negative guard runs before any writes, independent of Python assertions/-O.
probe=dict(py,rows=[r for r in py['rows'] if r['reading']!='R-MOD'])
try:require_coverage(probe,PYRING_COMPUTED)
except ValueError:pass
else:raise RuntimeError('Missing R-MOD silently accepted')
rows=[]
def entry(event,reading):return next(r for r in event['rows'] if r['reading']==reading)
def sigma(event):
    rb=entry(event,'R-B');return abs(rb['shift_05_50_95'][1])/rb['correction_over_sigma']
def logb(line):return line.get('lnB',line.get('lnB_conditional_uniform_prior'))
def group(name,events,summary,diag):
    weights=[1/sigma(e)**2 for e in events];sw=sum(weights);weights=[w/sw for w in weights]
    uncertainty=1/math.sqrt(sw);center=sum(w*e['quantiles']['dtau220'][1] for w,e in zip(weights,events))
    for reading in readings:
        analytic=reading in ('R-PROP','R-RAIZ-COHERENT')
        lines=[] if analytic else [entry(e,reading) for e in events]
        lb=[0.]*len(events) if analytic else [logb(r) for r in lines]
        total=sum(lb);bands=[0.,0.,0.] if analytic else [sum(r['lnB_bandwidth'][i] for r in lines) for i in range(3)]
        shifts=[0.]*len(events) if analytic else [r['shift_05_50_95'][1] for r in lines]
        delta=sum(w*d for w,d in zip(weights,shifts));jack=[total-v for v in lb]
        norm=sum(abs(v) for v in lb);maxln=0 if norm==0 else max(abs(v) for v in lb)/norm
        if not analytic:
            target=next(r for r in summary if r['reading']==reading)
            if abs(total-target['lnB'])>1e-10:raise ValueError('Stored sum mismatch')
            verdict=target['verdict']
        else:verdict='INCONCLUSIVE_SYSTEMATICS' if diag['GR_outside_95'] else 'NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL'
        rows.append(dict(dataset=name,reading=reading,N_events=len(events),lnB=total,lnB_bandwidth_min=min(bands),lnB_bandwidth_max=max(bands),delta_L_weighted=delta,sigma=uncertainty,
         observed_center=center,z=(center-delta)/uncertainty,correction_over_sigma=abs(delta)/uncertainty,GR_z=center/uncertainty,GR_HPD=diag['GR_HPD_content'],verdict=verdict,
         reason='GR outside 95% in this same diagnostic; failed systematics gate' if diag['GR_outside_95'] else 'Conditional comparison, not physical confirmation',
         sigma_scope='Inverse-variance combination of marginal posterior standard deviations; center and delta use event medians. Gaussian diagnostic, not the catalog KDE posterior nor a calibrated significance.',
         analytic=analytic,analytic_scope='Numerically zero under declared small-effect scenario; propagation/coherent realization mapping remains OPEN; not exact physical equality' if analytic else None,
         jackknife_lnB_min=min(jack),jackknife_lnB_max=max(jack),max_abs_lnB_fraction=maxln,max_information_fraction=max(weights),event_ids=[e['event'] for e in events],
         would_cross_BF_rule_without_relative_clause=all(b<=-math.log(100) for b in bands),
         scope='Conditional 220 sector; higher modes as in release. GWTC5 440 fixed to GR in 32/33 products; GW250114 free-440 nuisance. Not full multimode TGL likelihood.'))
for selection,ids in [('release_figure_selection_31',comb['selected_events']),('all_available_33',[e['event'] for e in cat['rows']])]:
    events=[e for e in cat['rows'] if e['event'] in ids]
    if len(events)!=len(ids):raise ValueError('Missing event')
    diag=next(d for d in comb['common_deformation_GR_diagnostics'] if d['selection']==selection and d['bandwidth']==1.)
    group('GWTC5_'+str(len(events)),events,comb['catalog'][selection],diag)
for data in [old10,old18]:
    events=[e for e in old['rows'] if e['event'] in data['selected_events']]
    diag=next(d for d in data['common_deformation_GR_diagnostics'] if d['bandwidth']==1.)
    group('GWTC3_'+str(len(events)),events,data['catalog'],diag)
gw=next(e for e in cat['rows'] if e['event']=='GW250114_082203')
for name,event in [('GW250114_pSEOB',gw),('GW250114_pyRing',py)]:
    # pyRing original JSON lacks a standard deviation. Preserve the honest quantile proxy.
    qs=event['quantiles']['dtau220'];std=sigma(event) if name.endswith('pSEOB') else (qs[2]-qs[0])/(2*statistics.NormalDist().inv_cdf(.95))
    for reading in readings:
        matches=[r for r in event['rows'] if r['reading']==reading]
        expected=EXPECTED_COMPUTED if name.endswith('pSEOB') else PYRING_COMPUTED
        analytic=reading in (set(readings)-expected)
        if bool(matches)==analytic:raise ValueError('Computed/analytic coverage inconsistent')
        if matches:
            line=matches[0];shift=line['shift_05_50_95'];delta=shift[1];lb=line['lnB'];bands=line['lnB_bandwidth'];verdict=line['verdict']
        else:shift=None;delta=0.;lb=0.;bands=[0.,0.,0.];verdict='NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL'
        rows.append(dict(dataset=name,reading=reading,N_events=1,lnB=lb,lnB_bandwidth_min=min(bands),lnB_bandwidth_max=max(bands),delta_L_weighted=delta,delta_L_05_50_95=shift,sigma=std,
          observed_center=qs[1],z=(qs[1]-delta)/std,correction_over_sigma=abs(delta)/std,GR_z=qs[1]/std,GR_HPD=event['GR_HPD_content'],verdict=verdict,
          reason='Small conditional density ratio; same event, not multiplied with catalog or other method',
          sigma_scope='Marginal posterior standard deviation' if name.endswith('pSEOB') else 'Gaussian-equivalent sigma from 5–95% interval; actual standard deviation not stored in source JSON',
          analytic=analytic,analytic_scope='Small-effect numerical equivalence, not an exact universal waveform identity' if analytic else None,
          scope='220 comparison with identical free-440 nuisance priors in each hypothesis; pyRing is secondary model robustness'))
if len(rows)!=60 or len({(r['dataset'],r['reading']) for r in rows})!=60:raise ValueError('Incomplete table')
for r in rows:
    r['nonblind']=True
    r['source_conditional_verdict']=r['verdict']
    r['physical_status']='INCONCLUSIVE_SYSTEMATICS__NO_PHYSICAL_CONFIRMATION'
    r['z_scope']='Gaussian diagnostic (observed median-based center minus conditional prediction)/stated sigma; not calibrated significance, and never converted from lnB'
    if r['reading']=='R-GLOBAL':
        r['result_type']='RELATIONAL_IDENTITY_IN_DECLARED_IMPLEMENTATION'
        r['analytic_scope']='Global common phase cancels by construction in the chosen relational observable; not a universal physical conclusion'
    elif r['reading'] in ('R-PROP','R-RAIZ-COHERENT'):
        r['result_type']='CONDITIONAL_NUMERICAL_EQUIVALENCE__PHYSICAL_MAPPING_OPEN'
        r['analytic_scope']='Zero is a declared small-effect scenario only; physical mapping remains OPEN'
    elif r['analytic']:
        r['result_type']='CONDITIONAL_NUMERICAL_EQUIVALENCE__BELOW_RESOLUTION'
        r['analytic_scope']='Planck-scale effect represented as zero at the diagnostic resolution; not an exact waveform identity'
    else:r['result_type']='COMPUTED_CONDITIONAL_DENSITY'
opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
doc=dict(status='NONBLIND_CONDITIONAL_COMPARISON__INCONCLUSIVE_SYSTEMATICS',utc=datetime.now(timezone.utc).isoformat(),opening_sha256=sha(opening),supersedes='bis/F2_ALL_READING_TABLES.json',supersedes_sha256=sha(ROOT/'bis/F2_ALL_READING_TABLES.json'),source_sha256=sources,code_sha256=sha(Path(__file__)),rows=rows,
 limitations=['No lnB converted to sigma','No repeated events multiplied between datasets','No new posterior or PE','Analytical zero is a declared numerical small-effect scenario, with physical mapping still open','pyRing sigma explicitly quantile-derived because source JSON lacks sample SD'],positive_medians_31=sum(e['quantiles']['dtau220'][1]>0 for e in cat['rows'] if e['event'] in comb['selected_events']))
new('bis/F2_ALL_READING_TABLES_v2.json',(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
columns=['dataset','reading','lnB','lnB_bandwidth_min','lnB_bandwidth_max','delta_L_weighted','sigma','z','correction_over_sigma','GR_HPD','verdict','sigma_scope','analytic','analytic_scope','scope','nonblind','physical_status','z_scope','source_conditional_verdict','result_type','reason','companion_json','companion_json_sha256']
for r in rows:
    r['companion_json']='F2_ALL_READING_TABLES_v2.json';r['companion_json_sha256']=sha(ROOT/'bis/F2_ALL_READING_TABLES_v2.json')
buf=io.StringIO();writer=csv.DictWriter(buf,fieldnames=columns,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
new('bis/F2_ALL_READING_TABLES_v2.csv',buf.getvalue().encode())
for r in rows:
    if r['dataset']=='GWTC5_31' and r['reading'] in ['R-B','R-LIN']:print(r)
