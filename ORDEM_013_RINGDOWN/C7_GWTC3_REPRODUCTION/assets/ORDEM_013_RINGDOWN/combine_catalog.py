"""Joint common-deformation GR control and source-declared catalog selection.

Importance sampling integrates the product of per-event KDE densities. This
is a credible-region diagnostic, not a frequentist significance or injection
calibration. Event exclusions are read from the release notebook as literals.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import ast
import hashlib
import json
import math
import h5py
import numpy as np
from scipy.stats import gaussian_kde
from scipy.special import logsumexp
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def literal_selection(path):
    book=json.loads(path.read_bytes());found={}
    for cell in book['cells']:
        source=''.join(cell.get('source',[]))
        if not any(name+' = ' in source for name in ['event_list','event_map']):continue
        for node in ast.parse(source).body:
            if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                name=node.targets[0].id
                if name in ['event_list','event_map']:found[name]=ast.literal_eval(node.value)
    result=[found['event_map'][event] for event in found['event_list']]
    if len(set(result))!=len(result):raise ValueError('Duplicate in source selection')
    return result

def weighted_quantile(x,w):
    order=np.argsort(x);return np.interp([.05,.5,.95],np.cumsum(w[order]),x[order]).tolist()

def main():
    folder=ROOT/'cache/public/21454847/extracted/pSEOB'
    book=folder/'pSEOBNR_main_figure.ipynb';chosen=literal_selection(book)
    catalog=json.loads((ROOT/'C4_CATALOG_220.json').read_bytes())
    if not set(chosen)<=set(r['event'] for r in catalog['rows']):raise ValueError('Selection missing samples')
    schema=json.loads((ROOT/'C4_CATALOG_SCHEMA.json').read_bytes());data={}
    for row in schema['rows']:
        path=folder/'metafiles'/row['filename']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Source changed')
        with h5py.File(path,'r') as h:s=h[row['label']+'/posterior_samples'][()]
        data[row['event']]=np.vstack([s['domega220'],s['dtau220']])
    selections={'release_figure_selection_31':chosen,'all_available_33':list(data)}
    rows=[]
    for bw,N,seed in [(1.,4096,130431),(1.,8192,130432),(.7,4096,130433),(1.4,4096,130434)]:
        densities={key:gaussian_kde(value,bw_method=lambda k:k.scotts_factor()*bw) for key,value in data.items()}
        proposal=densities['GW250114_082203'];points=proposal.resample(N,seed=seed)
        logq=proposal.logpdf(points)
        logdens={};loggr={}
        for key,kde in densities.items():
            logdens[key]=kde.logpdf(points);loggr[key]=float(kde.logpdf([0,0])[0])
        for name,events in selections.items():
            logs=np.sum([logdens[key] for key in events],axis=0)
            gr=sum(loggr[key] for key in events)
            lw=logs-logq;weights=np.exp(lw-logsumexp(lw));ess=1/np.sum(weights*weights)
            indicator=(logs>=gr).astype(float);content=float(weights@indicator)
            se=float(np.sqrt(np.sum(weights**2*(indicator-content)**2)))
            row=dict(selection=name,N_events=len(events),bandwidth=bw,draws=N,seed=seed,
                     importance_ESS=float(ess),GR_HPD_content=content,MC_standard_error=se,
                     GR_inside_95=bool(content+3*se<.95),
                     GR_outside_95=bool(content-3*se>.95),
                     posterior_quantiles={label:weighted_quantile(points[i],weights) for i,label in enumerate(['df220','dtau220'])},
                     lnB_point_density_GR_vs_max_sample=gr-float(max(logs)))
            rows.append(row);print(json.dumps(row),flush=True)
    sums={}
    for name,events in selections.items():
        selected=[row for row in catalog['rows'] if row['event'] in events]
        diagnostics=[r for r in rows if r['selection']==name]
        gr_safe=all(r['GR_inside_95'] and r['importance_ESS']>500 for r in diagnostics)
        gr_out=any(r['GR_outside_95'] for r in diagnostics)
        values=[]
        for reading in [r['reading'] for r in catalog['catalog']]:
            lines=[next(r for r in row['rows'] if r['reading']==reading) for row in selected]
            central=sum(r['lnB'] for r in lines);robust=np.sum([r['lnB_bandwidth'] for r in lines],axis=0)
            supported=all(min(r['support']['kernel_effective_samples'],row['GR_support']['kernel_effective_samples'])>=100 for row,r in zip(selected,lines))
            threshold=bool(np.all(robust<=-math.log(100)))
            if gr_out:verdict='INCONCLUSIVE_SYSTEMATICS'
            elif threshold and gr_safe and supported:verdict='EXCLUDED_IN_READING__CONDITIONAL_SECTOR_ONLY'
            elif not gr_safe:verdict='INCONCLUSIVE_GR_REGION_OR_MC'
            elif not supported:verdict='INCONCLUSIVE_DENSITY_SUPPORT'
            else:verdict='NOT_EXCLUDED'
            values.append(dict(reading=reading,lnB=central,lnB_bandwidth=robust.tolist(),
                    lnB_tau_marginal=sum(r['lnB_tau_marginal'] for r in lines),
                    individual_event_density_support=supported,verdict=verdict))
        sums[name]=values
    atomic_json(ROOT/'C4_CATALOG_COMBINATION.json',dict(status='NONBLIND_CONDITIONAL_220_SECTOR',
       selection_source_sha256=hashlib.sha256(book.read_bytes()).hexdigest(),
       selected_events=chosen,additional_control_events=sorted(set(data)-set(chosen)),
       exclusions_basis='Literal event_list/event_map from primary release; not selected by this analysis results',
       common_deformation_GR_diagnostics=rows,catalog=sums,
       physical_model_caution='GW250114 free440 nuisance; others fixed440. Not full TGL/full GR evidence.',
       unresolved=['Catalog KDE smoothing bias despite bandwidth sensitivity; waveform/strain systematics',
                   'Stochastic trajectory vs ensemble physical map','pyRing crosscheck','Higher-mode physical hypotheses']))
    print(json.dumps(dict(catalog=sums)),flush=True)

if __name__=='__main__':main()
