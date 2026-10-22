# Conditional IMR recovery extension

This is a **non-blind model-adequacy study**, not a new analysis of observed
GW250114 strain or a physical confirmation. It extends the previous QNM-basis
recovery using full, precomputed IMR harmonic shapes at the same fixed binary
parameters. Both model families, all eight scalar-rate readings and the original
bias/coverage criteria are retained.

## Measured outcome

576 cells, 206 paired held-out noise intervals per cell, O4 and O5 reference
PSDs, injected dephasing amplitudes 0 and 1, and ringdown network SNRs 40, 200,
600. The noise indices 50:256 were not used in the earlier 50-draw forecast;
the same intervals are reused across configurations, not independent events.

For the four identifiable readings, **19 of 24** PSD/reading/SNR groups pass
jointly for both injected amplitudes and both injection families using one
equal-family-mixture likelihood. There are 78 passing individual mixture cells,
76 passing same-family cells and **zero passing opposite-family cells**.
Half of the total cells are below observable precision and claim no calibration.

| PSD | Reading | Ringdown SNR | All four mixture cells |
|---|---|---:|---|
| O4 | R-B | 40 | FAIL |
| O4 | R-B | 200 | PASS |
| O4 | R-B | 600 | PASS |
| O4 | R-RAIZ-0 | 40 | PASS |
| O4 | R-RAIZ-0 | 200 | PASS |
| O4 | R-RAIZ-0 | 600 | PASS |
| O4 | R-LIN | 40 | PASS |
| O4 | R-LIN | 200 | PASS |
| O4 | R-LIN | 600 | PASS |
| O4 | R-MOD | 40 | FAIL |
| O4 | R-MOD | 200 | PASS |
| O4 | R-MOD | 600 | PASS |
| O5 | R-B | 40 | FAIL |
| O5 | R-B | 200 | PASS |
| O5 | R-B | 600 | PASS |
| O5 | R-RAIZ-0 | 40 | FAIL |
| O5 | R-RAIZ-0 | 200 | PASS |
| O5 | R-RAIZ-0 | 600 | PASS |
| O5 | R-LIN | 40 | PASS |
| O5 | R-LIN | 200 | PASS |
| O5 | R-LIN | 600 | PASS |
| O5 | R-MOD | 40 | FAIL |
| O5 | R-MOD | 200 | PASS |
| O5 | R-MOD | 600 | PASS |

## Scope that must accompany these results

The mixture includes the true injection family. Passing within this closed,
two-model set is not evidence that every astrophysical waveform is covered.
Masses, spins, inclination and source phase are fixed to one representative
source. The opposite-family-only failures remain visible. No mass/spin posterior
marginalization or broad source-population validation has been performed here.

Reading B still fails the registered calibration at SNR 40. Its success at SNR
200 or 600 cannot change the frozen C6 verdict at the observed sensitivity.
Positive mean log Bayes ratios also occur for a=0 at low SNR because of the
specified nuisance priors; do not convert them to sigma or claim a detection.

All 22/44 harmonic content receives its fundamental-mode Gamma, and other modes
are unchanged. That deformation, the source mass clock in B, and the ensemble
interpretation remain conditional. Negative amplitudes exist only on a profile
diagnostic grid; the physical point hypotheses are 0 and 1.

## Reproduce

Use Python with NumPy and SciPy. The tested environment is Python 3.12, NumPy
2.5.3 and SciPy 1.18.1. Run:

```sh
python -B reproduce.py
```

The runner verifies every shipped file, creates a fresh directory, recalculates
all 576 cells, and compares identities, statutes and numerical fields plus every
saved draw. It also executes an independent SVD likelihood oracle (96 cells,
288 draw comparisons; measured maximum error 1.0768417269e-09).

This package starts from hash-checked **derived** harmonic arrays and recolored
off-source noise. The earlier `C7_INJECTION_REPRODUCTION` package provides their
production from public raw strain and the actual PyCBC/LAL waveform generators.
The original v1/v2 delivery remains unchanged. No canonical um.py, Lean source,
global memory, real-event result or scientific gate is edited by this study.
