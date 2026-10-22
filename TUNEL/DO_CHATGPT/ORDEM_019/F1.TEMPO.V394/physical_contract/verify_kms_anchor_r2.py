"""Preregistered verification of the additive Gibbs anchor, isolated namespace."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
out=B/'RESULTADO_KMS_ANCHOR_R2.json'
if out.exists():raise RuntimeError('immutable result already exists')
pin=json.loads((B/'KMS_ANCHOR_PIN_R2.json').read_text(encoding='utf-8'))
for f,h in pin['files'].items():
    if hashlib.sha256((B/f).read_bytes()).hexdigest()!=h:raise RuntimeError('pin changed: '+f)
ns={'__name__':'v394_finite_contract_test'}
for f in ['physical_parameters.py','kms_root_anchor_r2.py']:
    exec(compile((B/f).read_text(encoding='utf-8'),str(B/f),'exec'),ns)
cfg=json.loads((B/'PREREGISTRO_KMS_ANCHOR_R2.json').read_text(encoding='utf-8'))
hb=6.62607015e-34/(2*math.pi)
derive=ns['v394_gibbs_root_parameters']
tol=cfg['relative_tolerance']
checks=[]
def ck(n,r):checks.append({'name':n,'residual':float(r),'pass':math.isfinite(r) and abs(r)<=tol})
p=derive(hb,2.)
for kappa in cfg['additional_kappa_s_inv']:
    q=derive(hb,kappa)
    P=q['kms_clock']['kms_period_s']
    kl,kh=q['density_surprise_eigenvalues']
    rate=(q['beta']/(2*P))*(math.sqrt(kh)-math.sqrt(kl))**2
    ck('rate_at_kappa_'+str(kappa),rate/q['gamma_s_inv']-1)
    ck('positive_K_at_'+str(kappa),0 if 0<kl<kh else 1)
    ck('offset_strict_at_'+str(kappa),0 if q['Eref_J']>q['V0_J'] else 1)
    ck('energy_high_at_'+str(kappa),(hb/P)*kh/q['energies_J'][1]-1)
    ck('energy_low_at_'+str(kappa),(hb/P)*kl/q['energies_J'][0]-1)
    for lam in cfg['clock_rescalings']:
        z=derive(lam*hb,lam*kappa)
        for key in ['Eref_J','Omega_rad_s','gamma_s_inv']:
            ck(str((kappa,lam,key)),z[key]/(lam*q[key])-1)
        for key in ['tau_eff_s','echo_dt_s']:
            ck(str((kappa,lam,key)),z[key]/(q[key]/lam)-1)
        ck(str((kappa,lam,'P')),z['kms_clock']['kms_period_s']/(P/lam)-1)
        for j in (0,1):ck(str((kappa,lam,'K',j)),z['density_surprise_eigenvalues'][j]/q['density_surprise_eigenvalues'][j]-1)
try:
    derive(hb,.1)
    refused=False
except ns['V394PhysicalContractError']:
    refused=True
ck('strict_offset_precision_refusal',0 if refused else 1)
P=p['kms_clock']['kms_period_s']
gap=2*P*p['Omega_rad_s']
result={'unit':'F1.TEMPO.V394','finished_utc':datetime.now(timezone.utc).isoformat(),
 'reference':p,'checks':checks,'checks_total':len(checks),'all_passed':all(x['pass'] for x in checks),
 'minus_log_Delta_spectrum':[0.,0.,-gap,gap],
 'positive_density_not_positive_modular_generator':gap>0,
 'pin_sha256':hashlib.sha256((B/'KMS_ANCHOR_PIN_R2.json').read_bytes()).hexdigest(),
 'scope':'Synthetic finite check; no global H2/light-net or empirical calibration'}
data=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
with out.open('xb') as f:f.write(data)
print(json.dumps({'all_passed':result['all_passed'],'checks':len(checks),'sha256':hashlib.sha256(data).hexdigest()}))
if not result['all_passed']:raise SystemExit(1)
