"""SEOB source integral using checked native modes and direct held-out phases.

Every evaluated source still faces the ORIGINAL complete waveform at three
off-grid phases. The stable phase-zero peak is a numerical refinement within
the registered tolerance, not a changed physical prior, clock or readout.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import native_seob_phase_source as native
import stable_peak_phase_source as api


def phase_marginal_loglikes(family,u,state,sample_rate=8192):
    if family!='SEOBNRv4HM':
        raise ValueError('Only SEOBNRv4HM is registered for this adapter')
    x=pm.six_to_physical(u)
    raw=native.raw_phase_samples(family,x,state['times'],sample_rate=sample_rate)
    # Shared between PSDs. This is the unchanged original PyCBC full waveform,
    # including its independently reoptimized peak at each held-out phase.
    direct={}
    for phase in (.173,.619,1.413):
        y=x.copy(); y[5]=phase
        direct[phase]=se.paired_polarizations(family,y,state['times'],sample_rate)[0]
    values=[[],[]]; max_wave=max_logl=max_quad=0.; largest=0
    for psd in ('O4','O5'):
        white,targets=state[psd+'_white'],state[psd+'_targets']
        bank=api.make_bank(raw,'R-B',[0.,1.],white)
        for phase,pairs in direct.items():
            for a in (0,1):
                exact=se.basis_from_polarizations(pairs[a],white)
                reconstructed=pc.evaluate_bank(bank,[phase],a)[0]
                relative=float(np.linalg.norm(exact-reconstructed)/np.linalg.norm(exact))
                _,ll=se.linear_statistics(exact,targets,3.)
                error=float(np.max(np.abs(ll-pc.bank_loglikes(bank,[phase],targets,a))))
                max_wave,max_logl=max(max_wave,relative),max(max_logl,error)
                if relative>1e-6 or error>.001:
                    raise ValueError(f'Native full-wave validation failed:relative={relative},logL={error},x={x.tolist()}')
        integrals,controls=api.marginal_loglikes(bank,targets)
        max_quad=max(max_quad,max(c['error'] for c in controls))
        largest=max(largest,max(c['phase_grid'] for c in controls))
        for a in (0,1):
            values[a].extend((integrals[a]-state[psd+'_centers']).tolist())
    result=np.asarray(values).ravel()
    if not np.all(np.isfinite(result)):
        raise ValueError('Nonfinite native phase-integrated likelihood')
    return result,dict(max_logL_interpolation_error=max_logl,
        max_relative_waveform_interpolation_error=max_wave,max_phase_quadrature_error=max_quad,
        largest_phase_grid=largest,native_high_step_M=raw['native_dynamics']['high_time_step_M'])
