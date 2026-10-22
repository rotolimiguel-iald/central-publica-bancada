"""Independent controls frozen in REVISAO_SUPORTE_H0DN_PROTOCOL; no real-data loader."""
from pathlib import Path
from datetime import datetime,timezone
import sys,math,json,hashlib,ast
sys.dont_write_bytecode=True
import numpy as np
from scipy.integrate import quad
from audit_provenance import OUT,atomic,metadata
ROOT=OUT.parent;S=ROOT/'covariance_support';checks=[];sources={}
def meta(p):
 m,b=metadata(p);sources[str(p)]=m;return m,b
def read(p):return json.loads(meta(p)[1])
def check(name,ok,detail=None,kind='analytical'):checks.append({'name':name,'passed':bool(ok),'kind':kind,'detail':detail})
def close(x,y):return bool(np.allclose(x,y,rtol=1e-11,atol=1e-11))
p=read(OUT/'REVISAO_SUPORTE_H0DN_PROTOCOL.json')
assert metadata(OUT/'covariance_support_under_review.py')[0]['sha256']==p['source']['sha256']==metadata(S/'singular_gaussian.py')[0]['sha256']
from covariance_support_under_review import SupportGaussian,gaussian_prior_marginal
manifest=read(S/'MANIFESTO.json')
for row in manifest['files']:
 f=Path(row['path']);assert f.resolve().is_relative_to(S.resolve());m,b=meta(f)
 check('pin '+f.name,m['sha256']==row['sha256'] and m['bytes']==row['bytes'],kind='identity')
result=read(S/'RESULT.json');freeze=read(S/'PROTOCOL_FREEZE.json');proto=read(S/'PROTOCOL_V1.json')
check('existing 18 controls recorded',len(result['checks'])==result['passed']==18 and all(x['passed'] for x in result['checks']),kind='recorded')
check('protocol freeze identity',freeze['protocol']==result['protocol'] and result['protocol']['sha256']==metadata(S/'PROTOCOL_V1.json')[0]['sha256'],kind='identity')
for row in result['scripts']:
 m,_=meta(Path(row['path']));check('execution pin '+Path(row['path']).name,m['sha256']==row['sha256'] and m['bytes']==row['bytes'],kind='identity')
B=np.array([[1.,0.],[0.,1.],[2.,-1.]]);V=np.array([[2.,.3],[.3,.7]]);z=np.array([.4,-.2]);C=B@V@B.T
g=SupportGaussian.from_covariance(C);v=g.evaluate(B@z);chi=float(z@np.linalg.solve(V,z));logdet=float(np.linalg.slogdet(V)[1]);logJ=.5*float(np.linalg.slogdet(B.T@B)[1]);expected=-.5*(2*math.log(2*math.pi)+logdet+chi)-logJ
check('redundant normalization includes Hausdorff Jacobian',close(v['log_density'],expected) and close(v['chi2_pseudoinverse'],chi) and v['rank']==2 and v['support_ok'],{'actual':v,'expected_log_density':expected,'log_volume_J':logJ})
full=SupportGaussian.from_covariance(V).evaluate(z);L=np.linalg.cholesky(V);w=np.linalg.solve(L,z);expected_full=-math.log(2*math.pi)-float(np.log(np.diag(L)).sum())-.5*float(w@w)
check('SPD absolute normalization Cholesky',close(full['log_density'],expected_full),{'actual':full['log_density'],'expected':expected_full})
norm=lambda x,m,v:math.exp(-.5*((x-m)**2/v))/(math.sqrt(2*math.pi*v))
integ,err=quad(lambda x:norm(1.,.1+2*x,.3)*norm(x,.2,.7),-np.inf,np.inf,epsabs=1e-12,epsrel=1e-12)
conv=gaussian_prior_marginal([1.],[.1],[[.3]],[[2.]],[.2],[[.7]])
check('proper Gaussian integral equals normalized quadrature',close(conv['log_density'],math.log(integ)),{'log_convolution':conv['log_density'],'log_quadrature':math.log(integ),'quad_error':err})
expanded=gaussian_prior_marginal([.2,.7],[0.,-.1],[[1.,0.],[0.,0.]],[[0.],[2.]],[.3],[[.25]])
check('proper prior expands singular support',expanded['rank']==2 and close(expanded['log_density'],-math.log(2*math.pi)-.04),expanded)
dirac=gaussian_prior_marginal([1.],[.1],[[.3]],[[2.]],[.2],[[0.]])
check('degenerate prior is proper Dirac probability',close(dirac['log_density'],math.log(norm(1.,.5,.3))),dirac)
# Explicit negative API controls: a successful return is a defect, even if arithmetic is finite.
for key,value in [('support_tolerance',math.inf),('absolute_cutoff',math.nan),('absolute_cutoff',math.inf),('relative_cutoff',math.inf)]:
 try:
  x=SupportGaussian.from_covariance(np.ones((2,2)),**{key:value}).evaluate([2.,0.] if key=='support_tolerance' else [0.,0.])
  check('reject nonfinite '+key+' '+str(value),False,x,'API-negative')
 except ValueError as exc:check('reject nonfinite '+key+' '+str(value),True,str(exc),'API-negative')
try:
 x=gaussian_prior_marginal([1.],[0.,0.],np.eye(2),np.eye(2),[0.,0.],np.eye(2))
 check('reject incompatible data dimension',False,x,'API-negative')
except ValueError as exc:check('reject incompatible data dimension',True,str(exc),'API-negative')
ad=read(ROOT/'H0DN_CONTRACT_AMENDMENT.json');meta(ROOT/'H0DN_ADENDO_CONTRATO.md')
lo,hi=ad['prior_transport_proposal']['old_s_prior'];delta=lambda s:-5*math.log10(1+s);inverse=lambda d:10**(-d/5)-1
ends=sorted([delta(lo),delta(hi)]);jac=lambda d:math.log(10)/5*10**(-d/5);dens=lambda d:jac(d)/(hi-lo)
area,error=quad(dens,*ends,epsabs=1e-12,epsrel=1e-12)
check('delta endpoints order and sign',close(ends,ad['prior_transport_proposal']['delta_C_endpoints_magnitude']) and delta(.1)<0<delta(-.1),ends)
check('delta inverse monotone',all(close(inverse(delta(s)),s) for s in [lo,-.07,0.,.04,hi]))
check('uniform-s transported prior normalized',close(area,1.),{'integral':area,'quad_error':error,'density_not_uniform':not close(dens(ends[0]),dens(ends[1]))})
step=1e-6;deriv=(delta(step)-delta(-step))/(2*step)
check('delta derivative and correction sign',close(deriv,-5/math.log(10)),{'finite_difference':deriv,'exact':-5/math.log(10),'apparent_H_increases_when_delta_decreases':True})
# Synthetic design: h column [0,1,1] differs from all-lines shift [1,1,1].
A=np.array([[1.,0.],[0.,1.],[1.,1.]]);hcol=A[:,1];dh=.02
check('universal response uses h column',np.array_equal(A@np.array([0.,dh]),hcol*dh) and not np.array_equal(hcol,np.ones(3)))
D=ROOT/'h0dn_documentary_review';um=read(D/'UPSTREAM_MANIFEST.json')
for rel in ['h0_constrainer/configs/config.ini','h0_constrainer/h0_constrainer/equations.py']:
 row=next(x for x in um['files'] if x['path']==rel);m,raw=meta(D/'upstream'/rel);git=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 check('archived upstream code pin '+rel,m['sha256']==row['sha256'] and len(raw)==row['bytes'] and git==row['git_blob_sha1'],kind='identity')
config=(D/'upstream/h0_constrainer/configs/config.ini').read_text();eq=(D/'upstream/h0_constrainer/h0_constrainer/equations.py').read_text()
check('baseline JAGB excluded in active config',any(line.startswith('host_exclude_list =') and '*jagb*' in line for line in config.splitlines()),kind='static')
check('upstream h equations', 'coeffs[ieq, ihub] = 1.0' in eq and 'log10(H0) - 0.2*M_0 = a_b + 5' in eq,kind='static')
for rel in ['REVISAO_H0DN_ACT.md','STRUCTURE_AUDIT.json','MANIFESTO_ENTREGA.json']:meta(D/rel)
check('adendum remains proposed',ad['status']=='PROPOSED_NOT_RATIFIED' and ad['no_new_fit'] and ad['no_change_to_frozen_V1'],kind='scope')
meta(OUT/'review_support_h0dn.py');meta(OUT/'covariance_support_under_review.py')
record={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'SYNTHETIC_ANALYTICAL_AND_API_REVIEW_NO_REAL_DATA_FIT_OR_V1_APPROVAL','protocol':metadata(OUT/'REVISAO_SUPORTE_H0DN_PROTOCOL.json')[0],'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'findings':[x for x in checks if not x['passed']],'sources':list(sources.values()),'numpy':np.__version__,'D_opened':False,'upstream_executed':False,'author_original_executed':False,'copied_density_helper_executed':True}
# NaN/inf are serialized explicitly as strings for faithful, portable failure evidence.
def sanitize(x):
 if isinstance(x,float) and not math.isfinite(x):return str(x)
 if isinstance(x,dict):return {k:sanitize(v) for k,v in x.items()}
 if isinstance(x,list):return [sanitize(v) for v in x]
 return x
atomic(OUT/'REVISAO_SUPORTE_H0DN.json',json.dumps(sanitize(record),ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps(sanitize({'passed':record['passed'],'total':len(checks),'findings':record['findings'],'sources':len(sources)}),ensure_ascii=False,indent=2))
