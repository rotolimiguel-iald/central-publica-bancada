"""Sparse support at posterior quantiles; no full density grid rerun."""
from f2_light_checks import R,get,need,density,put,sha
import json,math
import numpy as np
import h5py
from pathlib import Path
p=R/'bis/c1_review/f2_support_results.json';need(not p.exists(),'Output exists')
source=R/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
with h5py.File(source,'r') as h:s=h['pSEOBNRv5PHM/posterior_samples'][()]
spin=s['final_spin_non_evolved'];x=np.vstack([s['domega220'],s['dtau220']])
b=7.2973525693e-3*math.sqrt(math.e);wr=1.5251-1.1568*(1-spin)**.1292;Q=.7+1.4187*(1-spin)**(-.499);xb=b*wr*Q
rows=[]
for curve in get('bis/F2_FREE_CLOCK_EXTENDED.json')['curves']:
    bw=curve['bandwidth_multiplier'];posterior=next(z for z in curve['conditional_posteriors'] if z['ceiling_in_tM']==20)
    for point in [5.,8.,posterior['q_quantiles']['0.95']]:
        shift=-point*xb/(1+point*xb);moved=x.copy();moved[1]-=shift
        val,ess=density(moved,bw)
        rows.append(dict(bandwidth=bw,q=point,ESS_shifted=ess,ESS_100_pass=ess>=100,is_q95_L20=point==posterior['q_quantiles']['0.95']))
result=dict(source_sha256=sha(source),curve_sha256=sha(R/'bis/F2_FREE_CLOCK_EXTENDED.json'),script_sha256=sha(Path(__file__)),support=rows)
put(p,(json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
