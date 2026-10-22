# Conditional TGL ringdown research package

Internal handoff for independent review; not a publication or physical-confirmation claim.
TGL theory: Luiz Antonio Rotoli Miguel. This package audits conditional predictions
against public LIGO/Virgo/KAGRA data. It does not select a physical clock or unraveling.
The source program audited was the task's frozen local v369; the public/app v368 is
a different artifact. Neither program nor the canonical kernel is modified or shipped here.

## Quick start

Use a fresh virtual environment. The core source functions need only NumPy:

```sh
python -m pip install -r requirements-minimal.txt
python verify_manifest.py
python run_demo.py --output
```

The demo writes a waveform CSV and predictions for a fixed illustrative source.
It is not an observational fit. `tables/event_reading_predictions.csv` has
264 event/reading rows from the measured posterior analysis, with explicit
scope and source hashes. These medians are examples; posterior evidence integrates
mass/spin correlations and is not simply a likelihood at the median.

## Law, units and observables

For a diagonal self-adjoint jump L=f(H), coherence ij decays at
`Gamma_ij = (f(E_i)-f(E_j))^2 / 2`. The jump count `Tr(L†L rho)` is not that rate.
The positive-root formula requires a positive generator; a bilateral modular
`-log Delta` is not silently replaced by a positive matrix.

For the conditional energy-dephasing oscillator,
`Gamma = beta*tau_star*omega^2/2`, with beta computed as
`ALPHA_FINE_CODATA_2018*sqrt(e)` at runtime. Gamma is an ensemble AMPLITUDE rate,
not energy loss. With `x=Gamma*tau_GR`, the exact extra damping is
`delta_tau = -x/(1+x)` and `delta_f=0` for the deterministic ensemble template.

In the existing mass-clock reading B, put `t_M=G*M_detector/c^3`,
`omega=w(spin)/t_M`, `tau_GR=t_M/d(spin)`. Then
`Gamma=beta*w^2/(2*t_M)` and `Gamma/omega=beta*w/2`.
Distance changes received amplitude/SNR and, through cosmology, source/detector
conversion. It does not by itself change a local source rate. Source clocks
redshift by `(1+z)`. A propagation integral is a separate conditional model.

The coefficient of 1/s cannot be inferred from a bare dimensionless modular
operator without a clock identification. The quoted enormous rate proportional
to `GM/c^3` mistakes a time for an inverse time; it is not a physical exclusion.

| Reading | Assumption/status | Effective rate |
|---|---|---|
| R-A | INPUT Planck clock | beta*(1+z)*t_P*omega²/2 |
| R-B | INPUT mass clock, existing program branch | beta*t_M*omega²/2 |
| R-RAIZ-0 | Conditional vacuum-to-one coherence | beta*omega/2 |
| R-RAIZ-EP4 | INPUT positive offset E_P/4 | positive-root gap squared/2 |
| R-RAIZ-REST | CONJECTURE rest-energy offset | positive-root gap squared/2 |
| R-RAIZ-COHERENT | CONJECTURE oscillator occupation and readout | Poisson mixture, not one exponential |
| R-LIN | CONJECTURE physical clock for linear-gap law | beta*omega |
| R-MOD | CONJECTURE management hypothesis, not TGL canon | beta*(2*pi/kappa)*(omega-m*Omega_H)²/2 |
| R-GLOBAL | Conditional common system/reference time noise | zero relational phase decoherence |
| R-PROP | CONJECTURE independent local FLRW time noise | spectral exponent, not extra ringdown rate |

R-MOD restricts to an explicitly positive corotating mode and requires an exact
QNM; it does not assume a global Kerr Hartle–Hawking state. The core refuses
negative-spin BCW extrapolation and requires supplied exact frequencies for
every mode other than 220. Higher-mode angular factors must also be supplied;
the 220 inclination pattern is never silently reused.

## Source functions and conventions

`tgl_ringdown_prediction.prediction(M_detector, spin, reading, ...)` returns
rates, ratios and exact ensemble shifts. Default constants are CODATA2018/IAU2015;
`LEGACY_V346` is an explicit, distinct regression profile.

`tgl_ringdown_template.ringdown(time, M_detector, spin, reading, A, ...)`
returns `{'plus': array, 'cross': array}`. Time is in seconds, frequency in Hz,
mass in detector-frame solar masses, strain dimensionless, mode phase in radians.
Onset is explicit. Plus uses cosine, cross sine; `h_plus-i*h_cross` has the
negative-frequency circular convention for face-on orientation. Sum explicitly
specified modes. This is not a complete modified-gravity inspiral/merger.

`deformation=0` is the GR limit; `deformation=1` is the specified reading.
It multiplies Gamma, not beta. Physical template calls refuse negative dephasing.
Negative a in injection profile diagnostics is a separate, visibly marked estimator.

`tgl_ringdown_unravelings.conditional_ringdown` adds `cauchy_phase` for R-LIN,
and finite-N `ensemble` or `quantum_wiener` for R-RAIZ-COHERENT. Stochastic calls
require a seed. The exact Poisson sum supports `0<N<=4096` with a tail bound;
larger occupations are refused, not replaced by the large-N slope silently.
An occupation needs its own excitation/quantization assumption.

Brownian and Cauchy phase processes can share the same first-coherence mean,
but have different higher-harmonic laws. Pure phase paths preserve their modulus.
For a root-generator quantum trajectory, `|<a>|²` may change although oscillator
number is conserved. The density generator alone does not choose observed strain.

Bilby: use `WaveformGenerator(time_domain_source_model=conditional_ringdown,
parameter_conversion=lambda p:(dict(p),[]), waveform_arguments=...)`;
put fitted parameters and reading in `parameters`, fixed observable/seed/exact-QNM
options in `waveform_arguments`. Actual Bilby 2.8.2 consumer controls passed.
PyCBC: wrap the arrays with `TimeSeries(delta_t=..., epoch=...)`.
This is not a pyRing likelihood plugin.

## What the observations and controls support

The registered GW250114 H1/L1 220+440 experiment, primary start 10 t_M and
amplitude prior sd 1e-20 strain, gave **ln B(B/GR)=-0.002595070**.
Its status is **INCONCLUSIVE_SYSTEMATICS**, since the two-IMR-family calibration
did not pass. All five starts and three amplitude priors remain in the evidence
file; overlapping starts and analyses of the same event must not be multiplied.

The full 220+440 posterior, the 220-only sector posterior, and pyRing use different
models and priors. The saved JSONs identify those scopes. The catalogue result is
also INCONCLUSIVE_SYSTEMATICS under its registered GR-relative criterion.
NOT_EXCLUDED does not mean CONFIRMED. None of these Bayes ratios is a sigma count.

The O4/O5/ET/CE reference experiment contains 4608 cells,
50 paired held-out O4 intervals per cell, two IMR families, three mode sets,
eight readings and six SNRs. The same intervals are reused; this is not that many
independent observed events. The hypothetical channels share a reference PSD
and fixed response factors, not an actual future detector network geometry.

O5 means the A+ design curve here, not an achieved sensitivity or scheduled run.
ET and CE are also design scenarios. Noise is transported in a finite polynomial
quotient with an explicit Cholesky convention; future non-Gaussian noise is unknown.
Low-frequency extrapolation controls are retained. Matched-ringdown injections
calibrate numerical recovery separately from full-IMR model mismatch.

Adding overtones reduces waveform discrepancy but also erases information on
dephasing when their amplitudes are free. In the eight-mode O5 SNR40 control,
the small positive mean log ratio is also present in noise-only injections:
proper prior volume, not a detection. The report includes that control. All
forecasts fix the true remnant and are optimistic about mass/spin information.
The local Fisher number of ideal identical events for 5 sigma is not a prediction
of a real catalogue or a conversion of ln B to sigma.

## Recompute the actual-strain measurement

```sh
python -m pip install -r requirements-reproduction.txt
python reproduce_c6.py                 # verifies the frozen receipt and inputs
python reproduce_c6.py --run --download
```

The second command downloads about 82 MB of public H1/L1 strain, checks hashes,
then computes every registered start/refinement from strain in a separate folder.
Alternatively supply `--source-cache /path/to/verified/on_source` instead of
`--download`. Use a fresh copy to demonstrate all windows are newly computed;
the original orchestrator reuses matching results on subsequent runs and reports
this explicitly. The wrapper compares all rows with `evidence/C6_RESULTS.json`.
The raw HDF5 files and generated outputs are not in the shipped-file manifest.

Registration, exact input hashes and its delivered receipt are preserved byte
for byte under `reproduction/`. Degree-2 polynomial nuisance directions are
removed only within each cut interval. Original 4096-Hz PSD alias power is
included at retained 2048-Hz sample lags. Amplitude integrals retain their
Gaussian prior determinants; remnant mass/spin are marginalized, not fixed in C6.
The PSD and 256 held-out intervals per detector are included as derived inputs;
their raw off-source regeneration and full posterior-release analysis are not
automated by this small package yet. See the remaining-work note.

## Provenance and remaining work

The copied evidence is a dated record, not an update of old script hashes.
Compatibility of current prediction code with earlier 264 catalogue predictions
was measured separately. The C6 frozen code is independent of the optional new
readouts. Hashes identify files; they do not certify a mathematical claim.

Public observations: LIGO Scientific Collaboration, Virgo Collaboration and
KAGRA Collaboration; source URLs, DOIs, checksum receipts and release attribution
remain in the supplied evidence and original audit. GWOSC target URLs are in
`reproduction/ORDEM_013_RINGDOWN/C6_DOWNLOADS.json`.
This handoff does not distribute the private canonical program or credentials.

**Still open in the overall task:** a unique physical partition/clock and strain
unraveling are not selected by these measurements; model adequacy is conditional;
an older GWTC-3 release must be reconciled without duplicate events; three failed
full-text literature fetches remain visible; full posterior/injection regeneration
is not yet a one-command independent workflow. No gate or experimental-confirmation
status is changed by this package.
