# Public-posterior regeneration supplement

This supplements the immutable independent package v1. It recalculates numerical
results from public posterior samples, not from the reference JSON outputs.
It does not rerun the LVK samplers or claim independent scientific confirmation.

Use Python with NumPy 2.5.3, SciPy 1.18.1 and h5py 3.16.0 (tested versions).
Each command creates a fresh directory under cache, copies only the declared
inputs, verifies hashes, executes the existing analysis scripts unchanged, and
compares all numerical leaves of the declared output subtrees with the reference.
Per-script logs and failed runs are preserved. Counts and verdicts must agree.

```sh
python reproduce.py primary --download
python reproduce.py joint --download
python reproduce.py free_clock --download
python reproduce.py catalog --download
```

Alternatively use `--archive-cache /path/to/public` containing RECORD/filename,
or `--source-root /path/to/ORDEM_013_RINGDOWN` for existing verified extracted
files. About 2.4 GB of source archives are needed for all stages. Files are
attributed to LVK under CC BY 4.0; URLs and member hashes are in MANIFEST.json.
The notebook is parsed only with AST literal_eval, never executed.

These are conditional ensemble/ringdown sector comparisons. The catalog counts
GW250114 once and must not be multiplied by the standalone or joint-mode result.
Older GWTC-3 reconciliation and injection regeneration are separate work; they
are not claimed complete by this supplement. Earlier per-stage JSON status
strings preserve their historical scope; later controls are separate evidence.
Bayes ratios are not sigma. No physical clock or unraveling is selected here.
