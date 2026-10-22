"""Recompute E0.6 from existing C5 estimators; never generate injections or strain."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime, timezone
import importlib.util
import json
import hashlib
import time
import numpy as np
from scipy.interpolate import CubicSpline

OUT=Path(__file__).resolve().parent
B=OUT.parents[1]
T0=time.perf_counter()
CPU0=time.process_time()
START=datetime.now(timezone.utc)
SOURCES={}


def pin(p):
    raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest()
    SOURCES[str(p.relative_to(B))]={'sha256':h,'bytes':len(raw)}
    return h


def read(name):
    p=B/name;pin(p);return json.loads(p.read_bytes())


def create(name, raw):
    p=OUT/name
    if p.exists():raise FileExistsError(p)
    if not isinstance(raw,bytes):raw=(json.dumps(raw,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>25*1024*1024:raise ValueError('First-level cache required')
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise IOError('Temporary bytes differ')
    try:os.link(t,p)
    finally:t.unlink()


def delta(a,x):
    a=np.asarray(a,dtype=float)
    if np.any(~np.isfinite(a)) or np.any(1+a*x<=0):raise ValueError('Invalid damping conversion')
    return -a*x/(1+a*x)


def summarize(values, groups):
    v=np.asarray(values,dtype=float);n=len(v)
    if n<2 or not np.all(np.isfinite(v)) or len(groups)!=n:raise ValueError('Invalid archived estimates')
    m=float(v.mean());s=float(v.std(ddof=1));u=np.unique(groups);g=len(u)
    def error(influence):
        return float(np.sqrt(g/(g-1)*sum(float(influence[groups==k].sum())**2 for k in u))/n) if g>1 else None
    influence=(n/(n-1))*((v-m)**2-float(np.mean((v-m)**2)))/(2*s) if s else np.zeros(n)
    return {'N':n,'distinct_noise_groups':g,'mean':m,'median':float(np.median(v)),
        'sigma_ddof1':s,'SE_mean_grouped_conditional':error(v-m),'SE_sigma_influence_grouped_conditional':error(influence),
        'q05_50_95':np.quantile(v,[.05,.5,.95]).tolist(),
        'uncertainty_scope':'Finite archived noise library, grouped by saved paired GPS or interval index; conditional asymptotic SE only. No PSD/model uncertainty or inter-interval covariance calibrated; cells are paired, not independent.'}


def main():
    for n in ['SYSTEMATICS_ADENDO.json','SYSTEMATICS_ADENDO.md','SYSTEMATICS_COST.json']:
        if (OUT/n).exists():raise FileExistsError(OUT/n)
    dataset=read('bis/e0_core/DATASET.json');core=read('bis/e0_core/E0_CORE.json')
    reg=read('REGISTRO_C5_IMR_RECOVERY.json');imr=read('C5_IMR_RECOVERY.json')
    families=read('C5_IMR_CONTROLS.json')['families'];grid=read('QNM_GRID.json')['modes']
    noise=read('C5_RECOLORED_NOISE.json');starts=read('C5_EMPIRICAL_IMR_STARTS.json')
    bias=read('C5_BIAS_ABLATION.json');overtones=read('C5_OVERTONE_ABLATION.json')
    extra=read('C5_EXTRA_QNMS.json');budget=read('bis/PART_B_BUDGET_START.json')
    for name in ['calibrate_imr_recovery.py','empirical_imr_recovery.py','diagnose_imr_bias.py','diagnose_overtones.py','tgl_ringdown_prediction.py']:
        pin(B/name)
    if imr['registration_sha256']!=SOURCES['REGISTRO_C5_IMR_RECOVERY.json']['sha256']:raise ValueError('Registration pin mismatch')
    for name in ['calibrate_imr_recovery.py','tgl_ringdown_prediction.py','QNM_GRID.json','C5_IMR_CONTROLS.json','C5_RECOLORED_NOISE.json']:
        if reg['hashes'][name]!=SOURCES[name]['sha256']:raise ValueError('Registered conversion source changed '+name)
    p=B/'tgl_ringdown_prediction.py';spec=importlib.util.spec_from_file_location('systematics_pinned_prediction',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    x={}
    for f in families:
        g=grid['220'];w=complex(CubicSpline(g['spins'],np.array(g['real'])+1j*np.array(g['imag']),extrapolate=False)(f['remnant_spin']))
        for reading in reg['readings']:
            x[(f['family'],reading)]=module.prediction(f['remnant_mass_detector_solar'],f['remnant_spin'],reading,qnm_dimensionless=w)['x']
    caches={};groups={}
    for entry in imr['draws']:
        p=B/entry['path']
        if pin(p)!=entry['sha256']:raise ValueError('C5 draws pin mismatch')
        with np.load(p,allow_pickle=False) as z:
            if list(z['columns'])!=['lnB','a_hat','CI90_lower','CI90_upper']:raise ValueError('Draws schema changed')
            psd=p.name.split('_')[0];caches[psd]=z['draws'].copy()
            gps=np.column_stack([z['H1_original_GPS'],z['L1_original_GPS']])
            _,groups[psd]=np.unique(gps,axis=0,return_inverse=True)
    matrix=[]
    for i,r in enumerate(imr['results']):
        base={k:r[k] for k in ['injection_family','recovery','psd','reading','injected_a','SNR','N']}
        base.update(source='C5_IMR_RECOVERY.json',locator='/results/'+str(i),start_tM=reg['start_tM'],
            waveform_scope=reg['deformation'],noise_indices=reg['noise_indices'],noise='O4/O5 recolored archived off-source',
            original_status=r['status'],original_boundary_hits=r.get('boundary_hits'),
            kind='MIXTURE' if r['recovery']=='EQUAL_FAMILY_MIXTURE' else 'SAME' if r['recovery']==r['injection_family'] else 'OPPOSITE',
            paid_scope='CONDITIONAL_C5_ESTIMATOR_DIAGNOSTIC_ONLY',operational_calibration_paid=False)
        draws=caches[r['psd']][r['draws_index']]
        if draws.shape!=(r['N'],4):raise ValueError('Draw count mismatch')
        if r['absolute_bias'] is None:
            base.update(status='NAO_PAGO_UNIDENTIFIABLE',dtau_statistics=None,noiseless_dtau=None)
        else:
            ahat=draws[:,1];base['a_statistics']=summarize(ahat,groups[r['psd']])
            if abs(abs(float(np.median(ahat))-r['injected_a'])-r['absolute_bias'])>1e-12:raise ValueError('Archived bias/index mismatch')
            if r['recovery']=='EQUAL_FAMILY_MIXTURE':
                base.update(status='NAO_PAGO_DTAU_FAMILY_BRANCH_NOT_ARCHIVED',dtau_statistics=None,noiseless_dtau=None,
                    reason='a_hat alone lacks winning family at each profile maximum; no unique recovery x220')
            else:
                xr=x[(r['recovery'],r['reading'])];xi=x[(r['injection_family'],r['reading'])]
                transformed=delta(ahat,xr);truth=float(delta(r['injected_a'],xi));clean=float(delta(r['noiseless_a_hat'],xr))
                st=summarize(transformed,groups[r['psd']]);base.update(status='PAGO_RECOMPUTED_CONDITIONAL_CONVERSION',
                    x220_recovery=xr,x220_injection=xi,dtau_truth=truth,dtau_statistics=st,
                    bias_mean_dtau=st['mean']-truth,bias_median_dtau=st['median']-truth,
                    noiseless_a_hat=r['noiseless_a_hat'],noiseless_dtau=clean,noiseless_bias_dtau=clean-truth,
                    noiseless_N=1,noiseless_SE=None,noiseless_boundary=r['noiseless_boundary'],
                    linear_proxy_a_times_delta1_control=float(np.median(ahat)*delta(1,xr)),
                    cross_family_scope='Each deformation is relative to its family-specific GR baseline; not a common absolute damping discrepancy')
        matrix.append(base)
    empirical=[]
    ids=np.asarray(starts['noise_indices'])
    for i,r in enumerate(starts['results']):
        base={k:r[k] for k in ['family','reading','PSD','N','network_ringdown_SNR','injected_a','start_tM']}
        base.update(source='C5_EMPIRICAL_IMR_STARTS.json',locator='/results/'+str(i),kind='TWO_QNM_RECOVERY_OF_FULL_IMR',
            original_status=r['status'],operational_calibration_paid=False)
        xr=x[(r['family'],r['reading'])]
        if not np.isclose(xr,r['dimensionless_extra_damping'][0],rtol=1e-12,atol=0):raise ValueError('Stored Gamma tau does not match pinned runtime')
        fits=r['profile_intervals']
        if fits is None:base.update(status='NAO_PAGO_UNIDENTIFIABLE',dtau_statistics=None)
        else:
            if len(fits)!=r['N']:raise ValueError('Profile count mismatch')
            ahat=np.array([f['MLE'] for f in fits]);truth=float(delta(r['injected_a'],xr));st=summarize(delta(ahat,xr),ids)
            base.update(status='PAGO_RECOMPUTED_CONDITIONAL_CONVERSION',x220=xr,dtau_truth=truth,
                dtau_statistics=st,bias_mean_dtau=st['mean']-truth,bias_median_dtau=st['median']-truth,
                boundary_count=sum(f['boundary'] for f in fits),noiseless_a_hat=r['noiseless_MLE'],
                noiseless_dtau=float(delta(r['noiseless_MLE'],xr)),noiseless_N=1,noiseless_SE=None,
                estimator_scope=starts['amplitude_model_scope'],noise_policy=starts['noise_policy'])
        empirical.append(base)
    ablations=[]
    for name,data in [('C5_BIAS_ABLATION.json',bias),('C5_OVERTONE_ABLATION.json',overtones)]:
        for i,r in enumerate(data['results']):
            xr=x[(r['family'],'R-B')];value=float(delta(r['a_hat'],xr))
            row={k:r[k] for k in ['family','start_tM','content','fit','a_hat','profile_boundary']}
            row.update(source=name,locator='/results/'+str(i),reading='R-B',noise='NONE',N=1,SE_mean=None,
                sigma_repeated_sampling=None,dtau_hat=value,x220=xr,SNR_shape=40,
                status='PAGO_DETERMINISTIC_CONVERSION_NOT_REPEATABILITY',
                linear_proxy_control=float(r['a_hat']*delta(1,xr)),
                sigma_dtau_local_Fisher_at_a0=abs(xr)*r['local_sigma_a'] if 'local_sigma_a' in r else None,
                Fisher_is_SE_of_control=False,operational_calibration_paid=False)
            ablations.append(row)
    # Floors use the freshly computed GW250114 reference; no manager magnitudes.
    reference=next(r for r in dataset['rows'] if r['product_id']=='GWTC5:GW250114_082203')
    floors={rd:{'delta_GW250114':p['delta_tau'],'floor5_INPUT':abs(p['delta_tau'])/5 if p['delta_tau'] is not None else None,
                'floor15_INPUT':abs(p['delta_tau'])/15 if p['delta_tau'] is not None else None} for rd,p in reference['predictions'].items()}
    for rows in [matrix,empirical,ablations]:
        for r in rows:
            fl=floors[r['reading']];r['floors']=fl
            mag=abs(r['bias_mean_dtau']) if 'bias_mean_dtau' in r else abs(r['dtau_hat']) if 'dtau_hat' in r else None
            r['component_magnitude']=mag
            r['below_floor5']=mag<fl['floor5_INPUT'] if mag is not None and fl['floor5_INPUT'] not in (None,0) else None
            r['below_floor15']=mag<fl['floor15_INPUT'] if mag is not None and fl['floor15_INPUT'] not in (None,0) else None
            r['gate_today']='NAO_PAGO_SIGMA_C_CALIBRADO_PSEOB_E_TRANSFERENCIA'
    typing=[]
    for pop,modes in core['combinations'].items():
        for rd,p in reference['predictions'].items():
            r=modes['std_ddof1'][rd]
            kind='OPEN_LOCAL_OBSERVABLE' if p['delta_tau'] is None else 'ZERO_EFFECT' if r['z_comb']==0 else 'SUBRESOLUTION_ANALYTIC_ONLY' if r['analytic_small_effect_below_1e12_inverse'] else 'CONDITIONAL_FORECAST_UNCALIBRATED'
            typing.append({'population':pop,'reading':rd,'type':kind,'N_alvo_operacional':None,'I_alvo_operacional':None,
                'analytic_only':{'N50':r['N50'],'N90':r['N90'],'I90':r['I_tau_target90'],'N90_slope':r['N90_slope']},
                'reason':'No approved operational target while systematic gate unpaid; tiny analytic counts retained only as non-operational arithmetic' })
    # Recomputed components by family/window are correlated controls, never a quadrature budget.
    result={'status':'NONBLIND_E0_6_DIRECT_C5_ADENDO_PRESERVES_V1','created_utc':datetime.now(timezone.utc).isoformat(),
        'conversion':'delta_tau(a;family)=-a*x220/(1+a*x220), x220=Gamma220*tau_GR220 from pinned runtime plus exact QNM; transform each archived estimate BEFORE moments',
        'primary_code_locators':['calibrate_imr_recovery.py:146-151 (exp(-a Gamma t)), :206-220 (a_hat/interval columns)',
            'empirical_imr_recovery.py:65-67 (decay+a Gamma)', 'diagnose_overtones.py:42-49 (shared harmonic rate)'],
        'full_IMR_family_recovery':matrix,'empirical_QNM_recovery_by_window':empirical,'noiseless_ablations':ablations,
        'floors':floors,'target_typing_adendo':typing,
        'not_paid':['E1 c(sigma)/c(SNR) nuisance fit','Residual sigma(c) for full pSEOB free mass/spin','Unique family-mixture a->dtau without branch labels',
            'SE from a single deterministic noiseless control','Inter-interval dependence and PSD uncertainty','New R-PROP/coherent C5 controls','Operational N target or physical confirmation'],
        'not_performed':['new injection','new waveform','posterior HDF5 read','strain read','producer C5 execution','Monte Carlo'],
        'sources':SOURCES.copy(),'code_sha256':pin(Path(__file__))}
    create('SYSTEMATICS_ADENDO.json',result)
    lines=['[REAL — NÃO-CEGO; E0.6 reobtido dos estimadores C5 existentes; calibração operacional NÃO PAGA]',
        '', '# E0.6 — adendo direto C5 e tipagem de N', '',
        'Preserva DATASET.json/E0_CORE.json. Lê os draws/estimadores arquivados, sem rerun de C5, PE, onda ou strain. Nenhuma magnitude da gerência entrou nesta matriz.', '',
        '**Conversão:** δτ(a)=−a·x/(1+a·x), com x=Γτ do 220 exato da família de recuperação. Média/DP/EP foram calculados após transformar cada a_hat. O antigo proxy a·δτ(1) aparece somente como controle. Negativos são diagnósticos de ajuste, não geradores GKLS físicos.', '',
        f'Matriz: {len(matrix)} células IMR (206 ruídos cada); {len(empirical)} células 220+440 por janela (50 ruídos cada); {len(ablations)} controles sem ruído. Casos não identificáveis permanecem nulos. As células reutilizam intervalos e não são evidências independentes.', '',
        'EP da média e do DP: influência agrupada pelos pares GPS salvos/índices de intervalo, condicionada à biblioteca finita. Não inclui PSD, dependência entre intervalos ou erro de modelo. Controle sem ruído: N=1, EP=null; Fisher local não é EP medido. Na mistura, a família vencedora não está nos draws: conversão única e σδτ NÃO PAGOS.', '',
        'Exemplo R-B, O4, a injetado=0, SNR40, início 10tM; cada δ é relativo ao GR da sua família:', '',
        '| Injeção → recuperação | δτ sem ruído | Média δτ ± EP | DP δτ ± EP | N |', '|---|---:|---:|---:|---:|']
    for r in matrix:
        if r['reading']=='R-B' and r['psd']=='O4' and r['injected_a']==0 and r['SNR']==40 and r.get('dtau_statistics'):
            s=r['dtau_statistics'];lines.append(f"| {r['injection_family']} → {r['recovery']} | {r['noiseless_dtau']:.7g} | {s['mean']:.7g} ± {s['SE_mean_grouped_conditional']:.3g} | {s['sigma_ddof1']:.7g} ± {s['SE_sigma_influence_grouped_conditional']:.3g} | {s['N']} |")
    lines+=['','Pisos |δ|/5 e |δ|/15 vêm da referência GW250114 recalculada no DATASET, ambos INPUT. Cada célula tem fonte/índice, família, ruído, janela, bordas e comparação aos pisos. Nenhuma comparação de magnitude substitui σ(c_calibrado) pSEOB: gate operacional permanece NÃO PAGO.', '',
        '**N_alvo_operacional=null** no adendo, inclusive para todas as linhas de subresolução. N50/N90 astronômicos da v1 ficam apenas em analytic_only, sem constituir alvos de aquisição. R-GLOBAL é efeito nulo; R-RAIZ-COHERENT/R-PROP continuam OPEN para este observável. Não escolher leitura.', '',
        'A revisão escalar principal foi comunicada pelo operador; este adendo ainda requer revisão distinta. MC da rota IV não foi refeito. E1 não iniciado. Axiomas N/A; teoremas 0.', '',
        'Arquivos novos deste adendo: build_systematics_adendo.py, SYSTEMATICS_ADENDO.json, SYSTEMATICS_ADENDO.md, SYSTEMATICS_COST.json. SHA/fontes e custo nos JSONs.']
    create('SYSTEMATICS_ADENDO.md',('\n'.join(lines)+'\n').encode())
    # Verify consumed bytes again; originals stay immutable.
    for name,entry in SOURCES.items():
        if hashlib.sha256((B/name).read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('Source changed '+name)
    end=datetime.now(timezone.utc)
    cost={'status':'COMPLETED_EXISTING_ESTIMATOR_CONVERSION_ONLY','started_utc':START.isoformat(),'finished_utc':end.isoformat(),
        'wall_seconds':time.perf_counter()-T0,'process_cpu_seconds':time.process_time()-CPU0,'processes':1,'threads':1,
        'operator_budget_start_utc':budget['started_utc'],'deadline_utc':budget['hard_deadline_utc'],
        'accounting':'Continuous shared wall clock; do not sum concurrent worker durations',
        'outputs':{n:{'bytes':(OUT/n).stat().st_size,'sha256':pin(OUT/n)} for n in ['SYSTEMATICS_ADENDO.json','SYSTEMATICS_ADENDO.md']},
        'source_integrity_rechecked':True,'source_hashes':SOURCES,'code_sha256':pin(Path(__file__))}
    create('SYSTEMATICS_COST.json',cost)
    print(json.dumps({'status':result['status'],'IMR_cells':len(matrix),'empirical_cells':len(empirical),'noiseless_controls':len(ablations),'wall_seconds':cost['wall_seconds']}),flush=True)


if __name__=='__main__':main()
