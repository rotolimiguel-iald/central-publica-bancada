"""Audit completed frozen null receipts; descriptive checks never become a discovery."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,math
import numpy as np
from scipy.stats import binom,norm
B=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(B/'bis/e2_code'))
from registration_guard import checked_registration,sha,publish_new

def main():
    reg,digest=checked_registration();campaign_path=B/'bis/RESULT_E2_NULL_CAMPAIGN.json'
    campaign=json.loads(campaign_path.read_bytes())
    if campaign['registration_sha256']!=digest or campaign['failed'] is not None:
        raise ValueError('Incomplete or mismatched campaign; retain failure, no complete audit')
    registered=reg['nulls']['cells'];completed={r['cell']:r for r in campaign['completed']}
    if set(completed)!=set(registered) or len(campaign['completed'])!=len(registered):raise ValueError('Cell coverage differs')
    rows=[]
    for name,cell in registered.items():
        path=B/'bis'/('RESULT_E2_NULL_'+name+'.json');entry=json.loads(path.read_bytes());r=entry['result']
        if sha(path)!=completed[name]['result_sha256'] or entry['registration_sha256']!=digest or entry['cell']!=cell:
            raise ValueError('Changed null receipt')
        k=r['false_positives'];n=r['draws']
        if type(k) is not int or type(n) is not int or n!=cell['draws'] or not 0<=k<=n:raise ValueError('Invalid counts')
        if r['empirical_p']!=k/n:raise ValueError('Empirical ratio differs')
        # Independent CDF identities for the Clopper-Pearson endpoints.
        upper=r['one_sided_upper'];lo,hi=r['central_interval']
        checks=[]
        if k<n:checks.extend([math.isclose(float(binom.cdf(k,n,upper)),.05,rel_tol=1e-6,abs_tol=1e-9),
                            math.isclose(float(binom.cdf(k,n,hi)),.025,rel_tol=1e-6,abs_tol=1e-9)])
        if k>0:checks.append(math.isclose(float(binom.sf(k-1,n,lo)),.025,rel_tol=1e-6,abs_tol=1e-9))
        if not all(checks):raise ValueError('Binomial interval inversion failed: '+name)
        analytic=r.get('analytic_tail_control',{}).get('p')
        rows.append({'cell':name,'kind':cell['kind'],'population':cell['population'],
          'reading':cell.get('reading'),'model':cell.get('model'),'draws':n,'false_positives':k,
          'empirical_p':k/n,'one_sided_upper95':upper,'central95':[lo,hi],
          'analytic_p':analytic,'analytic_inside_pointwise95':None if analytic is None else lo<=analytic<=hi,
          'analytic_expected_false_positives':None if analytic is None else n*analytic,
          'normal_tail_equivalent_of_upper_bound_DESCRIPTIVE':float(norm.isf(upper)),
          'mean':r.get('mean'),'variance_ddof1':r.get('variance_ddof1'),
          'components':r.get('components'),'max_LRT':r.get('max_LRT'),
          'result_sha256':sha(path),'wall_seconds':entry['wall_seconds'],'cpu_seconds':entry['cpu_seconds']})
    value={'status':'RECEIPTS_AND_BINOMIAL_ENDPOINTS_VERIFIED__SYNTHETIC_ONLY',
      'registration_sha256':digest,'campaign_sha256':sha(campaign_path),
      'created_utc':datetime.now(timezone.utc).isoformat(),'cells':rows,
      'total_draws':sum(r['draws'] for r in rows),'campaign_wall_seconds':campaign['wall_seconds'],
      'sum_cell_cpu_seconds':sum(r['cpu_seconds'] for r in rows),
      'interpretation':'Pointwise 95% intervals may miss analytic p by chance across 25 cells; this audit does not select cells, alter thresholds, rerun a null or create a physical significance. IV zero counts give an upper limit, never p=0. E1 covariance is conditional INPUT.',
      'physical_gate':'INCONCLUSIVE_SYSTEMATICS','physical_5sigma_paid':False,
      'script_sha256':sha(Path(__file__))}
    out=B/'bis/E2_NULL_RECEIPTS_AUDIT_V1.json';publish_new(out,value)
    print(json.dumps({'status':value['status'],'sha256':sha(out),'total_draws':value['total_draws'],'cells':len(rows)}))

if __name__=='__main__':main()
