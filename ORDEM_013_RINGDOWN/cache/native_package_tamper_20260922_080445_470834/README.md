# Native SEOB conditional ringdown waveform

TGL: Luiz Antonio Rotoli Miguel. External GR generator: LALSuite/PyCBC.
Research supplement; no event significance or calibrated source evidence claimed.

## Model and limits

The generator retains the complete SEOBNRv4HM (SEOB41) mode set: positive
22,21,33,44,55 and the corresponding negative-m partners. For a supplied
conditional reading L and nonnegative strength a,

    h_a = h_all + (exp(-a Gamma_220 t)-1) h_22
                  + (exp(-a Gamma_440 t)-1) h_44.

The rates are calculated from the supplied prediction module using runtime
beta=ALPHA_FINE_CODATA_2018*sqrt(e), family-specific remnant and supplied exact
Kerr QNM interpolation grid. This is an effective whole-harmonic ENSEMBLE
envelope. It is not a derivation of a unique classical realization, a unique
overtone prescription or the physical modular partition/clock. A coherent-state
initial-slope prediction is explicitly rejected as a full exponential waveform.
The R-B mass clock, R-RAIZ-0 positive oscillator, R-LIN bridge and R-MOD restricted
corotating clock retain their respective INPUT/CONJECTURE scopes in metadata.
No default reading is selected and no physical rate is fitted here.

The peak is the phase-zero face-on intrinsic complex22 amplitude maximum.
Projection into inclination and orbital phase happens after constructing the
native modes. All other harmonics remain unchanged. Distance/polarization are
shared physical factors for the complete signal; there is no per-mode fitting.

## Use

With Python3.12, PyCBC2.11.0, LALSimulation6.2.1, NumPy2.3.5 and SciPy1.16.3:

```python
import numpy as np
from tgl_native_ringdown import prepare_ringdown, polarizations

# Detector-frame binary mass, mass ratio, aligned spins, inclination,
# orbital phase and peak displacement in milliseconds.
x = [np.log(90.), np.log(2.), .25, -.15, .9, 1.2, 0.]
times = .0034 + np.arange(410)/2048.
prepared = prepare_ringdown(x, times, sample_rate=8192)
hp, hc, metadata = polarizations(prepared, reading='R-B', strength=1.,
                                 distance_mpc=403., polarization_rad=.45)
```

hp,hc are dimensionless strain at the common luminosity distance in Mpc.
times are seconds after the specified intrinsic peak; the entire shifted
interval must be after it. Detector strain is F_plus*hp+F_cross*hc with whatever
sky response and time delay the consumer has explicitly supplied. The consumer
must provide its own likelihood, priors, detector noise and inference checks.
`prepared` may be reused across strengths/readings/orbital phases; it is only
a numerical representation, not a prior or a posterior.

## Reproduction and numerical scope

Run `python -B reproduce.py`. It verifies all packaged hashes and the LAL commit,
regenerates three sources at8192/16384Hz, compares four conditional readings,
three strengths and two distance/polarization choices against complete PyCBC
waveforms, then exercises six rejection cases. It writes a fresh cache directory.
It needs no original workspace, private file, task memory, network access,
canonical um.py or event strain. No dependencies are installed by the runner.

Selected-source high-resolution tests in the parent study still exceed the
registered log-likelihood tolerance at SNR200/600, even after actual internal-mesh
refinement. Output sample rate is not automatically internal solver resolution.
This package exposes the measured internal step in metadata and does not claim
high-SNR convergence or calibrated five-sigma sensitivity. Source-integrated
statistical precision, independent repeats and posterior coverage remain open.

The original failed mode reconstruction and corrected provenance remain in
the parent research records. Native helper bodies were copied verbatim and
AST-checked; task-only validation imports were removed. Bundled model files
are byte-identical copies, identified by the included provenance manifest.
LALSuite/PyCBC are external dependencies; their code is not bundled here.
