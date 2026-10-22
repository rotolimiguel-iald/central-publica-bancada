"""Independent, bounded C0 checks. Reads frozen sources; never imports them.
Run with the existing /opt/lal_env/bin/python -B under WSL.
Writes only the authorized JSON report, atomically. No PE or simulations.
"""
import ast
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
import h5py
import numpy as np

BASE = Path(__file__).resolve().parents[2]
ROOT = BASE.parent
OUT = BASE / 'bis/C0_ADVERSARIAL_SOURCE_REVIEW.json'
sources = {}

def winpath(p):
    return str(p).replace('/mnt/c/', 'C:/').replace('/', '\\')

def record(p):
    p = p.resolve()
    assert p.is_relative_to(ROOT), p
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    sources[winpath(p)] = {'bytes': p.stat().st_size, 'sha256': h.hexdigest()}
    return p

def readj(rel):
    return json.loads(record(BASE / rel).read_bytes())

u = record(BASE / 'cache/casa/um.py').read_text(encoding='utf-8').splitlines()
alpha_line = next((i, s) for i, s in enumerate(u, 1) if s.startswith('SEALED_CODATA_ALPHA ='))
ALPHA_FINE_CODATA_2018 = ast.literal_eval(alpha_line[1].split('=', 1)[1].split('#')[0].strip())
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
# Literal-only extraction of the embedded result; NO exec/eval/import of um.py.
d1line, literal = next((i, s) for i, s in enumerate(u, 1) if s.startswith("    'saida/D1_CAMB_V3_REAL_RESULT.json': '{"))
embedded = ast.literal_eval(literal.split(': ', 1)[1].rstrip(','))
d1 = json.loads(embedded)
posterior = d1['fases']['fase3_mcmc_primario']['summary']['beta']
sigma = (posterior['sigma_lower'] + posterior['sigma_upper']) / 2
d1check = {'line': d1line, 'embedded_utf8_sha256': hashlib.sha256(embedded.encode()).hexdigest(),
           'posterior': posterior, 'sigma_symmetric': sigma,
           'z_recomputed': abs(beta-posterior['median'])/sigma,
           'scope': 'ARITHMETIC_FROM_EMBEDDED_RESULT_NOT_NEW_MCMC',
           'autocorr': d1['fases']['fase3_mcmc_primario']['autocorr_time']}

# Independent matrix action on E_ij, not the builder's Kronecker implementation.
def diss(L, rho):
    A = L.conj().T @ L
    return L @ rho @ L.conj().T - (A @ rho + rho @ A) / 2

k = np.array([-3., -1., 0., 1., 3.])
rates = {}
for name, mapped in [('K_plus', np.maximum(k, 0)), ('abs_K', np.abs(k))]:
    L = np.diag(np.sqrt(beta * mapped))
    computed = np.empty((5, 5))
    residuals = []
    for i in range(5):
        for j in range(5):
            E = np.zeros((5, 5)); E[i, j] = 1
            rate = beta/2 * (math.sqrt(mapped[i])-math.sqrt(mapped[j]))**2
            actual = diss(L, E)
            computed[i, j] = -actual[i, j]
            residuals.append(float(np.max(np.abs(actual+rate*E))))
    rates[name] = {'rates': computed.tolist(), 'max_action_residual': max(residuals),
                   'rate_plus3_minus3': computed[4, 0], 'rate_0_1': computed[2, 3]}

rng = np.random.default_rng(11)
A = rng.standard_normal((4,4)); K = A@A.T/4
w, V = np.linalg.eigh(K); L = (V*np.sqrt(beta*w))@V.T
diagonal_residual = max(float(np.linalg.norm(diss(L,np.outer(V[:,i],V[:,i])))) for i in range(4))
rho0 = np.diag([.997,.001,.001,.001])
rho_star = V @ np.diag(np.diag(V.T@rho0@V)) @ V.T
kms = (V*np.exp(-w))@V.T; kms /= np.trace(kms)
proxy = {'seed':11,'dimension':4,'eigenvalues_K':w.tolist(),
         'four_independent_stationary_projectors_residual':diagonal_residual,
         'rho_star_minus_exp_minus_K_normalized_frobenius':float(np.linalg.norm(rho_star-kms))}
# Exact two-level counterexample to identifying Davies transitions with f(K).
Kb = np.diag([0.,1.]); rhog = np.diag([1.,0.]); rhop = np.full((2,2),.5)
up = beta/math.expm1(1); down = beta*(1+1/math.expm1(1))
Ddav = lambda r: diss(np.array([[0.,0.],[math.sqrt(up),0.]]),r)+diss(np.array([[0.,math.sqrt(down)],[0.,0.]]),r)
counter = {'K':[0,1], 'rho_population':[1,0], 'davies_d_rho11':float(Ddav(rhog)[1,1]),
           'root_d_rho11':float(diss(np.diag([0,math.sqrt(beta)]),rhog)[1,1]),
           'coherent_state_eigenvalues':np.linalg.eigvalsh(rhop).tolist(),
           'hamiltonian_changes_derivative_norm':float(np.linalg.norm(-1j*(Kb@rhop-rhop@Kb)))}

combo = readj('C4_CATALOG_COMBINATION.json')
catalog = readj('C4_CATALOG_220.json')
selected = set(combo['selected_events'])
raw = []
for p in sorted((BASE/'cache/public/21454847/extracted/pSEOB/metafiles').glob('*.h5')):
    event = p.name.removeprefix('pSEOB_').removesuffix('_Prod0.h5')
    if event not in selected:
        continue
    with h5py.File(record(p),'r') as f:
        datasets = []
        f.visititems(lambda n,o: datasets.append(n) if isinstance(o,h5py.Dataset) and n.endswith('/posterior_samples') else None)
        assert len(datasets)==1, datasets
        ds = f[datasets[0]]
        vals = ds['dtau220']
        med = float(np.median(vals))
        expected = next(r['quantiles']['dtau220'][1] for r in catalog['rows'] if r['event']==event)
        raw.append({'event':event,'path':winpath(p),'dataset':datasets[0], 'N':len(vals),
                    'dtau_median':med,'minus_existing_json':med-expected})
assert len(raw)==31

eventpath = BASE/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
with h5py.File(record(eventpath),'r') as f:
    ds = f['pSEOBNRv5PHM/posterior_samples']
    fields = ['dtau220','domega220','final_spin_non_evolved','final_mass_non_evolved']
    q = {field:np.quantile(ds[field],[.05,.5,.95]).tolist() for field in fields}
    sigma_tau = float(np.std(ds['dtau220']))
    spin = ds['final_spin_non_evolved']
    omega_mass = 1.5251-1.1568*(1-spin)**.1292
    quality = .7+1.4187*(1-spin)**(-.499)
    x = beta*quality*omega_mass
    delta = -x/(1+x)
    event = {'N':len(ds),'quantiles_05_50_95':q,'sigma_dtau_population':sigma_tau,
             'delta_RB_05_50_95':np.quantile(delta,[.05,.5,.95]).tolist(),
             'correction_over_sigma':float(abs(np.median(delta))/sigma_tau),
             'qnm_method':'BCW fit 2006; independently evaluated; no new QNM solve'}
a = q['final_spin_non_evolved'][1]
wr = 1.5251-1.1568*(1-a)**.1292; Q = .7+1.4187*(1-a)**(-.499)
x_naive = beta*2*Q/wr
event['Gamma_beta_over_tM'] = {'x':x_naive,'delta':-x_naive/(1+x_naive),
    'correction_over_sigma': x_naive/(1+x_naive)/sigma_tau,
    'distance_to_observed_median_in_sigma':abs(-x_naive/(1+x_naive)-q['dtau220'][1])/sigma_tau}
v2 = readj('cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json')['stacks']
for row in v2.values():
    row['power_B_recomputed'] = abs(row['delta_pred_B'])/row['sigma']

report = {'created_utc':datetime.now(timezone.utc).isoformat(),
 'status':'INDEPENDENT_SOURCE_REVIEW_WITH_CORRECTIONS_AND_EXPLICIT_GAPS',
 'independence':'This task did not construct C0, C1, C2 or their source artifacts. Independent source reading and arithmetic; previous auditors used as leads, not proof.',
 'beta_runtime':beta,'alpha_source_line':alpha_line[0], 'd1':d1check,'rates':rates,
 'proxy':proxy,'davies_counterexample':counter,'GW250114':event,'v2_stacks':v2,
 'catalog_primary':{'rows':raw,'positive_medians':sum(r['dtau_median']>0 for r in raw),
                    'max_existing_json_error':max(abs(r['minus_existing_json']) for r in raw)},
 'sources':sources, 'not_done':['No source execution/import','No PE','No Lean compilation','No MCMC','No final deliverables','No C0_v2','No memory/canonical edits']}
data = (json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
temp = OUT.parent/'c0_review/report.tmp'
temp.write_bytes(data)
assert temp.stat().st_size==len(data)
os.replace(temp,OUT)
print(json.dumps({k:report[k] for k in ['beta_runtime','d1','proxy','davies_counterexample','GW250114']},ensure_ascii=False,indent=2))
print('catalog:',report['catalog_primary']['positive_medians'],'/31; error:',report['catalog_primary']['max_existing_json_error'])
