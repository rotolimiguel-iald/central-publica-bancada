# GWTC-3 posterior and published-selection reproduction

This additive supplement recalculates all 18 released pSEOB posterior readouts,
extracts Table 13 and the two explicit author exclusions from the archived
primary article, and recomputes the separate ten-event combination. It never
multiplies a GWTC-3 likelihood by an overlapping newer-catalog likelihood.

```sh
python reproduce.py full --download
python reproduce.py full --archive-cache /path/to/public
```

The second command expects `17461225/IGWN-GWTC3-TGR-v2-rin.zip`. Alternatively,
`--source-root /path/to/ORDEM_013_RINGDOWN` uses verified extracted members.
Dependencies: NumPy, SciPy, h5py and LAL (UTC/GPS conversion). Tested versions
are recorded in the replay receipt. The archive is about 2.21 GB; the 18 inputs
about 1.23 GB. Provide additional free space for the fresh working directory.
All public files are attributed to LVK, CC BY 4.0; DOI, URLs and hashes are in
MANIFEST.json. The archived article is only read, never executed.

Each run verifies shipped files and public inputs, streams only declared ZIP
members to checked destinations, checks their CRC and SHA-256, then executes
the unchanged analysis scripts. It compares all numerical leaves and all
strings (including event identities and verdicts) in declared result subtrees.
Numerical tolerances are relative 2e-7 and absolute 1e-10; counts are exact.
Logs and failed runs are preserved. Reference target outputs are not inputs.

One explicit comparison input is `C4_CATALOG_220.json`: its event names identify
overlap by GPS, and its old-versus-new numbers populate a comparison column.
Its posterior likelihoods are never included in the GWTC-3 calculation. The
newer-catalog file itself can be regenerated with C7_POSTERIOR_REPRODUCTION.

The historical all-18 control is included under evidence, distinct from the
published ten-event selection. The former is not represented as the paper's
joint result; neither is pooled with the current release. Original executable
versions and remnant-postprocessing provenance are unavailable in the legacy
HDF5. Ratios are conditional on the inspected uniform-prior convention and
matched nuisance priors. The publication selection was audited nonblindly.

The conclusion is INCONCLUSIVE_SYSTEMATICS, not a physical confirmation or a
frequentist sigma. No clock, partition or physical unraveling is selected.
The primary newer catalog remains the preferred analysis on overlapping data.
This supplement does not rerun LVK parameter estimation or independently
validate its waveform or calibration assumptions.
