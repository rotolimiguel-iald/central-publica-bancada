# C7_POSTERIOR_REPRODUCTION v3

NONBLIND, conditional numerical reproduction supplement. This version changes temporary-directory handling, not frozen scientific programs. Historical results retain their original scope and calibration failures. No physical reading is selected. The old README is provenance only; the current bundle overview supersedes its scientific status.

Run `python -B reproduce.py --help` for available stages. Every execution now requires `--work-root /short/work --output-root /short/results`, both outside this package. Supply verified existing inputs with `--source-root /path/to/ORDEM_013_RINGDOWN`, or use the archive-cache/download options explicitly. Inputs are copied to a fresh temporary child, removed in finally on success/failure. Reports and logs survive in output-root. `--prepare-only` checks preparation and removes its temporary tree; it does not leave a prepared work directory.

Windows MAX_PATH: use short roots or enable long paths. No deep-path success is claimed. New cleanup is not a scientific recalibration. Do not run the full injection campaign as part of ORDEM013BIS; C5 is closed. The frozen original numeric replays are preserved in earlier validation receipts. These wrappers can be used independently by a later reviewer.

R-MOD remains [CONJECTURE — management hypothesis, not TGL canon], with Kerr-state and laboratory-partition walls. All catalogue ratios concern the conditional 220 sector with higher Kerr modes; alternatives on the same event are not multiplied. Realization mapping and actual free-source calibration remain OPEN. Occam effects in low-SNR injections are not detections.

Revision v3_1: output-directory preconditions now precede temporary creation; all subsequent preparation is protected by finally. Frozen calculation assets are unchanged.
