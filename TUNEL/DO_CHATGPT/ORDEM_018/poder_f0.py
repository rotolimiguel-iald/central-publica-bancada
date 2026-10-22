"""Pre-frozen forecast from primary sigmas, no observed centres or inference fit."""
import hashlib,json,math,time
from audit_inputs import ROOT,save_json,file_info
start=time.perf_counter()
p=ROOT/'F0_POWER_PROTOCOL_V1.json'
seal=json.loads((ROOT/'F0_POWER_PROTOCOL_HASHES.json').read_bytes())
assert file_info(p)['sha256']==seal['protocol_sha256']
assert file_info(__file__)['sha256']==seal['script_sha256']
a=json.loads(p.read_bytes());f=a['fiducials_INPUT_not_measured_centres']
b=f['alpha_CODATA2018']*math.sqrt(math.e)
e=math.sqrt(f['Omega_m']*(1+f['zstar'])**3+f['Omega_r']*(1+f['zstar'])**4+1-f['Omega_m']-f['Omega_r'])
k=e**(2*b/3);delta=(k-1)*f['Hfid'];bg=a['background_sigma']['sigma']
rows=[]
for name,components in a['local_sigma_components'].items():
 sig=math.sqrt(sum(v*v for v in components));total=math.hypot(sig,k*bg);s=delta/total
 # Two-sided alpha corresponding to 5 sigma, under Gaussian design alternative.
 power=.5*math.erfc((5-s)/math.sqrt(2))+.5*math.erfc((5+s)/math.sqrt(2))
 rows.append(dict(method=name,sigma_local=sig,sigma_contrast=total,expected_separation=s,power_at_5sigma_unadjusted=power))
cnu=(7/8)*(4/11)**(4/3)
dn=(4*b/3)*(1/cnu+f['Neff_SM'])
need=delta/5
out={'statute':'DERIVED_CONDITIONAL_FORECAST_NOT_VERDICT','protocol':file_info(p),'script':file_info(__file__),'beta':b,'K':k,'delta_H0_fiducial':delta,'hubble':rows,'sigma_contrast_needed_5sigma':need,'sigma_local_needed_5sigma_given_bg':math.sqrt(max(0,need*need-(k*bg)**2)),'neff':{'delta':dn,'rows':[dict(v,expected_separation=dn/v['value']) for v in a['neff_sigma']],'sigma_needed_5sigma':dn/5},'future_dates':{'2027':'NO_VERIFIED_CALENDAR_FORECAST','2030':'NO_VERIFIED_CALENDAR_FORECAST'},'central_values_used':False,'elapsed_seconds':time.perf_counter()-start}
assert k>1 and all(r['expected_separation']>0 for r in rows)
assert out['neff']['rows'][1]['expected_separation']>out['neff']['rows'][0]['expected_separation']
save_json(ROOT/'F0_POWER_RESULT.json',out)
print(json.dumps(out,ensure_ascii=False))
