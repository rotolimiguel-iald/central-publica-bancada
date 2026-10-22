"""Independent GLS and analytic-derivative review of a frozen conditional forecast."""
from pathlib import Path
import json,math,hashlib,datetime,re,io
from audit_provenance import OUT,atomic,metadata
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import cho_factor,cho_solve
BASE=OUT.parent/'derivacoes'/'poder_forma'
records=[];checks=[]
def rec(p,expected=None,role='delivered frozen input'):
 m,b=metadata(p);m['role']=role
 if expected is not None:
  m['matches_expected']=m['sha256']==expected
  assert m['matches_expected'],str(p)
 records.append(m);return b
def check(name,value,detail=None):
 checks.append({'name':name,'passed':bool(value),'detail':detail});assert value,name
manifest=json.loads(rec(BASE/'MANIFESTO_PODER_FORMA.json'))
for f in manifest['files']:
 if f.get('backup') or f['file']=='RECIBO_MAPA_PODER.json':continue
 rec(BASE/f['file'],f['sha256'])
def read(name):return json.loads((BASE/name).read_bytes())
result=read('PODER_FORMA.json');template=read('TEMPLATES_SEM_CENTROS.json');source=read('FONTES_COVARIANCIAS_METADATA.json')
for f in result['source_hashes']:
 check('result_pin_'+f['file'],hashlib.sha256((BASE/f['file']).read_bytes()).hexdigest()==f['sha256'])
for f in result['precalculation_plan']:
 check('plan_pin_'+Path(f['path']).name,hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256'])
# Capture the exact source bytes but convert only the authorized metadata columns.
rawsources={}
for s in source['sources']:
 b=rec(Path(s['path']),s['sha256'],'source bytes; only allowed metadata/alpha parsed')
 rawsources[Path(s['path']).name]=b
rows=rawsources['Pantheon+SH0ES.dat'].decode('utf-8').splitlines()
header=rows[0].split();cols={k:header.index(k) for k in ['zHD','zHEL','IS_CALIBRATOR']}
metasn=[{k:float(line.split()[col]) for k,col in cols.items()} for line in rows[1:] if line.strip()]
check('SN_metadata_source_order_exact',metasn==read('pantheon_metadata_only.json'))
metab=[]
for line in rawsources['desi_gaussian_bao_ALL_GCcomb_mean.txt'].decode('utf-8').splitlines():
 if not line.strip() or line.lstrip().startswith('#'):continue
 cols=line.split();metab.append({'z':float(cols[0]),'type':cols[2]})
check('BAO_metadata_source_order_exact',metab==read('desi_metadata_only.json'))
check('SN_cov_source_copy_exact',rawsources['pantheon_covariance.dat']==(BASE/'pantheon_STAT_SYS.cov').read_bytes())
check('BAO_cov_source_copy_exact',rawsources['desi_gaussian_bao_ALL_GCcomb_cov.txt']==(BASE/'desi_DR2.cov').read_bytes())
# Current public file identity is not refetched. Compare the captured Pantheon receipt chain.
public=json.loads(rawsources['FONTES_PUBLICAS_ADICIONAIS.json'])
for source_name,public_name in [('Pantheon+SH0ES.dat','pantheon_table.txt'),('pantheon_covariance.dat','pantheon_cov.txt')]:
 pr=next(x for x in public if Path(x['path']).name==public_name)
 digest=hashlib.sha256(rawsources[source_name]).hexdigest()
 check('captured_public_receipt_'+public_name,digest==pr['sha256']==pr['local_copy']['sha256'])
alpha=float(re.search(rb'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',rawsources['um.py'],re.M).group(1));beta=alpha*math.sqrt(math.e)
check('beta_from_source',beta==result['input']['beta_runtime'])
selected=[i for i,r in enumerate(metasn) if r['zHD']>.01 and r['IS_CALIBRATOR']==0]
check('SN_mask_count',len(selected)==1580==len(template['SN']))
check('SN_template_row_order',selected==[r['source_row_zero_based'] for r in template['SN']])
check('SN_template_z_order',all(r['zHD']==metasn[i]['zHD'] and r['zHEL']==metasn[i]['zHEL'] for r,i in zip(template['SN'],selected)))
check('BAO_template_order',all(r['z']==m['z'] and r['type']==m['type'] for r,m in zip(template['BAO'],metab)))
raw=(BASE/'pantheon_STAT_SYS.cov').read_text(encoding='utf-8');first,rest=raw.split('\n',1)
n=int(first);values=np.fromstring(rest,sep=' ')
check('SN_cov_dimensions',n==1701 and values.size==n*n)
full=values.reshape(n,n);cs=full[np.ix_(selected,selected)]
cb=np.loadtxt(io.BytesIO((BASE/'desi_DR2.cov').read_bytes()))
check('BAO_cov_dimensions',cb.shape==(13,13))
for label,cov in [('SN',cs),('BAO',cb)]:
 check(label+'_cov_finite',np.isfinite(cov).all())
 check(label+'_cov_symmetric',np.array_equal(cov,cov.T))
 check(label+'_cov_positive_diag',np.all(np.diag(cov)>0))
 cho_factor(cov,lower=True);check(label+'_cov_cholesky',True)
OM=result['input']['Omega_m_fid'];OR=result['input']['Omega_r_fid'];H=result['input']['H0_fid_km_s_Mpc'];RD=result['input']['rd_fid_Mpc'];LIGHT=299792.458
cache={}
def evaluate(z):
 if z in cache:return cache[z]
 def e2(x):return OM*(1+x)**3+OR*(1+x)**4+1-OM-OR
 I=quad(lambda x:1/math.sqrt(e2(x)),0,z,epsabs=2e-13,epsrel=2e-13)[0]
 A=quad(lambda x:e2(x)**(beta/3-.5),0,z,epsabs=2e-13,epsrel=2e-13)[0]
 dI=quad(lambda x:-.5*((1+x)**3-1)/e2(x)**1.5,0,z,epsabs=2e-13,epsrel=2e-13)[0]
 E=math.sqrt(e2(z));k=E**(2*beta/3);Q=A/I;dm=LIGHT/H*I;dh=LIGHT/H/E;dv=(dm*dm*z*dh)**(1/3)
 ldm=dI/I;ldh=-.5*((1+z)**3-1)/e2(z)
 cache[z]={'Q':Q,'sn':5*math.log10(Q),'dsn':5/math.log(10)*ldm,
  'DM_over_rs':(dm/RD,Q,dm/RD*ldm),'DH_over_rs':(dh/RD,k,dh/RD*ldh),'DV_over_rs':(dv/RD,Q**(2/3)*k**(1/3),dv/RD*(2*ldm+ldh)/3)}
 return cache[z]
sn=np.array([evaluate(r['zHD'])['sn'] for r in template['SN']]);ds=np.array([evaluate(r['zHD'])['dsn'] for r in template['SN']])
y=np.array([evaluate(m['z'])[m['type']][0] for m in metab]);ratio=np.array([evaluate(m['z'])[m['type']][1] for m in metab]);db=np.array([evaluate(m['z'])[m['type']][2] for m in metab]);sb=y*(ratio-1)
errors={
 'SN_Q':max(abs(evaluate(r['zHD'])['Q']-r['Q']) for r in template['SN']),
 'SN_signal_mag':float(np.max(abs(sn-np.array([r['signal_mu_mag'] for r in template['SN']])))),
 'SN_analytic_derivative':float(np.max(abs(ds-np.array([r['dmu_dOmega_m'] for r in template['SN']])))),
 'BAO_fiducial_not_observed':float(np.max(abs(y-np.array([r['fiducial_not_observed'] for r in template['BAO']])))),
 'BAO_signal':float(np.max(abs(sb-np.array([r['signal_map_B'] for r in template['BAO']])))),
 'BAO_analytic_derivative':float(np.max(abs(db-np.array([r['derivative_Om'] for r in template['BAO']])))),
 'BAO_sigma_order':float(np.max(abs(np.sqrt(np.diag(cb))-np.array([r['sigma_from_covariance'] for r in template['BAO']]))))}
for name,error in errors.items():check('template_'+name,error<(1e-6 if 'derivative' in name else 1e-10),error)
# Independent normal-equation GLS with Cholesky solves, not the author's whitened SVD.
fs=cho_factor(cs,lower=True);fb=cho_factor(cb,lower=True)
def calc(s,J,solver):
 if J.shape[1]:
  invJ=solver(J);g=J.T@invJ;b=J.T@solver(s);coeff=np.linalg.solve(g,b);r=s-J@coeff
  orth=float(np.max(abs(J.T@solver(r))))
 else:coeff=np.array([]);r=s;orth=0.
 d2=float(r@solver(r));return {'D':math.sqrt(max(0,d2)),'D2':d2,'orthogonality_normal_equations':orth,'nuisance_coefficients_from_synthetic_signal':coeff.tolist()}
ss=lambda x:cho_solve(fs,x);bs=lambda x:cho_solve(fb,x)
def js(x):return np.concatenate([ss(x[:len(sn)]),bs(x[len(sn):])],axis=0)
outputs=[]
def compare(label,s,J,solver,published):
 x=calc(s,J,solver);x.update({'label':label,'published_D':published['D_expected'],'abs_delta_D':abs(x['D']-published['D_expected'])});outputs.append(x);check(label+'_projection',x['abs_delta_D']<1e-7,x['abs_delta_D']);return x
ones=np.ones(len(sn));emptyS=np.empty((len(sn),0));emptyB=np.empty((len(y),0))
compare('SN_fixed',sn,emptyS,ss,result['SN']['fixed_amplitude'])
compare('SN_intercept',sn,ones[:,None],ss,result['SN']['intercept_projected'])
compare('SN_intercept_Om',sn,np.column_stack([ones,ds]),ss,result['SN']['intercept_Om_projected'])
compare('BAO_B_fixed',sb,emptyB,bs,result['BAO_B_extra_hypothesis']['fixed_amplitude'])
compare('BAO_B_scale',sb,y[:,None],bs,result['BAO_B_extra_hypothesis']['common_projected'])
compare('BAO_B_scale_Om',sb,np.column_stack([y,db]),bs,result['BAO_B_extra_hypothesis']['common_Om_projected'])
ja=np.r_[ones,np.zeros(len(y))];jb=np.r_[np.zeros(len(sn)),y];jom=np.r_[ds,db]
for label,bsignal in [('A_luminosity_only',np.zeros(len(y))),('B_universal_geometry_extra_assumption',sb)]:
 signal=np.r_[sn,bsignal]
 for name,J in [('fixed_amplitudes',np.empty((len(signal),0))),('independent_amplitudes',np.column_stack([ja,jb])),('independent_amplitudes_shared_Om',np.column_stack([ja,jb,jom]))]:
  compare('joint_'+label+'_'+name,signal,J,js,result['joint'][label][name])
const=calc(ones,ones[:,None],ss)['D'];scale=calc(y,y[:,None],bs)['D']
check('constant_SN_erased',const<1e-10,const);check('common_BAO_scale_erased',scale<1e-10,scale)
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CONDITIONAL_EXPECTED_SEPARATION_REVIEW_NO_OBSERVED_SIGNIFICANCE_NO_TEST_POWER','sources':records,'checks':checks,'checks_passed':len(checks),'metadata':{'SN_rows':len(metasn),'selected_SN_rows':len(sn),'BAO_components':len(y),'observed_centers_parsed':False,'source_table_bytes_hashed':True,'columns_parsed_SN':list(cols) if isinstance(cols,dict) else ['zHD','zHEL','IS_CALIBRATOR'],'columns_parsed_BAO':[0,2],'public_identity_scope':'captured receipts and local bytes, not new network retrieval'},'template_errors':errors,'projections':outputs,'max_D_discrepancy':max(x['abs_delta_D'] for x in outputs),'controls':{'SN_constant':const,'BAO_common_scale':scale},'findings':[{'id':'FORMA-REV-01','severity':'P3_terminology','issue':'The title and phrase resultado de poder can be read as probabilistic test power. D is a projected Gaussian template distance; no rejection threshold or sampling power was calculated. The body/protocol correctly limit the interpretation.','remedy':'Use separacao gaussiana esperada condicional or diagnostico de identificabilidade; do not append observed sigma or detection probability.'}],'scope_limits':['Gaussian fixed covariance and specified fiducial only','SN/BAO block independence assumed','Omega_m tangent, not nonlinear profiling','free independent common amplitudes, no external priors','map B additional hypothesis, not adopted motor prediction','no external source refresh or preregistration chronology certification'],'code_executed':'own reviewer code only','canonical_or_author_scripts_executed':False,'provider_calls':False,'observational_rites_repeated':False,'software':{'numpy':np.__version__,'scipy':scipy.__version__}}
atomic(OUT/'REVISAO_PODER_FORMA.json',json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps({'checks':len(checks),'sources':len(records),'template_errors':errors,'max_D_discrepancy':report['max_D_discrepancy'],'projections':[{k:x[k] for k in ['label','D','abs_delta_D']} for x in outputs]},indent=2))
