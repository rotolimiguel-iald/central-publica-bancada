"""Ablate harmonic content and nuisance modes without reading target strain.

The earlier registered C6 artifacts remain untouched. Late starts at fixed SNR
are shape diagnostics, not attainable SNR claims for the observed event.
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

def main():
    controls=json.loads((ROOT/'C5_IMR_CONTROLS.json').read_bytes())
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']
    modes={k:CubicSpline(v['spins'],np.asarray(v['real'])+1j*np.asarray(v['imag']),extrapolate=False) for k,v in grid.items()}
    noise={d:np.load(ROOT/f'cache/empirical_noise/{d}_noise.npz') for d in ('H1','L1')}
    ws={d:noise[d]['whitener_scaled'] for d in noise};t=np.arange(ws['H1'].shape[1])/2048.
    responses={'H1':(.7,.2),'L1':(-.3,.8)};rows=[]
    for family in controls['families']:
        path=ROOT/'cache/imr_controls'/f"{family['family']}.npz"
        if hashlib.sha256(path.read_bytes()).hexdigest()!=family['sha256']:raise ValueError('Source changed')
        waveform=np.load(path);mass,spin=family['remnant_mass_detector_solar'],family['remnant_spin']
        ps=[prediction(mass,spin,'R-B',mode=(ell,ell,0),qnm_dimensionless=complex(modes[str(ell)*2+'0'](spin))) for ell in (2,4)]
        omega=np.array([p['omega_rad_s'] for p in ps]);gamma=np.array([p['gamma_per_s'] for p in ps]);decay=np.array([1/p['tau_gr_s'] for p in ps])
        agrid=np.unique(np.r_[np.linspace(-.8,2.,1201)/max(gamma/decay),0.,1.])
        envelope=np.exp(-(decay[None,:]+agrid[:,None]*gamma[None,:])[:,:,None]*t[None,None,:])
        raw=np.stack([envelope[:,0,:]*np.cos(omega[0]*t),envelope[:,0,:]*np.sin(omega[0]*t),envelope[:,1,:]*np.cos(omega[1]*t),envelope[:,1,:]*np.sin(omega[1]*t)],axis=-1)
        basis={d:np.einsum('kt,gti->gki',w,raw,optimize=True) for d,w in ws.items()}
        for start in (6.,8.,10.,10.5,12.,20.,40.,60.,100.):
            ts=t+start*scales(mass,'CODATA2018_IAU2015')[0]
            components={key:np.interp(ts,waveform['time_from_peak_s'],waveform[key])*1e21 for key in ('22_plus','22_cross','44_plus','44_cross','other_plus','other_cross')}
            for content in ('22_ONLY','22_PLUS_44','FULL_IMR'):
                signals={}
                for d,(fp,fc) in responses.items():
                    y=fp*components['22_plus']+fc*components['22_cross']
                    if content!='22_ONLY':y=y+fp*components['44_plus']+fc*components['44_cross']
                    if content=='FULL_IMR':y=y+fp*components['other_plus']+fc*components['other_cross']
                    signals[d]=ws[d]@y
                norm=np.sqrt(sum(np.dot(y,y) for y in signals.values()))
                for fit in ('220_ONLY','220_PLUS_440'):
                    columns=2 if fit=='220_ONLY' else 4
                    profiles=[]
                    for d in ws:profiles.append(linear_statistics(basis[d][:,:,:columns],signals[d]*40/norm,10.)[0])
                    likelihood=sum(profiles)
                    estimate=profile_intervals(agrid,likelihood)[0]
                    best=float(np.max(likelihood))
                    mismatch_norm=float(max(0.,40**2-2*best))
                    rows.append(dict(family=family['family'],start_tM=start,content=content,fit=fit,
                        raw_network_SNR=float(norm),SNR_for_shape_test=40.,a_hat=estimate['MLE'],
                        residual_norm_squared=mismatch_norm,profile_boundary=estimate['boundary']))
        print(json.dumps(dict(family=family['family'],primary=[r for r in rows if r['family']==family['family'] and r['start_tM']==10.])),flush=True)
    atomic_json(ROOT/'C5_BIAS_ABLATION.json',dict(status='NOISELESS_HARMONIC_ABLATIONS_MEASURED',results=rows,
        scope='R-B injection a=0. No target strain accessed. Constant-SNR late starts diagnose waveform shape only.',
        original_C6_unchanged=True,source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('diagnose_imr_bias.py','C5_IMR_CONTROLS.json','tgl_ringdown_likelihood.py')}))

if __name__=='__main__':main()
