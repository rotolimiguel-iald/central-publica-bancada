"""Independent algebra oracle and regression against frozen V346 measurements."""
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
from tgl_ringdown_prediction import beta_tgl, prediction, G_CODATA_2018, C, HBAR_SI, GM_SUN_IAU_2015

ROOT = Path(__file__).resolve().parent

def dissipator(jump):
    d = len(jump)
    eye = np.eye(d)
    gram = jump.conj().T@jump
    return np.kron(jump.conj(),jump)-.5*(np.kron(eye,gram)+np.kron(gram.T,eye))

def main():
    b = beta_tgl()
    rng = np.random.default_rng(132026)
    q,_ = np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
    k = np.array([0.,.3,2.,5.])
    jump = q@np.diag(np.sqrt(b*k))@q.conj().T
    generator = dissipator(jump)
    analytic = -.5*b*(np.sqrt(k[:,None])-np.sqrt(k[None,:]))**2
    measured = np.linalg.eigvalsh(generator)
    eigen_error = float(np.max(np.abs(np.sort(analytic.ravel())-measured)))
    shifted = jump+1.7*np.eye(4)
    shift_error = float(np.linalg.norm(dissipator(shifted)-generator))
    rho = np.eye(4)/4
    rate = float(np.trace(jump.conj().T@jump@rho).real)
    shifted_rate = float(np.trace(shifted.conj().T@shifted@rho).real)
    assert eigen_error<1e-12 and shift_error<1e-12 and abs(rate-shifted_rate)>1
    signed = np.array([-3.,-1.,0.,1.,3.])
    positive = np.maximum(signed,0)
    absolute = np.abs(signed)
    rates = lambda v: (.5*b*(np.sqrt(v[:,None])-np.sqrt(v[None,:]))**2).tolist()
    signed_choices = {'spectrum':signed.tolist(),'positive_part_rates_per_clock':rates(positive),
                      'absolute_value_rates_per_clock':rates(absolute),
                      'selection_status':'INPUT_NOT_FIXED_BY_TOMITA_CONJUGATION'}
    # E|n><n+1| weighting of <a> in a coherent state is Poisson(N).
    coherent=[]
    for nbar in (4,16,64,256):
        n=np.arange(0,int(nbar+14*math.sqrt(nbar)+50))
        weights=np.exp(-nbar+n*np.log(nbar)-np.array([math.lgamma(float(i)+1) for i in n]))
        neighbor_rate=b/(2*(np.sqrt(n+1)+np.sqrt(n))**2)
        exact=float(weights@neighbor_rate)
        coherent.append({'N':nbar,'initial_slope_per_unit_gap':exact,'large_N_asymptote':b/(8*nbar),
                         'ratio':exact/(b/(8*nbar)),'retained_probability':float(weights.sum())})
    p=ROOT/'cache/casa/RINGDOWN_DEPHASING_V2_RESULT.json'
    legacy=json.loads(p.read_bytes())['per_series'][2]
    reg={}
    for letter in ('A','B'):
        pred=prediction(legacy['Mf_det'],legacy['a_f'],'R-'+letter,profile='LEGACY_V346')
        target=legacy['delta_pred_'+letter]
        err=abs(pred['delta_tau_linear']-target)/abs(target)
        assert err<=1e-12
        reg[letter]={'expected':target,'calculated':pred['delta_tau_linear'],'relative_error':err,
                     'exact_additive_rate_result':pred['delta_tau_ensemble_exact']}
    # SI exponents are [mass,length,time]. GM/c^3 has dimensions of time, not a rate.
    add=lambda *terms:tuple(sum(values) for values in zip(*terms))
    gdim=(-1,3,-2); mdim=(1,0,0); cminus3=(0,-3,3)
    assert add(gdim,mdim,cminus3)==(0,0,1)
    assert add((0,0,1),(0,0,-2))==(0,0,-1)
    mass_kg=60*GM_SUN_IAU_2015/G_CODATA_2018
    mp=math.sqrt(HBAR_SI*C/G_CODATA_2018)
    tp=math.sqrt(HBAR_SI*G_CODATA_2018/C**5)
    tm=G_CODATA_2018*mass_kg/C**3
    solar_kg=mass_kg/60
    unit_report={'GM_over_c3_SI_exponents':add(gdim,mdim,cminus3),'GM_over_c3_seconds_60_solar':tm,
                 'planck_time_s':tp,'mass_ratio_M_over_mPlanck':mass_kg/mp,'time_ratio_tM_over_tPlanck':tm/tp,
                 'one_solar_mass_squared_planck_ratio':(solar_kg/mp)**2,
                 'sixty_solar_mass_squared_planck_ratio':(mass_kg/mp)**2,
                 'origin_of_10e76':'CONJECTURE: squared ONE solar mass / Planck mass; not rate and not 60 solar masses'}
    event_table={event:{r:prediction(mass,spin,r,redshift=z) for r in ('R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-GLOBAL')}
                 for event,mass,spin,z in [('GW150914_legacy_remnant',legacy['Mf_det'],legacy['a_f'],0.),
                                         ('GW250114_example_INPUT_pending_API',68.1,.68,68.1/62.7-1)]}
    report={'at':datetime.now().astimezone().isoformat(),'status':'PARTIAL_C0_C3_NUMERICAL_CHECKS_PASS',
            'numpy':np.__version__,'python':sys.version,'beta_runtime':b,
            'liouvillian_eigenvalue_residual':eigen_error,'jump_shift_generator_residual':shift_error,
            'jump_rate':rate,'shifted_jump_rate_same_generator':shifted_rate,
            'signed_modular_extensions':signed_choices,'coherent_root_initial_slope':coherent,
            'units':unit_report,'legacy_regression':reg,'legacy_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'conditional_event_table':event_table,
            'pending':['C0_full_claim_audit','C1_all_readings','R_MOD_exact_QNM','C2_trajectories_detector_noise',
                       'C4_joint_posteriors','C5_detector_PSD_Fisher','C6_registered_strain_run','C7_package']}
    out=ROOT/'C0_C3_checks.json'
    if out.exists():
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        out.with_name(out.name+'.bak_'+stamp).write_bytes(out.read_bytes())
    temp=out.with_suffix('.tmp')
    temp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode())
    assert temp.stat().st_size>100
    temp.replace(out)
    print(json.dumps({k:report[k] for k in ('status','beta_runtime','liouvillian_eigenvalue_residual',
         'jump_shift_generator_residual','units','legacy_regression','coherent_root_initial_slope')},ensure_ascii=False))

if __name__=='__main__': main()
