[REAL — numerical implementation verification; physical readings remain conditional]

# C1/C6 addendum to the ringdown research delivery

The ten-reading C1 contract is complete and checked against the frozen source
anchors and all 18 saved two-event numerical rows. It distinguishes the supplied
clock, operator, physical bridge, FP-5 scope, distance dependence and atomic
universality condition. Null universal flags are unresolved, not “not excluded”.
The coherent-state initial slope is not an exponential damping rate; propagation
Xi is not a local ringdown shift. No reading was selected.

## Executed upstream implementation comparison

The original pyRing 2.7.0 source distribution was compiled locally, with no source
edits, no system-environment installation and no changes to the frozen C6 code.
Its installed likelihood.pyx was checked byte for byte against the public archive.
The actual compiled loglikelihood and three inverse-covariance functions ran on:

- 9 synthetic Toeplitz cases, with independent determinant checks;
- 6 held-out off-source noise vectors under the existing quotient covariance;
- 270 amplitude integrals for the registered five readings, three mass/spin
  points, three amplitude priors, two detectors and three off-source vectors.

Maximum relative inner-product difference: 7.78393363142e-15.
Maximum projected log-density difference: 1.830369456e-08.
Maximum log-evidence difference: 7.09974301571e-11.
An intentionally omitted determinant differs by 2.46136609387
and is rejected. The independent amplitude oracle convolves a 407-dimensional
data covariance, whereas production solves a 4-dimensional coefficient system.

## What this result does and does not establish

This pays the numerical **implementation** comparison. It does not reproduce the
published posterior under identical priors, modes or preprocessing. Published
pyRing 220/221 posteriors and this 220/440 model remain distinct; the inspected
release has no 10.5 tM posterior. No new on-source strain was read in this test.

The earlier two-family injection calibration still fails its declared bias and
coverage criteria. Its calculations are completed; the required scientific
acceptance is **NOT PASSED**. Agreement between numerical implementations cannot
repair an inadequate waveform model. No frozen measurement, Bayes ratio,
selection, gate, or physical partition was changed. There is no sigma claim.

## Reproduce

From the extracted delivery root, run `python verify_delivery.py`. In
`C1_C6_ADDENDUM`, with the scientific Python environment described by the base
package, execute:

```sh
python -B reproduce.py --download
```

Alternatively supply `--source-archive /path/to/pyRingGW-2.7.0.tar.gz`.
The source is hash-checked. The runner copies frozen inputs to a fresh directory,
builds pyRing and its task-only dependencies there, then runs the oracle without
target strain. An optional `--vendor-cache /path/to/prepared/vendor` reuses the
checked binary; that is explicitly recorded and is not called an independent
compiler run. No original inference sampler is rerun.

The package retains the earlier v1 artifacts and their full scope statements.
This addendum advances C1 documentation and C6 implementation verification; it
does not declare the full research objective or precision requirement complete.
