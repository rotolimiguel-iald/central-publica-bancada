"""Reclassify frozen C6 diagnostics without reopening target strain."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,math
import numpy as np
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tgl_ringdown_prediction import prediction
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={}
def read(n):sources[n]=sha(ROOT/n);return json.loads((ROOT/n).read_bytes())
def new(n,raw):
    p=ROOT/n
    if p.exists():raise FileExistsError(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise ValueError('Write mismatch')
    t.replace(p);print(n,sha(p))
c6=read('C6_RESULTS.json');timing=read('bis/C3_C6_TIMING_013BIS.json');noise=read('C5_EMPIRICAL_NOISE.json');gate=read('PORTAO_DO_PODER_013_v2.json');grid=read('QNM_GRID.json');comp=read('C6_PYRING_START_COMPARISON.json');reg=read('REGISTRO_C6.json')
primary=[r for r in c6['results'] if r['primary_start'] and r['amplitude_prior_sd_strain']==1e-20]
if len(primary)!=5:raise ValueError('C6 primary coverage')
q=grid['modes']['220'];interp=CubicSpline(q['spins'],np.array(q['real'])+1j*np.array(q['imag']),extrapolate=False)
reference=next(r for r in primary if r['reading']=='R-GLOBAL')
mass=reference['mass_05_50_95'][1];spin=reference['spin_05_50_95'][1]
rows=[]
for r in [g for g in gate['readings'] if g['base']=='GW250114_MEASURED_NORM_10tM']:
    reading=r['reading'];matches=[x for x in primary if x['reading']==reading]
    if reading in ['R-PROP','R-RAIZ-COHERENT']:
        delta=None;scope='OPEN physical mapping; analytic small-effect scenario only';lnb=None
    else:
        p=prediction(mass,spin,reading,qnm_dimensionless=complex(interp(spin)) if reading=='R-MOD' else None)
        delta=p['delta_tau_ensemble_exact'];scope='Reading evaluated at GR C6-pre median remnant; not posterior-marginalized prediction';lnb=matches[0]['lnB_vs_GR'] if matches else 0.
    rows.append(dict(reading=reading,lnB_220plus440=lnb,delta_L_at_GR_median=delta,prediction_scope=scope,
       sigma_effective_actual_route=None,z_actual_route=None,
       actual_route_uncertainty_status='NOT_MEASURED_NOT_CALIBRATED__SINGLE_220_NONIDENTIFIABLE',
       actual_route_scope='220-only has exact local M/spin degeneracy; 220+440 may break it, but no calibrated sigma was obtained. Do not assign zero uncertainty or transfer fixed-source Fisher as measured sigma.',
       optimistic_fixed_source_reference=r['fixed_source'],single_220_free_source=r['unknown_source_single_220'],
       verdict='INCONCLUSIVE_SYSTEMATICS',identity='Equivalent to GR by construction' if reading=='R-GLOBAL' else None))
nr=[]
for d in noise['detectors']:
    stderr=math.sqrt(2/(d['whitened_dof']*d['N_held_out']))
    nr.append(dict(detector=d['detector'],reduced_chisquare_mean=d['reduced_chisquare_mean'],mean_standard_error_iid_approx=stderr,z_unit_scale_iid_approx=(d['reduced_chisquare_mean']-1)/stderr,
      PSD_median_to_mean_quantiles=d['median_mean_PSD_ratio_20_1000_05_50_95'],training_end_GPS=d['GPSstart']+d['training_seconds'][1],last_validation_start_GPS=max(d['held_out_GPS']),
      limitation='Approximate Gaussian independent-window SE; not a calibrated detector-noise significance; no correction applied'))
audit=ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/auditoria_da_gerencia/aud_2_C6.txt'
text=audit.read_text(encoding='utf-8')
if 'R-B −0,0156' not in text or 'R-MOD −0,2681' not in text:raise ValueError('Auditor variant anchor changed')
variants=dict(status='DECLARADO_INDEPENDENT_AUDITOR__NOT_RERUN_IN_F5',source_path=str(audit),source_sha256=sha(audit),
  scope='Level0 diagnostic, only220deformed, nonblind, no physical verdict; rounded values transcribed from the named audit',
  lnB={'R-B':-.0156,'R-RAIZ-0':-.0566,'R-LIN':-.1189,'R-MOD':-.2681},
  choice='Deforming 440 is INPUT affecting the physical partition, not selected by the bench')
opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
doc=dict(status='C6_PRE_NONBLIND_PRE_POWER_GATE_UNCALIBRATED_DIAGNOSTIC',utc=datetime.now(timezone.utc).isoformat(),supersedes='C6_RESULTS.json',supersedes_sha256=sources['C6_RESULTS.json'],
 code_sha256=sha(Path(__file__)),source_sha256=sources,opening_sha256=sha(opening),on_source_strain_read_this_run=False,
 observation='ln B approximately zero from NON_IDENTIFIABLE_SINGLE_220 is a model degeneracy statement; finite-prior evidence need not be identically zero. R-GLOBAL alone is exact equality in this implementation.',
 primary_reference=dict(mass_detector_solar=mass,spin=spin,start_tM=10,amplitude_prior_sd=1e-20),rows=rows,timing=timing['rows'],noise=nr,only220_variant=variants,
 guard_scope=dict(registered='c6_engine and registered dependency subset',not_covered=['run_c6_grid.py','fetch_c6_strain.py','fetch_public.py'],receipt='Text receipt editable; hash substring check is not an external immutable witness',chronology='Registration before strain is preserved; power/implementation oracle came later, documented in audit'),
 differences_from_pyRing=comp['differences'],early_window_warning='6–8tM may contain unresolved221; overlapping start windows are not independent experiments',
 not_paid=['Calibrated effective sigma for actual free-remnant 220+440 route','Injection bias and coverage with free M/spin','Fractional-delay coherent-network pyRing reproduction (PartB E3.1)','New PSD/stationarity sensitivity and its effect on lnB','Independent rerun of auditor only220 diagnostic, forbidden strain reread in F5'])
new('C6_ADENDO_REALIZADO.json',(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
note=f'''[REAL — reclassificação documental; C6-pre NÃO-CEGA e não calibrada]\n\nExistiam C6_RESULTS.json e os dez grids de strain, REGISTRO_C6.json e C5_EMPIRICAL_NOISE.json. Reusados resultados e metadados; nenhum strain foi aberto nesta execução. Novo: C6_ADENDO_REALIZADO.json, SHA256 `{sha(ROOT/'C6_ADENDO_REALIZADO.json')}`, registra cortes, degenerescência, ruído, lacunas da guarda e variante do auditor com atribuição.\n\nNão pago: sigma calibrada da rota 220+440 com fonte livre, cobertura por injeção, equivalência posterior pyRing e efeitos de PSD. A aproximação Fisher com fonte fixa aparece separada. Reprodução: /opt/lal_env/bin/python -B refeito/record_c6pre_013bis.py em cópia isolada. Axiomas: N/A — sem Lean. Abertura SHA256 `{sha(opening)}`.\n'''
new('REAPROVEITAMENTO_C6.md',note.encode())
if sha(ROOT/'C6_RESULTS.json')!=sources['C6_RESULTS.json']:raise ValueError('Frozen result changed')
