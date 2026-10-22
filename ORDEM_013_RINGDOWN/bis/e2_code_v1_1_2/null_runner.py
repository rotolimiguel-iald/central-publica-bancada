"""Run only the synthetic null cells fixed by the E2 tunnel witness.

This does not open HDF5, fit physical nuisance, or accept an event into the test.
"""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k]='1'
import argparse,json,time,math,re
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm,chi2
from registration_guard import BASE,contained,checked_registration,time_guard,sha,publish_new,new_null_cells
from synthetic_null import projected_components,simulate_projection
from route_iv_null import run_null


def create(path,data):
    raw=(json.dumps(data,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>25_000_000:raise ValueError('Unexpectedly large null receipt')
    publish_new(path,data)


def projection_inputs(reg,cell):
    dataset=json.loads(contained(reg['nulls']['dataset_relative_to_Chatgpt']).read_bytes())
    nuisance=json.loads(contained(reg['nulls']['nuisance_relative_to_Chatgpt']).read_bytes())
    lookup={r['product_id']:r for r in dataset['rows']}
    rows=[lookup[k] for k in dataset['sets'][cell['population']]]
    if len(set(r['event'] for r in rows))!=len(rows):raise ValueError('Duplicate event in synthetic population')
    N=cell['N_target_balanced_catalog']
    if type(N) is not int or not 2<=N<=1_000_000 or not rows:raise ValueError('Invalid prospective catalog size')
    if any(r['predictions'].get(cell['reading'],{}).get('delta_tau') is None for r in rows):raise ValueError('Open prediction is not a null template')
    indices=np.arange(N)%len(rows)
    # Deterministic balanced catalog: original order cycles; no selection by width.
    delta=np.array([r['predictions'][cell['reading']]['delta_tau'] for r in rows])[indices]
    sigma=np.array([r['stats']['dtau']['std_ddof1'] for r in rows])[indices]
    X=np.column_stack((np.ones(N),sigma))
    variant=cell['nuisance_covariance_variant']
    if variant=='zero':V=np.zeros((2,2))
    elif variant=='kde_0.7':
        matches=[f for f in nuisance['conditional_diagnostics']['fits'] if f['reading']=='GR' and f['group']==cell['population'] and f['bandwidth_factor']==0.7 and f['covariate']=='sigma']
        if len(matches)!=1:raise ValueError('Missing/ambiguous KDE covariance')
        V=matches[0]['result']['covariance']
    elif variant=='WLS_q90':
        V=nuisance['conditional_diagnostics']['management_WLS_controls'][cell['population']]['median_q90_1.6449']['covariance']
    else:raise ValueError('Unregistered nuisance covariance variant')
    components=projected_components(delta,sigma,X,V)
    components.update(nuisance_covariance_variant=variant,nuisance_covariance_used=np.asarray(V).tolist())
    components.update(N=N,source_events=len(rows),
      nuisance_mean_subtracted=nuisance['synthetic_E2_nuisance_INPUT']['sigma_model']['mean_c0_k'],
      mean_handling='r = y - X*m; covariance V is fixed local E1 INPUT, not calibrated physical uncertainty',
      target_source='ceil(E0 N90 fixed-effect mixture); not 90% power guaranteed after adding nuisance')
    return components


def analytic_tail(components,model):
    if model=='gaussian':return {'p':float(norm.sf(5)),'method':'exact normal projection'}
    a=components['noise_variance_fraction'];b=components['nuisance_variance_fraction']
    # Conditional on U~chi2_5 the projection is normal, variance 3*a/U+b.
    value,err=quad(lambda u: norm.sf(5/math.sqrt(3*a/u+b))*chi2.pdf(u,5),0,np.inf,epsabs=1e-12,epsrel=1e-9,limit=200)
    return {'p':float(value),'quadrature_absolute_error_estimate':float(err),
      'method':'chi2_5 integral of conditional normal tail; measurement shared t5 scale plus Gaussian nuisance'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--cell',required=True);args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]{1,120}',args.cell):raise ValueError('Unsafe cell identifier')
    reg,digest=checked_registration();cells=new_null_cells(reg)
    if args.cell not in cells:raise ValueError('Unregistered null cell')
    cell=cells[args.cell];out=BASE/'bis'/('RESULT_E2_NULL_'+args.cell+'.json')
    failure=BASE/'bis'/('RESULT_E2_NULL_'+args.cell+'_FAILURE.json')
    if out.exists() or failure.exists():raise FileExistsError('Null cell already attempted; no silent retries')
    utc=datetime.now(timezone.utc).isoformat();wall=time.perf_counter();cpu=time.process_time()
    guard=lambda:time_guard(reg)
    try:
        if cell['kind']=='matched_projection':
            comp=projection_inputs(reg,cell)
            result=simulate_projection(comp,cell['draws'],cell['seed'],cell['model'],guard,cell['chunk'])
            result['analytic_tail_control']=analytic_tail(comp,cell['model'])
        elif cell['kind']=='route_IV':
            pins={k.split('ORDEM_013_RINGDOWN/',1)[1]:v for k,v in reg['input_pins_relative_to_Chatgpt'].items() if k.startswith('ORDEM_013_RINGDOWN/')}
            result=run_null(cell['population'],cell['N_target'],cell['draws'],cell['seed'],cell['sigma_sys_INPUT'],pins,guard,cell['chunk'])
        else:raise ValueError('Unknown cell kind')
        guard()
        receipt={'status':'SYNTHETIC_NULL_COMPLETED__NOT_PHYSICAL_CALIBRATION','registration_sha256':digest,
          'cell_id':args.cell,'cell':cell,'started_utc':utc,'finished_utc':datetime.now(timezone.utc).isoformat(),
          'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,'result':result,
          'familywise':'Per-cell intervals; no multiplicity-adjusted discovery from these controls',
          'physical_test_gate':'INCONCLUSIVE_SYSTEMATICS','null_runner_sha256':sha(Path(__file__))}
        create(out,receipt)
        print(json.dumps({'status':receipt['status'],'cell':args.cell,'wall_seconds':receipt['wall_seconds'],'sha256':sha(out)}))
    except Exception as e:
        create(failure,{'status':'FAILED_NO_TAIL_RESULT','registration_sha256':digest,'cell_id':args.cell,
          'started_utc':utc,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-wall,
          'exception_type':type(e).__name__,'exception':str(e)})
        raise


if __name__=='__main__':main()
