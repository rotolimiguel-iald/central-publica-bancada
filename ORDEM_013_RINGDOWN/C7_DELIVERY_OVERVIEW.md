# Conditional TGL ringdown: consolidated delivery

Internal research handoff for independent review. TGL: Luiz Antonio Rotoli Miguel. This addendum consolidates the delivered packages; earlier files remain dated records. It does not select a physical clock, partition or strain unraveling. It does not change a mathematical gate or claim physical confirmation.

## Four requested results

1. **Functional law.** For a self-adjoint jump L=f(H), Gamma_ij=(f(E_i)-f(E_j))^2/2. For the conditional oscillator with the quadratic energy generator, Gamma=beta*tau_star*omega^2/2. For the existing mass-clock reading B, tM=G*M_detector/c^3 and Gamma=beta*w(spin)^2/(2*tM). Distance affects amplitude/SNR and cosmological frame conversion, not the local source rate. Propagation over D is a separate, explicitly conditional spectral model.
2. **Size relative to QNM frequency.** The following entries are evaluated at the released GW250114 posterior medians. They are conditional examples, not fitted beta or proof of the clock identification. Beta is computed at runtime as ALPHA_FINE_CODATA_2018*sqrt(e).

| Reading | Gamma [1/s] | Gamma/omega | Exact ensemble delta_tau |
|---|---:|---:|---:|
| R-A | 8.60125759e-40 | 5.499614e-43 | -3.51878648e-42 |
| R-B | 4.94916297 | 0.00316447749 | -0.0198452854 |
| R-RAIZ-0 | 9.40832518 | 0.0060156502 | -0.0370630481 |
| R-RAIZ-EP4 | 8.60125759e-40 | 5.499614e-43 | -3.51878648e-42 |
| R-RAIZ-REST | 3.73707799e-80 | 2.38947459e-83 | -1.52884382e-82 |
| R-LIN | 18.8166504 | 0.0120313004 | -0.0714769429 |
| R-MOD | 9.27534086 | 0.00596126066 | -0.0368397228 |
| R-GLOBAL | 0 | 0 | -0 |

Gamma is an amplitude/coherence rate. The ensemble waveform is A exp[-(1/tau_GR+Gamma)t] cos(omega*t+phi), with delta_tau=-x/(1+x), x=Gamma*tau_GR. Energy dephasing conserves oscillator populations. Single stochastic phase realizations need not have that deterministic envelope. A coherent root-generator field is generally a Poisson mixture, not one exponential. A bare signed -log Delta cannot be square-rooted as a positive operator without specifying a positive extension.

3. **Expected Bayes ratios.** O4/O5 forecasts are distributions conditioned on sensitivity, SNR, waveform family, mode content, readout and priors. For the illustrative SEOBNRv4HM, O5 A+ curve, SNR40, 220+440 FULL_IMR experiment:

| Injection | Mean ln B(B/GR) | Standard deviation |
|---|---:|---:|
| a=0 | -0.131420444 | 0.42706783 |
| a=1 | 0.0154296244 | 0.426759243 |

The full matrix has 4608 cells, 50 paired off-source intervals each, two IMR families, three recovery mode sets and six SNRs. Noise intervals are reused across cells. Remnant mass/spin are fixed in this forecast: it is optimistic. **0 FULL_IMR groups passed the requested bias/coverage criteria for both families and both injected amplitudes.** Numerical SVD checks passed; scientific calibration did not. No selected positive log ratio is promoted to detection. O5/ET/CE use design scenarios, not measured future noise or a schedule.

4. **Waveforms for independent fits.** C7_INDEPENDENT contains the NumPy prediction, waveform and optional stochastic/finite-occupation APIs, explicit phase/polarization/onset conventions and a working Bilby consumer example. It is a ringdown model, not a complete modified-gravity inspiral-merger template. Other modes require exact QNMs and supplied angular projections.

## Actual-data confrontation

| Dataset / scope | ln B(B/GR) | Interpretation |
|---|---:|---|
| GW250114 H1/L1 strain, registered primary start 10 tM | -0.0025950697721 | INCONCLUSIVE_SYSTEMATICS; amplitude prior sd 1e-20 |
| Newer catalog, published 31-event selection, conditional 220 sector | -1.80827845748 | INCONCLUSIVE_SYSTEMATICS |
| GWTC-3, paper Table 13 minus author exclusions, 10 events | -0.820833771606 | INCONCLUSIVE_SYSTEMATICS |

These rows are **not independent measurements to multiply**. The catalogs share events and GW250114 is in the newer catalog. Thirty-three newer and eighteen older posterior products were inspected, with twelve overlaps. The all-eighteen older combination remains an auxiliary control, not the publication selection. Joint frequency/damping densities, sample-dependent spin predictions, bandwidth/bootstraps, marginal diagnostics and two free-clock priors are recorded. Common-deformation catalog GR checks fail the registered acceptance condition, so the catalog status remains inconclusive. Some newer-event tail densities also lack sufficient local support.

The registered strain experiment marginalizes remnant mass/spin and detector amplitudes. All five starts and three amplitude priors are retained. Comparison with eight released pyRing products is a model comparison, not exact reproduction: no 10.5 tM product was released and trigger, PSD, mode and prior conventions differ. Original sampler/remnant-postprocessing and some pyRing merging provenance are unavailable. Bayes factors are not frequentist sigma.

## Reproduction entry points

| Package | Command after unpacking | Scope |
|---|---|---|
| C7_INDEPENDENT | `python run_demo.py --output`; `python reproduce_c6.py --run --download` | Waveform demo and frozen actual-strain measurement |
| C7_POSTERIOR_REPRODUCTION | `python reproduce.py primary --download` (also joint, free_clock, catalog) | Recompute posterior analyses from public samples |
| C7_INJECTION_REPRODUCTION | `python reproduce.py full --download --imr-python /path/to/pycbc/python` | Regenerate IMR, off-source PSD/noise and injection forecast |
| C7_GWTC3_REPRODUCTION | `python reproduce.py full --download` | Older release, literal paper selection and separate joint diagnostic |

Each package README gives tested dependencies, source/archive-cache alternatives and file hashes. Use fresh directories. Reproduction receipts are checks of the implemented calculations, not independent physical confirmation. The original LVK samplers are not rerun. This round exercised verified local sources/archives; it did not re-fetch every download URL. No canonical um.py, private stack or credentials are distributed.

## Corrections to historical remaining-work notes

The original v1 README and early C1/C2 JSON notes predate the posterior/injection/GWTC-3 supplements. Colored-noise trajectories, higher-mode APIs, actual strain, cross-release reconciliation and the supplementary reproductions now exist. Do not repeat them because an old `pending` field survives. The three failed literature fetches were one GW250114 LaTeX archive and two abstract pages, not three unread full articles; the separate C0 addendum states the actual access. Kay-Wald and Milburn remain abstract-only citations here. The conditional finite KMS construction is not their full theorem or a physical Kerr-state construction.

The accompanying C7_REQUIREMENTS_AUDIT.json/.md maps each requested task to measured evidence and explicitly records failed or partial acceptance. The unresolved physical identification and failed calibration are not concealed as packaging work. Further goal-completion review must preserve those distinctions. N/A: no new Lean proof.


## Native SEOB waveform supplement — 2026-09-22T08:07:42.169719+00:00

[REAL — portable numerical reproduction; OPEN — calibrated physical evidence]

`cache/C7_NATIVE_SEOB_WAVEFORM_v1.zip` provides an independent consumer API for the full
SEOB41 waveform with conditional22/44 dephasing. Isolated Python replay passed
144 checks, maximum relative error4.0127806320932996e-16;
six input guards and corrupted-copy rejection passed. Read
`C7_NATIVE_SEOB_WAVEFORM/README.md` and `C7_NATIVE_SEOB_REPLAY_VALIDATION.json`.
The package receipt marked PACKAGED_REPLAY_PENDING is historical; the separate
replay validation above records completion. Source integration/calibration and
high-SNR precision remain open; this supplement does not replace prior packages
or promote their scientific status. Archive SHA256: a368ae336532096297ceb4a7a9554dbb13dc648b8024f770b94183433a1eb09d.
