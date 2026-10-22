# Conditional coherent IMR source controls

Research supplement, not an event significance or full source posterior.
TGL: Luiz Antonio Rotoli Miguel. Public waveform generators: LALSuite/PyCBC.

## What is new

The source varies nonlinearly in total mass, mass ratio, both aligned spins,
inclination, orbital phase and peak time. Distance and one polarization angle
are shared by the entire two-detector network. There are no independent fitted
amplitudes for each harmonic or detector.

Three simulated aligned binaries are dephased under the existing conditional
mass-clock reading B. GR candidates are found in both SEOBNRv4HM and the aligned
limit of IMRPhenomXPHM. These are local constructive mismatch bounds, not global
optimizer guarantees, Bayes ratios or bias/coverage calibration.

The corrected reference is the intrinsic complex-22 amplitude maximum, evaluated
face-on before projecting to the source orientation. The previous projected-norm
reference could jump between carrier peaks as resolution changed. The diagnostic
and provenance are included. Old C6 and all earlier runs remain unchanged.

## Physical and statistical scope

The effective ensemble envelope damps each entire 22/44 harmonic by its fundamental
Gamma; other harmonics are unchanged. This is an explicit conditional readout,
not a derivation of a unique overtone law or a choice of TGL partition/unraveling.
Beta is calculated by the supplied prediction module, never fitted here.

`coherent_imr_likelihood.py` additionally provides an exact two-coefficient
Gaussian marginalization for a supplied nonlinear source. Its prior is stated:
psi is uniform modulo pi and p(D)=403^2/(s^2 D^3) exp[-403^2/(2 s^2 D^2)], with
D in Mpc and s the common-amplitude prior sd. This is a proper input prior, NOT
uniform comoving volume. The intrinsic source still needs integration; no
full-source evidence is claimed by this supplement.

## Reproduce from actual generators

Tested runtime: Python 3.12, PyCBC 2.11.0, LALSimulation 6.2.1, NumPy 2.3.5,
SciPy 1.16.3. No private source, credentials, canonical um.py or event strain is
included. The noise metric was derived from public off-source strain and is
provided as a frozen array; prior public-data packages reproduce that step.

Run `python -B reproduce.py` using a Python that already has PyCBC/LAL/SciPy.
It checks every packaged hash, creates a fresh directory, checks the model and
distance/polarization integral, regenerates the 12 stored physical candidates
at 16384/32768 Hz, and independently verifies their residuals using QR.
It does NOT repeat the costly optimizer searches or claim independent external
review. Results are saved in the new run directory. Failures stay visible.

To repeat the searches themselves, use a separate new copy of the registered
inputs without a pre-existing `C5_NONLINEAR_COHERENT.json` or search checkpoints,
and run `python -B nonlinear_coherent_recovery.py run`. Original candidate seeds,
parameters and evaluation budgets are recorded and hashed. A local optimizer
budget exit is not a scientific acceptance test.

The reported five-sigma power bound is an analytic simple-pair Gaussian bound,
not an empirical tail measurement or a conversion of Bayes factor to sigma.
All hypotheses, onset conventions and limitations accompany the results.
