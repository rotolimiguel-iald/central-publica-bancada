"""Independent scalar algebra/coverage check using stdlib, not the producer."""
from pathlib import Path
import json,hashlib,math,statistics
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=B/'bis/e0_core/DATASET.json';d=json.loads(p.read_bytes());c=json.loads((B/'bis/e0_core/E0_CORE.json').read_bytes());idx={r['product_id']:r for r in d['rows']}
if sha(p)!=c['dataset_sha256']:raise ValueError('Dataset changed')
factor=(5+statistics.NormalDist().inv_cdf(.9))**2/25
maxrel=0.;checks=0;summary=[]
for name,ids in d['sets'].items():
    if len(ids)!=len(set(ids)) or len(ids)!=len({idx[i]['event'] for i in ids}):raise ValueError('Duplicate')
    rows=[idx[i] for i in ids]
    for mode in ['std_ddof1','sigma_q90']:
        w=[1/r['stats']['dtau'][mode]**2 for r in rows];I=math.fsum(w)
        center=math.fsum(ww*r['median_dtau'] for ww,r in zip(w,rows))/I
        for reading,r in c['combinations'][name][mode].items():
            if reading=='GR_FALSE_FALSIFIER':continue
            delta=[x['predictions'][reading]['delta_tau'] for x in rows]
            if delta[0] is None:
                if r['z_comb'] is not None:raise ValueError('OPEN coerced to zero')
                continue
            avg=math.fsum(ww*x for ww,x in zip(w,delta))/I
            Q=math.fsum(ww*x*x for ww,x in zip(w,delta));slope=math.fsum(ww*(x-avg)**2 for ww,x in zip(w,delta));N=len(rows)
            expect=dict(I_tau_current=I,delta_weighted=avg,z_comb=math.sqrt(Q),z_slope=math.sqrt(slope),N50=25*N/Q if Q else None,N90=25*N/Q*factor if Q else None,I_tau_target90=25*factor*I/Q if Q else None,N_spurious50_median=25*N/((center-avg)**2*I) if center!=avg else None)
            for key,value in expect.items():
                if value is None:
                    if r[key] is not None:raise ValueError('Null changed')
                elif not math.isclose(value,r[key],rel_tol=1e-11,abs_tol=1e-14):raise ValueError((name,mode,reading,key,value,r[key]))
                elif value: maxrel=max(maxrel,abs(value-r[key])/abs(value))
                checks+=1
            if mode=='std_ddof1' and reading in ['R-B','R-MOD','R-RAIZ-0','R-LIN']:
                summary.append(dict(population=name,reading=reading,z_comb=r['z_comb'],N50=r['N50'],N90=r['N90'],I90=r['I_tau_target90'],N_spurious50=r['N_spurious50_median'],z_slope=r['z_slope']))
mc=json.loads((B/'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes());errs=[]
for r in mc['per_event']:
    other=idx['GWTC5:'+r['event']]
    for key,target in [('sigma_df','stddf'),('sigma_tau','stdtau')]:
        e=abs(r[key]-other[target]);errs.append(e)
        if not math.isclose(r[key],other[target],rel_tol=1e-12):raise ValueError('Independent width discrepancy')
out=dict(status='SCALAR_ALGEBRA_AND_INDEPENDENT_WIDTHS_VERIFIED__NOT_FULL_E0_ACCEPTANCE',utc=datetime.now(timezone.utc).isoformat(),dataset_sha256=sha(p),core_sha256=sha(B/'bis/e0_core/E0_CORE.json'),checks=checks,max_relative_error=maxrel,max_independent_width_difference=max(errs),factor=factor,summary=summary,unpaid=['Systematic component magnitudes are inherited from management JSON; recompute from existing bench artifacts before asserting independent E0 matrix','Quality/SNR fit and live catalog metadata pending','Subresolution gigantic N should be transported as inaccessible analytic ceilings, not meaningful operational targets','Full-posterior nuisance is E1, not the median-WLS entries here'],code_sha256=sha(Path(__file__)))
target=B/'bis/E0_CORE_SCALAR_REVIEW.json'
with target.open('xb') as f:f.write((json.dumps(out,indent=2)+'\n').encode())
print(json.dumps(dict(checks=checks,max_relative_error=maxrel,width_difference=max(errs),summary=summary),indent=2))
