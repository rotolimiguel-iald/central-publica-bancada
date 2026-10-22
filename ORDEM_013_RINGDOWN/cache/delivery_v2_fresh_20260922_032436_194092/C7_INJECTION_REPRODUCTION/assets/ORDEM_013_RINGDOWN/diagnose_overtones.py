"""Test whether omitted decaying modes explain the earlier model discrepancy.

No target strain access. No outcome changes the registered C6 result. The
effective injection damps the whole 22/44 harmonic, so its overtones share
that harmonic's imposed Gamma. Other harmonics are unmodified in this control.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.interpolate import CubicSpline
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction,scales
from tgl_ringdown_likelihood import linear_statistics,profile_intervals

ROOT=Path(__file__).resolve().parent
GROUPS={
    '220_440':[(2,2,0),(4,4,0)],
    '220_221_440':[(2,2,0),(2,2,1),(4,4,0)],
    '220_221_222_440':[(2,2,0),(2,2,1),(2,2,2),(4,4,0)],
    'six_modes':[(2,2,0),(2,2,1),(2,2,2),(2,1,0),(3,3,0),(4,4,0)],
    'eight_modes':[(2,2,0),(2,2,1),(2,2,2),(2,1,0),(3,3,0),(4,4,0),(4,4,1),(5,5,0)]}

def control_modes(family):
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']
    exact={}
    for ell in (2,4):
        g=grid[str(ell)*2+'0']
        exact[(ell,ell,0)]=complex(CubicSpline(g['spins'],np.array(g['real'])+1j*np.array(g['imag']))(family['remnant_spin']))
    extra=json.loads((ROOT/'C5_EXTRA_QNMS.json').read_bytes())['rows']
    for r in extra:
        if r['family']==family['family']:exact[tuple(r['mode'])]=complex(r['omega_real'],r['omega_imag'])
    return exact

def mode_basis(times,family,reading,modes,agrid,exact):
    mass=family['remnant_mass_detector_solar'];spin=family['remnant_spin']
    tm=scales(mass,'CODATA2018_IAU2015')[0]
    gamma={ell:prediction(mass,spin,reading,mode=(ell,ell,0),qnm_dimensionless=exact[(ell,ell,0)])['gamma_per_s'] for ell in (2,4)}
    columns=[]
    for mode in modes:
        w=exact[mode];frequency=w.real/tm;decay=-w.imag/tm
        extra=gamma[mode[0]] if mode[:2] in ((2,2),(4,4)) else 0.
        total=decay+np.asarray(agrid)*extra
        if np.any(total<=0):raise ValueError('Diagnostic deformation gives growing mode')
        envelope=np.exp(-total[:,None]*times[None,:])
        columns.extend([envelope*np.cos(frequency*times),envelope*np.sin(frequency*times)])
    return np.stack(columns,axis=-1)

def main():
    families=json.loads((ROOT/'C5_IMR_CONTROLS.json').read_bytes())['families']
    caches={d:np.load(ROOT/f'cache/empirical_noise/{d}_noise.npz') for d in ('H1','L1')}
    ws={d:caches[d]['whitener_scaled'] for d in caches};times=np.arange(ws['H1'].shape[1])/2048.
    responses={'H1':(.7,.2),'L1':(-.3,.8)};rows=[]
    for family in families:
        exact=control_modes(family);mass=family['remnant_mass_detector_solar'];spin=family['remnant_spin']
        maxx=max(prediction(mass,spin,'R-B',mode=(ell,ell,0),qnm_dimensionless=exact[(ell,ell,0)])['x'] for ell in (2,4))
        agrid=np.unique(np.r_[np.linspace(-.8,2.,1201)/maxx,0.,1.])
        waveform=np.load(ROOT/'cache/imr_controls'/f"{family['family']}.npz")
        for label,modes in GROUPS.items():
            raw=mode_basis(times,family,'R-B',modes,agrid,exact)
            bases={d:np.einsum('kt,gti->gki',ws[d],raw,optimize=True) for d in ws}
            zero=int(np.flatnonzero(agrid==0.)[0]);step=.001
            slope=(mode_basis(times,family,'R-B',modes,[step],exact)[0]-mode_basis(times,family,'R-B',modes,[-step],exact)[0])/(2*step)
            slopes={d:ws[d]@slope for d in ws}
            for start in (6.,8.,10.,10.5,12.,20.):
                tp=times+start*scales(mass,'CODATA2018_IAU2015')[0]
                for content in ('22_ONLY','FULL_IMR'):
                    prefix='22_' if content=='22_ONLY' else 'all_'
                    plus=np.interp(tp,waveform['time_from_peak_s'],waveform[prefix+'plus'])*1e21
                    cross=np.interp(tp,waveform['time_from_peak_s'],waveform[prefix+'cross'])*1e21
                    signals={d:ws[d]@(fp*plus+fc*cross) for d,(fp,fc) in responses.items()}
                    norm=np.sqrt(sum(np.dot(x,x) for x in signals.values()))
                    prof=sum(linear_statistics(bases[d],signals[d]*40/norm,10.)[0] for d in ws)
                    fit=profile_intervals(agrid,prof)[0]
                    residual=float(40**2-2*np.max(prof))
                    if residual<-.001:raise ValueError('Numerically impossible negative squared residual')
                    fisher=0.
                    for d in ws:
                        base=bases[d][zero];target=signals[d]*40/norm
                        coefficients=np.linalg.lstsq(base,target,rcond=None)[0]
                        derivative=slopes[d]@coefficients
                        orthogonal=derivative-base@np.linalg.lstsq(base,derivative,rcond=None)[0]
                        fisher+=float(np.dot(orthogonal,orthogonal))
                    rows.append(dict(family=family['family'],start_tM=start,content=content,fit=label,
                        a_hat=fit['MLE'],profile_boundary=fit['boundary'],residual_norm_squared=residual,
                        local_z_R_B_at_SNR40=float(np.sqrt(fisher)),local_sigma_a=float(1/np.sqrt(fisher)),
                        fisher_scope='Projection against all free mode quadratures at a=0; remnant held fixed, not an event significance'))
            print(json.dumps(dict(family=family['family'],fit=label,primary=[r for r in rows if r['family']==family['family'] and r['fit']==label and r['start_tM']==10.])),flush=True)
    atomic_json(ROOT/'C5_OVERTONE_ABLATION.json',dict(status='OVERTONE_MODEL_ADEQUACY_MEASURED',results=rows,
        scope='Noiseless a=0, fixed true remnant and SNR40. Higher-mode amplitudes are unconstrained nuisance coefficients. This is adequacy diagnosis, not validation of empirical coverage or physical dephasing.',
        shared_harmonic_rate='22 overtones share the imposed 22 Gamma, 44 overtone shares 44 Gamma, other harmonic rates zero to match the declared manufactured injection',
        accessed_target_strain=False,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))

if __name__=='__main__':main()
