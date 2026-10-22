"""Focused independent review of the covariance API repair, no real data."""
from pathlib import Path
from datetime import datetime,timezone
import sys,math,json
sys.dont_write_bytecode=True
from audit_provenance import OUT,atomic,metadata
import numpy as np
P=OUT.parent/'covariance_support';checks=[];sources=[]
def meta(p):
 m,b=metadata(p);sources.append(m);return m,b
def read(p):return json.loads(meta(p)[1])
def check(name,ok,detail=None):checks.append({'name':name,'passed':bool(ok),'detail':detail})
pr=read(OUT/'REVISAO_SUPORTE_H0DN_V2_PROTOCOL.json')
assert metadata(OUT/'covariance_support_v2_under_review.py')[0]['sha256']==pr['source']['sha256']==metadata(P/'singular_gaussian_v2.py')[0]['sha256']
from covariance_support_v2_under_review import SupportGaussian as G,gaussian_prior_marginal as marginal
old=read(OUT/'REVISAO_SUPORTE_H0DN.json')
for name in ['singular_gaussian.py','PROTOCOL_V1.json','PROTOCOL_FREEZE.json','RESULT.json','MANIFESTO.json']:
 before=next(x for x in old['sources'] if x['path']==str(P/name));now,_=meta(P/name);check('initial artifact unchanged '+name,now['sha256']==before['sha256'] and now['bytes']==before['bytes'])
freeze=read(P/'FREEZE_V2.json');result=read(P/'RESULT_V2.json')
for row in freeze['files']:
 m,_=meta(Path(row['path']));check('V2 freeze pin '+Path(row['path']).name,m['sha256']==row['sha256'] and m['bytes']==row['bytes'])
check('37 new controls recorded',len(result['checks'])==result['passed']==37 and all(x['passed'] for x in result['checks']) and result['freeze']==freeze)
for key,value in [('support_tolerance',math.inf),('absolute_cutoff',math.nan),('absolute_cutoff',math.inf),('relative_cutoff',math.inf)]:
 try:G.from_covariance(np.ones((2,2)),**{key:value});check('fixed nonfinite '+key+' '+str(value),False)
 except ValueError as e:check('fixed nonfinite '+key+' '+str(value),True,str(e))
try:marginal([1.],[0.,0.],np.eye(2),np.eye(2),[0.,0.],np.eye(2));check('fixed short data broadcasting',False)
except ValueError as e:check('fixed short data broadcasting',True,str(e))
x=marginal([.2,.7],[0.,-.1],[[1.,0.],[0.,0.]],[[0.],[2.]],[.3],[[.25]])
check('support expansion remains normalized',x['rank']==2 and abs(x['log_density']+math.log(2*math.pi)+.04)<1e-11,x)
B=np.array([[1.,0.],[0.,1.],[2.,-1.]]);V=np.array([[2.,.3],[.3,.7]]);z=np.array([.4,-.2]);x=G.from_covariance(B@V@B.T).evaluate(B@z)
expected=-.5*(2*math.log(2*math.pi)+np.linalg.slogdet(V)[1]+np.linalg.slogdet(B.T@B)[1]+z@np.linalg.solve(V,z))
check('nonorthogonal normalization remains correct',x['support_ok'] and abs(x['log_density']-expected)<1e-11,{'actual':x['log_density'],'expected':float(expected)})
meta(OUT/'review_support_h0dn_v2.py')
record={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'INDEPENDENT_REPAIR_DELTA_ONLY_SYNTHETIC','checks':checks,'all_pass':all(x['passed'] for x in checks),'passed':sum(x['passed'] for x in checks),'sources':sources,'findings_resolution':{'H0DN-01':'RESOLVED_IN_PINNED_V2','H0DN-02':'RESOLVED_IN_PINNED_V2'},'real_data_opened':False,'author_original_executed':False,'copied_helper_executed':True,'V1_ratified':False}
atomic(OUT/'REVISAO_SUPORTE_H0DN_V2.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':record['all_pass'],'source':pr['source'],'failures':[x for x in checks if not x['passed']]}))
