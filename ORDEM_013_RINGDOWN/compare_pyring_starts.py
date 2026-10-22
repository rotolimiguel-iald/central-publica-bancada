"""Compare released GR remnant posteriors, keeping model differences explicit."""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    release=ROOT/'cache/public/17018009'
    receipt=json.loads((release/'extraction_receipt.json').read_bytes())
    ours=json.loads((ROOT/'C6_RESULTS.json').read_bytes())
    rows=[]
    for item in receipt['files']:
        match=re.search(r'CustomPSDs_Kerr_(220|221)_(6|8|10|12)M_weighted_posterior/Nested_sampler/posterior.dat$',item['member'])
        if not match:continue
        path=release/'selected'/item['path'].replace('\\','/').split('/')[-1]
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Released posterior changed')
        samples=np.genfromtxt(path,names=True)
        if any('weight' in k.lower() for k in samples.dtype.names):raise ValueError('Explicit weights require weighted quantiles')
        start=float(match[2]);model=match[1]
        ref=next(r for r in ours['results'] if r['start_tM']==start and r['reading']=='R-GLOBAL' and abs(r['amplitude_prior_sd_strain']-1e-20)<1e-30)
        rows.append(dict(start_tM=start,release_model='Fundamental 220' if model=='220' else 'Fundamental 220 plus first overtone 221',
            samples=len(samples),source_sha256=item['sha256'],member=item['member'],
            mass_detector_05_50_95=np.quantile(samples['Mf'],[.05,.5,.95]).tolist(),
            spin_05_50_95=np.quantile(samples['af'],[.05,.5,.95]).tolist(),
            this_220_440_mass_05_50_95=ref['mass_05_50_95'],this_220_440_spin_05_50_95=ref['spin_05_50_95']))
    if len(rows)!=8:raise ValueError('Expected four available starts for two released models')
    output=dict(status='RELEASED_START_TIME_CONTROLS_READ',results=rows,
        no_10_5M_release_posterior=True,
        differences=['Released Kerr220/221 uses H1 trigger 1420878141.2190118; this registered TEOB-based reference is 1420878141.2189023, difference 0.0001095 s',
            'Released 4096 Hz bandpassed external-PSD strain; this analysis uses exact stride-2 selection and polynomial quotient with independently measured PSD',
            'Released angular/amplitude priors and mode set differ from independent-detector 220+440 amplitude quadratures; this is a comparison, not a claimed reproduction',
            'Equal-weight interpretation of released posterior.dat; original nested-chain merging provenance remains a documented limitation'],
        not_independent='All refer to GW250114; neither different starts nor different inference pipelines supply independent evidence')
    atomic_json(ROOT/'C6_PYRING_START_COMPARISON.json',output)
    print(json.dumps(rows),flush=True)

if __name__=='__main__':main()
