"""Independent Gaussian integral, PSD simulation and matched-signal controls."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.linalg import cholesky,solve_triangular
from scipy.interpolate import CubicSpline
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction
from tgl_ringdown_likelihood import linear_statistics,profile_intervals

ROOT=Path(__file__).resolve().parent

def main():
    rng=np.random.default_rng(130529)
    basis=rng.normal(size=(9,2)); data=rng.normal(size=(5,9));sd=1.7
    profile,marginal=linear_statistics(basis,data,sd)
    covariance=np.eye(9)+sd**2*basis@basis.T
    direct=-.5*np.einsum('di,ij,dj->d',data,np.linalg.inv(covariance)-np.eye(9),data)-.5*np.linalg.slogdet(covariance)[1]
    integral_error=float(np.max(abs(direct-marginal[0])))
    coeff=np.linalg.lstsq(basis,data.T,rcond=None)[0]
    direct_profile=.5*(np.sum(data**2,axis=1)-np.sum((data.T-basis@coeff)**2,axis=0))
    profile_error=float(np.max(abs(direct_profile-profile[0])))
    if max(integral_error,profile_error)>1e-12:raise ValueError('Gaussian likelihood oracle failed')
    # Numerical quadrature of the actual two-dimensional amplitude integral.
    from scipy.integrate import dblquad
    sample=data[0]
    integrand=lambda b,a: np.exp(-.5*np.sum((sample-basis@np.array([a,b]))**2)+.5*np.dot(sample,sample)
                                -(a*a+b*b)/(2*sd*sd))/(2*np.pi*sd*sd)
    value,error=dblquad(integrand,-12*sd,12*sd,lambda _: -12*sd,lambda _:12*sd,epsabs=1e-10,epsrel=1e-9)
    quadrature_error=float(abs(np.log(value)-marginal[0,0]))
    if quadrature_error>1e-7:raise ValueError('Numerical amplitude integral failed')
    diagnostics=[]
    caches={d:np.load(ROOT/'cache/empirical_noise'/f'{d}_noise.npz') for d in ('H1','L1')}
    for detector,cache in caches.items():
        w=cache['whitener_scaled'];psd=cache['median_psd_strain']*1e42
        nfft=2*(len(psd)-1); fs=4096
        spectrum=(rng.normal(size=(256,len(psd)))+1j*rng.normal(size=(256,len(psd))))*np.sqrt(nfft*fs*psd/4)[None,:]
        spectrum[:,[0,-1]]=rng.normal(size=(256,2))*np.sqrt(nfft*fs*psd[[0,-1]]/2)[None,:]
        realization=np.fft.irfft(spectrum,n=nfft,axis=1)[:,::2][:,:w.shape[1]]
        independent=realization@w.T
        energy=float(np.mean(independent**2))
        # Polynomial invariance must hold on vectors before any observed fit.
        polynomial=np.polynomial.legendre.legvander(np.linspace(-1,1,w.shape[1]),2)
        invariance=float(np.linalg.norm(w@polynomial)/(np.linalg.norm(w)*np.linalg.norm(polynomial)))
        if abs(energy-1.)>.03 or invariance>1e-12:raise ValueError('Whitening/quotient independent oracle failed')
        diagnostics.append(dict(detector=detector,independent_frequency_noise_reduced_chisquare=energy,polynomial_relative_residual=invariance))
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']
    qs=[CubicSpline(grid[k]['spins'],np.array(grid[k]['real'])+1j*np.array(grid[k]['imag']))(.68) for k in ('220','440')]
    pred=[prediction(68.1,.68,'R-B',mode=m,qnm_dimensionless=complex(q)) for m,q in zip(((2,2,0),(4,4,0)),qs)]
    decay=np.array([1/p['tau_gr_s'] for p in pred]);gamma=np.array([p['gamma_per_s'] for p in pred]);omega=np.array([p['omega_rad_s'] for p in pred])
    agrid=np.unique(np.r_[np.linspace(-.8,2.,1001)/max(gamma/decay),0.,1.])
    t=np.arange(caches['H1']['whitener_scaled'].shape[1])/2048
    env=np.exp(-(decay[None,:]+agrid[:,None]*gamma[None,:])[:,:,None]*t[None,None,:])
    raw=np.stack([env[:,0,:]*np.cos(omega[0]*t),env[:,0,:]*np.sin(omega[0]*t),env[:,1,:]*np.cos(omega[1]*t),env[:,1,:]*np.sin(omega[1]*t)],axis=-1)
    bases={d:np.einsum('kt,gti->gki',caches[d]['whitener_scaled'],raw,optimize=True) for d in caches}
    coefficients={'H1':np.array([1.,.3,.06,.01]),'L1':np.array([-.4,.8,-.01,.04])}
    controls=[]
    for injected in (0.,1.):
        idx=int(np.flatnonzero(agrid==injected)[0])
        signals={d:bases[d][idx]@coefficients[d] for d in caches}
        norm=np.sqrt(sum(np.dot(y,y) for y in signals.values()))
        for snr in (20.,40.,80.):
            for source in ('GAUSSIAN_IDENTITY','EMPIRICAL_HELD_OUT','NOISELESS'):
                curves=[]
                for d in caches:
                    if source=='GAUSSIAN_IDENTITY':noise=rng.normal(size=(256,bases[d].shape[1]))
                    elif source=='EMPIRICAL_HELD_OUT':noise=caches[d]['held_out_strain_scaled']@caches[d]['whitener_scaled'].T
                    else:noise=np.zeros((1,bases[d].shape[1]))
                    curves.append(linear_statistics(bases[d],noise+signals[d][None,:]*snr/norm,10.)[0])
                fits=profile_intervals(agrid,sum(curves))
                coverage=float(np.mean([r['CI90'][0]<=injected<=r['CI90'][1] for r in fits]))
                median=float(np.median([r['MLE'] for r in fits]))
                if source=='NOISELESS' and abs(median-injected)>.005:raise ValueError('Matched noiseless injection failed')
                controls.append(dict(injected_a=injected,SNR=snr,noise=source,N=len(fits),median_a=median,
                    bias_a=abs(median-injected),coverage90=coverage,boundaries=sum(r['boundary'] for r in fits)))
    result=dict(status='INDEPENDENT_LIKELIHOOD_ORACLES_PASS',integral_error=integral_error,
        profile_error=profile_error,numerical_quadrature_error=quadrature_error,
        PSD_simulations=diagnostics,matched_injections=controls,
        hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('tgl_ringdown_likelihood.py','prepare_empirical_noise.py','verify_likelihood_and_noise.py')})
    atomic_json(ROOT/'C5_LIKELIHOOD_VALIDATION.json',result)
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
