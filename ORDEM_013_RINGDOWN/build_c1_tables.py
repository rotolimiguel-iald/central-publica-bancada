"""Compile reading examples and independent finite-KMS dissipator checks."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import math
import numpy as np
from scipy.interpolate import CubicSpline
from tgl_ringdown_prediction import prediction,beta_tgl,propagation_exponent
from verify_c0_c3 import dissipator
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']['220']
    interp=CubicSpline(grid['spins'],np.array(grid['real'])+1j*np.array(grid['imag']),extrapolate=False)
    old=json.loads((ROOT/'cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json').read_bytes())['per_series'][2]
    schema=json.loads((ROOT/'C4_CATALOG_SCHEMA.json').read_bytes())
    recent=next(r for r in schema['rows'] if r['event']=='GW250114_082203')['summary']
    events=[dict(event='GW150914_legacy_remnant',mass=old['Mf_det'],spin=old['a_f'],redshift=0.,
                 source='cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json per_series[2]; z=0 convention, not a measured redshift'),
            dict(event='GW250114_public_posterior_medians',mass=recent['final_mass_non_evolved']['median'],
                 spin=recent['final_spin_non_evolved']['median'],redshift=recent['redshift']['median'],
                 source='pSEOB public posterior; marginal medians for display, joint samples used in C4')]
    rows=[];proof=[]
    for event in events:
        m,a,z=event['mass'],event['spin'],event['redshift'];mode=complex(interp(a))
        for reading in ['R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-RAIZ-COHERENT','R-LIN','R-MOD','R-GLOBAL']:
            pred=prediction(m,a,reading,redshift=z,qnm_dimensionless=mode if reading=='R-MOD' else None,
                            occupation=1e78 if reading=='R-RAIZ-COHERENT' else None)
            if reading=='R-RAIZ-COHERENT':
                # Prediction's x-based proxies must not be reported as a fitted exponential.
                pred={k:v for k,v in pred.items() if not k.startswith('delta_tau') and k!='x'}
                pred['delta_tau']=None
            rows.append(dict(event=event['event'],inputs=event,prediction=pred))
        pred=prediction(m,a,'R-MOD',qnm_dimensionless=mode)
        tm=pred['t_mass_s'];sr=math.sqrt(1-a*a);kappa=sr/(2*tm*(1+sr));om=a/(2*tm*(1+sr))
        nu=pred['omega_rad_s']-2*om;gap=2*math.pi*nu/kappa
        n=np.arange(8);weights=np.exp(-gap*n);weights/=weights.sum()
        K=np.diag(-np.log(weights));rho=np.diag(weights)
        D=dissipator(math.sqrt(beta_tgl())*K)*(kappa/(2*math.pi))
        coherence=np.zeros((8,8));coherence[0,1]=1.
        action=(D@coherence.ravel(order='F')).reshape((8,8),order='F')
        measured=-float(action[0,1].real);expected=pred['gamma_per_s']
        residual=float(np.linalg.norm(D@rho.ravel(order='F')))
        assert abs(measured/expected-1)<1e-12 and residual<1e-12
        shifted=dissipator(math.sqrt(beta_tgl())*(K+3.7*np.eye(8)))*(kappa/(2*math.pi))
        shift_residual=float(np.linalg.norm(shifted-D)/np.linalg.norm(D))
        assert shift_residual<1e-12
        rootD=dissipator(math.sqrt(beta_tgl())*np.diag(np.sqrt(np.diag(K))))*(kappa/(2*math.pi))
        rootrate=-float((rootD@coherence.ravel(order='F')).reshape((8,8),order='F')[0,1].real)
        proof.append(dict(event=event['event'],kappa_per_s=kappa,horizon_omega_rad_s=om,positive_gap_rad_s=nu,
                     finite_KMS_dimension=8,min_state_eigenvalue=float(weights.min()),
                     gamma_dissipator=measured,gamma_prediction=expected,
                     relative_error=abs(measured/expected-1),KMS_state_stationarity_residual=residual,
                     K_shift_relative_residual=shift_residual,root_of_normalized_K_rate=rootrate,
                     root_zero_background_rate=beta_tgl()*nu/2,
                     status='FINITE_CONDITIONAL_CONSTRUCTION__NOT_PHYSICAL_KERR_STATE_PROOF'))
    source=ROOT/'cache/casa/um_absoluto.json';clock=json.loads(source.read_bytes())['core']['clock_test_result_v369']
    # Illustrative propagation integral; its H0/Om are explicit input, not a fit.
    z=np.linspace(0,events[1]['redshift'],4097);H0=70*1000/3.085677581491367e22;h=H0*np.sqrt(.3*(1+z)**3+.7)
    src=prediction(events[1]['mass'],events[1]['spin'],'R-A',redshift=events[1]['redshift'])
    xi=propagation_exponent(src['omega_rad_s'],src['t_planck_s'],z,h)
    report=dict(status='ALL_READING_FORMULAS_DOCUMENTED__CONDITIONAL_NUMERICAL_EXAMPLES',rows=rows,
                finite_modular_oracles=proof,propagation_example=dict(Xi=xi,H0_km_s_Mpc=70.,Omega_m=.3,
                   z_max=float(z[-1]),scope='INPUT flat FLRW illustration; not ringdown damping'),
                v369_clock_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                v369=dict(partition=clock['partition_declared'],verdict=clock['verdict_short'],
                          tau_upper_clock95_s=clock['P1']['tau_star_bound_clock_95_s'],root_law=clock['root_law']),
                hypothesis_selection='NONE',not_done=['Physical state/partition selection','Full stochastic detector inference'])
    atomic_json(ROOT/'C1_TABLES.json',report)
    text=['[DERIVED condicional; INPUT nas pontes físicas]','', '# Leituras: resultados numéricos','',
          'Valores recalculados dos insumos descritos em C1_TABLES.json. Nenhuma leitura selecionada.','',
          '| Evento | Leitura | Γ (s⁻¹) | Γ/ω | δτ do ensemble |','|---|---|---:|---:|---:|']
    for row in rows:
        p=row['prediction'];delta=p['delta_tau']
        text.append(f"| {row['event']} | {p['reading']} | {p['gamma_per_s']:.7g} | {p['gamma_over_omega']:.7g} | {delta if delta is None else format(delta,'.7g')} |")
    text+=['','None no campo coerente: taxa inicial não é uma exponencial exata. R-PROP é apresentado como Xi, não δτ.',
           '',f'Xi planckiano ilustrativo: {xi:.9g}; cosmologia INPUT explícita no JSON.',
           '', 'Os controles matriciais de KMS, positividade e estacionariedade estão no JSON. A tabela analítica está em C1_LEITURAS_E_RELOGIOS.md.']
    path=ROOT/'C1_RESULTADOS_NUMERICOS.md';raw=('\n'.join(text)+'\n').encode()
    if path.exists():path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(path.read_bytes())
    temp=path.with_suffix('.tmp');temp.write_bytes(raw);assert temp.stat().st_size==len(raw);temp.replace(path)
    print(json.dumps(dict(proof=proof,propagation_Xi=xi)),flush=True)

if __name__=='__main__':main()
