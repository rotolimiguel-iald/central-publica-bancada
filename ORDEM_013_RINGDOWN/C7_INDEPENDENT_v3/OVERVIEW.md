# Conditional ringdown research package v3

NONBLIND. This is an internal reproducible research handoff, with no selected physical reading. Theory attribution: Luiz Antonio Rotoli Miguel. Original canonical programs and private files are not shipped or modified.

Run `python -B verify_delivery.py` and `python -B -O unit_checks.py` in a scientific Python environment with NumPy. `python -B run_demo.py` is an illustrative waveform, not an observational fit. Dependencies are listed in the requirements files; installation is the recipient's choice.

## Scientific scope, generated from C1/C4/C6-pre

Every catalogue ln B applies to the **conditional 220 sector with higher Kerr modes**, with 440 fixed to GR in 32/33 GWTC5 products (`HIGHER_MODE_DEVIATIONS_FIXED_TO_GR`); GW250114 uses free-440 nuisance parameters. This is not a full multimode deformed likelihood. C4 and C6-pre cover the ensemble only. A detector observes one realization, and the physical unraveling mapping remains OPEN. A universal `realization` prediction returning calibrated mean delta-tau and width of delta-f is NOT PAID; named stochastic demonstrations do not settle that mapping.

`tables/reading_scope.json` and `.csv` contain all ten readings across six datasets, ln B, bands, predicted shifts (5–95% where retained by the source), GR z and HPD, conditional verdicts, nulls and analytic-scenario labels. For catalogues, a weighted median-based prediction is not a new 5–95% posterior interval. Sigma/z are labelled diagnostics, never conversions from ln B. Original current-evidence JSONs retain the per-event intervals and derivations.

| Reading | Status | Conditional rate/exponent | EXCLUDED_IF_UNIVERSAL |
|---|---|---|---|
| R-A | INPUT_PRINCIPLED_IDENTIFICATION | beta*(1+z)*t_P*omega^2/2 | {"excluded_if_universal": null, "excluded_if_universal_P1_matter": false, "excluded_if_universal_P2_independent_arm_light_modes": true} |
| R-B | INPUT_SOURCE_MASS_CLOCK | beta*w(chi)^2/(2*tM) | {"excluded_if_universal": null} |
| R-MOD | CONJECTURE — management hypothesis, not TGL canon | pi*beta*(omega-m*Omega_H)^2/kappa | {"excluded_if_universal": true} |
| R-RAIZ-0 | INPUT_POSITIVE_GENERATOR_AND_VACUUM_COHERENCE | beta*omega/2 | {"excluded_if_universal": true} |
| R-RAIZ-EP4 | INPUT_BACKGROUND_E_P_OVER_4 | beta*omega^2/[2*(sqrt(omega0+omega)+sqrt(omega0))^2] | {"excluded_if_universal": null, "excluded_if_universal_P1_matter": false, "excluded_if_universal_P2_independent_arm_light_modes": true} |
| R-RAIZ-REST | CONJECTURE_REMNANT_REST_OFFSET | beta*omega^2/[2*(sqrt(omega0+omega)+sqrt(omega0))^2] | {"excluded_if_universal": true} |
| R-RAIZ-COHERENT | CONJECTURE_OCCUPATION_AND_READOUT | Gamma_initial=(beta*omega/2)*E_Poisson[1/(sqrt(n+1)+sqrt(n))^2] ~ beta*omega/(8*Nbar) | {"excluded_if_universal": null} |
| R-LIN | CONJECTURE_LINEAR_GAP_PHYSICAL_BRIDGE | beta*omega | {"excluded_if_universal": true} |
| R-GLOBAL | INPUT_RELATIONAL_PARTITION | Gamma_relative=0 | {"excluded_if_universal": null} |
| R-PROP | CONJECTURE_PROPAGATION_MODEL | Xi=(beta*t_P*omega_obs^2/2)*integral_0^z (1+zprime)/H(zprime) dzprime | {"excluded_if_universal": null} |

R-MOD is **[CONJECTURE — management hypothesis, not TGL canon]**. Its positive corotating oscillator is not a global Kerr thermal state. The nonuniversal rule that would distinguish a horizon clock from excluded laboratory clock identifications remains OPEN. The modular double-commutator clock is an additional postulate, not the positive-root generator in disguise. R-RAIZ-0 is a vacuum-to-one-quantum coherence; assigning it to a macroscopic classical strain is a type/observable bridge, not a theorem. Propagation with the source mass clock is dimensionally consistent but requires an unproved rule transporting that clock along the path; a large conditional attenuation is not a local R-B exclusion. H(z) must be supplied explicitly; no cosmology is selected by the propagation function.

Gamma damps ensemble amplitude, not energy. With x=Gamma*tau_GR, delta_tau=-x/(1+x). Beta is ALPHA_FINE_CODATA_2018*sqrt(e) in runtime. The default constants profile is CODATA2018_IAU2015. LEGACY_V346 is a different, non-CODATA/IAU profile; the legacy regression uses `delta_tau_linear`, not the exact additive-rate shift. The exact/BCW comparison and units checks are in current_evidence/C1_NUMERICAL_CONTROLS_v2.json. Non-220 modes require externally supplied exact QNMs and angular factors; no BCW extrapolation is silently used.

Time is seconds, mass detector-frame solar masses, strain dimensionless. Phase is referenced to `t_start`; plus uses cosine and cross sine, with h_plus-i*h_cross the negative-frequency face-on convention. Before onset both polarizations vanish. This supplies arrays for Bilby/PyCBC consumers, not a pyRing likelihood plugin. The C6 timing table records actual detector sample cuts; identical L1 cuts at requested 10 and 10.5 t_M are not independent measurements. C5's common overtone damping convention differs from the per-mode template law; do not conflate them.

The C5 FULL_IMR calibration failed and is closed as a measured wall. MATCHED_RINGDOWN successes are separate closed-set numerical recovery controls. Low-SNR injection tables may have positive mean ln B from prior volume (Occam effect), including null injections; this is not a detection. C6-pre remains a pre-power-gate, uncalibrated nonblind diagnostic; near-zero ln B is not confirmation. Only R-GLOBAL is an exact relational identity in its declared implementation. The old lost template version is not byte-reproducible from its historical checks. The README under historical/ is a dated record superseded here, not current guidance.

## Clean C6-pre reproduction

Provide the two already downloaded public GWOSC files identified in `reproduction/ORDEM_013_RINGDOWN/C6_DOWNLOADS.json`. The wrapper verifies their SHA256 before copying them. It does not download or read any secret configuration.

```sh
python -B reproduce_c6.py
python -B reproduce_c6.py --run --source-cache /path/to/verified/on_source --work-root /short/work --output /short/results/C6_v3.json
```

Output must be outside the package. Every window is computed from verified strain in a fresh temporary directory; saved grids are refused. The wrapper compares numbers and accepts an explicit downgrade to an inconclusive/awaiting-data status; the scientific verdict is not fixed to one token. A numerical match does not calibrate the scientific model. Logs are preserved beside the output and temporaries are removed in finally, including failures. Frozen C6 code and registration are unchanged under reproduction/.

**Windows MAX_PATH:** use a short extraction/work path (for example C:\rdv3) or a long-path-enabled Python/OS. Deep paths can exceed legacy 260-character limits; no deep-path success is claimed. Minimum legacy fixture is `fixtures/legacy_per_series_2.json`, with source hash and selector. Unit checks include exact rate conversion, a=0/a=1, onset, legacy regression and invalid-input refusals, including under Python -O.

## Attribution and evidence

Public observations are by LIGO Scientific Collaboration, Virgo Collaboration and KAGRA Collaboration. Each upstream licence is preserved separately; there is no blanket licence inferred for this research code. GWOSC strain is CC BY 4.0; Zenodo 17018009 is MIT; 21454847 and 17461225 are CC BY 4.0. Source receipts identify those releases. Manifest hashes certify bytes, not proofs. No Lean is executed here and no gate changes. Independent review, calibration and physical interpretation retain the limitations in current_evidence.
