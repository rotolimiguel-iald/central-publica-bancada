import numpy as np
import pandas as pd

def augment_pyring_samples(samples, mode='221'):
    """Given a pandas DataFrame containing pyring samples, augment with the amplitude of the given mode in the detector."""
    x = samples['cosiota']
    ar = samples[f'A2{mode}_1']*(1+x)**2*np.sqrt(5/(64*np.pi))
    al = samples[f'A2{mode}_2']*(1-x)**2*np.sqrt(5/(64*np.pi))

    a = ar + al

    samples[f'A2{mode}_R'] = ar
    samples[f'A2{mode}_L'] = al
    samples[f'A2{mode}'] = a

def pyring_prior_rewight(samples, mode='221'):
    """Produce the weight factor required to re-sample the PyRing results to a flat prior in the given mode."""
    x = samples['cosiota']
    a = samples[f'A2{mode}']

    return 2*(x**2 - 1)**2/a

def resample_pyring_samples(samples, mode='221', rng=np.random.default_rng()):
    """Compute weights and then resample the PyRing samples to a flat prior in the given mode."""
    weights = pyring_prior_rewight(samples, mode=mode)
    neff = np.sum(weights)**2 / np.sum(weights**2)
    inds = rng.choice(len(samples), size=int(round(neff)), p=weights/np.sum(weights), replace=True)
    return samples.iloc[inds].reset_index(drop=True)
