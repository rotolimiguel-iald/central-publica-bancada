# Conditional nonlinear-source evidence: mathematical and numerical scope

This is a research implementation for the conditional whole-harmonic ringdown
model. It does not identify a physical clock, partition or stochastic unraveling.
It does not modify the frozen actual-strain experiment (`REGISTRO_C6.json`).
Pilot Bayes ratios require convergence and source-calibration checks before use.

## One physical integral, several computational proposals

The physical source coordinates remain detector-frame total mass, mass ratio,
two aligned spins, inclination, orbital reference phase and peak time shift.
Their proper priors are those in `REGISTRATION.json`. The amplitude pair is
shared by both detectors and has the same Gaussian prior throughout; its radial
interpretation is inverse-Rayleigh distance, not uniform spatial volume.
Known sky response and zero transverse spins are conditioning assumptions.

For hypothesis strength `a`, the desired component evidence is

`Z_a(d) = integral_[0,1]^6 [integral_0^(2pi) L_marg(d | u,phi,a) dphi/(2pi)] du`.

`L_marg` has already integrated the two common amplitude/polarization
coefficients. Complete source waveforms, their intrinsic complex-22 peak and
the same detector covariance are used at every source point. Every mock datum
has its own evidence. Averaging targets to train a proposal is computational;
their likelihoods are never multiplied as if the injections were events.

The phase integral is an average of **likelihoods**, not of waveforms. It is
Bayesian treatment of an unknown orbital phase, not physical dephasing.
Both orbital branches and all generated harmonics are retained. Fourier banks
accelerate only this phase integration; the six sampled source coordinates
still trigger direct full-waveform generation. Held-out phases and doubled
quadrature grids check this representation.

## Frequency/damping coordinates preserve the source prior

Write `M_f = M F(q,s1,s2)` and `chi_f = chi(q,s1,s2)`. With the inherited QNM
spline `w(chi) = w_R - i w_I`, where `w_I>0`, define

`y0 = log(f220/F0)`, `y1 = log(tau220/T0)`,
`f220 = w_R / (2pi t_Mf)`, `tau220 = t_Mf / w_I`.

`F0=250 Hz` and `T0=0.004 s` are coordinate units, not physical dephasing clocks.
The other coordinates are `u_q,u_spin2,u_cosi,u_t0`. Spin1 is recovered from
the quality factor and total mass from the frequency, with the original prior
bounds checked on inversion. No source parameter is fixed by this change.

Taking the determinant in `(M,s1)`, all derivatives of the remnant mass fraction
cancel because its logarithm enters frequency and damping with opposite signs:

`abs det d(log f,log tau)/d(M,s1)`
`= (1/M) (dchi/ds1) d[log(w_R/w_I)]/dchi`.

The original uniform intervals have widths60 solar masses and0.8 in spin1.
Thus the absolute forward Jacobian from the six unit-prior coordinates is

`J(u) = (48/M) (dchi/ds1) d[log(w_R/w_I)]/dchi`.

This identity is algebraic under differentiability and the invertibility
conditions. The remnant fit, spline, inverse and derivatives used here are
checked numerically, including a monotonicity grid, independent finite-difference
determinants and conditional prior moments. These checks are not presented as
a formal global theorem about either waveform approximant.

## Full support and rejected proposals

The proposal in transformed coordinates is

`q_y(y) = 0.1 * indicator_original_domain(y)/J(u(y)) + 0.9 * g(y)`,

where `g` is a normalized heavy-tailed Student-t mixture learned from previous
pilots. Inside the physical domain, `q_u(u)=J(u) q_y(y(u))` and the importance
weight is `L_phase(u)/q_u(u)`. The original-prior component retains full support.
Proposal fitting does not change a physical prior or likelihood.

Points without a physical inverse have zero integrand and remain in the total
draw count. The arrays preserve their actual proposed `y`, a cemetery mask,
and an explicit nonphysical sentinel in the unit-coordinate field. There is no
hidden rejection-normalization. Never treat the sentinel as a binary source.

The prior-moment oracle tests the normalization and twelve first/second moments
using fresh independent draws. It does not test astrophysical convergence.
New source integrations use new draws after their proposal is frozen. Old
training samples are not recycled into an allegedly independent validation.

## Continuous strength and resolution

`continuous_phase_source.py` implements

`h_a = h_all + (exp(-a Gamma220 t)-1) h22`
`             + (exp(-a Gamma440 t)-1) h44`.

Damping acts before detector whitening. This is the inherited conditional
whole-harmonic injection, not a separate derivation for every overtone.
The API alone selects no continuous-strength prior. Negative strength in
validation is a phenomenological numerical control, not a physical GKLS claim.

Pointwise resolution checks at SNR40,200,600 retain the original injected
waveforms and vary recovery generation rates. They can reveal recovery error;
they cannot establish injection accuracy at higher SNR or posterior coverage.
Errors at selected source points must not be confused with errors over the
posterior region. Both need the appropriate controls before acceptance.

## Evidence acceptance

The frozen numerical criteria include effective sample size at least100 for
each component, largest normalized weight at most0.05, paired Monte Carlo
uncertainty in log Bayes ratio at most0.2, independent repetitions and waveform
rate controls. The paired uncertainty retains covariance between the two
hypothesis estimates. Its delta-method approximation is unreliable when one
sample dominates; a small reported error cannot override low ESS.

These numerical checks do not replace the source-model bias/coverage tests.
Passed coordinate or density controls are not accepted Bayes factors, physical
confirmation, or a conversion to frequentist significance. Results and failed
attempts remain in their dated run directories; read the latest receipt before
starting a computation. Scripts that produce frozen artifacts are create-once.
