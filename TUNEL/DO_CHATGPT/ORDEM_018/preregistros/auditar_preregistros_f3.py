"""Read-only audit of supplied preregistrations; never opens D strain/posteriors."""
import ast, hashlib, json, math, os
from pathlib import Path
from datetime import datetime, timezone
INPUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_018_INSUMOS')
OUT = Path(__file__).resolve().parent

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def load(name): return json.loads((INPUT/name).read_text(encoding='utf-8-sig'))
def atomic_json(path, obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    if path.exists():
        backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        prior=path.read_bytes(); backup.write_bytes(prior); assert backup.read_bytes()==prior
    temp=path.with_name(path.name+'.tmp_'+str(os.getpid()))
    temp.write_bytes(data); assert temp.read_bytes()==data
    os.replace(temp,path); assert path.read_bytes()==data

manifest=load('MANIFESTO_INSUMOS.json')
checks=[]
for name,expected in manifest['arquivos'].items():
    data=(INPUT/name).read_bytes()
    checks.append(dict(name=name,bytes=len(data),sha256=sha_bytes(data),expected=expected,match=len(data)==expected['bytes'] and sha_bytes(data)==expected['sha256']))
assert all(c['match'] for c in checks), 'Input manifest mismatch'
r=load('RAMO_B_V1__PREREGISTRO_RAMO_B_RINGDOWN_V1.json')
spec_hash=sha_bytes(json.dumps(r['spec'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8'))
assert spec_hash==r['spec_sha256']
inner=load('RAMO_B_V1__V1_RAMO_B_HASHES.json')
inner_checks=[]
for name,e in inner['arquivos'].items():
    b=(INPUT/('RAMO_B_V1__'+name)).read_bytes()
    inner_checks.append(dict(name=name,sha256=sha_bytes(b),bytes=len(b),match=sha_bytes(b)==e['sha256'] and len(b)==e['bytes']))
assert all(c['match'] for c in inner_checks)
f=load('FASE8__PODER_FASE8_UNIVERSO_PRIMORDIAL.json')
ALPHA_FINE_CODATA_2018=f['beta']['alpha_regex']
beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
F=(7/8)*(4/11)**(4/3); N_SM=f['mapa_A_Neff']['N_SM']; delta_rad=4*beta/3
DN=(1/F+N_SM)*delta_rad
phase8={'beta':beta,'alpha_source':'hash-verified FASE8 power JSON beta.alpha_regex; original um.py not imported','delta_radiation_fraction':delta_rad,'Delta_Neff_after_annihilation':DN,'Delta_Nequiv_before_annihilation':delta_rad*43/7,'S_constant':math.sqrt(1+delta_rad),'sigma_required_5':DN/5,'relative_DN_reproduction_error':DN/f['mapa_A_Neff']['Delta_Neff']-1,'published_sigma_scenarios':[],'forecast_sigma_scenarios':[]}
for e in f['mapa_A_Neff']['medidas_publicadas']:
    phase8['published_sigma_scenarios'].append({'source':e['fonte'],'citation':e['referencia'],'sigma':e['sigma'],'contrast_over_sigma':DN/e['sigma'],'source_status':'DECLARADO in supplied frozen, verify primary separately'})
for e in f['mapa_A_Neff']['projecoes']:
    phase8['forecast_sigma_scenarios'].append({'source':e['instrumento'],'citation':e['referencia'],'sigma':e['sigma_N_eff'],'contrast_over_sigma':DN/e['sigma_N_eff'],'calendar_status':'NOT_VERIFIED_NOT_A_SCHEDULE','source_status':e['estatuto']})

def prediction(a):
    Fq=1.5251-1.1568*(1-a)**0.1292
    Q=0.7000+1.4187*(1-a)**(-0.4990)
    kap=math.sqrt(1-a*a)/(2*(1+math.sqrt(1-a*a)))
    k=2*math.pi/kap; N=Fq*Q; x=beta*k*N
    return -x/(1+x)
rows=r['sigma_por_evento_A31_so_sigma_e_spin']
pred=[prediction(x['spin_q50']) for x in rows]
sig=[x['sigma_std'] for x in rows]
assert len(rows)==31 and all(s>0 for s in sig)
max_prediction_diff=max(abs(d-x['delta_exato']) for d,x in zip(pred,rows))
assert max_prediction_diff<1e-10

def projection(sys):
    w=[1/(s*s+sys*sys) for s in sig]
    S0=sum(w); S1=sum(wi*si for wi,si in zip(w,sig)); S2=sum(wi*si*si for wi,si in zip(w,sig))
    T0=sum(wi*di for wi,di in zip(w,pred)); T1=sum(wi*si*di for wi,si,di in zip(w,sig,pred))
    det=S0*S2-S1*S1
    assert det>0
    a0=(T0*S2-T1*S1)/det; a1=(S0*T1-S1*T0)/det
    residual=[di-a0-a1*si for di,si in zip(pred,sig)]
    const=T0/S0
    z_raw=math.sqrt(sum(wi*di*di for wi,di in zip(w,pred)))
    z_c0=math.sqrt(sum(wi*(di-const)**2 for wi,di in zip(w,pred)))
    z_full=math.sqrt(sum(wi*di*di for wi,di in zip(w,residual)))
    assert abs(sum(wi*di for wi,di in zip(w,residual)))<1e-9
    assert abs(sum(wi*si*di for wi,si,di in zip(w,sig,residual)))<1e-9
    return dict(sigma_sys_diagonal_scenario=sys,naive_weighted_mean_contrast=abs(T0)/math.sqrt(S0),gaussian_simple_hypothesis_norm=z_raw,after_free_c0_norm=z_c0,after_free_c0_plus_kc_sigma_norm=z_full,retained_squared_norm_fraction=z_full*z_full/(z_raw*z_raw),projected_coefficients={'c0':a0,'kc':a1},weighted_residual_sum=sum(wi*di for wi,di in zip(w,residual)))
profiles=[projection(s) for s in [0,0.029,0.038]]
source_inventory=[]
for e in r['fontes']:
    if any(k in e.get('papel','').lower() for k in ['5sigma','systematics','t01','e0','f4','decisão','poder','reconciliação']):
        p=Path(e['caminho']); rec={'role':e['papel'],'path':str(p),'hash_in_V1':e['sha256']}
        try:
            b=p.read_bytes();rec.update(bytes=len(b),sha256=sha_bytes(b),matches_V1=sha_bytes(b)==e['sha256'])
        except OSError as ex: rec.update(read_error=type(ex).__name__,message=str(ex))
        source_inventory.append(rec)
functions={}
for name in ['RAMO_B_V1__gerar_preregistro_ramo_b_05out.py','RAMO_B_V1__poder_cego_ramo_b_v2.py','FASE8__poder_fase8_universo_primordial.py']:
    tree=ast.parse((INPUT/name).read_text(encoding='utf-8'))
    functions[name]=[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
result={'audit_utc':datetime.now(timezone.utc).isoformat(),'status':'PREPARATION_AUDIT_NO_VERDICT','manifest_checks':checks,'manifest_all_match':True,'ringdown_inner_hashes':inner_checks,'spec_sha256_computed':spec_hash,'spec_sha256_matches':True,'phase8_sigma_only_reproduction':phase8,'ringdown_nuisance_design_diagnostic':{'dataset':'A31 frozen sigma/spin only; calibration NOT_BLIND; no observed dtau values read','assumptions':'Independent Gaussian event errors. Diagonal systematic scenarios illustrative. Fully free shared nuisance under both hypotheses. No auxiliary calibration information. Not D power, not a verdict, not an amendment of V1.','formula':'Delta_perp=(I-X(X^T C^-1 X)^-1 X^T C^-1)Delta; X=[1,sigma]; Z_shape^2=Delta_perp^T C^-1 Delta_perp','prediction_max_absolute_diff':max_prediction_diff,'n':len(rows),'profiles':profiles,'D_status':'sigma_i absent from V1; no D covariance or power computed'},'D_freeze_status':r['conjuntos']['D']['congelamento_por_evento'],'D_eligible_names':r['conjuntos']['D']['eventos_elegiveis'],'D_no_hold_names':r['conjuntos']['D']['elegiveis_sem_hold'],'D_hold_names':r['conjuntos']['D']['com_data_quality_hold'],'D_missing_GPS_count':sum(x['GPS'] is None for x in r['conjuntos']['D']['previsao_da_hipotese_por_evento_INFORMACAO_CEGA']),'dependency_inventory':source_inventory,'legacy_generator_functions_static_only':functions,'bounds':{'D_strain_or_posteriors_opened':False,'PE_executed':False,'legacy_generators_executed':False,'canonical_changed':False,'remote_provider_called':False}}
atomic_json(OUT/'AUDITORIA_PREREGISTROS_F3.json',result)
print(json.dumps({'all_inputs_match':True,'n_inputs':len(checks),'inner_checks':len(inner_checks),'spec_hash_match':True,'phase8_DN':DN,'A31_prediction_max_abs_diff':max_prediction_diff,'A31_profiles':profiles,'dependency_checks':len(source_inventory),'legacy_functions':functions,'output':str(OUT/'AUDITORIA_PREREGISTROS_F3.json')},ensure_ascii=False,indent=2))
