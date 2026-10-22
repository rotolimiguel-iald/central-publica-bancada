"""Independent exact KDE fits of GR and R-B; no producer imports or new PE."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,time,ast
import numpy as np,h5py
from scipy.optimize import minimize
from scipy.special import logsumexp
B=Path(__file__).resolve().parents[1];R=B.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((B/n).read_bytes())
def main():
    start=time.perf_counter();resultfile=B/'bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json'
    result=json.loads(resultfile.read_bytes());data=read('bis/e0_core/DATASET.json');arrays={};sources={}
    tree=ast.parse((B/'tgl_ringdown_prediction.py').read_text(encoding='utf-8'))
    alpha=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ALPHA_FINE_CODATA_2018' for t in n.targets))
    beta=alpha*math.sqrt(math.e)
    for row in data['rows']:
        if row['product_id'] not in data['sets']['GWTC5_33']:continue
        p=R/row['source_path']
        if sha(p)!=row['source_sha256']:raise ValueError('Posterior source changed')
        with h5py.File(p,'r') as h:
            v=h[row['dataset']].fields([row['field_mapping']['dtau'],row['field_mapping']['spin']])[:]
        tau=np.asarray(v[row['field_mapping']['dtau']],dtype=float);spin=np.asarray(v[row['field_mapping']['spin']],dtype=float)
        omega=1.5251-1.1568*np.power(1-spin,.1292);Q=.7+1.4187*np.power(1-spin,-.499)
        x=beta*omega*Q;delta=-x/(1+x)
        key=row['product_id'];arrays[key]={'GR':tau,'R-B':tau-delta}
        want=result['events'][key]['predictions']['R-B']['mean']
        if not math.isclose(float(delta.mean()),want,rel_tol=1e-12,abs_tol=1e-14):raise ValueError('R-B samplewise reduction differs')
        sources[row['source_path']]=row['source_sha256']
    checks=[]
    for pop in ['GWTC5_31','GWTC5_33']:
      ids=data['sets'][pop]
      for reading in ['GR','R-B']:
        us=[arrays[i][reading] for i in ids]
        hs=[float(u.std(ddof=1)*len(u)**(-.2)) for u in us]
        for covariate in ['sigma','inverse_SNR']:
          xx=np.array([result['events'][i]['sigma_dtau_ddof1'] if covariate=='sigma' else 40/result['events'][i]['metadata']['network_matched_filter_snr'] for i in ids])
          center=xx.mean();scale=xx.std();X=np.column_stack([np.ones(len(xx)),(xx-center)/scale]);T=np.array([[1.,-center/scale],[0,1/scale]])
          def calc(z):
            points=X@z;lp=[];grad=[]
            for p,u,h in zip(points,us,hs):
              t=(u-p)/h;v=-.5*t*t;norm=logsumexp(v);ww=np.exp(v-norm)
              lp.append(norm-math.log(len(u)*h*math.sqrt(2*math.pi)));grad.append(float(ww@t)/h)
            return -float(sum(lp)),-(X.T@np.array(grad))
          y=np.array([u.mean() for u in us]);w=1/np.array([u.var(ddof=1) for u in us])
          initial=np.linalg.solve(X.T@(w[:,None]*X),X.T@(w*y))
          opt=minimize(calc,initial,jac=True,method='BFGS',options={'gtol':1e-7,'maxiter':100})
          value,g=calc(opt.x)
          if np.max(np.abs(g))>1e-4:raise ValueError('Exact optimizer nonstationary')
          step=1e-5;H=np.column_stack([(calc(opt.x+np.eye(2)[j]*step)[1]-calc(opt.x-np.eye(2)[j]*step)[1])/(2*step) for j in range(2)])
          V=T@np.linalg.inv(H)@T.T;params=T@opt.x
          f=next(f['result'] for f in result['fits'] if f['group']==pop and f['reading']==reading and f['covariate']==covariate and f['bandwidth_factor']==1)
          dist=np.sqrt((params-np.array([f['c0'],f['k']]))@np.linalg.solve(np.array(f['covariance']),params-np.array([f['c0'],f['k']])))
          covrelative=float(np.max(np.abs(V-np.array(f['covariance']))/np.maximum(np.abs(V),1e-10)))
          if dist>.01 or covrelative>.005:raise ValueError('Exact direct fit differs materially')
          checks.append({'population':pop,'reading':reading,'covariate':covariate,'exact_parameters':params.tolist(),
            'finite_difference_covariance':V.tolist(),'parameter_distance_in_local_metric':float(dist),
            'max_relative_covariance_difference':covrelative,'log_density_difference':-value-f['conditional_log_density'],
            'optimizer_reported_success':bool(opt.success),'max_abs_gradient':float(np.max(np.abs(g)))})
    output={'status':'PASS_INDEPENDENT_DIRECT_KDE_GR_RB__CONDITIONAL_ONLY','utc':datetime.now(timezone.utc).isoformat(),
      'result_sha256':sha(resultfile),'code_sha256':sha(Path(__file__)),'checks':checks,'source_hashes':sources,
      'sample_count':sum(len(v['GR']) for v in arrays.values()),'wall_seconds':time.perf_counter()-start,
      'scope':['Exact fullsample log-sum-exp KDE, no FFT or producer import','Independent samplewise R-B dimensionless reduction x=beta*omegaM*Q','BFGS from Gaussian-moment seed; Hessian by numerical differentiation of direct gradient','Only GR/R-B nominal bandwidth, two populations/two covariates; other readings/source-statutes separately reviewed','Selection/priors/model-systematic calibration not established; no physical sigma or Bayes factor']}
    with (B/'bis/E1_DIRECT_KDE_REVIEW.json').open('x',encoding='utf-8') as f:json.dump(output,f,indent=2,allow_nan=False)
    print(json.dumps({'status':output['status'],'checks':len(checks),'wall_seconds':output['wall_seconds'],'max_local_distance':max(c['parameter_distance_in_local_metric'] for c in checks)}))
if __name__=='__main__':main()
